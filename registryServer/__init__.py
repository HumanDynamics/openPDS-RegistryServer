from rpc4django import rpcmethod
from oauth2app.authenticate import JSONAuthenticator, AuthenticationException
from oauth2app.models import AccessRange
#from account.models import *
from django.http import HttpResponse, HttpRequest


@rpcmethod(name='registryServer.validate', signature=['HttpRequest'])
def validate(request):
    datastore_owner = ""
    pk = ""
    try:
        authenticator.validate(request)
        pk = str(authenticator.user.pk)
	if request.GET.__contains__('datastore_owner'):
   	    datastore_owner = id_to_sid(pk, request.GET.['datastore_owner'])
	else:
	    datastore_owner = None
    except AuthenticationException:
        logging.debug(authenticator.error_response())
        return authenticator.error_response()
    return {'key': pk, 'datastore_owner': datastore_owner}
    
def id_to_sid(guest, host_symbolic):
    #implement retrieval of id from symbolic id
    prof = Profile.objects.filter(user=guest)
    logging.debug('symbolic id to ID')
    logging.debug(prof)
    logging.debug(host_symbolic)
    mapping = UserToUser.objects.filter(profileGuest=prof[0], id=host_symbolic)
    if(mapping.count() != 1):
        logging.debug("couldn't find symbolic mapping.")
        return {"error": "counldn't find specified symbolic mapping"}
    logging.debug(mapping[0].profileHost)
    return mapping[0].profileHost

