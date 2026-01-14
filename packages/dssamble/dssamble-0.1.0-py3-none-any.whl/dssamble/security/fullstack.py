from ..utils import ProjectManager
from pathlib import Path

class ProjectFullstack(ProjectManager):
        def create_fullstack(name: str):
            base = Path(name)
            backend = base/'backend'
            frontend=base/'frontend'
            folders = [
                backend/'test',
                frontend/'public'
            ]

            for i in folders: 
                i.mkdir(parents=True, exist_ok=True)
                if "frontend" not in str(i):
                    ProjectManager.create_file(str(i/'__init__.py'), '')
