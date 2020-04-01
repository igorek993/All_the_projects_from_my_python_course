# -*- coding: utf-8 -*-

import os, time, shutil
import zipfile as zp

# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени создания файла.
# Обработчик файлов делать в обьектном стиле - на классах.
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит)
#
# Пригодятся функции:
#   os.walk
#   os.path.dirname
#   os.path.join
#   os.path.normpath
#   os.path.getmtime
#   time.gmtime
#   os.makedirs
#   shutil.copy2
#
# Чтение документации/гугла по функциям - приветствуется. Как и поиск альтернативных вариантов :)
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

ICONS_ZIP = os.path.normpath('icons.zip')

FINAL_FOLDER = os.path.normpath('icons_by_year')


class PhotosSorter:

    def __init__(self, scanned_files_dir, zip_to_scan):
        self.zip_to_scan = zip_to_scan
        self.end_folder = scanned_files_dir

    def unzip_files(self, file):
        with zp.ZipFile(file, 'r') as file_z:
            file_z.extractall()

    def create_end_folder(self):
        if not os.path.isdir(self.end_folder):
            os.makedirs(self.end_folder)

    def sort_files(self):
        for dirpath, dirnames, filenames in os.walk(self.zip_to_scan):
            for img in filenames:
                img_path = os.path.join(dirpath, img)
                time_of_creation = time.gmtime(os.path.getmtime(img_path))[0:2]
                final_dir = os.path.join(self.end_folder, str(time_of_creation[0]),
                                         str(time_of_creation[1]))
                if not os.path.isdir(final_dir):
                    os.makedirs(final_dir)
                shutil.copy2(img_path, final_dir)

    def sort(self):
        self.create_end_folder()
        self.sort_files()


class PhotosSorterZip(PhotosSorter):

    def zip_namelist(self):
        with zp.ZipFile(self.zip_to_scan, 'r') as myzip:
            return myzip.namelist()

    def get_date(self, file_name):
        with zp.ZipFile(self.zip_to_scan, 'r') as myzip:
            return myzip.getinfo(file_name).date_time

    def get_obj_info(self, file_name):
        with zp.ZipFile(self.zip_to_scan, 'r') as myzip:
            return myzip.getinfo(file_name)

    def check_folder_existence(self, final_dir):
        if not os.path.isdir(final_dir):
            os.makedirs(final_dir)

    def extract_image(self, filename, final_dir):
        with zp.ZipFile(self.zip_to_scan, 'r') as myzip:
            with myzip.open(filename) as source:
                with open(os.path.normpath(os.path.join(final_dir, filename)), 'wb') as target:
                    shutil.copyfileobj(source, target)

    #  Вы пытаетесь открыть папку на запись, а надо открывать файл: добавьте к папке имя копируемого файла.

    #  Maybe I am blind or stupid, but I tried to do these two options:
    # with open(os.path.normpath(os.path.join(final_dir, filename)), 'wb') as target:
    # and
    # with zp.ZipFile(os.path.normpath(os.path.join(self.zip_to_scan, filename)) 'r') as myzip:
    #  none of them works for me...
    #  Would you please, explain to me one thing. How come that we have to add a name of a file to a directory
    #  if we have to copy a certain FILE to this FOLDER. Shouldn't we have a file as a source(in this case) and
    #  the name of a folder as a target??? Please, explain it to me like if I were in the 1st grade,
    #  cause I am really confused. I am sorry for making you look at it over and over again.
    # TODO 1) Функция copyfileobj ожидает два файла, файл-источник и файл-приемник, так она устроена. Возможно другие
    #  функции имеют другой интерфейс.
    #  2) вы используете filename который содержит и папки указанные в архиве-источнике, а вам нужен "очищенное" от
    #  папок имя файла, используйте os.path.basename чтобы его получить



    #  I keep getting the same mistake for some reason... I tried to fix it before, but it  keeps telling me this
    # TODO Вы пытаетесь открыть папку на запись, а надо открывать файл: добавьте к папке имя копируемого файла.
    # C:\Python38-32\python.exe C:/Users/igorek/PycharmProjects/python_base/lesson_009/03_files_arrange.py
    # Traceback (most recent call last):
    #   File "C:/Users/igorek/PycharmProjects/python_base/lesson_009/03_files_arrange.py", line 115, in <module>
    #     a.sort_files()
    #   File "C:/Users/igorek/PycharmProjects/python_base/lesson_009/03_files_arrange.py", line 107, in sort_files
    #     self.extract_image(filename, final_dir)
    #   File "C:/Users/igorek/PycharmProjects/python_base/lesson_009/03_files_arrange.py", line 93, in extract_image
    #     with open(final_dir, 'wb') as target:
    # PermissionError: [Errno 13] Permission denied: 'C:\\Users\\igorek\\PycharmProjects\\python_base\\lesson_009\\2017\\9'

    def sort_files(self):
        for filename in self.zip_namelist():
            if 'png' in filename:
                date = self.get_date(filename)
                final_dir = os.path.join(self.end_folder,
                                         str(date[0]), str(date[1]))
                self.check_folder_existence(final_dir)
                self.extract_image(filename, final_dir)

    def sort(self):
        self.create_end_folder()
        self.sort_files()


a = PhotosSorterZip(FINAL_FOLDER, ICONS_ZIP)
a.sort_files()

# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Это относится ктолько к чтению файлов в архиве. В случае паттерна "Шаблонный метод" изменяется способ
# получения данных (читаем os.walk() или zip.namelist и т.д.)
# Документация по zipfile: API https://docs.python.org/3/library/zipfile.html
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
