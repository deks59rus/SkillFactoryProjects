from config import API_KEY
import requests, json


class Request_To_API:
    @staticmethod
    def get_price(base: str, quote:str, amount:str):
    #Отлов ошибок
        if quote == base:
            raise (ConvertionException("Попытка конвертации идентичных валют!"))
        try:
            amount = float(amount)
        except ValueError:
            raise (ConvertionException("Количество валюты не является числовым значением!"))
        if amount<=0:
            raise (ConvertionException("Некорректное количество валюты!"))
    # Формирование корректной строки запроса
        url = "https://api.currencyapi.com/v3/latest?apikey=" + API_KEY + "&currencies=" + quote + '&base_currency=' + base

    #Получение данных о курсах валют с сайта currencyAPI
        response = requests.get(url)
    #Парсинг ответа с помощью JSON
        data = json.loads(response.content)

        cost = dict(data["data"][quote])
        cost= float(cost["value"])
        result = cost*float(amount)

        return round(result, 2)


class ConvertionException(Exception):
    pass
# dictionary = {}
# with open("values.txt", 'r') as f:
#     for line in f:
#         valute, code= line.split(",")
#         valute, code = valute.strip().lower(), code.strip()
#         dictionary[valute]=code
# print(dictionary)


