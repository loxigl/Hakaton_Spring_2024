import typer
from core.database import drop_tables, create_tables
from user.models import User, Token
from worksheet.models import Worksheet
from hobby.models import Hobby
from dotenv import load_dotenv
from core.config import Config

load_dotenv()

app = typer.Typer()


@app.command()
def create_db():
    try:
        create_tables()
    except Exception as e:
        typer.echo(f"Error: {e}")
    typer.echo("Database created")


@app.command()
def drop_db():
    typer.echo(Config.db_connection_string)
    try:
        drop_tables()
    except Exception as e:
        typer.echo(f"Error: {e}")
    typer.echo("Database dropped")


if __name__ == "__main__":
    app()
