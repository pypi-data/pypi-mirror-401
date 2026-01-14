"""Functionality to install CodeServer."""

import os
import shutil
from importlib.resources import open_text

from pydantic import BaseModel
from rich.progress import Progress

from ou_container_builder.state import State
from ou_container_builder.util import docker_copy_cmd, docker_run_cmd

name = "code_server"


class Options(BaseModel):
    """Options for the CodeServer pack."""

    version: str = "4.103.0"
    extensions: list[str] = []


def init(state: State) -> None:
    """Initialise packs.code_server."""
    state.update(
        {
            "sources": {
                "apt": [
                    {
                        "name": "nodesource",
                        "key_url": "https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key",
                        "dearmor": True,
                        "deb": {
                            "url": "https://deb.nodesource.com/node_22.x",
                            "distribution": "nodistro",
                            "component": "main",
                        },
                    }
                ]
            },
            "packages": {"apt": {"deploy": ["nodejs", "yarn"]}},
            "web_apps": [
                {
                    "path": "code-server",
                    "options": {
                        "command": [
                            "code-server",
                            "--auth",
                            "none",
                            "--disable-update-check",
                            "--bind-addr",
                            "0.0.0.0",  # noqa: S104
                            "--port",
                            "{port}",
                        ],
                        "timeout": 60,
                        "new_browser_tab": False,
                        "launcher_entry": {
                            "title": "VS Code",
                            "icon_path": "/usr/share/ou/packs/code_server/vscode.svg",
                        },
                    },
                }
            ],
        }
    )


def generate(state: State, progress: Progress) -> None:  # noqa: ARG001
    """Generate the docker blocks to install Code Server."""
    if os.path.exists(os.path.join("ou-builder-build", "code_server")):
        shutil.rmtree(os.path.join("ou-builder-build", "code_server"))
    os.makedirs(os.path.join("ou-builder-build", "code_server"), exist_ok=True)
    with open(os.path.join("ou-builder-build", "code_server", "vscode.svg"), "w") as out_f:
        with open_text("ou_container_builder.packs.code_server", "vscode.svg") as in_f:
            out_f.write(in_f.read())
    version = state["packs"]["code_server"]["version"]
    state.update(
        {
            "output_blocks": {
                "build": [
                    {
                        "block": docker_run_cmd(
                            [
                                f"curl -L --output /tmp/code-server.tar.gz https://github.com/coder/code-server/releases/download/v{version}/code-server-{version}-linux-amd64.tar.gz",
                                "tar -zxf /tmp/code-server.tar.gz --directory /opt",
                            ]
                        ),
                        "weight": 1041,
                    },
                    {
                        "block": docker_run_cmd(
                            [f"ln -s /opt/code-server-{version}-linux-amd64/bin/code-server /usr/local/bin"]
                        ),
                        "weight": 1042,
                    },
                ],
                "deploy": [
                    {
                        "block": docker_copy_cmd(
                            f"/opt/code-server-{version}-linux-amd64",
                            f"/opt/code-server-{version}-linux-amd64",
                            from_stage="base",
                        ),
                        "weight": 1041,
                    },
                    {
                        "block": docker_copy_cmd(
                            os.path.join("ou-builder-build", "code_server", "vscode.svg"),
                            "/usr/share/ou/packs/code_server/vscode.svg",
                        ),
                        "weight": 1042,
                    },
                    {
                        "block": docker_run_cmd(
                            [f"ln -s /opt/code-server-{version}-linux-amd64/bin/code-server /usr/local/bin"]
                        ),
                        "weight": 1043,
                    },
                ],
            }
        }
    )
    if len(state["packs"]["code_server"]["extensions"]) > 0:
        if os.path.exists(os.path.join("ou-builder-build", "code-server")):
            shutil.rmtree(os.path.join("ou-builder-build", "code-server"))
        os.makedirs(os.path.join("ou-builder-build", "code-server", "startup"), exist_ok=True)
        with open(
            os.path.join("ou-builder-build", "code-server", "startup", "100-install-vscode-default-extensions"), "w"
        ) as out_f:
            out_f.write(
                """#!/bin/bash

if [ ! -d "$HOME/.local/share/code-server/extensions/" ]; then
    mkdir -p "$HOME/.local/share/code-server/extensions/"
    cp -r /usr/share/ou/code-server-extensions/* "$HOME/.local/share/code-server/extensions/"
fi

"""
            )
        state.update(
            {
                "output_blocks": {
                    "deploy": [
                        {
                            "block": docker_copy_cmd(
                                os.path.join("ou-builder-build", "code-server", "startup"), "/usr/share/ou/startup.d"
                            ),
                            "weight": 1044,
                        },
                    ]
                }
            }
        )
        for extension in state["packs"]["code_server"]["extensions"]:
            state.update(
                {
                    "output_blocks": {
                        "build": [
                            {
                                "block": docker_run_cmd(
                                    [
                                        "mkdir /usr/share/ou/code-server-extensions",
                                        "chown ou:users /usr/share/ou/code-server-extensions",
                                    ]
                                ),
                                "weight": 1043,
                            },
                            {"block": f"USER {state['image']['user']}", "weight": 1044},
                            {
                                "block": docker_run_cmd(
                                    [
                                        f"code-server --install-extension {extension} --extensions-dir /usr/share/ou/code-server-extensions",  # noqa:E501
                                    ]
                                ),
                                "weight": 1045,
                            },
                            {"block": "USER root", "weight": 1046},
                        ],
                        "deploy": [
                            {
                                "block": docker_copy_cmd(
                                    "/usr/share/ou/code-server-extensions",
                                    "/usr/share/ou/code-server-extensions",
                                    from_stage="base",
                                ),
                                "weight": 1045,
                            },
                        ],
                    }
                }
            )
