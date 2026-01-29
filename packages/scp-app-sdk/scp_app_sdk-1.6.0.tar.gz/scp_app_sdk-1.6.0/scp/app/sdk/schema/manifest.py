from marshmallow import Schema, fields, validate


class ActionOnInstall(Schema):
    schema = fields.String(
        required=False,
        metadata={
            "description": "Path to the json schema in the zip file",
            "example": "install/schema.json",
        },
    )
    ui_schema = fields.String(
        required=False,
        metadata={
            "description": "Path to the json ui schema in the zip file",
            "example": "install/ui-schema.json",
        },
    )
    script = fields.String(
        required=True,
        metadata={
            "description": "Path (relative path in the zip file) to the install script executed when the end user sets up the app.",
            "example": "install/install.py",
        },
    )


class ActionOnRemove(Schema):
    script = fields.String(
        required=True,
        metadata={
            "description": "Path (relative path in the zip file) to the uninstall script executed when the end user removes the app.",
            "example": "install/uninstall.py",
        },
    )


class ActionOnMigrate(Schema):
    script = fields.String(
        required=True,
        metadata={
            "description": "Path (relative path in the zip file) to the migration script executed when the end user migrates/upgrades the app.",
            "example": "install/migrate",
        },
    )


class Actions(Schema):
    onInstall = fields.Nested(
        ActionOnInstall,
        required=False,
        metadata={
            "description": "Action during the installation of the APP by the end user"
        },
    )
    onUninstall = fields.Nested(
        ActionOnRemove,
        required=False,
        metadata={
            "description": "Action during the uninstall of the APP by the end user"
        },
    )
    onMigrate = fields.Nested(
        ActionOnMigrate,
        required=False,
        metadata={
            "description": "Action during the migration of the APP by the end user"
        },
    )


class Author(Schema):
    name = fields.String(
        required=True, metadata={"description": "Author name", "example": "John Doe"}
    )
    email = fields.String(
        required=True,
        metadata={"description": "Author email", "example": "john.doe@dstny.com"},
    )


class Icon(Schema):
    src = fields.String(
        required=True,
        dump_default="images/icon.png",
        metadata={
            "description": "Icon path",
            "example": "images/icon.png",
        },
    )
    type = fields.String(
        required=True,
        validate=validate.OneOf(["image/png"]),
        metadata={
            "description": "Encoding type",
            "example": "image/png",
        },
    )


class CSFE(Schema):
    id = fields.String(
        required=True, metadata={"description": "CSFE ID", "example": "dstny"}
    )
    uri = fields.Url(
        required=True,
        metadata={
            "description": "URL to CSFE API",
            "example": "http://dstny.csfe:8980",
        },
    )


class UiPlugin(Schema):
    src = fields.String(
        required=True,
        metadata={
            "description": "Path to the UI plugin manifest file",
            "example": "ui/plugin-manifest.json",
        },
    )
    name = fields.String(
        required=True,
        metadata={
            "description": "Name of the UI plugin",
            "example": "my-awesome-plugin",
        },
    )


class Rollout(Schema):
    strategy = fields.String(
        load_default="none",
        validate=validate.OneOf(["all", "none"]),
        metadata={
            "description": "Rollout strategy for the APP",
            "example": "all",
        },
    )
    set_preferred_build = fields.Boolean(
        load_default=False,
        metadata={
            "description": "Use this build as the default during installation.",
            "example": True,
        },
    )


class Manifest(Schema):
    manifest_version = fields.String(
        required=True,
        validate=validate.Regexp(
            r"^\d+\.\d+\.\d+$", error="Invalid version format, must be X.Y.Z"
        ),
        metadata={
            "description": "Version of the manifest",
            "example": "1.0.0",
        },
    )
    id = fields.String(
        required=True,
        validate=validate.Length(max=100),
        metadata={
            "description": "The unique identifier of the APP. It will be given to you during the APP creation on the SCP APP store",
            "example": "e4c9f92e-93e2-4920-81d5-3925de1a8e90",
        },
    )
    name = fields.String(
        required=True,
        validate=validate.Length(max=255),
        metadata={
            "description": "The name of APP. It should be unique and match the APP name.",
            "example": "Dstny APP",
        },
    )

    description = fields.String(
        required=False,
        metadata={
            "description": "APP description",
            "example": "This is the first Dstny APP",
        },
    )
    version = fields.String(
        required=True,
        validate=validate.Length(max=255),
        metadata={
            "description": "APP version",
            "example": "1.0.0",
        },
    )
    authors = fields.List(
        fields.Nested(Author),
        required=True,
        metadata={"description": "List of authors"},
    )
    icons = fields.List(
        fields.Nested(Icon),
        metadata={"description": "List of icons"},
    )
    tags = fields.List(
        fields.String(
            required=True, metadata={"description": "Tag", "example": "dstny"}
        ),
        required=True,
        metadata={"description": "List of tags"},
    )
    csfe = fields.List(
        fields.Nested(CSFE),
        required=False,
        metadata={"description": "CSFE used for the APP"},
    )
    actions = fields.Nested(
        Actions,
        required=False,
        metadata={"description": "Action performed during the APP events"},
    )
    ui_plugins = fields.Nested(
        UiPlugin, metadata={"description": "File for the UI plugins"}, required=False
    )
    rollout = fields.Nested(
        Rollout,
        metadata={"description": "Rollout strategy for the APP"},
        load_default={},
    )
