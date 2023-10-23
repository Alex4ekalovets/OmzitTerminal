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
-[ ] В скрипте worker.html на вызов диспетчера и мастера необходимо добавить if (st_id != "0") или можно вызывать независимо от СЗ?
-[ ] убрать лишнее 
```python
            elif 'запланировано' in request.POST['task_id']:
                alert_message = 'СЗ принято в работу.'
```
-[ ] `elif st_number == '0':` переместить до вызова функции с обращением к БД. Для чего пункт выберите сменное задание в select
-[ ] переписать на dict
```python
        if request.GET.get('call') == 'True':
            alert_message = 'Вызов мастеру отправлен.'
        elif request.GET.get('call') == 'False_wrong':
            alert_message = 'Неверный выбор.'
        elif request.GET.get('call') == 'False':
            alert_message = 'Сменное задание не принято в работу или вызов мастеру был отправлен ранее.'
        elif request.GET.get('call') == 'True_disp':
            alert_message = 'Сообщение диспетчеру отправлено.'
        else:
            alert_message = ''
```
```python
        call_messages = {
            'True': 'Вызов мастеру отправлен.',
            'False': 'Сменное задание не принято в работу или вызов мастеру был отправлен ранее.',
            'False_wrong': 'Неверный выбор.',
            'True_disp': 'Сообщение диспетчеру отправлено.',
        }
        alert_message = call_messages.get(request.GET.get('call'), '')
```
-[ ] аналогично 
```python
            if 'брак' in request.POST['task_id']:
                alert_message = 'Это СЗ уже принято как БРАК. Необходимо перепланирование.'
            elif 'принято' in request.POST['task_id']:
                alert_message = 'Сменно задание закрыто.'
            elif 'ожидание мастера' in request.POST['task_id']:
                alert_message = 'Мастер УЖЕ вызван.'
            elif 'ожидание контролёра' in request.POST['task_id']:
                alert_message = 'Ожидается контролёр.'
            elif 'в работе' in request.POST['task_id']:
                alert_message = 'Требуется вызов мастера'
            elif 'запланировано' in request.POST['task_id']:
                alert_message = 'СЗ принято в работу.'
            else:
                alert_message = 'Все ок'
```
на
```python
            status_messages = {
                'брак': 'Это СЗ уже принято как БРАК. Необходимо перепланирование.',
                'принято': 'Сменно задание закрыто.',
                'ожидание мастера': 'Мастер УЖЕ вызван.',
                'ожидание контролёра': 'Ожидается контролёр.',
                'в работе': 'Требуется вызов мастера',
                'запланировано': 'СЗ принято в работу.'
            }
            status = re.search(r'\w*?--([а-яА-Я\s]*?)--', request.POST['task_id'])[1]
            print(status)
            alert_message = status_messages.get(status, 'Все ок')
```
-[ ] `if 'запланировано' in request.POST['task_id']:` включает так же "не запланировано", заменить на `if status == 'запланировано':`