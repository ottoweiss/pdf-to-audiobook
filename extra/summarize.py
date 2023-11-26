import openai
import json
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Manager


GPT_3 = "gpt-3.5-turbo"
GPT_4 = "gpt-4"
GPT_4_32K = "gpt-4-32k"
GPT_3_16K = "gpt-3.5-turbo-16k"

MODEL_COST = {
    GPT_3 : 0.002,
    GPT_4 : 0.03,
    GPT_4_32K : 0.06,
    GPT_3_16K: 0.003
}


system_prompt = "You are an excellent text summarizer. You are always provided with a chunk of text from a book and the summary of the previous chunk for context."
prompt = "Can you provide a comprehensive summary of the given text? I've provided a summary of the previous chunk for context. The summary should cover all the key points and main ideas presented in the original text, while also condensing the information into a concise and easy-to-understand format. Please ensure that the summary includes relevant details and examples that support the main ideas, while avoiding any unnecessary information or repetition. The length of the summary should be appropriate for the length and complexity of the original text, providing a clear and accurate overview without omitting any important information."

def gpt_summarize(prev_sum: str, text: str):
    prev_sum = "Summary of previous chunk: \"" + prev_sum + "\""
    response = openai.ChatCompletion.create(
        model=GPT_4,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
            {"role": "user", "content": prev_sum},
            {"role": "user", "content": text}
        ],
        temperature=0.74,
        max_tokens=1000,
    )
    answer = response["choices"][0]["message"]["content"]
    print(answer)
    return answer

def get_summaries(sections_json, section_summaries_json):
    with open(sections_json, "r") as fj:
        sections: dict = json.load(fj)
    section_summaries = {}
    with open(section_summaries_json, "r") as fj:
        section_summaries: dict[str, list] = json.load(fj)
    num_chunks_seen = 0
    num_chunks =0
    for section, chunks in tqdm(sections.items()):
        num_chunks += 1

    for section, chunks in tqdm(sections.items()):
        if section in section_summaries:
            if len(section_summaries[section]) < len(chunks):
                chunks = chunks[len(section_summaries[section]) + 1:]
                previous_chunk = section_summaries[section][-1]
            else:
                continue
        else:
            section_summaries[section] = list()
            previous_chunk = "This is the first chunk of a section of this book, so there are no previous chunks."
        for chunk in chunks:
            previous_chunk =  gpt_summarize(previous_chunk, chunk)
            num_chunks_seen += 1
            section_summaries[section].append(previous_chunk)
            if num_chunks_seen % 3 == 0:
                with open("summaries.json", "w") as js:
                    json.dump(section_summaries, js, indent=2)
    with open("summaries.json", "w") as js:
        json.dump(section_summaries, js, indent=2)
    
get_summaries("hw6_rewritten.json", "summaries_6.json")
