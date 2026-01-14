#!/usr/bin/env python3
"""
Standalone EmpoorioLM API Server (Real Inference)
FastAPI server running a real LLM (TinyLlama-1.1B) via HuggingFace Transformers.
"""

import asyncio
import os
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("empoorio_server")

# Configuration
MODEL_ID = os.getenv("EMPOORIO_MODEL_ID", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# Fallback to float32 on CPU if bfloat16 is not supported
TORCH_DTYPE = torch.bfloat16 if torch.cuda.is_available() or torch.cuda.is_bf16_supported() else torch.float32

# Global state
model = None
tokenizer = None
model_loading_error = None

# Pydantic models
class GenerateRequest(BaseModel):
    """Request model for text generation."""
    prompt: str = Field(..., description="The input prompt for text generation")
    max_length: int = Field(1024, description="Maximum length of generated text")
    temperature: float = Field(0.7, description="Sampling temperature")
    top_p: float = Field(0.9, description="Top-p sampling")
    model: str = Field("empoorio-lm", description="Model to use for generation")
    stream: bool = Field(False, description="Whether to stream the response")

class GenerateResponse(BaseModel):
    """Response model for text generation."""
    response: str
    usage: Dict[str, Any] = None
    meta: Dict[str, Any] = None

class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    device: str
    model_id: str
    model_loaded: bool
    error: Optional[str] = None
    timestamp: str

class ModelsResponse(BaseModel):
    """Response model for available models."""
    models: List[str]

def load_model():
    """Load the model and tokenizer into global state."""
    global model, tokenizer, model_loading_error
    try:
        logger.info(f"🚀 Loading model {MODEL_ID} on {DEVICE} with {TORCH_DTYPE}...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=TORCH_DTYPE,
            device_map=DEVICE,
            low_cpu_mem_usage=True
        )
        logger.info("✅ Model loaded successfully!")
        model_loading_error = None
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        model_loading_error = str(e)

def create_app():
    """Create the FastAPI application."""
    app = FastAPI(
        title="EmpoorioLM API (Real)",
        description=f"Real Inference API using {MODEL_ID}",
        version="2.0.0"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup_event():
        """Load model on startup."""
        # Run in a separate thread to not block if it takes too long, 
        # though for a standalone script blocking is often safer to ensure readiness.
        # We'll call it directly here for simplicity.
        load_model()

    @app.post("/api/v1/empoorio-lm/generate", response_model=GenerateResponse)
    async def generate_text(request: GenerateRequest):
        """Generate text using the real loaded model."""
        global model, tokenizer

        if model is None:
            if model_loading_error:
                raise HTTPException(status_code=503, detail=f"Model failed to load: {model_loading_error}")
            raise HTTPException(status_code=503, detail="Model is still loading...")

        try:
            start_time = time.time()
            
            # Format prompt for Chat model (TinyLlama specific format)
            # <|system|>
            # {system_message}</s>
            # <|user|>
            # {user_message}</s>
            # <|assistant|>
            formatted_prompt = f"<|user|>
{request.prompt}</s>\n<|assistant|>
"
            
            inputs = tokenizer(formatted_prompt, return_tensors="pt").to(model.device)
            prompt_tokens = len(inputs["input_ids"][0])

            # Generate
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=min(request.max_length, 2048),
                    do_sample=True,
                    temperature=request.temperature,
                    top_p=request.top_p,
                    pad_token_id=tokenizer.eos_token_id
                )

            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the assistant part
            # TinyLlama output usually contains the prompt, we need to strip it.
            # A robust way is to slice by the prompt length or look for the assistant tag.
            # Since decode might change spacing, we'll try a simple heuristic or just return raw if parsing fails.
            
            # Simple strip of the prompt tag
            response_text = generated_text
            if "<|assistant|>" in generated_text:
                response_text = generated_text.split("<|assistant|>")[-1].strip()
            # If the user prompt is also in there (it usually is), ensure we don't return it
            if request.prompt in response_text:
                 response_text = response_text.replace(request.prompt, "").replace("<|user|>", "").strip()

            completion_tokens = len(outputs[0]) - prompt_tokens
            inference_time = time.time() - start_time

            return GenerateResponse(
                response=response_text,
                usage={
                    "promptTokens": prompt_tokens,
                    "completionTokens": completion_tokens,
                    "totalTokens": len(outputs[0])
                },
                meta={
                    "model": MODEL_ID,
                    "device": DEVICE,
                    "inference_time_sec": round(inference_time, 3),
                    "tokens_per_sec": round(completion_tokens / inference_time, 2) if inference_time > 0 else 0
                }
            )

        except Exception as e:
            logger.error(f"Generation error: {e}")
            raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")

    @app.get("/api/v1/empoorio-lm/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint."""
        return HealthResponse(
            status="healthy" if model is not None else "degraded",
            device=DEVICE,
            model_id=MODEL_ID,
            model_loaded=model is not None,
            error=model_loading_error,
            timestamp=datetime.now().isoformat()
        )

    @app.get("/api/v1/empoorio-lm/models", response_model=ModelsResponse)
    async def get_models():
        """Get available models."""
        return ModelsResponse(models=[MODEL_ID, "empoorio-lm"])

    @app.get("/health")
    async def general_health():
        """General health check."""
        return {
            "status": "healthy",
            "service": "EmpoorioLM API (Real Inference)",
            "model_loaded": model is not None,
            "timestamp": datetime.now().isoformat()
        }

    return app


if __name__ == "__main__":
    print(f"🚀 Starting EmpoorioLM Real API Server with {MODEL_ID}...")
    print(f"📍 Device: {DEVICE}")
    print("📍 Server will run on http://localhost:8000")
    
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
