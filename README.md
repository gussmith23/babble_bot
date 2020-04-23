# babble_bot

it's that babble boy

[best of.](https://docs.google.com/document/d/1UiTHk2Z7wy-_rXSBy8YJ_N2CqeXsEROLD5NXcvXYd8A/edit?usp=sharing)

## Running

Now using Docker to make life easier!

1. `git clone https://github.com/gussmith23/babble_bot && cd babble_bot`
1. Get a Telegram Bot API Key by making a new bot using Telegram's BotFather.
1. Rename the config example to `babble_bot.cfg` and copy in your API key.
1. Build the Docker image:
   ```bash
   docker build -t babble-bot .
   ```
1. Run the Docker image:
   ```bash
   docker run -it babble-bot
   ```
