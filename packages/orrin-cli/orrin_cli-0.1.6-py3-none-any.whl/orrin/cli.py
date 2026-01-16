import typer
import requests
import json
import os
from pathlib import Path
from platformdirs import user_config_dir

app = typer.Typer(help="""
Welcome to Orrin CLI v0.1.6!\n\n
                  
Orrin CLI enables you to perform actions within your terminal that would otherwise require
an entire dashboard. Though there is a dashboard, Orrin CLI enables a feasible development
experience for all developers, as they can swiftly run a command to upload their frontend,
perform checks on their app review status, and more!
""", no_args_is_help=True)

config = typer.Typer(help="Configure your Orrin Apps developer API with Orrin CLI")
app.add_typer(config, name='config')

ui = typer.Typer(help="UI related commands")
app.add_typer(ui, name="ui")

API_BASE = "http://192.168.1.153:8080"

APP_NAME = "orrin"
APP_AUTHOR = "orrin"  # optional but recommended on Windows

config_dir = Path(user_config_dir(APP_NAME, APP_AUTHOR))
config_dir.mkdir(parents=True, exist_ok=True)

config_file = config_dir / "config.json"

# ---- Configuration based commands/helper functions ----

def save_api_key(api_key: str):
    data = {"api_key": api_key}
    with open(config_file, "w") as f:
        json.dump(data, f)

def load_api_key() -> str | None:
    if not config_file.exists():
        return None
    with open(config_file) as f:
        return json.load(f).get("api_key")

@config.command(help="Add your Developer API key to the Orrin CLI to perform tasks explicitly relating to your developer account")
def configure_dev_api():
    dev_api = typer.prompt(
        "Enter your Developer API key",
        hide_input=True,
        confirmation_prompt=True,
    )
    
    resp = requests.post(
        f'{API_BASE}/api/orrin_apps/developer_api_exists',
        json={'developer_api_key': dev_api}
    )
    
    if not resp.ok:
        typer.echo(f'❌ No developer account was found with API key:\n\n{dev_api}')
        raise typer.Exit(1)
    
    save_api_key(dev_api)
    typer.echo("✅ Developer API configured with Orrin CLI")

@config.command(help='Revokes the Developer API currently configured with Orrin CLI')
def revoke_config():
    if not config_file.exists():
        typer.echo("ℹ️ No configuration found to revoke.")
        raise typer.Exit(code=0)

    try:
        config_file.unlink()
        typer.echo("✅ Credentials revoked. Local config removed.")
    except Exception as e:
        typer.echo(f"❌ Failed to revoke credentials: {e}")
        raise typer.Exit(code=1)

@config.command(help='Show configured Developer API key')
def show_configuration():
    if not config_file.exists():
        typer.echo("ℹ️ No Developer API key configured with Orrin CLI")
        raise typer.Exit(code=0)
    
    dev_api_key = load_api_key()

    typer.echo(f'Configured Developer API key: {dev_api_key}')

# -------------------------------------------------------

# ---- UI based commands/helper functions ----

@ui.command(help='''Build static output for next.js code, and generate a zip file to be uploaded.\n\nEnsure you have the following in next.config.tsx:\n\n
------------------------------------------------------\n\n
/** @type {import('next').NextConfig} */\n\n
const nextConfig = {\n\n
  output: 'export',\n\n
  trailingSlash: true,\n\n
  basePath: '/<your_app_name>/current',\n\n
  reactStrictMode: true,\n\n
};\n\n
\n\n
module.exports = nextConfig;
------------------------------------------------------\n\n
\n\n
Where <your_app_name> is the name of your app, which was configured in your backend.
''')
def generate_zip():
    os.system('npm install && npm run build')
    os.system('cd out && zip -r ../ui-build.zip .')

@ui.command(help="Upload your frontend code to be reviewed")
def upload(
    #zip_path: Path = typer.Argument(..., exists=True),
    app_name: str = typer.Option(..., "--app")
):
    """
    Upload a UI zip to Orrin.
    """
    if not os.path.isfile(os.path.join(os.getcwd(), 'ui-build.zip')):
        typer.echo(f"❌ Path {os.path.join(os.getcwd(), 'ui-build.zip')} does not exist.\n\nEnsure you run `orrin ui generate-zip`, or build the zip yourself.")
        raise typer.Exit(1)
    
    dev_api = load_api_key()

    if dev_api is None:
        typer.echo("❌ You have not configured an API key. Please register with `orrin configure configure-dev-api`.")
        raise typer.Exit(1)
    
    with open(os.path.join(os.getcwd(), 'ui-build.zip'), "rb") as f:
        response = requests.post(
            f"{API_BASE}/ui/upload",
            files={"file": f},
            data={
                "developer_id": dev_api,
                "app_name": app_name
            }
        )

    if response.status_code != 200:
        try:
            data = response.json()
            typer.echo(f'❌ Upload failed: {response.status_code}\n\nMessage: {data["Message"]}')
        except:
            typer.echo("❌ Upload failed")
        raise typer.Exit(1)

    data = response.json()
    typer.echo("✅ Uploaded")
    typer.echo(f"Upload ID: {data.get('upload_id')}")

# --------------------------------------------

def main():
    app()

if __name__ == "__main__":
    main()
