from ..utils import ProjectManager
import os
class ProjectCreateFiles(ProjectManager):
    @staticmethod
    def createfiles(files: list):
        path = os.getcwd()
        for file_path in files:
            full_path = os.path.join(path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write('test')
                
        return {'success': 'ok'}
