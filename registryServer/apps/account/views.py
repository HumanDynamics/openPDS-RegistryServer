#-*- coding: utf-8 -*-

from forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from oauth2app.models import Client, AccessRange
#from .forms import *
from django.contrib.admin.views.decorators import staff_member_required
#from datastoreUtils import *
import pymongo
import json

@login_required
def clients(request):
    if request.method == "POST":
        form = CreateClientForm(request.POST)
        remove_form = ClientRemoveForm(request.POST)
        if form.is_valid():
            Client.objects.create(
                name=form.cleaned_data["name"],
                user=request.user)
        elif remove_form.is_valid():
            Client.objects.filter(
                id=remove_form.cleaned_data["client_id"]).delete()
            form = CreateClientForm()           
    else:
        form = CreateClientForm()
    template = {
        "form":form, 
        "clients":Client.objects.filter(user=request.user)}
    return render_to_response(
        'account/clients.html', 
        template, 
        RequestContext(request))    

@login_required    
def logout(request):
    auth.logout(request)
    return render_to_response(
        'account/logout.html', 
        {}, 
        RequestContext(request))

def profiles(request): 
    return render_to_response(
        'account/profiles.html',
        {},
        RequestContext(request))

def members(request): 
    clients = Client.objects.all()
    template = {}
    template['clients'] = clients
    return render_to_response(
        'account/members.html',
        template,
        RequestContext(request))

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                    form.cleaned_data["username"],
                    form.cleaned_data["username"],
                    form.cleaned_data["password1"],)
            #profile = Profile.objects.create(user=user)
            user = auth.authenticate(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password1"])
            auth.login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = SignupForm()
    template = {"form":form}
    return render_to_response(
        'account/signup.html', 
        template, 
        RequestContext(request))

def getProfile(user):
    try:
        profile = user.get_profile()
    except:
        profile = Profile(user=user)
        profile.save()
    return profile

def getStaticObjectOrCreate(Object, **kwargs):
    try:
        object = Object.objects(**kwargs)[0]
    except:
        object = Object(**kwargs)
        object.save()
    return object

@login_required
#@staff_member_required
def roleUsers(request, hostUserID):
    hostUser = get_object_or_404(User, pk=hostUserID)
    profile = getProfile(hostUser)
    
    roleToProfileForm = RoleToProfileForm()
    roleToProfiles = []
    roles = {}
    try:
        # process Form
        if request.method == 'POST':
            roleToProfileForm = RoleToProfileForm(request.POST)
            if roleToProfileForm.is_valid():
                role = roleToProfileForm.cleaned_data['role']
                userGuestID = roleToProfileForm.cleaned_data['uid']
                try:
                    userGuest = User.objects.get(id=userGuestID)
                    u2u, isNew = UserToUser.objects.get_or_create(profileHost=profile, profileGuest=getProfile(userGuest),role=str(role))
                    u2uPk = str(u2u.pk)
#                    roles = pp['roles']
#                    uidRoles = pp['uidRoles']
#                    if not roles.__contains__(role):
#                        roles[role] = False
#                    if not uidRoles.__contains__(u2uPk):
#                        uidRoles[u2uPk] = []
#		    #TODO needs to be created in user's pds
#		    pds_location = profile.pds_location
#
#                    uidRoles[u2uPk].append(role)
#                    uidRoles[u2uPk] = list(set(uidRoles[u2uPk]))
#                    db.personalPermissions.save(pp)
                except:
                    pass #TODO return FormValidation error - User with uid does not exist
        
        # get current Roles
#        roles = pp['roles']
#        uidRoles = pp['uidRoles']
	uidRoles = {}
	roles = {}
        
        for uid, value in uidRoles.items():
            try:
                userGuest = UserToUser.objects.get(pk=uid).profileGuest.user
                roleToProfiles.append((userGuest, value, uid))
            except:
                continue
            
        
    finally:
        #connection.disconnect()
	print "end"
    
    return render_to_response(
        'account/groupUsers.html', 
        {
          'roleToProfileForm': roleToProfileForm,
          'roleToProfiles': roleToProfiles,
          'roles': roles,
          'host': hostUser,
        }, 
        RequestContext(request))


def addRoleToPDS(pds_location, sid, key):

    try:
        # get pds location and user id
        request_path=str(pds_location)+"api/roles/role/?format=json&token=e3912e17bc&scope=funf_write"
	pds_json = {'key':key,'ids':sid}
        data = json.dumps(pds_json)
        req = urllib2.Request(request_path, data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()

    except Exception as ex:
        logging.debug(ex.args)
        return None
    return response

@login_required
@staff_member_required
def adminToolbar(request):
    saved = False
    uid = None
    user = None
    profileform = ProfileForm()
    if request.method == 'GET' and request.GET.__contains__('uid'):
        try:
            user = User.objects.get(id=request.GET['uid'])
            userform = UserForm(instance=user)
            uid = user.pk
            profileform = ProfileForm(instance=getProfile(user))
        except:
            userform = UserForm()
    elif request.method == 'POST':
        try:
            user = User.objects.get(id=request.GET['uid'])
            userform = UserForm(request.POST, instance=user)
        except:
            userform = UserForm(request.POST)
        if userform.is_valid():
            user = userform.save()
            saved = True
        if user != None:
            profileform = ProfileForm(request.POST, instance=getProfile(user))
            profileform.save()
    else:
        userform = UserForm()
    return render_to_response(
        'account/adminToolbar.html',
        {
          'userform': userform,
          'saved': saved,
          'uid': uid,
          'profileform': profileform,
        },
        RequestContext(request))


def json_auth(request):
    response_data = {}
    try:
        qdict = request.POST
        user = auth.authenticate(
            username=qdict['x'],
            password=qdict['y'])
        accessranges = AccessRange.objects.all()

        response_data['username']=str(user)
        if user is not None:
            response_data['status']="success"
            scope_list = list()
            for accessrange in accessranges:
                scope = {}
                scope['key'] = accessrange.key
                scope['description'] = accessrange.description
                scope_list.append(scope)
            response_data['scope']=scope_list
            role_list = list()
            if(user.is_staff and user.is_active):
                response_data['IDC_ADMIN']=True
            else:
                response_data['IDC_ADMIN']=False
            #    role_list.append("staff")
            #if(user.is_active):
            #    role_list.append("active")
            #if(user.is_superuser):
            #    role_list.append("superuser")
            #response_data['role']=role_list
            response_data['implicit_scope']=False

        else:
            response_data['status']="error"
            response_data['message']="Invalid username or password"
    except Exception as e:
        print e
        response_data['status']="error"
        response_data['message']="Malformed request.  Ensure your are posting x and y parameters"
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


