from datetime import timedelta, date, datetime

import pymssql
import requests


def NBP_data(currency):
    days = 360
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    past_date = start_date - timedelta(days=days)

    response1 = requests.get("http://api.nbp.pl/api/exchangerates/rates/a/{}/{}/{}/?=format=json"
                             .format(currency, start_date, end_date))
    resposne2 = requests.get("http://api.nbp.pl/api/exchangerates/rates/a/{}/{}/{}/?=format=json"
                             .format(currency, past_date, start_date))

    return response1.json(), resposne2.json()


def to_data(data):
    dates = []
    values = []
    for item in data['rates']:
        values.append(item['mid'])
        dates.append(item['effectiveDate'])

    return dates, values


def main():
    USD1, USD2 = NBP_data('usd')

    baseCurrency = 'PLN'
    currency = 'USD'

    date_USD1, value_USD1 = to_data(USD1)
    date_USD2, value_USD2 = to_data(USD2)

    all_dates = date_USD2 + date_USD1
    all_values = value_USD2 + value_USD1

    data = []
    counter = 1

    # for i in range(len(all_dates) - 1):
    #     print(tuple([counter, baseCurrency, currency, all_values[i], all_dates[i]]))
    #     counter += 1

    print(100 * "=")

    for i in range(len(all_dates) - 1):
        days_ = 1
        if datetime.strptime(all_dates[i + 1], '%Y-%m-%d') == datetime.strptime(all_dates[i], '%Y-%m-%d') \
                + timedelta(days=1):
            data.append(tuple([counter, baseCurrency, currency, all_values[i], all_dates[i]]))
            counter += 1
        else:
            data.append(tuple([counter, baseCurrency, currency, all_values[i], all_dates[i]]))
            counter += 1
            while datetime.strptime(all_dates[i + 1], '%Y-%m-%d') != (
                    datetime.strptime(data[counter - 2][4], '%Y-%m-%d')
                    + timedelta(days=1)):
                data.append(tuple([counter, baseCurrency, currency, all_values[i],
                                   datetime.strftime(datetime.strptime(all_dates[i], '%Y-%m-%d') +
                                                     timedelta(days=days_), '%Y-%m-%d')]))
                counter += 1
                days_ += 1

    conn = pymssql.connect(server='DESKTOP-SQ9SGJH', database='TIDB')

    cursor = conn.cursor()

    cursor.execute('DROP TABLE dbo.CurrencyRateData')

    cursor.execute('CREATE TABLE'
                   ' CurrencyRateData(ID int, BaseCurrency varchar(3), Currency varchar(3), Rate money, Date date)')

    sql = "INSERT INTO CurrencyRateData (ID, BaseCurrency , Currency , Rate , Date)" \
          " VALUES (%s, %s, %s, %s, %s)"

    cursor.executemany(sql, data)

    conn.commit()

    cursor.execute('SELECT * FROM CurrencyRateData')
    row = cursor.fetchone()
    while row:
        print(row)
        row = cursor.fetchone()


if __name__ == "__main__":
    main()
