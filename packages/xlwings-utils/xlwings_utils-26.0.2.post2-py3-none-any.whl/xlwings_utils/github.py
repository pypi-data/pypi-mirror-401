import os
import requests
from pathlib import Path
import importlib
import sys
import base64
from urllib.parse import unquote


missing = object()

_token = missing
_owner = None
_initialized = False


def init(owner=missing, token=missing):
    """
    This function may to be called prior to using any github function
    to specify the owner and token.

    Parameters
    ----------
    owner : str
        owner (optional)

        if omitted: try to get environment variable GITHUB.OWNER

    token : str
        token

        if omitted: try to get the environment variable GITHUB.TOKEN


    Returns
    -------
    None
    """

    global _token
    global _owner
    global _initialized
    global _headers

    try:
        import pyodide_http

        pyodide_http.patch_all()  # required to reliably use requests on pyodide platforms

    except ImportError:
        ...
    _initialized = True

    if owner is missing:
        if "GITHUB.OWNER" in os.environ:
            _owner = os.environ["GITHUB.OWNER"]

    if token is missing:
        if "GITHUB.TOKEN" in os.environ:
            _token = os.environ["GITHUB.TOKEN"]

    if _token is missing:
        _headers = {}
    else:
        _headers = {"Authorization": f"Bearer {_token}"}


def get_owner(owner):
    if owner is missing:
        if "GITHUB.OWNER" in os.environ:
            owner = os.environ["GITHUB.OWNER"]
        else:
            raise ValueError("no owner specified and no GITHUB.OWNER in environment variable")
    return owner

def _login():
    if not _initialized:
        init()  # use environment


def dir(path="", repo=missing, owner=missing, recursive=False, show_files=True, show_folders=False):
    """
    returns all github files/folders in path on owner/repo

    Parameters
    ----------
    path : str or Pathlib.Path
        path from which to list all files (default: '')

    repo : str
        repo to read from (not optional)

    owner : str
        if omitted, use the global owner

    recursive : bool
        if True, recursively list files and folders. if False (default) no recursion

    show_files : bool
        if True (default), show file entries
        if False, do not show file entries

    show_folders : bool
        if True, show folder entries
        if False (default), do not show folder entries

    Returns
    -------
    files : list

    Note
    ----
    It is necessary to call github.init() prior to any github function,
    particularly if owner and token are defined as environment variables.
    """
    _login()

    owner = get_owner(owner)
    if repo is None:
        raise ValueError("no repo specified")

    url = unquote(f"https://api.github.com/repos/{owner}/{repo}/contents/{path}")

    resp = requests.get(url, headers=_headers)
    files = resp.json()
    if not isinstance(files,list):
        raise ValueError("incorrect", files)
    result = []

    for f in files:
        if f["type"] == "file" and show_files:
            result.append(f"{path}/{f['name']}")
        if f["type"] == "dir":
            if show_folders:
                result.append(f"{path}/{f['name']}/")
            if recursive:
                result.extend(dir(repo=repo, path=f"{path}/{f['name']}", owner=owner, show_files=show_files, show_folders=show_folders, recursive=recursive))
    return result


def read(path, repo, owner=missing, cached=True):
    """
    read file from dropbox

    Parameters
    ----------
    path : str or Pathlib.Path
        path to read from

    cached : bool
        if True (default), result will be cached

        if False, read on each call

    Returns
    -------
    contents of the dropbox file : bytes

    Note
    ----
    If the file could not be read, an OSError will be raised.

    Note
    ----
    If DROPBOX.REFRESH_TOKEN, DROPBOX.APP_KEY and DROPBOX.APP_SECRET environment variables are specified,
    it is not necessary to call dropbox_init() prior to any dropbox function.
    """
    if cached:
        if path in read.cache:
            return read.cache[path]
    else:
        read.cache = {}
    _login()
    owner = get_owner(owner)

    file_url = unquote(f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref=main")
    data = requests.get(file_url).json()

    content = base64.b64decode(data["content"])
    return content


read.cache = {}


def get_repos(owner=missing):
    _login()
    owner = get_owner(owner)

    result = []
    page = 1

    while True:
        url = unquote(f"https://api.github.com/users/{owner}/repos?per_page=100&page={page}")
        response = requests.get(url).json()
        if not response:
            break
        result.extend(repo["name"] for repo in response)
        page += 1

    return result


def import_from_folder(folder_name, repo, owner=missing):
    """
    imports a module from a folder

    Parameters
    ----------
    folder_name: str or Path
        fully qualified name of the folder containing the module, e.g.

        /Python/istr/istr

    Returns
    -------
        link to module

    Note
    ----
    If the module is already imported, no action
    """
    _login()
    owner = get_owner(owner)

    folder_name_path = Path(folder_name)
    module_name = folder_name_path.parts[-1]
    if module_name in sys.modules:
        return sys.modules[module_name]

    my_packages = Path("/my_packages/")
    my_packages.mkdir(parents=True, exist_ok=True)

    for entry in dir(folder_name, repo=repo, owner=owner, recursive=True):
        entry_path = Path(entry)
        rel_path = entry_path.relative_to(folder_name_path)
        if "__pycache__" in str(rel_path):
            continue
        contents = read(str(entry_path).replace("\\", "/"), repo=repo, owner=owner)

        (my_packages / module_name).mkdir(parents=True, exist_ok=True)
        with open(my_packages / module_name / rel_path, "wb") as f:
            f.write(contents)

    if str(my_packages) not in sys.path:
        sys.path = [str(my_packages)] + sys.path
    return importlib.import_module(module_name)


if __name__ == "__main__":
    ...
