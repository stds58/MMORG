from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from appcore.models import Comment
from django.core.mail import send_mail
from django.contrib.auth.models import User


@receiver(post_save, sender = Comment)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.user} {instance.date_create.strftime("%d %m %Y")}'
        recipient = User.objects.filter(username=instance.user).values('email')
        c1 = Comment.objects.get(id=instance.id)
        c1.is_sendet = True
        c1.save()

        send_mail(
            subject=subject,
            message='ваш отклик отправлен',
            from_email='stds58@yandex.ru',
            recipient_list=[recipient[0]['email'], ],
        )

@receiver(post_delete, sender = Comment)
def delete_managers_appointment(sender, instance, **kwargs):
    subject = f'{instance.user} {instance.date_create.strftime("%d %m %Y")}'
    recipient = User.objects.filter(username=instance.user).values('email')

    send_mail(
        subject=subject,
        message='ваш отклик удалён',
        from_email='stds58@yandex.ru',
        recipient_list=[recipient[0]['email'], ],
    )








