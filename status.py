import requests
import a2s
import time
import json
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1342146792921497712/rJVBkbox_QV2b4JaSAGDYtRioci2905SiPhFXgI-2pc-eigODkcTEZ-Jhpt0G0niR1fP"
SERVER_IP = "62.122.215.43"
SERVER_PORT = 27047
MESSAGE_FILE = "message_id.json"

# Функция для загрузки message_id из файла
def load_message_id():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, "r") as f:
            return json.load(f).get("message_id")
    return None

# Функция для сохранения message_id
def save_message_id(message_id):
    with open(MESSAGE_FILE, "w") as f:
        json.dump({"message_id": message_id}, f)

# Загружаем message_id при запуске
message_id = load_message_id()

while True:
    try:
        server_address = (SERVER_IP, SERVER_PORT)
        info = a2s.info(server_address)
        players = a2s.players(server_address)
        status = f"🎮 **{info.server_name}**\n" \
                 f"📡 **IP:** {SERVER_IP}:{SERVER_PORT}\n" \
                 f"👥 **Игроки:** {len(players)}/{info.max_players}\n" \
                 f"🎭 **Карта:** {info.map_name}"
    except:
        status = "❌ Сервер недоступен!"

    if message_id is None:
        # Отправляем первое сообщение
        response = requests.post(WEBHOOK_URL, json={"content": status})
        if response.status_code == 200:
            message_id = response.json().get("id")  # Запоминаем ID сообщения
            save_message_id(message_id)  # Сохраняем ID в файл
    else:
        # Редактируем уже отправленное сообщение
        edit_url = f"{WEBHOOK_URL}/messages/{message_id}"
        response = requests.patch(edit_url, json={"content": status})
        
        # Если сообщение было удалено, создаем новое
        if response.status_code == 404:
            response = requests.post(WEBHOOK_URL, json={"content": status})
            if response.status_code == 200:
                message_id = response.json().get("id")
                save_message_id(message_id)

    time.sleep(60)  # Обновление каждую минуту
