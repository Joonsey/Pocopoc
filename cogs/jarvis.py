from discord.ext import commands, tasks
import speech_recognition as sr
import discord
import asyncio
import io
from pydub import AudioSegment
from pydub.utils import mediainfo
import openai
from secret import OPENAI_TOKEN, OPENAI_ORG_ID 
openai.organization = OPENAI_ORG_ID 
openai.api_key = OPENAI_TOKEN


def search_query(prompt: str):
    print("asking gpt: ", prompt)
    result = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{'role': 'system', 'content' : prompt}])

    print("gpt responded: ", result)
    return result.choices[0].message.content

async def finished_callback(sink: discord.sinks.MP4Sink, channel: discord.TextChannel, author : discord.Member,*args):
    recorded_users = [f"<@{user_id}>" for user_id, audio in sink.audio_data.items()]
    audio_data = sink.audio_data[author.id].file

    audio_segment = AudioSegment.from_file(audio_data, format="mp4")
    audio_wav_data = audio_segment.export(format="wav").read()

    r = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(audio_wav_data)) as source:
        audio = r.record(source)
        transcript = r.recognize_google(audio)

    await sink.vc.disconnect()
    await channel.send(
        f"Finished! \n{search_query(transcript)}\n@{author}."
    )

class Jarvis(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.connection = None


    @commands.command()
    async def join(self, ctx: discord.ApplicationContext):
        if ctx.message.author.voice:
            channel = ctx.message.author.voice.channel
            vc = await channel.connect()
            self.connection = vc
            vc.start_recording(
                discord.sinks.MP4Sink(),
                finished_callback,
                ctx.channel,
                ctx.message.author
            )
        await ctx.message.delete()


    @commands.command()
    async def stop(self, ctx: discord.ApplicationContext):
        """Stop recording."""
        self.connection.stop_recording()
        await ctx.message.delete()
