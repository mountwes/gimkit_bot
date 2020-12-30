# gimkit_bot

A bot written in python that plays the educational game Gimkit.

## Dependencies

python3.8

selenium

chrome

[chromedriver](https://chromedriver.chromium.org/)

## Usage

Install dependencies and specify location of chromedriver, i.e.

`"/usr/bin/chromedriver"`

Make `bot.py` executable

`chmod +x bot.py`

Run `bot.py` and specify a game code and name

`./bot.py <code> <name>`

### Docker

Build docker image

`docker build -t gimkit_bot .`

Run docker image

`docker run --rm --name gimkit_bot -e CODE=<code> -e NAME=<name> -it gimkit_bot`