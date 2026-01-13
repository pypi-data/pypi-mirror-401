import os
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict

class TemplateService:
    """Service for applying project templates."""
    
    TEMPLATES = {
        "react-vite": "Create a React app using Vite + TailwindCSS",
        "python-fastapi": "Create a Python FastAPI backend",
        "python-basic": "Create a basic Python project",
        "nextjs": "Create a Next.js application"
    }

    @classmethod
    def list_templates(cls) -> Dict[str, str]:
        return cls.TEMPLATES

    @classmethod
    async def apply_template(cls, template_name: str, project_path: Path, extra_context: Optional[Dict] = None):
        """Apply a template to the given project path."""
        if template_name not in cls.TEMPLATES:
            raise ValueError(f"Unknown template: {template_name}")
            
        method_name = f"_apply_{template_name.replace('-', '_')}"
        if hasattr(cls, method_name):
            await getattr(cls, method_name)(project_path)
        else:
            raise NotImplementedError(f"Template implementation missing for {template_name}")

    @staticmethod
    async def _run_command(command: str, cwd: Path):
        """Run a shell command asynchronously."""
        process = await asyncio.create_subprocess_shell(
            command,
            cwd=str(cwd),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise RuntimeError(f"Command failed: {command}\nError: {stderr.decode()}")
        return stdout.decode()

    @classmethod
    async def _apply_react_vite(cls, cwd: Path):
        """Apply React+Vite+Tailwind."""
        # Note: 'npm create vite' prompts for input unless we pass flags.
        # We use 'vite' template.
        print(f"Applying React-Vite template to {cwd}")
        
        # 1. Scaffolding
        # If directory is empty (except .agentic), we can use '.'
        # But 'npm create vite' might complain. 
        # Better to run it and output to temp, then move? 
        # Or use 'npm create vite@latest . -- --template react' if supported?
        # Yes, 'npm create vite@latest . -- --template react' works if dir is empty.
        
        # Check if empty (ignore .agentic)
        has_files = any(p.name != ".agentic" for p in cwd.iterdir())
        if has_files:
             raise RuntimeError("Project directory must be empty to apply template.")

        # Allow insecure if needed? No, assumes user has node.
        # Use --yes to skip confirmation
        cmd = "npm create vite@latest . -- --template react"
        await cls._run_command(cmd, cwd)
        
        # 2. Tailwind Setup (Simplified)
        await cls._run_command("npm install", cwd)
        await cls._run_command("npm install -D tailwindcss postcss autoprefixer", cwd)
        await cls._run_command("npx tailwindcss init -p", cwd)
        
        # Update index.css
        index_css = cwd / "src" / "index.css"
        if index_css.exists():
            index_css.write_text(
                "@tailwind base;\n@tailwind components;\n@tailwind utilities;\n" + index_css.read_text()
            )

    @classmethod
    async def _apply_python_fastapi(cls, cwd: Path):
        """Apply FastAPI template."""
        # 1. Structure
        (cwd / "app").mkdir()
        (cwd / "app" / "__init__.py").touch()
        
        # 2. Files
        (cwd / "requirements.txt").write_text("fastapi\nuvicorn\n")
        
        main_py = """
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
"""
        (cwd / "app" / "main.py").write_text(main_py.strip())
        
        # 3. README
        (cwd / "README.md").write_text("# FastAPI Project\n\nRun with `uvicorn app.main:app --reload`")

    @classmethod
    async def _apply_python_basic(cls, cwd: Path):
        """Apply Basic Python."""
        (cwd / "main.py").write_text("print('Hello World')")
        (cwd / "requirements.txt").touch()

    @classmethod
    async def _apply_nextjs(cls, cwd: Path):
        """Apply Next.js."""
        # npx create-next-app@latest . --typescript --eslint --tailwind --no-src-dir --import-alias "@/*" --app --use-npm --yes
        cmd = "npx create-next-app@latest . --typescript --eslint --tailwind --no-src-dir --import-alias '@/*' --app --use-npm --yes"
        await cls._run_command(cmd, cwd)

import asyncio
