import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils.timezone import utc
from board.models import Post
from accounts.models import RegistrationCodes
from users.models import CustomUser
import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


logger = logging.getLogger(__name__)


def weekly_sending():
    users = CustomUser.objects.all()
    emails = [user.email for user in users]
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    posts = Post.objects.filter(creation_time__range=[now - datetime.timedelta(days=7), now])
    if posts:
        html_content = render_to_string(
            'email_templates/weekly_sending.html', {'posts': posts}
        )
        msg = EmailMultiAlternatives(
            subject='Новое на этой неделе!',
            body=f'Здравствуй!. Новые посты появились за эту неделю!',
            from_email=None,
            to=emails,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def daily_codes_clear():
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    codes = RegistrationCodes.objects.filter(creation_time__range=[now - datetime.timedelta(days=1), now])
    for code in codes:
        code.delete()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_sending,
            trigger=CronTrigger(week="*/1"),
            id="weekly_sending",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_sending'.")

        scheduler.add_job(
            daily_codes_clear,
            trigger=CronTrigger(day="*/1"),
            id="daily_codes_clear",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'daily_codes_clear'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")