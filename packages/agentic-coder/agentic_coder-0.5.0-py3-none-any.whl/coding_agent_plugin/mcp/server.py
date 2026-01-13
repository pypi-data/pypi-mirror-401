"""
Internal MCP Server for Project Resources.

This module implements a Model Context Protocol (MCP) server that exposes
project files as resources and provides search capabilities.
"""

import os
import asyncio
from typing import List, Optional
from pathlib import Path

# Try to import FastMCP, fallback or mock if not available (since we just added the dependency)
try:
    from mcp.server.fastmcp import FastMCP
    from mcp.server.fastmcp import Context
except ImportError:
    # If mcp is not installed in the environment yet, we might need to rely on what's available
    # or fail gracefully. For now, assuming it will be available or we use a basic structure.
    # This is a placeholder for the actual implementation using the mcp library.
    class FastMCP:
        def __init__(self, name): self.name = name
        def resource(self, uri): return lambda f: f
        def tool(self): return lambda f: f
        def run(self): print("Mock MCP Server Running")

from coding_agent_plugin.managers import ProjectManager

# Initialize FastMCP server
mcp = FastMCP("agentic-coder-resources")

@mcp.resource("project://{project_id}/{file_path}")
def read_project_file(project_id: str, file_path: str) -> str:
    """
    Read the content of a file in a project.
    
    Args:
        project_id: ID of the project
        file_path: Relative path to the file
    """
    pm = ProjectManager()
    project = pm.get_project(project_id)
    
    if not project:
        raise ValueError(f"Project '{project_id}' not found")
        
    storage_path = Path(project["storage_path"])
    full_path = storage_path / file_path
    
    # Security check: ensure file is within project directory
    try:
        full_path.resolve().relative_to(storage_path.resolve())
    except ValueError:
        raise ValueError("Access denied: File outside project directory")
        
    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
        
    return full_path.read_text(encoding="utf-8")

@mcp.tool()
def list_project_files(project_id: str) -> List[str]:
    """
    List all files in a project.
    
    Args:
        project_id: ID of the project
    """
    pm = ProjectManager()
    return pm.list_files(project_id)

@mcp.tool()
def search_code(project_id: str, query: str) -> List[str]:
    """
    Search for a string in all files of a project.
    
    Args:
        project_id: ID of the project
        query: String to search for
        
    Returns:
        List of strings formatting as "file_path:line_number: content"
    """
    pm = ProjectManager()
    project = pm.get_project(project_id)
    
    if not project:
        raise ValueError(f"Project '{project_id}' not found")
        
    storage_path = Path(project["storage_path"])
    results = []
    
    # Using ripgrep-like search (simple python implementation for now)
    # In a real scenario, use `grep` or `rg` for performance
    for file_path in pm.list_files(project_id):
        full_path = storage_path / file_path
        try:
            lines = full_path.read_text(encoding="utf-8").splitlines()
            for i, line in enumerate(lines, 1):
                if query.lower() in line.lower():
                    results.append(f"{file_path}:{i}: {line.strip()}")
                    if len(results) >= 50:  # Limit results
                        return results
        except Exception:
            continue  # Skip binary or unreadable files
            
    return results

def start_resource_server():
    """Start the MCP resource server."""
    mcp.run()

if __name__ == "__main__":
    start_resource_server()
