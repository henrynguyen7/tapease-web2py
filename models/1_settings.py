# -*- coding: utf-8 -*-

import logging

from gluon.tools import Crud, Service, PluginManager
from gluon.custom_import import track_changes


""" GENERAL """

# Basic web2py services
crud, service, plugins = Crud(db), Service(), PluginManager()

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

#  Reloads modules on every request... remove from production
if request.is_local:
    track_changes(True)


""" AUTH """
auth.settings.password_min_length = 8
auth.settings.create_user_groups = False


""" LOGGING """
logger = logging.getLogger(request.application)
logger.setLevel(logging.DEBUG)