*If anyone would like to build it out—like adding more cleaning configurations or fixing anything—feel free to contribute and submit pull requests.*

A simple PDF conversion to a professional-grade audiobook with OpenAI's text to speech models. Should work for book PDFs and most others, but some PDFs with unusual formatting may require you to change the cleaning prompt (config.py).

I made this for myself but thought I should share it because I've found it useful; maybe it could help people with vision and reading difficulties.

## Getting Started

### Prerequisites

- **OpenAI API Key**: Enter your OpenAI API key into `config.py`.

*Can also alter cleaning prompt, see config.py*

### Installation
After cloning repository, navigate to root and install requirements.

'''pip install -r requirements.txt'''


Place desired pdf in root of folder.


Run main.py and follow prompts:

'''python main.py'''
