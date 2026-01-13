import shutil
import subprocess
from pathlib import Path
from typing import Optional

class QualityService:
    """Service for code quality checks and formatting."""

    @staticmethod
    def format_file(file_path: str | Path) -> bool:
        """
        Format a file using appropriate tools (black, prettier).
        Returns True if successful.
        """
        path = Path(file_path)
        if not path.exists():
            return False
            
        ext = path.suffix.lower()
        
        try:
            if ext == ".py":
                return QualityService._format_python(path)
            elif ext in [".js", ".jsx", ".ts", ".tsx", ".json", ".css", ".md"]:
                return QualityService._format_prettier(path)
            elif ext == ".go":
                return QualityService._format_go(path)
            elif ext == ".rs":
                return QualityService._format_rust(path)
        except Exception as e:
            # Fallback (don't crash agent if formatter fails, just log)
            print(f"Formatting failed for {path}: {e}")
            return False
            
        return False

    @staticmethod
    def _format_python(path: Path) -> bool:
        """Format using black."""
        # Check if black is importable first for speed, or just run subprocess?
        # Subprocess is safer for isolated environment usage (CLI tool), 
        # but library usage is faster. Since we added 'black' to deps, we can use CLI mode via python -m
        
        # Using subprocess to isolate from plugin's runtime constraints if any
        cmd = ["python3", "-m", "black", str(path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0

    @staticmethod
    def _format_prettier(path: Path) -> bool:
        """Format using prettier (if available)."""
        # Check for npx or prettier
        prettier_exec = shutil.which("prettier")
        
        if prettier_exec:
            cmd = [prettier_exec, "--write", str(path)]
            subprocess.run(cmd, capture_output=True)
            return True
            
        # Try npx (slower)
        if shutil.which("npx"):
            cmd = ["npx", "prettier", "--write", str(path)]
            subprocess.run(cmd, capture_output=True)
            return True
            
        return False

    @staticmethod
    def _format_go(path: Path) -> bool:
        """Format using gofmt."""
        if shutil.which("gofmt"):
            cmd = ["gofmt", "-w", str(path)]
            subprocess.run(cmd, capture_output=True)
            return True
        return False

    @staticmethod
    def _format_rust(path: Path) -> bool:
        """Format using rustfmt."""
        if shutil.which("rustfmt"):
            cmd = ["rustfmt", str(path)]
            subprocess.run(cmd, capture_output=True)
            return True
        return False
