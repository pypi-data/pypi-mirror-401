from pathlib import Path
from typing import Optional
import click


class ProjectManager:
    """Менеджер для создания файлов и папок проекта"""
    
    @staticmethod
    def create_file(path: str, content: str = "") -> None:
        """
        Создает файл с указанным содержимым
        
        Args:
            path: Путь к файлу
            content: Содержимое файла (по умолчанию пустое)
        """
        try:
            file_path = Path(path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            click.echo(f"✓ Создан: {path}")
        except Exception as e:
            click.echo(f"✗ Ошибка при создании {path}: {e}", err=True)
            raise
    
    @staticmethod
    def create_directory(path: str) -> None:
        """
        Создает директорию
        
        Args:
            path: Путь к директории
        """
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            click.echo(f"✓ Создана папка: {path}")
        except Exception as e:
            click.echo(f"✗ Ошибка при создании папки {path}: {e}", err=True)
            raise
    
    @staticmethod
    def validate_project_name(name: str) -> bool:
        """
        Проверяет корректность имени проекта
        
        Args:
            name: Имя проекта
            
        Returns:
            True если имя корректно
        """
        invalid_chars = '<>:"/\\|?*'
        if any(char in name for char in invalid_chars):
            return False
        reserved = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 
                   'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 
                   'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 
                   'LPT7', 'LPT8', 'LPT9'}
        if name.upper() in reserved:
            return False
            
        return True