# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from chatterbot.input import InputAdapter
from chatterbot.conversation import Statement
from chatterbot.utils import input_function


from pocketsphinx import Decoder
import sphinxbase
import time
import os
import pyaudio
import thread
import logging
import queue

class LiepaRecognitionAdapter(InputAdapter):

    CHUNK = 4096
    CHANNELS = 1
    FORMAT = pyaudio.paInt16
    RATE = 16000

    def __init__(self, **kwargs):
        super(LiepaRecognitionAdapter, self).__init__(**kwargs)
        self.messageQueue = queue.Queue()
        try:
            thread.start_new_thread( self.process_pocketsphinx, ("Thread-1", 2, self.messageQueue) )
        except:
           print "Error: unable to start thread"


    """
    A simple adapter that allows ChatterBot to
    communicate through the terminal.
    """
    def process_pocketsphinx(self, threadName, someNumber, messageQueue):
        # self.config = self.createConfig("liepa_commands");
        config = Decoder.default_config()
        config.set_string("-fsg".encode('ascii','ignore'), "./resources/liepa_commands.fsg".encode('ascii','ignore'))
        config.set_string('-hmm'.encode('ascii','ignore'), os.path.join("./resources", 'bendrinis').encode('ascii','ignore'))
        config.set_string('-dict'.encode('ascii','ignore'), os.path.join("./resources/", 'liepa-lt-lt.dict').encode('ascii','ignore'))
        config.set_string('-logfn'.encode('ascii','ignore'), '/dev/null'.encode('ascii','ignore'))
        self.logger.info ("[createConfig]---")
        decoder = Decoder(config);

        p = pyaudio.PyAudio()
        pPyAudio = p.open(format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK)
        self.logger.info ("READY....")
        decoder.start_utt()
        cur_vad_state = 0
        #
        while(True):
            data = pPyAudio.read(self.CHUNK)
            time.sleep (0.100)
            decoder.process_raw(data, False, False)
            vad_state = decoder.get_in_speech()
            if vad_state and not cur_vad_state:
                #silence -> speech transition,
                #let user know that we heard
                self.logger.info("Listening...\n")
            if not vad_state and cur_vad_state:
                #speech -> silence transition,
                #time to start new utterance
                pPyAudio.stop_stream()
                decoder.end_utt()
                # Retrieve hypothesis.
                hypothesis = decoder.hyp()
                if hypothesis is not None:
                    hypothesisStr = hypothesis.hypstr.decode(encoding='UTF-8',errors='strict')
                    messageQueue.put(hypothesisStr, False)
                    self.logger.info ('Best hypothesis: '+hypothesis.hypstr.decode(encoding='UTF-8',errors='strict'))
                    time.sleep(5)
                #    Indicate listening for next utterance
                pPyAudio.start_stream()
                decoder.start_utt()
                self.logger.info ("READY....")
                self.logger.info ("[recognized]---")
            cur_vad_state = vad_state
            # self.logger.info("[process_pocketsphinx]----")
        pass



    def process_input(self, *args, **kwargs):
        """
        Read the user's input from the terminal.
        """
        self.logger.info("[process_input]++++")

        # user_input = input_function()
        while True:
            user_input = ""
            try:
                user_input = self.messageQueue.get(True, 3);
            except queue.Empty:
                # Handle empty queue here
                pass
            else:
                self.logger.info("[process_input]---")
                return Statement(user_input)
