import pandas as pd


class RoleCalculator:
    """Класс для расчета эффективных рейтингов игроков по ролям (Football Manager)."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        # Отладка: проверяем типы данных
        print("\nТипы данных перед расчетом:")
        for col in ['Ввод', 'Вза', 'Выб', 'ИШтр', 'СВВ', 'Рук', '1на1', 'Ркц', 'Взд', 'Поз', 'Инт', 'Кнц', 'ПРш',
                    'Лвк']:
            if col in df.columns:
                print(f"  {col}: {df[col].dtype}, пример: {df[col].iloc[0] if len(df) > 0 else 'N/A'}")

    def calculate_goalkeepers(self) -> pd.DataFrame:
        """Расчет ролей вратарей с округлением до 1 знака после запятой."""
        df = self.df.copy()

        # Список всех атрибутов для вратарей
        keeper_attrs = [
            'Ввод', 'Вза', 'Выб', 'ИШтр', 'СВВ', 'Рук', '1на1', 'Клк', 'Ркц',
            'Взд', 'Экц', 'Поз', 'Инт', 'Кнц', 'ПРш', 'Лвк', 'Пас', 'ПКас',
            'Вид', 'Смб', 'Уск'
        ]

        # Принудительно преобразуем все атрибуты в числа
        for attr in keeper_attrs:
            if attr in df.columns:
                df[attr] = pd.to_numeric(df[attr], errors='coerce').fillna(0)
                # Проверяем что все значения числовые
                if df[attr].dtype != 'float64' and df[attr].dtype != 'int64':
                    print(f"ВНИМАНИЕ: {attr} не преобразован в число!")

        # Удаляем старые расчетные столбцы если есть
        roles_to_calc = [
            'Вратарь (Зщ)', 'Вратарь-чистильщик (Зщ)',
            'Вратарь-чистильщик (По)', 'Вратарь-чистильщик (Ат)'
        ]
        for role in roles_to_calc:
            if role in df.columns:
                df = df.drop(columns=[role])

        print("\nРасчет ролей вратарей...")

        # Вратарь (Защита)
        df['Вратарь (Зщ)'] = (
                0.50 * (
                df['Ввод'] * 0.75 +
                df['Вза'] +
                df['Выб'] +
                df['ИШтр'] +
                df['Рук'] +
                df['1на1'] * 0.75 +
                df['Ркц'] +
                df['Взд']
        ) +
                0.30 * (
                        df['Поз'] +
                        df['Инт'] * 0.75 +
                        df['Кнц'] +
                        df['ПРш'] * 0.75
                ) +
                0.20 * (
                    df['Лвк']
                )
        ).round(1)

        # Вратарь-чистильщик (Защита)
        df['Вратарь-чистильщик (Зщ)'] = (
                0.50 * (
                df['Ввод'] * 0.75 +
                df['Вза'] * 0.75 +
                df['Выб'] +
                df['ИШтр'] +
                df['СВВ'] * 0.75 +
                df['Рук'] * 0.75 +
                df['1на1'] +
                df['Пас'] * 0.75 +
                df['ПКас'] * 0.75 +
                df['Ркц'] +
                df['Взд'] * 0.75
        ) +
                0.30 * (
                        df['Вид'] * 0.75 +
                        df['Поз'] +
                        df['Инт'] +
                        df['Кнц'] +
                        df['ПРш'] * 0.75 +
                        df['Смб'] * 0.75
                ) +
                0.20 * (
                        df['Лвк'] +
                        df['Уск'] * 0.75
                )
        ).round(1)

        # Вратарь-чистильщик (Поддержка)
        df['Вратарь-чистильщик (По)'] = (
                0.50 * (
                df['Ввод'] * 0.75 +
                df['Вза'] * 0.75 +
                df['Выб'] +
                df['ИШтр'] +
                df['СВВ'] +
                df['Рук'] * 0.75 +
                df['1на1'] +
                df['Пас'] * 0.75 +
                df['ПКас'] * 0.75 +
                df['Ркц'] +
                df['Взд'] * 0.75
        ) +
                0.30 * (
                        df['Вид'] * 0.75 +
                        df['Поз'] +
                        df['Инт'] +
                        df['Кнц'] +
                        df['ПРш'] * 0.75 +
                        df['Смб']
                ) +
                0.20 * (
                        df['Лвк'] +
                        df['Уск'] * 0.75
                )
        ).round(1)

        # Вратарь-чистильщик (Атака)
        df['Вратарь-чистильщик (Ат)'] = (
                0.50 * (
                df['Ввод'] * 0.75 +
                df['Вза'] * 0.75 +
                df['Выб'] +
                df['ИШтр'] +
                df['СВВ'] +
                df['Рук'] * 0.75 +
                df['1на1'] +
                df['Пас'] * 0.75 +
                df['ПКас'] * 0.75 +
                df['Ркц'] +
                df['Взд'] * 0.75 +
                df['Экц'] * 0.75
        ) +
                0.30 * (
                        df['Вид'] * 0.75 +
                        df['Поз'] +
                        df['Инт'] +
                        df['Кнц'] +
                        df['ПРш'] * 0.75 +
                        df['Смб']
                ) +
                0.20 * (
                        df['Лвк'] +
                        df['Уск'] * 0.75
                )
        ).round(1)

        # Ограничиваем значения от 0 до 100
        for role in roles_to_calc:
            if role in df.columns:
                df[role] = df[role].clip(0, 100)
                # Проверяем что нет строк
                if df[role].dtype == 'object':
                    print(f"ВНИМАНИЕ: {role} содержит строки!")

        print(f"Пример расчета Вратарь (Зщ): {df['Вратарь (Зщ)'].iloc[0] if len(df) > 0 else 'N/A'}")

        self.df = df
        return df

    def calculate_defenders(self) -> pd.DataFrame:
        df = self.df
        return df

    def calculate_midfielders(self) -> pd.DataFrame:
        df = self.df
        return df

    def calculate_forwards(self) -> pd.DataFrame:
        df = self.df
        return df

    def calculate_all(self) -> pd.DataFrame:
        """Единый запуск расчетов по всем амплуа."""
        self.calculate_goalkeepers()
        self.calculate_defenders()
        self.calculate_midfielders()
        self.calculate_forwards()
        return self.df
