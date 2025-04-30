from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token


# custom authentication class to authenticate users using tokens stored in cookies
class CookiesTokenAuthentication(TokenAuthentication):

    def authenticate(self, request):
        token = request.COOKIES.get('token')
        if not token:
            return None
        try:
            return self.authenticate_credentials(token)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid Token")