""" Относительный путь до виджета. """
widget_path = '../'

""" Директория компиляции кода виджета. """
widget_compiled_path = 'widget_src/'

""" Директория итогового архива виджета. """
widget_archive_path = 'archive/'

""" Расширение файлов, в которых будет заменена версия импортируемых модулей. """
widget_files_extension = '.js'

""" Паттерн для замены в файлах виджета. """
widget_version_string = '{%widget_version%}'

""" Игнорировать следующие названия файлов. """
exclude_filenames = ['.gitignore']

""" Игнорировать следующие директории при замене версии виджета. """
exclude_directories = ['.compiled', '.devcomment', '.git', '.idea', '.gitignore']