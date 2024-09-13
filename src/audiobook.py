import io
from pydub import AudioSegment
import openai
import json
from tqdm import tqdm
from config import KEY
import os
import atexit
from concurrent.futures import ThreadPoolExecutor
import re

def split_audio_into_segments(file_path, mins=119):
    """
    Splits an audio file into segments of a specified maximum length in minutes
    and saves each segment as a new file.

    :param file_path: Path of the input audio file.
    :param mins: Maximum length of each segment in minutes.
    :return: None
    """
    audio = AudioSegment.from_file(file_path, format="mp3")
    max_length_ms = mins * 60 * 1000
    segments = []
    start = 0
    end = max_length_ms
    count = 0

    while start < len(audio):
        end = min(start + max_length_ms, len(audio))
        segment = audio[start:end]
        file_name = f"{file_path}-segment-{count}.mp3"
        segment.export(file_name, format="mp3") 
        segments.append(segment)
        start += max_length_ms
        end += max_length_ms
        count += 1

def split_at_sentence_boundary(text, max_length=4000):
    if len(text) <= max_length:
        return [text]
    else:
        split_point = text.rfind('.', 0, max_length) + 1
        return [text[:split_point]] + split_at_sentence_boundary(text[split_point:], max_length)


def save_full(book_title):
    book_directory = f"{book_title}"
    full_book_file = f"{book_title}/{book_title}_full.mp3"

    combined_audio = AudioSegment.silent(duration=0)
    ordered_files = []
    pattern = re.compile(r'part(\d+)\.mp3')

    for file in os.listdir(book_directory):
        filename = os.fsdecode(file)
        if filename.endswith(".mp3") and filename != os.path.basename(full_book_file):
            match = pattern.search(filename)
            if match:
                order = int(match.group(1))  # Extract the sequence number
                ordered_files.append((order, filename))

    ordered_files.sort(key=lambda x: x[0])
    if len(ordered_files) == 1:
        os.rename(os.path.join(book_directory, ordered_files[0][1]), full_book_file)
        return

    for _, filename in ordered_files:
        file_path = os.path.join(book_directory, filename)
        combined_audio += AudioSegment.from_file(file_path, format="mp3")

    combined_audio.export(full_book_file, format="mp3")

def play_split_and_combine(index, text, voice, speed, model):
    client = openai.OpenAI(api_key=KEY)
    combined_audio = AudioSegment.silent(duration=0)
    segments = split_at_sentence_boundary(text)
    for segment in segments:
        response = client.audio.speech.create(model=model, voice=voice, input=segment, speed=speed)
        byte_stream = io.BytesIO(response.content)
        audio = AudioSegment.from_file(byte_stream, format="mp3")
        combined_audio += audio
    return index, combined_audio

def get_audiobook(json_file, book_title="audiobook", voice="onyx", speed="1.0", model="tts-1"):
    book_directory = f"{book_title}"
    atexit.register(save_full, book_title)

    if not os.path.exists(book_directory):
        os.makedirs(book_directory)

    with open(json_file, "r") as j:
        vals = json.load(j)

    for text_index, text_list in tqdm(enumerate(vals), total=len(vals)):
        audio_section_file = f"{book_directory}/part{text_index}.mp3"
        if not os.path.exists(audio_section_file):
            with ThreadPoolExecutor(max_workers=len(text_list)) as executor:
                futures = [executor.submit(play_split_and_combine, i, text, voice, speed, model) for i, text in enumerate(text_list)]
                combined_audio = AudioSegment.silent(duration=0)
                for future in futures:
                    try:
                        ind, audio = future.result()
                        combined_audio += audio
                    except Exception as e:
                        print(f"Error processing segment {ind}: {e}")
            combined_audio.export(audio_section_file, format="mp3")
    save_full(book_title)
