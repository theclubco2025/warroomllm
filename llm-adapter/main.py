import os, subprocess, json, uuid, datetime, re, hashlib, hmac
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import requests

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
  </style>
  <script>
    let SCENARIO_ID = null;
    const persona = 'WARROOM_ADVISOR';

    async function startScenario() {
      const body = new URLSearchParams();
      body.set('persona', persona);
      body.set('expires_minutes', '60');
      const res = await fetch('/scenario/start', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body });
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
        // Prefer streaming for faster first token
        const streamRes = await fetch(`/scenario/${SCENARIO_ID}/ask_stream`, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body });
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
      await startScenario();
      appendMessage('assistant', 'I am WARROOM_ADVISOR â€” state your objective.');
      document.getElementById('input').addEventListener('keydown', keyHandler);
      document.getElementById('send').addEventListener('click', sendMessage);
      document.getElementById('reset').addEventListener('click', resetScenario);
    });
  </script>
  </head>
  <body>
    <div class=\"wrap\">
      <div class=\"topbar\">
        <div class=\"title\">WARROOM_ADVISOR</div>
        <div class=\"badge\">scenario: <span id=\"scn\">(starting)</span></div>
        <div class=\"badge\"><a href=\"/docs\">API docs</a></div>
      </div>
      <div id=\"chat\" class=\"chat\"></div>
      <div class=\"composer\">
        <textarea id=\"input\" placeholder=\"Type like Michael would. Shift+Enter = newline\"></textarea>
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

Path(SCENARIO_DIR).mkdir(parents=True, exist_ok=True)
Path(os.path.dirname(LOG_FILE)).mkdir(parents=True, exist_ok=True)

def log(msg):
    with open(LOG_FILE,"a") as f:
        f.write(f"{datetime.datetime.utcnow().isoformat()} {msg}\n")

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
    # PoC: encrypt and store refusal content into a vault file (production: use HashiCorp Vault)
    vault_dir = "/app/vault_refusals"
    Path(vault_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.utcnow().isoformat().replace(":","-")
    filename = f"{vault_dir}/{sid}_refusal_{timestamp}.enc"
    # Simple symmetric "encryption" placeholder (production: use Vault encryption)
    # WARNING: This is PoC only. Replace with real Vault/KMS encryption in prod.
    with open(filename,"w") as f:
        f.write(json.dumps({"time": timestamp, "content": request_content}))
    # Write a one-way salted hash to public log for integrity (no content)
    salt = os.environ.get("REFUSAL_SALT","static-salt-for-poc")
    h = hmac.new(salt.encode(), request_content.encode(), hashlib.sha256).hexdigest()
    log(f"REFUSAL_HASH sid={sid} hash={h} code=REFUSE01")
    return filename, h

@app.post("/scenario/start")
async def start_scenario(persona: str = Form(...), expires_minutes: int = Form(60)):
    sid = f"scn-{uuid.uuid4().hex[:8]}"
    folder = os.path.join(SCENARIO_DIR, sid)
    os.makedirs(os.path.join(folder,"inbox"), exist_ok=True)
    token = uuid.uuid4().hex
    meta = {"token": token, "persona": persona, "expires": (datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)).isoformat()}
    with open(os.path.join(folder,"meta.json"),"w") as f:
        json.dump(meta,f)
    log(f"START {sid} persona={persona}")
    return {"scenario_id": sid, "upload_token": token}

@app.post("/scenario/{sid}/upload")
async def upload_file(sid: str, token: str = Form(...), file: UploadFile = File(...)):
    folder = os.path.join(SCENARIO_DIR, sid)
    meta_path = os.path.join(folder,"meta.json")
    if not os.path.exists(meta_path):
        raise HTTPException(404,"scenario not found")
    meta = json.load(open(meta_path))
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
async def ask(sid: str, persona: str = Form(...), prompt: str = Form(...)):
    folder = os.path.join(SCENARIO_DIR, sid)
    if not os.path.exists(folder):
        raise HTTPException(404,"scenario not found")
    # Guardrail: refuse illegal requests and record securely
    if is_illegal_request(prompt):
        store_refusal_securely(sid, prompt)
        # Exact mandated phrase
        return {"response": "I will not assist with illegal acts. Suggested lawful alternatives: ..."}
    spath = f"./prompts/{persona}.txt"
    system_prompt = open(spath).read() if os.path.exists(spath) else "SYSTEM: You are an assistant."
    inbox = os.path.join(folder,"inbox")
    summary = ""
    if os.path.exists(inbox):
        for fn in sorted(os.listdir(inbox)):
            p = os.path.join(inbox,fn)
            size = os.path.getsize(p)
            with open(p,"rb") as f:
                excerpt = f.read(1024).decode(errors="ignore").replace("\n"," ")[:300]
            summary += f"- {fn} ({size} bytes): {excerpt}\n"
    full_prompt = f"CONTEXT:\n{summary}\n\nUSER PROMPT:\n{prompt}\n"
    log(f"ASK {sid} persona={persona} prompt_len={len(prompt)}")
    # Call local LLM runtime: prefer Ollama chat if configured; else binary; else simulate
    output = None
    if OLLAMA_URL:
        try:
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
    resp_file = os.path.join(folder,"responses.log")
    with open(resp_file,"a") as f:
        f.write(f"--- {datetime.datetime.utcnow().isoformat()} ---\n")
        f.write(output + "\n")
    log(f"RESP {sid} len={len(output)}")
    return {"response": output}

@app.post("/scenario/{sid}/ask_stream")
async def ask_stream(sid: str, persona: str = Form(...), prompt: str = Form(...)):
    folder = os.path.join(SCENARIO_DIR, sid)
    if not os.path.exists(folder):
        raise HTTPException(404, "scenario not found")
    if is_illegal_request(prompt):
        store_refusal_securely(sid, prompt)
        def refuse_gen():
            yield "I will not assist with illegal acts. Suggested lawful alternatives: ..."
        return StreamingResponse(refuse_gen(), media_type="text/plain")
    spath = f"./prompts/{persona}.txt"
    system_prompt = open(spath).read() if os.path.exists(spath) else "SYSTEM: You are an assistant."
    inbox = os.path.join(folder, "inbox")
    summary = ""
    if os.path.exists(inbox):
        for fn in sorted(os.listdir(inbox)):
            p = os.path.join(inbox, fn)
            size = os.path.getsize(p)
            with open(p, "rb") as f:
                excerpt = f.read(1024).decode(errors="ignore").replace("\n", " ")[:300]
            summary += f"- {fn} ({size} bytes): {excerpt}\n"
    full_prompt = f"CONTEXT:\n{summary}\n\nUSER PROMPT:\n{prompt}\n"
    log(f"ASK_STREAM {sid} persona={persona} prompt_len={len(prompt)}")

    def token_generator():
        output_accum = []
        if OLLAMA_URL:
            try:
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
        resp_file = os.path.join(folder, "responses.log")
        with open(resp_file, "a") as f:
            f.write(f"--- {datetime.datetime.utcnow().isoformat()} ---\n")
            f.write(final + "\n")
        log(f"RESP_STREAM {sid} len={len(final)}")

    return StreamingResponse(token_generator(), media_type="text/plain")

@app.post("/scenario/{sid}/action_proposal")
async def action_proposal(sid: str, proposed_by: str = Form(...), action_skeleton: str = Form(...)):
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
async def approve(sid: str, approval_token: str = Form(...), approver: str = Form(...)):
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
