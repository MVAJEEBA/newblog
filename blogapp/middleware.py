from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization', None)
        
        if token:
            try:
                # Strip the 'Bearer' prefix if present
                token = token.split(' ')[1] if token.startswith('Bearer ') else token

                # Initialize JWT authentication and authenticate the token
                jwt_auth = JWTAuthentication()
                user, auth = jwt_auth.authenticate(request)

                # Set the user on the request object
                request.user = user

            except Exception as e:
                # Raise an AuthenticationFailed exception which is handled by DRF
                raise AuthenticationFailed("Invalid or expired token")

        # Continue processing the request
        response = self.get_response(request)
        return response
