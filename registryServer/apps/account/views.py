#-*- coding: utf-8 -*-


from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from oauth2app.models import Client, AccessRange
#from .forms import *
from django.contrib.admin.views.decorators import staff_member_required
#from registryServer.datastoreUtils import *
import pymongo

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


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                    form.cleaned_data["username"],
                    form.cleaned_data["email"],
                    form.cleaned_data["password1"],)
            profile = Profile.objects.create(user=user)
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
        (connection, db) = connectToMongoDB(str(hostUser.pk))
        # get current PersonalPermissions
        pp = findOrCreate('personalPermissions', db, emptyPersonalPermissions)

        # process Form
        if request.method == 'POST':
            roleToProfileForm = RoleToProfileForm(request.POST)
            if roleToProfileForm.is_valid():
                role = roleToProfileForm.cleaned_data['role']
                userGuestID = roleToProfileForm.cleaned_data['uid']
                try:
                    userGuest = User.objects.get(id=userGuestID)
                    u2u, isNew = UserToUser.objects.get_or_create(profileHost=profile, profileGuest=getProfile(userGuest))
                    u2uPk = str(u2u.pk)
                    roles = pp['roles']
                    uidRoles = pp['uidRoles']
                    if not roles.__contains__(role):
                        roles[role] = False
                    if not uidRoles.__contains__(u2uPk):
                        uidRoles[u2uPk] = []
                    uidRoles[u2uPk].append(role)
                    uidRoles[u2uPk] = list(set(uidRoles[u2uPk]))
                    db.personalPermissions.save(pp)
                except:
                    pass #TODO return FormValidation error - User with uid does not exist
        
        # get current Roles
        roles = pp['roles']
        uidRoles = pp['uidRoles']
        
        for uid, value in uidRoles.items():
            try:
                userGuest = UserToUser.objects.get(pk=uid).profileGuest.user
                roleToProfiles.append((userGuest, value, uid))
            except:
                continue
            
        
    finally:
        connection.disconnect()
    
    return render_to_response(
        'account/groupUsers.html', 
        {
          'roleToProfileForm': roleToProfileForm,
          'roleToProfiles': roleToProfiles,
          'roles': roles,
          'host': hostUser,
        }, 
        RequestContext(request))

@login_required
@staff_member_required
def removeRole(request, hostPk, guestPk, role):
    hostUser = get_object_or_404(User, pk=hostPk)
    try:
        (connection, db) = connectToMongoDB(hostPk)
        if db.personalPermissions.count() == 0:
            return HttpResponseRedirect('/account/role_users/' +hostPk)
        pp = db.personalPermissions.find_one()
        roles = pp['uidRoles'][guestPk]
        roles.remove(role)
        if len(roles) == 0:
            del pp['uidRoles'][guestPk]
        db.personalPermissions.save(pp)
    finally:
        connection.disconnect()
    return HttpResponseRedirect('/account/role_users/' +hostPk)
    

@login_required
@staff_member_required
def adminToolbar(request):
    saved = False
    uid = None
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
