#!/usr/bin/python
# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# chatbot = ChatBot("Ron Obvious")

# Create a new instance of a ChatBot
chatbot = ChatBot(
    "Liepa Test")


conversation = [
    "Labas",
    "Sveiki!",
    "Kaip sekas?",
    "Puiki diena.",
    "Smagu girdėti",
    "Ačiū.",
    "Prašom."
]

chatbot.set_trainer(ListTrainer)
chatbot.train(conversation)

response = chatbot.get_response("sveika")# does not equal 'Sveiki!''
print(response)# Response after 'Sveiki!' is 'Kaip sekas?'
