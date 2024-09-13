KEY = ""

TEXT_CLEANING_SYSTEM_PROMPT = "You are an AI that rewrites text extracted from pdfs of books. You write exactly what the book has in the main body of text, but you remove all typos, footnotes, headers, and page numbers. You always respond with the exact cleaned text of the main body of the book excerpt."
TEXT_CLEANING_PROMPT = "Please clean the following text, removing footnotes, typos, headers (ex. \'\nChapter 1 \n29\'), page numbers, and unneccesary 'newline' characters. Respond with the exact cleaned text: \n"

# Use get_rewrite in src/clean_pdf.py with the two json files to test cleaning prompt (maybe cut to only a few in the non-cleaned text for testing)
