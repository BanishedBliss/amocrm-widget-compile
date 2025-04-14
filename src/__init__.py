import codecs
import os
import shutil
from pathlib import Path

from src.settings import widget_path, exclude_directories, widget_files_extension, widget_compiled_path, \
    widget_archive_path, exclude_filenames


def remove_previous_compilation():
    """ Удаляет предыдущие компиляции виджета. """
    if os.path.exists(widget_compiled_path):
        shutil.rmtree(widget_compiled_path)
    if os.path.exists(widget_archive_path):
        shutil.rmtree(widget_archive_path)
    ensure_directory_exists(widget_compiled_path)
    ensure_directory_exists(widget_archive_path)

def get_widget_version():
    """ Получает текущую версию виджета в файле manifest.json. """
    with open(widget_path + 'manifest.json', 'rt') as f:
        data = f.readlines()
    for line in data:
        if '"version": ' in line:
            version_quoted = line.split('"version": ')[1]
            return version_quoted.split('"')[1]

def get_compile_version(version: str, increment_version: bool):
    """ Возвращает версию, с которой будет компилироваться виджет. """
    if increment_version:
        return increment_last_version_segment(version)
    else:
        return version

def increment_last_version_segment(version: str):
    """ Увеличивает строковое значение версии виджета. Строка должна быть без двойных кавычек. """
    version_segments = version.split('.')
    version_segments[-1] = str(int(version_segments[-1]) + 1)
    return '.'.join(version_segments)

def change_manifest_version(version: str, new_version: str):
    """ Изменяет версию виджета в файле manifest.json. """
    replace_str = '"version": "' + version + '"'
    new_string = '"version": "' + new_version + '"'
    replace(widget_path + 'manifest.json', replace_str, new_string)
    replace_and_copy(widget_path + 'manifest.json', replace_str, new_string)

def get_widget_files_paths():
    """ Получает пути всех файлов виджета, критерий поиска которых указан в настройках. """
    replace_files = []
    copy_files = []
    # Найти файлы для замены.
    for dname, dirs, files in os.walk(widget_path):
        dirs[:] = [d for d in dirs if d not in exclude_directories]
        files[:] = [f for f in files if f not in exclude_filenames]
        for fname in files:
            if fname.lower().endswith(widget_files_extension):
                replace_files.append(os.path.join(dname, fname))
            else:
                copy_files.append(os.path.join(dname, fname))

    return replace_files, copy_files

def replace_in_all_files(files: list, pattern, substr):
    """ Заменяет переданную последовательность во всех файлах на переданную строку. """
    for fpath in files:
        replace_and_copy(fpath, pattern, substr)

def replace(fpath: str, pattern: str, substr: str):
    """ Заменяет переданную последовательность в файле на переданную строку. Изменяет исходный файл. """
    with open(fpath, 'r', encoding='utf-8') as old_file:
        filedata = old_file.read()
    filedata = filedata.replace(pattern, substr)
    with open(fpath, 'w', encoding='utf-8') as new_file:
        new_file.write(filedata)

def replace_and_copy(fpath: str, pattern: str, substr: str):
    """ Заменяет переданную последовательность в файле на переданную строку.
    Новый файл сохраняет в папку скомпилированного кода виджета из настроек. """
    with open(fpath, 'r', encoding='utf-8') as old_file:
        filedata = old_file.read()
    filedata = filedata.replace(pattern, substr)
    with open(get_new_file_path(fpath), 'w', encoding='utf-8') as new_file:
        new_file.write(filedata)

def copy_unchanged_files(file_paths: list):
    """ Копирует файлы в папку скомпилированного кода виджета из настроек. """
    for file_path in file_paths:
        shutil.copyfile(file_path, get_new_file_path(file_path))

def get_new_file_path(src_path: str):
    """ Получает путь к новому файла в папке скомпилированного кода виджета. """
    relative_path = src_path.split('../')[1]
    new_file_path = widget_compiled_path + relative_path
    ensure_directory_exists(new_file_path)
    return new_file_path

def ensure_directory_exists(filepath: str):
    """ Убеждается что директория файла существует. """
    ensure_dir = os.path.dirname(filepath)
    Path(ensure_dir).mkdir(parents=True, exist_ok=True)

def create_zip_archive():
    """ Создаёт архив виджета. """
    ensure_directory_exists(widget_archive_path)
    shutil.make_archive(widget_archive_path + 'widget', 'zip', widget_compiled_path)