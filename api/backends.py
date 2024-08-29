from django.contrib.auth import get_user_model
from .models import MentorModel
from django.contrib.auth.backends import ModelBackend

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=username)
            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:           
            return user_model.objects.get(id=user_id)
        except user_model.DoesNotExist:
            return None


class MentorBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            mentor = MentorModel.objects.get(username=username)
            if mentor.check_password(password):
                return mentor
        except MentorModel.DoesNotExist:
            return None
    