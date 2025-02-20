import requests
import a2s
import time

WEBHOOK_URL = "https://discord.com/api/webhooks/1342146792921497712/rJVBkbox_QV2b4JaSAGDYtRioci2905SiPhFXgI-2pc-eigODkcTEZ-Jhpt0G0niR1fP"
SERVER_IP = "62.122.215.43"
SERVER_PORT = 27047

# Получаем информацию о вебхуке
webhook_info = requests.get(WEBHOOK_URL).json()
webhook_name = webhook_info.get("name", "")
message_id = webhook_name.split(" | ID: ")[-1] if " | ID: " in webhook_name else None

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
            message_id = response.json().get("id")  # Получаем ID сообщения

            # Сохраняем ID в названии вебхука
            webhook_new_name = f"Server Status | ID: {message_id}"
            requests.patch(WEBHOOK_URL, json={"name": webhook_new_name})

    else:
        # Редактируем уже отправленное сообщение
        edit_url = f"{WEBHOOK_URL}/messages/{message_id}"
        response = requests.patch(edit_url, json={"content": status})

        # Если сообщение удалено — создаем новое и обновляем название вебхука
        if response.status_code == 404:
            response = requests.post(WEBHOOK_URL, json={"content": status})
            if response.status_code == 200:
                message_id = response.json().get("id")
                webhook_new_name = f"Server Status | ID: {message_id}"
                requests.patch(WEBHOOK_URL, json={"name": webhook_new_name})

    time.sleep(60)  # Обновление каждую минуту
