'''
Created on Mar 20, 2018
@author: mindaugas greibus
'''

from pocketsphinx import Decoder
import sphinxbase
import time
import os
import pyaudio
import subprocess

class ChatterBotSphinx(object):
    CHUNK = 4096
    CHANNELS = 1
    FORMAT = pyaudio.paInt16
    RATE = 16000
    MODELDIR = "./liepa_akustinis_modelis"

    def __init__(self):
        '''
        Constructor
        '''
        print ("[__init__]+++")
        self.config = self.createConfig("liepa_commands");
        self.decoder = Decoder(self.config);
        print ("[__init__] created decoder")

        print ("[__init__]---")

        p = pyaudio.PyAudio()

        self.stream = p.open(format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK)
        #Indicate listening for next utterance
        print ("READY....")



    def createConfig(self,pGramma):
        print ("[createConfig]+++")
        config = Decoder.default_config()
        config.set_string('-hmm', os.path.join(self.MODELDIR, 'bendrinis'))
        config.set_string('-fsg', os.path.join("./resources/", pGramma+'.fsg'))
        #config.set_string('-jsgf', os.path.join("../resource/", pGramma+'.gram'))
        config.set_string('-dict', os.path.join("./resources/", 'liepa-lt-lt.dict'))
        config.set_string('-logfn', '/dev/null')
        print ("[createConfig]---")
        return config;


    def recognized(self, pStream, pDecoder):
        print ("[recognized]+++")
        pStream.stop_stream()
        pDecoder.end_utt()
        # Retrieve hypothesis.
        hypothesis = pDecoder.hyp()
        if hypothesis is not None:
            print ('Best hypothesis: ', hypothesis.prob, hypothesis.best_score, hypothesis.hypstr)

        time.sleep (0.100)
        #Indicate listening for next utterance
        pStream.start_stream()
        pDecoder.start_utt()
        print ("READY....")
        print ("[recognized]---")
        return


    def run(self):
        '''
        Executor
        '''
        print("* start recording")
        self.decoder.start_utt()
        cur_vad_state = 0
        while True:
            data = self.stream.read(self.CHUNK)
            time.sleep (0.100)
            #frames.append(data)
            self.decoder.process_raw(data, False, False)
            vad_state = self.decoder.get_in_speech()
            if vad_state and not cur_vad_state:
                #silence -> speech transition,
                #let user know that we heard
                print("Listening...\n")
            if not vad_state and cur_vad_state:
                #speech -> silence transition,
                #time to start new utterance
                self.recognized(self.stream,self.decoder);
                # if aiContext.state == aiContext.STATE_THANKS:
                #     break
            cur_vad_state = vad_state


if __name__ == "__main__":
    sphinx = ContinuousPocketsphinx();
    sphinx.run()
