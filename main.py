#импортируем Flask и библиотеку Request
from flask import Flask, render_template, request
import requests
from requests.exceptions import Timeout, RequestException

#импортируем объект класса Flask
app = Flask(__name__)

#формируем путь и методы GET и POST
@app.route('/', methods=['GET', 'POST'])
#создаем функцию с переменной weather, где мы будем сохранять погоду
def index():
    weather = None
    news = None
    quote = None
#формируем условия для проверки метода. Форму мы пока не создавали, но нам из неё необходимо будет взять только город.
    if request.method == 'POST':
    #этот определенный город мы будем брать для запроса API
        city = request.form['city']
        #получаем погоду
        news = get_news()
        quote = get_quote()
        weather = get_weather(city)


    return render_template("index.html", weather=weather, news=news, quote=quote)


def get_weather(city):
    api_key = "bf482bfd8cfca1bf615f8c7f3db2b464"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=5)  # Устанавливаем тайм-аут 5 секунд
        response.raise_for_status()  # Проверка на успешный статус ответа
        return response.json()  # Если всё успешно, возвращаем результат в формате JSON
    except Timeout:
        print("Запрос занял слишком много времени и был прерван.")
    except RequestException as e:
        print(f"Произошла ошибка при запросе данных: {e}")

    return None  # Возвращаем None, если произошла ошибка

def get_news():
    api_key = "a617b533135849c1b9cf361a6b4b84ea"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    return response.json().get('articles', [])
def get_quote():
    url = "http://api.quotable.io/random"
    response = requests.get(url)
    return response.json()


if __name__ == '__main__':
    app.run(debug=True)
