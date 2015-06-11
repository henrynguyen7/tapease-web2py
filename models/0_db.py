import os
import json

from gluon.tools import Auth


conffile = os.path.join(request.folder, "private", "conf.json")
with open(conffile) as conf:
    configs = json.load(conf)

mysql_username, mysql_password, mysql_database, mysql_host, mysql_port = (
    configs.get("mysql").get('username'),
    configs.get("mysql").get('password'),
    configs.get("mysql").get('database'),
    configs.get("mysql").get('host'),
    configs.get("mysql").get('port'),
)

db = DAL('mysql://' + mysql_username + ':' + mysql_password + '@' + mysql_host + ':' + mysql_port + '/' + mysql_database, pool_size=3, check_reserved=['mysql'], migrate=True)


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

auth = Auth(db)

auth.settings.extra_fields['auth_user'] = [
    Field('name', 'string'),
    Field('image_url', 'string'),
    Field('is_enabled', 'boolean', default=True),
]

auth.define_tables()

db.auth_user.first_name.readable = db.auth_user.first_name.writable = False
db.auth_user.last_name.readable = db.auth_user.last_name.writable = False
db.auth_user.registration_id.readable = db.auth_user.registration_id.writable = False
db.auth_user.registration_key.readable = db.auth_user.registration_key.writable = False
db.auth_user.reset_password_key.readable = db.auth_user.reset_password_key.writable = False

db.define_table(
    'org',
    Field('name', 'string', required=True, notnull=True, unique=True, length=255),
    Field('url', 'string'),
    Field('image_url', 'string'),
    Field('created_on', 'datetime', default=request.now),
)

db.define_table(
    'membership',
    Field('user_id', 'reference auth_user'),
    Field('org_id', 'reference org'),
    Field('is_admin', 'boolean'),
)

db.define_table(
    'tap',
    Field('user_id', 'reference auth_user', required=True, notnull=True),
    Field('org_id', 'reference org', required=True, notnull=True),
    Field('page_uid', 'string'),
    Field('page_token', 'string'),
    Field('element_route', 'string', required=True, notnull=True),
    Field('element_node', 'string', required=True, notnull=True),
    Field('comment', 'string', required=True, notnull=True),
    Field('created_on', 'datetime', default=request.now),
)