import pandas as pd


class RoleCalculator:
    """Класс для расчета эффективных рейтингов игроков по ролям (Football Manager)."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def calculate_goalkeepers(self) -> pd.DataFrame:
        """Расчет ролей вратарей с округлением до 1 знака после запятой."""
        df = self.df

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

        return df

    def calculate_defenders(self) -> pd.DataFrame:
        """Расчет ролей защитников."""
        df = self.df
        return df

    def calculate_midfielders(self) -> pd.DataFrame:
        """Расчет ролей полузащитников."""
        df = self.df
        return df

    def calculate_forwards(self) -> pd.DataFrame:
        """Расчет ролей нападающих."""
        df = self.df
        return df

    def calculate_all(self) -> pd.DataFrame:
        """Единый запуск расчетов по всем амплуа."""
        self.calculate_goalkeepers()
        self.calculate_defenders()
        self.calculate_midfielders()
        self.calculate_forwards()
        return self.df
