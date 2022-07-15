# --------------------------------------------------------------------------- #
#   Proofscape Manage                                                         #
#                                                                             #
#   Copyright (c) 2021-2022 Alpine Mathematics contributors                   #
#                                                                             #
#   Licensed under the Apache License, Version 2.0 (the "License");           #
#   you may not use this file except in compliance with the License.          #
#   You may obtain a copy of the License at                                   #
#                                                                             #
#       http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                             #
#   Unless required by applicable law or agreed to in writing, software       #
#   distributed under the License is distributed on an "AS IS" BASIS,         #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#   See the License for the specific language governing permissions and       #
#   limitations under the License.                                            #
# --------------------------------------------------------------------------- #

"""
High-level installation routines.

Sometimes installing a project involves several steps, beyond merely cloning a
single repo. For example, a Python project might depend on a library which
cannot currently be obtained from PyPI, since we require a development branch
which has not yet been released.

Other times the procedure is not complex, but does differ from merely cloning
a repo. For example, a Javascript library may need to be obtained from npm,
instead of cloning and building.

The functions defined here are meant to carry out the steps that may sometimes
be involved in installing a project, in such cases.
"""

import os

import click

from manage import cli, PFSC_ROOT

SRC_DIR = os.path.join(PFSC_ROOT, 'src')
STATIC_DIR = os.path.join(PFSC_ROOT, 'static')


@cli.group()
def install():
    """
    Utilities for installing projects.
    """
    pass


@install.command()
@click.option('--dry-run', is_flag=True, help="Do not actually install; just print installation commands.")
def server(dry_run):
    """
    Install the pfsc-server project.
    """
    script_lines = []

    server_dir = os.path.join(SRC_DIR, 'pfsc-server')
    if not os.path.exists(server_dir):
        script_lines.append('pfsc repo clone server')

    sympy_dir = os.path.join(SRC_DIR, 'sympy')
    if not os.path.exists(sympy_dir):
        script_lines.append('pfsc repo clone sympy')

    # FIXME:
    #  Can we activate a venv while executing code such as this? Is one already
    #  active? Does it need to be deactivated first?
    #venv_dir = os.path.join(server_dir, 'venv')
    #if not os.path.exists(venv_dir):
        #script_lines.append(f'cd {server_dir}; python -m venv venv')
    #script_lines.append(f'cd {server_dir}; . venv/bin/activate; pip install -e ../sympy')

    script = ' \\\n'.join(script_lines)
    print(script)
    if not dry_run:
        os.system(script)


@install.command()
@click.option('--dry-run', is_flag=True, help="Do not actually install; just print installation commands.")
def elkjs(dry_run):
    """
    Install the elkjs Javascript library.
    """
    script = f'cd {STATIC_DIR}; npm install @alpinemath/tmp-elk-fork@0.8.0'
    print(script)
    if not dry_run:
        os.system(script)
