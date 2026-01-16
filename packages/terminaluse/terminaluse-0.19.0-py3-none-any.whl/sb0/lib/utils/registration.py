import os
import json
import base64
import asyncio

import httpx

from sb0.lib.utils.logging import make_logger
from sb0.lib.environment_variables import EnvironmentVariables

logger = make_logger(__name__)


def get_auth_principal(env_vars: EnvironmentVariables):
    if not env_vars.AUTH_PRINCIPAL_B64:
        return None

    try:
        decoded_str = base64.b64decode(env_vars.AUTH_PRINCIPAL_B64).decode("utf-8")
        return json.loads(decoded_str)
    except Exception:
        return None


def get_build_info():
    build_info_path = os.environ.get("BUILD_INFO_PATH")
    logger.info(f"Getting build info from {build_info_path}")
    if not build_info_path:
        return None
    try:
        with open(build_info_path, "r") as f:
            return json.load(f)
    except Exception:
        return None


async def register_agent(env_vars: EnvironmentVariables):
    """Register this container with the Sb0 server.

    This function registers the container's deployment/version with the platform.
    The container must have SB0_DEPLOYMENT_ID and SB0_VERSION_ID environment
    variables set (provided by the platform during deployment via Helm).

    On success, stores agent_id, agent_name, agent_api_key, and deployment_id
    in environment variables for use by the application.
    """
    if not env_vars.SB0_BASE_URL:
        logger.warning("SB0_BASE_URL is not set, skipping registration")
        return

    # Deployment context is required - these are set by the platform during deploy
    if not env_vars.SB0_DEPLOYMENT_ID or not env_vars.SB0_VERSION_ID:
        logger.warning(
            "SB0_DEPLOYMENT_ID or SB0_VERSION_ID not set, skipping registration. "
            "These are required for deployment-based registration."
        )
        return

    # Build the agent's ACP URL
    full_acp_url = f"{env_vars.ACP_URL.rstrip('/')}:{env_vars.ACP_PORT}"

    # Prepare deployment-centric registration data
    registration_data = {
        "deployment_id": env_vars.SB0_DEPLOYMENT_ID,
        "version_id": env_vars.SB0_VERSION_ID,
        "acp_url": full_acp_url,
    }

    # New endpoint for deployment-based registration
    registration_url = f"{env_vars.SB0_BASE_URL.rstrip('/')}/deployments/register"

    # Retry logic with configurable attempts and delay
    max_retries = 3
    base_delay = 5  # seconds
    last_exception = None

    attempt = 0
    while attempt < max_retries:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(registration_url, json=registration_data, timeout=30.0)
                if response.status_code == 200:
                    result = response.json()

                    # Extract agent info from response
                    agent_id = result["agent_id"]
                    agent_name = result["agent_name"]
                    agent_api_key = result["agent_api_key"]
                    deployment_id = result["deployment_id"]

                    # Store in environment for application use
                    os.environ["AGENT_ID"] = agent_id
                    os.environ["AGENT_NAME"] = agent_name
                    os.environ["AGENT_API_KEY"] = agent_api_key
                    os.environ["SB0_DEPLOYMENT_ID"] = deployment_id

                    # Update env_vars object
                    env_vars.AGENT_ID = agent_id
                    env_vars.AGENT_NAME = agent_name
                    env_vars.AGENT_API_KEY = agent_api_key
                    env_vars.SB0_DEPLOYMENT_ID = deployment_id

                    # Update the cached environment variables so sandbox has access
                    EnvironmentVariables.set_cached(env_vars)

                    logger.info(
                        f"Successfully registered container for deployment '{deployment_id}' "
                        f"agent '{agent_name}' with acp_url: {full_acp_url}"
                    )
                    return  # Success, exit the retry loop
                else:
                    error_msg = f"Failed to register container. Status: {response.status_code}, Response: {response.text}"
                    logger.error(error_msg)
                    last_exception = Exception(f"Failed to register container: {response.text}")

        except Exception as e:
            logger.error(f"Exception during container registration attempt {attempt + 1}: {e}")
            last_exception = e

        attempt += 1
        if attempt < max_retries:
            delay = attempt * base_delay  # 5, 10, 15 seconds
            logger.info(f"Retrying in {delay} seconds... (attempt {attempt}/{max_retries})")
            await asyncio.sleep(delay)

    # If we get here, all retries failed
    raise last_exception or Exception(f"Failed to register container after {max_retries} attempts")
