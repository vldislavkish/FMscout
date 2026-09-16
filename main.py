import os
from src.parser import get_latest_file, parse_fm_html
from src.roles import RoleCalculator
from src.utils import save_to_csv


def main():
    data_dir = "data"
    result_dir = "result"

    # 1. Поиск и чтение последнего сохраненного HTML-файла
    input_file = get_latest_file(folder_path=data_dir, extension="*.html")
    print(f"Загрузка файла: {input_file}")

    df = parse_fm_html(input_file)

    # 2. Расчет показателей по ролям
    calculator = RoleCalculator(df)
    df_processed = calculator.calculate_all()

    # 3. Формирование динамического имени и сохранение результата
    file_name = os.path.basename(input_file).replace(".html", ".csv")
    output_file = os.path.join(result_dir, f"final_{file_name}")

    save_to_csv(df_processed, output_file)
    print(f"Результат сохранен в: {output_file}")


if __name__ == "__main__":
    main()
