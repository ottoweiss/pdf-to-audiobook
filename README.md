*If anyone would like to build it out—like adding GPT-4 as a possible cleaner or fixing anything—feel free to contribute and submit pull requests.*

Download or upload a PDF and convert it into a professional-grade audiobook. Should work for book PDFs and most others, but some PDFs with unusual formatting may require you to change the cleaning prompt.

I made this for myself but thought I should share it because I've found it useful; maybe it could help people with vision and reading difficulties.


## Step 1
After cloning repository, navigate to root and install requirements.

```
pip install -r requirements.txt
```

## Step 2

- **OpenAI API Key**: Enter your OpenAI API key into `config.py`.

*Can also alter cleaning prompt, see config.py*

## Step 3
Place desired pdf in root of folder.

## Step 4
Place desired pdf in root of folder.

Run main.py and follow prompts:

```
python main.py
```
