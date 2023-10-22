## #Предложения
-[ ] Из `tehnolog.views.tehnolog_wp` вынести `group_id = -908012934` в .env
-[ ] В `tehnolog.views.tehnolog_wp` проверку доступа через  `@permission_required("scheduler.view_workshopschedule", login_url="../scheduler/login/")`. 
Предварительно распределить пользователей по группам
```python
    if str(request.user.username).strip() != "admin" and str(request.user.username[:8]).strip() != "tehnolog":
        raise PermissionDenied
```
-[ ] Переписать raw запросы в `worker.services.master_call_db.select_master_call`,  на Django ORM
-[ ] Бот вынести в отдельный сервис. для взаимодействия с ботом использовать REDIS. Обращаться в эндпоинту Django и выдавать сообщения для бота
-[ ] переписать draws. Хранить ссылки на чертеже в отдельной модели
-[ ] Заменить на проверку участия в группах `scheduler.views.LoginUser`
```python
        if 'admin' in self.request.user.username:
            return reverse_lazy('home')
        elif 'disp' in self.request.user.username:
            return reverse_lazy('scheduler')
        elif 'tehnolog' in self.request.user.username:
            return reverse_lazy('tehnolog')
        elif 'constructor' in self.request.user.username:
            return reverse_lazy('constructor')
```
-[ ] `QueryAnswerForm` заменить на `QueryChoiceField`
-[ ] Два одинаковых запроса дублируются в двух формах `tehnolog.forms.GetTehDataForm`, `tehnolog.forms.ChangeOrderModel`
-[ ] Какие статусы еще есть, почему не исключить записи только по времени
```python
    initial_shift_tasks = (ShiftTask.objects.values('id', 'ws_number', 'model_name', 'order', 'op_number',
                                                    'op_name_full', 'norm_tech', 'fio_doer', 'st_status',
                                                    'datetime_job_start', 'decision_time')
                           .filter(ws_number=ws_number).exclude(fio_doer='не распределено')
                           .exclude(Q(decision_time__lte=datetime.datetime.strptime(today, '%d.%m.%Y')) &
                                    Q(st_status='принято'))
                           .exclude(Q(decision_time__lte=datetime.datetime.strptime(today, '%d.%m.%Y')) &
                                    Q(st_status='брак'))
                           .exclude(Q(decision_time__lte=datetime.datetime.strptime(today, '%d.%m.%Y')) &
                                    Q(st_status='не принято'))
                           .order_by("st_status"))
```
-[ ] В скрипте worker.html на вызов диспетчера и мастера необходимо добавить if (st_id != "0") или можно вызывать независимо от СЗ?
-[ ] убрать лишнее 
```python
            elif 'запланировано' in request.POST['task_id']:
                alert_message = 'СЗ принято в работу.'
```
-[ ] `elif st_number == '0':` переместить до вызова функции с обращением к БД. Для чего пункт выберите сменно задание в select