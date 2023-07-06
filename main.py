import sqlite3
import os
import zstandard as zstd


# Функция для распаковки данных сжатия ZStd
def decompress_zstd(data):
    dctx = zstd.ZstdDecompressor()
    return dctx.decompress(data)


# Подключение к базе данных SQLite
conn = sqlite3.connect("./content.db")
cursor = conn.cursor()

# Получение всех существующих ForkId
cursor.execute("SELECT DISTINCT ForkId FROM ContentVersion")
fork_ids = cursor.fetchall()

# Вывод всех ForkId
print("Существующие ForkId:")
for fork_id in fork_ids:
    print(fork_id[0])

# Ввод ForkId
fork_id = input("Введите ForkId: ")

# Получение ContentVersion id по ForkId
cursor.execute("SELECT id FROM ContentVersion WHERE ForkId = ?", (fork_id,))
content_version_id = cursor.fetchone()

if content_version_id is not None:
    # Получение элементов из ContentManifest по VersionId
    cursor.execute("SELECT Id, Path, ContentId FROM ContentManifest WHERE VersionId = ?", (content_version_id[0],))
    content_manifest_items = cursor.fetchall()

    # Цикл по значениям массива
    for item in content_manifest_items:
        item_id, item_path, content_id = item

        os.makedirs(os.path.dirname("./data/" + item_path), exist_ok=True)
        # Получение данных и сжатия из Content по id
        cursor.execute("SELECT data, compression FROM Content WHERE id = ?", (content_id,))
        content_data, compression = cursor.fetchone()

        # Проверка типа сжатия
        if compression == 0:
            # Запись файла по относительному пути

            with open("./data/"+item_path, "bw+") as file:
                file.write(content_data)
        elif compression == 2:
            # Распаковка данных сжатия ZStd и запись файла по относительному пути
            decompressed_data = decompress_zstd(content_data)
            with open("./data/"+item_path, "bw+") as file:
                file.write(decompressed_data)

        print(f"Файл {item_path} успешно записан.")
else:
    print("Форк с таким ForkId не найден.")

# Закрытие соединения с базой данных
conn.close()
