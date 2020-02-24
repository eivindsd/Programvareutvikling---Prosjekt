from website.models import Bruker

class BrukerAuth(object):
    def authenticate(self, username=None, password=None):
        try:
            user = Bruker.objects.get(username=username)
            if user.check_password(password):
                return user
        except Bruker.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = Bruker.objects.get(id= user_id)
            if user.is_active:
                return user
            return None
        except Bruker.DoesNotExist:
            return None