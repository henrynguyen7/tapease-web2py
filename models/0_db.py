# -*- coding: utf-8 -*-

import json
import os

from gluon.tools import Auth


""" DB """

db = DAL('sqlite://tapease.db', migrate=True)


""" DB Definitions """

auth = Auth(db)

########################################################################
# Reference: valid web2py field types
# field type                default field validators
# string                    IS_LENGTH(length) default length is 512
# text                      IS_LENGTH(65536)
# blob                      None
# boolean                   None
# integer                   IS_INT_IN_RANGE(-1e100, 1e100)
# double                    IS_FLOAT_IN_RANGE(-1e100, 1e100)
# decimal(n,m)              IS_DECIMAL_IN_RANGE(-1e100, 1e100)
# date                      IS_DATE()
# time                      IS_TIME()
# datetime                  IS_DATETIME()
# password                  None
# upload                    None
# reference <table>         IS_IN_DB(db,table.field,format)
# list:string               None
# list:integer              None
# list:reference <table>    IS_IN_DB(db,table.field,format,multiple=True)
# json                      IS_JSON()
# bigint                    None
# big-id                    None
# big-reference             None
########################################################################

# Field(name, 'string', length=None, default=None,
#       required=False, requires='<default>',
#       ondelete='CASCADE', notnull=False, unique=False,
#       uploadfield=True, widget=None, label=None, comment=None,
#       writable=True, readable=True, update=None, authorize=None,
#       autodelete=False, represent=None, compute=None,
#       uploadfolder=os.path.join(request.folder,'uploads'),
#       uploadseparate=None,uploadfs=None)

db.define_table(
    'org',
    Field('name', 'string', required=True, notnull=True, unique=True),
    Field('created_on', 'datetime', default=request.now),
)

auth.settings.extra_fields['auth_user'] = [
    Field('org_id', 'reference org', required=True, notnull=True),
    Field('image_url', 'string'),
    Field('is_enabled', 'boolean', default=True),
    Field('is_admin', 'boolean', default=False),
]

auth.define_tables()

db.define_table(
    'tap',
    Field('user_id', 'reference auth_user', required=True, notnull=True),
    Field('org_id', 'reference org'),
    Field('page_token', 'string'),
    Field('page_uid', 'string', required=True, notnull=True),
    Field('element_route', 'string', required=True, notnull=True),
    Field('node', 'string', required=True, notnull=True),
    Field('comment', 'string', required=True, notnull=True),
    Field('created_on', 'datetime', default=request.now),
)