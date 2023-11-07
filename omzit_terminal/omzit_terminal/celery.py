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
    # wsl --install
    # curl -fsSL https://get.docker.com -o get-docker.sh
    # sudo sh get-docker.sh
    # docker run -d -p 5672:5672 rabbitmq
    # pip install eventlet
    # celery -A omzit_terminal worker -l info -P eventlet
    try:
        # подключение к БД
        con = sqlite3.connect('D:\Projects\OmzitTerminal\omzit_terminal\db.sqlite3')
        # # con = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        # # con.autocommit = True
        # # запрос на все статусы ожидания мастера
        # select_query = f"""SELECT st_status
        #                 FROM shift_task
        #                 WHERE id={st_number}
        #                 """
        # try:
        #     cur = con.cursor()
        #     cur.execute(select_query)
        #     con.commit()
        #     shift_tasks = cur.fetchall()
        # except Exception as e:
        #     print(e, 'ошибка выборке')
        # if shift_tasks == 'ожидание мастера':  # выход при отсутствии записей
        print('Сельдерей!')
        print('Обновление статуса')
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
