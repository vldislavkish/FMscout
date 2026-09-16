import pandas as pd


def prepare_export_structure(df: pd.DataFrame) -> pd.DataFrame:
    """Формирует итоговую структуру колонок согласно заданному порядку."""

    # Исправление опечатки FM ("Сумма транфера" -> "Сумма трансфера")
    if 'Сумма транфера' in df.columns and 'Сумма трансфера' not in df.columns:
        df = df.rename(columns={'Сумма транфера': 'Сумма трансфера'})

    # Список целевых колонок
    target_columns = [
        'Возраст',
        'Позиции',
        'Имя',
        'Зарплата',
        'Сумма трансфера',
        'Ликвидность',
        'Характер',
        'Физ',
        'Псих',
        'Тех',
        'ОВР',
        'Вратарь',
        # Роли вратарей
        'Вратарь (Зщ)',
        'Вратарь-чистильщик (Зщ)',
        'Вратарь-чистильщик (По)',
        'Вратарь-чистильщик (Ат)',
        # Остальные позиции
        'ЦЗ',
        'КЗ',
        'ОП',
        'ЦП',
        'КП',
        'АП',
        'АКП',
        'ЦН'
    ]

    # Гарантируем наличие всех требуемых колонок (если нет — создаем пустые)
    for col in target_columns:
        if col not in df.columns:
            df[col] = None

    # Возвращаем DataFrame с точным порядком колонок
    return df[target_columns]


def save_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """Сохраняет итоговый DataFrame в CSV файл с разделителем ';', чтобы Excel правильно разбивал колонки."""
    formatted_df = prepare_export_structure(df)
    formatted_df.to_csv(output_path, sep=';', index=False, encoding='utf-8-sig')
