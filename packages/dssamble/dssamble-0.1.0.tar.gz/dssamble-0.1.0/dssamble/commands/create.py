import click
import os
from ..security.basic import ProjectBasic
from ..security.fullstack import ProjectFullstack
@click.command()
@click.argument('structure', type=click.Choice(['basic', 'fullstack']))
@click.argument('name')
def create(structure, name):
    """Создать структуру проекта\n
    Типы:\n
    - basic : Базовая структура данных\n
    - fullstack : fullstack приложение с auth 
    """
    if os.path.exists(name):
        click.echo(f'X Папка [{name}] уже существует!')
        return 
    generators = {
        'basic': ProjectBasic.create_basic,
        'fullstack': ProjectFullstack.create_fullstack,
    }

    generators[structure](name)