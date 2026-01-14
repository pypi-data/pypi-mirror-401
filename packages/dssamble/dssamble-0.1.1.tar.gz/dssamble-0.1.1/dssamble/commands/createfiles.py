import click
import os
from ..security.createfiles import ProjectCreateFiles

@click.command()
@click.argument("files", nargs=-1)
def createfiles(files):
    """
    Массовое создание файлов, папок. \n
    После команды укажите файлы , н: createfiles main.py readme.md text.txt \n
    Если хотите включить папку, то просто укажите путь. Н: creafiles utils/test.py
    """
    ProjectCreateFiles.createfiles(files)
    click.echo('Успешно!')