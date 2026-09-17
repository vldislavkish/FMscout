import glob
import os
import pandas as pd
from bs4 import BeautifulSoup


def get_latest_file(folder_path: str = "data", extension: str = "*.html") -> str:
    """Находит последний сохраненный файл в указанной папке по времени изменения."""
    search_pattern = os.path.join(folder_path, extension)
    files = glob.glob(search_pattern)
    if not files:
        raise FileNotFoundError(f"В папке {folder_path} не найдено файлов с расширением {extension}")

    latest_file = max(files, key=os.path.getmtime)
    return latest_file


def parse_fm_html(file_path: str) -> pd.DataFrame:
    """Загружает HTML дамп из Football Manager и преобразует его в DataFrame."""

    # Читаем файл
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Парсим HTML вручную с помощью BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')

    if not table:
        raise ValueError("В HTML файле не найдена таблица")

    # Извлекаем заголовки
    headers = []
    header_row = table.find('tr')
    if header_row:
        for th in header_row.find_all(['th', 'td']):
            headers.append(th.get_text(strip=True))

    # Извлекаем данные
    data = []
    rows = table.find_all('tr')[1:]  # Пропускаем заголовок

    for row in rows:
        row_data = []
        cells = row.find_all(['td', 'th'])
        for cell in cells:
            row_data.append(cell.get_text(strip=True))
        if row_data:  # Добавляем только непустые строки
            data.append(row_data)

    # Создаем DataFrame
    if headers and data:
        df = pd.DataFrame(data, columns=headers)
    else:
        df = pd.DataFrame()
        return df

    # Отладка: выводим информацию о столбцах
    print(f"Найдено столбцов: {len(df.columns)}")
    print(f"Столбцы: {df.columns.tolist()}")
    print(f"Строк данных: {len(df)}")

    # Список всех атрибутов которые должны быть числами
    numeric_columns = [
        'Возраст', 'Ввод', 'Вза', 'Выб', 'ИШтр', 'СВВ', 'Рук', '1на1', 'Клк',
        'Ркц', 'Взд', 'Экц', 'Агр', 'Вид', 'Поз', 'Ибм', 'Имп', 'Инт', 'Ком',
        'Кнц', 'Лид', 'ПРш', 'Раб', 'Реш', 'Смб', 'Хрб', 'Вын', 'Прг', 'Крд',
        'Лвк', 'ПрД', 'Сил', 'Скр', 'Уск', 'Вбр', 'Длн', 'Дрб', 'Зав', 'Глв',
        'Штр', 'Нав', 'Опк', 'Отб', 'Пас', 'Пен', 'ПКас', 'Тех', 'Угл', 'ОВР'
    ]

    # Преобразуем в числа только те столбцы которые есть в DataFrame
    for col in numeric_columns:
        if col in df.columns:
            original_values = df[col].copy()
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            # Проверяем были ли ошибки конвертации
            converted_count = (original_values != df[col].astype(str)).sum()
            if converted_count > 0:
                print(f"Столбец '{col}': преобразовано {converted_count} значений")

    # Проверяем что все атрибуты теперь числа
    for col in numeric_columns:
        if col in df.columns:
            non_numeric = df[~df[col].astype(str).str.match(r'^\d+(\.\d+)?$')][col].unique()
            if len(non_numeric) > 0 and non_numeric[0] != '0':
                print(f"ВНИМАНИЕ: В столбце '{col}' остались нечисловые значения: {non_numeric[:5]}")

    return df
