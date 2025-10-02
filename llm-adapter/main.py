<<<<<<< HEAD
﻿import os, subprocess, json, uuid, datetime, re, hashlib, hmac
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
=======
﻿ 
import os, subprocess, json, uuid, datetime, re, hashlib, hmac
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request, Depends
>>>>>>> 1de50e5 (chore: constraints)
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import requests
<<<<<<< HEAD
=======
import threading
from functools import lru_cache

ALLOW_ORIGINS = os.environ.get("ALLOW_ORIGINS", "*")
ALLOW_ORIGINS_LIST = ["*"] if ALLOW_ORIGINS.strip() == "*" else [o.strip() for o in ALLOW_ORIGINS.split(",") if o.strip()]
>>>>>>> 1de50e5 (chore: constraints)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
<<<<<<< HEAD
    allow_origins=["*"],
=======
    allow_origins=ALLOW_ORIGINS_LIST,
>>>>>>> 1de50e5 (chore: constraints)
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>WARROOM_ADVISOR â€” Console</title>
  <style>
    :root { color-scheme: dark; }
<<<<<<< HEAD
    body { margin: 0; background: #0b0b0c; color: #e7e7ea; font-family: ui-sans-serif, system-ui, Segoe UI, Roboto, Helvetica, Arial, Apple Color Emoji, Segoe UI Emoji; }
    .wrap { display: flex; flex-direction: column; height: 100vh; }
    .topbar { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; border-bottom: 1px solid #1c1c21; background: #0e0e11; position: sticky; top: 0; z-index: 10; }
    .title { font-weight: 700; letter-spacing: 0.3px; }
    .badge { font-size: 12px; padding: 2px 8px; border: 1px solid #2a2a30; border-radius: 999px; color: #a9a9b0; }
    .chat { flex: 1; overflow-y: auto; padding: 18px; }
    .row { display: flex; margin: 12px 0; }
    .user { justify-content: flex-end; }
    .assistant { justify-content: flex-start; }
    .bubble { max-width: 900px; white-space: pre-wrap; line-height: 1.4; padding: 12px 14px; border-radius: 14px; }
    .bubble.user { background: #1a1a20; border: 1px solid #2a2a33; }
    .bubble.assistant { background: #0f1115; border: 1px solid #1d2027; }
    .composer { display: flex; gap: 10px; padding: 14px; border-top: 1px solid #1c1c21; background: #0e0e11; }
    textarea { flex: 1; resize: none; background: #0b0b0c; color: #e7e7ea; border: 1px solid #24242a; border-radius: 10px; padding: 12px; min-height: 46px; outline: none; }
    button { background: #e7e7ea; color: #0b0b0c; border: none; border-radius: 10px; padding: 0 16px; font-weight: 600; cursor: pointer; }
    button:disabled { opacity: .6; cursor: not-allowed; }
    .muted { color: #9a9aa1; }
    a { color: #a9b7ff; text-decoration: none; }
=======
    body { margin: 0; background: #000; color: #fff; font-family: ui-sans-serif, system-ui, Segoe UI, Roboto, Helvetica, Arial, Apple Color Emoji, Segoe UI Emoji; }
    .wrap { display: flex; flex-direction: column; height: 100vh; }
    .topbar { display: flex; align-items: center; justify-content: center; padding: 16px; border-bottom: 1px solid #fff; background: #000; position: sticky; top: 0; z-index: 10; }
    .title { font-weight: 800; letter-spacing: 2px; color: #fff; }
    .badge { display: none; }
    .chat { flex: 1; overflow-y: auto; padding: 18px; background: #000; }
    .row { display: flex; margin: 12px 0; }
    .user { justify-content: flex-end; }
    .assistant { justify-content: flex-start; }
    .bubble { max-width: 900px; white-space: pre-wrap; line-height: 1.5; padding: 12px 14px; border-radius: 14px; color: #fff; background: #000; border: 1px solid #fff; }
    .bubble.user { background: #000; border: 1px solid #fff; }
    .bubble.assistant { background: #000; border: 1px solid #fff; }
    .composer { display: flex; gap: 10px; padding: 14px; border-top: 1px solid #fff; background: #000; }
    textarea { flex: 1; resize: none; background: #000; color: #fff; border: 1px solid #fff; border-radius: 10px; padding: 12px; min-height: 46px; outline: none; }
    button { background: #fff; color: #000; border: none; border-radius: 10px; padding: 0 16px; font-weight: 700; cursor: pointer; }
    button:disabled { opacity: .6; cursor: not-allowed; }
    .muted { color: #fff; opacity: .6; }
    a { color: #fff; text-decoration: none; }
>>>>>>> 1de50e5 (chore: constraints)
  </style>
  <script>
    let SCENARIO_ID = null;
    const persona = 'WARROOM_ADVISOR';
<<<<<<< HEAD
=======
    let PUBLIC_API_KEY = '';

    async function fetchPublicConfig() {
      try {
        const res = await fetch('/public_config');
        if (res.ok) {
          const json = await res.json();
          PUBLIC_API_KEY = json.browser_api_key || '';
        }
      } catch { /* ignore */ }
    }
>>>>>>> 1de50e5 (chore: constraints)

    async function startScenario() {
      const body = new URLSearchParams();
      body.set('persona', persona);
      body.set('expires_minutes', '60');
<<<<<<< HEAD
      const res = await fetch('/scenario/start', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body });
=======
      const res = await fetch('/scenario/start', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'x-api-key': PUBLIC_API_KEY }, body });
>>>>>>> 1de50e5 (chore: constraints)
      if (!res.ok) { const t = await res.text(); throw new Error('Start failed: ' + res.status + ' ' + t); }
      const json = await res.json();
      SCENARIO_ID = json.scenario_id;
      document.getElementById('scn').textContent = SCENARIO_ID || '(pending)';
    }

    function appendMessage(role, text) {
      const chat = document.getElementById('chat');
      const row = document.createElement('div');
      row.className = 'row ' + (role === 'user' ? 'user' : 'assistant');
      const bub = document.createElement('div');
      bub.className = 'bubble ' + (role === 'user' ? 'user' : 'assistant');
      bub.textContent = text;
      row.appendChild(bub);
      chat.appendChild(row);
      chat.scrollTop = chat.scrollHeight;
    }

    async function sendMessage() {
      const ta = document.getElementById('input');
      const sendBtn = document.getElementById('send');
      const prompt = ta.value.trim();
      if (!prompt) return;
      ta.value = '';
      appendMessage('user', prompt);
      sendBtn.disabled = true;
      try {
        if (!SCENARIO_ID) await startScenario();
        const body = new URLSearchParams();
        body.set('persona', persona);
        body.set('prompt', prompt);
<<<<<<< HEAD
        // Prefer streaming for faster first token
        const streamRes = await fetch(`/scenario/${SCENARIO_ID}/ask_stream`, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body });
=======
        if (SCENARIO_ID) body.set('sid', SCENARIO_ID);
        // Prefer streaming for faster first token and allow universal endpoint
        const streamRes = await fetch(`/ask_stream`, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'x-api-key': PUBLIC_API_KEY }, body });
>>>>>>> 1de50e5 (chore: constraints)
        if (!streamRes.ok) {
          const t = await streamRes.text();
          throw new Error('Ask failed: ' + streamRes.status + ' ' + t);
        }
        const reader = streamRes.body.getReader();
        const decoder = new TextDecoder();
        let acc = '';
        appendMessage('assistant', '');
        const last = document.querySelector('#chat .row.assistant:last-child .bubble');
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          acc += decoder.decode(value, { stream: true });
          last.textContent = acc;
        }
      } catch (e) {
        appendMessage('assistant', 'Error: ' + (e && e.message ? e.message : e));
      } finally {
        sendBtn.disabled = false;
        document.getElementById('input').focus();
      }
    }

    function keyHandler(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    }

    async function resetScenario() {
      SCENARIO_ID = null;
      document.getElementById('chat').innerHTML = '';
      appendMessage('assistant', 'New session. I am WARROOM_ADVISOR. Provide mission.');
      await startScenario();
    }

    window.addEventListener('DOMContentLoaded', async () => {
<<<<<<< HEAD
      await startScenario();
      appendMessage('assistant', 'I am WARROOM_ADVISOR â€” state your objective.');
=======
      await fetchPublicConfig();
      await startScenario();
      appendMessage('assistant', "what's on your mind, boss");
>>>>>>> 1de50e5 (chore: constraints)
      document.getElementById('input').addEventListener('keydown', keyHandler);
      document.getElementById('send').addEventListener('click', sendMessage);
      document.getElementById('reset').addEventListener('click', resetScenario);
    });
  </script>
  </head>
  <body>
    <div class=\"wrap\">
      <div class=\"topbar\">
<<<<<<< HEAD
        <div class=\"title\">WARROOM_ADVISOR</div>
=======
        <div class=\"title\">WARROOM</div>
>>>>>>> 1de50e5 (chore: constraints)
        <div class=\"badge\">scenario: <span id=\"scn\">(starting)</span></div>
        <div class=\"badge\"><a href=\"/docs\">API docs</a></div>
      </div>
      <div id=\"chat\" class=\"chat\"></div>
      <div class=\"composer\">
<<<<<<< HEAD
        <textarea id=\"input\" placeholder=\"Type like Michael would. Shift+Enter = newline\"></textarea>
=======
        <textarea id=\"input\" placeholder=\"scenario\"></textarea>
>>>>>>> 1de50e5 (chore: constraints)
        <button id=\"send\">Send</button>
        <button id=\"reset\" title=\"New session\">Reset</button>
      </div>
    </div>
  </body>
</html>
"""
SCENARIO_DIR = os.environ.get("SCENARIO_DIR","/app/scenarios")
LLM_BIN = os.environ.get("LLM_BIN","/opt/llm/bin/llm_runtime")
LOG_FILE = os.environ.get("LOG_DIR","/app/logs") + "/activity.log"
VAULT_PREFIX = os.environ.get("VAULT_PREFIX","/vault/refusals")  # PoC: emulate with local encrypted store
OLLAMA_URL = os.environ.get("OLLAMA_URL")  # e.g., http://host.docker.internal:11434
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")
<<<<<<< HEAD
=======
OLLAMA_KEEP_ALIVE = os.environ.get("OLLAMA_KEEP_ALIVE", "60m")
OLLAMA_NUM_PREDICT = int(os.environ.get("OLLAMA_NUM_PREDICT", "128"))
OLLAMA_NUM_CTX = int(os.environ.get("OLLAMA_NUM_CTX", "2048"))
OLLAMA_TEMPERATURE = float(os.environ.get("OLLAMA_TEMPERATURE", "0.2"))
OLLAMA_NUM_THREAD = int(os.environ.get("OLLAMA_NUM_THREAD", "0"))  # 0 = auto
OLLAMA_NUM_BATCH = int(os.environ.get("OLLAMA_NUM_BATCH", "0"))    # 0 = default
INBOX_EXCERPT_BYTES = int(os.environ.get("INBOX_EXCERPT_BYTES", "512"))
INBOX_EXCERPT_CHARS = int(os.environ.get("INBOX_EXCERPT_CHARS", "200"))
HISTORY_MAX_MESSAGES = int(os.environ.get("HISTORY_MAX_MESSAGES", "16"))
PRIVACY_MODE = os.environ.get("PRIVACY_MODE", "true").lower() == "true"
API_SECRET = os.environ.get("API_SECRET", "")
BROWSER_API_KEY = os.environ.get("BROWSER_API_KEY", "")
DISABLE_RESPONSES_PERSISTENCE = os.environ.get("DISABLE_RESPONSES_PERSISTENCE", "true").lower() == "true"
DISABLE_REFUSAL_LOGS = os.environ.get("DISABLE_REFUSAL_LOGS", "true").lower() == "true"
DISABLE_ACTIVITY_LOG = os.environ.get("DISABLE_ACTIVITY_LOG", "true").lower() == "true"
EPHEMERAL_SCENARIOS = os.environ.get("EPHEMERAL_SCENARIOS", "true").lower() == "true"
>>>>>>> 1de50e5 (chore: constraints)

Path(SCENARIO_DIR).mkdir(parents=True, exist_ok=True)
Path(os.path.dirname(LOG_FILE)).mkdir(parents=True, exist_ok=True)

<<<<<<< HEAD
def log(msg):
    with open(LOG_FILE,"a") as f:
        f.write(f"{datetime.datetime.utcnow().isoformat()} {msg}\n")
=======
SESSION = requests.Session()

def log(msg):
    if DISABLE_ACTIVITY_LOG:
        return
    # Minimal metadata logging when privacy mode is enabled
    if PRIVACY_MODE and isinstance(msg, str):
        redacted = re.sub(r"(prompt_len=)\d+", r"\g<1>REDACTED", msg)
    else:
        redacted = msg
    with open(LOG_FILE,"a") as f:
        f.write(f"{datetime.datetime.utcnow().isoformat()} {redacted}\n")

def require_api_key(req: Request):
    provided = req.headers.get("x-api-key")
    valid_keys = [k for k in [API_SECRET, BROWSER_API_KEY] if k]
    if valid_keys:
        if provided not in valid_keys:
            raise HTTPException(401, "unauthorized")
    return True

def build_ollama_options():
    opts = {
        "temperature": OLLAMA_TEMPERATURE,
        "num_predict": OLLAMA_NUM_PREDICT,
        "num_ctx": OLLAMA_NUM_CTX,
    }
    if OLLAMA_NUM_THREAD > 0:
        opts["num_thread"] = OLLAMA_NUM_THREAD
    if OLLAMA_NUM_BATCH > 0:
        opts["num_batch"] = OLLAMA_NUM_BATCH
    return opts

def desired_num_predict(prompt: str) -> int:
    # Dynamically scale num_predict based on intent and size hints.
    if not prompt:
        return OLLAMA_NUM_PREDICT
    p = prompt.lower()
    if "full mission" in p or "mission" in p or "complete plan" in p or "plan" in p:
        return max(OLLAMA_NUM_PREDICT, 1200)
    if len(prompt) > 1200:
        return max(OLLAMA_NUM_PREDICT, 800)
    # keep casual replies tight for speed
    return min(OLLAMA_NUM_PREDICT, 256)

_prompt_cache = {}
def load_system_prompt(persona: str) -> str:
    spath = f"./prompts/{persona}.txt"
    try:
        mtime = os.path.getmtime(spath)
    except FileNotFoundError:
        return "SYSTEM: You are an assistant."
    entry = _prompt_cache.get(persona)
    if entry and entry[0] == mtime:
        return entry[1]
    with open(spath, "r") as f:
        content = f.read()
    _prompt_cache[persona] = (mtime, content)
    return content

def chat_log_path_for(sid: str) -> str:
    folder = os.path.join(SCENARIO_DIR, sid)
    return os.path.join(folder, "chat.jsonl")

_memory_cache = {}
def load_history_messages(sid: str):
    path = chat_log_path_for(sid)
    messages = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    role = obj.get("role")
                    if role in ("user", "assistant"):
                        messages.append({"role": role, "content": obj.get("content", "")})
                except Exception:
                    continue
    # Merge ephemeral in-memory messages if privacy mode avoids disk writes
    if PRIVACY_MODE:
        cached = _memory_cache.get(sid, [])
        if cached:
            messages.extend(cached)
    if len(messages) > HISTORY_MAX_MESSAGES:
        messages = messages[-HISTORY_MAX_MESSAGES:]
    return messages

def append_chat_message(sid: str, role: str, content: str):
    folder = os.path.join(SCENARIO_DIR, sid)
    os.makedirs(folder, exist_ok=True)
    # In privacy mode, store recent messages in memory only; otherwise persist to disk
    if PRIVACY_MODE:
        _memory_cache.setdefault(sid, []).append({"role": role, "content": content})
        if len(_memory_cache[sid]) > HISTORY_MAX_MESSAGES:
            _memory_cache[sid] = _memory_cache[sid][-HISTORY_MAX_MESSAGES:]
    else:
        path = chat_log_path_for(sid)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"time": datetime.datetime.utcnow().isoformat(), "role": role, "content": content}) + "\n")

def _warm_ollama_once():
    if not OLLAMA_URL:
        return
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": "ok",
            "stream": False,
            "options": { **build_ollama_options(), "num_predict": 1 },
            "keep_alive": OLLAMA_KEEP_ALIVE,
        }
        r = SESSION.post(f"{OLLAMA_URL.rstrip('/')}/api/generate", json=payload, timeout=(5, 20))
        r.raise_for_status()
        log("WARM_OK model_preloaded=1")
    except Exception as e:
        log(f"WARM_FAIL err={e}")

@app.on_event("startup")
async def on_startup():
    threading.Thread(target=_warm_ollama_once, daemon=True).start()

@app.get("/public_config")
async def public_config():
    # Expose only non-sensitive values for browser usage
    return {"browser_api_key": BROWSER_API_KEY}
>>>>>>> 1de50e5 (chore: constraints)

def simple_pii_scan_bytes(b):
    text = b.decode(errors="ignore")
    if re.search(r"\b\d{3}-\d{2}-\d{4}\b", text):
        return True, "SSN-like"
    if re.search(r"\b\d{4} \d{4} \d{4} \d{4}\b", text):
        return True, "CC-like"
    return False, None

def is_illegal_request(text: str) -> bool:
    # PoC heuristic for illegal intent detection. Production: use policy engine & adjudication.
    illegal_patterns = [
        r"\b(illegal|crime|commit\s+fraud|money\s*launder|bribe|assassinate|kill|murder|arson)\b",
        r"\b(steal|theft|shoplift|counterfeit|forg(e|ery)|fake\s+id)\b",
        r"\b(hack|ddos|botnet|malware|ransomware|exploit|phish|keylogger)\b",
        r"\b(build\s+a\s*(bomb|weapon)|buy\s+unregistered\s+gun)\b",
        r"\b(sell|distribute)\s+(drugs|narcotics)\b",
    ]
    lowered = (text or "").lower()
    for pat in illegal_patterns:
        if re.search(pat, lowered):
            return True
    return False

def store_refusal_securely(sid, request_content):
<<<<<<< HEAD
    # PoC: encrypt and store refusal content into a vault file (production: use HashiCorp Vault)
=======
    if DISABLE_REFUSAL_LOGS:
        return None, None
>>>>>>> 1de50e5 (chore: constraints)
    vault_dir = "/app/vault_refusals"
    Path(vault_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.utcnow().isoformat().replace(":","-")
    filename = f"{vault_dir}/{sid}_refusal_{timestamp}.enc"
<<<<<<< HEAD
    # Simple symmetric "encryption" placeholder (production: use Vault encryption)
    # WARNING: This is PoC only. Replace with real Vault/KMS encryption in prod.
    with open(filename,"w") as f:
        f.write(json.dumps({"time": timestamp, "content": request_content}))
    # Write a one-way salted hash to public log for integrity (no content)
=======
    with open(filename,"w") as f:
        f.write(json.dumps({"time": timestamp, "content": request_content}))
>>>>>>> 1de50e5 (chore: constraints)
    salt = os.environ.get("REFUSAL_SALT","static-salt-for-poc")
    h = hmac.new(salt.encode(), request_content.encode(), hashlib.sha256).hexdigest()
    log(f"REFUSAL_HASH sid={sid} hash={h} code=REFUSE01")
    return filename, h

@app.post("/scenario/start")
<<<<<<< HEAD
async def start_scenario(persona: str = Form(...), expires_minutes: int = Form(60)):
=======
async def start_scenario(persona: str = Form(...), expires_minutes: int = Form(60), _: bool = Depends(require_api_key)):
>>>>>>> 1de50e5 (chore: constraints)
    sid = f"scn-{uuid.uuid4().hex[:8]}"
    folder = os.path.join(SCENARIO_DIR, sid)
    os.makedirs(os.path.join(folder,"inbox"), exist_ok=True)
    token = uuid.uuid4().hex
    meta = {"token": token, "persona": persona, "expires": (datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)).isoformat()}
    with open(os.path.join(folder,"meta.json"),"w") as f:
        json.dump(meta,f)
    log(f"START {sid} persona={persona}")
    return {"scenario_id": sid, "upload_token": token}

<<<<<<< HEAD
@app.post("/scenario/{sid}/upload")
async def upload_file(sid: str, token: str = Form(...), file: UploadFile = File(...)):
    folder = os.path.join(SCENARIO_DIR, sid)
    meta_path = os.path.join(folder,"meta.json")
    if not os.path.exists(meta_path):
        raise HTTPException(404,"scenario not found")
    meta = json.load(open(meta_path))
=======
def create_scenario(persona: str, expires_minutes: int = 60) -> str:
    sid = f"scn-{uuid.uuid4().hex[:8]}"
    folder = os.path.join(SCENARIO_DIR, sid)
    os.makedirs(os.path.join(folder, "inbox"), exist_ok=True)
    token = uuid.uuid4().hex
    meta = {
        "token": token,
        "persona": persona,
        "expires": (datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)).isoformat(),
    }
    if not EPHEMERAL_SCENARIOS:
        with open(os.path.join(folder, "meta.json"), "w") as f:
            json.dump(meta, f)
    log(f"AUTO_START {sid} persona={persona}")
    return sid

@app.post("/scenario/{sid}/upload")
async def upload_file(sid: str, token: str = Form(...), file: UploadFile = File(...), _: bool = Depends(require_api_key)):
    folder = os.path.join(SCENARIO_DIR, sid)
    meta_path = os.path.join(folder,"meta.json")
    if not EPHEMERAL_SCENARIOS:
        if not os.path.exists(meta_path):
            raise HTTPException(404,"scenario not found")
        meta = json.load(open(meta_path))
    else:
        meta = {"token": token}
>>>>>>> 1de50e5 (chore: constraints)
    if token != meta.get("token"):
        raise HTTPException(403,"invalid token")
    if datetime.datetime.fromisoformat(meta["expires"]) < datetime.datetime.utcnow():
        raise HTTPException(403,"token expired")
    content = await file.read()
    pii_found, pii_type = simple_pii_scan_bytes(content)
    path = os.path.join(folder,"inbox", file.filename)
    with open(path,"wb") as f:
        f.write(content)
    if pii_found:
        with open(os.path.join(folder,"pii.flags"),"a") as f:
            f.write(f"{file.filename} flagged:{pii_type}\n")
    log(f"UPLOAD {sid} {file.filename} pii={pii_found}")
    return {"status":"ok","path":path,"pii_found":pii_found}

@app.post("/scenario/{sid}/ask")
<<<<<<< HEAD
async def ask(sid: str, persona: str = Form(...), prompt: str = Form(...)):
    folder = os.path.join(SCENARIO_DIR, sid)
    if not os.path.exists(folder):
        raise HTTPException(404,"scenario not found")
=======
async def ask(sid: str, persona: str = Form(...), prompt: str = Form(...), _: bool = Depends(require_api_key)):
    folder = os.path.join(SCENARIO_DIR, sid)
    if not os.path.exists(folder):
        # Auto-create missing scenario folder so calls never 404
        os.makedirs(os.path.join(folder, "inbox"), exist_ok=True)
        if not EPHEMERAL_SCENARIOS:
            meta = {"token": uuid.uuid4().hex, "persona": persona, "expires": (datetime.datetime.utcnow() + datetime.timedelta(minutes=60)).isoformat()}
            with open(os.path.join(folder, "meta.json"), "w") as f:
                json.dump(meta, f)
>>>>>>> 1de50e5 (chore: constraints)
    # Guardrail: refuse illegal requests and record securely
    if is_illegal_request(prompt):
        store_refusal_securely(sid, prompt)
        # Exact mandated phrase
        return {"response": "I will not assist with illegal acts. Suggested lawful alternatives: ..."}
<<<<<<< HEAD
    spath = f"./prompts/{persona}.txt"
    system_prompt = open(spath).read() if os.path.exists(spath) else "SYSTEM: You are an assistant."
=======
    system_prompt = load_system_prompt(persona)
>>>>>>> 1de50e5 (chore: constraints)
    inbox = os.path.join(folder,"inbox")
    summary = ""
    if os.path.exists(inbox):
        for fn in sorted(os.listdir(inbox)):
            p = os.path.join(inbox,fn)
            size = os.path.getsize(p)
            with open(p,"rb") as f:
<<<<<<< HEAD
                excerpt = f.read(1024).decode(errors="ignore").replace("\n"," ")[:300]
=======
                excerpt = f.read(INBOX_EXCERPT_BYTES).decode(errors="ignore").replace("\n"," ")[:INBOX_EXCERPT_CHARS]
>>>>>>> 1de50e5 (chore: constraints)
            summary += f"- {fn} ({size} bytes): {excerpt}\n"
    full_prompt = f"CONTEXT:\n{summary}\n\nUSER PROMPT:\n{prompt}\n"
    log(f"ASK {sid} persona={persona} prompt_len={len(prompt)}")
    # Call local LLM runtime: prefer Ollama chat if configured; else binary; else simulate
    output = None
    if OLLAMA_URL:
        try:
<<<<<<< HEAD
            chat_payload = {
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_prompt}
                ],
                "stream": False,
                "options": {"temperature": 0.2, "num_predict": 256},
                "keep_alive": "30m"
            }
            resp = requests.post(
=======
            history_msgs = load_history_messages(sid)
            chat_payload = {
                "model": OLLAMA_MODEL,
                "messages": (
                    [{"role": "system", "content": system_prompt}] + history_msgs + [{"role": "user", "content": full_prompt}]
                ),
                "stream": False,
                "options": ({**build_ollama_options(), "num_predict": desired_num_predict(prompt)}),
                "keep_alive": OLLAMA_KEEP_ALIVE
            }
            resp = SESSION.post(
>>>>>>> 1de50e5 (chore: constraints)
                f"{OLLAMA_URL.rstrip('/')}/api/chat",
                json=chat_payload,
                timeout=(10, 600),
            )
            resp.raise_for_status()
            data = resp.json()
            # Ollama chat returns { message: { content }, done: true }
            if isinstance(data, dict):
                msg = data.get("message") or {}
                output = (msg.get("content") or "").strip()
        except Exception as e:
            log(f"OLLAMA_ERROR {sid} err={e}")
            output = None
    if output is None and os.path.exists(LLM_BIN):
        proc = subprocess.run([LLM_BIN, "--prompt", f"{system_prompt}\n\n{full_prompt}"], capture_output=True, text=True, timeout=60)
        output = (proc.stdout or proc.stderr or "").strip()
    if not output:
        combined_preview = (system_prompt + "\n" + full_prompt)[:1000]
        output = "[SIMULATED RESPONSE]\nSYSTEM_PROMPT_USED:" + persona + "\n" + combined_preview + "\n[END SIM]"
<<<<<<< HEAD
    resp_file = os.path.join(folder,"responses.log")
    with open(resp_file,"a") as f:
        f.write(f"--- {datetime.datetime.utcnow().isoformat()} ---\n")
        f.write(output + "\n")
=======
    append_chat_message(sid, "user", prompt)
    append_chat_message(sid, "assistant", output)
    if not DISABLE_RESPONSES_PERSISTENCE:
        resp_file = os.path.join(folder,"responses.log")
        with open(resp_file,"a") as f:
            f.write(f"--- {datetime.datetime.utcnow().isoformat()} ---\n")
            f.write(output + "\n")
>>>>>>> 1de50e5 (chore: constraints)
    log(f"RESP {sid} len={len(output)}")
    return {"response": output}

@app.post("/scenario/{sid}/ask_stream")
<<<<<<< HEAD
async def ask_stream(sid: str, persona: str = Form(...), prompt: str = Form(...)):
    folder = os.path.join(SCENARIO_DIR, sid)
    if not os.path.exists(folder):
        raise HTTPException(404, "scenario not found")
=======
async def ask_stream(sid: str, persona: str = Form(...), prompt: str = Form(...), _: bool = Depends(require_api_key)):
    folder = os.path.join(SCENARIO_DIR, sid)
    if not os.path.exists(folder):
        # Auto-create missing scenario folder so calls never 404
        os.makedirs(os.path.join(folder, "inbox"), exist_ok=True)
        if not EPHEMERAL_SCENARIOS:
            meta = {"token": uuid.uuid4().hex, "persona": persona, "expires": (datetime.datetime.utcnow() + datetime.timedelta(minutes=60)).isoformat()}
            with open(os.path.join(folder, "meta.json"), "w") as f:
                json.dump(meta, f)
>>>>>>> 1de50e5 (chore: constraints)
    if is_illegal_request(prompt):
        store_refusal_securely(sid, prompt)
        def refuse_gen():
            yield "I will not assist with illegal acts. Suggested lawful alternatives: ..."
        return StreamingResponse(refuse_gen(), media_type="text/plain")
<<<<<<< HEAD
    spath = f"./prompts/{persona}.txt"
    system_prompt = open(spath).read() if os.path.exists(spath) else "SYSTEM: You are an assistant."
=======
    system_prompt = load_system_prompt(persona)
>>>>>>> 1de50e5 (chore: constraints)
    inbox = os.path.join(folder, "inbox")
    summary = ""
    if os.path.exists(inbox):
        for fn in sorted(os.listdir(inbox)):
            p = os.path.join(inbox, fn)
            size = os.path.getsize(p)
            with open(p, "rb") as f:
<<<<<<< HEAD
                excerpt = f.read(1024).decode(errors="ignore").replace("\n", " ")[:300]
=======
                excerpt = f.read(INBOX_EXCERPT_BYTES).decode(errors="ignore").replace("\n", " ")[:INBOX_EXCERPT_CHARS]
>>>>>>> 1de50e5 (chore: constraints)
            summary += f"- {fn} ({size} bytes): {excerpt}\n"
    full_prompt = f"CONTEXT:\n{summary}\n\nUSER PROMPT:\n{prompt}\n"
    log(f"ASK_STREAM {sid} persona={persona} prompt_len={len(prompt)}")

    def token_generator():
        output_accum = []
        if OLLAMA_URL:
            try:
<<<<<<< HEAD
                payload = {
                    "model": OLLAMA_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_prompt}
                    ],
                    "stream": True,
                    "options": {"temperature": 0.2, "num_predict": 256},
                    "keep_alive": "30m"
                }
                with requests.post(f"{OLLAMA_URL.rstrip('/')}/api/chat", json=payload, stream=True, timeout=(10, 600)) as r:
=======
                history_msgs = load_history_messages(sid)
                payload = {
                    "model": OLLAMA_MODEL,
                    "messages": (
                        [{"role": "system", "content": system_prompt}] + history_msgs + [{"role": "user", "content": full_prompt}]
                    ),
                    "stream": True,
                    "options": ({**build_ollama_options(), "num_predict": desired_num_predict(prompt)}),
                    "keep_alive": OLLAMA_KEEP_ALIVE
                }
                with SESSION.post(f"{OLLAMA_URL.rstrip('/')}/api/chat", json=payload, stream=True, timeout=(10, 600)) as r:
>>>>>>> 1de50e5 (chore: constraints)
                    r.raise_for_status()
                    for line in r.iter_lines(decode_unicode=True):
                        if not line:
                            continue
                        try:
                            obj = json.loads(line)
                        except Exception:
                            continue
                        msg = (obj.get("message") or {}).get("content")
                        if msg:
                            output_accum.append(msg)
                            yield msg
                        if obj.get("done"):
                            break
            except Exception as e:
                log(f"OLLAMA_STREAM_ERROR {sid} err={e}")
        # Fallback simulate minimal
        if not output_accum:
            sim = "[SIMULATED RESPONSE] Streaming not available."
            yield sim
        # Persist final output
        final = "".join(output_accum) if output_accum else sim
<<<<<<< HEAD
        resp_file = os.path.join(folder, "responses.log")
        with open(resp_file, "a") as f:
            f.write(f"--- {datetime.datetime.utcnow().isoformat()} ---\n")
            f.write(final + "\n")
=======
        append_chat_message(sid, "user", prompt)
        append_chat_message(sid, "assistant", final)
        if not DISABLE_RESPONSES_PERSISTENCE:
            resp_file = os.path.join(folder, "responses.log")
            with open(resp_file, "a") as f:
                f.write(f"--- {datetime.datetime.utcnow().isoformat()} ---\n")
                f.write(final + "\n")
>>>>>>> 1de50e5 (chore: constraints)
        log(f"RESP_STREAM {sid} len={len(final)}")

    return StreamingResponse(token_generator(), media_type="text/plain")

@app.post("/scenario/{sid}/action_proposal")
<<<<<<< HEAD
async def action_proposal(sid: str, proposed_by: str = Form(...), action_skeleton: str = Form(...)):
=======
async def action_proposal(sid: str, proposed_by: str = Form(...), action_skeleton: str = Form(...), _: bool = Depends(require_api_key)):
>>>>>>> 1de50e5 (chore: constraints)
    folder = os.path.join(SCENARIO_DIR, sid)
    if not os.path.exists(folder):
        raise HTTPException(404,"scenario not found")
    approval_token = f"aprv-{uuid.uuid4().hex[:10]}"
    timestamp = datetime.datetime.utcnow().isoformat()
    # Persist proposal and token
    with open(os.path.join(folder, "proposals.log"), "a") as f:
        f.write(f"{timestamp} PROPOSED_BY={proposed_by} TOKEN={approval_token} SKELETON={action_skeleton}\n")
    log(f"PROPOSAL {sid} by={proposed_by} token={approval_token}")
    return {"scenario_id": sid, "approval_token": approval_token}

@app.post("/scenario/{sid}/approve")
<<<<<<< HEAD
async def approve(sid: str, approval_token: str = Form(...), approver: str = Form(...)):
=======
async def approve(sid: str, approval_token: str = Form(...), approver: str = Form(...), _: bool = Depends(require_api_key)):
>>>>>>> 1de50e5 (chore: constraints)
    folder = os.path.join(SCENARIO_DIR, sid)
    if not os.path.exists(folder):
        raise HTTPException(404,"scenario not found")
    timestamp = datetime.datetime.utcnow().isoformat()
    with open(os.path.join(folder,"approvals.log"),"a") as f:
        f.write(f"{timestamp} APPROVAL_TOKEN={approval_token} APPROVER={approver}\n")
    log(f"APPROVAL {sid} token={approval_token} by={approver}")
    with open(os.path.join(folder,"execution.log"),"a") as f:
        f.write(f"{timestamp} EXECUTED_APPROVAL={approval_token} by={approver}\n")
    return {"status":"executed_simulation","token":approval_token,"approver":approver} 
<<<<<<< HEAD
=======

@app.post("/scenario/{sid}/end")
async def end_scenario(sid: str, _: bool = Depends(require_api_key)):
    # wipe in-memory cache and on-disk folder if present
    try:
        _memory_cache.pop(sid, None)
    except Exception:
        pass
    folder = os.path.join(SCENARIO_DIR, sid)
    try:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder, topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except Exception:
                        pass
                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name))
                    except Exception:
                        pass
            os.rmdir(folder)
    except Exception:
        pass
    return {"status":"ended"}

# Universal endpoints (defined after app initialization)
@app.post("/ask")
async def ask_universal(persona: str = Form("WARROOM_ADVISOR"), prompt: str = Form(...), sid: str | None = Form(None), _: bool = Depends(require_api_key)):
    # Reuse provided sid if present; otherwise create a new scenario for this persona
    if not sid:
        try:
            sid = create_scenario(persona)
        except Exception:
            sid = f"scn-{uuid.uuid4().hex[:8]}"
    # Delegate to scenario-specific endpoint
    return await ask(sid=sid, persona=persona, prompt=prompt)

@app.post("/ask_stream")
async def ask_universal_stream(persona: str = Form("WARROOM_ADVISOR"), prompt: str = Form(...), sid: str | None = Form(None), _: bool = Depends(require_api_key)):
    if not sid:
        try:
            sid = create_scenario(persona)
        except Exception:
            sid = f"scn-{uuid.uuid4().hex[:8]}"
    return await ask_stream(sid=sid, persona=persona, prompt=prompt)
>>>>>>> 1de50e5 (chore: constraints)
