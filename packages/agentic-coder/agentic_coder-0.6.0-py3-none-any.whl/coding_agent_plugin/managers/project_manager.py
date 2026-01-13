"""Project manager for creating and managing projects."""

import json
import uuid
import shutil
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime

class ProjectManager:
    """Manages project creation, listing, and switching using the File System."""
    
    def __init__(self):
        """Initialize project manager."""
        from coding_agent_plugin.core.config import AGENTIC_PROJECTS_DIR
        
        # Use configured projects directory
        self.projects_dir = Path(AGENTIC_PROJECTS_DIR).resolve()
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_project_path(self, project_id: str) -> Path:
        """Get path for a project ID."""
        return self.projects_dir / project_id
        
    def _read_metadata(self, project_dir: Path) -> Optional[Dict]:
        """Read project metadata from config.json."""
        config_file = project_dir / ".agentic" / "config.json"
        if not config_file.exists():
            return None
        try:
            return json.loads(config_file.read_text())
        except:
            return None

    def create_project(self, name: str, description: Optional[str] = None) -> Dict:
        """
        Create a new project folder and metadata.
        """
        # unexpected, but check if name exists in scanning? 
        # For simplicity in FS mode, we allow duplicates names but different IDs, 
        # or we scan. Let's scan to enforce unique names if possible, but 
        # for performance, unique ID is safer.
        
        project_id = str(uuid.uuid4())
        project_dir = self.projects_dir / project_id
        
        # Create directory structure
        project_dir.mkdir(parents=True, exist_ok=True)
        metadata_dir = project_dir / ".agentic"
        metadata_dir.mkdir(exist_ok=True)
        
        # Metadata
        metadata = {
            "id": project_id,
            "name": name,
            "description": description,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "storage_path": str(project_dir),
            "version": "1.0"
        }
        
        # Write config
        (metadata_dir / "config.json").write_text(json.dumps(metadata, indent=2))
        
        return metadata
    
    def list_projects(self) -> List[Dict]:
        """
        List all projects by scanning folders.
        """
        projects = []
        if not self.projects_dir.exists():
            return []
            
        for path in self.projects_dir.iterdir():
            if path.is_dir():
                # Check for metadata
                meta = self._read_metadata(path)
                if meta:
                    projects.append(meta)
        
        # Sort by created_at desc
        return sorted(projects, key=lambda x: x.get("created_at", ""), reverse=True)
    
    def get_project(self, name_or_id: str) -> Optional[Dict]:
        """
        Get project by name or ID.
        """
        # 1. Direct ID check (fast)
        potential_dir = self.projects_dir / name_or_id
        if potential_dir.exists():
             meta = self._read_metadata(potential_dir)
             if meta: 
                 return meta
        
        # 2. Name search (scan)
        for proj in self.list_projects():
            if proj["name"] == name_or_id or proj["id"] == name_or_id:
                return proj
                
        return None
    
    def delete_project(self, name_or_id: str) -> bool:
        """Delete a project folder."""
        project = self.get_project(name_or_id)
        if not project:
            return False
            
        path = Path(project["storage_path"])
        if path.exists():
            shutil.rmtree(path)
        return True
    
    def get_current_project(self) -> Optional[str]:
        """
        Get current active project name from a local state file.
        In FS mode, we store this in ~/.agentic-coder/.state.json or similar.
        """
        from coding_agent_plugin.models.database import AGENTIC_HOME # We can still use the home dir
        state_file = Path(AGENTIC_HOME) / "state.json"
        if state_file.exists():
            try:
                data = json.loads(state_file.read_text())
                return data.get("current_project")
            except:
                return None
        return None
    
    def set_current_project(self, name_or_id: str) -> bool:
        """Set current active project."""
        project = self.get_project(name_or_id)
        if not project:
            return False
            
        from coding_agent_plugin.models.database import AGENTIC_HOME
        state_file = Path(AGENTIC_HOME) / "state.json"
        
        current_state = {}
        if state_file.exists():
            try:
                current_state = json.loads(state_file.read_text())
            except:
                pass
                
        current_state["current_project"] = project["name"]
        state_file.write_text(json.dumps(current_state))
        return True
    
    def get_project_stats(self, name_or_id: str) -> Optional[Dict]:
        """Get project statistics."""
        project = self.get_project(name_or_id)
        if not project:
            return None
        
        storage_path = Path(project["storage_path"])
        
        file_count = 0
        total_size = 0
        
        if storage_path.exists():
            for file in storage_path.rglob("*"):
                if file.is_file() and ".agentic" not in str(file):
                    file_count += 1
                    total_size += file.stat().st_size
        
        return {
            **project,
            "file_count": file_count,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }
    
    def list_files(self, name_or_id: str) -> List[str]:
        """List files in project."""
        project = self.get_project(name_or_id)
        if not project:
            return []
            
        base_path = Path(project["storage_path"])
        if not base_path.exists():
             return []
             
        files = []
        for path in base_path.rglob("*"):
            if path.is_file():
                rel_path = path.relative_to(base_path)
                # Filter hidden
                if any(p.startswith(".") for p in rel_path.parts):
                    continue
                if "__pycache__" in rel_path.parts:
                    continue
                files.append(str(rel_path))
        return sorted(files)
