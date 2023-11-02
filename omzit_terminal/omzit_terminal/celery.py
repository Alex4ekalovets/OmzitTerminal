import os
import sqlite3

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omzit_terminal.settings')

app = Celery('omzit_terminal')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task
def return_in_work_status(st_number):
    # celery - A omzit_terminal worker - l INFO
    # docker run - d - p 5672: 5672 rabbitmq

    try:
        # подключение к БД
        print('Сельдерей!')
        con = sqlite3.connect('/Users/MacAlex/WorkFolder/Python/Projects/omzit_terminal/omzit_terminal/db.sqlite3')
        update_query = f"""UPDATE shift_task SET master_called = 'вызван', st_status='в работе'
                                        WHERE id={st_number};
                            """
        try:
            cur = con.cursor()
            cur.execute(update_query)
            con.commit()
        except Exception as e:
            print(e, 'ошибка обновления')
    except Exception as e:
        print('Ошибка подключения к базе', e)
    finally:
        con.close()
        print('Сельдерей!')
