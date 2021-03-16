from datetime import date

import pandas as pd
import pymssql

conn = pymssql.connect(server='DESKTOP-SQ9SGJH', database='TIDB')

cursor = conn.cursor()

cursor.execute('DROP TABLE CurrencyRateData')

cursor.execute('CREATE TABLE'
               ' CurrencyRateData(ID int, BaseCurrency varchar(3), Currency varchar(3), Rate money, Date date)')

cursor.executemany(
    "INSERT INTO CurrencyRateData VALUES (%s, %s, %s, %s, %s)",
    [(1, 'PLN', 'USD', 3.145, date.today()),
     (2, 'PLN', 'USD', 3.145, date.today()),
     (3, 'PLN', 'USD', 3.145, date.today())])
conn.commit()

cursor.execute('SELECT * FROM CurrencyRateData')
row = cursor.fetchone()
A = []
while row:
    A.append(row)
    print(row)
    row = cursor.fetchone()

df = pd.DataFrame(A)
df.to_csv('zad2.csv')
