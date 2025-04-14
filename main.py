import sys

from src import get_widget_version, change_manifest_version, get_widget_files_paths, \
    replace_in_all_files, copy_unchanged_files, create_zip_archive, remove_previous_compilation, get_compile_version
from src.settings import widget_version_string


def compile_widget(increment_version: bool):
    remove_previous_compilation()
    version = get_widget_version()
    new_version = get_compile_version(version, increment_version)
    change_manifest_version(version, new_version)
    replace_files, copy_files = get_widget_files_paths()
    replace_in_all_files(replace_files, widget_version_string, new_version)
    copy_unchanged_files(copy_files)
    create_zip_archive()

if __name__ == '__main__':
    if sys.argv[1:]:
        increment_version_param = False
    else:
        increment_version_param = True

    compile_widget(increment_version_param)