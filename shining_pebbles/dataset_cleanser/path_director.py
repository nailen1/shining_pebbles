import os

def get_file_path(file_folder, file_name):
    return os.path.join(file_folder, file_name)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_DIR = os.path.join(ROOT_DIR)

DATA_DIR = './data'
FILE_FOLDER_MENU2205 = 'dataset-menu2205'
FILE_FOLDER_MENU2205_SNAPSHOT = 'dataset-menu2205-snapshot'

file_folder = {
    'menu2205': get_file_path(DATA_DIR, FILE_FOLDER_MENU2205),
    'menu2205-snapshot': get_file_path(DATA_DIR, FILE_FOLDER_MENU2205_SNAPSHOT),
}