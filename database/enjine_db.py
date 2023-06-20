import time

from .models import *


async def get_or_create_user(uid: int):
    obj = await User.objects.filter(uid == uid).exists()
    if not obj:
        obj = await User.objects.create(uid=uid)
    return obj


async def check_last_publication(uid):
    user = await User.objects.get(uid=uid)
    last_post = user.last_publication
    if last_post == 0:
        return True
    if (time.time() - last_post) > (3600 * 72):
        return True

    return False


async def new_publication(uid,
                          link,
                          category,
                          subscribers,
                          price,
                          hours_top,
                          hours_wall,
                          count_veiw,
                          mutual_pr,
                          admin):
    user = await User.objects.get(uid=uid)
    await user.update(last_publication=int(time.time()))

    public = await Publication.objects.create(
        author=user,
        data_channel={
            "link": link,
            "category": category,
            "subscribers": subscribers,
            "price": price,
            "hours_top": hours_top,
            "hours_wall": hours_wall,
            "count_veiw": count_veiw,
            "mutual_pr": mutual_pr,
            "admin": admin
        }
    )
    return public
