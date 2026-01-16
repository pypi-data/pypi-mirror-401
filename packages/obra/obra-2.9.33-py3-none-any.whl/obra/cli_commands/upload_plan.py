"""CLI command for uploading MACHINE_PLAN.yaml files to Obra SaaS.

This module provides the UploadPlanCommand class which implements
the 'obra upload-plan' command. It uploads plan files to Firestore
for later use with 'obra derive --plan-id'.

Usage:
    $ obra upload-plan path/to/MACHINE_PLAN.yaml
    $ obra upload-plan --validate-only plan.yaml

Reference: FEAT-PLAN-IMPORT-OBRA-001 Component 5: Client-Side CLI Commands
"""

import json
import logging
from pathlib import Path

import click
import yaml

from obra.api import APIClient
from obra.auth import ensure_valid_token, get_current_auth
from obra.display import console, print_error, print_success
from obra.display.errors import display_obra_error
from obra.exceptions import ObraError

logger = logging.getLogger(__name__)


def _strip_tasks_for_upload(plan_data: dict) -> dict:
    """Strip tasks array to reduce upload size.

    Keeps: work_id, version, created, story_count, flags, completion_checklist
    Strips: stories array (entire array)

    Returns:
        Stripped plan with metadata only (~2KB vs 50KB)
    """
    stories = plan_data.get("stories", [])
    story_count = len(stories) if isinstance(stories, list) else 0

    stripped = {
        "work_id": plan_data.get("work_id"),
        "version": plan_data.get("version"),
        "created": plan_data.get("created"),
        "context": plan_data.get("context", {}),
        "flags": plan_data.get("flags", {}),
        "completion_checklist": plan_data.get("completion_checklist", []),
        "story_count": story_count,
    }
    return {k: v for k, v in stripped.items() if v is not None}


class UploadPlanCommand:
    """Command handler for uploading MACHINE_PLAN.yaml files.

    This class implements the 'obra upload-plan' CLI command which:
    1. Parses YAML plan file
    2. Uploads plan to Firestore via upload_plan endpoint (server validates)
    3. Returns plan_id for use with 'obra derive --plan-id'

    Features:
    - Server-side validation (authoritative schema validation)
    - Plan library storage (upload once, use many times)
    - Colored output and progress indication

    Example:
        >>> cmd = UploadPlanCommand()
        >>> cmd.execute("plan.yaml", validate_only=False)
        0  # Returns exit code
    """

    def __init__(self) -> None:
        """Initialize UploadPlanCommand."""

    def execute(
        self,
        file_path: str,
        validate_only: bool = False,
    ) -> int:
        """Execute plan upload and display results.

        Parses YAML file and uploads to server for validation and storage.
        Server performs authoritative schema validation.

        Args:
            file_path: Path to the YAML plan file to upload
            validate_only: If True, only check YAML syntax without uploading

        Returns:
            Exit code: 0 if successful, 1 if failed

        Example:
            >>> cmd = UploadPlanCommand()
            >>> exit_code = cmd.execute("plan.yaml")
            >>> sys.exit(exit_code)
        """
        # Validate file path
        path = Path(file_path)

        if not path.exists():
            print_error(f"File not found: {path}")
            return 1

        console.print()
        console.print("[bold]Uploading Plan[/bold]", style="cyan")
        console.print(f"File: {path}")
        console.print()

        # Parse plan file
        console.print("[dim]Parsing YAML file...[/dim]")
        try:
            with open(path, encoding="utf-8") as f:
                plan_data = yaml.safe_load(f)
        except Exception as e:
            console.print()
            print_error(f"Failed to parse YAML: {e}")
            return 1

        if not isinstance(plan_data, dict):
            console.print()
            print_error(f"Invalid plan format: expected mapping, got {type(plan_data).__name__}")
            return 1

        print_success("YAML syntax is valid")
        console.print()

        # If validate-only, stop here (full schema validation happens on server)
        if validate_only:
            console.print("[dim]Note: Full schema validation happens on server during upload[/dim]")
            return 0

        # Strip tasks to reduce upload size
        original_size_bytes = len(json.dumps(plan_data).encode("utf-8"))
        stripped_plan_data = _strip_tasks_for_upload(plan_data)
        stripped_size_bytes = len(json.dumps(stripped_plan_data).encode("utf-8"))
        saved_bytes = max(original_size_bytes - stripped_size_bytes, 0)

        # Extract plan name from work_id
        plan_name = plan_data.get("work_id", path.stem)

        # Ensure authenticated
        try:
            auth = get_current_auth()
            if not auth:
                print_error("Not logged in")
                console.print("\nRun 'obra login' to authenticate.")
                return 1

            ensure_valid_token()
        except ObraError as e:
            display_obra_error(e, console)
            return 1

        # Step 4: Upload to server
        console.print("[dim]Uploading to server...[/dim]")
        try:
            client = APIClient.from_config()
            response = client.upload_plan(plan_name, stripped_plan_data)

            plan_id = response.get("plan_id")
            story_count = response.get("story_count", 0)
            if story_count == 0:
                story_count = stripped_plan_data.get("story_count", 0)

            console.print()
            print_success("Plan uploaded successfully!")
            console.print()
            console.print(f"Plan ID: [cyan]{plan_id}[/cyan]")
            console.print(f"Name: {plan_name}")
            console.print(f"Stories: {story_count}")
            console.print(
                f"Uploaded {stripped_size_bytes / 1024:.1f}KB "
                f"(saved {saved_bytes / 1024:.1f}KB by stripping tasks)"
            )
            console.print()
            console.print("[dim]Use this plan with:[/dim]")
            console.print(f'  [cyan]obra derive --plan-id {plan_id} "objective"[/cyan]')
            console.print()

            return 0

        except ObraError as e:
            console.print()
            display_obra_error(e, console)
            return 1
        except Exception as e:
            console.print()
            print_error(f"Upload failed: {e}")
            logger.exception("Unexpected error in upload_plan command")
            return 1


# Click command decorator for CLI integration
@click.command(name="upload-plan")
@click.argument(
    "file_path",
    type=click.Path(exists=True),
    required=True,
)
@click.option(
    "--validate-only",
    is_flag=True,
    help="Only validate the plan file without uploading",
)
def upload_plan_cli(file_path: str, validate_only: bool) -> None:
    """Upload MACHINE_PLAN.yaml file to Obra SaaS.

    Validates and uploads a plan file to Firestore for later use.
    After upload, use the returned plan_id with 'obra derive --plan-id'.

    The plan is stored in your account and can be:
    - Reused across multiple sessions
    - Listed with 'obra plans list'
    - Deleted with 'obra plans delete <plan_id>'

    Examples:

        \b
        # Upload a plan file
        $ obra upload-plan docs/development/MY_PLAN.yaml

        \b
        # Validate without uploading
        $ obra upload-plan --validate-only plan.yaml

        \b
        # Use the uploaded plan
        $ obra derive --plan-id abc123-uuid "Implement authentication"

    Exit Codes:
        0: Upload successful or validation passed
        1: Upload failed or validation failed
    """
    import sys

    command = UploadPlanCommand()
    exit_code = command.execute(file_path, validate_only)
    sys.exit(exit_code)


if __name__ == "__main__":
    # Allow running as standalone script
    upload_plan_cli()
