*If anyone would like to build it out—like adding GPT-4 as a possible cleaner or fixing anything—feel free to contribute and submit pull requests.*

Simple way to convert PDF into a professional-grade audiobook by using GPT and OpenAI's text-to-speech. Should work for book PDFs and most others, but some PDFs with unusual formatting may require you to change the cleaning prompt.

I made this for myself but thought I should share it because I've found it useful; maybe it could help people with vision and reading difficulties.


### Steps
1. After cloning repository, navigate to root and install requirements.

```
pip install -r requirements.txt
```


2. Enter your OpenAI API key into `config.py`.
*Can also alter cleaning prompt, see config.py*

3. Place desired pdf in root of folder.


4. Run main.py and follow prompts:

```
python main.py
```
