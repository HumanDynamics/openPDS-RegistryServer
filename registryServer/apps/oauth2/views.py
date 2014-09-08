#-*- coding: utf-8 -*-
import json, ast
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from uni_form.helpers import FormHelper, Submit, Reset
from django.contrib.auth.decorators import login_required
from oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException
from oauth2app.authorize import UnvalidatedRequest, UnauthenticatedUser
from apps.oauth2.forms import AuthorizeForm
from apps.oauth2.authorization import SchemeAgnosticAuthorizer
from oauth2app.models import AccessRange
from oauth2app.authenticate import Authenticator, AuthenticationException, JSONAuthenticator
import pdb

@login_required
def missing_redirect_uri(request):
    return render_to_response(
        'oauth2/missing_redirect_uri.html', 
        {}, 
        RequestContext(request))

def userinfo(request):
    scope = AccessRange.objects.get(key="funf_write")
    authenticator = JSONAuthenticator(scope=scope)
    try:
        # Validate the request.
        authenticator.validate(request)
    except AuthenticationException as e:
        # Return an error response.
        print e
        return authenticator.error_response("You didn't authenticate.")
    profile = authenticator.user.get_profile()
    response_dict = {}
    response_dict['id'] = profile.uuid
    response_dict['email'] = profile.user.email
    response_dict['name'] = profile.user.username
    response_dict['pds_location'] = 'http://'+str(profile.pds_location).replace("http://", "")

    return HttpResponse(json.dumps(response_dict), content_type='application/json')


@login_required
def authorize(request):
#    pdb.set_trace()
    CODE_AND_TOKEN = 3
    authorizer = Authorizer(response_type=CODE_AND_TOKEN)
    try:
        authorizer.validate(request)
    except MissingRedirectURI, e:
        return HttpResponseRedirect("/oauth2/missing_redirect_uri")
    except AuthorizationException, e:
        # The request is malformed or invalid. Automatically 
        # redirects to the provided redirect URL.
        return authorizer.error_redirect()
    if request.method == 'GET':
        # Make sure the authorizer has validated before requesting the client
        # or access_ranges as otherwise they will be None.
        template = {
            "client":authorizer.client, 
            "access_ranges":authorizer.access_ranges}
        template["form"] = AuthorizeForm()
        helper = FormHelper()
        no_submit = Submit('connect','No')
        helper.add_input(no_submit)
        yes_submit = Submit('connect', 'Yes')
        helper.add_input(yes_submit)
        helper.form_action = '/oauth2/authorize?%s' % authorizer.query_string
        helper.form_method = 'POST'
        template["helper"] = helper
        return render_to_response(
            'oauth2/authorize.html', 
            template, 
            RequestContext(request))
    elif request.method == 'POST':
        form = AuthorizeForm(request.POST)
        if form.is_valid():
            if request.POST.get("connect") == "Yes":
                return authorizer.grant_redirect()
            else:
                return authorizer.error_redirect()
    return HttpResponseRedirect("/")

@login_required
def grant(request):
    CODE_AND_TOKEN=3
    authorizer = SchemeAgnosticAuthorizer(response_type=CODE_AND_TOKEN)
    try:
        authorizer.validate(request)
    except MissingRedirectURI as e:
        print e
        return HttpResponseRedirect("/oauth2/missing_redirect_uri")
    except AuthorizationException, e:
        # The request is malformed or invalid. Automatically 
        # redirects to the provided redirect URL.
        return authorizer.error_redirect()
    return authorizer.grant_redirect()
