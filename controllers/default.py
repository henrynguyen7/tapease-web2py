
response.view = 'generic.json'
response.headers['Content-Type'] = 'application/json'


@request.restful()
def user():

    def GET(*args, **vars):
        user = auth.login_bare(vars.get('email'), vars.get('password'))
        if user:
            orgs_result = db(
                (db.user_to_org.user_id == user.id) &
                (db.org.id == db.user_to_org.org_id)
            ).select()
            orgs = [org.get('org') for org in orgs_result.as_list()]
            return dict(
                id=user.id,
                name=user.name,
                email=user.email,
                image_url=user.image_url,
                is_enabled=user.is_enabled,
                orgs=orgs
            )
        else:
            raise HTTP(401)

    def POST(*args, **vars):
        result = db.auth_user.validate_and_insert(**vars)
        if result.errors:
            return result.as_dict()
        else:
            user = auth.login_bare(vars.get('email'), vars.get('password'))
            return dict(
                id=user.id,
                name=user.name,
                email=user.email,
                image_url=user.image_url,
                is_enabled=user.is_enabled,
            )

    @auth.requires_login()
    def PUT(*args, **vars):
        # TODO: Add ability to remove org from user
        if vars.get('org_name'):
            org = db(db.org.name == vars.get('org_name')).select().first()
            if org:
                result = db.user_to_org.update_or_insert(user_id=auth.user.id, org_id=org.id)
                # TODO: Recover from 500
                return dict(success=True)
        else:
            result = db(db.auth_user.id == auth.user.id).update(**vars)
        return result.as_dict()

    @auth.requires_login()
    def DELETE(*args, **vars):
        result = db(db.user.id == auth.user.id).delete()
        return result.as_dict()

    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)


@request.restful()
def org():

    @auth.requires_login()
    def GET(*args, **vars):
        org_ids = db(db.user_to_org.user_id == auth.user.id).select(db.user_to_org.ord_id).as_list()
        orgs = (db.org.id.belongs(org_ids))
        return dict(orgs=orgs)

    @auth.requires_login()
    def POST(*args, **vars):
        result = db.org.validate_and_insert(**vars)
        return result.as_dict()

    @auth.requires_login()
    def PUT(*args, **vars):
        result = db(db.org.id == vars.get('id')).update(**vars)
        return result.as_dict()

    @auth.requires_membership('admins')
    def DELETE(*args, **vars):
        result = db(db.org.id == vars.get('id')).delete()
        return result.as_dict()

    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)


@request.restful()
def tap():

    @auth.requires_login()
    def GET(*args, **vars):
        if vars.get('org_id'):
            query = db.tap.org_id == vars.get('org_id')
        else:
            org_ids = [org.get('org_id') for org in db(db.user_to_org.user_id == auth.user.id).select(db.user_to_org.org_id).as_list()]
            query = db.tap.org_id.belongs(org_ids)
        if vars.get('user_id'):
            query = query.__and__(db.tap.page_uid == vars.get('user_id'))
        if vars.get('page_uid'):
            query = query.__and__(db.tap.page_uid == vars.get('page_uid'))
        if vars.get('page_token'):
            query = query.__and__(db.tap.page_token == vars.get('page_token'))
        taps = db(query).select(orderby=db.tap.created_on)
        return dict(taps=taps.as_list())

    @auth.requires_login()
    def POST(*args, **vars):
        result = db.tap.validate_and_insert(
            user_id=auth.user.id,
            org_id=vars.get('org_id'),
            page_uid=vars.get('page_uid'),
            page_token=vars.get('page_token'),
            element_route=vars.get('element_route'),
            element_node=vars.get('element_node'),
            comment=vars.get('comment'),
        )
        return result.as_dict()

    @auth.requires_login()
    def PUT(*args, **vars):
        result = db(db.tap.id == vars.get('id')).update(**vars)
        return result.as_dict()

    @auth.requires_login()
    # TODO: Add @auth.requires_membership(tap.org_id) and @auth.requires_membership(ADMIN)
    def DELETE(*args, **vars):
        result = db(db.tap.id == vars.get('id')).delete()
        return result.as_dict()

    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)