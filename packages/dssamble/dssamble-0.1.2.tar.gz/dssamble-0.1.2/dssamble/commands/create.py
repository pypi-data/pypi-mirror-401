import click
import os
from ..security.basic import ProjectBasic
from ..security.fullstack import ProjectFullstack


@click.command()
@click.argument('structure', type=click.Choice(['basic', 'fullstack'], case_sensitive=False))
@click.argument('name')
@click.option('--force', '-f', is_flag=True, help='Перезаписать если папка существует')
def create(structure, name, force):
    """
    Создать структуру проекта
    
    \b
    Доступные типы:
      basic      - Базовая структура FastAPI проекта
      fullstack  - Fullstack приложение с backend и frontend
    
    \b
    Примеры:
      dssamble create basic my_api
      dssamble create fullstack my_webapp
      dssamble create basic my_project --force
    """
    if os.path.exists(name):
        if not force:
            click.echo(f"\n✗ Папка '{name}' уже существует!")
            click.echo(f"  Используйте флаг --force для перезаписи\n")
            return
        else:
            click.echo(f"\n⚠ Внимание: папка '{name}' будет перезаписана!")
            if not click.confirm('Продолжить?'):
                click.echo("Отменено.")
                return
    
    generators = {
        'basic': ProjectBasic.create_basic,
        'fullstack': ProjectFullstack.create_fullstack,
    }
    
    try:
        generators[structure.lower()](name)
    except Exception as e:
        click.echo(f"\n✗ Ошибка при создании проекта: {e}\n", err=True)
        raise