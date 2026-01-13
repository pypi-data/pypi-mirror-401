import os
import pytest
from unittest.mock import patch, MagicMock
from devops_runner_python.discovery import get_workspace_paths, find_python_projects


@pytest.fixture(autouse=True)
def reset_workspace_paths_cache():
    """Reset the global _workspace_paths cache before each test."""
    import devops_runner_python.discovery as discovery
    discovery._workspace_paths = None
    discovery._projects = None
    yield
    discovery._workspace_paths = None
    discovery._projects = None


class TestGetWorkspacePaths:
    """Tests for get_workspace_paths function."""

    def test_no_root_pyproject_returns_empty_list(self, tmp_path):
        """When no root pyproject.toml exists, should return empty list."""
        with patch.dict(os.environ, {'MONOREPO_ROOT': str(tmp_path)}):
            result = get_workspace_paths()
        
        assert result == []

    def test_pyproject_without_workspace_members_returns_empty_list(self, tmp_path):
        """When pyproject.toml exists but has no workspace members, should return empty list."""
        pyproject_content = b"""
[project]
name = "test-project"
version = "0.1.0"
"""
        (tmp_path / "pyproject.toml").write_bytes(pyproject_content)
        
        with patch.dict(os.environ, {'MONOREPO_ROOT': str(tmp_path)}):
            result = get_workspace_paths()
        
        assert result == []

    def test_pyproject_with_empty_workspace_members_returns_empty_list(self, tmp_path):
        """When workspace members is empty array, should return empty list."""
        pyproject_content = b"""
[project]
name = "test-project"
version = "0.1.0"

[tool.uv.workspace]
members = []
"""
        (tmp_path / "pyproject.toml").write_bytes(pyproject_content)
        
        with patch.dict(os.environ, {'MONOREPO_ROOT': str(tmp_path)}):
            result = get_workspace_paths()
        
        assert result == []

    def test_pyproject_with_workspace_members_returns_matching_paths(self, tmp_path):
        """When workspace members match directories with pyproject.toml, should return those paths."""
        pyproject_content = b"""
[project]
name = "test-project"
version = "0.1.0"

[tool.uv.workspace]
members = ["packages/*", "apps/*"]
"""
        (tmp_path / "pyproject.toml").write_bytes(pyproject_content)
        
        # Create workspace directories with pyproject.toml files
        packages_dir = tmp_path / "packages"
        packages_dir.mkdir()
        
        pkg1_dir = packages_dir / "pkg1"
        pkg1_dir.mkdir()
        (pkg1_dir / "pyproject.toml").write_bytes(b'[project]\nname = "pkg1"')
        
        pkg2_dir = packages_dir / "pkg2"
        pkg2_dir.mkdir()
        (pkg2_dir / "pyproject.toml").write_bytes(b'[project]\nname = "pkg2"')
        
        apps_dir = tmp_path / "apps"
        apps_dir.mkdir()
        
        app1_dir = apps_dir / "app1"
        app1_dir.mkdir()
        (app1_dir / "pyproject.toml").write_bytes(b'[project]\nname = "app1"')
        
        with patch.dict(os.environ, {'MONOREPO_ROOT': str(tmp_path)}):
            result = get_workspace_paths()
        
        assert len(result) == 3
        assert str(pkg1_dir) in result
        assert str(pkg2_dir) in result
        assert str(app1_dir) in result

    def test_workspace_members_pattern_not_matching_returns_empty(self, tmp_path):
        """When workspace members pattern doesn't match any directories, should return empty."""
        pyproject_content = b"""
[project]
name = "test-project"
version = "0.1.0"

[tool.uv.workspace]
members = ["packages/*"]
"""
        (tmp_path / "pyproject.toml").write_bytes(pyproject_content)
        # Don't create any packages directory
        
        with patch.dict(os.environ, {'MONOREPO_ROOT': str(tmp_path)}):
            result = get_workspace_paths()
        
        assert result == []

    def test_caches_workspace_paths(self, tmp_path):
        """Should cache workspace paths after first call."""
        pyproject_content = b"""
[project]
name = "test-project"
version = "0.1.0"

[tool.uv.workspace]
members = ["packages/*"]
"""
        (tmp_path / "pyproject.toml").write_bytes(pyproject_content)
        
        packages_dir = tmp_path / "packages"
        packages_dir.mkdir()
        pkg_dir = packages_dir / "pkg1"
        pkg_dir.mkdir()
        (pkg_dir / "pyproject.toml").write_bytes(b'[project]\nname = "pkg1"')
        
        with patch.dict(os.environ, {'MONOREPO_ROOT': str(tmp_path)}):
            result1 = get_workspace_paths()
            # Modify the file system (this shouldn't affect cached result)
            pkg2_dir = packages_dir / "pkg2"
            pkg2_dir.mkdir()
            (pkg2_dir / "pyproject.toml").write_bytes(b'[project]\nname = "pkg2"')
            result2 = get_workspace_paths()
        
        # Both results should be the same due to caching
        assert result1 == result2
        assert len(result1) == 1


class TestFindPythonProjects:
    """Tests for find_python_projects function."""

    def test_finds_projects_from_workspace_members(self, tmp_path):
        """Should find Python projects from workspace members."""
        pyproject_content = b"""
[project]
name = "test-project"
version = "0.1.0"

[tool.uv.workspace]
members = ["packages/*"]
"""
        (tmp_path / "pyproject.toml").write_bytes(pyproject_content)
        
        packages_dir = tmp_path / "packages"
        packages_dir.mkdir()
        
        pkg_dir = packages_dir / "my-package"
        pkg_dir.mkdir()
        pkg_pyproject = b"""
[project]
name = "my-package"
version = "0.1.0"

[tool.devops.scripts]
test = "pytest"

[tool.devops.deployment]
service_name = "my-service"
port = 8080
"""
        (pkg_dir / "pyproject.toml").write_bytes(pkg_pyproject)
        
        with patch.dict(os.environ, {'MONOREPO_ROOT': str(tmp_path)}):
            with patch('builtins.print'):  # Suppress discovery message
                result = find_python_projects()
        
        assert "my-package" in result
        assert result["my-package"].path == str(pkg_dir)
        assert result["my-package"].scripts == {"test": "pytest"}
        assert result["my-package"].deployment == {"service_name": "my-service", "port": 8080}

    def test_does_not_find_projects_in_node_modules(self, tmp_path):
        """Should NOT find projects in node_modules directories."""
        pyproject_content = b"""
[project]
name = "test-project"
version = "0.1.0"

[tool.uv.workspace]
members = ["packages/*"]
"""
        (tmp_path / "pyproject.toml").write_bytes(pyproject_content)
        
        packages_dir = tmp_path / "packages"
        packages_dir.mkdir()
        
        # Create a legitimate package
        pkg_dir = packages_dir / "real-package"
        pkg_dir.mkdir()
        (pkg_dir / "pyproject.toml").write_bytes(b'[project]\nname = "real-package"')
        
        # Create a package inside node_modules (should be ignored by workspace pattern)
        node_modules_dir = tmp_path / "node_modules" / "some-pkg"
        node_modules_dir.mkdir(parents=True)
        (node_modules_dir / "pyproject.toml").write_bytes(b'[project]\nname = "node-pkg"')
        
        with patch.dict(os.environ, {'MONOREPO_ROOT': str(tmp_path)}):
            with patch('builtins.print'):
                result = find_python_projects()
        
        assert "real-package" in result
        assert "node-pkg" not in result
