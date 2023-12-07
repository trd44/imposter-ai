"""
db.py

Author: Tim Duggan
Date: 12/3/2023
Company: ImposterAI
Contact: csw73@cornell.edu

This file provides functionality for accessing the sqlite3 databases.
"""
# region Imports
import click
import sqlite3
from sqlite3 import Connection
from flask import current_app, g

# endregion


def get_db() -> Connection:
    """
    Establishes and returns a connection to the SQLite3 database.

    Checks if a database connection already exists in the application context.
    If not, creates a new connection and sets it as the database for the current
    application context.

    Returns:
        A connection object for the SQLite3 database.
    """
    # Check if there's no DB connection
    if "db" not in g:
        # Connect to the SQLite3 Database
        g.db = sqlite3.connect(
            database=current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        # Row factory makes rows behave like Python dictionaries
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None) -> None:
    """
    Closes the SQLite3 database connection.

    This function pops the "db" object from the global context of the application
    and closes the connection to the database if it exists.

    Args:
        e (Exception, optional): An error instance passed in after failure of a
        request context. Default is None, which means no error has occurred.
    """
    # Remove the DB object from global context
    db = g.pop("db", None)

    # Close the DB connection if it exists
    if db is not None:
        db.close()


def init_db() -> None:
    """
    Initializes the database by creating tables according to schema.sql.

    Example:
        To initialize the database, simply call this function:
            >>> init_db()
    """
    # Get the DB connection
    db = get_db()

    # Execute script from 'schema.sql' file
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command(name="init-db")
def init_db_command() -> None:
    """
    Command to clear the existing data and create new tables.
    """
    # Initialize the DB
    init_db()
    # Print the success message
    click.echo("Initialized the database.")


def init_app(app) -> None:
    """
    Set up database related hooks on the given Flask application instance.

    This function does two things:
    1. Registers a new command that initializes the database to the Flask
       application instance.
    2. Configures the application to call the 'close_db' function at the end
       of each request, even if unhandled exceptions are raised.

    Args:
        app (Flask): the Flask application instance to configure.

    Example:
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> init_app(app)
    """

    # Register a function to run at the end of each request, whether they are
    # successful or not
    app.teardown_appcontext(close_db)

    # Add the command to the application instance
    app.cli.add_command(init_db_command)
