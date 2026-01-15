"""Function class for defining DataLab functions from Python callables."""

from __future__ import annotations

import inspect
import json
import shutil
import subprocess
import sys
import tempfile
import textwrap
from collections.abc import Callable
from pathlib import Path
from typing import Any, get_args, get_origin

from .gfhub import analyze_undefined_globals, validate_imports, validate_signature

__all__ = ["Function"]


def _is_stdlib(pkg: str) -> bool:
    """Check if a package name is a Python standard library module."""
    # Extract base package name (e.g., "json" from "json>=1.0")
    base_name = (
        pkg.split("[")[0].split(">")[0].split("<")[0].split("=")[0].split("!")[0]
    )
    return base_name in sys.stdlib_module_names


class Function:
    """A DataLab function defined from a Python callable.

    This class wraps a Python function and its dependencies, validates that
    all undefined globals are covered by the provided imports, and generates
    a uv-style script for upload to DataLab.

    Args:
        func: A Python function to upload. Must have a valid signature with
            positional-only input parameters and keyword-only config parameters:
            `def func(input1: Path, input2: Path, /, *, param: float = 1.0) -> dict`
        dependencies: A dict mapping package specs to import statement(s).
            The package spec can include version constraints (e.g., "pandas>=2.0").
            The import statement(s) define what names become available.

    Raises:
        ValueError: If the dependencies don't cover all undefined globals used
            in the function body.

    Examples:
        ```python
        def analyze(input_path: Path, /, *, threshold: float = 0.5) -> dict:
            df = pd.read_parquet(input_path)
            result = df[df["value"] > threshold]
            output = input_path.with_suffix(".filtered.parquet")
            result.to_parquet(output)
            return {"output": output}

        func = Function(
            analyze,
            dependencies={"pandas>=2.0": "import pandas as pd"},
        )

        client.add_function("filter_data", func)
        ```
    """

    def __init__(
        self,
        func: Callable,
        dependencies: dict[str, str | list[str]] | None = None,
    ) -> None:
        """Initialize a Function from a callable.

        Args:
            func: The Python function to wrap.
            dependencies: Dict mapping package specs to import statement(s).
        """
        self._func = func
        self._func_name = func.__name__

        # Get and dedent source code
        self._source = textwrap.dedent(inspect.getsource(func))

        # Normalize dependencies to dict[str, list[str]]
        if dependencies is None:
            dependencies = {}
        self._dependencies: dict[str, list[str]] = {}
        for pkg, imports in dependencies.items():
            if isinstance(imports, str):
                self._dependencies[pkg] = [imports]
            else:
                self._dependencies[pkg] = list(imports)

        # Analyze and validate
        self._validate()

    def _validate(self) -> None:
        """Validate the function signature and dependencies.

        Raises:
            ValueError: If the function signature is invalid or if any
                undefined global is not covered by imports.
        """
        # Get source with function renamed to main for signature validation
        source_as_main = self._source
        if self._func_name != "main":
            source_as_main = self._source.replace(
                f"def {self._func_name}(", "def main(", 1
            )

        # Validate function signature
        sig_result = json.loads(validate_signature(source_as_main))
        if not sig_result["is_valid"]:
            errors = sig_result["errors"]
            msg = f"Invalid function signature: {'; '.join(errors)}"
            raise ValueError(msg)

        # Analyze undefined globals
        analysis_result = json.loads(
            analyze_undefined_globals(self._source, self._func_name)
        )
        self._undefined_globals = set(analysis_result["undefined_globals"])

        # Validate that dependencies cover all undefined globals
        if self._undefined_globals:
            validation_result = json.loads(
                validate_imports(
                    json.dumps(list(self._undefined_globals)),
                    json.dumps(self._dependencies),
                )
            )
            if not validation_result["is_valid"]:
                missing = validation_result["missing"]
                msg = (
                    "The following names are used but not covered by imports: "
                    f"{missing}. Please add them to the dependencies parameter."
                )
                raise ValueError(msg)

    def to_script(self) -> str:
        """Generate a uv-style Python script.

        Returns:
            A string containing the complete uv script with dependency
            metadata, imports, and the function definition.
        """
        # Build import statements
        all_imports = []
        for imports in self._dependencies.values():
            all_imports.extend(imports)

        # Extract package specs for uv dependency list (exclude stdlib)
        pkg_specs = [pkg for pkg in self._dependencies if not _is_stdlib(pkg)]

        # Generate uv script
        script_lines = [
            "# /// script",
            "# dependencies = [",
        ]
        script_lines.extend([f'#   "{pkg}",' for pkg in pkg_specs])
        script_lines.append("# ]")
        script_lines.append("# ///")
        script_lines.append("")

        # Make annotations lazy so type hints don't need runtime imports
        script_lines.append("from __future__ import annotations")
        script_lines.append("")

        # Add imports
        script_lines.append("from pathlib import Path")
        if "matplotlib" in self._dependencies:
            script_lines.append("import os")
            script_lines.append("os.environ['MPLBACKEND'] = 'Agg'")
        script_lines.extend(all_imports)
        script_lines.append("")

        # Add the function source, renaming to main if needed
        source = self._source
        if self._func_name != "main":
            source = source.replace(f"def {self._func_name}(", "def main(", 1)
        script_lines.append(source)

        return "\n".join(script_lines)

    @property
    def func(self) -> Callable:
        """The wrapped Python function."""
        return self._func

    @property
    def name(self) -> str:
        """The function name."""
        return self._func_name

    @property
    def dependencies(self) -> dict[str, list[str]]:
        """The normalized dependencies dict."""
        return self._dependencies

    @property
    def undefined_globals(self) -> set[str]:
        """The set of undefined globals found in the function."""
        return self._undefined_globals

    def eval(self, *inputs: Any, **kwargs: Any) -> dict[str, Any]:
        """Evaluate the function locally using uv run.

        This runs the function in a subprocess with `uv run --script`, which
        will automatically install the required dependencies. The execution
        mirrors how the backend runs functions.

        Args:
            *inputs: Positional inputs to pass to the function. Path objects
                will be resolved to absolute paths. Other types (int, float,
                str, dict, list) are passed as-is.
            **kwargs: Keyword parameters to pass to the function.

        Returns:
            A dictionary mapping output names to output values. Path strings
            in the output are converted back to Path objects.

        Raises:
            RuntimeError: If the function execution fails.

        Examples:
            ```python
            func = Function(analyze, dependencies={"pandas": "import pandas as pd"})
            result = func.eval(Path("input.parquet"), threshold=0.5)
            print(result)
            # {"output": Path("/tmp/.../output.parquet")}
            ```
        """
        input_json = json.dumps(_serialize_inputs(inputs))
        kwargs_json = json.dumps(kwargs)

        # Write script and run
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            script_path = tmpdir_path / "script.py"
            output_path = tmpdir_path / "output.json"

            # Generate script with injected inputs/kwargs
            script = self._create_eval_script(
                output_file=str(output_path),
                input_json=input_json,
                kwargs_json=kwargs_json,
            )
            script_path.write_text(script)

            # Run with uv run --script
            uv = shutil.which("uv")
            if uv is None:
                msg = "Failed to execute function: uv executable not found."
                raise FileNotFoundError(msg)
            uv = str(Path(uv).resolve())
            result = subprocess.run(  # noqa: S603
                [uv, "run", "--script", str(script_path)],
                capture_output=True,
                text=True,
                check=True,
            )

            # Read result from output file
            if not output_path.exists():
                msg = (
                    f"Function did not produce output.\n"
                    f"stdout:\n{result.stdout}\n"
                    f"stderr:\n{result.stderr}"
                )
                raise RuntimeError(msg)

            output = json.loads(output_path.read_text())

            return_annot = inspect.signature(self._func).return_annotation
            if return_annot is Path:
                output["output"] = Path(output['output']).resolve()
            elif get_origin(return_annot) is tuple:
                outs = list(output["output"])
                args = get_args(return_annot)
                for i, (out, arg) in enumerate(zip(outs, args, strict=True)):
                    if arg is Path:
                        outs[i] = Path(out).resolve()
                output["output"] = tuple(outs)
            return output

    def _create_eval_script(
        self,
        output_file: str,
        input_json: str,
        kwargs_json: str,
    ) -> str:
        """Create a wrapper script that mirrors the backend's execution.

        This generates a script that:
        1. Defines the main function
        2. Parses injected JSON inputs/kwargs
        3. Converts types based on function signature (Path, list[Path], etc.)
        4. Calls main() and captures the result
        5. Writes result as {"success": bool, "output": ...} JSON
        """
        base_script = self.to_script()

        # Wrapper that mirrors backend's create_wrapper_script
        wrapper = f"""

if __name__ == '__main__':
    import json
    from pathlib import Path
    import inspect
    import traceback
    from typing import get_args, get_origin, get_type_hints

    def convert_to_type(value, annotation):
        '''Convert JSON value to the expected type based on annotation.'''
        # Handle string annotations (from __future__ import annotations)
        if isinstance(annotation, str):
            if annotation == "Path" or annotation == "pathlib.Path":
                if isinstance(value, str):
                    return Path(value)
                return value
            if annotation.lower().startswith("list[path]"):
                if isinstance(value, list):
                    return [Path(item).resolve() if isinstance(item, str) else item
                            for item in value]
                return value
            # Unknown string annotation, return unchanged
            return value

        # Handle Path type
        if annotation is Path or annotation == Path:
            if isinstance(value, str):
                return Path(value)
            return value

        # Handle list[Path] and similar generic types
        origin = get_origin(annotation)
        if origin is list:
            args = get_args(annotation)
            if args and (args[0] is Path or args[0] == Path):
                # Convert list of strings to list of Paths
                if isinstance(value, list):
                    return [Path(item).resolve() if isinstance(item, str) else item
                            for item in value]

        # Return unchanged if no conversion needed
        return value

    try:
        # Call the main function with input
        inputs = json.loads('''{input_json}''')
        kwargs = json.loads('''{kwargs_json}''')

        # Get the signature of the main function
        sig = inspect.signature(main)
        params = list(sig.parameters.values())

        # Convert inputs based on function signature type annotations
        if isinstance(inputs, list):
            converted_inputs = []
            for i, (inp, param) in enumerate(zip(inputs, params)):
                if param.annotation != inspect.Parameter.empty:
                    converted_inputs.append(convert_to_type(inp, param.annotation))
                else:
                    converted_inputs.append(inp)
            result = main(*converted_inputs, **kwargs)
        else:
            # Single input - convert if needed
            if params and params[0].annotation != inspect.Parameter.empty:
                result = main(convert_to_type(inputs, params[0].annotation), **kwargs)
            else:
                result = main(inputs, **kwargs)

        # Convert Path objects in result to strings for JSON serialization
        def path_to_str(obj):
            if isinstance(obj, Path):
                return str(obj.resolve())
            elif isinstance(obj, dict):
                return {{k: path_to_str(v) for k, v in obj.items()}}
            elif isinstance(obj, (list, tuple)):
                return [path_to_str(item) for item in obj]
            return obj

        result = path_to_str(result)

        # Store the result as JSON with success flag
        with open('{output_file}', 'w') as f:
            json.dump({{"success": True, "output": result}}, f, indent=2)

    except Exception as e:
        # Capture the full traceback
        error_msg = (
            str(type(e).__name__) + ": " + str(e) + "\\n" + traceback.format_exc()
        )
        print("Error during function execution:", error_msg)

        # Store the error as JSON with success flag
        with open('{output_file}', 'w') as f:
            json.dump({{"success": False, "output": error_msg}}, f, indent=2)
"""
        return base_script + wrapper

    def __repr__(self) -> str:
        deps = list(self._dependencies.keys())
        return f"Function({self._func_name!r}, dependencies={deps!r})"

    def __str__(self) -> str:
        return self.to_script()


def _serialize_inputs(inputs: Any) -> Any:
    if isinstance(inputs, Path):
        return str(inputs.resolve())
    if isinstance(inputs, dict):
        return {k: _serialize_inputs(v) for k, v in inputs.items()}
    if isinstance(inputs, list):
        return [_serialize_inputs(x) for x in inputs]
    if isinstance(inputs, tuple):
        return tuple(_serialize_inputs(x) for x in inputs)
    if isinstance(inputs, set):
        return {_serialize_inputs(x) for x in inputs}
    return inputs
