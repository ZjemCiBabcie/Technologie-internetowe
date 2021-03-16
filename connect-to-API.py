import requests
from datetime import timedelta, date
import matplotlib.pyplot as plt


def NBP_data(currency, days):
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    response = requests.get("http://api.nbp.pl/api/exchangerates/rates/a/{}/{}/{}/?=format=json"
                            .format(currency, start_date, end_date))

    return response.json()


def to_data(data):
    dates = []
    values = []
    for item in data['rates']:
        values.append(item['mid'])
        dates.append(item['effectiveDate'])

    return dates, values


def main():
    USD = NBP_data('usd', 180)

    EUR = NBP_data('eur', 180)

    date_USD, value_USD = to_data(USD)
    date_EUR, value_EUR = to_data(EUR)

    plt.plot(date_USD, value_USD, color='red', marker='o', label="USD")
    plt.plot(date_EUR, value_EUR, color='blue', marker='o', label="EUR")
    plt.legend(loc="upper right")
    plt.title('Exchange rates for USD, EUR')
    plt.xlabel('Date')
    plt.xticks(rotation='vertical')
    plt.ylabel('Rate')
    plt.show()
    plt.savefig('plot.svg')


if __name__ == "__main__":
    main()
