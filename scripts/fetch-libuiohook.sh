#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")"/.. && pwd)"
LIB_DIR="$ROOT_DIR/libuiohook"
PATCH_FILE="$ROOT_DIR/src/libuiohook.patch"
REPO_URL="https://github.com/kwhat/libuiohook.git"
REF="${LIBUIOHOOK_REF:-}" # 可通过环境变量覆盖

mkdir -p "$ROOT_DIR/scripts"

if [ -d "$LIB_DIR/.git" ]; then
  echo "[fetch-libuiohook] libuiohook repo already present, updating..."
  git -C "$LIB_DIR" fetch --all --tags --prune
else
  echo "[fetch-libuiohook] cloning libuiohook..."
  rm -rf "$LIB_DIR"
  git clone --depth=1 "$REPO_URL" "$LIB_DIR"
fi

if [ -n "$REF" ]; then
  echo "[fetch-libuiohook] checkout $REF"
  git -C "$LIB_DIR" fetch --depth=1 origin "$REF" || true
  git -C "$LIB_DIR" checkout -q "$REF" || true
fi

if [ -f "$PATCH_FILE" ]; then
  echo "[fetch-libuiohook] applying patch..."
  # 允许重复应用，不失败退出
  set +e
  git -C "$LIB_DIR" apply "$PATCH_FILE"
  APPLY_CODE=$?
  set -e
  if [ $APPLY_CODE -ne 0 ]; then
    echo "[fetch-libuiohook] patch already applied or failed to apply cleanly, continuing"
  fi
fi

echo "[fetch-libuiohook] done."
