from datetime import (
    date,
    datetime,
    timedelta
)

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
def return_book_notification_3_day_before():
    borrowed_book_to_return_3_day_before = BorrowedBook.objects.filter(date_end=datetime.today() + timedelta(days=3))
    for borrowed_book in borrowed_book_to_return_3_day_before:
        send_mail('A borrowed book to return', f'In 3 days the deadline for returning the book '
                                               f'{borrowed_book.book.title} expires. Remember that.\n'
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
