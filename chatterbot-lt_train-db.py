#!/usr/bin/python
# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
import os
from chatterbot.corpus import Corpus
from chatterbot.conversation import Statement, Response
from chatterbot import utils

# Enable info level logging
logging.basicConfig(level=logging.INFO)

chatterbot = ChatBot("Training Example",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="./chatterbot-lt_liepa_db.sqlite3",
    language='LTU',)
chatterbot.set_trainer(ChatterBotCorpusTrainer)

chatterbot.train(
    "./chatterbot_corpus/data/lithuanian"
)
