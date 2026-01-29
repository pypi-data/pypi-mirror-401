"""
Installation and configuration logic for serena-vbnet.
"""

import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path
from typing import List, Dict, Any
import requests

from . import __version__

# Installation paths
SERENA_DIR = Path.home() / ".serena"
LS_DIR = SERENA_DIR / "language_servers" / "roslyn_vbnet"

# GitHub repository for pre-built binaries
GITHUB_REPO = "LaunchCG/roslyn-vbnet-languageserver"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


def get_platform_rid() -> str:
    """Detect platform runtime identifier (RID)"""
    system = platform.system().lower()
    machine = platform.machine().lower()

    # Map to .NET RIDs
    if system == "linux":
        if machine in ["x86_64", "amd64"]:
            return "linux-x64"
        elif machine in ["aarch64", "arm64"]:
            return "linux-arm64"
    elif system == "darwin":
        if machine == "x86_64":
            return "osx-x64"
        elif machine in ["arm64", "aarch64"]:
            return "osx-arm64"
    elif system == "windows":
        if machine in ["amd64", "x86_64"]:
            return "win-x64"
        elif machine in ["arm64", "aarch64"]:
            return "win-arm64"

    raise RuntimeError(f"Unsupported platform: {system}/{machine}")


def download_prebuilt_binary() -> Path:
    """Download pre-built binary from GitHub Releases"""
    rid = get_platform_rid()
    print(f"Detected platform: {rid}")

    # Get latest release info
    print(f"Fetching latest release from {GITHUB_REPO}...")
    response = requests.get(GITHUB_API)
    response.raise_for_status()

    release_data = response.json()
    tag_name = release_data["tag_name"]
    print(f"Latest version: {tag_name}")

    # Find asset for this platform
    ext = "zip" if "win" in rid else "tar.gz"
    asset_name = f"roslyn-vbnet-{rid}.{ext}"

    asset = None
    for a in release_data["assets"]:
        if a["name"] == asset_name:
            asset = a
            break

    if not asset:
        raise RuntimeError(f"No pre-built binary found for {rid}")

    # Download
    download_url = asset["browser_download_url"]
    print(f"Downloading {asset_name}...")

    response = requests.get(download_url, stream=True)
    response.raise_for_status()

    # Save to temp file
    temp_file = Path(tempfile.gettempdir()) / asset_name
    with open(temp_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Downloaded to {temp_file}")
    return temp_file


def extract_binary(archive_path: Path, dest_dir: Path):
    """Extract downloaded binary to destination"""
    print(f"Extracting to {dest_dir}...")

    # Create destination
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Extract based on file type
    if archive_path.suffix == ".zip":
        with zipfile.ZipFile(archive_path, "r") as zip_ref:
            zip_ref.extractall(dest_dir)
    else:  # .tar.gz
        with tarfile.open(archive_path, "r:gz") as tar_ref:
            tar_ref.extractall(dest_dir)

    # Handle nested directory structure (e.g., LanguageServer subdirectory)
    # If extraction created a single subdirectory containing the DLLs, flatten it
    _flatten_single_subdirectory(dest_dir)

    print("[OK] Extraction complete")


def _flatten_single_subdirectory(dest_dir: Path):
    """
    If dest_dir contains a single subdirectory with the actual files,
    move everything up one level and remove the empty subdirectory.
    """
    items = list(dest_dir.iterdir())

    # Check if there's a LanguageServer subdirectory or similar containing the DLLs
    language_server_dir = dest_dir / "LanguageServer"
    if language_server_dir.exists() and language_server_dir.is_dir():
        main_dll = language_server_dir / "Microsoft.CodeAnalysis.LanguageServer.dll"
        if main_dll.exists():
            print("Flattening LanguageServer subdirectory...")
            # Move all files from LanguageServer to dest_dir
            for item in language_server_dir.iterdir():
                target = dest_dir / item.name
                if target.exists():
                    if target.is_dir():
                        shutil.rmtree(target)
                    else:
                        target.unlink()
                shutil.move(str(item), str(target))
            # Remove the now-empty LanguageServer directory
            language_server_dir.rmdir()
            return

    # Generic case: if there's exactly one subdirectory and no files at root level
    # (except maybe VERSION.txt or similar metadata), flatten it
    subdirs = [item for item in items if item.is_dir()]
    files = [item for item in items if item.is_file()]

    if len(subdirs) == 1 and len(files) <= 1:
        subdir = subdirs[0]
        # Check if the subdir contains the main DLL
        main_dll = subdir / "Microsoft.CodeAnalysis.LanguageServer.dll"
        if main_dll.exists():
            print(f"Flattening {subdir.name} subdirectory...")
            # Move all files from subdir to dest_dir
            for item in subdir.iterdir():
                target = dest_dir / item.name
                if target.exists():
                    if target.is_dir():
                        shutil.rmtree(target)
                    else:
                        target.unlink()
                shutil.move(str(item), str(target))
            # Remove the now-empty subdirectory
            subdir.rmdir()


def build_from_source():
    """Build Roslyn LanguageServer from source"""
    print("Building from source...")
    print("This will take 10-15 minutes...")

    # Check for .NET SDK
    try:
        result = subprocess.run(
            ["dotnet", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"Using .NET SDK: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError(
            ".NET SDK not found. Please install .NET 8 SDK or later from https://dot.net"
        )

    # Get build script from GitHub
    temp_dir = Path(tempfile.gettempdir())
    script_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/scripts/build-roslyn-vbnet.sh"
    script_path = temp_dir / "build-roslyn-vbnet.sh"

    print("Downloading build script...")
    response = requests.get(script_url)
    response.raise_for_status()

    script_path.write_text(response.text)
    script_path.chmod(0o755)

    # Run build
    rid = get_platform_rid()
    print(f"Building for {rid}...")

    result = subprocess.run(
        [str(script_path), rid],
        cwd=str(temp_dir),
        check=True,
    )

    # Copy output
    source_dir = temp_dir / "roslyn-build" / "output"
    if not source_dir.exists():
        raise RuntimeError("Build failed - output directory not found")

    LS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Copying to {LS_DIR}...")
    for item in source_dir.iterdir():
        if item.is_file():
            shutil.copy2(item, LS_DIR / item.name)
        elif item.is_dir():
            shutil.copytree(item, LS_DIR / item.name, dirs_exist_ok=True)

    print("[OK] Build complete")


def install_language_server(force: bool = False, from_source: bool = False):
    """Install VB.NET language server"""
    if LS_DIR.exists() and not force:
        print(f"Language server already installed at {LS_DIR}")
        print("Use --force to reinstall")
        return

    if LS_DIR.exists():
        print("Removing existing installation...")
        shutil.rmtree(LS_DIR)

    if from_source:
        build_from_source()
    else:
        try:
            archive_path = download_prebuilt_binary()
            extract_binary(archive_path, LS_DIR)
            archive_path.unlink()  # Clean up
        except Exception as e:
            print(f"[WARN] Failed to download pre-built binary: {e}")
            print("Falling back to build from source...")
            build_from_source()

    # Verify language server files only (not Serena patching - that happens in Step 2)
    issues = verify_language_server_files()
    if issues:
        raise RuntimeError(f"Installation incomplete: {', '.join(issues)}")


def find_serena_installation() -> Path:
    """Find Serena's solidlsp package installation"""
    try:
        import solidlsp
        path = Path(solidlsp.__file__).parent

        # Check if this is a UV cache path - warn user
        path_str = str(path).lower()
        if "uv" in path_str and "cache" in path_str:
            print("[WARN] Detected UV cache installation path!")
            print(f"  Path: {path}")
            print("  UV caches packages separately from site-packages.")
            print("  If you encounter 'Invalid language: vbnet' errors, run:")
            print("    uv cache clean")
            print("    pip uninstall serena-agent && pip install serena-agent")
            print("    serena-vbnet setup --force")

        return path
    except ImportError:
        raise RuntimeError(
            "Serena not found. Please install: pip install serena-agent"
        )


def find_serena_config_path() -> Path:
    """Find Serena's config module where Language enum is defined"""
    try:
        import serena.config.serena_config as serena_config
        return Path(serena_config.__file__)
    except ImportError:
        # Try alternative import
        try:
            import serena
            serena_path = Path(serena.__file__).parent
            config_path = serena_path / "config" / "serena_config.py"
            if config_path.exists():
                return config_path
        except ImportError:
            pass
        raise RuntimeError(
            "Serena config not found. Please install: pip install serena-agent"
        )


def patch_serena():
    """Add VB.NET support to Serena"""
    solidlsp_path = find_serena_installation()
    ls_config_path = solidlsp_path / "ls_config.py"

    if not ls_config_path.exists():
        raise RuntimeError(f"ls_config.py not found at {ls_config_path}")

    # Find serena config path for Language enum
    try:
        serena_config_path = find_serena_config_path()
    except RuntimeError:
        serena_config_path = None
        print("[WARN] Could not find serena_config.py - Language enum may not be patched")

    # Copy vbnet_language_server.py into Serena's solidlsp/language_servers directory
    language_servers_path = solidlsp_path / "language_servers"
    if not language_servers_path.exists():
        raise RuntimeError(f"Language servers directory not found: {language_servers_path}")

    # Copy our vbnet_language_server.py
    source_file = Path(__file__).parent / "vbnet_language_server.py"
    dest_file = language_servers_path / "vbnet_language_server.py"

    if not dest_file.exists() or True:  # Always copy to ensure latest version
        print(f"Copying VB.NET language server to {dest_file}...")
        shutil.copy(source_file, dest_file)
        print("[OK] VB.NET language server file installed")

    # Patch serena_config.py first (for Language enum validation)
    if serena_config_path and serena_config_path.exists():
        _patch_serena_config(serena_config_path)

    # Patch ls_config.py (for Language enum and file matcher)
    _patch_ls_config(ls_config_path)

    # Patch ls.py (for language server instantiation)
    ls_py_path = solidlsp_path / "ls.py"
    if ls_py_path.exists():
        _patch_ls_py(ls_py_path)


def _patch_serena_config(config_path: Path):
    """Patch serena/config/serena_config.py to add VBNET to Language enum"""
    print(f"[DEBUG] Config path: {config_path}")
    print(f"[DEBUG] Path exists: {config_path.exists()}")
    print(f"[DEBUG] Path is file: {config_path.is_file()}")

    try:
        import os
        print(f"[DEBUG] File permissions: {oct(os.stat(config_path).st_mode)}")
        print(f"[DEBUG] File writable: {os.access(config_path, os.W_OK)}")
    except Exception as e:
        print(f"[DEBUG] Could not check permissions: {e}")

    print(f"Reading {config_path}...")
    content = config_path.read_text()

    print(f"[DEBUG] File size: {len(content)} bytes")
    print(f"[DEBUG] File lines: {len(content.splitlines())}")

    # Check if already patched (case-insensitive)
    if "vbnet" in content.lower():
        print("serena_config.py already has VB.NET support")
        return

    print(f"Patching {config_path}...")

    lines = content.split("\n")
    patched = False
    insert_index = -1

    # Find the Language class definition first
    in_language_class = False
    class_indent = 0
    found_language_class = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Look for class Language definition (be more flexible)
        if "class Language" in line:
            in_language_class = True
            found_language_class = True
            class_indent = len(line) - len(line.lstrip())
            print(f"  Found Language class at line {i+1}: {line.strip()[:60]}")
            continue

        if in_language_class:
            # Check if we've left the class (less indentation or new class/def)
            current_indent = len(line) - len(line.lstrip()) if stripped else class_indent + 4
            if stripped and current_indent <= class_indent and not stripped.startswith('#'):
                if stripped.startswith('class ') or stripped.startswith('def '):
                    print(f"  Left Language class at line {i+1}")
                    break

            # Look for any enum entry pattern: name = "name" or name = 'name'
            if '=' in stripped and ('"' in stripped or "'" in stripped):
                # Try to extract name = "value" pattern
                try:
                    if '= "' in stripped:
                        parts = stripped.split('= "')
                        quote = '"'
                    elif "= '" in stripped:
                        parts = stripped.split("= '")
                        quote = "'"
                    else:
                        continue

                    if len(parts) == 2:
                        name = parts[0].strip()
                        value = parts[1].rstrip(quote).rstrip("'\"")
                        # Check if this looks like a language enum entry (name matches value)
                        if name.lower() == value.lower() and name.replace('_', '').isalpha():
                            insert_index = i
                            # Remember the indent of enum entries
                            entry_indent = len(line) - len(line.lstrip())
                            print(f"  Found enum entry '{name}' at line {i+1}")
                except Exception as e:
                    print(f"  [DEBUG] Parse error on line {i+1}: {e}")

    if not found_language_class:
        # Language enum might be imported from solidlsp.ls_config instead
        # Check if it's imported
        for line in lines:
            if "from solidlsp" in line and "Language" in line:
                print("  Language enum is imported from solidlsp.ls_config (will be patched there)")
                return  # Don't fail - ls_config.py will be patched instead
        print("[DEBUG] Searching for any 'Language' in file...")
        for i, line in enumerate(lines):
            if "Language" in line:
                print(f"  Line {i+1}: {line.strip()[:80]}")

    # Insert vbnet after the last found enum entry
    if insert_index >= 0:
        entry_indent = len(lines[insert_index]) - len(lines[insert_index].lstrip())
        vbnet_line = " " * entry_indent + 'vbnet = "vbnet"'
        lines.insert(insert_index + 1, vbnet_line)
        patched = True
        print(f"[DEBUG] Will insert at line {insert_index + 2}: {vbnet_line}")

    if patched:
        new_content = "\n".join(lines)
        print(f"[DEBUG] New content size: {len(new_content)} bytes")
        try:
            config_path.write_text(new_content)
            print("[DEBUG] Write completed")
            # Verify the write worked
            verify_content = config_path.read_text()
            print(f"[DEBUG] Re-read file size: {len(verify_content)} bytes")
            if "vbnet" in verify_content.lower():
                print("[OK] serena_config.py patched with vbnet language")
            else:
                print("[ERROR] Write appeared to succeed but vbnet not found in file!")
                print("[DEBUG] This may indicate UV cache issue - try: uv cache clean")
        except PermissionError as e:
            print(f"[ERROR] Permission denied writing to {config_path}: {e}")
            print("  Try running as Administrator or check file permissions")
            print("  If using UV, try: uv cache clean && pip install --force-reinstall serena-agent")
        except Exception as e:
            print(f"[ERROR] Failed to write {config_path}: {e}")
    else:
        print("[ERROR] Could not find Language enum entries in serena_config.py")
        if found_language_class:
            print("  Language class was found but no enum entries detected")
            print("[DEBUG] Showing first 30 lines of Language class:")
            in_class = False
            shown = 0
            for i, line in enumerate(lines):
                if "class Language" in line:
                    in_class = True
                if in_class and shown < 30:
                    print(f"  {i+1}: {line}")
                    shown += 1
        else:
            print("  Language class not found in file")
        print("  File may have unexpected format. Please report this issue.")


def _patch_ls_config(ls_config_path: Path):
    """Patch solidlsp/ls_config.py for language server configuration"""
    content = ls_config_path.read_text()

    # Check what's already patched - we need both enum and file matcher
    has_enum = 'VBNET = "vbnet"' in content
    has_file_matcher = 'case self.VBNET:' in content and '*.vb' in content

    if has_enum and has_file_matcher:
        print("ls_config.py already fully configured for VB.NET")
        return

    print(f"Patching {ls_config_path}...")
    lines = content.split("\n")
    modified = False

    # Step 1: Add VBNET to Language enum (skip if already present)
    if "class Language(str, Enum):" in content and not has_enum:
        in_language_class = False
        last_enum_index = -1
        enum_indent = 4  # default

        for i, line in enumerate(lines):
            if "class Language(str, Enum):" in line:
                in_language_class = True
                continue

            if in_language_class:
                stripped = line.strip()
                # Check if we've left the class
                if stripped and not stripped.startswith('#') and not stripped.startswith('"'):
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent == 0 and stripped:
                        break
                    # Look for enum entries: NAME = "value"
                    if '=' in stripped and '"' in stripped:
                        # Check pattern: UPPERCASE = "lowercase"
                        parts = stripped.split('=')
                        if len(parts) == 2:
                            name = parts[0].strip()
                            if name.isupper() or name.replace('_', '').isalpha():
                                last_enum_index = i
                                enum_indent = len(line) - len(line.lstrip())
                    # Stop at methods or other class definitions
                    if stripped.startswith('@') or stripped.startswith('def ') or stripped.startswith('class '):
                        break

        if last_enum_index >= 0:
            vbnet_line = " " * enum_indent + 'VBNET = "vbnet"'
            lines.insert(last_enum_index + 1, vbnet_line)
            modified = True
            print(f"  Added VBNET to Language enum after line {last_enum_index + 1}")

    # Rebuild content after enum modification
    content = "\n".join(lines)
    lines = content.split("\n")

    # Step 2: Add file matcher for .vb files (skip if already present)
    file_matcher_method = None
    if has_file_matcher:
        print("  File matcher already present, skipping")
    else:
        # Find the file matcher method (may be named file_matcher or get_source_fn_matcher)
        if "def get_source_fn_matcher(self)" in content:
            file_matcher_method = "def get_source_fn_matcher(self)"
        elif "def file_matcher(self)" in content:
            file_matcher_method = "def file_matcher(self)"

    if not has_file_matcher and file_matcher_method and "FilenameMatcher" in content:
        in_file_matcher = False
        last_case_return_index = -1
        case_indent = 16  # typical indent for case statements

        for i, line in enumerate(lines):
            if file_matcher_method in line:
                in_file_matcher = True
                continue

            if in_file_matcher:
                stripped = line.strip()
                # Look for case statements with FilenameMatcher returns
                if stripped.startswith("case self.") and ":" in stripped:
                    # Find the corresponding return statement
                    for j in range(i + 1, min(i + 5, len(lines))):
                        if "return FilenameMatcher" in lines[j]:
                            last_case_return_index = j
                            case_indent = len(lines[i]) - len(lines[i].lstrip())
                            break
                # Stop at next def or end of match
                if stripped.startswith("def ") or (stripped and not stripped.startswith("case") and "return" not in stripped.lower() and not stripped.startswith("#")):
                    if "raise" in stripped or stripped.startswith("def "):
                        break

        if last_case_return_index >= 0:
            # Insert after the last case's return
            return_indent = len(lines[last_case_return_index]) - len(lines[last_case_return_index].lstrip())
            new_case = " " * case_indent + "case self.VBNET:"
            new_return = " " * return_indent + 'return FilenameMatcher("*.vb")'
            lines.insert(last_case_return_index + 1, new_case)
            lines.insert(last_case_return_index + 2, new_return)
            modified = True
            print(f"  Added VBNET file matcher case")

    # Rebuild content
    content = "\n".join(lines)
    lines = content.split("\n")

    # Step 3: Add import for VBNetLanguageServer
    # Find last language_server import
    last_import_index = -1
    for i, line in enumerate(lines):
        if "from solidlsp.language_servers." in line and "import" in line:
            last_import_index = i

    if last_import_index >= 0:
        import_line = "from solidlsp.language_servers.vbnet_language_server import VBNetLanguageServer"
        if import_line not in content:
            lines.insert(last_import_index + 1, import_line)
            modified = True
            print(f"  Added VBNetLanguageServer import")

    # Rebuild content
    content = "\n".join(lines)
    lines = content.split("\n")

    # Step 4: Add case for VBNET in language_server property
    if "def language_server(self)" in content:
        in_language_server = False
        last_ls_case_return_index = -1
        case_indent = 12

        for i, line in enumerate(lines):
            if "def language_server(self)" in line:
                in_language_server = True
                continue

            if in_language_server:
                stripped = line.strip()
                if stripped.startswith("case self.") and ":" in stripped:
                    for j in range(i + 1, min(i + 5, len(lines))):
                        if "return " in lines[j] and "LanguageServer" in lines[j]:
                            last_ls_case_return_index = j
                            case_indent = len(lines[i]) - len(lines[i].lstrip())
                            break
                if stripped.startswith("def ") or "raise" in stripped:
                    break

        if last_ls_case_return_index >= 0:
            return_indent = len(lines[last_ls_case_return_index]) - len(lines[last_ls_case_return_index].lstrip())
            new_case = " " * case_indent + "case self.VBNET:"
            new_return = " " * return_indent + "return VBNetLanguageServer"
            lines.insert(last_ls_case_return_index + 1, new_case)
            lines.insert(last_ls_case_return_index + 2, new_return)
            modified = True
            print(f"  Added VBNET language_server case")

    if modified:
        content = "\n".join(lines)
        ls_config_path.write_text(content)
        print("[OK] ls_config.py patched successfully")
    else:
        print("[WARN] Could not find insertion points in ls_config.py")
        print("  File format may have changed. Please report this issue.")


def _patch_ls_py(ls_py_path: Path):
    """Patch solidlsp/ls.py to add VBNET language server instantiation"""
    content = ls_py_path.read_text()

    # Check if already patched correctly
    if "VBNetLanguageServer(config, repository_root_path, solidlsp_settings)" in content:
        print("ls.py already configured for VB.NET with correct signature")
        return

    # Check if patched with wrong signature (from v1.0.14 and earlier)
    if "VBNetLanguageServer(config, logger, repository_root_path, solidlsp_settings=" in content:
        print("ls.py has VB.NET with incorrect signature, re-patching...")
        # Remove the old patch
        lines = content.split("\n")
        filtered_lines = [
            line for line in lines
            if "VBNET" not in line and "VBNetLanguageServer" not in line and "vbnet_language_server" not in line
        ]
        content = "\n".join(filtered_lines)
        ls_py_path.write_text(content)
        # Continue to re-patch with correct signature

    print(f"Patching {ls_py_path}...")
    lines = content.split("\n")
    modified = False

    # Find the last elif case for Language.SOMETHING before the else clause
    # Pattern: elif config.code_language == Language.BASH:
    last_elif_index = -1
    elif_indent = 8  # typical indent

    for i, line in enumerate(lines):
        if "elif config.code_language == Language." in line:
            last_elif_index = i
            elif_indent = len(line) - len(line.lstrip())

    if last_elif_index >= 0:
        # Find where this elif block ends (next elif or else)
        block_end_index = last_elif_index + 1
        for j in range(last_elif_index + 1, len(lines)):
            stripped = lines[j].strip()
            if stripped.startswith("elif ") or stripped.startswith("else:"):
                block_end_index = j
                break

        # Insert our VBNET case before the else clause
        vbnet_block = [
            "",
            " " * elif_indent + "elif config.code_language == Language.VBNET:",
            " " * elif_indent + "    from solidlsp.language_servers.vbnet_language_server import VBNetLanguageServer",
            "",
            " " * elif_indent + "    ls = VBNetLanguageServer(config, repository_root_path, solidlsp_settings)",
        ]

        for idx, vbnet_line in enumerate(vbnet_block):
            lines.insert(block_end_index + idx, vbnet_line)

        modified = True
        print("  Added VBNET case to ls.py")

    if modified:
        content = "\n".join(lines)
        ls_py_path.write_text(content)
        print("[OK] ls.py patched successfully")
    else:
        print("[WARN] Could not find insertion point in ls.py")


def unpatch_serena():
    """Remove VB.NET support from Serena"""
    # Unpatch ls_config.py
    serena_path = find_serena_installation()
    ls_config_path = serena_path / "ls_config.py"

    if ls_config_path.exists():
        content = ls_config_path.read_text()
        if "VBNET" in content or "VBNetLanguageServer" in content:
            lines = content.split("\n")
            filtered_lines = [
                line
                for line in lines
                if "VBNET" not in line and "VBNetLanguageServer" not in line and "vbnet_language_server" not in line
            ]
            ls_config_path.write_text("\n".join(filtered_lines))
            print("[OK] ls_config.py unpatched")

    # Unpatch serena_config.py
    try:
        serena_config_path = find_serena_config_path()
        if serena_config_path.exists():
            content = serena_config_path.read_text()
            if "VBNET" in content or '"vbnet"' in content:
                lines = content.split("\n")
                filtered_lines = [
                    line
                    for line in lines
                    if "VBNET" not in line and '"vbnet"' not in line
                ]
                serena_config_path.write_text("\n".join(filtered_lines))
                print("[OK] serena_config.py unpatched")
    except RuntimeError:
        pass  # serena_config.py not found, skip

    print("[OK] Serena unpatched")


def verify_language_server_files() -> List[str]:
    """Verify language server files are installed (DLLs only, not Serena patching)"""
    issues = []

    # Check language server directory
    if not LS_DIR.exists():
        issues.append("Language server directory not found")
        return issues

    # Check main DLL
    main_dll = LS_DIR / "Microsoft.CodeAnalysis.LanguageServer.dll"
    if not main_dll.exists():
        issues.append("Main language server DLL not found")

    # Check VB.NET assemblies
    vb_dlls = [
        "Microsoft.CodeAnalysis.VisualBasic.dll",
        "Microsoft.CodeAnalysis.VisualBasic.Features.dll",
        "Microsoft.CodeAnalysis.VisualBasic.Workspaces.dll",
    ]

    for dll in vb_dlls:
        dll_path = LS_DIR / dll
        if not dll_path.exists():
            issues.append(f"Missing VB.NET assembly: {dll}")

    return issues


def verify_installation() -> List[str]:
    """Verify full installation including Serena patching"""
    # First check language server files
    issues = verify_language_server_files()

    # Then check Serena ls_config.py patch (case-insensitive)
    try:
        serena_path = find_serena_installation()
        ls_config = (serena_path / "ls_config.py").read_text().lower()
        if "vbnet" not in ls_config:
            issues.append("solidlsp/ls_config.py not patched with VB.NET support")
    except Exception as e:
        issues.append(f"Cannot verify ls_config.py patch: {e}")

    # Check serena_config.py patch (Language enum, case-insensitive)
    # Note: In some versions of Serena, Language enum is imported from ls_config.py
    # so we only fail if Language is defined locally and not patched
    try:
        serena_config_path = find_serena_config_path()
        serena_config = serena_config_path.read_text()
        serena_config_lower = serena_config.lower()

        # Check if Language is imported from solidlsp (then we don't need to patch here)
        language_imported = "from solidlsp" in serena_config and "language" in serena_config_lower

        if "vbnet" not in serena_config_lower and not language_imported:
            issues.append("serena/config/serena_config.py not patched - Language enum missing vbnet")
    except Exception as e:
        issues.append(f"Cannot verify serena_config.py patch: {e}")

    return issues


def update_language_server():
    """Update language server to latest version"""
    print("Checking for updates...")
    # For now, just reinstall
    install_language_server(force=True)


def uninstall_language_server():
    """Remove language server"""
    if not LS_DIR.exists():
        print("Language server not installed")
        return

    shutil.rmtree(LS_DIR)
    print(f"Removed {LS_DIR}")


def get_installation_info() -> Dict[str, Any]:
    """Get installation information"""
    info = {
        "plugin_version": __version__,
        "ls_path": str(LS_DIR),
        "ls_status": "Installed" if LS_DIR.exists() else "Not installed",
        "serena_patched": False,
        "ls_assemblies": [],
    }

    # Check for assemblies
    if LS_DIR.exists():
        vb_dlls = [
            "Microsoft.CodeAnalysis.VisualBasic.dll",
            "Microsoft.CodeAnalysis.VisualBasic.Features.dll",
            "Microsoft.CodeAnalysis.VisualBasic.Workspaces.dll",
        ]
        info["ls_assemblies"] = [dll for dll in vb_dlls if (LS_DIR / dll).exists()]

    # Check Serena patch (case-insensitive)
    try:
        serena_path = find_serena_installation()
        ls_config = (serena_path / "ls_config.py").read_text().lower()
        serena_config_path = find_serena_config_path()
        serena_config = serena_config_path.read_text().lower()
        info["serena_patched"] = "vbnet" in ls_config and "vbnet" in serena_config
    except:
        pass

    return info
