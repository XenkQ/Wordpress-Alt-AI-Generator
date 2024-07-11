# Wordpress-images-alt-AI-generator

## Generate alt image text with AI and insert it to wordpress images
When you manage wordpress website and people are adding images without alt text that can be flustrating so I created this project to fill alt text in all images in wordpress media for accessibility purposes. I want to create alt text using local models for free. Currently app is connecting to mysql database not by wordpress api, but I will add that option.

## How to use this script
1. Download [ollama](https://github.com/ollama/ollama/tree/main) for running language models locally.
2. Pull language models: [llava](https://ollama.com/library/llava) for creating text from image and [bielik](https://ollama.com/mwiewior/bielik) for polish translation.
3. Add extension [alt-manager](https://pl.wordpress.org/plugins/alt-manager/) to wordpress that can update images after alt text has changed.
4. In extension options set all images setting to **"Image Alt"**.
5. Fill your desired connection method credentials in "credentials.json" file.
6. Open console and run python script **py main.py**
