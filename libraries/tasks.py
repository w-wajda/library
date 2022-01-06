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


@app.task()
def return_book_notification_after_time():
    borrowed_book_to_return_after_time = BorrowedBook.objects.filter(date_end__lt=date.today())
    for borrowed_book in borrowed_book_to_return_after_time:
        send_mail('A borrowed book to return - reminder',
                  f'You are after the book return deadline {borrowed_book.book.title}. Please return it. \n'
                  f'Best regards, \nYour Library', from_email='wioletta.wajda82@gmail.com',
                  recipient_list=[borrowed_book.user.email])
