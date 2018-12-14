import json
from datetime import datetime

from django.http import HttpResponse

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from authentication.serializers import CustomJWTSerializer


class Login_view(APIView):
    """
    login view class:

    can authenticate user both with JWT and OAuth standards;
    needs a json body which specifies the login type (JWt, OAuth)

    (@Response): json with token

    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = CustomJWTSerializer

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
            response_data = {'token': token, 'username': user.username}
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

    def SocialAuth(self, request):
        pass

    def post(self, request, *args, **kwargs):
        try:
            auth_info = json.loads(request.body)
            login_type = auth_info['login_type']
        except:
            return HttpResponse(content="request has no body", status=status.HTTP_400_BAD_REQUEST)

        if login_type == 'guest':
            return self.JWTAuth(request)
        else:
            return self.SocialAuth(request)

    # token authentication for guest users
    # def TokenAuth(self, request):
    #     try:
    #         user = self.create_guest_user()
    #     except:
    #         return HttpResponse(content="cannot create new user", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    #     try:
    #         token, _ = Token.objects.get_or_create(user=user)
    #         jsonRes = JSONRenderer().render({'token': token.key})
    #         return Response(data=jsonRes, status=status.HTTP_200_OK)
    #     except:
    #         return HttpResponse(content="problem in tokenizing", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    # def SocialAuth(self, request):
    #     pass
    #
    # def post(self, request):
    #     try:
    #         auth_info = json.loads(request.body)
    #         login_type = auth_info['login_type']
    #     except:
    #         return HttpResponse(content="request has no body", status=status.HTTP_400_BAD_REQUEST)
    #
    #     if login_type == 'guest':
    #         return self.JWTAuth(request)
    #     else:
    #         return self.SocialAuth(request)
