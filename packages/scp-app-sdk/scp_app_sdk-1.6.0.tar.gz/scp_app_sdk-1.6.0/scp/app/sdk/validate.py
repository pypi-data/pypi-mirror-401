import json
import os
from pathlib import Path

import click

from marshmallow import ValidationError

from scp.app.sdk.manifest import check_manifest as m_check_manifest, decode_manifest, MANIFEST_FILE_NAME, InvalidManifestException
from scp.app.sdk.schema.ui_plugin import UiPluginsSchema

UI_PLUGINS_PATH = 'install/ui-plugins.json'

class InvalidAppException(Exception):
    pass


def check_manifest(dir):
    manifest_file = os.path.join(dir, MANIFEST_FILE_NAME)

    if not os.path.isfile(manifest_file):
        raise InvalidAppException(f"Manifest file not found at {manifest_file}")

    try:
        manifest = decode_manifest(manifest_file)
        m_check_manifest(manifest)
    except InvalidManifestException as e:
        raise InvalidAppException(f"Invalid manifest: {e}")
    return manifest


def check_action(actions: dict, dir: str|Path) -> None:
    if not actions:
        return

    def _check_script(path: str) -> None:
        script_path = os.path.join(dir, path)
        if not os.path.exists(script_path):
            raise InvalidAppException(f'Missing script {script_path}')
        if not os.access(script_path, os.X_OK):
            raise InvalidAppException(f'This script is not executable {script_path}')
        with open(script_path,'rb') as script_file:
            script_content=script_file.read()
        if b'\r\n' in script_content:
            click.secho(f'⚠️ Windows line endings ("\\r\\n") detected in script file: {path} - replacing (with "\\n")', err=True, fg='yellow')
            with open(script_path,'wb') as script_file:
                script_file.write(script_content.replace(b'\r\n',b'\n'))

    def _check_json_schema(path: str) -> None:
        if not path:
            return # All good: schama is optional
        schema_path = os.path.join(dir, path)
        if not os.path.exists(schema_path):
            raise InvalidAppException(f'Missing json schema {schema_path}')
        with open(schema_path) as json_file:
            try:
                json.load(json_file)
            except json.decoder.JSONDecodeError as e:
                 raise InvalidAppException(f"Invalid json / schema: {path}\n{e}") from e

    def _check_json_schema_ui(path: str) -> None:
        if not path:
            return # All good: ui_schama is optional
        schema_path = os.path.join(dir, path)
        if not os.path.exists(schema_path):
            raise InvalidAppException(f'Missing json ui schema {schema_path}')
        with open(schema_path) as json_file:
            try:
                json.load(json_file)
            except json.decoder.JSONDecodeError as e:
                 raise InvalidAppException(f"Invalid json / ui schema: {path}\n{e}") from e

    # On install check
    on_install = actions.get('onInstall')
    if on_install:
        _check_script(on_install.get('script'))
        _check_json_schema(on_install.get('schema'))
        _check_json_schema_ui(on_install.get('ui_schema'))

    # On uninstall check
    on_uninstall = actions.get('onUninstall')
    if on_uninstall:
        _check_script(on_uninstall.get('script'))

    # On migrate check
    on_migrate = actions.get('onMigrate')
    if on_migrate:
        _check_script(on_migrate.get('script'))


def check_icon(icons, dir):
    if icons:
        for icon in icons:
            src = icon.get('src')
            icon_path = os.path.join(dir, src)
            if not os.path.exists(icon_path):
                raise InvalidAppException(f'Missing icon on path {icon_path}')


def check_ui_plugins(dir: Path) -> None:
    """
    Check if UI plugins file exists and is valid and schema is respected.
    :param dir: App directory
    """
    plugin_path = os.path.join(dir, UI_PLUGINS_PATH)
    schema = UiPluginsSchema(many=True)
    if os.path.exists(plugin_path):
        try:
            with open(plugin_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                schema.load(data)
        except json.JSONDecodeError:
            raise InvalidAppException(f'Invalid UI plugins JSON file: {plugin_path}')
        except ValidationError as e:
            raise InvalidAppException(
                f"UI plugins schema validation failed: {e.messages}"
            )

def validate_app(dir: Path) -> None:
    manifest = check_manifest(dir)
    check_action(manifest.get('actions'), dir)
    check_icon(manifest.get('icons'), dir)
    check_ui_plugins(dir)
