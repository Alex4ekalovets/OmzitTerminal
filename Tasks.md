## #Предложения
-[ ] Из `tehnolog.views.tehnolog_wp` вынести `group_id = -908012934` в .env
-[ ] В `tehnolog.views.tehnolog_wp` проверку доступа через  `@permission_required("scheduler.view_workshopschedule", login_url="../scheduler/login/")`. 
Предварительно распределить пользователей по группам
```python
    if str(request.user.username).strip() != "admin" and str(request.user.username[:8]).strip() != "tehnolog":
        raise PermissionDenied
```
-[ ] Переписать raw запросы в `worker.services.master_call_db.select_master_call`,  на Django ORM, либо вынести в отдельный сервис
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