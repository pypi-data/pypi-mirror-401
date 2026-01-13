"""Parser for various project definition files."""

import json
import logging
import tomllib
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)


class ProjectFileParser:
    """Parse project definition files and extract dependency information."""

    SUPPORTED_FILES = {
        "pyproject.toml": "python",
        "requirements.txt": "python",
        "setup.py": "python",
        "package.json": "npm",
        "package-lock.json": "npm",
        "pom.xml": "maven",
        "build.gradle": "gradle",
        "build.gradle.kts": "gradle",
        "build.sbt": "sbt",
        "Cargo.toml": "rust",
        "go.mod": "go",
        "Gemfile": "ruby",
    }

    def discover_project_files(self, directory: Path) -> list[tuple[Path, str]]:
        """
        Discover project definition files in a directory.

        Args:
            directory: Path to scan

        Returns:
            List of tuples (file_path, file_type)
        """
        found_files = []

        for file_name, file_type in self.SUPPORTED_FILES.items():
            file_path = directory / file_name
            if file_path.exists():
                found_files.append((file_path, file_type))

        return found_files

    def parse_file(self, file_path: Path) -> dict[str, Any]:
        """
        Parse a project file and extract dependencies.

        Args:
            file_path: Path to the project file

        Returns:
            Dictionary with file type and dependencies
        """
        file_name = file_path.name

        if file_name not in self.SUPPORTED_FILES:
            raise ValueError(f"Unsupported file type: {file_name}")

        file_type = self.SUPPORTED_FILES[file_name]

        if file_name == "pyproject.toml":
            return self._parse_pyproject_toml(file_path)
        elif file_name == "requirements.txt":
            return self._parse_requirements_txt(file_path)
        elif file_name == "package.json":
            return self._parse_package_json(file_path)
        elif file_name == "pom.xml":
            return self._parse_pom_xml(file_path)
        elif file_name.startswith("build.gradle"):
            return self._parse_gradle(file_path)
        elif file_name == "build.sbt":
            return self._parse_sbt(file_path)
        elif file_name == "Cargo.toml":
            return self._parse_cargo_toml(file_path)
        elif file_name == "go.mod":
            return self._parse_go_mod(file_path)
        elif file_name == "Gemfile":
            return self._parse_gemfile(file_path)
        else:
            return {"file_type": file_type, "dependencies": {}, "dev_dependencies": {}}

    def _parse_pyproject_toml(self, file_path: Path) -> dict[str, Any]:
        """Parse pyproject.toml file."""
        with open(file_path, "rb") as f:
            data = tomllib.load(f)

        dependencies = {}
        dev_dependencies = {}

        # Standard dependencies
        if "project" in data and "dependencies" in data["project"]:
            for dep in data["project"]["dependencies"]:
                name, version = self._parse_python_requirement(dep)
                dependencies[name] = version

        # Optional dependencies
        if "project" in data and "optional-dependencies" in data["project"]:
            for group, deps in data["project"]["optional-dependencies"].items():
                for dep in deps:
                    name, version = self._parse_python_requirement(dep)
                    dev_dependencies[f"{name} ({group})"] = version

        return {
            "file_type": "python",
            "dependencies": dependencies,
            "dev_dependencies": dev_dependencies,
        }

    def _parse_requirements_txt(self, file_path: Path) -> dict[str, Any]:
        """Parse requirements.txt file."""
        dependencies = {}

        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    name, version = self._parse_python_requirement(line)
                    dependencies[name] = version

        return {"file_type": "python", "dependencies": dependencies, "dev_dependencies": {}}

    def _parse_package_json(self, file_path: Path) -> dict[str, Any]:
        """Parse package.json file."""
        with open(file_path, "r") as f:
            data = json.load(f)

        dependencies = data.get("dependencies", {})
        dev_dependencies = data.get("devDependencies", {})

        return {
            "file_type": "npm",
            "dependencies": dependencies,
            "dev_dependencies": dev_dependencies,
        }

    def _parse_pom_xml(self, file_path: Path) -> dict[str, Any]:
        """Parse Maven pom.xml file."""
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Handle XML namespaces
        namespace = {"mvn": "http://maven.apache.org/POM/4.0.0"}

        dependencies = {}
        dev_dependencies = {}

        for dep in root.findall(".//mvn:dependency", namespace):
            group_id = dep.find("mvn:groupId", namespace)
            artifact_id = dep.find("mvn:artifactId", namespace)
            version = dep.find("mvn:version", namespace)
            scope = dep.find("mvn:scope", namespace)

            if group_id is not None and artifact_id is not None:
                name = f"{group_id.text}:{artifact_id.text}"
                ver = version.text if version is not None else "unspecified"

                if scope is not None and scope.text in ["test", "provided"]:
                    dev_dependencies[name] = ver
                else:
                    dependencies[name] = ver

        return {
            "file_type": "maven",
            "dependencies": dependencies,
            "dev_dependencies": dev_dependencies,
        }

    def _parse_gradle(self, file_path: Path) -> dict[str, Any]:
        """Parse Gradle build file (basic parsing)."""
        # This is a simplified parser - full Gradle parsing would require more complex logic
        dependencies = {}
        dev_dependencies = {}

        with open(file_path, "r") as f:
            content = f.read()

        # Simple regex-based parsing for demonstration
        import re

        # Look for implementation, api, testImplementation, etc.
        dep_pattern = (
            r'(implementation|api|testImplementation|compileOnly)\s*[("\']\s*([^"\']+)\s*[")\']'
        )
        matches = re.findall(dep_pattern, content)

        for scope, dep in matches:
            if "test" in scope.lower():
                dev_dependencies[dep] = "unspecified"
            else:
                dependencies[dep] = "unspecified"

        return {
            "file_type": "gradle",
            "dependencies": dependencies,
            "dev_dependencies": dev_dependencies,
        }

    def _parse_sbt(self, file_path: Path) -> dict[str, Any]:
        """Parse Scala SBT build file."""
        dependencies = {}
        dev_dependencies = {}

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        import re

        # Pattern for single dependency: "org" % "artifact" % "version"
        # or "org" %% "artifact" % "version" (for Scala version specific)
        single_dep_pattern = r'"([^"]+)"\s*%%?\s*"([^"]+)"\s*%\s*"([^"]+)"(?:\s*%\s*(\w+))?'

        matches = re.findall(single_dep_pattern, content)

        for match in matches:
            org, artifact, version, scope = match
            # %% means Scala version specific, add _2.13 or similar suffix
            if "%%" in content:
                dep_name = f"{org}:{artifact}_scala"
            else:
                dep_name = f"{org}:{artifact}"

            # Check if it's a test dependency
            if scope and scope.lower() in ["test", "it"]:
                dev_dependencies[dep_name] = version
            else:
                dependencies[dep_name] = version

        return {
            "file_type": "sbt",
            "dependencies": dependencies,
            "dev_dependencies": dev_dependencies,
        }

    def _parse_cargo_toml(self, file_path: Path) -> dict[str, Any]:
        """Parse Rust Cargo.toml file."""
        with open(file_path, "rb") as f:
            data = tomllib.load(f)

        dependencies = data.get("dependencies", {})
        dev_dependencies = data.get("dev-dependencies", {})

        # Convert dict format to string versions
        def normalize_dep(dep):
            if isinstance(dep, dict):
                return dep.get("version", "unspecified")
            return str(dep)

        dependencies = {k: normalize_dep(v) for k, v in dependencies.items()}
        dev_dependencies = {k: normalize_dep(v) for k, v in dev_dependencies.items()}

        return {
            "file_type": "rust",
            "dependencies": dependencies,
            "dev_dependencies": dev_dependencies,
        }

    def _parse_go_mod(self, file_path: Path) -> dict[str, Any]:
        """Parse Go go.mod file."""
        dependencies = {}

        with open(file_path, "r") as f:
            in_require = False
            for line in f:
                line = line.strip()

                if line.startswith("require"):
                    in_require = True
                    if "(" in line:
                        continue
                    else:
                        # Single line require
                        parts = line.split()
                        if len(parts) >= 3:
                            dependencies[parts[1]] = parts[2]

                elif in_require:
                    if line == ")":
                        in_require = False
                    elif line:
                        parts = line.split()
                        if len(parts) >= 2:
                            dependencies[parts[0]] = parts[1]

        return {"file_type": "go", "dependencies": dependencies, "dev_dependencies": {}}

    def _parse_gemfile(self, file_path: Path) -> dict[str, Any]:
        """Parse Ruby Gemfile (basic parsing)."""
        dependencies = {}

        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("gem"):
                    # Simple parsing: gem 'name', 'version'
                    import re

                    match = re.search(
                        r"gem\s+['\"]([^'\"]+)['\"](?:\s*,\s*['\"]([^'\"]+)['\"])?", line
                    )
                    if match:
                        name = match.group(1)
                        version = match.group(2) if match.group(2) else "unspecified"
                        dependencies[name] = version

        return {"file_type": "ruby", "dependencies": dependencies, "dev_dependencies": {}}

    @staticmethod
    def _parse_python_requirement(req: str) -> tuple[str, str]:
        """
        Parse a Python requirement string.

        Args:
            req: Requirement string (e.g., 'package>=1.0.0')

        Returns:
            Tuple of (package_name, version_spec)
        """
        # Remove extras like package[extra]>=1.0.0
        if "[" in req:
            req = req.split("[")[0] + req.split("]")[1] if "]" in req else req.split("[")[0]

        # Common version specifiers
        for sep in ["==", ">=", "<=", "~=", ">", "<", "!="]:
            if sep in req:
                parts = req.split(sep)
                return parts[0].strip(), sep + parts[1].strip()

        return req.strip(), "any"
