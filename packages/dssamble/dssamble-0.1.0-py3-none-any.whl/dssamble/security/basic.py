from ..utils import ProjectManager
from pathlib import Path
class ProjectBasic(ProjectManager):
    def create_basic(name: str):
        base = Path(name)
        folders = [
            base / 'test',
            base / 'app',
            base / 'module',
            base / 'services',
        ]
        for i in folders:
            i.mkdir(parents=True, exist_ok=True)
            ProjectManager.create_file(str(i/'__init__.py'), '')
        ProjectManager.create_file(str(base/'main.py'), '''
from fastapi import FastAPI
app = FastAPI()

''')