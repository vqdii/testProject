from flask import Flask, request, render_template

from main import LaptopFinder

app = Flask(__name__)


finder = LaptopFinder('games_data.csv', 'laptops.csv')

@app.route("/", methods=["GET", "POST"])
def index():
    laptops = []
    if request.method == "POST":
        # Получаем название игры от пользователя
        game_name = request.form.get("game")
        if game_name:
            # Вызываем метод для поиска подходящих ноутбуков
            laptops = finder.find_suitable_laptops(game_name)
    return render_template("client/index.html", laptops=laptops)

if __name__ == "__main__":
    app.run(debug=True)