import discord
from discord.ext import commands
import pytubefix
import os
import asyncio
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# Получение токена из переменных окружения
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Убедитесь, что ffmpeg доступен в системном пути
os.environ["FFMPEG_BINARY"] = r"C:\Users\User\Documents\discord python\ffmpeg\bin\ffmpeg.exe"

ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# Очередь для воспроизведения
queue = []
is_playing = False

@bot.command()
async def join(ctx):
    """Подключение к голосовому каналу"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if not voice or not voice.is_connected():
            await channel.connect()
            await ctx.send(f"Sankt Bogen")
    else:
        await ctx.send("Вы должны быть квинси")

@bot.command()
async def play(ctx, url):
    """Добавление трека в очередь"""
    global is_playing
    try:
        yt = pytubefix.YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()

        if not stream:
            raise Exception("Аудиопоток не найден.")

        queue.append((stream.url, yt.title))

        await ctx.send(f"Heilig Bogen: {yt.title}")

        if not is_playing:
            await play_next(ctx)
    except Exception as e:
        await ctx.send(f"Heilig Pfeil: {str(e)}")

async def play_next(ctx):
    """Воспроизведение следующего трека"""
    global is_playing
    if len(queue) > 0:
        is_playing = True
        url, title = queue.pop(0)
        await play_audio(ctx, url, title)
    else:
        is_playing = False
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice:
            await ctx.send("魂を切り裂くもの")
            # Ожидаем 1 минуту перед отключением
            await asyncio.sleep(60)
            if not voice.is_playing():
                await voice.disconnect()
                await ctx.send("Kojaku")


async def play_audio(ctx, url, title):
    """Воспроизведение аудио"""
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice or not voice.is_connected():
        await ctx.invoke(join)

    try:
        voice.play(discord.FFmpegPCMAudio(url, **ffmpeg_opts), after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
        await ctx.send(f"Ginrei Kojaku: {title}")

        while voice.is_playing():
            await asyncio.sleep(1)
    except Exception as e:
        await ctx.send(f"Hoffnung: {str(e)}")

@bot.command()
async def leave(ctx):
    """Отключение от голосового канала"""
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send("Diagramm")
    else:
        await ctx.send("Freund Schild")

@bot.command()
async def skip(ctx):
    """Пропуск текущего трека"""
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.stop()
        await ctx.send("Музыка хуйня ставлю другую")
        await play_next(ctx)
    else:
        await ctx.send("Ты шо глухой музыки и так нету ")

@bot.command()
async def Yhwach(ctx):
    """Проигрывание локального файла song.mp3"""
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice or not voice.is_connected():
        await ctx.invoke(join)

    try:
        # Путь к локальному файлу
        file_path = os.path.join(os.getcwd(), "song_PmNMoUoF.mp3")

        if not os.path.exists(file_path):
            await ctx.send("Че вякнул")
            return

        voice.play(discord.FFmpegPCMAudio(file_path), after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
        await ctx.send("СОО такакаока")

        while voice.is_playing():
            await asyncio.sleep(1)
    except Exception as e:
        await ctx.send(f"иди нахуй {str(e)}")

@bot.command()
async def Hado90(ctx):
    """Проигрывание локального файла song.mp3"""
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice or not voice.is_connected():
        await ctx.invoke(join)

    try:
        # Путь к локальному файлу
        file_path = os.path.join(os.getcwd(), "hado-90.mp3")

        if not os.path.exists(file_path):
            await ctx.send("Че вякнул")
            return

        voice.play(discord.FFmpegPCMAudio(file_path), after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
        await ctx.send("hado 90 kurohitsugi")

        while voice.is_playing():
            await asyncio.sleep(1)
    except Exception as e:
        await ctx.send(f"иди нахуй {str(e)}")

bot.run(TOKEN)