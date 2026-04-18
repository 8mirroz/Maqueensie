#!/usr/bin/env python3
"""Automated NotebookLM integration using notebooklm-py.

- Automatically exports bundles
- Creates notebooks for each domain
- Uploads sources
- Generates podcasts
- Manages authentication
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List, Optional

# Import notebooklm-py if available
notebooklm_available = True
try:
    from notebooklm import NotebookLMClient
except ImportError:
    notebooklm_available = False

ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = ROOT / "exports" / "nblm"
DOMAINS = [
    "01_Architecture",
    "02_Interior",
    "03_Renovation",
    "04_Decor",
    "05_Furniture",
    "06_RealEstate",
]

AUTH_STORAGE = ROOT / ".auth" / "notebooklm_state.json"


def export_bundles() -> List[str]:
    """Export markdown bundles using existing script."""
    print("Exporting markdown bundles...")
    
    # Run existing export script
    import subprocess
    result = subprocess.run(
        ["python3", "scripts/export_nblm_bundles.py"],
        cwd=str(ROOT),
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("Error exporting bundles:", result.stderr)
        return []
    
    # List exported files
    exported = [f"{domain}_bundle.md" for domain in DOMAINS]
    print(f"Exported {len(exported)} bundles")
    return exported


def create_notebook(client: NotebookLMClient, domain: str) -> str:
    """Create a new notebook for the domain."""
    print(f"Creating notebook for: {domain}")
    notebook_name = f"{domain} - Market Intelligence"
    
    try:
        notebook = asyncio.run(client.notebooks.create(notebook_name))
        print(f"Created notebook: {notebook.id}")
        return notebook.id
    except Exception as e:
        print(f"Error creating notebook: {e}")
        return ""


def upload_sources(client: NotebookLMClient, notebook_id: str, domain: str) -> bool:
    """Upload sources to the notebook."""
    print(f"Uploading sources for notebook: {notebook_id}")
    
    bundle_path = EXPORT_DIR / f"{domain}_bundle.md"
    if not bundle_path.exists():
        print(f"Bundle not found: {bundle_path}")
        return False
    
    try:
        # Upload the markdown file
        source = asyncio.run(client.sources.add_file(notebook_id, str(bundle_path)))
        print(f"Uploaded source: {source.id}")
        return True
    except Exception as e:
        print(f"Error uploading sources: {e}")
        return False


def generate_podcast(client: NotebookLMClient, notebook_id: str, domain: str) -> bool:
    """Generate podcast for the notebook."""
    print(f"Generating podcast for notebook: {notebook_id}")
    
    try:
        # Generate audio artifact
        task = asyncio.run(client.artifacts.generate_audio(notebook_id))
        print(f"Audio generation started: {task.task_id}")
        
        # Wait for completion
        asyncio.run(client.artifacts.wait_for_completion(notebook_id, task.task_id))
        print("Audio generation completed")
        
        # Download audio
        audio_path = EXPORT_DIR / f"{domain}_podcast.mp3"
        asyncio.run(client.artifacts.download_audio(notebook_id, str(audio_path)))
        print(f"Podcast saved to: {audio_path}")
        return True
    except Exception as e:
        print(f"Error generating podcast: {e}")
        return False


def setup_authentication() -> Optional[NotebookLMClient]:
    """Setup authentication for NotebookLM."""
    print("Setting up NotebookLM authentication...")
    
    if not notebooklm_available:
        print("notebooklm-py not installed. Please run: pip install notebooklm-py")
        return None
    
    try:
        # Try to load from storage
        client = asyncio.run(NotebookLMClient.from_storage(str(AUTH_STORAGE)))
        print("Loaded authentication from storage")
        return client
    except Exception as e:
        print(f"Authentication error: {e}")
        print("Please authenticate manually:")
        print("1. Open browser and login to NotebookLM")
        print('2. Run: python3 -c "from notebooklm import AuthTokens; print(AuthTokens.from_browser())"')
        print("3. Save the output to: .auth/notebooklm_state.json")
        return None


def main() -> int:
    print("=== Maqueensie NotebookLM Automation ===")
    
    # Export bundles first
    exported = export_bundles()
    if not exported:
        print("No bundles exported. Exiting.")
        return 1
    
    # Setup authentication
    client = setup_authentication()
    if not client:
        print("Authentication not configured. Exiting.")
        return 1
    
    # Process each domain
    for domain in DOMAINS:
        print(f"\nProcessing domain: {domain}")
        
        # Create notebook
        notebook_id = create_notebook(client, domain)
        if not notebook_id:
            continue
        
        # Upload sources
        if upload_sources(client, notebook_id, domain):
            # Generate podcast
            generate_podcast(client, notebook_id, domain)
        
        print(f"Domain {domain} processing complete")
    
    print("\n=== Automation Complete ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
