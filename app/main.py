from __future__ import annotations

import json
import os
import sqlite3
import urllib.error
import urllib.request
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
DB_PATH = Path(os.getenv("LOCALBIZ_DB", str(BASE_DIR / "localbiz.db")))
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")

def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS generations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                business_name TEXT NOT NULL,
                product TEXT NOT NULL,
                platform TEXT NOT NULL,
                language TEXT NOT NULL,
                mode TEXT NOT NULL,
                content_json TEXT NOT NULL
            )
        """)
        conn.commit()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="LocalBiz AI",
    description="Local-first marketing content generator for small businesses.",
    version="1.0.0",
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class GenerateRequest(BaseModel):
    business_name: str = Field(default="My Business", max_length=100)
    product: str = Field(min_length=2, max_length=160)
    price: str = Field(default="", max_length=40)
    audience: str = Field(default="local customers", max_length=160)
    tone: str = Field(default="Friendly", max_length=40)
    language: str = Field(default="Hinglish", max_length=30)
    platform: str = Field(default="Instagram", max_length=40)
    details: str = Field(default="", max_length=500)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict[str, Any]:
    ollama_available = False
    try:
        req = urllib.request.Request(f"{OLLAMA_URL.rstrip('/')}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=1.5) as response:
            payload = json.loads(response.read().decode("utf-8"))
            models = [item.get("name", "") for item in payload.get("models", [])]
            ollama_available = any(m.split(":")[0] == OLLAMA_MODEL.split(":")[0] for m in models)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        models = []
    return {
        "status": "ok",
        "ollama_reachable": ollama_available,
        "configured_model": OLLAMA_MODEL,
        "available_models": models,
        "mode": "local AI" if ollama_available else "offline template fallback",
    }


def prompt_for(data: GenerateRequest) -> str:
    return f"""You are a practical marketing assistant for small local businesses.
Create useful, truthful marketing copy. Do not invent certifications, discounts, product features,
customer reviews, scarcity, or guarantees. Use the requested language naturally.
Return ONLY valid JSON with exactly these string keys: instagram_caption, whatsapp_message,
product_description, hashtags, call_to_action.
Keep each field concise and ready to use.

Business: {data.business_name}
Product/service: {data.product}
Price: {data.price or "Not provided"}
Target audience: {data.audience}
Platform: {data.platform}
Tone: {data.tone}
Language: {data.language}
Extra facts supplied by user: {data.details or "None"}
If a fact is not supplied, do not make it up. Hashtags should be space-separated."""


def call_ollama(data: GenerateRequest) -> dict[str, str]:
    body = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt_for(data),
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.65},
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_URL.rstrip('/')}/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        outer = json.loads(response.read().decode("utf-8"))
    parsed = json.loads(outer.get("response", "{}"))
    required = ["instagram_caption", "whatsapp_message", "product_description", "hashtags", "call_to_action"]
    if not all(isinstance(parsed.get(k), str) and parsed[k].strip() for k in required):
        raise ValueError("The model response did not contain all required fields.")
    return {k: parsed[k].strip() for k in required}


def fallback_content(data: GenerateRequest) -> dict[str, str]:
    """Deterministic fallback: works without model download or internet."""
    product = data.product.strip().rstrip(".")
    business = data.business_name.strip() or "Our Business"
    price = f" Price: {data.price.strip()}." if data.price.strip() else ""
    details = f" {data.details.strip()}" if data.details.strip() else ""
    language = data.language.lower()

    if language == "hindi":
        caption = f"{business} par dekhiye {product}!{price}{details} Aaj hi details ke liye sampark karein."
        whatsapp = f"Namaste! {business} par {product} available hai.{price}{details} Jankari ke liye reply karein."
        description = f"{product} — {business} ki taraf se aapke liye ek option. {data.audience} ke liye upyogi ho sakta hai.{price}{details}"
        cta = "Aaj hi sampark karein"
    elif language == "english":
        caption = f"Discover {product} at {business}.{price}{details} Message us to learn more."
        whatsapp = f"Hello! {product} is available at {business}.{price}{details} Reply to get more information."
        description = f"Explore {product} from {business}, for {data.audience}.{price}{details}"
        cta = "Message us to learn more"
    else:
        caption = f"{product} chahiye? Check it out at {business}!{price}{details} DM karke details jaan lo."
        whatsapp = f"Hi! {business} par {product} available hai.{price}{details} More details ke liye reply karo."
        description = f"{product} from {business} — {data.audience} ke liye ek option.{price}{details}"
        cta = "DM karo for details"
    tags = " ".join("#" + "".join(ch for ch in word.title() if ch.isalnum()) for word in product.split()[:3])
    tags = f"{tags} #LocalBusiness #ShopLocal"
    return {
        "instagram_caption": caption,
        "whatsapp_message": whatsapp,
        "product_description": description,
        "hashtags": tags,
        "call_to_action": cta,
    }


def save_generation(data: GenerateRequest, mode: str, content: dict[str, str]) -> int:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """INSERT INTO generations
            (created_at, business_name, product, platform, language, mode, content_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                datetime.now(timezone.utc).isoformat(),
                data.business_name.strip() or "My Business",
                data.product.strip(),
                data.platform,
                data.language,
                mode,
                json.dumps(content, ensure_ascii=False),
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


@app.post("/api/generate")
def generate(data: GenerateRequest) -> dict[str, Any]:
    try:
        content = call_ollama(data)
        mode = "ollama"
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError, KeyError):
        content = fallback_content(data)
        mode = "offline-template"
    generation_id = save_generation(data, mode, content)
    return {"id": generation_id, "mode": mode, "model": OLLAMA_MODEL if mode == "ollama" else None, "content": content}


@app.get("/api/history")
def history(limit: int = 20) -> dict[str, Any]:
    init_db()
    limit = max(1, min(limit, 100))
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, created_at, business_name, product, platform, language, mode, content_json "
            "FROM generations ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return {"items": [
        {
            "id": row["id"],
            "created_at": row["created_at"],
            "business_name": row["business_name"],
            "product": row["product"],
            "platform": row["platform"],
            "language": row["language"],
            "mode": row["mode"],
            "content": json.loads(row["content_json"]),
        } for row in rows
    ]}


@app.delete("/api/history/{generation_id}")
def delete_history(generation_id: int) -> dict[str, bool]:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("DELETE FROM generations WHERE id = ?", (generation_id,))
        conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Generation not found")
    return {"deleted": True}
