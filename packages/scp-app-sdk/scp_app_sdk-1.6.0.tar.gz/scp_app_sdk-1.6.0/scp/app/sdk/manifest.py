import jinja2
import marshmallow
import os
import yaml
import pprint

from scp.app.sdk.schema.manifest import Manifest as ManifestSchema

MANIFEST_FILE_NAME = 'manifest.yaml'


class InvalidManifestException(Exception):
    pass


def decode_manifest(file=None, dir=None):
    """
    Decode the manifest file
    :param file: Path of the manifest file
    :param dir: APP directory (don't mention the file in that case)
    :return: Manifest content
    """
    if dir:
        file = os.path.join(dir, MANIFEST_FILE_NAME)

    if not os.path.exists(file):
        raise InvalidManifestException(f'Manifest not found on this path {file}')

    # Validate the structure of the manifest
    try:
        with open(file, 'r') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        # Extract detailed location info if available
        if hasattr(e, 'problem_mark') and e.problem_mark:
            mark = e.problem_mark
            message = f"Invalid YAML syntax at line {mark.line + 1}, column {mark.column + 1}: {e.problem}"
            # Try to show the line that caused the problem
            try:
                with open(file, 'r') as src:
                    lines = src.readlines()
                    bad_line = lines[mark.line].rstrip()
                    message += f"\n--> {mark.line + 1} | {bad_line}"
            except Exception:
                pass
            raise InvalidManifestException(message)
        else:
            raise InvalidManifestException(f"Invalid YAML file: {str(e)}")

    return data


def check_manifest(manifest):
    """
    Detect error in manifest.
    :param manifest: manifest content
    """
    try:
        return ManifestSchema().load(manifest)
    except marshmallow.ValidationError as e:
        formatted = _format_validation_errors(e.messages)
        raise InvalidManifestException(f"Some errors in the manifest:\n{formatted}")


def _format_validation_errors(errors, indent=2):
    """
    Recursively formats marshmallow validation errors into a readable string.
    Example output:
      • id → Not a valid string
      • metadata.name → Missing data for required field
    """
    lines = []

    def recurse(errs, prefix=""):
        if isinstance(errs, dict):
            for key, val in errs.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                recurse(val, new_prefix)
        elif isinstance(errs, list):
            for val in errs:
                if isinstance(val, (dict, list)):
                    recurse(val, prefix)
                else:
                    lines.append(f"{' ' * indent}• {prefix} → {val}")

    recurse(errors)
    return "\n".join(lines)


def is_valid_manifest(manifest) -> bool:
    try:
        check_manifest(manifest)
    except InvalidManifestException:
        return False
    return True


def app_manifest():
    """
    Loads the application manifest

    :return: manifest content
    """
    script_directory = os.environ.get('SCP_APP_BUILD_DIR')
    manifest_file = os.path.join(script_directory, MANIFEST_FILE_NAME)

    with open(manifest_file, 'r') as file:
        manifest = yaml.safe_load(file)

    return manifest


def render_manifest(manifest_template, env):
    """
    Render manifest template (Jinja2 template). Evaluate the manifest with the env variables.
    :param manifest_template: Manifest content in Jinja2 format
    :param env: Environment variables
    :return: Manifest evaluated
    """
    template = jinja2.Template(manifest_template)
    rendered_content = template.render(env)
    return rendered_content
