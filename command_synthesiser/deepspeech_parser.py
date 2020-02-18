from deepspeech import Model
import numpy as np
import pyaudio
from threading import Thread
from array import array
from scipy.io import wavfile as wav
import wave, os, glob

try:
    from shhlex import quote
except ImportError:
    from pipes import quote



def do_the_work(ds,inp,rate):
    spoken = ds.stt(inp)
    #print (spoken)
    # Store the commands in a text file
    return spoken
    
def live_recognizer():
# load model
  # Beam width used in the CTC decoder when building candidate transcriptions
  BEAM_WIDTH = 500

# The alpha hyperparameter of the CTC decoder. Language Model weight
  LM_WEIGHT = 1.50

# Valid word insertion weight. This is used to lessen the word insertion penalty
# when the inserted word is part of the vocabulary
  VALID_WORD_COUNT_WEIGHT = 2.10

# These constants are tied to the shape of the graph used (changing them changes
# the geometry of the first layer), so make sure you use the same constants that
# were used during training
  LM_ALPHA = 0.75
  LM_BETA = 1.85
# Number of MFCC features to use
  N_FEATURES = 26

# Size of the context window used for producing timesteps in the input vector
  N_CONTEXT = 9

  FORMAT = pyaudio.paInt16
  CHANNELS = 1
  RATE = 16000
  CHUNK = 1024
  RECORD_SECONDS = 5
  ds = Model('models/output_graph.pbmm', BEAM_WIDTH)
  ds.enableDecoderWithLM('models/lm.binary', 'models/trie', LM_ALPHA, LM_BETA)

# initialize recording
  audio = pyaudio.PyAudio()
  stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)


  print("Give Command(Press Ctrl+c to stop ):")
  while True:    
# record audio
    frames = [] 
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
      data = stream.read(CHUNK)
       #print (data)
      data_chunk = array('h', data)
       #print (data_chunk)
      vol = max(data_chunk)
      if (vol >= 500):
          frames.append(data)
	#recording finished
    speech_input = np.frombuffer(b''.join(frames), np.int16)
    text=do_the_work(ds,speech_input,RATE)
    #print ("Inside the NLP engine:",text)
    return text
def test_wavs(filename):
    ds = Model('models/output_graph.pbmm',500)
    #zero = []
    #path = '/home/raghu/Desktop/kiki/command_synthesiser/'
    #for filename in glob.glob(os.path.join(path, '*.wav')):
    fs,data = wav.read(filename)
    processed_data = ds.stt(data)
    return processed_data
  #print (data)
