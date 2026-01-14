from pathlib import Path
import click
from ..utils import ProjectManager


class ProjectBasic(ProjectManager):
    @staticmethod
    def create_basic(name: str) -> None:
        """
        Создает базовую структуру FastAPI проекта
        
        Args:
            name: Имя проекта
        """
        if not ProjectManager.validate_project_name(name):
            click.echo("✗ Недопустимое имя проекта!", err=True)
            return
        
        click.echo(f"\n🚀 Создание проекта '{name}' с базовой структурой...\n")
        
        base = Path(name)
        folders = [
            base / 'app',
            base / 'module',
            base / 'services',
            base / 'test',
        ]
        
        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)
            ProjectManager.create_file(
                str(folder / '__init__.py'),
                f'"""Модуль {folder.name}"""\n'
            )
        
        main_content = '''"""
Главный файл FastAPI приложения
"""
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API созданный с помощью dssamble",
    version="0.1.0"
)


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    """Проверка здоровья приложения"""
    return {"status": "healthy"}
'''
        ProjectManager.create_file(str(base / 'main.py'), main_content)
        
        gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.env.local

# Database
*.db
*.sqlite3
'''
        ProjectManager.create_file(str(base / '.gitignore'), gitignore_content)
        
        requirements_content = '''fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.9.0
python-dotenv==1.0.0
'''
        ProjectManager.create_file(str(base / 'requirements.txt'), requirements_content)
        
        readme_content = f'''# {name}

Проект создан с помощью [dssamble](https://github.com/Dasakami/dssamble)

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
uvicorn main:app --reload
```

## Структура проекта

```
{name}/
├── app/          # Основной код приложения
├── module/       # Модули приложения
├── services/     # Сервисный слой
├── test/         # Тесты
├── main.py       # Точка входа
└── requirements.txt
```
'''
        ProjectManager.create_file(str(base / 'README.md'), readme_content)
        
        click.echo(f"\n✓ Проект '{name}' успешно создан!")
        click.echo(f"\n📝 Для начала работы:")
        click.echo(f"  cd {name}")
        click.echo(f"  pip install -r requirements.txt")
        click.echo(f"  uvicorn main:app --reload\n")