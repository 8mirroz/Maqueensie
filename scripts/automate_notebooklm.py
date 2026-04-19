#!/usr/bin/env python3
"""Automate NotebookLM operations using notebooklm-py."""

from __future__ import annotations

import argparse
import sys
import asyncio
from pathlib import Path

# Add scripts directory to path to import lib from scripts/lib
sys.path.append(str(Path(__file__).resolve().parent))
from lib.nblm_utils import NotebookLMAuthManager

async def run_list(manager):
    client = await manager.get_notebook_client()
    if not client:
        print("[ERROR] NotebookLM client not initialized. Run setup_notebooklm_auth.py first.")
        return

    async with client:
        notebooks = await client.notebooks.list()
        print("\n=== Your Notebooks ===")
        if not notebooks:
            print("No notebooks found.")
        for nb in notebooks:
            print(f"- {nb.title} (ID: {nb.id})")

async def run_notebook_action(manager, notebook_id):
    client = await manager.get_notebook_client()
    if not client:
        print("[ERROR] NotebookLM client not initialized. Run setup_notebooklm_auth.py first.")
        return

    async with client:
        print(f"[*] Interacting with notebook: {notebook_id}")
        # Add more logic here as needed

def main():
    parser = argparse.ArgumentParser(description="Automate NotebookLM Sync and Ingestion")
    parser.add_argument("--notebook", help="Specific notebook ID to interact with")
    parser.add_argument("--list", action="store_true", help="List all notebooks")
    args = parser.parse_args()

    manager = NotebookLMAuthManager()

    try:
        if args.list:
            asyncio.run(run_list(manager))
        elif args.notebook:
            asyncio.run(run_notebook_action(manager, args.notebook))
        else:
            print("[INFO] No action specified. Use --list or --notebook <ID>")

    except Exception as e:
        print(f"[ERROR] NotebookLM automation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
