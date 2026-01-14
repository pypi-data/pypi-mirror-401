"""Log collection module for Agent and Worker container logs."""

from __future__ import annotations

import subprocess

from loguru import logger

from recurvedata.agent._internal.docker import docker_client
from recurvedata.agent.config import CONFIG

# Docker compose project name for recurve services
COMPOSE_PROJECT_NAME = "recurve_services"


def collect_agent_logs(tail_lines: int = 500) -> tuple[str, str | None]:
    """
    Collect Agent logs from the configured log file.

    Args:
        tail_lines: Number of lines to read from the end of the log file.

    Returns:
        A tuple of (log_content, log_path). If log collection fails,
        log_content contains an error message and log_path is the attempted path.
    """
    log_path = CONFIG.log_config.log_file_path

    try:
        if not log_path.exists():
            return f"File not found: {log_path}", str(log_path)

        # Use subprocess to call tail command for efficient tail reading
        result = subprocess.run(
            ["tail", "-n", str(tail_lines), str(log_path)],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0:
            return result.stdout, str(log_path)
        else:
            return f"Failed to read log file: {result.stderr}", str(log_path)

    except subprocess.TimeoutExpired:
        return f"Timeout reading log file: {log_path}", str(log_path)
    except PermissionError:
        return f"Permission denied: {log_path}", str(log_path)
    except Exception as e:
        logger.error(f"Error collecting agent logs: {e}")
        return f"Error collecting logs: {e}", str(log_path)


def collect_compose_container_logs(tail_lines: int = 500) -> dict[str, str]:
    """
    Collect logs from all containers in the recurve_services docker-compose project.

    Args:
        tail_lines: Number of lines to read from the end of each container log.

    Returns:
        A dictionary with keys in format "{container_name}_logs" and values
        containing the log content or error message for each container.
    """
    result = {}

    try:
        # Get all containers with the recurve_services compose project label
        containers = docker_client.containers.list(
            all=True, filters={"label": f"com.docker.compose.project={COMPOSE_PROJECT_NAME}"}
        )

        if not containers:
            return result

        # Collect logs from each container
        for container in containers:
            # Use container name directly as key, append _logs suffix
            key = f"{container.name}_logs"

            try:
                # Get logs from the container
                logs = container.logs(tail=tail_lines, stdout=True, stderr=True, timestamps=False)

                # Decode bytes to string
                if isinstance(logs, bytes):
                    logs = logs.decode("utf-8", errors="replace")

                result[key] = logs
            except Exception as e:
                error_msg = f"Error collecting logs from {container.name}: {e}"
                logger.error(error_msg)
                result[key] = error_msg

    except Exception as e:
        logger.error(f"Error collecting compose container logs: {e}")
        result["error_logs"] = f"Docker API error: {e}"

    return result


def format_log_collection_response(
    tail_lines: int = 500,
) -> dict[str, str | None]:
    """
    Format log collection response for both Agent and all compose containers.

    Args:
        tail_lines: Number of lines to read from the end of logs.

    Returns:
        A dictionary with agent_logs and container_{id}_logs keys for each container.
        All log keys end with "_logs" as required by Gateway.
    """
    agent_logs, agent_log_path = collect_agent_logs(tail_lines)
    container_logs = collect_compose_container_logs(tail_lines)

    # Build response with agent logs and all container logs
    response = {
        "agent_logs": agent_logs,
        "agent_log_path": str(agent_log_path),
    }
    response.update(container_logs)

    return response
