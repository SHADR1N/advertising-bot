from .models import *


async def get_or_create_user(uid: int):
    obj = await User.objects.filter(uid == uid).exists()
    if not obj:
        obj = await User.objects.create(uid=uid)
    return obj


async def new_publication():
    ...