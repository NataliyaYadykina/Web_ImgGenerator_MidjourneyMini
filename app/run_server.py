# run_server.py
from flask import Flask, request, render_template  # , send_file
from models.pipeline import generate_image_from_text
import json
import os
from datetime import datetime

app = Flask(__name__)

# Путь к файлу для сохранения истории запросов
history_file = 'app/history/history.json'

# Функция для записи истории запросов в JSON-файл


def save_history(user_id, description, image_path):
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    else:
        history = {}

    if user_id not in history:
        history[user_id] = []

    history[user_id].append({
        'description': description,
        'image_path': image_path,
        'timestamp': datetime.now().isoformat()
    })

    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_id = request.form["user_id"]
        description = request.form.get("description", "").strip()
        if not description:
            return "Описание не может быть пустым", 400

        image = generate_image_from_text(description)
        image_name = "generated_image"\
            + f"_{user_id}_{int(datetime.now().timestamp())}.png"
        image_path = f"app/static/{image_name}"
        image.save(image_path)
        image_path = image_path.replace("app/", "")

        save_history(user_id, description, image_path)

        return render_template("index.html",
                               image_path=image_path,
                               description=description)

    return render_template("index.html")


@app.route("/history/<user_id>")
def history(user_id):
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
            user_history = history.get(user_id, [])
    else:
        user_history = []
    return render_template("history.html",
                           user_id=user_id,
                           history=user_history)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
