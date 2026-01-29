import os
import json
import requests
import shutil
import uuid
import yaml
import zipfile
import click
from pathlib import Path

import scp.app.sdk.template as template_pkg
from scp.app.sdk.manifest import decode_manifest, render_manifest, MANIFEST_FILE_NAME
from scp.app.sdk.version import app_version
from scp.app.sdk.appignore import load_appignore, should_include

class BuildAppException(Exception):
    pass


class AppPublishException(Exception):
    def __init__(self, message, status_code=None, response_body=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


def internal_env():
    return {
        "appVersion": app_version
    }


def render_app(source_dir, destination_dir, env=None):
    """
    Render the directory APP to a dedicated directory with only information need for the APP evaluated.
    :param source_dir: Source directory of the APP
    :param destination_dir: Destination of the APP
    :param env: environment name
    """
    os.makedirs(destination_dir, exist_ok=True)

    src_manifest_path = os.path.join(source_dir, MANIFEST_FILE_NAME)
    if not os.path.exists(src_manifest_path):  # fallback if not finding manifest
        template_manifest = Path(template_pkg.__file__).parent / "template" / MANIFEST_FILE_NAME
        if not template_manifest.exists():
            raise BuildAppException(f"No manifest found in project or template: {MANIFEST_FILE_NAME}")
        src_manifest_path = str(template_manifest)

    dst_manifest_path = os.path.join(destination_dir, MANIFEST_FILE_NAME)

    # Get environment information
    values_file = os.path.join(source_dir, f"values.{env}.yaml" if env else "values.yaml")
    values_file_exist = os.path.exists(values_file)
    if not env and not values_file_exist:
        # No manifest rendering, just skipping
        shutil.copy2(src_manifest_path, dst_manifest_path)
    else:
        if not values_file_exist and env:
            raise BuildAppException(f"No values file found: {values_file}")
        with open(values_file, "r") as file:
            values = yaml.safe_load(file)

        # Render manifest
        env = internal_env()
        env.update(values)
        with open(src_manifest_path, "r") as file:
            manifest_data = file.read()
        try:
            manifest = render_manifest(manifest_data, env)
        except Exception as e:
            shutil.rmtree(destination_dir)
            raise e
        with open(dst_manifest_path, "w") as file:
            file.write(manifest)

    # Load .appignore spec
    spec = load_appignore(Path(source_dir))

    cp_list = []
    excluded_files = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = Path(root) / file
            if should_include(file_path, spec, Path(source_dir)):
                rel_path = file_path.relative_to(source_dir).as_posix()
                cp_list.append(rel_path)
            else:
                rel_path = file_path.relative_to(source_dir).as_posix()
                project_path = Path(source_dir) / rel_path
                excluded_files.append(project_path)

    click.secho('Excluded files:', fg='red')
    for file in excluded_files:
        click.secho(file, fg='red')

    # Copy files with fallback to template
    template_dir = Path(template_pkg.__file__).parent / "template"

    click.secho('Included files:', fg='bright_green')
    for file in cp_list:
        src_file = os.path.join(source_dir, file)
        click.secho(src_file, fg='bright_green')
        if not os.path.exists(src_file):
            # fallback to template
            fallback_file = template_dir / file
            if fallback_file.exists():
                src_file = str(fallback_file)
            else:
                raise BuildAppException(f"File not found in project or template: {file}")
        dst_file = os.path.join(destination_dir, file)
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        shutil.copy2(src_file, dst_file)


def build_app(source_dir, destination_dir):
    """
    Build the app file from the rendered APP directory
    :param source_dir: Source directory of the rendered APP
    :param destination_dir: Directory where the APP file will be set
    """
    manifest = decode_manifest(os.path.join(source_dir, MANIFEST_FILE_NAME))
    app_file_name = f"{manifest.get('name').lower()}-{manifest.get('version').lower()}.sap"
    Path(destination_dir).mkdir(exist_ok=True)
    destination_file = os.path.join(destination_dir, app_file_name)

    # ZIP the app directory, excluding the output file itself
    with zipfile.ZipFile(destination_file, "w") as zip_file:
        for root, dirs, files in os.walk(source_dir, followlinks=False):
            for file in files:
                full_path = os.path.join(root, file)
                if full_path == destination_file:
                    continue
                if file.startswith("."):
                    continue
                arcname = os.path.relpath(full_path, source_dir)
                zip_file.write(full_path, arcname=arcname)

    return destination_file


def extract_app(source_file, destination_dir):
    extension = os.path.splitext(source_file)[1]
    if extension != '.sap':
        raise BuildAppException('You build should be a SCP APP Package (.sap)')

    Path(destination_dir).mkdir(exist_ok=True)

    if not zipfile.is_zipfile(source_file):
        raise BuildAppException('Invalid build format (sap file)')

    try:
        with zipfile.ZipFile(source_file, 'r') as zip_ref:
            for i in zip_ref.infolist():
                zip_ref.extract(i, destination_dir)
                extracted_path = os.path.join(destination_dir, i.filename)
                if os.path.isfile(extracted_path):
                    # Keep permission
                    os.chmod(extracted_path, i.external_attr >> 16)

    except zipfile.BadZipFile as e:
        raise BuildAppException(f'Error to extract the file ({source_file}): {e}')


def publish_build(build_path, remote_server, key=None):
    headers = {
        "Authorization": f"Bearer {key}" if key else "",
    }
    tmp_dir = f"/tmp/{str(uuid.uuid4())}"
    try:
        extract_app(build_path, tmp_dir)
        manifest = decode_manifest(os.path.join(tmp_dir, MANIFEST_FILE_NAME))
    except Exception as e:
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        raise AppPublishException(str(e))
    shutil.rmtree(tmp_dir)
    app_id = manifest.get('id')
    app_name = manifest.get('name')
    if not os.path.exists(build_path):
        raise AppPublishException(f'SCP APP file (.sap) not found {build_path}')

    # Create a new APP if it's exist in the SCP APP store
    try:
        response = requests.get(f'{remote_server}/api/v1/apps/{app_id}', headers=headers, verify=False)
    except requests.exceptions.RequestException as e:
        status = response.status_code if 'response' in locals() and response else 599
        raise AppPublishException(
            f"SCP APP store error {status}",
            status_code=status,
            response_body=response.text if status != 599 else json.dumps({"error": str(e)})
        )

    if response.status_code != 200:
        if response.status_code != 404:
            raise AppPublishException(
                f"SCP APP store error {response.status_code}",
                status_code=response.status_code,
                response_body=response.text
            )
            print(f"APP not found in the SCP APP store, creating a new one: {app_id}")

    # Publish the build
    with open(build_path, 'rb') as f:
        files = {'file': (os.path.basename(build_path), f, 'text/plain')}
        try:
            print(f'request: {remote_server}/api/v1/apps/{app_id}/builds')
            response = requests.post(f'{remote_server}/api/v1/apps/{app_id}/builds', files=files, headers=headers, verify=False)
        except requests.exceptions.RequestException as e:
            status = response.status_code if 'response' in locals() and response else 599
    
            raise AppCreationException(
                f"SCP APP store error {status}",
                status_code=status,
                response_body=response.text if status != 599 else json.dumps({"error": str(e)})
            )

    if response.status_code != 200:
        raise AppPublishException(
            f"SCP APP store error {response.status_code}",
            status_code=response.status_code,
            response_body=response.text
        )
