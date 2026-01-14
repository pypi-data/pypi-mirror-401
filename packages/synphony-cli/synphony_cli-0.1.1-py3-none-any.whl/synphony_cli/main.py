import click
import os
import json
import time
import requests
from pathlib import Path
from typing import List
import sys
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import secrets
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


CONFIG_DIR = Path.home() / ".synphony"
CONFIG_FILE = CONFIG_DIR / "config.json"
SYNPHONY_FILE = ".synphony"
GENERATED_DIR = "generated"

# API Configuration
API_BASE_URL = "https://dev.synphony.co/api/cli"

# Supported video formats
VIDEO_FORMATS = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm", ".m4v", ".mpg", ".mpeg", ".3gp", ".ogv"}

# Concurrent download settings
MAX_CONCURRENT_DOWNLOADS = 4


class CLICallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for OAuth 2.0 loopback redirect"""
    token = None
    state = None

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if '/callback' in self.path:
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)

            received_state = params.get('state', [''])[0]
            if received_state != CLICallbackHandler.state:
                self.send_response(403)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<h1>Error: Invalid state parameter</h1>")
                return

            token = params.get('token', [''])[0]
            if not token:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<h1>Error: No token received</h1>")
                return

            CLICallbackHandler.token = token

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            success_html = """
            <html>
            <head>
                <title>Synphony CLI</title>
                <style>
                    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                           text-align: center; padding: 50px; background: #fafafa; }
                    .container { background: white; padding: 40px; border-radius: 8px; max-width: 400px;
                                 margin: 0 auto; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
                    h1 { color: #333; font-weight: 500; }
                    p { color: #666; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Authentication Complete</h1>
                    <p>You can close this window and return to your terminal.</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(success_html.encode('utf-8'))

            def shutdown():
                self.server.shutdown()
            threading.Thread(target=shutdown, daemon=True).start()
            return

        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>Not found</h1>")


def echo_info(msg: str):
    click.echo(click.style(f"  {msg}", fg="bright_black"))

def echo_success(msg: str):
    click.echo(click.style(f"  [OK] {msg}", fg="green"))

def echo_error(msg: str):
    click.echo(click.style(f"  [ERROR] {msg}", fg="red"))

def echo_warn(msg: str):
    click.echo(click.style(f"  [WARN] {msg}", fg="yellow"))

def echo_step(msg: str):
    click.echo(click.style(f"\n> {msg}", fg="white", bold=True))


def is_video_file(file_path: str) -> bool:
    return Path(file_path).suffix.lower() in VIDEO_FORMATS


def ensure_config_dir():
    CONFIG_DIR.mkdir(exist_ok=True)


def save_token(token: str):
    ensure_config_dir()
    config = {"token": token}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


def load_token() -> str | None:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config.get("token")
        except:
            return None
    return None


def load_dataset_id() -> str | None:
    if not Path(SYNPHONY_FILE).exists():
        return None
    try:
        with open(SYNPHONY_FILE, "r") as f:
            data = json.load(f)
            return data.get("dataset_id")
    except:
        return None


def load_dataset_name() -> str | None:
    if not Path(SYNPHONY_FILE).exists():
        return None
    try:
        with open(SYNPHONY_FILE, "r") as f:
            data = json.load(f)
            return data.get("name")
    except:
        return None


def save_dataset(dataset_id: str, name: str):
    data = {"dataset_id": dataset_id, "name": name}
    with open(SYNPHONY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def find_video_files(exclude_generated=True) -> List[str]:
    video_files = []
    for root, dirs, files in os.walk("."):
        if exclude_generated and GENERATED_DIR in dirs:
            dirs.remove(GENERATED_DIR)
        for file in files:
            file_path = os.path.join(root, file)
            if is_video_file(file_path):
                video_files.append(file_path)
    return sorted(video_files)


def find_video_files_by_pattern(patterns: tuple) -> List[str]:
    import glob as glob_module
    video_files = set()
    for pattern in patterns:
        if pattern == '.':
            pattern = '*'
        matched = glob_module.glob(pattern, recursive=True)
        for file_path in matched:
            if os.path.isfile(file_path):
                if GENERATED_DIR not in file_path and is_video_file(file_path):
                    video_files.add(file_path)
    return sorted(list(video_files))


def format_bytes(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"


def call_multiply_endpoint(dataset_id: str, file_ids: List[str], prompts: List[str], token: str) -> dict | None:
    try:
        headers = {"X-API-Key": token, "Content-Type": "application/json"}
        payload = {"dataset_id": dataset_id, "file_ids": file_ids, "prompts": prompts}

        echo_step("Submitting processing tasks")
        response = requests.post(f"{API_BASE_URL}/multiply", json=payload, headers=headers, timeout=30)

        if response.status_code != 200:
            echo_error(f"Failed to submit tasks (HTTP {response.status_code})")
            return None

        response_data = response.json()
        if not response_data.get("ok"):
            echo_error(response_data.get('error', 'Unknown error'))
            return None

        return response_data

    except requests.exceptions.RequestException as e:
        echo_error(f"Network error: {str(e)}")
        return None
    except Exception as e:
        echo_error(str(e))
        return None


def create_dataset(token: str, name: str | None = None) -> dict | None:
    try:
        headers = {"X-API-Key": token, "Content-Type": "application/json"}
        payload = {"name": name} if name else {}

        echo_step("Creating dataset")
        response = requests.post(f"{API_BASE_URL}/create", json=payload, headers=headers, timeout=10)

        if response.status_code != 200:
            echo_error(f"Failed to create dataset (HTTP {response.status_code})")
            return None

        response_data = response.json()
        if not response_data.get("ok"):
            echo_error(response_data.get('error', 'Unknown error'))
            return None

        dataset_id = response_data.get("dataset_id")
        dataset_name = response_data.get("name")
        if not dataset_id or not dataset_name:
            echo_error("Invalid response from server")
            return None

        echo_success(f"Created: {dataset_name}")
        return {"dataset_id": dataset_id, "name": dataset_name}

    except requests.exceptions.RequestException as e:
        echo_error(f"Network error: {str(e)}")
        return None
    except Exception as e:
        echo_error(str(e))
        return None


def lookup_dataset(name: str, token: str) -> dict | None:
    try:
        headers = {"X-API-Key": token, "Content-Type": "application/json"}

        echo_step(f"Looking up dataset '{name}'")
        response = requests.post(f"{API_BASE_URL}/lookup", json={"name": name}, headers=headers, timeout=10)

        if response.status_code != 200:
            echo_error(f"Failed to lookup dataset (HTTP {response.status_code})")
            return None

        response_data = response.json()
        if not response_data.get("ok"):
            echo_error(response_data.get('error', 'Unknown error'))
            return None

        dataset_id = response_data.get("dataset_id")
        dataset_name = response_data.get("name")
        if not dataset_id or not dataset_name:
            echo_error("Invalid response from server")
            return None

        echo_success(f"Found: {dataset_name}")
        return {"dataset_id": dataset_id, "name": dataset_name}

    except requests.exceptions.RequestException as e:
        echo_error(f"Network error: {str(e)}")
        return None
    except Exception as e:
        echo_error(str(e))
        return None


def upload_single_file(file_path: str, presigned_url: str, content_type: str = "video/mp4") -> tuple[str, bool, str]:
    """Upload a single file. Returns (filename, success, error_msg)"""
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
        # Must include Content-Type header matching what presigned URL was created with
        headers = {"Content-Type": content_type}
        response = requests.put(presigned_url, data=file_content, headers=headers, timeout=300)
        if response.status_code == 200:
            return (os.path.basename(file_path), True, "")
        else:
            # Try to get error details from S3 response
            error_detail = response.text[:200] if response.text else ""
            return (os.path.basename(file_path), False, f"HTTP {response.status_code}: {error_detail}")
    except Exception as e:
        return (os.path.basename(file_path), False, str(e))


def upload_videos(dataset_id: str, file_list: List[str], token: str) -> dict | None:
    try:
        files_data = []
        for file_path in file_list:
            file_size = os.path.getsize(file_path)
            files_data.append({
                "filename": os.path.basename(file_path),
                "size": file_size,
                "content_type": "video/mp4"
            })

        headers = {"X-API-Key": token, "Content-Type": "application/json"}
        payload = {"files": files_data, "dataset_id": dataset_id}

        echo_step("Requesting upload URLs")
        response = requests.post(f"{API_BASE_URL}/upload", json=payload, headers=headers, timeout=10)

        if response.status_code != 200:
            echo_error(f"Failed to get upload URLs (HTTP {response.status_code})")
            return None

        response_data = response.json()
        if not response_data.get("ok"):
            echo_error(response_data.get('error', 'Unknown error'))
            return None

        files_info = response_data.get("files", [])
        echo_success(f"Got URLs for {len(files_info)} file(s)")

        echo_step(f"Uploading {len(file_list)} file(s)")

        # Upload concurrently
        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_DOWNLOADS) as executor:
            futures = {}
            for file_path, file_info in zip(file_list, files_info):
                future = executor.submit(upload_single_file, file_path, file_info.get("presigned_url"))
                futures[future] = file_path

            for future in as_completed(futures):
                filename, success, error_msg = future.result()
                if success:
                    echo_success(filename)
                else:
                    echo_error(f"{filename} - {error_msg or 'upload failed'}")
                    return None

        return {"files": files_info, "count": len(files_info)}

    except requests.exceptions.RequestException as e:
        echo_error(f"Network error: {str(e)}")
        return None
    except Exception as e:
        echo_error(str(e))
        return None


@click.group()
@click.version_option(version="0.1.1", prog_name="synphony")
def cli():
    """Synphony CLI - Video processing and dataset management"""
    pass


def validate_token(token: str) -> dict | None:
    try:
        headers = {"X-API-Key": token, "Content-Type": "application/json"}
        response = requests.post(f"{API_BASE_URL}/auth", headers=headers, timeout=10)

        if response.status_code == 401:
            return {"error": "invalid_token"}
        elif response.status_code != 200:
            return {"error": "server_error", "status": response.status_code}

        data = response.json()
        if not data.get("ok"):
            return {"error": "invalid_token"}

        return data.get("user")
    except requests.exceptions.ConnectionError:
        return {"error": "connection_failed"}
    except requests.exceptions.Timeout:
        return {"error": "timeout"}
    except Exception as e:
        return {"error": "unknown", "details": str(e)}


@cli.command()
@click.argument("token")
def auth(token: str):
    """Authenticate with an API token"""
    echo_step("Validating token")

    result = validate_token(token)

    if result is None:
        echo_error("Could not validate token")
        return

    if "error" in result:
        error = result["error"]
        if error == "invalid_token":
            echo_error("Invalid token")
        elif error == "connection_failed":
            echo_error("Could not connect to server")
        elif error == "timeout":
            echo_error("Server request timed out")
        elif error == "server_error":
            echo_error(f"Server error (HTTP {result.get('status', '?')})")
        else:
            echo_error(result.get('details', 'Unknown error'))
        return

    save_token(token)
    email = result.get("email", "Unknown")
    echo_success(f"Authenticated as {email}")


@cli.command()
def whoami():
    """Show current authentication status"""
    token = load_token()
    if not token:
        echo_error("Not authenticated. Run: synphony auth <token>")
        return

    echo_step("Checking authentication...")

    result = validate_token(token)

    if result is None:
        echo_error("Could not connect to server")
        return

    if "error" in result:
        echo_error("Token is invalid or expired. Run: synphony auth <token>")
        return

    echo_success("Authenticated")
    click.echo(f"  Email: {result.get('email', 'Unknown')}")
    click.echo(f"  Name: {result.get('name', 'Unknown')}")

    # Show current dataset if in a project
    dataset_id = load_dataset_id()
    dataset_name = load_dataset_name()
    if dataset_id:
        click.echo(f"  Dataset: {dataset_name} ({dataset_id})")


@cli.command()
@click.option('--port', default=0, help='Local callback server port (0 = random)')
@click.option('--timeout', default=120, help='Authentication timeout in seconds')
def login(port: int, timeout: int):
    """Authenticate via browser"""
    existing_token = load_token()
    if existing_token:
        echo_warn("Already authenticated")
        if not click.confirm("  Login again?"):
            click.echo("  Cancelled.")
            return

    state_token = secrets.token_urlsafe(32)
    CLICallbackHandler.state = state_token
    CLICallbackHandler.token = None

    try:
        server = HTTPServer(('127.0.0.1', port), CLICallbackHandler)
    except OSError as e:
        if "Address already in use" in str(e):
            echo_error(f"Port {port} is already in use")
            echo_info("Try: synphony login --port <port>")
        else:
            echo_error(f"Failed to start server: {str(e)}")
        return

    real_port = server.server_address[1]
    redirect_uri = f"http://127.0.0.1:{real_port}/callback"

    NEXTJS_URL = "https://dev.synphony.co"
    auth_url = (
        f"{NEXTJS_URL}/api/generate-cli-token?"
        f"redirect_uri={urllib.parse.quote(redirect_uri, safe='')}"
        f"&state={state_token}"
    )

    echo_step("Starting authentication")
    echo_info(f"Callback server: http://127.0.0.1:{real_port}")

    try:
        webbrowser.open(auth_url)
        echo_info("Opening browser...")
    except Exception as e:
        echo_warn(f"Could not open browser: {str(e)}")
        echo_info(f"Open manually: {auth_url}")

    echo_info("Waiting for authentication...")
    server.timeout = 0.5
    start_time = time.time()

    try:
        while CLICallbackHandler.token is None:
            server.handle_request()
            elapsed = time.time() - start_time
            if elapsed > timeout:
                echo_error(f"Timeout after {timeout}s")
                server.server_close()
                return

        time.sleep(0.1)
        server.server_close()

        token = CLICallbackHandler.token
        save_token(token)
        echo_success("Authenticated successfully")

    except KeyboardInterrupt:
        echo_error("Cancelled")
        server.server_close()
    except Exception as e:
        echo_error(str(e))
        server.server_close()


@cli.command()
@click.argument("name", required=False, default=None)
@click.option("--new", "-n", is_flag=True, help="Create a new dataset")
def init(name: str, new: bool):
    """Initialize dataset in current directory

    Examples:
        synphony init mydata        # Link to existing dataset 'mydata'
        synphony init --new         # Create new dataset (auto-named)
        synphony init --new mydata  # Create new dataset named 'mydata'
    """
    if Path(SYNPHONY_FILE).exists():
        echo_error(f"Already initialized (see {SYNPHONY_FILE})")
        return

    token = load_token()
    if not token:
        echo_error("Not authenticated. Run: synphony login")
        return

    if new:
        # Create new dataset (with optional name)
        result = create_dataset(token, name)
    elif name:
        # Link to existing dataset by name
        result = lookup_dataset(name, token)
        if not result:
            echo_info(f"To create a new dataset, use: synphony init --new {name}")
            return
    else:
        # No args - show usage
        echo_error("Please specify a dataset name or use --new")
        click.echo()
        echo_info("Usage:")
        echo_info("  synphony init <name>        Link to existing dataset")
        echo_info("  synphony init --new         Create new dataset")
        echo_info("  synphony init --new <name>  Create new dataset with name")
        return

    if not result:
        return

    save_dataset(result["dataset_id"], result["name"])
    Path(GENERATED_DIR).mkdir(exist_ok=True)

    echo_success(f"Initialized: {result['name']}")
    echo_info(f"Config: {SYNPHONY_FILE}")
    echo_info(f"Output: {GENERATED_DIR}/")


@cli.command("list")
def list_datasets():
    """List all your datasets"""
    token = load_token()
    if not token:
        echo_error("Not authenticated. Run: synphony login")
        return

    echo_step("Fetching datasets...")

    try:
        headers = {"X-API-Key": token, "Content-Type": "application/json"}
        response = requests.post(f"{API_BASE_URL}/list", headers=headers, timeout=10)

        if response.status_code == 401:
            echo_error("Invalid token. Run: synphony login")
            return

        if response.status_code != 200:
            echo_error(f"Failed to fetch datasets ({response.status_code})")
            return

        data = response.json()
        if not data.get("ok"):
            echo_error(data.get("error", "Unknown error"))
            return

        datasets = data.get("datasets", [])
        if not datasets:
            echo_info("No datasets found")
            return

        echo_success(f"Found {len(datasets)} dataset(s)\n")

        # Get current dataset ID if in a project
        current_id = load_dataset_id()

        for ds in datasets:
            marker = "*" if ds["id"] == current_id else " "
            name = ds["name"]
            orig = ds.get("original_files", 0)
            gen = ds.get("generated_files", 0)
            click.echo(f"  {marker} {name}")
            click.echo(f"      ID: {ds['id']}")
            click.echo(f"      Files: {orig} original, {gen} generated")
            click.echo()

        if current_id:
            echo_info("* = current directory")

    except requests.exceptions.Timeout:
        echo_error("Request timed out")
    except requests.exceptions.RequestException as e:
        echo_error(f"Network error: {e}")
    except Exception as e:
        echo_error(f"Error: {e}")


def fetch_remote_status(dataset_id: str, token: str) -> dict | None:
    try:
        headers = {"X-API-Key": token, "Content-Type": "application/json"}
        response = requests.post(f"{API_BASE_URL}/status", json={"dataset_id": dataset_id}, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        response_data = response.json()
        return response_data if response_data.get("ok") else None
    except:
        return None


@cli.command()
@click.option("--detailed", "-d", is_flag=True, help="Show detailed file list")
def status(detailed: bool):
    """Show dataset status"""
    dataset_id = load_dataset_id()
    dataset_name = load_dataset_name()
    if not dataset_id:
        echo_error("No dataset initialized. Run: synphony init")
        return

    token = load_token()
    if not token:
        echo_error("Not authenticated. Run: synphony login")
        return

    video_files = find_video_files()
    generated_files = []
    if Path(GENERATED_DIR).exists():
        for root, dirs, files in os.walk(GENERATED_DIR):
            for file in files:
                if is_video_file(os.path.join(root, file)):
                    generated_files.append(os.path.join(root, file))

    click.echo(f"\n  Dataset:     {dataset_name}")
    click.echo(f"  Local:       {len(video_files)} video(s)")
    click.echo(f"  Downloaded:  {len(generated_files)} file(s)")

    remote = fetch_remote_status(dataset_id, token)
    if not remote:
        echo_error("Could not fetch remote status")
        return

    summary = remote.get("summary", {})
    by_type = summary.get("by_type", {})
    by_status = summary.get("by_status", {})

    click.echo(f"\n  Remote files:")
    click.echo(f"    Original:   {by_type.get('original', 0)}")
    click.echo(f"    Generated:  {by_type.get('generated', 0)}")
    click.echo(f"    Augmented:  {by_type.get('augmented', 0)}")

    click.echo(f"\n  Status:")
    click.echo(f"    Pending:    {by_status.get('pending', 0)}")
    click.echo(f"    Processing: {by_status.get('processing', 0)}")
    click.echo(f"    Ready:      {by_status.get('ready', 0)}")
    error_count = by_status.get('error', 0)
    if error_count > 0:
        click.echo(click.style(f"    Error:      {error_count}", fg="red"))
    else:
        click.echo(f"    Error:      {error_count}")

    if detailed:
        files = remote.get("files", [])
        if files:
            click.echo(f"\n  Files ({len(files)}):")
            for f in files:
                status_str = f.get("status", "unknown")
                type_label = f.get("type", "?")
                name = f.get("name", "unknown")

                if status_str == "ready":
                    indicator = click.style("[OK]", fg="green")
                elif status_str == "error":
                    indicator = click.style("[ERR]", fg="red")
                elif status_str == "processing":
                    indicator = click.style("[...]", fg="yellow")
                else:
                    indicator = "[--]"

                click.echo(f"    {indicator} [{type_label}] {name}")
        else:
            click.echo("\n  No files in dataset.")


def fetch_pull_urls(dataset_id: str, token: str) -> dict | None:
    try:
        headers = {"X-API-Key": token, "Content-Type": "application/json"}
        response = requests.post(f"{API_BASE_URL}/pull", json={"dataset_id": dataset_id}, headers=headers, timeout=30)
        if response.status_code != 200:
            return None
        response_data = response.json()
        return response_data if response_data.get("ok") else None
    except Exception as e:
        echo_error(f"Failed to fetch download URLs: {e}")
        return None


def download_file(url: str, dest_path: Path, expected_size: int | None = None) -> bool:
    try:
        response = requests.get(url, stream=True, timeout=300)
        response.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
        return True
    except Exception:
        if dest_path.exists():
            dest_path.unlink()
        return False


def download_single_file(file_info: dict, gen_dir: Path, force: bool) -> tuple[str, str, int]:
    """Download a single file. Returns (name, status, size)"""
    name = file_info.get("name", "unknown")
    size = file_info.get("size", 0)
    url = file_info.get("presigned_url")

    if not url:
        return (name, "no_url", size)

    dest_path = gen_dir / name

    if not force and dest_path.exists():
        local_size = dest_path.stat().st_size
        if size and local_size == size:
            return (name, "skipped", size)

    if download_file(url, dest_path, size):
        return (name, "downloaded", size)
    else:
        return (name, "failed", size)


@cli.command()
@click.option("--force", "-f", is_flag=True, help="Re-download existing files")
@click.option("--workers", "-w", default=MAX_CONCURRENT_DOWNLOADS, help="Concurrent downloads")
def pull(force: bool, workers: int):
    """Download generated files"""
    dataset_id = load_dataset_id()
    dataset_name = load_dataset_name()
    if not dataset_id:
        echo_error("No dataset initialized. Run: synphony init")
        return

    token = load_token()
    if not token:
        echo_error("Not authenticated. Run: synphony login")
        return

    echo_step(f"Pulling: {dataset_name}")

    result = fetch_pull_urls(dataset_id, token)
    if not result:
        echo_error("Could not fetch download URLs")
        return

    files = result.get("files", [])
    if not files:
        echo_info("No files ready for download")
        return

    echo_info(f"Found {len(files)} file(s)")

    gen_dir = Path(GENERATED_DIR)
    gen_dir.mkdir(exist_ok=True)

    downloaded = 0
    skipped = 0
    failed = 0
    total_bytes = 0

    # Download concurrently
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(download_single_file, f, gen_dir, force): f for f in files}

        for future in as_completed(futures):
            name, status, size = future.result()

            if status == "downloaded":
                echo_success(f"{name} ({format_bytes(size)})")
                downloaded += 1
                total_bytes += size
            elif status == "skipped":
                echo_info(f"{name} (skipped)")
                skipped += 1
            elif status == "no_url":
                echo_error(f"{name} - no URL")
                failed += 1
            else:
                echo_error(f"{name} - failed")
                failed += 1

    click.echo(f"\n  Downloaded: {downloaded} ({format_bytes(total_bytes)})")
    if skipped > 0:
        click.echo(f"  Skipped:    {skipped}")
    if failed > 0:
        click.echo(click.style(f"  Failed:     {failed}", fg="red"))
    click.echo(f"  Location:   {GENERATED_DIR}/")


@cli.command()
@click.argument("file_patterns", nargs=-1)
@click.option("--prompts", "-p", multiple=True, help="Processing prompts")
def multiply(file_patterns, prompts):
    """Process videos with prompts

    Examples:
        synphony multiply .
        synphony multiply *.mp4
        synphony multiply video.mp4 -p "prompt 1" -p "prompt 2"
    """
    dataset_id = load_dataset_id()
    if not dataset_id:
        echo_error("No dataset initialized. Run: synphony init")
        return

    token = load_token()
    if not token:
        echo_error("Not authenticated. Run: synphony login")
        return

    if file_patterns:
        video_files = find_video_files_by_pattern(file_patterns)
    else:
        video_files = find_video_files()

    if not video_files:
        echo_error("No video files found")
        return

    echo_step(f"Found {len(video_files)} video(s)")
    for f in video_files:
        echo_info(f)

    prompts_list = list(prompts) if prompts else []
    if not prompts_list:
        click.echo("\n  Enter prompts (empty line to finish):")
        while True:
            try:
                prompt = click.prompt("  >", default="", show_default=False)
                if not prompt:
                    break
                prompts_list.append(prompt)
            except EOFError:
                break

    if not prompts_list:
        echo_error("At least one prompt is required")
        return

    echo_info(f"Prompts: {len(prompts_list)}")

    upload_result = upload_videos(dataset_id, video_files, token)
    if not upload_result:
        return

    file_ids = [f['file_id'] for f in upload_result['files']]

    multiply_result = call_multiply_endpoint(dataset_id, file_ids, prompts_list, token)
    if not multiply_result:
        return

    Path(GENERATED_DIR).mkdir(exist_ok=True)

    dataset_name = load_dataset_name()
    click.echo(f"\n  Dataset:   {dataset_name}")
    click.echo(f"  Files:     {multiply_result.get('files_processed', len(file_ids))}")
    click.echo(f"  Prompts:   {len(prompts_list)}")
    click.echo(f"  Tasks:     {multiply_result.get('tasks_sent', 0)}")
    click.echo(f"  Output:    {multiply_result.get('total_generated_files', 0)} file(s)")
    click.echo(f"\n  Run 'synphony status' to check progress")
    click.echo(f"  Run 'synphony pull' when ready")


# Augmentation definitions with defaults
AUGMENTATIONS = {
    "flip": {
        "name": "RandomHorizontalFlip",
        "defaults": {"p": 1, "same_on_batch": 0}
    },
    "rotation": {
        "name": "RandomRotation",
        "defaults": {"p": 1, "degrees": 45, "resample": "bilinear"}
    },
    "affine": {
        "name": "RandomAffine",
        "defaults": {"p": 1, "degrees": 45}
    },
    "perspective": {
        "name": "RandomPerspective",
        "defaults": {"p": 1, "distortion_scale": 0.5, "resample": "bilinear"}
    },
    "crop": {
        "name": "RandomResizedCrop",
        "defaults": {"p": 1, "size": 0.5}
    },
    "noise": {
        "name": "RandomGaussianNoise",
        "defaults": {"p": 1, "mean": 0, "std": 1}
    },
    "jitter": {
        "name": "ColorJitter",
        "defaults": {"p": 1, "brightness": 1, "contrast": 1}
    },
    "erasing": {
        "name": "RandomErasing",
        "defaults": {"p": 1}
    }
}


def parse_aug_params(param_str: str) -> dict:
    """Parse key=value,key=value string into dict with type conversion."""
    if not param_str:
        return {}
    params = {}
    for pair in param_str.split(","):
        if "=" not in pair:
            continue
        key, value = pair.split("=", 1)
        key = key.strip()
        value = value.strip()
        # Try to convert to appropriate type
        if value.lower() in ("true", "false"):
            params[key] = value.lower() == "true"
        elif value in ("nearest", "bilinear"):
            params[key] = value
        else:
            try:
                params[key] = int(value)
            except ValueError:
                try:
                    params[key] = float(value)
                except ValueError:
                    params[key] = value
    return params


def build_aug_list(flip, rotation, affine, perspective, crop, noise, jitter, erasing, all_augs, config) -> list:
    """Build augmentation list from CLI flags or config file."""
    aug_list = []

    # If config file provided, use that
    if config:
        try:
            with open(config, "r") as f:
                config_data = json.load(f)
            for item in config_data:
                aug_list.append({
                    "augName": item["name"],
                    "augParams": item.get("params", {})
                })
            return aug_list
        except Exception as e:
            echo_error(f"Failed to load config file: {e}")
            return []

    # If --all flag, add all augmentations with defaults
    if all_augs:
        for aug_key, aug_info in AUGMENTATIONS.items():
            aug_list.append({
                "augName": aug_info["name"],
                "augParams": aug_info["defaults"].copy()
            })
        return aug_list

    # Process individual flags
    flag_values = {
        "flip": flip,
        "rotation": rotation,
        "affine": affine,
        "perspective": perspective,
        "crop": crop,
        "noise": noise,
        "jitter": jitter,
        "erasing": erasing
    }

    for aug_key, flag_value in flag_values.items():
        if flag_value is None:
            continue

        aug_info = AUGMENTATIONS[aug_key]
        params = aug_info["defaults"].copy()

        # If flag has a value (not just True), parse it
        if flag_value and flag_value is not True:
            custom_params = parse_aug_params(flag_value)
            params.update(custom_params)

        aug_list.append({
            "augName": aug_info["name"],
            "augParams": params
        })

    return aug_list


def call_augment_endpoint(dataset_id: str, file_ids: List[str], aug_list: list, token: str) -> dict | None:
    """Call the augment API endpoint."""
    try:
        headers = {"X-API-Key": token, "Content-Type": "application/json"}
        payload = {"dataset_id": dataset_id, "file_ids": file_ids, "aug_list": aug_list}

        echo_step("Submitting augmentation tasks")
        response = requests.post(f"{API_BASE_URL}/augment", json=payload, headers=headers, timeout=30)

        if response.status_code != 200:
            echo_error(f"Failed to submit tasks (HTTP {response.status_code})")
            try:
                error_data = response.json()
                if error_data.get("error"):
                    echo_error(error_data["error"])
            except:
                pass
            return None

        response_data = response.json()
        if not response_data.get("ok"):
            echo_error(response_data.get('error', 'Unknown error'))
            return None

        return response_data

    except requests.exceptions.RequestException as e:
        echo_error(f"Network error: {str(e)}")
        return None
    except Exception as e:
        echo_error(str(e))
        return None


@cli.command()
@click.argument("file_patterns", nargs=-1)
@click.option("--flip", is_flag=False, flag_value=True, default=None, help="Horizontal flip")
@click.option("--rotation", is_flag=False, flag_value=True, default=None, help="Random rotation (e.g. --rotation or --rotation degrees=30,p=0.8)")
@click.option("--affine", is_flag=False, flag_value=True, default=None, help="Affine transformation")
@click.option("--perspective", is_flag=False, flag_value=True, default=None, help="Perspective transformation")
@click.option("--crop", is_flag=False, flag_value=True, default=None, help="Random resized crop")
@click.option("--noise", is_flag=False, flag_value=True, default=None, help="Gaussian noise (e.g. --noise or --noise std=0.5)")
@click.option("--jitter", is_flag=False, flag_value=True, default=None, help="Color jitter (e.g. --jitter or --jitter brightness=1.5,contrast=1.2)")
@click.option("--erasing", is_flag=False, flag_value=True, default=None, help="Random erasing/occlusion")
@click.option("--all", "all_augs", is_flag=True, help="Apply all augmentations with defaults")
@click.option("--config", "-c", type=click.Path(exists=True), help="JSON config file for augmentations")
def augment(file_patterns, flip, rotation, affine, perspective, crop, noise, jitter, erasing, all_augs, config):
    """Apply augmentations to videos

    Examples:
        synphony augment *.mp4 --flip --rotation --jitter
        synphony augment *.mp4 --rotation degrees=30,p=0.8
        synphony augment *.mp4 --all
        synphony augment *.mp4 --config augs.json
    """
    dataset_id = load_dataset_id()
    if not dataset_id:
        echo_error("No dataset initialized. Run: synphony init")
        return

    token = load_token()
    if not token:
        echo_error("Not authenticated. Run: synphony login")
        return

    # Build augmentation list
    aug_list = build_aug_list(flip, rotation, affine, perspective, crop, noise, jitter, erasing, all_augs, config)

    if not aug_list:
        echo_error("No augmentations specified")
        click.echo()
        echo_info("Usage:")
        echo_info("  synphony augment *.mp4 --flip --rotation --jitter")
        echo_info("  synphony augment *.mp4 --rotation degrees=30")
        echo_info("  synphony augment *.mp4 --all")
        echo_info("  synphony augment *.mp4 --config augs.json")
        click.echo()
        echo_info("Available augmentations:")
        echo_info("  --flip        Horizontal flip")
        echo_info("  --rotation    Random rotation (degrees, p, resample)")
        echo_info("  --affine      Affine transformation (degrees, p)")
        echo_info("  --perspective Perspective warp (distortion_scale, p)")
        echo_info("  --crop        Random resized crop (size, p)")
        echo_info("  --noise       Gaussian noise (mean, std, p)")
        echo_info("  --jitter      Color jitter (brightness, contrast, p)")
        echo_info("  --erasing     Random erasing (p)")
        return

    # Find video files
    if file_patterns:
        video_files = find_video_files_by_pattern(file_patterns)
    else:
        video_files = find_video_files()

    if not video_files:
        echo_error("No video files found")
        return

    echo_step(f"Found {len(video_files)} video(s)")
    for f in video_files:
        echo_info(f)

    echo_info(f"Augmentations: {len(aug_list)}")
    for aug in aug_list:
        echo_info(f"  - {aug['augName']}")

    # Upload videos first
    upload_result = upload_videos(dataset_id, video_files, token)
    if not upload_result:
        return

    file_ids = [f['file_id'] for f in upload_result['files']]

    # Call augment endpoint
    augment_result = call_augment_endpoint(dataset_id, file_ids, aug_list, token)
    if not augment_result:
        return

    Path(GENERATED_DIR).mkdir(exist_ok=True)

    dataset_name = load_dataset_name()
    click.echo(f"\n  Dataset:       {dataset_name}")
    click.echo(f"  Files:         {augment_result.get('files_processed', len(file_ids))}")
    click.echo(f"  Augmentations: {augment_result.get('augmentations_applied', len(aug_list))}")
    click.echo(f"\n  Run 'synphony status' to check progress")
    click.echo(f"  Run 'synphony pull' when ready")


if __name__ == "__main__":
    cli()
