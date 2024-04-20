import typer
from core.database import drop_tables, create_tables

app = typer.Typer()


@app.command()
def create_db():
    create_tables()
    typer.echo("Database created")


@app.command()
def drop_db():
    drop_tables()
    typer.echo("Database dropped")


if __name__ == "__main__":
    app()
