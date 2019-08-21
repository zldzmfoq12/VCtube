Voice synthesizer for korean using Deep-voice2
====================================================================
- [Deep Voice 2: Multi-Speaker Neural Text-to-Speech](https://arxiv.org/abs/1705.08947)

## Prerequisites

- Python 3.6+
- FFmpeg
- [Tensorflow 1.8](https://www.tensorflow.org/install/, "tensorflow-gpu would be better" https://www.tensorflow.org/install/gpu)
- youtube-dl
- If you don't have any datasets, go to https://www.kaggle.com/zldzmfoq12/korean-voice, https://www.kaggle.com/bryanpark/korean-single-speaker-speech-dataset and download datasets.

## Usage

### 1. Install prerequisites

    pip3 install -r requirements.txt
    python -c "import nltk; nltk.download('punkt')
    
After preparing prerequisites, install tensorflow(or tensorflow-gpu)

### 2-2. Generate Korean datasets

Follow below commands. (explain with `channel1` dataset)

1. Download speech(or video) and text.

       youtube-dl --download-archive downloaded.txt --no-overwrites -ic -o "./datasets/channel1/audio/%(id)s.%(ext)s" --yes-playlist --extract-audio --audio-format wav --audio-quality 0 --socket-timeout 5 "youtube channel url"
       python3 -m caption --base_dir "./datasets/" --channels=channel1,channel2,channel3

2. Segment all audios on silence.

       python3 -m audio.split --audio_pattern "./datasets/channel1/audio/*.wav" --method=pydub

3. Finally, generated numpy files which will be used in training.

       python3 -m datasets.generate_data ./datasets/channel1/alignment.json

Because the automatic generation is extremely naive, the dataset is noisy. However, if you have enough datasets (20+ hours with random initialization or 5+ hours with pretrained model initialization), you can expect an acceptable quality of audio synthesis.

### 2-2. Generate custom datasets

The `datasets` directory should look like:

    datasets
    ├── channel1
    │   ├── alignment.json
    │   └── audio
    │       ├── 1.wav
    │       ├── 2.wav
    │       ├── 3.wav
    │       └── ...
    └── OTHER_DATASET
        ├── alignment.json
        └── audio
            ├── 1.wav
            ├── 2.wav
            ├── 3.wav
            └── ...
   
 and `OTHER_DATASET/alignment.json` should look like:

    {
        "./datasets/OTHER_DATASET/audio/001.wav": "그래서 사람들도 날 핍이라고 불렀다.",
        "./datasets/OTHER_DATASET/audio/002.wav": "크리스마스 덕분에 부엌에 먹을게 가득했다.",
        "./datasets/OTHER_DATASET/audio/003.wav": "조가 자신이 그 사람이라고 나섰다.",
    }
 
 
After you prepare as described, you should genearte preprocessed data with:

    python3 -m datasets.generate_data ./datasets/OTHER_DATASET/alignment.json
    
    
### 3. Train a model

The important hyperparameters for a models are defined in `hparams.py`.


To train a model:

    python3 train.py --data_path=datasets/channel1,datasets/channel2
    python3 train.py --data_path=datasets/channel1,datasets/channel2 --initialize_path=PATH_TO_CHECKPOINT

To restart a training from previous experiments such as `logs/channel1+channel2_2019-07-25_10-35-31`:

    python3 train.py --data_path=datasets/channel3,datasets/channel4 --load_path logs/channel1+channel2_2019-07-25_10-35-31

If you don't have good and enough (10+ hours) dataset, it would be better to use `--initialize_path` to use a well-trained model as initial parameters.

### 4. Synthesize audio

You can train your own models with:

    python3 app.py --load_path logs/channel1+channel2_2019-07-25_10-35-31 --num_speakers=2

or generate audio directly with:

    python3 synthesizer.py --load_path logs/channel1+channel2_2019-07-25_10-35-31 --num_speakers 2 --speaker_id 0 --text "간장 공장 공장장은 강 공장장이다"
