#!/usr/bin/env python3
"""
Setup script for agent-runtime binary.
Called by Go CLI or Python worker before starting worker.

This script:
1. Downloads agent-runtime binary from GitHub releases
2. Verifies SHA256 checksum
3. Makes binary executable
4. Optionally starts the server
5. Returns server info as JSON

Usage:
    python setup_agent_runtime.py [config_dir] [--start-server] [--version VERSION]
"""

import asyncio
import sys
import json
import argparse
from pathlib import Path


async def ensure_agent_runtime(
    config_dir: str,
    version: str = "latest",
    start_server: bool = False,
    grpc_port: int = 50052,
    http_port: int = 8082,
) -> dict:
    """
    Ensure agent-runtime binary available and optionally start server.

    Args:
        config_dir: Directory for config and binaries
        version: Version to download (default: "latest")
        start_server: Whether to start the server
        grpc_port: GRPC server port
        http_port: HTTP health check port

    Returns:
        Dictionary with binary info and server info (if started)
    """
    from control_plane_api.worker.binary_manager import BinaryManager
    from control_plane_api.worker.agent_runtime_server import AgentRuntimeServer, ServerConfig

    binary_manager = BinaryManager(Path(config_dir))

    # Download/verify binary
    binary_path = await binary_manager.ensure_binary(version)

    result = {
        "binary_path": str(binary_path),
        "version": binary_manager._get_current_version(),
        "executable": binary_path.is_file() and binary_path.stat().st_mode & 0o111,
    }

    if start_server:
        # Start server
        server_config = ServerConfig(
            grpc_port=grpc_port,
            http_port=http_port,
            config_dir=Path(config_dir),
        )

        server = AgentRuntimeServer(binary_path, server_config)
        await server.start(wait_for_health=True, timeout=30)

        result.update({
            "server_started": True,
            "grpc_address": server.grpc_address,
            "http_port": http_port,
            "pid": server.process.pid if server.process else None,
            "config_file": str(server.config_file),
        })
    else:
        result["server_started"] = False

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Setup agent-runtime binary and optionally start server"
    )
    parser.add_argument(
        "config_dir",
        nargs="?",
        default=str(Path.home() / ".kubiya"),
        help="Config directory (default: ~/.kubiya)",
    )
    parser.add_argument(
        "--start-server",
        action="store_true",
        help="Start agent-runtime server after download",
    )
    parser.add_argument(
        "--version",
        default="latest",
        help="Version to download (default: latest)",
    )
    parser.add_argument(
        "--grpc-port",
        type=int,
        default=50052,
        help="GRPC server port (default: 50052)",
    )
    parser.add_argument(
        "--http-port",
        type=int,
        default=8082,
        help="HTTP health check port (default: 8082)",
    )

    args = parser.parse_args()

    try:
        result = asyncio.run(
            ensure_agent_runtime(
                config_dir=args.config_dir,
                version=args.version,
                start_server=args.start_server,
                grpc_port=args.grpc_port,
                http_port=args.http_port,
            )
        )

        # Output JSON for Go CLI or other callers to parse
        print(json.dumps(result, indent=2))
        sys.exit(0)

    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e),
        }
        print(json.dumps(error_result, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
