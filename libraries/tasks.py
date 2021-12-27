from datetime import date

from django.core.mail import send_mail

from base.celery import app
from libraries.models import (
    BorrowedBook,
)


@app.task()
def return_book_notification():
    borrowed_book_to_return = BorrowedBook.objects.filter(date_end=date.today())
    for borrowed_book in borrowed_book_to_return:
        send_mail('A borrowed book to return', f'Today you have to return {borrowed_book.book.title}.\n'
                                               f'Best regards, \nYour Library', from_email='wioletta.wajda82@gmail.com',
                  recipient_list=[borrowed_book.user.email])


