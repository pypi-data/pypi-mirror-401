from pathlib import Path
class ProjectManager:
    def create_file(path: str, content: str = ""):
        with open(path, 'w',encoding='utf-8' ) as f:
            f.write(content)
    