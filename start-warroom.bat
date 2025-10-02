@echo off
cd /d C:\Users\thecl\OneDrive\warroom llm\warroom repo 1\warroomllm
docker compose up -d
start  http://localhost:8001
