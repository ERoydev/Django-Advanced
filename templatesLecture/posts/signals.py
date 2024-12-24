from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from posts.models import Post
from posts.tasks import send_approval_email, send_notification_when_post_deleted


@receiver(post_delete, sender=Post)
def send_notification_when_post_deleted_by_staff(sender, instance, **kwargs):
    if instance.author and instance.author.email:
        send_notification_when_post_deleted.delay(
            instance.author.username,
            instance.author.email,
            instance.title
        )


# @receiver(post_save, sender=Post)
# def send_approval_notification(sender, instance, created, **kwargs):
#     if not created and instance.approved:
#         send_approval_email.delay( # .delay() sends to redis DB where celery worker will get and execute the task
#             instance.author.username,
#             instance.author.email,
#             instance.title
#         )
