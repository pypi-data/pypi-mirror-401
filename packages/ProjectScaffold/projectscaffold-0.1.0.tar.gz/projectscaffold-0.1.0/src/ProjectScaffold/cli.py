import click

from ProjectScaffold.scaffold import create_project


@click.command()
def main():
    """Project scaffold generator"""

    name = click.prompt("Project name", type=str)

    backend = click.prompt(
        "Backend",
        type=click.Choice(
            ["flask", "django", "fastapi", "nodejs", "express", "springboot"],
            case_sensitive=False,
        ),
    )

    frontend = click.prompt(
        "Frontend",
        type=click.Choice(
            ["vanilla", "react", "vue", "angular", "svelte"],
            case_sensitive=False,
        ),
    )

    db = click.prompt(
        "DB",
        type=click.Choice(
            ["sqlite", "postgres", "mysql", "mongodb"],
            case_sensitive=False,
        ),
    )

    create_project(
        name=name,
        backend=backend,
        frontend=frontend,
        db=db,
    )


if __name__ == "__main__":
    main()
