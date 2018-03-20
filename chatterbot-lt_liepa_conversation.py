# -*- coding: utf-8 -*-
from chatterbot import ChatBot



# Uncomment the following lines to enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)


# Create a new instance of a ChatBot
bot = ChatBot(
    "Terminal",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="./liepa_db2.sqlite3",
    language='LTU',
    logic_adapters=[
        {'import_path': "chatterbot.logic.BestMatch"},
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'Atsiprašau nesupratau. Gal galite pakartoti?'
        }
    ],
    input_adapter="input.LiepaRecognitionAdapter",
    output_adapter="output.LiepaTtsAdapter",

    # preprocessors=[
    #     'chatterbot.preprocessors.clean_whitespace'
    # ]
)

print("Type something to begin...")

# The following loop will execute each time the user enters input
while True:
    try:
        # We pass None to this method because the parameter
        # is not used by the TerminalAdapter
        bot_input = bot.get_response(None)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
