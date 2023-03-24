import os
import logging
import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from pytube import YouTube
from moviepy.editor import *

# Configuração do bot
bot_token = 'SEU_TOKEN_AQUI'
bot = telegram.Bot(token=bot_token)

# Configuração do logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    """Função para lidar com o comando /start."""
    update.message.reply_text('Olá! Envie um link do YouTube com o comando /baixar para baixar um vídeo e convertê-lo em MP3.')

def baixar(update, context):
    """Função para lidar com o comando /baixar."""
    url = context.args[0]
    try:
        # Baixa o vídeo do YouTube
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        video.download()

        # Converte o arquivo de vídeo para MP3
        mp4_file = video.default_filename
        mp3_file = os.path.splitext(mp4_file)[0] + '.mp3'
        audio_clip = AudioFileClip(mp4_file)
        audio_clip.write_audiofile(mp3_file)
        audio_clip.close()

        # Envia o arquivo MP3 para o usuário
        context.bot.send_audio(chat_id=update.message.chat_id, audio=open(mp3_file, 'rb'))

        # Exclui os arquivos MP4 e MP3
        os.remove(mp4_file)
        os.remove(mp3_file)

    except Exception as e:
        logging.error(e)
        update.message.reply_text('Desculpe, não foi possível baixar o vídeo. Verifique o link e tente novamente.')

def main():
    """Função principal do bot."""
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    # Define os manipuladores de comando e mensagem
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('baixar', baixar))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, start))

    # Inicia o bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
