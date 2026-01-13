"""Project context system for understanding existing projects."""

import os
from pathlib import Path
from typing import Dict, List, Optional
import json


class ProjectContext:
    """Manages context and understanding of an existing project."""
    
    def __init__(self, project_path: str):
        """
        Initialize project context.
        
        Args:
            project_path: Path to the project directory
        """
        self.project_path = Path(project_path)
        self.files: Dict[str, str] = {}
        self.structure: Dict[str, List[str]] = {}
        self.agent_context_path = self.project_path / ".agent_context"
        
    def is_valid_project(self) -> bool:
        """Check if this is a valid coding-agent project."""
        return (self.agent_context_path.exists() and 
                (self.agent_context_path / "planning.md").exists())
    
    def load_project(self) -> bool:
        """
        Load and analyze the project structure (metadata only).
        
        Returns:
            bool: True if successful
        """
        try:
            # Scan all files (excluding hidden and common dirs to ignore)
            ignore_dirs = {".git", ".agent_context", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}
            ignore_exts = {".pyc", ".pyo", ".db", ".sqlite", ".log", ".DS_Store"}
            
            for root, dirs, files in os.walk(self.project_path):
                # Remove ignored directories from search
                dirs[:] = [d for d in dirs if d not in ignore_dirs]
                
                rel_root = Path(root).relative_to(self.project_path)
                
                for file in files:
                    file_path = Path(root) / file
                    
                    # Skip ignored extensions
                    if file_path.suffix in ignore_exts:
                        continue
                    
                    rel_path = str(file_path.relative_to(self.project_path))
                    
                    # Store valid file path in structure but DO NOT read content
                    directory = str(Path(rel_path).parent)
                    if directory not in self.structure:
                        self.structure[directory] = []
                    self.structure[directory].append(Path(rel_path).name)
            
            return True
            
        except Exception as e:
            print(f"Error loading project: {e}")
            return False
            
    def file_iterator(self):
        """
        Generator that yields (relative_path, content) for all valid files.
        Lazy loads content from disk one by one.
        """
        for directory, files in self.structure.items():
            for filename in files:
                rel_path = Path(directory) / filename
                abs_path = self.project_path / rel_path
                
                try:
                    with open(abs_path, 'r', encoding='utf-8') as f:
                        yield (str(rel_path), f.read())
                except (UnicodeDecodeError, PermissionError):
                    continue
    
    def get_file_content(self, file_path: str) -> Optional[str]:
        """Get content of a specific file (reads on demand)."""
        try:
            abs_path = self.project_path / file_path
            if abs_path.exists():
                with open(abs_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception:
            pass
        return None
    
    def get_files_by_extension(self, extension: str) -> List[str]:
        """Get all files with a specific extension."""
        results = []
        for directory, files in self.structure.items():
            for f in files:
                if f.endswith(extension):
                    path = Path(directory) / f
                    results.append(str(path))
        return results
    
    def get_main_files(self) -> List[str]:
        """Get likely main entry point files."""
        main_names = {"main.py", "app.py", "index.py", "__init__.py", "server.py"}
        results = []
        for directory, files in self.structure.items():
            for f in files:
                if f in main_names:
                    path = Path(directory) / f
                    results.append(str(path))
        return results
    
    def get_project_summary(self) -> str:
        """Get a summary of the project structure."""
        summary_parts = []
        
        total_files = sum(len(files) for files in self.structure.values())
        summary_parts.append(f"Project Path: {self.project_path}")
        summary_parts.append(f"\nTotal Files: {total_files}")
        
        # Directory structure (truncated if too large)
        summary_parts.append("\nDirectory Structure:")
        for directory, files in sorted(self.structure.items())[:50]:
            if directory == ".":
                summary_parts.append(f"  / ({len(files)} files)")
            else:
                summary_parts.append(f"  {directory}/ ({len(files)} files)")
                
        if len(self.structure) > 50:
            summary_parts.append(f"  ... + {len(self.structure) - 50} more directories")
        
        return "\n".join(summary_parts)

    def save_conversation_history(self, request: str, changes: List[Dict]) -> bool:
        """
        Save a conversation turn to history.
        """
        try:
            history_file = self.agent_context_path / "conversation.json"
            
            # Load existing history
            if history_file.exists():
                with open(history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = {"sessions": []}
            
            # Add new session
            import datetime
            history["sessions"].append({
                "timestamp": datetime.datetime.now().isoformat(),
                "request": request,
                "changes": changes
            })
            
            # Save
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Warning: Failed to save history: {e}")
            return False
