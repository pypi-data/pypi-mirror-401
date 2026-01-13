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
        "nextjs": "Create a Next.js application",
        "go-gin": "Create a Go API with Gin",
        "rust-actix": "Create a Rust API with Actix-Web",
        "express-api": "Create a Node.js Express API (TypeScript)"
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

    @staticmethod
    def _check_tool(tool_name: str):
        """Check if a tool is installed."""
        if not shutil.which(tool_name):
            raise RuntimeError(
                f"Required tool '{tool_name}' is not installed.\n"
                f"Please install it to use this template."
            )

    @classmethod
    async def _apply_react_vite(cls, cwd: Path):
        """Apply React+Vite+Tailwind."""
        cls._check_tool("npm")
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
        cls._check_tool("npm")
        # npx create-next-app@latest . --typescript --eslint --tailwind --no-src-dir --import-alias "@/*" --app --use-npm --yes
        cmd = "npx create-next-app@latest . --typescript --eslint --tailwind --no-src-dir --import-alias '@/*' --app --use-npm --yes"
        await cls._run_command(cmd, cwd)

    @classmethod
    async def _apply_go_gin(cls, cwd: Path):
        """Apply Go + Gin template."""
        cls._check_tool("go")
        # 1. Initialize Go Module
        project_name = cwd.name
        await cls._run_command(f"go mod init {project_name}", cwd)
        
        # 2. Files
        main_go = """
package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func main() {
	r := gin.Default()
	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "Hello from Agentic Coder!",
		})
	})
	r.Run() // listen on 0.0.0.0:8080
}
"""
        (cwd / "main.go").write_text(main_go.strip())
        
        # 3. Dependencies
        await cls._run_command("go get -u github.com/gin-gonic/gin", cwd)
        # Tidy up
        await cls._run_command("go mod tidy", cwd)


    @classmethod
    async def _apply_rust_actix(cls, cwd: Path):
        """Apply Rust + Actix template."""
        cls._check_tool("cargo")
        # Cargo expects directory to be empty-ish or we use 'cargo init'
        # 'cargo init' works in existing directory
        await cls._run_command("cargo init --bin", cwd)
        
        # Add dependency to Cargo.toml
        cargo_toml = cwd / "Cargo.toml"
        content = cargo_toml.read_text()
        if "[dependencies]" not in content:
            content += "\n[dependencies]\n"
        content += 'actix-web = "4"\n'
        cargo_toml.write_text(content)
        
        # Main.rs
        main_rs = """
use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};

#[get("/")]
async def hello() -> impl Responder {
    HttpResponse::Ok().body("Hello from Agentic Coder (Rust)!")
}

#[actix_web::main]
async def main() -> std::io::Result<()> {
    println!("Server running at http://127.0.0.1:8080/");
    HttpServer::new(|| {
        App::new()
            .service(hello)
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
"""
        src = cwd / "src"
        src.mkdir(exist_ok=True)
        (src / "main.rs").write_text(main_rs.strip())

    @classmethod
    async def _apply_express_api(cls, cwd: Path):
        """Apply Node/Express/TS template."""
        cls._check_tool("npm")
        # Init package.json
        await cls._run_command("npm init -y", cwd)
        
        # Install deps (Express, TS)
        await cls._run_command("npm install express cors dotenv", cwd)
        await cls._run_command("npm install -D typescript ts-node @types/node @types/express @types/cors", cwd)
        
        # tsconfig.json
        await cls._run_command("npx tsc --init", cwd)
        
        # Source
        (cwd / "src").mkdir()
        
        index_ts = """
import express, { Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get('/', (req: Request, res: Response) => {
  res.json({ message: 'Hello from Agentic Coder (Express)' });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
"""
        (cwd / "src" / "index.ts").write_text(index_ts.strip())
        
        # Update package.json scripts
        pkg_path = cwd / "package.json"
        # Simplistic string replace, robust solution would parse JSON
        # Assuming defaults
        pkg_content = pkg_path.read_text()
        if '"scripts": {' in pkg_content:
             new_scripts = '"scripts": {\n    "dev": "ts-node src/index.ts",\n    "build": "tsc",'
             pkg_content = pkg_content.replace('"scripts": {', new_scripts)
             pkg_path.write_text(pkg_content)


import asyncio
