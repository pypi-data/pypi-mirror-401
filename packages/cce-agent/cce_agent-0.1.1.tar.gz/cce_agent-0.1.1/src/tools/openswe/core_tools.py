"""
Core Open SWE Tools

Basic tools for shell execution, HTTP requests, and web search.
These are the fundamental building blocks for software engineering tasks.
"""

import asyncio
import logging
import os
from typing import Any

import aiohttp
from langchain_core.tools import tool

from .command_safety import validate_command_safety

logger = logging.getLogger(__name__)


@tool
async def execute_bash(command: str, timeout: int = 180) -> dict[str, Any]:
    """
    Execute a bash command and return the result.
    Includes safety validation to prevent prompt injection and malicious commands.

    Args:
        command: The bash command to execute
        timeout: Timeout in seconds (default: 30)

    Returns:
        Dictionary containing execution results
    """
    try:
        # Validate command safety
        safety_validation = await validate_command_safety(command)

        if not safety_validation.get("is_safe", False):
            return {
                "success": False,
                "result": f"Command blocked - safety validation failed: {safety_validation.get('reasoning', 'Unknown reason')}",
                "status": "error",
            }

        # Execute the command
        process = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
        except TimeoutError:
            process.kill()
            await process.wait()
            return {"success": False, "result": f"Command timed out after {timeout} seconds", "status": "error"}

        stdout_str = stdout.decode("utf-8") if stdout else ""
        stderr_str = stderr.decode("utf-8") if stderr else ""

        if process.returncode != 0:
            return {
                "success": False,
                "result": stderr_str or stdout_str,
                "status": "error",
                "exit_code": process.returncode,
            }

        return {"success": True, "result": stdout_str, "status": "success", "exit_code": 0}

    except Exception as e:
        return {"success": False, "result": f"Error executing command: {str(e)}", "status": "error"}


@tool
async def http_request(
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Make an HTTP request to a URL.

    Args:
        url: The URL to make the request to
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        headers: Optional headers dictionary
        data: Optional data dictionary for POST/PUT requests

    Returns:
        Dictionary containing the HTTP response
    """
    try:
        async with aiohttp.ClientSession() as session:
            kwargs = {"url": url, "headers": headers or {}, "timeout": aiohttp.ClientTimeout(total=30)}

            if data and method.upper() in ["POST", "PUT", "PATCH"]:
                kwargs["json"] = data

            async with session.request(method.upper(), **kwargs) as response:
                try:
                    response_data = await response.json()
                except:
                    response_data = await response.text()

                return {
                    "success": response.status < 400,
                    "status_code": response.status,
                    "headers": dict(response.headers),
                    "data": response_data,
                    "status": "success" if response.status < 400 else "error",
                }

    except Exception as e:
        return {"success": False, "result": f"HTTP request failed: {str(e)}", "status": "error"}


@tool
async def web_search(query: str, max_results: int = 5) -> dict[str, Any]:
    """
    Search the web for information using Tavily API.

    Args:
        query: The search query
        max_results: Maximum number of results to return (default: 5)

    Returns:
        Dictionary containing search results
    """
    try:
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if not tavily_api_key:
            return {
                "success": False,
                "result": "Tavily API key not found. Please set TAVILY_API_KEY environment variable.",
                "status": "error",
            }

        async with aiohttp.ClientSession() as session:
            payload = {
                "api_key": tavily_api_key,
                "query": query,
                "search_depth": "basic",
                "include_answer": True,
                "include_images": False,
                "include_raw_content": False,
                "max_results": max_results,
            }

            async with session.post(
                "https://api.tavily.com/search", json=payload, timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status != 200:
                    return {"success": False, "result": f"Tavily API error: {response.status}", "status": "error"}

                data = await response.json()

                # Format results
                results = []
                for result in data.get("results", []):
                    results.append(
                        {
                            "title": result.get("title", ""),
                            "url": result.get("url", ""),
                            "content": result.get("content", ""),
                        }
                    )

                return {
                    "success": True,
                    "results": results,
                    "answer": data.get("answer", ""),
                    "query": query,
                    "status": "success",
                }

    except Exception as e:
        return {"success": False, "result": f"Web search failed: {str(e)}", "status": "error"}


__all__ = ["execute_bash", "http_request", "web_search"]
