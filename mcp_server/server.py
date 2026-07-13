from mcp.server.fastmcp import FastMCP
from app.core.config import get_settings
from app.services.repository_service import RepositoryService

mcp = FastMCP("AI Coding Agent")
service = RepositoryService(get_settings())

@mcp.tool()
def list_repository_files(repository_path: str = ".") -> list[str]:
    """List safe source and text files."""
    return service.list_files(repository_path)

@mcp.tool()
def read_repository_file(relative_path: str, repository_path: str = ".") -> str:
    """Read one safe repository file."""
    return service.read_file(repository_path, relative_path)

@mcp.tool()
def search_repository(query: str, repository_path: str = ".") -> list[str]:
    """Search repository filenames and text."""
    return service.search(repository_path, query)

@mcp.tool()
def summarize_repository(repository_path: str = ".") -> str:
    """Return a compact repository tree and selected contents."""
    return service.snapshot(repository_path, "architecture entry point configuration tests", 12, 25000).context

if __name__ == "__main__":
    mcp.run(transport="stdio")
