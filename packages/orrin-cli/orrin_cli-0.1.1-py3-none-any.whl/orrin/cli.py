import typer
import requests
from pathlib import Path

app = typer.Typer(help='Test Help')

API_BASE = "https://api.stellr-company.com"

@app.command()
def upload(
    zip_path: Path = typer.Argument(..., exists=True),
    app_name: str = typer.Option(..., "--app")
):
    """
    Upload a UI zip to Orrin.
    """
    with open(zip_path, "rb") as f:
        response = requests.post(
            f"{API_BASE}/ui/upload",
            files={"file": f},
            data={"app_name": app_name}
        )

    if response.status_code != 200:
        typer.echo("❌ Upload failed")
        raise typer.Exit(1)

    data = response.json()
    typer.echo("✅ Uploaded")
    typer.echo(f"Upload ID: {data.get('upload_id')}")

def main():
    app()

if __name__ == "__main__":
    main()
