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
import jinja2

from tools.util import squash

this_dir = os.path.dirname(__file__)
templates_dir = os.path.join(this_dir, 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))

def write_nginx_conf(
        listen_on=80, server_name='localhost',
        ssl=False, basic_auth_title=None,
        static_redir=None, static_acao=False,
        redir_http=False, twin_server_name=None,
        hsts_seconds=None,
        **kwargs):
    # Define mapping {URL_path_extension: nginx_subdir}.
    # This means URLs pointing to
    #   {{app_url_prefix}}/ise/static{{path_ext}}
    # will be served from the directory
    #   /usr/share/nginx{{subdir}}
    # in the Nginx container.
    loc_map = {
        # Special subdirs of `static` are routed to special directories:
        '/PDFLibrary': '/PDFLibrary',
        '/pdfjs': '/pdfjs',
        '/whl': '/whl',
        '/pyodide': '/pyodide',
        '/css': '/css',
        '/img': '/img',
        # Everything else goes to the pfsc-ise directory:
        '': '/ise',
    }
    template = jinja_env.get_template('nginx.conf')
    return squash(template.render(
        listen_on=listen_on,
        redir_http=redir_http,
        twin_server_name=twin_server_name,
        hsts_seconds=hsts_seconds,
        server_name=server_name,
        ssl=ssl,
        basic_auth_title=basic_auth_title,
        static_redir=static_redir, static_acao=static_acao,
        loc_map=loc_map,
        **kwargs
    ))