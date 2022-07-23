# Proofscape Configuration

# Root Directory for Proofscape.
#
# Ordinarily `PFSC_ROOT` should be left as `None`, and the root dir will be
# inferred automatically. This is the case when this project (`pfsc-manage`)
# lives directly under the root. For example, if the root is `~/proofscape`,
# then this project should be in `~/proofscape/pfsc-manage`.
#
# If you put `pfsc-manage` in a different location relative to the root,
# then you need to provide the absolute path to the root dir here, like so:
# PFSC_ROOT = '/the/path/to/proofscape/'
#
# *** NOTE: Generally, when a config variable in this file defines a filesystem
# path, then it will be interpreted as relative to `PFSC_ROOT` unless it begins
# with a slash. ***
PFSC_ROOT = None

# Front End
#
# Set `SSL` to True to turn on SSL in the front end Nginx server.
# In this case make sure that `SSL_CERT` and `SSL_KEY` point to your certificate
# and key files, and that `SERVER_NAME` is a name included in the certificate.
#
# WARNING: This encrypts connections only to the Proofscape ISE itself; it does
# not encrypt connections to other services, such as databases, etc.
# So be careful if you are exposing those other services to the Internet! See
# the `..._HOST` settings in the next section below.
SSL = False
SSL_CERT = "deploy/.ssl/fullchain1.pem"
SSL_KEY = "deploy/.ssl/privkey1.pem"
SERVER_NAME = "localhost"
# Set a port number, to redirect HTTP traffic from this port to the MCA's
# main port, as set below in PFSC_ISE_MCA_PORT.
REDIRECT_HTTP_FROM = None
# Set ttl in seconds for the HTTP String-Transport-Security header. Leave None
# if you don't want to send it.
HSTS_SECONDS = None
# To activate basic auth in the front end Nginx server, set a non-empty string
# as the value of `AUTH_BASIC_PASSWORD`. You can also set the title and username
# as you wish.
AUTH_BASIC_TITLE = "Testing Area"
AUTH_BASIC_USERNAME = "dev"
AUTH_BASIC_PASSWORD = None

# Twin Site
#
# In some MCA deployments you may want a "twin" or "companion" site, to be
# served alongside the PISE site, under a different host name. For example,
# some static pages (like docs or legal agreements) might be hosted here.
#
# A twin site can be configured in the Nginx front end by defining these
# variables. If you define TWIN_SERVER_NAME, be sure to also define SERVER_NAME
# above to be something different.
#
# The TWIN_ROOT_DIR is a filesystem path (may be absolute, or relative to
# PFSC_ROOT) pointing to the root directory of the html docs you want to serve
# for the twin site.
#
# Note that any SSL and/or Basic Auth settings made above will apply equally
# to the twin site.
TWIN_SERVER_NAME = None
TWIN_ROOT_DIR = None

# Email templates directory
#
# This variable has the same name as one of the pfsc-server config vars, but
# you should set it here, not directly in the env var classes at the bottom of
# this file, because it needs special treatment.
#
# For local deployment, you want to use this directory itself. However, for the
# MCA deployment we need to bind-mount this directory into the docker container,
# and set a corresponding value for the variable in docker.env, which will make
# sense inside the container.
EMAIL_TEMPLATE_DIR = None

# Host and Port Bindings for Various Services.
#
# This affects the visibility of these services only to your machine, or
# to others connected to it. When deployed with docker-compose, these services
# can always see each other within the docker network.
#
# If testing locally, keep `LOCAL_ONLY` as the host. If testing on a remote
# machine, you may need to change to `INADDR_ANY`.
#
# WARNING: If running on Ubuntu, use of `INADDR_ANY` as the host will
# completely circumvent the UFW firewall! See <https://askubuntu.com/q/652556>.
LOCAL_ONLY = '127.0.0.1'
INADDR_ANY = '0.0.0.0'
# The Proofscape ISE:
#  as MCA (multi-container app):
PFSC_ISE_MCA_HOST = LOCAL_ONLY
PFSC_ISE_MCA_PORT = 7371
#  as OCA (one-container app):
PFSC_ISE_OCA_HOST = LOCAL_ONLY
PFSC_ISE_OCA_PORT = 7372
# Redis:
REDIS_HOST = LOCAL_ONLY
REDIS_PORT = 6379
# RedisGraph:
#  as part of MCA (multi-container app):
REDISGRAPH_MCA_HOST = LOCAL_ONLY
REDISGRAPH_MCA_PORT = 6381
#  as part of OCA (one-container app):
REDISGRAPH_OCA_HOST = LOCAL_ONLY
REDISGRAPH_OCA_PORT = 6382
# RedisInsight:
REDISINSIGHT_HOST = LOCAL_ONLY
REDISINSIGHT_PORT = 6363
# Neo4j database:
NEO4J_BOLT_HOST = LOCAL_ONLY
NEO4J_BOLT_PORT = 7687
# Neo4j interactive web app:
NEO4J_BROWSE_HOST = LOCAL_ONLY
NEO4J_BROWSE_PORT = 7474
# TinkerGraph:
TINKERGRAPH_HOST = LOCAL_ONLY
TINKERGRAPH_PORT = 8182
# JanusGraph:
JANUSGRAPH_HOST = LOCAL_ONLY
JANUSGRAPH_PORT = 8183

# Docker Image Tags
#
# These are the default docker image tags that will be used, for various services:
REDIS_IMAGE_TAG = '6.2.1'
REDISGRAPH_IMAGE_TAG = '2.4.13'
REDISINSIGHT_IMAGE_TAG = '1.11.0'
NEO4J_IMAGE_TAG = '4.0.6'
GREMLIN_SERVER_IMAGE_TAG = '3.6.0'
JANUSGRAPH_IMAGE_TAG = '0.6.0'
NGINX_IMAGE_TAG = '1.22.0'

# Wheel Files
#
# During development, Pyodide and all required python packages running in the
# browser should be served locally (not over a CDN). We also want local copies
# for building the OCA docker image. For any package that would
# be loaded from a `.whl` file, the project repo should exist under PFSC_ROOT/src,
# and you should build the `.whl` file there (`$ python setup.py bdist_wheel`),
# so that it exists under that project's `dist` folder. The wheel file names
# contain version numbers, so need to be kept up to date. Make those settings here.
LOCAL_WHEELS = {
    # Format:
    #  key: repo name
    #  value: wheel filename
    "pfsc-util": "pfsc_util-0.22.7-py3-none-any.whl",
    "typeguard": "typeguard-2.13.3-py3-none-any.whl",
    "displaylang": "displaylang-0.22.7-py3-none-any.whl",
    "sympy": "alpinemath_sympy-0.10.3-py3-none-any.whl",
    "lark": "lark067-0.6.7-py2.py3-none-any.whl",
    "pfsc-examp": "pfsc_examp-0.22.7-py3-none-any.whl",
}
# If you want to generate a deployment that loads one or more wheels from a
# remote source, define those sources here. You can use a URL, or a line like
# `typeguard==2.13.3` that you would ordinarily pass to pip (to load from PyPI).
# If you define a remote wheel here, you do _not_ need to delete the corresponding
# local wheel definition above; it will be automatically overridden.
REMOTE_WHEELS = {
    "pfsc-util": None,
    "typeguard": None,
    "displaylang": None,
    "sympy": None,
    "lark": None,
    "pfsc-examp": None,
}
# By default, the remote wheels are only included in the docker.env configuration.
# To include them also in the local.env configuration, set this True:
USE_REMOTE_WHEELS_IN_LOCAL_ENV = False

# App URL Prefix
#
# The APP_URL_PREFIX supports different ways of deploying the Proofscape ISE.
# For example, if you wanted it to be found under
# https://example.org/tools/proofscape/ise, then you would set
# APP_URL_PREFIX = '/tools/proofscape/ise'
# On the other hand, you might prefer to use a subdomain and no prefix,
# as in https://pise.example.org. In that case you would leave
# the APP_URL_PREFIX as `None`.
APP_URL_PREFIX = None

# Docker Command
#
# In `DOCKER_CMD` we set the (basic) command name that is used for all Docker
# operations (such as `docker build`, `docker run`, etc.). Depending on your
# environment, you may need to substitute 'sudo docker' here.
DOCKER_CMD = 'docker'

##############################################################################
# Infrastructure-specific settings
#
# You can safely ignore any settings in this section, that do not apply to your
# specific use case.

# AWS Neptune
# Applies only if using AWS Neptune for your graph database.
# Optionally, set the first three segments of the Neptune URI here, e.g.:
#   "my-db-name.cluster-qwertyuiop.us-east-1"
# The system will then append ".neptune.amazonaws.com", and attach the protocol
# and path parts, to build the final URI for you.
# Alternatively, you can leave this `None` and just set the entire URI manually
# (starting with "wss://" and ending with "/gremlin") by defining your own
# GRAPHDB_URI variable in the DockerVars class below.
AWS_NEPTUNE_URI_PREFIX = None

##############################################################################
# Environment Variables
#
# This section defines several classes that you can use to control environment
# variables that will be set in the `local.env` and `docker.env` files generated
# by `pfsc deploy generate`.

class CommonVars:
    """
    Vars defined here will be added to both local.env and docker.env.
    """
    # Some config vars commonly used during development are listed below.
    # For the list of all vars, see `pfsc-server/config.py`.
    #PERSONAL_SERVER_MODE = 1
    #PFSC_TRUSTED_LIBPATHS = "gh.alpinemath"
    #USE_TRANSACTIONS = 1
    #BUILD_IN_GDB = 1

class LocalVars:
    """
    Vars defined here will be added only to local.env, and will override
    definitions in CommonVars.
    """
    # To test handling of "500's" (internal system errors) via unit tests,
    # uncomment these two lines. To test the same through the browser, do
    # likewise in `DockerVars`.
    #DEBUG = 0
    #PROPAGATE_EXCEPTIONS = 0

class DockerVars:
    """
    Vars defined here will be added only to docker.env, and will override
    definitions in CommonVars.
    """
    #DEBUG = 0
    #PROPAGATE_EXCEPTIONS = 0
