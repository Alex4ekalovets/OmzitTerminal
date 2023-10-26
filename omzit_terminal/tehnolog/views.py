import datetime
import json
import os
import asyncio

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect

from constructor.forms import QueryAnswer
from .services.service_handlers import handle_uploaded_file, handle_uploaded_draw_file
from .services.tech_data_get import tech_data_get
from .forms import GetTehDataForm, ChangeOrderModel, SendDrawBack
from scheduler.models import WorkshopSchedule
from worker.services.master_call_function import terminal_message_to_id
from django.core.exceptions import PermissionDenied



@login_required(login_url="../scheduler/login/")
@permission_required("scheduler.view_workshopschedule", login_url="../scheduler/login/")
def tehnolog_wp(request):
    """
    Загрузка технологических данных
    :param request:
    :return:
    """
    group_id = -4027358064  # тг группа
    # group_id = -908012934  # тг группа
    td_queries = (WorkshopSchedule.objects.values('model_order_query', 'query_prior', 'td_status')
                  .exclude(td_status='завершено'))
    change_model_query_form = ChangeOrderModel()
    send_draw_back_form = SendDrawBack()
    alert = ''
    print(request.user.username[:8], 'tehnolog')
    # if str(request.user.username).strip() != "admin" and str(request.user.username[:8]).strip() != "tehnolog":
    #     raise PermissionDenied
    context = {}
    context.update(upload_draws(
        request=request,
        draws_path=os.path.join('D:/', 'Projects', 'OmzitTerminal', 'draws'),
        group_id=group_id
    ))
    if request.method == 'POST' and context['upload_alert'] == '':
        get_teh_data_form = GetTehDataForm(request.POST, request.FILES)  # класс форм с частично заполненными данными
        if get_teh_data_form.is_valid():
            # ключ excel_file в словаре request.FILES должен быть равен имени формы созданной в классе
            # GetTehDataForm
            file = request.FILES['excel_file']
            filename = file.name
            file_extension = os.path.splitext(filename)[1] # имя файла и расширение
            # обработка выбора не excel файла
            if file_extension != '.xlsx':
                get_teh_data_form.add_error(None, 'Файл должен быть .xlsx!')
                context.update(
                    {
                        'get_teh_data_form': get_teh_data_form,
                        'td_queries': td_queries,
                        'alert': alert,
                        'change_model_query_form': change_model_query_form,
                        'send_draw_back_form': send_draw_back_form,
                    }
                )
                return render(request, r"tehnolog/tehnolog.html", context=context)
            file_save_path = os.path.join(os.getcwd(), 'xlsx')
            os.makedirs(file_save_path, exist_ok=True)
            # обработчик загрузки файла
            xlsx_file = handle_uploaded_file(f=file, filename=filename,
                                             path=file_save_path)
            print('filename=', filename, 'path=', file_save_path, 'xlsx=', xlsx_file)
            list_name = get_teh_data_form.cleaned_data['list_names']
            # вызов сервиса получения данных из xlsx
            is_uploaded = tech_data_get(exel_file=xlsx_file, excel_list=list_name,
                          model_order_query=get_teh_data_form.cleaned_data['model_order_query'].model_order_query)
            success_message = False
            if is_uploaded:
                alert = 'Загружено успешно!'
                (WorkshopSchedule.objects.filter(model_order_query=get_teh_data_form.
                                                 cleaned_data['model_order_query'].model_order_query)
                 .update(tehnolog_query_td_fio=f'{request.user.first_name} {request.user.last_name}',
                         td_status="утверждено",
                         td_tehnolog_done_datetime=datetime.datetime.now()
                         ))
                # сообщение в группу
                success_message = True
            else:
                alert = 'Ошибка загрузки! Изменены недопустимые поля, добавлены, удалены или перемещены строки!'
               # try:
                #
                # except Exception as e:
                #     print(f'Ошибка загрузки {filename}', e)
                #     alert = f'Ошибка загрузки {filename}'
                #     success_message = False
            if success_message:
                success_group_message = (f"Загружен технологический процесс. Заказ-модель: "
                                         f"{get_teh_data_form.cleaned_data['model_order_query'].model_order_query} "
                                         f"доступен для планирования. "
                                         f"Данные загрузил: {request.user.first_name} {request.user.last_name}."
                                         )
                # asyncio.run(terminal_message_to_id(to_id=group_id, text_message_to_id=success_group_message))
                print(success_group_message, group_id)
            else:
                print('Ошибка загрузки')
            print(get_teh_data_form.cleaned_data)
    else:
        get_teh_data_form = GetTehDataForm()  # чистая форма для первого запуска
    context.update(
        {
         'get_teh_data_form': get_teh_data_form,
         'td_queries': td_queries,
         'alert': alert,
         'change_model_query_form': change_model_query_form,
         'send_draw_back_form': send_draw_back_form,
        }
    )
    print(context)
    return render(request, r"tehnolog/tehnolog.html", context=context)


def upload_draws(request, draws_path, group_id):
    alert = ''
    files = dict(request.FILES).get("draw_files")
    if request.method == 'POST' and files is not None:
        draw_files_upload_form = QueryAnswer(request.POST, request.FILES)
        if draw_files_upload_form.is_valid():
            model_order_query = draw_files_upload_form.cleaned_data['model_order_query'].model_order_query
            file_save_path = os.path.join(draws_path, model_order_query)

            # создаем файл с доступами, если не существует
            permissions_json_path = os.path.join(file_save_path, 'permissions.json')
            if not os.path.exists(permissions_json_path):
                try:
                    with open(permissions_json_path, 'w') as json_file:
                        json.dump({}, json_file)
                except Exception as e:
                    print(f'При попытке создания файла доступов {permissions_json_path} вызвано исключение: {e}')

            success = True

            for file in files:
                filename = str(file)
                print('-----', filename)
                # обработчик загрузки файла
                uploaded_file = handle_uploaded_draw_file(
                    username=request.user.username,
                    f=file,
                    filename=filename,
                    path=file_save_path
                )
                if not os.path.exists(uploaded_file):
                    alert = f'Ошибка загрузки {filename}.'
                    success = False
                    break

            if success:
                # обновление данных в БД
                WorkshopSchedule.objects.filter(
                    model_order_query=model_order_query
                ).update(
                    td_status='передано',  # статус СЗ
                    td_tehnolog_done_datetime=datetime.datetime.now(),  # время загрузки
                    tehnolog_query_td_fio=f'{request.user.first_name} {request.user.last_name}',  # ФИО констр
                    td_remarks=''
                )
                alert = 'Все файлы успешно загружены.'

                success_group_message = (f"Передано КД. Заказ-модель "
                                         f"{model_order_query}. "
                                         f"Открыт доступ в папке сервера: file://svr-003/draws/"
                                         f"{model_order_query}/. "
                                         f"Передал КД: {request.user.first_name} {request.user.last_name}. "
                                         f"Загружено файлов: {len(files)}.")
                # asyncio.run(terminal_message_to_id(to_id=group_id, text_message_to_id=success_group_message))
                print(success_group_message, group_id)

        else:
            print('INVALID FORM!')
            alert = 'Ошибка! Форма не валидна!'
    else:
        draw_files_upload_form = QueryAnswer()

    context = {'draw_files_upload_form': draw_files_upload_form, 'upload_alert': alert}
    return context


# функция с разрешенной частичной загрузкой файла
def upload_draws2(request, draws_path, group_id):
    alert = ''
    if request.method == 'POST':
        draw_files_upload_form = QueryAnswer(request.POST, request.FILES)
        if draw_files_upload_form.is_valid():
            files = dict(request.FILES)["draw_files"]
            model_order_query = draw_files_upload_form.cleaned_data['model_order_query'].model_order_query
            file_save_path = os.path.join(draws_path, model_order_query)

            if not os.path.exists(file_save_path):
                os.makedirs(file_save_path)

            not_uploaded_files = []
            for file in files:
                # обработчик загрузки файла
                is_uploaded, _ = handle_uploaded_file(
                                            f=file,
                                            filename=file.name,
                                            path=file_save_path
                                        )
                if not is_uploaded:
                    not_uploaded_files.append(file.name)

                # обновление данных в БД
                WorkshopSchedule.objects.filter(
                    model_order_query=model_order_query
                ).update(
                    td_status='передано',  # статус СЗ
                    td_tehnolog_done_datetime=datetime.datetime.now(),  # время загрузки
                    tehnolog_query_td_fio=f'{request.user.first_name} {request.user.last_name}',  # ФИО констр
                    td_remarks=''
                )

            success_message = len(not_uploaded_files) != len(files)
            if success_message:
                uploaded = len(files) - len(not_uploaded_files)
                if len(not_uploaded_files) == 0:
                    alert = 'Все файлы успешно загружены.'
                else:
                    alert = (f'Загружено {uploaded} из {len(files)}.\n'
                             f'Не удалось загрузить файлы {", ".join(not_uploaded_files)}')
                success_group_message = (f"Передано КД. Заказ-модель "
                                         f"{model_order_query}. "
                                         f"Открыт доступ в папке сервера: file://svr-003/draws/"
                                         f"{model_order_query}/. "
                                         f"Передал КД: {request.user.first_name} {request.user.last_name}. "
                                         f"Загружено файлов: {uploaded}.")
                # asyncio.run(terminal_message_to_id(to_id=group_id, text_message_to_id=success_group_message))
                print(success_group_message, group_id)
            else:
                alert = f'Ошибка при загрузке файлов!'
        else:
            print('INVALID FORM!')
            alert = 'Ошибка! Форма не валидна!'
    else:
        draw_files_upload_form = QueryAnswer()

    context = {'draw_files_upload_form': draw_files_upload_form, 'upload_alert': alert}
    return context


@login_required(login_url="../scheduler/login/")
def send_draw_back(request):
    """
    Отправка КД на доработку с замечаниями
    :param request:
    :return:
    """
    group_id = -4027358064  # тг группа
    # group_id = -908012934  # тг группа
    if request.method == 'POST':
        send_draw_back_form = SendDrawBack(request.POST)
        if send_draw_back_form.is_valid():
            # заполнение данных замечания
            (WorkshopSchedule.objects.filter(model_order_query=send_draw_back_form.
                                             cleaned_data['model_order_query'].model_order_query)
             .update(tehnolog_remark_fio=f'{request.user.first_name} {request.user.last_name}',
                     is_remark=True,
                     remark_datetime=datetime.datetime.now(),
                     td_remarks=send_draw_back_form.cleaned_data['td_remarks'],
                     td_status='замечание'
                     )
             )
            # сообщение в группу
            success_group_message = (f"КД на заказ-модель: "
                                     f"{send_draw_back_form.cleaned_data['model_order_query'].model_order_query} "
                                     f"возвращено с замечанием: {send_draw_back_form.cleaned_data['td_remarks']}. "
                                     f"КД вернул: {request.user.first_name} {request.user.last_name}."
                                     )
            # asyncio.run(terminal_message_to_id(to_id=group_id, text_message_to_id=success_group_message))
            print(success_group_message, group_id)
        else:
            pass

    return redirect('tehnolog')  # обновление страницы при успехе


@login_required(login_url="../scheduler/login/")
def new_model_query(request):
    """
    Корректировка заказ-модели
    :param request:
    :return:
    """
    group_id = -908012934  # тг группа
    if request.method == 'POST':
        change_model_query_form = ChangeOrderModel(request.POST)
        if change_model_query_form.is_valid():
            # модель_заказ
            old_model_order_query = change_model_query_form.cleaned_data['model_order_query'].model_order_query

            new_order = change_model_query_form.cleaned_data['order_query'].strip()
            new_model = change_model_query_form.cleaned_data['model_query'].strip()
            new_model_order_query = f"{new_order}_{new_model}"
            (WorkshopSchedule.objects.filter(model_order_query=old_model_order_query)
             .update(order=new_order,
                     model_name=new_model,
                     model_order_query=new_model_order_query))

            # переименование папки
            old_folder = os.path.join("C:/", "draws", old_model_order_query)
            new_folder = os.path.join("C:/", "draws", new_model_order_query)
            os.rename(old_folder, new_folder)

            # сообщение в группу
            success_group_message = (f"Заказ-модель переименован технологической службой в: "
                                     f"{new_model_order_query}. "
                                     f"Откорректировал: {request.user.first_name} {request.user.last_name}."
                                     )
            # asyncio.run(terminal_message_to_id(to_id=group_id, text_message_to_id=success_group_message))
            print(success_group_message, group_id)
        else:
            pass
    return redirect('tehnolog')  # обновление страницы при успехе

