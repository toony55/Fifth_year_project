from django.db.models import Count
from .models import Report
from django.contrib.auth import get_user_model


def deactivate_users():
    all_users= get_user_model().objects.all()
    for userr in all_users:
        num_reports=userr.reports_received.aggregate(count=Count('reason')).get('count', 0)
        if num_reports >=10:
            userr.is_active = False
            userr.save()

#get_user_model().objects.filter(reports_received__reason__isnull=False).annotate(num_reports=Count('reports_received')).filter(num_reports__gte=10).update(is_active=False)


#red this is the way to run this file every day at 9:00 am
    """
You can execute the tasks.py file every 24 hours by scheduling a cron job.
 A cron job is a scheduled task that runs automatically at specified intervals.
 Here is an example of how you can schedule a cron job to run your tasks.py file every 24 hours:

Open your terminal or command prompt.
Type crontab -e to open the cron job editor.

0 9 * * * /path/to/your/virtualenv/bin/python /path/to/FifthYear/manage.py runserver && /path/to/your/virtualenv/bin/python /path/to/FifthYear/service/tasks.py

    """

#red OR
"""
pip install celery

from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'deactivate_users_daily': {
        'task': 'service.tasks.deactivate_users',
        'schedule': crontab(hour=9, minute=0),
    },
}
"""

#green pythonanywhere
"""
Reporting system for websites.
https://chat.openai.com/chat/e192c917-b5bc-460f-b8dc-41e065744888
"""