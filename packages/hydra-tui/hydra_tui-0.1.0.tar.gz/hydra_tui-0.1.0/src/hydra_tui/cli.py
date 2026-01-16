"""CLI entry point for hydra-tui."""

import json
import subprocess
import sys
from typing import Any, Optional

from rich.console import Console

from .tui.app import run_tui
from .tui.models import ConfigGroup, ConfigValue, HydraConfig


def parse_intercept_output(output: str) -> Optional[dict]:
    """Parse the JSON output from the intercept launcher."""
    start_marker = "__HYDRA_INTERCEPT_START__"
    end_marker = "__HYDRA_INTERCEPT_END__"

    start_idx = output.find(start_marker)
    end_idx = output.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        return None

    json_str = output[start_idx + len(start_marker) : end_idx].strip()
    return json.loads(json_str)


def flatten_config(config: dict, prefix: str = "") -> dict[str, Any]:
    """Flatten a nested config into dot-notation paths."""
    flattened = {}

    if isinstance(config, dict):
        for key, value in config.items():
            new_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, (dict, list)) and value:
                flattened.update(flatten_config(value, new_key))
            else:
                flattened[new_key] = value
    elif isinstance(config, list):
        for i, value in enumerate(config):
            new_key = f"{prefix}.{i}"
            if isinstance(value, (dict, list)) and value:
                flattened.update(flatten_config(value, new_key))
            else:
                flattened[new_key] = value
    else:
        flattened[prefix] = config

    return flattened


def build_hydra_config(data: dict, command: list[str]) -> HydraConfig:
    """Build HydraConfig model from intercepted data."""
    groups_data = data.get("groups", {})
    config_data = data.get("config", {})

    # Build config groups (filter out hydra internal groups)
    groups = {}
    for group_name, group_info in groups_data.items():
        # Skip hydra internal groups
        if group_name.startswith("hydra"):
            continue

        options = group_info.get("options", [])
        selected_str = group_info.get("selected")

        # Parse selected value(s)
        selected = []
        if selected_str:
            selected = [selected_str]

        groups[group_name] = ConfigGroup(
            name=group_name,
            options=options,
            selected=selected,
            original_selected=selected_str,
            multirun=False,
        )

    # Build config values (flatten and exclude hydra config)
    config_without_hydra = {k: v for k, v in config_data.items() if k != "hydra"}
    flattened = flatten_config(config_without_hydra)

    values = {}
    for path, value in flattened.items():
        values[path] = ConfigValue(
            path=path,
            value=value,
            original_value=value,
        )

    return HydraConfig(groups=groups, values=values, command=command)


def main() -> None:
    """Main entry point for hydra-tui CLI."""
    console = Console()

    if len(sys.argv) < 2:
        console.print("[bold cyan]Hydra TUI[/bold cyan] - Interactive Hydra Configuration")
        console.print()
        console.print("[bold]Usage:[/bold] hydra-tui <command>")
        console.print("[dim]Example: hydra-tui uv run jetrl-router[/dim]")
        sys.exit(1)

    # Get the command to intercept
    command = sys.argv[1:]

    # Append the intercept launcher override and -m flag for multirun mode
    # (launchers are only invoked in multirun mode)
    intercept_command = command + ["-m", "hydra/launcher=hydra_tui_inspector"]

    try:
        # Run the command and capture output with spinner
        with console.status("[bold cyan]Loading configuration groups...[/bold cyan]", spinner="dots"):
            result = subprocess.run(
                intercept_command,
                capture_output=True,
                text=True,
            )

            # Combine stdout and stderr (Hydra may print to either)
            output = result.stdout + result.stderr

            # Parse the intercept output
            data = parse_intercept_output(output)

        if data is None:
            console.print("[bold red]Error:[/bold red] Failed to load configuration.")
            console.print("[dim]Command output:[/dim]")
            console.print(output)
            sys.exit(1)

        # Build config model
        assert data is not None  # For type checker
        config = build_hydra_config(data, command)

        # Launch TUI
        should_execute, overrides = run_tui(config)

        if should_execute:
            # Build final command with overrides
            final_command = list(command)  # Copy the command

            # Add -m flag if multirun is active and not already present
            multirun_count = config.get_multirun_count()
            if multirun_count:
                # Check if -m or --multirun is already in the command
                if "-m" not in final_command and "--multirun" not in final_command:
                    final_command.append("-m")

            final_command.extend(overrides)

            # Show beautiful command display
            console.print()
            console.print("─" * console.width)

            if multirun_count and multirun_count > 1:
                console.print(f"[bold green]🚀 Launching {multirun_count} experiments[/bold green]")
            else:
                console.print("[bold green]🚀 Running command[/bold green]")

            console.print()

            # Show command with syntax highlighting
            cmd_str = " ".join(final_command)
            # Highlight overrides in the command
            for override in overrides:
                if override.startswith("~"):
                    # Deletion (red)
                    cmd_str = cmd_str.replace(override, f"[red]{override}[/red]")
                elif override.startswith("+"):
                    # New config group (green)
                    cmd_str = cmd_str.replace(override, f"[green]{override}[/green]")
                else:
                    # Regular override (yellow)
                    cmd_str = cmd_str.replace(override, f"[yellow]{override}[/yellow]")

            # Highlight the -m flag if present and we're in multirun mode
            if multirun_count and multirun_count > 1:
                if " -m " in cmd_str:
                    cmd_str = cmd_str.replace(" -m ", " [magenta]-m[/magenta] ", 1)
                elif " --multirun " in cmd_str:
                    cmd_str = cmd_str.replace(" --multirun ", " [magenta]--multirun[/magenta] ", 1)

            console.print(f"  [bold cyan]$[/bold cyan] {cmd_str}")
            console.print()
            console.print("─" * console.width)
            console.print()

            # Execute the command (stdout/stderr will appear naturally)
            subprocess.run(final_command, check=False)
        else:
            console.print("\n[yellow]Cancelled[/yellow]")

    except FileNotFoundError:
        console.print(f"[bold red]✗ Error:[/bold red] Command not found: {command[0]}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        console.print(f"[bold red]✗ Error:[/bold red] Failed to parse configuration: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")
        sys.exit(130)


if __name__ == "__main__":
    main()
