from flask.cli import FlaskGroup

from yahooApp import app


cli = FlaskGroup(app)


if __name__ == "__main__":
    cli()
