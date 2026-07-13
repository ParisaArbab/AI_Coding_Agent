from langchain_core.tools import tool
from app.services.repository_service import RepositoryService

def build_repository_tools(service: RepositoryService, repository_path: str):
    @tool
    def list_repository_files() -> list[str]:
        """List safe text and source files in the repository."""
        return service.list_files(repository_path)
    @tool
    def read_repository_file(relative_path: str) -> str:
        """Read one safe file using a repository-relative path."""
        return service.read_file(repository_path, relative_path)
    @tool
    def search_repository(query: str) -> list[str]:
        """Search repository filenames and text contents."""
        return service.search(repository_path, query)
    return [list_repository_files, read_repository_file, search_repository]
