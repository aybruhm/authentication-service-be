# Account Service Imports
from account_service.models import AccountUser

# Users Timestamps Imports
from account_service.services.users.timestamps import get_now


def user_record_login(*, user: AccountUser) -> AccountUser:
    user.last_login = get_now()
    user.save()

    return user