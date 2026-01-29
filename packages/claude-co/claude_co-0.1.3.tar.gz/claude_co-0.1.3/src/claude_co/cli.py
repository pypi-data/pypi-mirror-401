"""CLI for Claude-Co setup and configuration."""

import json
import os
import sys
from pathlib import Path


def get_claude_config_path() -> Path:
    """Find Claude Code's config file."""
    # Check common locations
    candidates = [
        Path.home() / ".claude.json",
        Path.home() / ".config" / "claude" / "settings.json",
        Path.home() / ".claude" / "settings.json",
    ]

    for path in candidates:
        if path.exists():
            return path

    # Default to ~/.claude.json
    return Path.home() / ".claude.json"


def install_mcp_server(agent_id: str = None):
    """Add claude-co to Claude Code's MCP config."""
    config_path = get_claude_config_path()

    # Load existing config or create new
    if config_path.exists():
        with open(config_path) as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                config = {}
    else:
        config = {}

    # Ensure mcpServers exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # Check if already installed
    if "claude-co" in config["mcpServers"]:
        print(f"claude-co is already configured in {config_path}")
        existing = config["mcpServers"]["claude-co"]
        if "env" in existing and "AGENT_ID" in existing["env"]:
            print(f"  AGENT_ID: {existing['env']['AGENT_ID']}")
        return True

    # Get agent ID
    if not agent_id:
        # Try to get username
        default_id = os.environ.get("USER", "user") + "-claude"
        agent_id = input(f"Enter your agent ID [{default_id}]: ").strip() or default_id

    # Add claude-co MCP server
    config["mcpServers"]["claude-co"] = {
        "command": "python",
        "args": ["-m", "claude_co"],
        "env": {
            "AGENT_ID": agent_id
        }
    }

    # Backup existing config
    if config_path.exists():
        backup_path = config_path.with_suffix(".json.backup")
        config_path.rename(backup_path)
        print(f"Backed up existing config to {backup_path}")

    # Write new config
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"\nInstalled claude-co to {config_path}")
    print(f"  AGENT_ID: {agent_id}")
    print("\nRestart Claude Code for changes to take effect.")
    return True


def setup_project(url: str, api_key: str, group: str, codebase: str = None):
    """Create .claude-co.json in current directory."""
    if not codebase:
        codebase = Path.cwd().name

    project_path = str(Path.cwd().absolute())
    config = {
        "url": url,
        "api_key": api_key,
        "group": group,
        "codebase": codebase,
        "project_path": project_path
    }

    # Save to project directory
    config_path = Path.cwd() / ".claude-co.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    # Also save as "current" project so MCP server can find it
    current_dir = Path.home() / ".claude-co"
    current_dir.mkdir(exist_ok=True)
    with open(current_dir / "current.json", "w") as f:
        json.dump(config, f, indent=2)

    print(f"Created {config_path}")
    print(f"  Server: {url}")
    print(f"  Group: {group}")
    print(f"  Codebase: {codebase}")
    print(f"  Project path: {project_path}")


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Claude-Co: Multi-agent coordination for Claude Code"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # install command
    install_parser = subparsers.add_parser(
        "install",
        help="Add claude-co to Claude Code's MCP config"
    )
    install_parser.add_argument(
        "--agent-id",
        help="Your agent ID (default: username-claude)"
    )

    # setup command
    setup_parser = subparsers.add_parser(
        "setup",
        help="Configure current project to use a coordination server"
    )
    setup_parser.add_argument("url", help="Server URL")
    setup_parser.add_argument("api_key", help="API key")
    setup_parser.add_argument("group", help="Group name")
    setup_parser.add_argument("--codebase", help="Codebase name (default: directory name)")

    # run command (default - runs MCP server)
    subparsers.add_parser(
        "run",
        help="Run the MCP server (used by Claude Code)"
    )

    args = parser.parse_args()

    if args.command == "install":
        install_mcp_server(args.agent_id)
    elif args.command == "setup":
        setup_project(args.url, args.api_key, args.group, args.codebase)
    elif args.command == "run" or args.command is None:
        # Run MCP server
        from .server import main as run_server
        run_server()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
