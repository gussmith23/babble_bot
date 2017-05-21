# babble_bot

it's that babble boy

[best of.](https://docs.google.com/document/d/1UiTHk2Z7wy-_rXSBy8YJ_N2CqeXsEROLD5NXcvXYd8A/edit?usp=sharing)

Uses Python 3.

You must rename the config to `babble_bot.cfg` and insert working fields. This means you must

1. Get an API key for a new bot using Telegram's "BotFather"
2. Get an API key for Microsoft's Azure Cognitive Services Text Translate API (which does 2M translations free per month). [Instructions here.](https://www.microsoft.com/en-us/translator/getstarted.aspx)

## Dependencies:
- microsofttranslator - [newearthmartin's fork, specifically the develop branch.](https://github.com/newearthmartin/Microsoft-Translator-Python-API/tree/develop). Microsoft moved their translation service to Azure, and the original microsofttranslator owners did not update their library, so at the time of writing I'm using newearthmartin's patch. Clone newearthmartin's repo, switch to the develop branch, and run `sudo python setup.py install`.
- pyTelegramBotAPI 
- configparser
