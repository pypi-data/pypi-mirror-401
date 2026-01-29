# SCP APP SDK

[![Coverage](https://code.internal.destiny.be/escaux/scp/csfe/dev/scp-app-sdk/badges/develop/coverage.svg)](https://code.internal.destiny.be/escaux/scp/csfe/dev/scp-app-sdk/-/graphs/develop/charts)

Software Development Kit for the SCP APP store. It provides schemas, functions, documentation and the CLI for the APP store.

You can find more documentation here: https://doc.chefhub.smartflowagent.net

## Install SCP-APP SDK via pipx

### install pipx
```
# debian/ubuntu
sudo apt install pipx # debian/ubuntu

# arch linux
sudo pacman -S python-pipx

# fedora
sudo dnf install python3-pipx

# alpine
sudo apk add py3-pipx

# macos
brew install pipx
pipx ensurepath

# windows
python -m pip install --user pipx
python -m pipx ensurepath
```

### Install the package
```
pipx install scp.app.sdk
```

## Use the scp-app cli tool

### Discover the scp-app cli tool
When the package is installed, just type 'scp-app' to get the help menu of the CLI.

```
Usage: scp-app [OPTIONS] COMMAND [ARGS]...

  🚀 SCP APP CLI – Your assistant to create, build, test, and publish SCP Apps.

  Configure SCP APP CLI:
      scp-app configure               → Configure default value to use.

  Typical workflow:
      scp-app create                  → Start a new SCP App project.
      scp-app validate                → Verify your app meets SCP standards.
      scp-app run                     → Run your app locally for testing.
      scp-app build /your/app/dir     → Compile & bundle your app.
      scp-app publish /dir/app.sap    → Release your app to the SCP store.

  Get help:
      scp-app create help             → Get help on creating an app.
      scp-app validate help           → Get help on validating an app.
      scp-app build help              → Get help on building an app.
      scp-app run help                → Get help on running an app.
      scp-app publish help            → Get help on publishing an app.

  For more information, you can refer to the documentation at:
  👉 https://doc.chefhub.smartflowagent.net/apps/cli

Options:
  --help  Show this message and exit.

Commands:
  build      Build the SCP APP
  configure  Interactive configuration for SCP App.
  create     Create a new SCP APP
  publish    Publish your SCP APP build
  run        Execute and run apt script
  validate   Check if the SCP APP is valid
```

### Configure the CLI 

##### Create your application
Follow the prompts from the tool in order to create your app.

```
scp-app create
```

Your app will be generated in your chosen directory.

##### Validate your application
You can check if your app structure is valid by using the validate command and the path of your app.

```
scp-app validate /tmp/test
```


### Run your application
You can check your app scripts are valid by using the run command.

```
# To run the install script
scp-app run install /tmp/test

# To run the uninstall script
scp-app run uninstall /tmp/test

# To run the migrate script
scp-app run migrate /tmp/test
```

##### Build your application
Once your application is validated and the scripts run without errors, you can create the build.

```
scp-app validate /tmp/test
```

It will build a '.sap' file in your app directory.
For example, for /tmp/test directory, it will be something like: /tmp/test/build/test-0.1.0.sap

#### Exclude files from the build
When you create an app, an `.appignore` file is created in the root of your app. It works similarly to a `.gitignore` file.
The default comes with some commonly ignored files, but feel free to edit and customize it to your needs.

Example of `.appignore` file:
```
# Exclude all .log files
*.log
# Exclude the temp directory
temp/
# Include a specific file (always add those at the end)
!important.log
```

### Publish your application
Once your application is built into a .sap file, you can publish the build on the SCP Appstore.

```
scp-app publish /tmp/test/build/test-0.1.0.sap
```


### How to use the SDK in your scripts ? 
You can check in the configuration.py and the user.py to use the built-in function of the SDK.

Get the input of app config:

```
#!/usr/local/bin/python3
from scp.app.sdk.configuration import get_inputs

# Get input of app config
inputs = get_inputs()
print(f"Inputs={inputs}")
```

Use the userId:
```
# Get the userId 
from scp.app.sdk.scripts.user import get_user_id
x = get_user_id()
print(x)

```
note: the userId is the uepId, you can find it in SAM UI in the "ID" column in the users table.

Use the ISS:
```
# Get the ISS 
from scp.app.sdk.scripts.user import get_iss
x = get_iss()
print(x)
```