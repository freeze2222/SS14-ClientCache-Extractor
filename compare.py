import os
import hashlib
import requests
import shutil

manifest_url = 'https://cdn.backmen.ru/cdn/version/164b8901639923a5535db79de76f359da1dfb84e/manifest'
folder = './data'
output_folder = './diff_tree'


# Создание папки вывода, если она не существует


def run():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Загрузка манифеста
    response = requests.get(manifest_url)
    manifest_lines = response.text.splitlines()

    # Извлечение хеш-сумм из манифеста
    manifest_hashes = {}
    for line in manifest_lines:
        line = line.strip()
        if line:
            hash_value, relative_path = line.split(' ', 1)
            manifest_hashes[relative_path] = hash_value
    # Сравнение файлов и копирование различающихся файлов в новую папку
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder).replace('/', '\\')
            # Чтение хеш-суммы файла
            with open(file_path, 'rb') as f:
                file_hash = hashlib.blake2b(f.read()).hexdigest().upper()
            # Проверка, отличается ли хеш-сумма файла от хеш-суммы в манифесте

            if manifest_hashes.get(relative_path) is None or file_hash != manifest_hashes.get(relative_path):
                output_path = os.path.join(output_folder, relative_path)
                output_dir = os.path.dirname(output_path)
                # Создание директории в папке вывода, если она не существует
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # Копирование файла в папку вывода
                shutil.copy2(file_path, output_path)

    print("Готово!")
