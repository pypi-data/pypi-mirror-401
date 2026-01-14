from pathlib import Path
import click
from ..utils import ProjectManager


class ProjectFullstack(ProjectManager):
    @staticmethod
    def create_fullstack(name: str) -> None:
        """
        Создает fullstack структуру проекта с backend и frontend
        
        Args:
            name: Имя проекта
        """
        if not ProjectManager.validate_project_name(name):
            click.echo("✗ Недопустимое имя проекта!", err=True)
            return
        
        click.echo(f"\n🚀 Создание fullstack проекта '{name}'...\n")
        
        base = Path(name)
        backend = base / 'backend'
        frontend = base / 'frontend'
        
        backend_folders = [
            backend / 'app',
            backend / 'app' / 'api',
            backend / 'app' / 'core',
            backend / 'app' / 'models',
            backend / 'app' / 'schemas',
            backend / 'test',
        ]
        
        for folder in backend_folders:
            folder.mkdir(parents=True, exist_ok=True)
            ProjectManager.create_file(
                str(folder / '__init__.py'),
                f'"""Модуль {folder.name}"""\n'
            )
        frontend_folders = [
            frontend / 'public',
            frontend / 'src',
            frontend / 'src' / 'components',
            frontend / 'src' / 'pages',
            frontend / 'src' / 'assets',
        ]
        
        for folder in frontend_folders:
            folder.mkdir(parents=True, exist_ok=True)
        
        backend_main = '''"""
Backend FastAPI приложение
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Fullstack API",
    version="0.1.0"
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Backend is running"}


@app.get("/api/health")
async def health():
    return {"status": "healthy"}
'''
        ProjectManager.create_file(str(backend / 'main.py'), backend_main)
        
        backend_reqs = '''fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.9.0
python-dotenv==1.0.0
sqlalchemy==2.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
'''
        ProjectManager.create_file(str(backend / 'requirements.txt'), backend_reqs)
        
        env_example = '''# Database
DATABASE_URL=sqlite:///./app.db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
FRONTEND_URL=http://localhost:3000
'''
        ProjectManager.create_file(str(backend / '.env.example'), env_example)
        
        package_json = '''{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "axios": "^1.6.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
'''
        ProjectManager.create_file(str(frontend / 'package.json'), package_json)
        
        frontend_readme = f'''# Frontend

React frontend для {name}

## Установка

```bash
npm install
```

## Запуск

```bash
npm start
```

Приложение откроется на http://localhost:3000
'''
        ProjectManager.create_file(str(frontend / 'README.md'), frontend_readme)
        
        root_readme = f'''# {name}

Fullstack приложение создано с помощью [dssamble](https://github.com/Dasakami/dssamble)

## Структура проекта

```
{name}/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/     # API endpoints
│   │   ├── core/    # Основные конфиги
│   │   ├── models/  # Модели БД
│   │   └── schemas/ # Pydantic схемы
│   ├── test/        # Тесты
│   └── main.py
└── frontend/        # React frontend
    ├── public/
    └── src/
        ├── components/
        ├── pages/
        └── assets/
```

## Запуск

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

Backend будет доступен на http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm start
```

Frontend будет доступен на http://localhost:3000

## API Documentation

После запуска backend, документация доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
'''
        ProjectManager.create_file(str(base / 'README.md'), root_readme)
        
        gitignore = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.db
*.sqlite3

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnp/
.pnp.js

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDEs
.vscode/
.idea/
*.swp

# Build
/frontend/build
/backend/dist
'''
        ProjectManager.create_file(str(base / '.gitignore'), gitignore)
        
        click.echo(f"\n✓ Fullstack проект '{name}' успешно создан!")
        click.echo(f"\n📝 Для начала работы:")
        click.echo(f"\n  Backend:")
        click.echo(f"    cd {name}/backend")
        click.echo(f"    pip install -r requirements.txt")
        click.echo(f"    uvicorn main:app --reload")
        click.echo(f"\n  Frontend:")
        click.echo(f"    cd {name}/frontend")
        click.echo(f"    npm install")
        click.echo(f"    npm start\n")