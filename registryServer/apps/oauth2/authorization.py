from oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException
from oauth2app.authorize import UnvalidatedRequest, UnauthenticatedUser, InvalidRequest, RESPONSE_TYPES
from oauth2app.lib.uri import add_parameters, add_fragments, normalize
from oauth2app.models import Client, AccessRange, AccessToken
from oauth2app.consts import CODE, TOKEN, CODE_AND_TOKEN, ACCESS_TOKEN_EXPIRATION, AUTHENTICATION_METHOD, MAC, BEARER, MAC_KEY_LENGTH
from django.http import HttpResponse


class SchemeAgnosticAuthorizer(Authorizer):
    """ OAuth 2.0 authorizer that doesn't require an http or https scheme on redirect URIs 
    This is useful for providing URIs that cause native applications to open, rather than web broswers."""
    def _validate(self):
        """Validate the request."""
        if self.client_id is None:
            raise InvalidRequest('No client_id')
        try:
            self.client = Client.objects.get(key=self.client_id)
        except Client.DoesNotExist:
            raise InvalidClient("client_id %s doesn't exist" % self.client_id)
        # Redirect URI
        if self.redirect_uri is None:
            if self.client.redirect_uri is None:
                raise MissingRedirectURI("No redirect_uri"
                    "provided or registered.")
        elif self.client.redirect_uri is not None:
            if normalize(self.redirect_uri) != normalize(self.client.redirect_uri):
                self.redirect_uri = self.client.redirect_uri
                raise InvalidRequest("Registered redirect_uri doesn't "
                    "match provided redirect_uri.")
        self.redirect_uri = self.redirect_uri or self.client.redirect_uri
        # Check response type
        if self.response_type is None:
            raise InvalidRequest('response_type is a required parameter.')
        if self.response_type not in ["code", "token"]:
            raise InvalidRequest("No such response type %s" % self.response_type)
        # Response type
        if self.authorized_response_type & RESPONSE_TYPES[self.response_type] == 0:
            raise UnauthorizedClient("Response type %s not allowed." %
                self.response_type)
        # Scope
        if self.authorized_scope is not None and self.scope is None:
            self.scope = self.authorized_scope
        if self.scope is not None:  
            self.access_ranges = AccessRange.objects.filter(key__in=self.scope)
            access_ranges = set(self.access_ranges.values_list('key', flat=True))
            difference = access_ranges.symmetric_difference(self.scope)
            if len(difference) != 0:
                raise InvalidScope("Following access ranges do not "
                    "exist: %s" % ', '.join(difference))
            if self.authorized_scope is not None:
                new_scope = self.scope - self.authorized_scope
                if len(new_scope) > 0:
                    raise InvalidScope("Invalid scope: %s" % ','.join(new_scope))

    def _check_redirect_uri(self):
        """Raise MissingRedirectURI if no redirect_uri is available."""
        if self.redirect_uri is None:
            raise MissingRedirectURI('No redirect_uri to send response.')

    def error_redirect(self):
        """In the event of an error, return a Django HttpResponseRedirect
        with the appropriate error parameters.

        Raises MissingRedirectURI if no redirect_uri is available.

        *Returns HttpResponseRedirect*"""
        self._check_redirect_uri()
        if self.error is not None:
            e = self.error
        else:
            e = AccessDenied("Access Denied.")
        parameters = {'error': e.error, 'error_description': u'%s' % e.message}
        if self.state is not None:
            parameters['state'] = self.state
        redirect_uri = self.redirect_uri
        if self.authorized_response_type & CODE != 0:
            redirect_uri = add_parameters(redirect_uri, parameters)
        if self.authorized_response_type & TOKEN != 0:
            redirect_uri = add_fragments(redirect_uri, parameters)
        response = HttpResponse("", status=302)
        response["Location"] = redirect_uri
        return response


    def grant_redirect(self):
        """On successful authorization of the request, return a Django
        HttpResponseRedirect with the appropriate authorization code parameters
        or access token URI fragments..

        Raises UnvalidatedRequest if the request has not been validated.

        *Returns HttpResponseRedirect*"""
        if not self.valid:
            raise UnvalidatedRequest("This request is invalid or has not "
                "been validated.")
        if self.user.is_authenticated():
            parameters = {}
            fragments = {}
            if self.scope is not None:
                access_ranges = list(AccessRange.objects.filter(key__in=self.scope))
            else:
                access_ranges = []
            if RESPONSE_TYPES[self.response_type] & CODE != 0:
                code = Code.objects.create(
                    user=self.user,
                    client=self.client,
                    redirect_uri=self.redirect_uri)
                code.scope.add(*access_ranges)
                code.save()
                parameters['code'] = code.key
            if RESPONSE_TYPES[self.response_type] & TOKEN != 0:
                access_token = AccessToken.objects.create(
                    user=self.user,
                    client=self.client)
                access_token.scope = access_ranges
                fragments['access_token'] = access_token.token
                if access_token.refreshable:
                    fragments['refresh_token'] = access_token.refresh_token
                fragments['expires_in'] = ACCESS_TOKEN_EXPIRATION
                if self.scope is not None:
                    fragments['scope'] = ' '.join(self.scope)
                if self.authentication_method == MAC:
                    access_token.mac_key = KeyGenerator(MAC_KEY_LENGTH)()
                    fragments["mac_key"] = access_token.mac_key
                    fragments["mac_algorithm"] = "hmac-sha-256"
                    fragments["token_type"] = "mac"
                elif self.authentication_method == BEARER:
                    fragments["token_type"] = "bearer"
                access_token.save()
            if self.state is not None:
                parameters['state'] = self.state
            redirect_uri = add_parameters(self.redirect_uri, parameters)
            redirect_uri = add_fragments(redirect_uri, fragments)
            response = HttpResponse("", status=302)
            response["Location"] = redirect_uri
            return response
        else:
            raise UnauthenticatedUser("Django user object associated with the "
                "request is not authenticated.")

