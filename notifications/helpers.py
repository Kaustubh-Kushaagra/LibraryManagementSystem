from .models import Notification


# def create_notification(
#     user,
#     title,
#     message,
#     link="",
# ):

#     print("===================================")
#     print("TITLE:", title)
#     print("LINK RECEIVED:", link)
#     print("===================================")

#     return Notification.objects.create(
#         user=user,
#         title=title,
#         message=message,
#         link=link,
#     )

def create_notification(user, title, message, link=""):
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        link=link,
    )

    print("SAVED LINK:", repr(notification.link))

    return notification