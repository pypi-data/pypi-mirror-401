import argparse
import logging
import os
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

from azure.core.exceptions import AzureError

from gettopology import __version__
from gettopology.azure_auth import get_azure_credential
from gettopology.azure_service import (
    check_subscription_roles,
    collect_topology,
    get_all_subscription_ids,
    get_vnets,
    validate_subscription_access,
)
from gettopology.diagram_generator import (
    generate_hld_diagram,
    generate_index_html,
    generate_markmap_diagram,
    hybrid_connection_diagram,
)
from gettopology.utils import (
    normalize_subscription_ids,
    setup_logging,
    validate_file_path,
)


def generate_output_directory(output_arg: str | None) -> str:
    """Generate output directory path with timestamp if not provided.

    If output_arg is None (not provided), creates a timestamped folder:
    format: topology_YYYYMMDD_HHMMSS

    Args:
        output_arg: Output directory from CLI argument (None if not provided)

    Returns:
        str: Output directory path (absolute path)

    Raises:
        OSError: If directory creation fails due to permissions or other OS errors
        PermissionError: If user doesn't have permission to create directory
    """
    if output_arg is None:
        # Generate timestamped folder name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"topology_{timestamp}"
        output_dir = os.path.abspath(folder_name)
    else:
        # Use provided output directory
        output_dir = os.path.abspath(output_arg)

    # Create directory with error handling
    try:
        os.makedirs(output_dir, exist_ok=True)
        logging.info(f"Output directory: {output_dir}")
    except PermissionError as e:
        error_msg = f"Permission denied: Cannot create output directory '{output_dir}'. "
        if sys.platform == "win32":
            error_msg += "Check if you have write permissions in the current directory."
        else:
            error_msg += "Check directory permissions and user access rights."
        logging.critical(error_msg)
        raise PermissionError(error_msg) from e
    except OSError as e:
        error_msg = f"Failed to create output directory '{output_dir}': {e}"
        if sys.platform == "win32":
            error_msg += " On Windows, ensure the path is valid and you have write access."
        else:
            error_msg += " Check if the path is valid and you have write permissions."
        logging.critical(error_msg)
        raise OSError(error_msg) from e

    return output_dir


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="GetTopology - Azure VNet Topology Generator"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"gettopology {__version__}"
    )
    parser.add_argument(
        "-s", "--subscriptions",
        help="Comma-separated subscription IDs (optional)"
    )
    parser.add_argument(
        "-f", "--subscriptions-file",
        help="File with subscription IDs (optional)"
    )
    parser.add_argument(
        "-vnet", "--virtual-network",
        action="store_true",
        help="Generate markmap diagram instead of HLD diagram"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level (default: INFO)"
    )
    # Service Principal authentication (optional)
    # Authentication order: 1) Azure CLI, 2) Service Principal (CLI args -> env vars -> .env file), 3) Managed Identity
    parser.add_argument(
        "--client-id",
        help="Service Principal client ID (for SPN authentication). Priority: CLI arg > AZURE_CLIENT_ID env var > .env file."
    )
    parser.add_argument(
        "--client-secret",
        help="Service Principal client secret (for SPN authentication). Priority: CLI arg > AZURE_CLIENT_SECRET env var > .env file."
    )
    parser.add_argument(
        "--tenant-id",
        help="Azure tenant ID (for SPN authentication). Priority: CLI arg > AZURE_TENANT_ID env var > .env file."
    )
    parser.add_argument(
        "--skip-roles",
        action="store_true",
        help="Skip role verification. By default, the tool verifies that the authenticated user/service principal has at least 'Reader' role on subscriptions before proceeding"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output directory for generated diagrams (default: auto-generated timestamped folder)",
        default=None
    )
    return parser.parse_args()



def resolve_subscriptions(
    args: argparse.Namespace,
    credential: Any,
    ) -> tuple[list[str], bool]:
    """Resolve and validate subscriptions from CLI arguments.

    Subscription resolution priority:
    1. If -s (--subscriptions) provided: Only validate and use those subscriptions
    2. If -f (--subscriptions-file) provided: Only validate and use subscriptions from file
    3. If neither provided: Discover and use all accessible subscriptions

    Args:
        args: Parsed command-line arguments
        credential: Azure credential object

    Returns:
        tuple: (subscription_ids, strict_role_check)
            - subscription_ids: List of validated subscription IDs (only those specified, or all if none specified)
            - strict_role_check: True if subscriptions were explicitly provided, False if auto-discovered
    """
    if args.subscriptions:
        # Case 1: User explicitly provided subscriptions via -s flag
        # Only validate and use these specific subscriptions
        subscriptions, invalid_ids = normalize_subscription_ids(args.subscriptions.split(","))
        if invalid_ids:
            logging.error(f"Invalid subscription ID format(s): {', '.join(invalid_ids)}")
            sys.exit(1)
        if not subscriptions:
            logging.error("No valid subscriptions found in provided list")
            sys.exit(1)

        # Validate that subscriptions are accessible
        accessible, inaccessible = validate_subscription_access(subscriptions, credential)
        if inaccessible:
            logging.error(
                f"Subscription ID(s) not accessible or not found: {', '.join(inaccessible)}"
            )
            logging.error(
                "Note: Subscriptions must be in the same tenant as your authentication. "
                "Azure CLI and Service Principal authentication can only access one tenant at a time."
            )
            sys.exit(1)
        if not accessible:
            logging.error("None of the provided subscription IDs are accessible")
            sys.exit(1)
        if accessible:
            logging.info(
                f"Validated {len(accessible)} accessible subscription(s): {', '.join(accessible)}"
            )
        return accessible, True  # Strict check for explicitly provided subscriptions

    elif args.subscriptions_file:
        # Case 2: User explicitly provided subscriptions via -f flag (file)
        # Only validate and use these specific subscriptions from the file
        file_path = validate_file_path(args.subscriptions_file)
        with file_path.open("r", encoding="utf-8") as file:
            subscriptions, invalid_ids = normalize_subscription_ids(file.read().splitlines())
        if invalid_ids:
            logging.error(f"Invalid subscription ID format(s) in file: {', '.join(invalid_ids)}")
            sys.exit(1)
        if not subscriptions:
            logging.error("No valid subscriptions found in file")
            sys.exit(1)

        # Validate that subscriptions are accessible
        accessible, inaccessible = validate_subscription_access(subscriptions, credential)
        if inaccessible:
            logging.error(
                f"Subscription ID(s) from file not accessible or not found: {', '.join(inaccessible)}"
            )
            logging.error(
                "Note: Subscriptions must be in the same tenant as your authentication."
            )
            sys.exit(1)
        if not accessible:
            logging.error("None of the subscription IDs from file are accessible")
            sys.exit(1)
        return accessible, True  # Strict check for explicitly provided subscriptions

    else:
        # Case 3: No subscriptions specified via -s or -f
        # Discover and use all accessible subscriptions for the authenticated user/service principal
        logging.info("No subscriptions specified via -s or -f. Discovering all accessible subscriptions...")
        subscriptions = get_all_subscription_ids(credential)
        if subscriptions:
            logging.info(f"Found {len(subscriptions)} accessible subscription(s): {', '.join(subscriptions)}")
        return subscriptions, False  # Lenient check for auto-discovered subscriptions


def check_roles_if_enabled(
    subscriptions: list[str],
    credential: Any,
    skip_roles: bool,
    strict_role_check: bool,
    ) -> list[str]:
    """Check role permissions (enabled by default).

    This function only checks the subscriptions passed to it. The subscription list
    is already filtered by resolve_subscriptions():
    - If -s or -f was provided: Only those subscriptions are checked
    - If nothing was provided: All discovered subscriptions are checked

    Args:
        subscriptions: List of subscription IDs to check (already filtered by resolve_subscriptions)
        credential: Azure credential object
        skip_roles: Whether to skip role checking (from --skip-roles flag)
        strict_role_check: True if subscriptions were explicitly provided, False if auto-discovered

    Returns:
        List of subscription IDs with proper roles (filtered if not strict)
    """
    if skip_roles or not subscriptions:
        if skip_roles:
            logging.info("Skipping role verification (--skip-roles flag provided)")
        return subscriptions

    logging.info(f"Checking role permissions on {len(subscriptions)} subscription(s)...")
    with_role, without_role = check_subscription_roles(subscriptions, credential)

    if without_role:
        if strict_role_check:
            # For explicitly provided subscriptions, fail if any lack proper role
            logging.error(
                f"Subscription ID(s) without Reader role or above: {', '.join(without_role)}"
            )
            logging.error("The authenticated user/service principal needs at least 'Reader' role on all subscriptions")
            sys.exit(1)
        else:
            # For "get all" case, filter out subscriptions without proper roles
            logging.warning(
                f"Subscription ID(s) without Reader role or above: {', '.join(without_role)}"
            )
            logging.warning("These subscriptions will be excluded from topology collection")
            subscriptions = with_role
            if not subscriptions:
                logging.error("No subscriptions with Reader role or above found")
                sys.exit(1)

    if with_role:
        logging.info(
            f"Verified Reader role or above on {len(with_role)} subscription(s): {', '.join(with_role)}"
        )

    return subscriptions


def run_topology_collection(
    args: argparse.Namespace,
    credential: Any,
    ) -> None:
    """Orchestrate the topology collection workflow.

    This function handles the business logic flow:
    1. Resolve and validate subscriptions
    2. Check roles (enabled by default, can be skipped with --skip-roles)
    3. Resolve virtual networks
    4. Collect topology data (Phase 3)
    5. Generate diagrams (Phase 4)

    Args:
        args: Parsed command-line arguments
        credential: Azure credential object
    """
    # Step 1: Resolve and validate subscriptions
    subscriptions, strict_role_check = resolve_subscriptions(args, credential)

    # Step 2: Check roles (enabled by default, can be skipped with --skip-roles)
    subscriptions = check_roles_if_enabled(
        subscriptions,
        credential,
        args.skip_roles,
        strict_role_check,
    )

    # Step 3: Get all VNets from specified subscriptions
    virtual_networks = get_vnets(
        subscription_ids=subscriptions,
        credential=credential,
    )

    logging.info(f"Subscriptions: {subscriptions}")
    logging.info(f"Virtual Networks: {len(virtual_networks)}: [{', '.join(virtual_networks)}] VNet(s) found")

    # Step 4: Collect topology data (Phase 3)
    topology = collect_topology(virtual_networks, subscriptions, credential)
    if topology.virtual_networks == []:
        logging.critical("No virtual networks found: Aborting...")
        sys.exit(1)
    else:
        logging.info(f"Topology collected: {len(topology.virtual_networks)} VNet(s) with complete details")
        logging.debug(f"{topology.model_dump_json(indent=2)}")  # Print the full topology

    # Step 5: Generate diagrams (Phase 4)
    if topology.virtual_networks:
        # Generate or use output directory
        try:
            output_dir = generate_output_directory(args.output)
        except (OSError, PermissionError) as e:
            logging.critical(f"Cannot proceed without output directory: {e}")
            sys.exit(1)

        # Collect hybrid connectivity data once (used for both printing and diagram)
        from gettopology.azure_service import collect_hybrid_connectivity
        hybrid_data = collect_hybrid_connectivity(topology, subscriptions, credential)

        # Generate hybrid connectivity diagram (Phase 1: data collection and printing)
        hybrid_connection_diagram(topology, output_dir, subscriptions, credential, hybrid_data)

        # Always generate HLD diagram (writes to output_dir/hld/)
        hld_path = generate_hld_diagram(topology, output_dir, hybrid_data)
        logging.info(f"HLD diagram generated: {hld_path}")

        # Additionally generate markmap diagram if -vnet flag is provided (writes to output_dir/vnet/)
        if args.virtual_network:
            generate_markmap_diagram(topology, output_dir, subscriptions, credential)
            logging.info(f"Markmap diagrams generated in: {os.path.join(output_dir, 'vnet')}/")

        # Generate index.html
        generate_index_html(output_dir, hld_path)

        # Create zip file
        zip_path = create_output_zip(output_dir)
        logging.info(f"Output packaged: {zip_path}")
    else:
        logging.warning("No virtual networks to diagram")


def create_output_zip(output_dir: str) -> str:
    """Create a zip file of the output directory.

    Args:
        output_dir: Path to the output directory

    Returns:
        str: Path to the created zip file
    """
    output_path = Path(output_dir)
    zip_path = output_path.parent / f"{output_path.name}.zip"

    # Remove existing zip if it exists
    if zip_path.exists():
        zip_path.unlink()

    # Create zip file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in output_path.rglob('*'):
            if file_path.is_file():
                # Use relative path in zip (preserves directory structure)
                arcname = file_path.relative_to(output_path.parent)
                zipf.write(file_path, arcname)

    return str(zip_path)


def main() -> None:
    """Main entry point for the CLI tool."""
    args = parse_arguments()
    setup_logging(args.log_level)

    # Authenticate with Azure
    # get_azure_credential handles the priority: CLI args -> env vars -> .env file
    try:
        credential = get_azure_credential(
            client_id=args.client_id,
            client_secret=args.client_secret,
            tenant_id=args.tenant_id,
        )
    except (ValueError, AzureError) as e:
        logging.error(f"Authentication failed: {e}")
        sys.exit(1)

    # Run the topology collection workflow
    run_topology_collection(args, credential)


if __name__ == "__main__":
    main()
