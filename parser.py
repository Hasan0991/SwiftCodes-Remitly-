import pandas as pd
import mysql.connector


def parse_swift_xlsx(filepath):

    df = pd.read_excel(filepath, header=0)  

    print(df.columns)

   
    parsed = []
    for _, row in df.iterrows():
        swift = row['SWIFT CODE'].strip()  # Используем правильное имя столбца
        country_code = row['COUNTRY ISO2 CODE'].strip().upper()  # Код страны в верхнем регистре
        country_name = row['COUNTRY NAME'].strip().upper()  # Имя страны в верхнем регистре
        bank_name = row['NAME'].strip()  # Имя банка

        # Проверяем, является ли значение в ADDRESS строкой, иначе присваиваем пустую строку
        address = row['ADDRESS'] if isinstance(row['ADDRESS'], str) else ''

        # Определяем, является ли это головным офисом или филиалом
        is_headquarter = swift.endswith('XXX')


        # Добавляем данные в список
        parsed.append({
            'swiftCode': swift,
            'bankName': bank_name,
            'countryISO2': country_code,
            'countryName': country_name,
            'address': address.strip(), 
            'isHeadquarter': is_headquarter,
        })

    return parsed


filepath = "Book2.xlsx"

# Парсим файл
data = parse_swift_xlsx(filepath)

# Проверяем результат
print(data)

def insert_data(data):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hasan099",
        database="swift"
    )
    cursor = connection.cursor()
    for item in data:
        cursor.execute("""
                INSERT INTO swift_codes (swiftCode, bankName, countryISO2, countryName, address, isHeadquarter)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (item['swiftCode'], item['bankName'], item['countryISO2'], item['countryName'], item['address'],
                  item['isHeadquarter']))
    connection.commit()
    cursor.close()
    connection.close()

insert_data(data)
