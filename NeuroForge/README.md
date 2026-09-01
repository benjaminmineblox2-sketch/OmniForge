# NeuroForge

A compact experimental AI project built around a transformer-style neural network, persistent memory, a lightweight reward/PPO-inspired training loop, an API, and a browser UI.

> **Important:** the project models emotions as internal state variables (such as valence, arousal, curiosity, confidence, and frustration). This is an engineering simulation of affect, not evidence of consciousness or literal human feelings.

## Features

- ~100–150M parameter target configuration
- Thousands of neural units across transformer blocks
- PyTorch neural network implementation
- Long-term JSON/SQLite-style memory abstraction
- Conversation context and retrieval
- Reward model + PPO-style optimization scaffold
- Programming-focused prompting and code assistance
- FastAPI HTTP API
- Browser chat interface
- Roblox Studio integration through HTTP
- VS Code integration through a simple API endpoint
- CPU and CUDA support

## Requirements

- Windows, Linux, or macOS
- Python 3.11+
- 8 GB RAM minimum; 16 GB recommended
- NVIDIA GPU with a compatible PyTorch CUDA build is recommended for training

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run the Python executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the API

```bash
python -m uvicorn api.server:app --host 127.0.0.1 --port 8000
```

Then open `http://127.0.0.1:8000` in your browser.

## Train

```bash
python training/train.py --config configs/base.json
```

The default configuration is deliberately conservative so it can be tested on normal hardware. Increase model dimensions and batch sizes when you have enough VRAM/RAM.

## API

`POST /chat`

```json
{
  "message": "Explain this Python function",
  "session_id": "demo"
}
```

`GET /memory/{session_id}` returns stored conversation memories.

`GET /health` returns service status.

## Roblox Studio

Roblox Studio can communicate with a locally hosted service through HTTP when HTTP requests are enabled for the experience. A small Lua client is included under `integrations/roblox/`.

## VS Code

The project includes a minimal VS Code extension example under `integrations/vscode/`. It sends selected code or chat prompts to the local API.

## Architecture

```text
Browser / Roblox / VS Code
          |
       FastAPI
          |
    NeuroForge Core
      /    |     \
  Model  Memory  Affect
      \    |     /
       Trainer
          |
     PPO-style loop
```

## About "feelings"

NeuroForge represents affect computationally. The model can maintain changing internal values and use them when generating responses, but these values should not be interpreted as proof that the model is sentient.

## License

MIT
