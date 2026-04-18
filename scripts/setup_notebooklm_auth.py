#!/usr/bin/env python3
"""Setup authentication for NotebookLM using notebooklm-py.

This script helps you authenticate and save the authentication state.
"""

from __future__ import annotations

from notebooklm import AuthTokens
import json
import os

# Create .auth directory if it doesn't exist
auth_dir = ".auth"
if not os.path.exists(auth_dir):
    os.makedirs(auth_dir)

auth_path = os.path.join(auth_dir, "notebooklm_state.json")

print("=== NotebookLM Authentication Setup ===")
print("This script will help you authenticate with NotebookLM.")
print("You'll need to:")
print("1. Open NotebookLM in your browser and login")
print("2. Run the following command in another terminal:")
print('   python3 -c "from notebooklm import AuthTokens; print(AuthTokens.from_browser())"')
print("3. Copy the output and paste it here")
print("\nPress Enter to continue...")
input()

try:
    # Get authentication tokens from browser
    print("\nGetting authentication tokens...")
    auth_tokens = AuthTokens.from_browser()
    
    # Save to file
    with open(auth_path, 'w') as f:
        json.dump(auth_tokens.to_dict(), f, indent=2)
    
    print(f"\nAuthentication saved to: {auth_path}")
    print("You can now use the automate_notebooklm.py script.")
    
except Exception as e:
    print(f"Error during authentication: {e}")
    print("Please follow the manual steps above.")

print("\n=== Setup Complete ===")
