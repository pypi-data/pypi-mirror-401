"""CLI commands for design system stylesheet management."""

import click

from konigle.cli.main import cli, get_client


@cli.group()
def design():
    """Manage design system stylesheets."""
    pass


@design.command()
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Save stylesheet content to file",
)
@click.pass_context
def get_stylesheet(ctx: click.Context, output: str | None):
    """Get the design system stylesheet content."""
    client = get_client(ctx.obj["api_key"], ctx.obj["base_url"])

    try:
        content = client.stylesheets.get_content()

        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(content)
            click.echo(f"✅ Stylesheet saved to {output}")
        else:
            click.echo(content)

    except Exception as e:
        click.echo(f"Error getting stylesheet: {e}", err=True)


@design.command()
@click.option(
    "--content",
    help="Stylesheet content as string",
)
@click.option(
    "--file",
    "-f",
    type=click.Path(exists=True, readable=True),
    help="Path to stylesheet file",
)
@click.pass_context
def set_stylesheet(
    ctx: click.Context,
    content: str | None,
    file: str | None,
):
    """Set the design system stylesheet content."""
    client = get_client(ctx.obj["api_key"], ctx.obj["base_url"])

    # Validate input
    if not content and not file:
        click.echo(
            "Error: Either --content or --file must be provided", err=True
        )
        return

    if content and file:
        click.echo("Error: Cannot specify both --content and --file", err=True)
        return

    # Get content from file or direct input
    stylesheet_content = content
    if file:
        try:
            with open(file, "r", encoding="utf-8") as f:
                stylesheet_content = f.read()
        except Exception as e:
            click.echo(f"Error reading file: {e}", err=True)
            return

    try:
        client.stylesheets.set_content(stylesheet_content or "")
        click.echo("✅ Stylesheet content updated successfully")

    except Exception as e:
        click.echo(f"Error setting stylesheet: {e}", err=True)


@design.command("get-theme-css")
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Save theme css content to file",
)
@click.pass_context
def get_theme_css(ctx: click.Context, output: str | None):
    """Get the website theme css content."""
    client = get_client(ctx.obj["api_key"], ctx.obj["base_url"])

    try:
        content = client.themes.get_theme_css()
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(content)
            click.echo(f"✅ Theme css saved to {output}")
        else:
            click.echo(content)

    except Exception as e:
        import traceback

        traceback.print_exc()
        click.echo(f"Error getting theme css: {e}", err=True)


@design.command("set-theme-css")
@click.option(
    "--content",
    help="Theme css content as string",
)
@click.option(
    "--file",
    "-f",
    type=click.Path(exists=True, readable=True),
    help="Path to theme.css file",
)
@click.pass_context
def set_theme_css(
    ctx: click.Context,
    content: str | None,
    file: str | None,
):
    """Set the website theme css content."""
    client = get_client(ctx.obj["api_key"], ctx.obj["base_url"])

    # Validate input
    if not content and not file:
        click.echo(
            "Error: Either --content or --file must be provided", err=True
        )
        return

    if content and file:
        click.echo("Error: Cannot specify both --content and --file", err=True)
        return

    # Get content from file or direct input
    css_content = content
    if file:
        try:
            with open(file, "r", encoding="utf-8") as f:
                css_content = f.read()
        except Exception as e:
            click.echo(f"Error reading file: {e}", err=True)
            return

    try:
        client.themes.set_theme_css(css_content or "")
        click.echo("✅ Theme css content updated successfully")

    except Exception as e:
        click.echo(f"Error setting theme css: {e}", err=True)


@design.command("get-reference-template")
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Save reference HTML template content to file",
)
@click.pass_context
def get_reference_template(ctx: click.Context, output: str | None):
    """Get the reference html template for the website."""
    client = get_client(ctx.obj["api_key"], ctx.obj["base_url"])

    try:
        content = client.themes.get_reference_theme_template()

        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(content)
            click.echo(f"✅ Reference template saved to {output}")
        else:
            click.echo(content)

    except Exception as e:
        click.echo(f"Error getting reference template: {e}", err=True)


if __name__ == "__main__":
    design()
