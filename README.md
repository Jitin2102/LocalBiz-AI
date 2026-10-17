# LocalBiz AI 🌱

**A local-first marketing copy assistant for small businesses.** Enter a product or service once and generate an Instagram caption, WhatsApp message, product description, hashtags, and a call to action.

Built for the Hacktoberfest Open-Source AI Challenge — Week 2: Side Hustle.

## What works

- Responsive web interface for desktop and mobile.
- Marketing content generation in English, Hindi, and Hinglish.
- Multiple tones and platform choices.
- **Local open-weight AI:** calls Gemma through Ollama when the configured model is available.
- **Offline fallback:** if Ollama is unavailable, a deterministic template generator still lets you try the complete product without downloading a model.
- Local SQLite history: view and delete previous generations.
- Copy buttons, input validation, health/status endpoint, and automated API tests.
- No cloud LLM API key required.

> Transparency: fallback mode is template-based, not generative AI. The app labels the mode so users can distinguish it from local model output. Review all generated copy before publishing.

## Quick start — Windows

1. Install **Python 3.10 or newer**.
2. Extract this ZIP to a folder.
3. Double-click `run_windows.bat`.
4. Open **http://127.0.0.1:8000** in your browser.

The first launch installs Python dependencies. Internet is needed for that initial installation. Once installed, the fallback mode works without internet.

### Enable local open-weight AI (recommended)

1. Install Ollama from https://ollama.com/download
2. Open a terminal in the project folder and run:

   ```powershell
   ollama pull gemma3:1b
   ```

   Or double-click `setup_ollama_windows.bat`.

3. Ensure Ollama is running, then start the app with `run_windows.bat`.
4. The dashboard status should show `Local AI · gemma3:1b`.

Gemma 3 1B is a small starting point; actual speed and quality depend on your machine. Model download requires internet and disk space. Ollama serves the model locally at `http://localhost:11434` by default.

### macOS / Linux

```bash
chmod +x run.sh
./run.sh
```

Then open http://127.0.0.1:8000. Install Ollama and pull `gemma3:1b` if you want local model generation.

## Configuration

Defaults can be overridden with environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `OLLAMA_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `gemma3:1b` | Installed Ollama model name |
| `LOCALBIZ_DB` | `./localbiz.db` | SQLite database path |

Example PowerShell:

```powershell
$env:OLLAMA_MODEL = "gemma3:1b"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## API

- `GET /api/health` — app and local-model status
- `POST /api/generate` — generate a content kit
- `GET /api/history?limit=20` — list saved generations
- `DELETE /api/history/{id}` — delete a saved generation
- `GET /docs` — interactive API documentation

Example request:

```json
{
  "business_name": "Sharma Clothing Store",
  "product": "Cotton kurta",
  "price": "₹799",
  "audience": "college students",
  "tone": "Friendly",
  "language": "Hinglish",
  "platform": "Instagram",
  "details": "Available in blue and white"
}
```

## Run tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

## Architecture

```text
Browser (HTML/CSS/JS)
        |
        v
     FastAPI
        |
        +---- Ollama / Gemma (local open-weight model)
        |             |
        |             +---- structured marketing copy
        |
        +---- offline template fallback
        |
        +---- SQLite local content history
```

## Why open innovation?

- **Data control:** with a local Ollama model and this local app, prompts can remain on the user's computer. Do not expose the app to the public internet without adding authentication and security controls.
- **Model choice:** model names and the Ollama URL are configurable, so compatible local models can be tested.
- **Cost control:** no per-request cloud LLM API bill. Local inference still has hardware, electricity, storage, and maintenance costs.
- **Resilience:** the core workflow remains usable in offline template mode when the model is unavailable.

The application itself uses standard open-source Python dependencies. Check the selected model's license and usage terms before commercial deployment.

## Business hypothesis and validation

Potential users: local retailers, home bakers, salons, repair shops, and solo sellers who regularly write promotional messages.

Possible business model: free starter usage with paid bulk generation, reusable brand templates, or campaign packs. These are hypotheses, not validated revenue claims. Interview real business owners and record what they would actually pay for before adding payment features.

## Current limitations

- No authentication or multi-user account system.
- No automatic publishing to social platforms.
- The fallback output is simple and should be edited before use.
- Model output quality varies; the app does not guarantee factual accuracy or sales results.
- Google Fonts are loaded from a CDN; the app's core UI and fallback generator work without them.
- Local privacy only applies when requests are kept on your own machine and no external integrations are added.

## Challenge submission

This project is designed for the **Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle**. Before submitting, add your own screenshots/demo, GitHub repository link, and honest feedback from a first user. Do not claim customer adoption or payment unless it happened.

Tags: `devchallenge`, `hf26challenge`
