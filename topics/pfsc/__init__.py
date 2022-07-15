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

import os

import click
import jinja2

import conf
from tools.util import squash
from tools.deploy import write_wheels_dot_env

this_dir = os.path.dirname(__file__)
templates_dir = os.path.join(this_dir, 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))


##############################################################################
# Components

def write_startup_system(
        dir_where_startup_system_lives,
        numbered_inis=None, tmp_dir_name=None):
    numbered_inis = numbered_inis or {}
    template = jinja_env.get_template(f'Dockerfile.startup_system')
    return template.render(
        dir_where_startup_system_lives=dir_where_startup_system_lives,
        numbered_inis=numbered_inis,
        tmp_dir_name=tmp_dir_name,
        ensure_dirs=True,
    )


def write_oca_eula_file(version):
    template = jinja_env.get_template('EULA.txt')
    return template.render(
        version=version,
    )


def write_pfsc_installation(
        python_cmd='python',
        ubuntu=True, demos=False, use_venv=False,
        oca_version_file=None, eula_file=None):
    template = jinja_env.get_template(f'Dockerfile.pfsc')
    return template.render(
        python_cmd=python_cmd,
        ubuntu=ubuntu,
        demos=demos,
        use_venv=use_venv,
        oca_version_file=oca_version_file,
        eula_file=eula_file,
    )


def write_oca_static_setup(tmp_dir_name, nginx=False):
    template = jinja_env.get_template('Dockerfile.oca_static')

    pyodide_files = """
    pyodide.js packages.json pyodide_py.tar pyodide.asm.wasm
    """.split()

    pyodide_names = """
    pyodide.asm distutils micropip pyparsing packaging
    Jinja2 MarkupSafe mpmath
    """.split()

    for name in pyodide_names:
        pyodide_files.extend([f'{name}.js', f'{name}.data'])

    return template.render(
        tmp_dir_name=tmp_dir_name,
        nginx=nginx,
        pyodide_files=pyodide_files,
        wheels=conf.LOCAL_WHEELS,
    )


def write_oca_final_setup(tmp_dir_name, final_workdir='/home/pfsc'):
    wheel_vars = {}
    write_wheels_dot_env(wheel_vars, for_local=True)
    template = jinja_env.get_template('Dockerfile.oca_final_setup')
    return template.render(
        tmp_dir_name=tmp_dir_name,
        final_workdir=final_workdir,
        wheel_vars=wheel_vars,
    )


def write_oca_nginx_conf():
    """
    Write an nginx.conf for use in the OCA. (Currently not used, but we keep
    this around for reference.)
    """
    from topics.nginx import write_nginx_conf
    return write_nginx_conf(
        listen_on='0.0.0.0:7372',
        app_url_prefix='', root_url='/',
        use_docker_ns=False,
        pfsc_web_hostname='localhost'
    )


def write_worker_and_web_supervisor_ini(worker=True, web=True, use_venv=True, oca=False):
    template = jinja_env.get_template('pfsc.ini')
    return template.render(
        use_venv=use_venv,
        worker=worker,
        web=web,
        oca=oca,
    )

##############################################################################
# Whole Dockerfiles

def write_single_service_dockerfile(demos=False):
    pfsc_install = write_pfsc_installation(
        ubuntu=True, demos=demos, use_venv=False
    )
    template = jinja_env.get_template('Dockerfile.single_service')
    df = template.render(
        pfsc_install=pfsc_install,
    )
    return squash(df)


def write_proofscape_oca_dockerfile(tmp_dir_name):
    pfsc_install = write_pfsc_installation(
        ubuntu=True, demos=True, use_venv=False,
        oca_version_file=f'{tmp_dir_name}/oca_version.txt',
        eula_file=f'{tmp_dir_name}/eula.txt',
    )
    startup_system = write_startup_system(
        '/home/pfsc', numbered_inis={
            100: 'redisgraph',
            200: 'pfsc',
        }, tmp_dir_name=tmp_dir_name
    )
    static_setup = write_oca_static_setup(
        tmp_dir_name, nginx=False
    )
    final_setup = write_oca_final_setup(
        tmp_dir_name, final_workdir='/home/pfsc'
    )
    template = jinja_env.get_template('Dockerfile.oca')
    df = template.render(
        redisgraph_image_tag=conf.REDISGRAPH_IMAGE_TAG,
        pfsc_install=pfsc_install,
        startup_system=startup_system,
        static_setup=static_setup,
        final_setup=final_setup,
    )
    return squash(df)


##############################################################################
def test01():
    import sys
    n = int(sys.argv[1])
    demos = bool(n & 1)
    vim = bool(n & 4)
    w3m = bool(n & 8)

    df = write_single_service_dockerfile(demos=demos, vim=vim, w3m=w3m)
    sys.stdout.write(df)
