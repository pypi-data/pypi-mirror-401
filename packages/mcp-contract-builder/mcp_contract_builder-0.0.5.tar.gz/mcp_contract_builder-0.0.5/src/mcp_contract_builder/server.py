from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from .runtime.builder import build_contract


def build_server() -> FastMCP:
    server = FastMCP(log_level="ERROR")

    @server.tool(name="contract_build")
    def contract_build(cwd: str, query: str, mode: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        res = build_contract(cwd=cwd, query=query, mode=mode)
        return res.to_dict()

    return server


def run_server(*, transport: str = "stdio") -> None:
    if transport != "stdio":
        raise ValueError("unsupported transport")
    build_server().run(transport=transport)
