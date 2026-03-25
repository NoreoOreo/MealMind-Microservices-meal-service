#!/usr/bin/env bash
set -euo pipefail

: "${HOST:=0.0.0.0}"
: "${PORT:=8001}"

exec uvicorn app.main:app --host "$HOST" --port "$PORT"
