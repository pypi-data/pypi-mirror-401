import click
import shutil

import ast
from typing import List

from .project_context import ProjectContext


class DependenciesManager:
    def __init__(self, ctx: ProjectContext, platform: str | None = None) -> None:
        self.dependencies_path = ctx.dependencies_path
        if platform:
            # During init - use provided platform
            from ...config import get_platform_dependencies_template
            self.dependencies_template = get_platform_dependencies_template(platform)
        else:
            # Existing project - read from context (which reads from toml)
            self.dependencies_template = ctx.dependencies_template

    def create(self):
        shutil.copy(self.dependencies_template, self.dependencies_path)
        click.echo(f"Created the dependecies file at {self.dependencies_path}")

    def read_user_dependencies(self) -> List[str] | None:
        """
        Read DEFAULT_DEPENDENCIES from the user's dependencies.py file.

        Args:
            file_path: Path to the dependencies.py file

        Returns:
            List of dependency strings

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If DEFAULT_DEPENDENCIES is not found or invalid
        """
        path = self.dependencies_path

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        # Read and parse the file
        with open(path, "r") as f:
            content = f.read()

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax in {path}: {e}")

        # Find DEFAULT_DEPENDENCIES
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if (
                        isinstance(target, ast.Name)
                        and target.id == "DEFAULT_DEPENDENCIES"
                    ):
                        # Handle BinOp (BASE_DEPENDENCIES + USER_DEPENDENCIES)
                        if isinstance(node.value, ast.BinOp):
                            # Need to evaluate the expression by importing the file
                            # This is safer than ast.literal_eval for our use case
                            import importlib.util
                            import sys

                            spec = importlib.util.spec_from_file_location("dependencies", path)
                            if spec and spec.loader:
                                module = importlib.util.module_from_spec(spec)
                                sys.modules["dependencies"] = module
                                spec.loader.exec_module(module)

                                if hasattr(module, "DEFAULT_DEPENDENCIES"):
                                    return module.DEFAULT_DEPENDENCIES
                                else:
                                    raise ValueError("DEFAULT_DEPENDENCIES not found after import")
                        # Handle List (direct list assignment)
                        elif isinstance(node.value, ast.List):
                            dependencies = []
                            for element in node.value.elts:
                                if isinstance(element, ast.Constant):
                                    dependencies.append(element.value)
                                else:
                                    print(
                                        "Warning: Skipping non-string element in DEFAULT_DEPENDENCIES"
                                    )
                            return dependencies
                        else:
                            raise ValueError("DEFAULT_DEPENDENCIES must be a list or expression")

        raise ValueError("DEFAULT_DEPENDENCIES not found in file")
