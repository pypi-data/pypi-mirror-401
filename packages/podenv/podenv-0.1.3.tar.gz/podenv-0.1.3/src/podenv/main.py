#!/usr/bin/env python3
"""podenv CLI entry point"""

import os
import sys
import subprocess
from pathlib import Path


def ensure_path_configured():
    """Check and auto-configure ~/.local/bin in PATH"""
    local_bin = Path.home() / ".local" / "bin"
    bashrc = Path.home() / ".bashrc"
    path_line = 'export PATH="$HOME/.local/bin:$PATH"'

    # Check if ~/.local/bin is in current PATH
    if str(local_bin) in os.environ.get("PATH", ""):
        return

    # Check if already in .bashrc
    if bashrc.exists():
        content = bashrc.read_text()
        if ".local/bin" in content:
            return

    # Add to .bashrc
    print("Configuring PATH: adding ~/.local/bin to ~/.bashrc...")
    with open(bashrc, "a") as f:
        f.write(f"\n# Added by podenv\n{path_line}\n")

    # Update current PATH
    os.environ["PATH"] = f"{local_bin}:{os.environ.get('PATH', '')}"
    print("PATH configured. Changes will apply to new terminals automatically.")


def main():
    """Run podenv bash script"""
    # Auto-configure PATH on first run
    ensure_path_configured()

    script_path = Path(__file__).parent / "podenv.sh"

    if not script_path.exists():
        print(f"Error: Script not found {script_path}", file=sys.stderr)
        sys.exit(1)

    # Pass all command line arguments to bash script
    args = ["bash", str(script_path)] + sys.argv[1:]

    try:
        result = subprocess.run(args)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
