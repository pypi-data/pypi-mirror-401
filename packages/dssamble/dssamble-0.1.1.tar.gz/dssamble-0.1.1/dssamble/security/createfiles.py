import os
from pathlib import Path
import click
from ..utils import ProjectManager


class ProjectCreateFiles(ProjectManager):
    @staticmethod
    def createfiles(files: tuple) -> dict:
        """
        Создает множество файлов с автоматическим созданием папок
        
        Args:
            files: Кортеж путей к файлам
            
        Returns:
            Словарь с результатом операции
        """
        if not files:
            click.echo("✗ Не указаны файлы для создания!", err=True)
            return {'success': False, 'message': 'No files specified'}
        
        click.echo(f"\n📁 Создание {len(files)} файлов...\n")
        
        path = os.getcwd()
        created_count = 0
        failed_count = 0
        
        for file_path in files:
            try:
                full_path = os.path.join(path, file_path)
                
                dir_path = os.path.dirname(full_path)
                if dir_path:
                    os.makedirs(dir_path, exist_ok=True)
                
                ext = os.path.splitext(file_path)[1]
                content = ProjectCreateFiles._get_template_content(ext, file_path)
                
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                click.echo(f"  ✓ {file_path}")
                created_count += 1
                
            except Exception as e:
                click.echo(f"  ✗ {file_path}: {e}", err=True)
                failed_count += 1

        click.echo(f"\n{'='*50}")
        click.echo(f"✓ Создано: {created_count}")
        if failed_count > 0:
            click.echo(f"✗ Ошибок: {failed_count}")
        click.echo(f"{'='*50}\n")
        
        return {
            'success': failed_count == 0,
            'created': created_count,
            'failed': failed_count
        }
    
    @staticmethod
    def _get_template_content(ext: str, filepath: str) -> str:
        """
        Возвращает шаблон содержимого для файла по его расширению
        
        Args:
            ext: Расширение файла
            filepath: Путь к файлу
            
        Returns:
            Строка с шаблонным содержимым
        """
        filename = os.path.basename(filepath)
        
        templates = {
            '.py': f'"""\nМодуль {filename}\n"""\n\n',
            '.js': f'/**\n * {filename}\n */\n\n',
            '.ts': f'/**\n * {filename}\n */\n\n',
            '.jsx': f'/**\n * {filename}\n */\n\nimport React from "react";\n\n',
            '.tsx': f'/**\n * {filename}\n */\n\nimport React from "react";\n\n',
            '.css': f'/* {filename} */\n\n',
            '.html': f'<!DOCTYPE html>\n<html lang="ru">\n<head>\n  <meta charset="UTF-8">\n  <title>Document</title>\n</head>\n<body>\n  \n</body>\n</html>\n',
            '.md': f'# {os.path.splitext(filename)[0]}\n\n',
            '.json': '{\n  \n}\n',
            '.yaml': f'# {filename}\n\n',
            '.yml': f'# {filename}\n\n',
            '.txt': '',
            '.env': '# Environment variables\n\n',
        }
        
        return templates.get(ext, f'# {filename}\n\n')