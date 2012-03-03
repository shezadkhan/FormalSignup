# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
########################################################################

from gluon.custom_import import track_changes; track_changes(True)
import SignUpController

pointer_list_for_current_signedup_formals = []

@auth.requires_login()

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    
    current_formal_list = db().select(db.formal.ALL)
    
    return dict(formals=current_formal_list)

def show():
    formal = db(db.formal.id==request.args(0)).select().first()

    previously_signed_up = db(db.user.created_by==auth.user_id).select()

    currently_signed_up = db(db.signup_list.formal_id==formal).select()

    temp_csp_list = []

    for person in currently_signed_up:
        temp_u = db(db.user.id==person.user_id).select()
        temp_csp_list.append(temp_u)

    return dict(formal=formal, previously_signed_up=previously_signed_up, currently_signed_up=temp_csp_list)

def add_to_list():
    formal_id, user_id = request.args
    check = db(db.signup_list.user_id==user_id and db.signup_list.formal_id==formal_id).select()
    if check.__nonzero__():
        response.flash = 'Already on the signup list you blind fool!'
    #    redirect(URL('index'))
    else:
        db.signup_list.insert(user_id= user_id, formal_id=formal_id)
        response.flash = 'Added to sign up list!'
    redirect(URL('index'))
    return dict()

def add_formal():
    form = SQLFORM(db.formal)
    if form.process().accepted:
        response.flash = 'New formal added'
        signup_object = SignUpController.SignUpToFormal(db, form.vars.id) #does all the work....
        pointer_list_for_current_signedup_formals.append(signup_object) #add it to a global list....
        redirect(URL('index'))
    return dict(form=form)

def sign_me_up():
    formal_id = request.args(0)
    form = SQLFORM.factory(
        Field('username', requires=IS_NOT_EMPTY()),
        Field('password', 'password'))
    if form.process().accepted:
        response.flash = 'form accepted'
        session.signup_username = form.vars.username
        session.signup_password = form.vars.password

        user_id = db.user.insert(email=session.signup_username, password=session.signup_password) #add user
        db.signup_list.insert(user_id=user_id, formal_id=formal_id)

    elif form.errors:
        response.flash = 'form has errors'
    return dict(formal_id=formal_id, form=form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

