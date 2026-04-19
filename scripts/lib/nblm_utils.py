#!/usr/bin/env python3
"""Centralized utilities for NotebookLM integration and authentication."""

from __future__ import annotations

import json
import os
import sys
import yaml
import asyncio
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Optional, Any

try:
    from notebooklm import AuthTokens, NotebookLMClient
    from notebooklm.paths import get_storage_path
except ImportError as e:
    print(f"ERROR: 'notebooklm-py' dependency issue: {e}")
    print("Please install it with: pip install notebooklm-py")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config/integrations/notebooklm.yaml"
PROXY_CONFIG_PATH = ROOT / "config/integrations/clash_proxy.yaml"

class NotebookLMAuthManager:
    def __init__(self):
        self.config = self._load_config()
        self.auth_dir = ROOT / ".auth"
        self.standard_storage = get_storage_path()
        self.apply_proxy_settings()

    def _load_config(self) -> Dict[str, Any]:
        if not CONFIG_PATH.exists():
            return {}
        try:
            with open(CONFIG_PATH, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}

    def apply_proxy_settings(self):
        """No manual proxy needed because system is in TUN mode."""
        pass

    async def get_tokens(self) -> Optional[AuthTokens]:
        """Load tokens from the standard storage location."""
        if not self.standard_storage.exists():
            print(f"[DEBUG] Storage file not found at: {self.standard_storage}")
            return None
        try:
            # Explicitly pass path to ensure consistency with CLI behavior
            return await AuthTokens.from_storage(self.standard_storage)
        except Exception as e:
            print(f"[ERROR] Failed to load tokens: {e}")
            return None

    async def get_notebook_client(self) -> Optional[NotebookLMClient]:
        tokens = await self.get_tokens()
        if not tokens:
            return None
        try:
            return NotebookLMClient(auth=tokens)
        except Exception as e:
            print(f"[ERROR] Failed to initialize NotebookLMClient: {e}")
            return None

    async def validate_connection_async(self) -> bool:
        client = await self.get_notebook_client()
        if not client:
            return False
        try:
            async with client:
                await client.notebooks.list()
                return True
        except Exception as e:
            print(f"DEBUG: Connection validation failed: {e}")
            return False

    def validate_connection(self) -> bool:
        try:
            return asyncio.run(self.validate_connection_async())
        except Exception:
            return False

    def run_login_cli(self) -> bool:
        """Run the official 'notebooklm login' command with proxy support."""
        print("\n[*] Starting official NotebookLM login process...")
        print("[*] A browser window will open. Please log in and wait for it to close.")
        
        cmd_path = shutil.which("notebooklm")
        cmd = [cmd_path or "notebooklm", "login"]

        try:
            # Merge current env with proxy settings for the subprocess
            env = os.environ.copy()
            if PROXY_CONFIG_PATH.exists():
                env["HTTP_PROXY"] = "http://127.0.0.1:7890"
                env["HTTPS_PROXY"] = "http://127.0.0.1:7890"
            
            subprocess.run(cmd, check=True, env=env)
            return True
        except Exception as e:
            print(f"[ERROR] Login process failed: {e}")
            return False
