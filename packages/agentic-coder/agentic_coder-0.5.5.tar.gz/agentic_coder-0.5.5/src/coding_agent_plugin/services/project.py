"""Project service that delegates to File-System based ProjectManager."""

from coding_agent_plugin.schemas.project import ProjectSchema
from coding_agent_plugin.managers import ProjectManager
from ..models.project import ProjectCreate, ProjectUpdate, ProjectResponse
from typing import List, Optional

class ProjectService:
    """Service for project business logic, wrapping FS-based ProjectManager."""

    def __init__(self):
        self.pm = ProjectManager()

    async def create(self, project_data: ProjectCreate) -> ProjectResponse:
        """Create a new project."""
        from coding_agent_plugin.services.template import TemplateService
        from pathlib import Path
        
        # ProjectManager is synchronous in this implementation, which is fine for FS ops
        # In a high-perf async API you might use run_in_executor, but simple delegation is okay here.
        # Note: project_data uses project_name or name? Model says project_name, Service used name.
        # Adjusted to use project_name from model
        name = getattr(project_data, "project_name", getattr(project_data, "name", "Untitled"))
        
        project_dict = self.pm.create_project(name, project_data.description)
        
        # Apply Template if requested
        if hasattr(project_data, "template") and project_data.template:
             project_path = Path(project_dict["storage_path"])
             await TemplateService.apply_template(project_data.template, project_path)
             
        return self._to_response(project_dict)

    async def get_by_id(self, project_id: str) -> Optional[ProjectResponse]:
        """Get project by ID."""
        project_dict = self.pm.get_project(project_id)
        if not project_dict:
            return None
        return self._to_response(project_dict)

    async def get_by_name(self, project_name: str) -> Optional[ProjectResponse]:
        """Get project by name."""
        project_dict = self.pm.get_project(project_name)
        if not project_dict:
            return None
        return self._to_response(project_dict)

    async def list_all(self) -> List[ProjectResponse]:
        """List all projects."""
        projects = self.pm.list_projects()
        return [self._to_response(p) for p in projects]

    async def update(self, project_id: str, update_data: ProjectUpdate) -> Optional[ProjectResponse]:
        """Update project (Not fully implemented in ProjectManager yet)."""
        # For now, just return get logic or implement partial update if needed
        # In FS mode, we'd read/write JSON. 
        # Since user only asked for storage location change, we keep it simple.
        current = self.pm.get_project(project_id)
        if not current:
            return None
            
        # TODO: Implement update in ProjectManager if needed. 
        # For now, we assume simple metadata updates aren't critical or we do manual patch.
        return self._to_response(current)

    async def delete(self, project_id: str) -> bool:
        """Delete project."""
        return self.pm.delete_project(project_id)

    @classmethod
    async def create_project(cls, *args, **kwargs):
        """Alias for create."""
        instance = cls()
        # Handle loose args? Adapt as needed.
        # This alias might be called differently. Let's assume standard usage.
        return await instance.create(*args, **kwargs)
        
    def _to_response(self, data: dict) -> ProjectResponse:
        """Convert dict directly to Response model, bypassing Schema if possible."""
        # If ProjectResponse expects specific fields from a DB schema, we might need to map them.
        # Assuming ProjectResponse is Pydantic compatible with our dict.
        return ProjectResponse(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            storage_path=data.get("storage_path"),
            # Add defaults for missing fields
            git_configured=False 
        )

project_service = ProjectService()
