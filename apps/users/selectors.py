from apps.users.models import User

def get_user_by_phone(phone):
    return User.objects.filter(phone=phone).first()