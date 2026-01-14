import typer
import subprocess
from gen_commit.git_utils import get_git_diff
from gen_commit.groq_client import generate_commit

app = typer.Typer(help="Generate git commit messages using Groq LLMs")

@app.command()
def gen_commit(
    api_key: str = typer.Option(None, help="Groq API Key"),
    model: str = typer.Option(
        "llama-3.1-8b-instant",
        help="Groq model",
    ),
    commit: bool = typer.Option(False, help="Automatically create the git commit"),
):
    diff = get_git_diff()

    if not diff:
        typer.echo("❌ No staged changes found. Run `git add` first.")
        raise typer.Exit(code=1)

    message = generate_commit(diff, api_key, model)

    typer.echo("\n✅ Generated commit message:\n")
    typer.echo(message)

    if commit:
        subprocess.run(["git", "commit", "-m", message])


def main():
    app()


if __name__ == "__main__":
    main()
