import glob
import os
import pandas as pd


def get_latest_file(folder_path: str = "data", extension: str = "*.html") -> str:
    """Находит последний сохраненный файл в указанной папке по времени изменения."""
    search_pattern = os.path.join(folder_path, extension)
    files = glob.glob(search_pattern)

    if not files:
        raise FileNotFoundError(f"В папке {folder_path} не найдено файлов с расширением {extension}")

    # Сортировка по времени последней модификации
    latest_file = max(files, key=os.path.getmtime)
    return latest_file


def parse_fm_html(file_path: str) -> pd.DataFrame:
    """Загружает HTML дамп из Football Manager и преобразует его в DataFrame."""
    dfs = pd.read_html(file_path, encoding='utf-8')
    df = dfs[0] if dfs else pd.DataFrame()
    return df
