import click
@click.command()
def info():
    """
    Доступные типы структур
    """
    text = [
        'Доступные типы структур',
        '1. basic - Базовая структура FastAPI проекта',
        '2. fullstack - Fullstack приложение с аутентификацией'
    ]
    click.echo('\n'.join(text))
