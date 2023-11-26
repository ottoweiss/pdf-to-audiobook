import json
from tqdm import tqdm
from config import KEY
from openai import OpenAI
import concurrent.futures
import os

def gpt_rewrite(text: str):
    system_prompt_rewrite = "You are an AI that rewrites text extracted from pdfs of books. You write exactly what the book has in the main body of text, but you remove all typos, footnotes, headers, and page numbers. You always respond with the exact cleaned text of the main body of the book excerpt."
    text = "Please clean the following text, removing footnotes, typos, headers (ex. \'\nChapter 1 \n29\'), page numbers, and unneccesary 'newline' characters. Respond with the exact cleaned text: \n" + text
    client = OpenAI(api_key=KEY)
    response = client.chat.completions.create(model="gpt-3.5-turbo-1106",temperature=0.74,
    max_tokens=2000,
    messages=[
    {"role": "system", "content": system_prompt_rewrite},
    {"role": "user", "content": text}]

    )
    answer = response.choices[0].message.content
    return answer

def finalize_list(text_dict: dict[int, list[str]]) -> list[list[str]]:
    cores = os.cpu_count() - 1
    final_list: list[list[str]] = list()
    temp_list = []
    count = 0
    for sub_list in text_dict.values():
        for item in sub_list:
            temp_list.append(item)
            if count == cores:
                final_list.append(temp_list)
                temp_list = []
                count = 0
            else:
                count += 1
    final_list.append(temp_list)
    return final_list


def get_rewrite(text_json: str, output_json: str):
    with open(text_json, "r") as fj:
        text_json: dict[str, list] = json.load(fj)
    if not os.path.exists(output_json):
        with open(output_json, "w") as fj:
            json.dump({}, fj)
    with open(output_json, "r") as fj:
        current_texts: dict[str, list] = json.load(fj)
        if isinstance(current_texts, list):
            current_texts = {}
    new_texts_json = {}
    for section, chunks in tqdm(text_json.items(), total=len(text_json.keys())):
        if section in current_texts:
            new_texts_json[section] = current_texts[section]
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1) as executor:
                new_chunks = list(executor.map(gpt_rewrite, chunks))
            new_texts_json[section] = new_chunks
        with open(output_json, "w") as js:
            json.dump(new_texts_json, js, indent=2)
    with open(output_json, "w") as js:
        final_reformatted_list = finalize_list(new_texts_json)
        json.dump(final_reformatted_list, js, indent=2)