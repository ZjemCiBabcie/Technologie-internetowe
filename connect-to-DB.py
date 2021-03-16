import pymssql
import pandas as pd

conn = pymssql.connect(server='DESKTOP-SQ9SGJH', database='AdventureWorksTI2014')

cursor = conn.cursor()

cursor.execute('SELECT  CustomerID, PersonID, StoreID, TerritoryID, AccountNumber FROM Sales.Customer')
row = cursor.fetchone()
A = []
while row:
    A.append(row)
    print(row)
    row = cursor.fetchone()

df = pd.DataFrame(A)
df.to_csv('zad1.csv')
