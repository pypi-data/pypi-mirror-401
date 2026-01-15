import os


def setup_phoenix():
    proxy_config_dict = {
        "timeout": 30,
        "launcher_entry": {
            # Option to disable launcher, e.g. for users that are not supposed to have editor available
            "enabled": False if os.environ.get("JSP_PHOENIX_LAUNCHER_DISABLED") else True,
            "icon_path": os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "icons/phoenix.svg",
            ),
            "title": "Arize Phoenix",
            "path_info": "phoenix",
            "category": "Notebook",
        },
        "new_browser_tab": True,
    }

    # if phoenix is already running and listening to TCP port
    jsp_phoenix_port = os.environ.get("JSP_PHOENIX_PORT", None)
    if jsp_phoenix_port:
        # set `command` be empty to avoid starting new phoenix server process and proxy requests to port specified
        proxy_config_dict.update({
            "command": [],
            "absolute_url": False,
            "port": int(jsp_phoenix_port),
        })
        return proxy_config_dict

    # set default working directory for phoenix
    working_directory = os.environ.get("PHOENIX_WORKING_DIR", None)
    if not working_directory:
        working_directory = os.environ.get("JUPYTERHUB_ROOT_DIR", os.environ.get("JUPYTER_SERVER_ROOT", os.environ.get("HOME")))

    # set phoenix port
    phoenix_port = os.environ.get("PHOENIX_PORT", "6006")

    # set full configuration to start new phoenix server process
    proxy_config_dict.update({
        "environment": {
            "PHOENIX_PORT": phoenix_port,
            "PHOENIX_GRPC_PORT": os.getenv("PHOENIX_GRPC_PORT", "4317"),
            "PHOENIX_HOST_ROOT_PATH": "/phoenix",
            "PHOENIX_TELEMETRY_ENABLED": "false",
        },
        "port": int(phoenix_port),
        "command": ["phoenix", "serve"],
    })
    return proxy_config_dict
