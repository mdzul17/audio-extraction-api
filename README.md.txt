MFCC AUDIO EXTRACTION

====================

Overview
--------

Following API Server is to calculate MFCC value from the given audio file. There are some default values is set:

- sampling_rate = 16000 (16KHz)
- dct_type = 3
- cepstral_coefficients / n_mfcc = 13
- window = hamming
- fmin = 300
- fmax = 8000
- frame_length = 25 (KHz)
- frame_shift = 10 (KHz)
- num_mel_bins = 0

As for frame_length, frame_shit, and num_mel_bins, you can still customize it by fill in the form.
Notice that if you want to still use the default number for these 3 parameters, give it 0 value.

Because the API Server is built in Python flask, it needs flask requirement. For more requirements detailed below.

Requirements
------------

- Flask 1.1.1 or later
- Librosa 0.9.1
- Numpy

How to run:
-----------

For running the API Server, here are the steps:
1. Open windows terminal / cmd
2. Change directory path to webapp folder i.e "cd D:/Project/Machine-learning/webapp"
3. Run app.py file "python app.py"
4. Wait until terminal gives you an url to open the server API. i.e "https://127.0.0.0:5000/"
5. Open web browser and open the given url


How to use:
-----------

Here how to use and get the MFFC's value as the result:

1. Browse your audio file via browse button.
2. There will pop another window to choose your audio file. Click open if you have choose the file.
3. Fill in the form:
	- Frame Length: how long frame length you want for windowing purpose.
	- Frame Shift: how long hop length you want for windowing purpose.
	- Number of Mel Bins: how much mel filter you want for Mel Filtering purpose

As has been explained above, if you wanted to use its default value, fill it with 0

4. Click Process button to start the process
5. After the process is done, the MFCC's value will be shown below. It has n_frame x cepstral_coefficients matrix dimension.