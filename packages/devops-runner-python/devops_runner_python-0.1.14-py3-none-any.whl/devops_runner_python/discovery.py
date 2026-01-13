import os
from glob import glob
import tomli
from typing import Dict, Any, List
from pydantic import BaseModel
from colorama import Fore, Style

class Project(BaseModel):
    name: str
    path: str
    scripts: Dict[str, str]
    deployment: dict[str, Any]

_projects: Dict[str, Project] | None = None
_workspace_paths: List[str] | None = None


def get_workspace_paths() -> List[str]:
    """
    Get workspace paths from root pyproject.toml's tool.uv.workspace.members.
    
    Returns:
        A list of absolute paths to workspace directories.
    """
    global _workspace_paths
    
    if _workspace_paths is not None:
        return _workspace_paths
    
    base_dir = os.getenv("MONOREPO_ROOT", os.getcwd())
    root_pyproject_path = os.path.join(base_dir, "pyproject.toml")
    
    if not os.path.exists(root_pyproject_path):
        _workspace_paths = []
        return _workspace_paths
    
    try:
        with open(root_pyproject_path, "rb") as f:
            root_pyproject = tomli.load(f)
        
        workspace_members: List[str] = (
            root_pyproject.get("tool", {})
            .get("uv", {})
            .get("workspace", {})
            .get("members", [])
        )
        
        # Glob each member pattern to find actual workspace directories
        workspace_dirs = []
        for member in workspace_members:
            pattern = os.path.join(base_dir, member, "pyproject.toml")
            pyproject_paths = glob(pattern)
            workspace_dirs.extend([os.path.dirname(p) for p in pyproject_paths])
        
        _workspace_paths = workspace_dirs
        return _workspace_paths
    except Exception as e:
        print(f"Error reading workspace members from {root_pyproject_path}: {e}")
        _workspace_paths = []
        return _workspace_paths


def find_python_projects() -> Dict[str, Project]:
    """
    Finds Python projects defined in workspace members from root pyproject.toml
    and creates a dictionary mapping project names to their paths and scripts.
    
    Returns:
        A dictionary mapping project names to tuples containing:
        - The directory path
        - A dictionary of script names to their entry points
    """
    global _projects

    if _projects is not None:
        return _projects

    base_dir = os.getenv("MONOREPO_ROOT", os.getcwd())
    workspace_dirs = get_workspace_paths()
    
    projects = {}
    
    for pyproject_dir in workspace_dirs:
        pyproject_path = os.path.join(pyproject_dir, "pyproject.toml")
        
        try:
            # Read and parse the pyproject.toml file
            with open(pyproject_path, "rb") as f:
                pyproject_data = tomli.load(f)
            
            # Extract the project name if it exists
            if "project" in pyproject_data and "name" in pyproject_data["project"]:
                project_name = pyproject_data["project"]["name"]
                
                # Extract scripts if they exist
                scripts = pyproject_data.get("tool", {}).get("devops", {}).get("scripts", {})

                # Extract deployment configuration if it exists
                deployment = pyproject_data.get("tool", {}).get("devops", {}).get("deployment", {})
                
                # Store the directory containing the pyproject.toml file and its scripts
                projects[project_name] = Project(
                    name=project_name, 
                    path=pyproject_dir, 
                    scripts=scripts,
                    deployment=deployment
                )
        except Exception as e:
            # Skip files that can't be parsed
            print(f"Error processing {pyproject_path}: {e}")
    
    print(f"{Fore.YELLOW}Workspace Discovery initialized in {base_dir}. Workspaces found: {', '.join(projects.keys())}{Style.RESET_ALL}")

    _projects = projects
    return projects


def get_port_for_service_name(service_name: str) -> int | None:
    """
    Returns the port for the given service name, or None if not found.
    Iterates the discovered projects and returns as soon as a match is found.
    """
    projects = find_python_projects()
    for project in projects.values():
        svc_name = project.deployment.get("service_name")
        if svc_name != service_name:
            continue
        port = project.deployment.get("port")
        if port is None:
            continue
        try:
            return int(port)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid port value for service {service_name}: {port}")
    return None
