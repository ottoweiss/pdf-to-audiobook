from audiobook import get_audiobook
from clean_pdf import get_rewrite
from pdf_to_json import extract_text_from_pdf
import os
import time

if __name__ == "__main__":
    print("\n\nControl Q to quit\n\n")
    print("\n\nBefore Continuing, make sure that you have provided your Openai API key in the config.py file.\n\n")
    file_included = False
    while not file_included:
        pdf_file_q = input("Have you added the pdf file to this folder? (y/[n]): ")
        if pdf_file_q == "y":
            correct_pdf_file_name = False
            while not correct_pdf_file_name:
                pdf_file_name = input("Enter pdf file name: ")
                correct_pdf_file_name = os.path.exists(pdf_file_name)
                if not correct_pdf_file_name:
                    print("File not in folder. Please try again.")
            file_included = True
        else:
            print("\nDownload File Here then Add to Folder: https://singlelogin.re/\n\n")
            time.sleep(3)
    
    correct_page_range = False
    while not correct_page_range:
        try:
            page_start = int(input("\n\nWhat page should the audiobook start?: ").strip())
            page_end = int(input("\n\nWhat page should the audiobook end?: ").strip())
            title = input("Enter Your Book Title: ").strip()
        except:
            print("\n\nPlease Provide an integer for starting and ending page number.")
        try:
            cost, e_time = extract_text_from_pdf(pdf_file_name, {title: (page_start, page_end)})
            correct_page_range = True
        except:
            print("\n\nEncountered error while converting pdf. Please make sure that information provided is correct and the page range is valid.")
    print(f"ESTIMATED COST FOR CONVERSION: {cost}")
    print(f"ESTIMATED TIME FOR CONVERSION: {e_time}")
    print("\n\nCLEANING TEXT with GPT...\n\n")
    json_file = pdf_file_name.replace(".pdf", ".json")
    output_json = json_file.replace(".json", "-cleaned.json")
    get_rewrite(json_file, output_json)
    voices = set(["alloy", "echo", "fable", "onyx", "nova", "shimmer"])

    correct_audio_configuration = False
    while not correct_audio_configuration:
        voice = input('''Which voice would you like to use? (See https://platform.openai.com/docs/guides/text-to-speech for examples.) [alloy, echo, fable, onyx, nova, shimmer]: ''').strip()
        if voice in voices:
            speed = input("What speed would you like the audio? (Recommend 1.0 and altering after) [0.1-3.0]: ").strip()
            try:
                speed = float(speed)
            except:
                print("\n\nPlease provide a valid speed from 0.1 to 3.0.\n\n")
        else:
            print("\n\nPlease provide a voice model in the given list.\n\n")
        try:
            print("\n\nCONVERTING Text to Audiobook with GPT...\n\n")
            get_audiobook(output_json, title, voice, speed)
            correct_audio_configuration = True
        except:
            print("ERROR - Please try again.")
    print(f"COMPLETE - see folder with book title for full audiobook mp3.")