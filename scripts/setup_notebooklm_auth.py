#!/usr/bin/env python3
"""Strengthened authentication setup for NotebookLM."""

from __future__ import annotations

import argparse
import sys
import asyncio
from pathlib import Path

# Add scripts directory to path to import lib
sys.path.append(str(Path(__file__).resolve().parents[1]))
from lib.nblm_utils import NotebookLMAuthManager

async def test_and_report(manager: NotebookLMAuthManager):
    print("\n[*] Testing connection to NotebookLM...")
    if await manager.validate_connection_async():
        print("[SUCCESS] NotebookLM connection is active.")
        return True
    else:
        print("[FAILED] Authentication is expired or missing.")
        return False

def main():
    parser = argparse.ArgumentParser(description="Secure Setup for NotebookLM Authentication")
    parser.add_argument("--test", action="store_true", help="Test existing authentication")
    args = parser.parse_args()

    manager = NotebookLMAuthManager()

    if args.test:
        if asyncio.run(test_and_report(manager)):
            sys.exit(0)
        else:
            if not input("Proceed with new login? [y/N]: ").lower().startswith('y'):
                sys.exit(1)

    print("\n" + "="*45)
    print("   NotebookLM AUTHENTICATION SETUP (V2)   ")
    print("="*45)
    
    # Check if we already have tokens
    if manager.standard_storage.exists():
        print(f"[!] Found existing session at {manager.standard_storage}")
        if not input("    Refresh session? [y/N]: ").lower().startswith('y'):
            print("Aborted.")
            sys.exit(0)

    # Use the official login command
    if manager.run_login_cli():
        print("\n[SUCCESS] Login completed.")
        
        print("\n[*] Verifying connection...")
        if manager.validate_connection():
            print("[SUCCESS] Connection verified! You are ready to sync.")
        else:
            print("[WARNING] Login finished, but verification FAILED.")
            print("          Check if NotebookLM is accessible (VPN might be needed).")
    else:
        print("\n[ERROR] Login process failed.")

    print("\n" + "="*45)
    print("   Setup Complete")
    print("="*45)

if __name__ == "__main__":
    main()
