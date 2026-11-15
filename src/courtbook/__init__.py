import os
import sqlite3

import click
from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "courtbook.sqlite"),
    )
    os.makedirs(app.instance_path, exist_ok=True)

    from .routes import auth_bp
    app.register_blueprint(auth_bp)

    @app.cli.command("init-db")
    def init_db():
        conn = sqlite3.connect(app.config["DATABASE"])
        with app.open_resource("schema.sql") as f:
            conn.executescript(f.read().decode("utf-8"))
        conn.close()
        click.echo("Initialized the database.")

    return app
