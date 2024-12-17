from celery import shared_task
from django.core.mail import send_mail
import logging

host_email = 'postAppEmail@emil.com'


@shared_task
def send_approval_email(author_username, author_email, post_title):
    print("DEBUG ------------ send_approval_email task started.")
    send_mail(
        subject='Your post has been approved',
        message=f'Hi {author_username}, \n\nYour post {post_title} has been approved!',
        from_email=host_email,
        recipient_list=[author_email],
    )
    logging.info("DEBUG ------------ send_approval_email task completed.")


@shared_task
def send_notification_when_post_deleted(receiver_username, receiver_email, post_title):
    logging.info(" --- send_notification_when_post_deleted task started.")
    send_mail(
        subject='Your post has been deleted by our staff',
        message=f'Hi {receiver_username}, \n\nYour post {post_title} has been deleted from our staff!\n\nTry to create your post again! :)',
        from_email=host_email,
        recipient_list=[receiver_email],
    )
    logging.info(" --- send_notification_when_post_deleted task completed.")

