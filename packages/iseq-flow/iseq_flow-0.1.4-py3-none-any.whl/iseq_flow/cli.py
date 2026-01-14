"""Main CLI entry point for iseq-flow."""

import click

from iseq_flow import __version__
from iseq_flow.commands.auth import login, logout, status
from iseq_flow.commands.config import config
from iseq_flow.commands.files import files
from iseq_flow.commands.orders import orders
from iseq_flow.commands.pipelines import pipelines
from iseq_flow.commands.runs import runs


@click.group()
@click.version_option(version=__version__, prog_name="flow")
def main():
    """
    iseq-flow - CLI for IntelliSeq Flow platform.

    \b
    Examples:
      flow login                        # Authenticate with OAuth
      flow status                       # Check login status
      flow files ls -p ID               # List files in project
      flow pipelines list               # List available pipelines
      flow runs submit -p ID --pipeline SLUG -P key=value
    """
    pass


# Auth commands
main.add_command(login)
main.add_command(logout)
main.add_command(status)

# File commands
main.add_command(files)

# Config commands
main.add_command(config)

# Pipeline commands
main.add_command(pipelines)

# Run commands
main.add_command(runs)

# Order commands
main.add_command(orders)


if __name__ == "__main__":
    main()
