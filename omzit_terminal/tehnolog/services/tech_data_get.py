import copy
from typing import List, Dict

import openpyxl
import re
# from ..models import TechData, ProductCategory, ProductModel
from ..models import TechData, ProductCategory
from scheduler.models import ShiftTask


def tech_data_get(model_order_query: str, exel_file: str, excel_list: str):
    """
    Функция получает технологические данные из файла exel_file по списку моделей изделия model_list,
    который равен списку имен листов файла исключая имена листов в списке exclusion_list и сохраняет в модели
    django ProductModel, TechData
    :param model_order_query: заказ-модель
    :param exel_file: имя файла excel
    :param excel_list: модель изделия для получения данных - лист книги excel
    :return: None
    """
    # имя модели в базу
    model_from_model_order_query = model_order_query[model_order_query.find("_") + 1:]
    # номер заказа в базу модели в базу
    order_from_model_order_query = model_order_query[:model_order_query.find("_")]

    # Получение списка данных
    data = {
        'model_name': model_from_model_order_query,
        'order': order_from_model_order_query,
        'model_order_query': model_order_query
    }
    data_list = get_excel_data(data, exel_file, excel_list)

    # добавление в модель TechData технологических данных
    shift_tasks = ShiftTask.objects.filter(model_order_query=model_order_query)
    if (not shift_tasks.exists() or
            (shift_tasks.exists() and shift_tasks.first().st_status != 'не запланировано')):
        ShiftTask.objects.filter(model_order_query=model_order_query).delete()
        print('Удалено!')
        tasks = [ShiftTask(**data) for data in data_list]
        ShiftTask.objects.bulk_create(tasks)
    else:
        tasks = []
        errors = {
            'changed_rows': {},
            'deleted_rows': {},
            'added_rows': {}
        }
        for data in data_list:
            updated_data = dict()
            for key in ('ws_number', 'norm_tech', 'draw_filename'):
                updated_data[key] = data.pop(key)
            try:
                shift_tasks = shift_tasks.exclude(excel_list_name=data['excel_list_name'])
                task = ShiftTask.objects.get(**data)
                task.ws_number = updated_data['ws_number']
                task.norm_tech = updated_data['norm_tech']
                task.draw_filename = updated_data['draw_filename']
                tasks.append(task)
            except ShiftTask.DoesNotExist:
                current_data = ShiftTask.objects.filter(excel_list_name=data['excel_list_name'])
                row = int(data['excel_list_name'].split('-')[-1]) + 1
                if current_data.exists():
                    errors['changed_rows'].update({row: (current_data[0], data)})
                else:
                    errors['added_rows'].update({row: data})
        for task in shift_tasks:
            row = int(task.excel_list_name.split('-')[-1]) + 1
            errors['deleted_rows'].update({row: task})
        ShiftTask.objects.bulk_update(tasks, ['ws_number', 'norm_tech', 'draw_filename'])
        return errors


def get_excel_data(data: Dict, exel_file: str, excel_list: str) -> List:
    ex_wb = openpyxl.load_workbook(exel_file, data_only=True)
    excel_list = excel_list.strip()
    ex_sh = ex_wb[excel_list.strip()]

    # шаблон номера операции
    op_number_template = r'\d\d.\d\d*'

    # определение максимальной строки для чтения
    max_read_row = 1
    for row in ex_sh.iter_rows(min_row=2, min_col=1, max_row=ex_sh.max_row,
                               max_col=2, values_only=True):
        max_read_row += 1
        if 'итого' in str(row[1]).lower():
            break

    data_list = []
    for i, row in enumerate(ex_sh.iter_rows(min_row=1, min_col=1, max_row=max_read_row,
                               max_col=ex_sh.max_column, values_only=True)):
        if re.fullmatch(op_number_template, str(row[0])):
            data.update(
                {
                    'excel_list_name': f'{excel_list}-{i}',
                    'op_number': row[0],
                    'op_name': row[1],
                    'ws_name': row[2],
                    'op_name_full': row[1] + '-' + row[2],
                    'ws_number': str(row[3]),
                    'norm_tech': row[11],
                    'draw_filename': row[15],
                }
            )
            previous_op_number = str(row[0])  # обработка объединенных ячеек имени операции
            previous_op_name = row[1]
        elif row[0] is None and row[2] is not None:  # если объединённая ячейка
            data.update(
                {
                    'excel_list_name': f'{excel_list}-{i}',
                    'op_number': previous_op_number,
                    'op_name': previous_op_name,
                    'ws_name': row[2],
                    'op_name_full': previous_op_name + '-' + row[2],
                    'ws_number': str(row[3]),
                    'norm_tech': row[11],
                    'draw_filename': row[15],
                }
            )
        else:
            continue
        data_list.append(copy.copy(data))
    return data_list



if __name__ == '__main__':
    ex_file_dir_tst = r'D:\АСУП\Python\Projects\OmzitTerminal\Трудоёмкость серия I.xlsx'
    model_list_tst = ['7000М+', '800М+']
    exclusion_list_tst = ('Интерполяция М', 'гофрирование', 'Интерполяция R')
    # tech_data_get(exel_file=ex_file_dir_tst)
