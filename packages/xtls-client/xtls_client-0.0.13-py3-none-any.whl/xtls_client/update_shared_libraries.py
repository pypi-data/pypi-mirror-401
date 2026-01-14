import requests
from pathlib import Path
import time

shared_library_version = "1.13.1"
github_download_url = "https://github.com/bogdanfinn/tls-client/releases/download/v{}/{}"
github_repo_filenames = [
    # Windows
    f"tls-client-windows-32-{shared_library_version}.dll",
    f"tls-client-windows-64-{shared_library_version}.dll",
    # MacOS
    f"tls-client-darwin-arm64-{shared_library_version}.dylib",
    f"tls-client-darwin-amd64-{shared_library_version}.dylib",
    # Linux
    f"tls-client-linux-alpine-amd64-{shared_library_version}.so",
    f"tls-client-linux-ubuntu-amd64-{shared_library_version}.so",
    f"tls-client-linux-arm64-{shared_library_version}.so"
]
dependency_filenames = [
    # Windows
    "tls-client-32.dll",
    "tls-client-64.dll",
    # MacOS
    "tls-client-arm64.dylib",
    "tls-client-x86.dylib",
    # Linux
    "tls-client-amd64.so",
    "tls-client-x86.so",
    "tls-client-arm64.so"
]

dependencies_dir = Path(__file__).resolve().parent / "dependencies"
dependencies_dir.mkdir(parents=True, exist_ok=True)

session = requests.Session()

for github_filename, dependency_filename in zip(github_repo_filenames, dependency_filenames):
    url = github_download_url.format(shared_library_version, github_filename)
    target_path = dependencies_dir / dependency_filename
    tmp_path = target_path.with_suffix(target_path.suffix + ".tmp")

    last_error = None
    for attempt in range(3):
        try:
            response = session.get(url=url, timeout=60)
            response.raise_for_status()
            if not response.content:
                raise RuntimeError(f"empty response: {url}")

            content_type = (response.headers.get("Content-Type") or "").lower()
            if "text/html" in content_type:
                raise RuntimeError(f"unexpected content-type {content_type}: {url}")

            tmp_path.write_bytes(response.content)
            tmp_path.replace(target_path)
            last_error = None
            break
        except Exception as e:
            last_error = e
            time.sleep(1 + attempt)

    if last_error is not None:
        raise last_error
