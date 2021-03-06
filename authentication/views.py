import json
from datetime import datetime

# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.conf import settings
from django.http import HttpResponse

# Create your views here.
# from rest_auth.registration.views import SocialConnectView
from requests import HTTPError
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from social_django.utils import psa

from authentication.serializers import CustomJWTSerializer, SocialSerializer
from maingame.models import Profile


class Login_view(APIView):
    """
    login view class:

    can authenticate user both with JWT and OAuth standards;
    needs a json body which specifies the login type (JWt, OAuth)

    (@Response): json with token

    """
    permission_classes = ([AllowAny])
    authentication_classes = ()
    serializer_class = CustomJWTSerializer

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def JWTAuth(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = {'token': token,
                             'username': user.username}
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @psa()
    def SocialAuth(request, backend):
        """
           Exchange an OAuth2 access token for one for this site.
           This simply defers the entire OAuth2 process to the front end.
           The front end becomes responsible for handling the entirety of the
           OAuth2 process; we just step in at the end and use the access token
           to populate some user identity.
           The URL at which this view lives must include a backend field, like:
               url(API_ROOT + r'social/(?P<backend>[^/]+)/$', exchange_token),
           Using that example, you could call this endpoint using i.e.
               POST API_ROOT + 'social/facebook/'
               POST API_ROOT + 'social/google-oauth2/'
           Note that those endpoint examples are verbatim according to the
           PSA backends which we configured in settings.py. If you wish to enable
           other social authentication backends, they'll get their own endpoints
           automatically according to PSA.
           ## Request format
           Requests must include the following field
           - `access_token`: The OAuth2 access token provided by the provider
           """
        serializer = SocialSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # set up non-field errors key
            # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
            try:
                nfe = settings.NON_FIELD_ERRORS_KEY
            except AttributeError:
                nfe = 'non_field_errors'

            try:
                # this line, plus the psa decorator above, are all that's necessary to
                # get and populate a user object for any properly enabled/configured backend
                # which python-social-auth can handle.
                user = request.backend.do_auth(serializer.validated_data['access_token'])
            except HTTPError as e:
                # An HTTPError bubbled up from the request to the social auth provider.
                # This happens, at least in Google's case, every time you send a malformed
                # or incorrect access key.
                return Response(
                    {'errors': {
                        'token': 'Invalid token',
                        'detail': str(e),
                    }},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if user:
                profile = Profile.objects.get_or_create(user=user)
                profile = Profile.objects.filter(user=user).update(name=user.first_name)
                if user.is_active:
                    payload = Login_view.jwt_payload_handler(user)

                    return Response({
                        'token': Login_view.jwt_encode_handler(payload),
                        'username': user.username
                    }, status=status.HTTP_200_OK)
                    # token, _ = Token.objects.get_or_create(user=user)
                    # return Response({'token': token.key})
                else:
                    # user is not active; at some point they deleted their account,
                    # or were banned by a superuser. They can't just log in with their
                    # normal credentials anymore, so they can't log in with social
                    # credentials either.
                    return Response(
                        {'errors': {nfe: 'This user account is inactive'}},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                # Unfortunately, PSA swallows any information the backend provider
                # generated as to why specifically the authentication failed;
                # this makes it tough to debug except by examining the server logs.
                return Response(
                    {'errors': {nfe: "Authentication Failed"}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def post(self, request, *args, **kwargs):
        try:
            auth_info = json.loads(request.body)
            login_type = auth_info['login_type']
        except:
            return HttpResponse(content="request has no body", status=status.HTTP_400_BAD_REQUEST)

        if login_type == 'guest':
            return self.JWTAuth(request)
        else:
            backend = login_type
            return Login_view.SocialAuth(request, backend)


@api_view(['GET', ])
@permission_classes([AllowAny, ])
def handshake(request):
    return HttpResponse('hello to you', status=status.HTTP_200_OK)
