from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import (
    post_save,
    post_delete,
    pre_save,
)
from django.dispatch import receiver

from libraries.models import (
    Author,
    BorrowedBook,
)

@receiver(post_save, sender=User)  # dekorator, który nasłuchuje zapisy użytkownika, następnie wsyła mail powitalny
def send_welcome_email(sender, instance: User, created=False, **kwargs):
    if created and instance.email:  # jeśli użytkownik został stworzony, instacja to user, stad instance.email
        send_mail('Welcome in Library', f'Thanks for your registration. Your account details: \n'
                                        f'Login - {instance.username} \n'
                                        f'Best regards,\n'
                                        f'Your Library',
                  from_email='wioletta.wajda82@gmail.com',
                  recipient_list=[instance.email])


@receiver(post_delete, sender=User)
def send_goodbye_email(sender, instance: User, **kwargs):
    if instance.email:
        send_mail('Goodbye in Library', f'Thank you for being a reader of our library.\n'
                                        f'We hope you will come back to us again: {instance.username}\n'
                                        f'Best regards,\n'
                                        f'Your Library',
                  from_email='wioletta.wajda82@gmail.com',
                  recipient_list=[instance.email])


@receiver(post_save, sender=BorrowedBook)  # dekorator nasłuchuje powstanie obiektu i wsyła mail z info o wypozyczeniu
def send_notification_email(sender, instance: BorrowedBook, created=False, **kwargs):
    if created and instance.user.email:
        send_mail('A borrowed book', f'In day {instance.book.title}, You have borrowed the book {instance.book.title}. '
                                     f'Remember to return to {instance.date_end}.\n'
                                     f'Best regards, \nYour Library', from_email='wioletta.wajda82@gmail.com',
                  recipient_list=[instance.user.email])


@receiver(pre_save, sender=Author)
def author_before_save(sender, instance, **kwargs):  # arg co wysało funkcję, obiekt zarejestrowany, argumenty z funkcji
    print('We are about to sign the author')
    print(instance.name, instance.surname)


@receiver(post_save, sender=Author)
def author_after_save(sender, instance, **kwargs):
    print('We just signed the author')
    print(instance.name, instance.surname)

