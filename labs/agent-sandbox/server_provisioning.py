#!/usr/bin/env python3
"""Server Provisioning Agent - MCP Tools Demo."""

import logging

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

import agentic_llm_labs.logging

# Initialize logging
agentic_llm_labs.logging.colorized_config(level=logging.INFO)
logger = logging.getLogger("mcp_server")
logger.info("Starting Server Provisioning MCP Tools...")

# Initialize FastMCP
mcp = FastMCP("server_provisioning")


# --------------------------------------------------------------------------------------
# Tools
# --------------------------------------------------------------------------------------

# Define your tools here. For demonstration purposes, we'll define a simple tool.
# In a real-world scenario, these would be more complex and interact with actual systems.

# -----------------------------------------------------------------------------
# Provision Server Tool
# -----------------------------------------------------------------------------


class ProvisionedServer(BaseModel):
    server_name: str = Field(..., description="The name of the provisioned server")
    cpu_cores: int = Field(..., description="Number of CPU cores")
    memory_gb: int = Field(..., description="Memory in GB")
    storage_gb: int = Field(..., description="Storage in GB")
    vlan_name: str = Field(
        ..., description="The name of the VLAN the server is attached to"
    )
    status: str = Field(default="provisioned", description="Status of the server")


@mcp.tool()
def provision_server(
    server_name: str = Field(..., description="The name of the server to provision"),
    cpu_cores: int = Field(..., description="Number of CPU cores"),
    memory_gb: int = Field(..., description="Amount of memory in GB"),
    storage_gb: int = Field(..., description="Amount of storage in GB"),
    vlan_name: str = Field(
        ..., description="The name of the VLAN to attach the server to"
    ),
) -> ProvisionedServer:
    """Provisions a new server with the specified resources.
    Args:
        server_name (str): The name of the server to provision.
        cpu_cores (int): Number of CPU cores.
        memory_gb (int): Amount of memory in GB.
        storage_gb (int): Amount of storage in GB.
        vlan_name (str): The name of the VLAN to attach the server to.
    Returns:
        ProvisionedServer: Details of the provisioned server.
    """
    logger.warning(
        f"Provisioning server '{server_name}' with {cpu_cores} CPU cores, "
        f"{memory_gb}GB memory, and {storage_gb}GB storage on VLAN '{vlan_name}'."
    )
    # Here you would add the logic to provision the server.
    # For demonstration, we'll just return a success message.

    return ProvisionedServer(
        server_name=server_name,
        cpu_cores=cpu_cores,
        memory_gb=memory_gb,
        storage_gb=storage_gb,
        vlan_name=vlan_name,
        status="provisioning",
    )


# -----------------------------------------------------------------------------
# Provision VLAN Tool
# -----------------------------------------------------------------------------


class ProvisionedVLAN(BaseModel):
    vlan_id: int = Field(..., description="The ID of the VLAN")
    name: str = Field(..., description="The name of the VLAN")
    cidr: str = Field(..., description="The CIDR block for the VLAN")
    status: str = Field(default="provisioned", description="Status of the VLAN")


@mcp.tool()
def provision_vlan(
    vlan_id: int = Field(..., description="The ID of the VLAN to create"),
    name: str = Field(..., description="The name of the VLAN to create"),
    cidr: str = Field(..., description="The CIDR block for the VLAN"),
) -> ProvisionedVLAN:
    logger.warning(f"Provisioning VLAN {vlan_id} '{name}' with CIDR block {cidr}.")
    # Here you would add the logic to provision the VLAN.
    # For demonstration, we'll just return a success message.

    return ProvisionedVLAN(vlan_id=vlan_id, name=name, cidr=cidr, status="provisioned")


# --------------------------------------------------------------------------------------
# Main - Start MCP Server
# --------------------------------------------------------------------------------------


def main():
    # mcp.run(transport="stdio")
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Shutting down Server Provisioning MCP Tools...")
