import os
from typing import Tuple


def handle_uploaded_file(f, filename: str, path: str) -> Tuple[bool, str]:
    """
    Обработчик копирует файл из формы загрузки частями в директорию path
    :param path: директория сохранения файла
    :param f: объект файла django
    :param filename: имя файла
    :return: полный путь сохраненного файла
    """
    is_uploaded = True
    with open(os.path.join(path, filename), 'wb+') as destination:
        for chunk in f.chunks():
            try:
                destination.write(chunk)
            except Exception as e:
                is_uploaded = False
                print(e, f"Ошибка копирования файла! {destination.name}")
                break
        else:
            print(f'Файл {destination.name} успешно загружен!')
    return is_uploaded, destination.name
