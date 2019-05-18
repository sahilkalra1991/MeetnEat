import urllib
import traceback

from django.conf import settings

from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed


class User(object):
    user_id = None
    name = None

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True


class FBLAuthentication(BasicAuthentication):
    """
    Authenticate User from JAVA User Auth API
    """
    def authenticate_credentials(self, userid, password):
        """
        Authenticate the userid and password against username and password.
        """
        # # Do some authentication from JAVA API here and get user data
        # #
        request = urllib.request.Request("{0}/auth/id/{1}?{2}".format(
            settings.JAVA_API_URL,
            userid,
            urllib.parse.urlencode({"password": password})
        ))
        try:
            with urllib.request.urlopen(request) as response:
                if response.status == 200:
                    java_user_id = response.read().decode('utf-8')
                    # Create User
                    user = User()
                    user.user_id = java_user_id
                else:
                    raise AuthenticationFailed('Invalid username/password.')
        except urllib.error.URLError:
            print("Authentication attempt URL: {}".format(request.full_url))
            traceback.print_exc()
            raise AuthenticationFailed("Invalid username/password. Error is logged")

        return user, None
