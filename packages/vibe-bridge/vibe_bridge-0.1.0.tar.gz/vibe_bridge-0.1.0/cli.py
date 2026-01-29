import os
import sys
import questionary
from datetime import datetime
from pathlib import Path

def init():
    """Sets up the Git Hook in the current directory."""
    hook_path = Path(".git/hooks/post-commit")
    if not Path(".git").exists():
        print("❌ Error: Not a git repository.")
        return

    # The hook script calls our python command
    hook_content = "#!/bin/sh\nvibe-bridge ask"
    
    with open(hook_path, "w") as f:
        f.write(hook_content)
    
    # Make the hook executable
    os.chmod(hook_path, 0o755)
    print("🚀 Vibe-Bridge activated! We are watching your commits.")

def ask():
    """The interactive interview."""
    print("\n🧠 Vibe-Bridge: Documenting the 'Why'...")
    
    intent = questionary.select(
        "Why did you write this code?",
        choices=["Performance hack", "Technical debt", "Feature add", "Just vibes"]
    ).ask()
    
    tradeoff = questionary.text("What was the trade-off or 'vibe' choice?").ask()

    if intent and tradeoff:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_entry = f"\n### [{timestamp}]\n**Intent:** {intent}\n**Trade-off:** {tradeoff}\n---\n"
        
        with open("CONTEXT.md", "a") as f:
            f.write(log_entry)
        print("✨ Context saved to CONTEXT.md.")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "init":
            init()
        elif sys.argv[1] == "ask":
            ask()
    else:
        print("Usage: vibe-bridge [init|ask]")

if __name__ == "__main__":
    main()