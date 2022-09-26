from sanitize_filename import sanitize
from pytube import YouTube
from time import sleep
import requests
import json
import os

BOT_TOKEN = ""
URL = "https://api.telegram.org/bot{}/".format(BOT_TOKEN)
ALLOWED_CHAT_IDS = [
    1234567890,
]


def download_audio(url):

    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()

    destination = '.'

    out_file = video.download(output_path=destination)

    new_file = sanitize(yt.title) + '.mp3'
    new_file = new_file.replace(' ', '_')
    os.rename(out_file, new_file)

    return new_file


def main():

    for allowed_chat in ALLOWED_CHAT_IDS:
        url = URL + f'sendMessage?text=Bot is online&chat_id={allowed_chat}'
        requests.get(url)

    update_url = URL + "getUpdates?limit=1&offset=-1"

    old_update_id = None

    while True:
        response = requests.get(update_url)
        content = response.content.decode("utf8")
        last_update = json.loads(content)

        try:
            last_update_id = last_update['result'][0]['update_id']

        except Exception as e:
            last_update_id = None

        if last_update_id:
            if not old_update_id:
                old_update_id = last_update_id

            if last_update_id != old_update_id:
                old_update_id = last_update_id

                client_chat_id = last_update['result'][0]['message']['from']['id']
                if client_chat_id not in ALLOWED_CHAT_IDS:
                    for allowed_chat in ALLOWED_CHAT_IDS:
                        url = URL + f'sendMessage?text=Someone with id {client_chat_id} tried accessing the bot&chat_id={allowed_chat}'
                        requests.get(url)
                else:
                    video_url = last_update['result'][0]['message']['text']

                    try:
                        url = URL + f'sendMessage?text=Downloading...&chat_id={client_chat_id}'
                        requests.get(url)

                        audio_file = download_audio(video_url)

                        file_stats = os.stat(audio_file)
                        if file_stats.st_size / (1024 * 1024) < 50.0:
                            file = {'document': open(f'{audio_file}', 'rb')}
                            requests.post(URL + 'sendDocument?chat_id=' + str(client_chat_id), files=file)
                        else:
                            url = URL + f'sendMessage?text=File dimension larger than 50MB&chat_id={client_chat_id}'
                            requests.get(url)

                        os.remove(audio_file)

                    except Exception as e:
                        url = URL + f'sendMessage?text=Encountered error "{e}" while trying to download {video_url}&chat_id={client_chat_id}'
                        requests.get(url)

        sleep(10)


if __name__ == '__main__':
    main()

