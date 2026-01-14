import os
import shutil
from pathlib import Path


def main():
    import sys
    
    if len(sys.argv) < 2 or sys.argv[1] != 'init':
        print("Usage: flask-mvc-starter init <project-name>")
        sys.exit(1)
    
    if len(sys.argv) < 3:
        print("Error: Project name is required")
        print("Usage: flask-mvc-starter init <project-name>")
        sys.exit(1)
    
    project_name = sys.argv[2]
    current_dir = Path.cwd()
    project_path = current_dir / project_name
    
    if project_path.exists():
        print(f"Error: Directory '{project_name}' already exists")
        sys.exit(1)
    
    template_dir = Path(__file__).parent / 'templates'
    
    print(f"Creating Flask MVC project: {project_name}")
    
    shutil.copytree(template_dir, project_path)
    
    print(f"✓ Project created successfully!")
    print(f"\nNext steps:")
    print(f"  cd {project_name}")
    print(f"  python -m venv venv")
    print(f"  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print(f"  pip install -r requirements.txt")
    print(f"  cp .env.example .env")
    print(f"  # Edit .env file with your settings")
    print(f"  python run.py")
