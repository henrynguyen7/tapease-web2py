
response.view = 'generic.json'
response.headers['Content-Type'] = 'application/json'


@request.restful()
def tap():

    @auth.requires_login()
    def GET(*args, **vars):
        result = db(
            (db.tap.org_id==auth.user.org_id) &
            (db.tap.page_uid==vars.get('page_uid'))
        ).select()
        return dict(taps=result.as_list())

    @auth.requires_login()
    def POST(*args, **vars):
        result = db.tap.validate_and_insert(**vars)
        return result.as_dict()

    @auth.requires_login()
    def PUT(*args, **vars):
        result = db(db.tap.id==vars.get('id')).update(**vars)
        return result.as_dict()

    @auth.requires_login()
    def DELETE(*args, **vars):
        result = db(db.tap.id==vars.get('id')).delete()
        return result.as_dict()

    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)


@request.restful()
def user():

    def GET(*args, **vars):
        result = auth.login_bare(vars.get('email'), vars.get('password'))
        if result:
            result.pop('password', None)
            result.pop('registration_id', None)
            result.pop('registration_key', None)
            result.pop('reset_password_key', None)
            return result.as_dict()
        else:
            raise HTTP(401)

    def POST(*args, **vars):
        result = db.auth_user.validate_and_insert(**vars)
        return result.as_dict()

    @auth.requires_login()
    def PUT(*args, **vars):
        result = db(db.user.id==auth.user.id).update(**vars)
        return result.as_dict()

    @auth.requires_login()
    def DELETE(*args, **vars):
        result = db(db.user.id==auth.user.id).delete()
        return result.as_dict()

    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)