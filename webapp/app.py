
from flask import Flask, request, render_template
from flask_uploads import configure_uploads
import os
import librosa
import json
import numpy as np
import sys
import logging

app = Flask(__name__)
datatest = os.path.join('static', 'datatest')
app.config['UPLOAD_FOLDER'] = datatest


class Loader():
  def __init__ (self):
    self.sample_rate = 16000
  
  def load(self, file_path):
    signal, _ = librosa.load(file_path,
                          sr=self.sample_rate)
    
    return signal
    
class Windowing():
  def __init__ (self):
    self.sample_rate = 16000
  
  def frame_n_hop(self, frame_length = 25, frame_shift = 10):
    samples_per_frame = (frame_length / 1000) * self.sample_rate
    hop_length = (frame_shift / 1000) * self.sample_rate

    return samples_per_frame, hop_length

  def mel_spectogram(self, signal, hop_length, samples_per_frame, mel_filter_args = {}):
    melspectogram = librosa.feature.melspectrogram(signal,
                                  sr=self.sample_rate,
                                  hop_length=hop_length,
                                  n_fft= samples_per_frame,
                                  window="hamming",
                                  **mel_filter_args)

    return melspectogram

  def mel_filter(self, num_mel_bins = 0):
    mel_filter_args = {
    "n_mels": num_mel_bins,
    "fmin": 300,
    "fmax": 8000
  }

    return mel_filter_args

class Extraction:
  def __init__ (self):
    self.n_mfcc = 13
    self.sample_rate = 16000
    self.dct_type = 3

  def extract(self, signal, mel_spectogram):
    mel_spectogram = librosa.power_to_db(mel_spectogram)
    mfccs = librosa.feature.mfcc(signal,
                                n_mfcc=self.n_mfcc,
                                sr=self.sample_rate,
                                S=mel_spectogram,
                                dct_type=self.dct_type)

    return mfccs


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/process', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        if 'audio' not in request.files:
            return 'audio not found'
        upload_audio = request.files['audio']
        upload_audio_path = "static/datatest/" + upload_audio.filename
        upload_audio.save(upload_audio_path)

        signal = loader.load(upload_audio_path)

        input_frame_length = int(request.form.get("frameLength"))
        input_frame_shift = int(request.form.get("frameShift"))
        input_num_mel_bins = int(request.form.get("numMelBins"))

        if input_frame_length == 0 or input_frame_shift == 0:
            if input_frame_length == 0 and input_frame_shift != 0:
                samples_per_frame, hop_length = windowing.frame_n_hop(frame_shift=input_frame_shift)
            elif input_frame_length != 0 and input_frame_shift == 0:
                samples_per_frame, hop_length = windowing.frame_n_hop(frame_length=input_frame_length)
            elif input_frame_length == 0 and input_frame_shift == 0:
                samples_per_frame, hop_length = windowing.frame_n_hop()
        elif input_frame_length != 0 and input_frame_shift != 0:
            samples_per_frame, hop_length = windowing.frame_n_hop(frame_length=input_frame_length,frame_shift=input_frame_shift)
            logging.info(samples_per_frame, hop_length)

        if input_num_mel_bins == 0:
            mel_filter_banks = windowing.mel_filter()
            melspectogram = windowing.mel_spectogram(signal, hop_length=int(round(hop_length)), samples_per_frame=int(round(samples_per_frame)))
            mfccs = extraction.extract(signal, mel_spectogram=melspectogram)
        else:
            mel_filter_banks = windowing.mel_filter(input_num_mel_bins)
            melspectogram = windowing.mel_spectogram(signal, hop_length=int(round(hop_length)), samples_per_frame=int(round(samples_per_frame)),mel_filter_args=mel_filter_banks)
            mfccs = extraction.extract(signal, mel_spectogram=melspectogram)

        #Store it to JSON Format
        mfcc_dict = {}
        mfcc_dict['matrix'] = mfccs.transpose().tolist()

        json.dumps(mfcc_dict)
        
        mfccs = mfccs.transpose()

    return render_template("index.html", mfcc=mfccs)

if __name__ == '__main__':
    loader = Loader()
    windowing = Windowing()
    extraction = Extraction()

    app.run(debug=True)
