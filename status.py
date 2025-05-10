import requests
import a2s
import time
import os

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
SERVER_IP = "62.122.213.50"
SERVER_PORT = 27047

# Загружаем message_id из переменной окружения
message_id = os.getenv("MESSAGE_ID")

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
            os.environ["MESSAGE_ID"] = message_id  # Сохраняем в переменную окружения
    else:
        # Редактируем уже отправленное сообщение
        edit_url = f"{WEBHOOK_URL}/messages/{message_id}"
        response = requests.patch(edit_url, json={"content": status})

        # Если сообщение было удалено, создаем новое
        if response.status_code == 404:
            response = requests.post(WEBHOOK_URL, json={"content": status})
            if response.status_code == 200:
                message_id = 1342183512631152642
                os.environ["MESSAGE_ID"] = message_id  # Обновляем переменную

    time.sleep(60)  # Обновление каждую минуту

