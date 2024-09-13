from src.audiobook import get_audiobook
from src.clean_pdf import get_rewrite
from src.pdf_to_json import extract_text_from_pdf
import os
import time
from colorama import Fore, Style
import inquirer
import sys

def input_q(text):
    print(Fore.YELLOW + text, end="")
    inp = input()
    print(Style.RESET_ALL, end="")
    if inp == ":q":
        exit()
    return inp

def print_info(message):
    print(Fore.CYAN + message + Style.RESET_ALL)

def print_error(message):
    print(Fore.RED + "ERROR: " + message + Style.RESET_ALL)

def print_success(message):
    print(Fore.GREEN + message + Style.RESET_ALL)

if __name__ == "__main__":
    print_info("Enter :q to quit at any time.\n")
    print_info("Before Continuing, ensure your Openai API key is in the config.py file.\n")
    file_included = False
    while not file_included:
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        if not pdf_files:
            print_error("No PDF files found in the current directory.")
            print_info("\nPlease add PDF files to the current directory and try again.\n")
            sys.exit()
        else:
            questions = [
                inquirer.List(
                    'pdf_file_name',
                    message="Select the PDF file",
                    choices=pdf_files,
                ),
            ]
            answers = inquirer.prompt(questions)
            pdf_file_name = answers['pdf_file_name']
            file_included = True

    correct_page_range = False
    while not correct_page_range:
        try:
            page_start = int(input_q("What page should the audiobook start?: ").strip())
            page_end = int(input_q("What page should the audiobook end?: ").strip())
            title = input_q("Enter Your Book Title: ").strip()
            n_cost, e_time, h_cost = extract_text_from_pdf(pdf_file_name, {title: (page_start, page_end)})
            correct_page_range = True
        except ValueError:
            print_error("Please provide a valid integer for page numbers.")
        except Exception as e:
            print_error(f"Error while converting PDF: {e}")
    
    print_info(f"ESTIMATED TIME FOR CONVERSION: {e_time}\n")
    audio_model = ""
    while  audio_model not in ["tts-1-hd", "tts-1"]:
        audio_quality = input_q(f"Would you like normal (cost ~${n_cost}) or high (cost ~${h_cost} audio quality? [n]/h: ").strip()
        if audio_quality == "h":
            audio_model = "tts-1-hd"
        elif audio_quality == "n" or audio_quality == "":
            audio_model = "tts-1"
    
    print_info("CLEANING TEXT with GPT...\n")
    json_file = pdf_file_name.replace(".pdf", ".json")
    output_json = json_file.replace(".json", "-cleaned.json")
    get_rewrite(json_file, output_json)
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    correct_audio_configuration = False
    while not correct_audio_configuration:
        voice_question = [
            inquirer.List(
                'voice',
                message="Choose a voice",
                choices=voices,
            ),
        ]
        voice_answer = inquirer.prompt(voice_question)
        voice = voice_answer['voice']

        speed = input_q("Audio speed (0.1-3.0, recommend 1.0): ").strip()
        try:
            speed = float(speed)
            if 0.1 <= speed <= 3.0:
                print_info("CONVERTING Text to Audiobook with GPT...\n")
                get_audiobook(output_json, title, voice, speed, audio_model)
                correct_audio_configuration = True
                print_success(f"COMPLETE - Audiobook mp3 found in folder: {title}")
            else:
                print_error("Speed must be between 0.1 and 3.0.")
        except ValueError:
            print_error("Please provide a valid speed.")
