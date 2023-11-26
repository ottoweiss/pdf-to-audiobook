from src.audiobook import get_audiobook
from src.clean_pdf import get_rewrite
from src.pdf_to_json import extract_text_from_pdf
import os
import time
from colorama import Fore, Style

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
        pdf_file_q = input_q("Have you added the pdf file to this folder? (y/[n]): ")
        if pdf_file_q.lower() == "y":
            correct_pdf_file_name = False
            while not correct_pdf_file_name:
                pdf_file_name = input_q("Enter pdf file name: ")
                if os.path.exists(pdf_file_name):
                    correct_pdf_file_name = True
                else:
                    print_error("File not in folder. Please try again.")
            file_included = True
        else:
            print_info("\nDownload File Here then Add to Folder: https://singlelogin.re/\n")
            time.sleep(3)
    
    correct_page_range = False
    while not correct_page_range:
        try:
            page_start = int(input_q("What page should the audiobook start?: ").strip())
            page_end = int(input_q("What page should the audiobook end?: ").strip())
            title = input_q("Enter Your Book Title: ").strip()
            cost, e_time = extract_text_from_pdf(pdf_file_name, {title: (page_start, page_end)})
            correct_page_range = True
        except ValueError:
            print_error("Please provide a valid integer for page numbers.")
        except Exception as e:
            print_error(f"Error while converting pdf: {e}")

    print_info(f"ESTIMATED COST FOR CONVERSION: {cost}")
    print_info(f"ESTIMATED TIME FOR CONVERSION: {e_time}")
    print_info("CLEANING TEXT with GPT...\n")
    json_file = pdf_file_name.replace(".pdf", ".json")
    output_json = json_file.replace(".json", "-cleaned.json")
    get_rewrite(json_file, output_json)
    voices = {"alloy", "echo", "fable", "onyx", "nova", "shimmer"}

    correct_audio_configuration = False
    while not correct_audio_configuration:
        voice = input_q("Choose a voice [alloy, echo, fable, onyx, nova, shimmer]: ").strip()
        if voice in voices:
            speed = input_q("Audio speed (0.1-3.0, recommend 1.0): ").strip()
            try:
                speed = float(speed)
                if 0.1 <= speed <= 3.0:
                    print_info("CONVERTING Text to Audiobook with GPT...\n")
                    get_audiobook(output_json, title, voice, speed)
                    correct_audio_configuration = True
                    print_success(f"COMPLETE - Audiobook mp3 found in folder: {title}")
                else:
                    print_error("Speed must be between 0.1 and 3.0.")
            except ValueError:
                print_error("Please provide a valid speed.")
        else:
            print_error("Please choose a valid voice from the list.")
