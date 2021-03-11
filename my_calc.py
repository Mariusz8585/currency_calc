from flask import Flask, request, render_template
import requests, csv
import my_calc

app = Flask(__name__)


@app.route("/calc", methods=["GET", "POST"])
def currency():
    if request.method == "POST":
        my_calc.data()
        data = request.form
        currency = data.get("currency")
        currency = str(currency)
        amount = data.get("quantity")
        price = my_calc.price(currency, amount)
        return render_template("currency.html", currency=currency, amount=amount, price=price)


    else:
        return render_template("currency_template.html")


def data():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    data_dict = data[0]
    data_dict = data_dict['rates']

    with open('bank_data.csv', 'w', encoding="utf-8") as csvfile:
        fieldnames = ["currency", "code", "bid", "ask"]
        writer = csv.DictWriter(csvfile, delimiter=";", fieldnames=fieldnames)
        writer.writeheader()
        for _, n in enumerate(data_dict):
            writer.writerow(n)


def price(currency, amount):
    with open("bank_data.csv", encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                if row['currency'] == currency:
                    price = float(amount) * float(row['ask'])
                    price = round(price, 2)
                    return price

# resoults = price('dolar amerykański', 19)
# print(resoults)

