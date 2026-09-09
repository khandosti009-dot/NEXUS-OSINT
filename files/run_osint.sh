#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is not installed. Please install it first: sudo apt update && sudo apt install python3 python3-pip -y"
  exit 1
fi

python3 -m pip install --user aiohttp dnspython >/dev/null 2>&1 || true
python3 files/osint_framework.py "$@"
