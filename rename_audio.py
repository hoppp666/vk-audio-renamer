import os
import time
import requests
import vk_api

TOKEN = os.getenv("VK_TOKEN")
GROUP_ID = int(os.getenv("VK_GROUP_ID"))
TAG = "@stage_style_media"

def main():
    # Настраиваем сессию с User-Agent для корректной работы токена Маруси
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'VKAndroidApp/5.52-4543 (Android 5.1.1; SDK 22; x86_64; unknown Android SDK built for x86_64; en; 320x240)'
    })

    vk_session = vk_api.VkApi(token=TOKEN, session=session)
    vk = vk_session.get_api()
    owner_id = -abs(GROUP_ID)

    offset = 0
    count = 100
    total_updated = 0

    print("Начинаем загрузку и обработку аудиозаписей...")

    while True:
        # Получаем треки порциями по 100 штук
        response = vk.audio.get(owner_id=owner_id, count=count, offset=offset)
        tracks = response.get("items", [])

        if not tracks:
            break

        for track in tracks:
            audio_id = track["id"]
            artist = track["artist"]
            old_title = track["title"]

            # Проверяем, нет ли уже тега в названии, чтобы не дублировать его
            if TAG not in old_title:
                new_title = f"{old_title} {TAG}"
                try:
                    vk.audio.edit(
                        owner_id=owner_id,
                        audio_id=audio_id,
                        artist=artist,
                        title=new_title
                    )
                    total_updated += 1
                    print(f"[{total_updated}] Обновлено: {artist} — {new_title}")
                    # Пауза 2 секунды для защиты от капчи и блокировок ВК
                    time.sleep(2)
                except Exception as e:
                    print(f"Ошибка при обновлении трека '{old_title}' (ID {audio_id}): {e}")
                    time.sleep(5)
            else:
                print(f"Пропущено (тег уже есть): {artist} — {old_title}")

        offset += count

    print(f"Готово! Всего обновлено треков: {total_updated}")

if __name__ == "__main__":
    main()
