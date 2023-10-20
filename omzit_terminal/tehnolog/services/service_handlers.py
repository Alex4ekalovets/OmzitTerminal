import os


def handle_uploaded_file(f, filename: str, path: str) -> str:
    """
    Обработчик копирует файл из формы загрузки частями в директорию path
    :param path: директория сохранения файла
    :param f: объект файла django
    :param filename: имя файла
    :return: полный путь сохраненного файла
    """
    with open(os.path.join(path, filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return destination.name
