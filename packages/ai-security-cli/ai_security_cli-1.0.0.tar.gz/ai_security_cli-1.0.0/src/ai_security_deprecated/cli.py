"""Deprecated CLI wrapper - redirects to aisentry."""
import sys
import click

@click.command()
@click.pass_context
def main(ctx):
    """
    DEPRECATED: ai-security-cli has been renamed to aisentry.
    
    Please update your installation:
        pip uninstall ai-security-cli
        pip install aisentry
    
    The new CLI command is: aisentry
    """
    click.secho("\n" + "=" * 60, fg="yellow")
    click.secho("DEPRECATION WARNING: ai-security-cli is now 'aisentry'", fg="yellow", bold=True)
    click.secho("=" * 60, fg="yellow")
    click.echo("\nPlease update your installation:")
    click.secho("    pip uninstall ai-security-cli", fg="cyan")
    click.secho("    pip install aisentry", fg="green", bold=True)
    click.echo("\nThe new CLI command is:")
    click.secho("    aisentry scan ./my-project", fg="green")
    click.secho("    aisentry audit ./my-project", fg="green")
    click.secho("    aisentry test -p openai -m gpt-4", fg="green")
    click.secho("\n" + "=" * 60 + "\n", fg="yellow")
    
    # Pass through to aisentry
    from aisentry.cli import main as aisentry_main
    ctx.invoke(aisentry_main)

if __name__ == "__main__":
    main()
