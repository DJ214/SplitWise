from celery import shared_task
from django.core.mail import send_mail
from .models import Participant,User
from django.conf import settings

@shared_task
def send_expense_email(email, total_amount, participant_share):
    message = f"You have been added to an expense. You owe INR {participant_share} for a total expense of INR {total_amount}."
    send_mail(
        'Expense Notification',
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )



@shared_task
def send_weekly_balance_email():
    users = User.objects.all()

    for user in users:
        total_owe = 0
        participant_set = Participant.objects.filter(user=user)

        for participant in participant_set:
            total_owe += participant.share

        if total_owe > 0:
            email_content = f"Hello {user.name},\n\n"
            email_content += "Here is the total amount of money you owe to each user:\n\n"

            for participant in participant_set:
                if participant.share > 0:
                    email_content += f"- {participant.user.name}: INR {participant.share}\n"

            email_content += "\nPlease settle your dues at your earliest convenience.\n\nBest regards,\nYour Application"

            send_mail(
                'Weekly Balance Reminder',
                email_content,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
