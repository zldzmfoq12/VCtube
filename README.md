Audio, Caption Crawler and Processor -TTS Data Generator-
=====================================


##### Downloads and processes the audios and captions(subtitles) from Youtube videos for Speech AI
##### Generates audio datas from Youtube for TTS



Requirements
-------------

* Currently requires python >= 3.6
* FFmpeg

To Use
--------

      from vctube import VCtube

      playlist_name=""
      playlist_url = ""

      vc = VCtube(playlist_name, playlist_url)

      vc.download_audio()    #download audios from youtube

      vc.download_caption()  #download captions from youtube

      vc.audio_split()       #split with caption


Results
----------
   
      datasets
        |- playlist name
            |- metadata.csv
            |- alignment.json
            |- wavs
                 ├── 1.wav
                 ├── 2.wav
                 ├── 3.wav
                 └── ...
  
   
   and `metadata.csv` should look like:

    {
        "0001.wav|그래서 사람들도 날 핍이라고 불렀다.",
        "0002.wav|크리스마스 덕분에 부엌에 먹을게 가득했다.",
        "0003.wav|조가 자신이 그 사람이라고 나섰다.",
        ...
    }
    
   and `alignment.json` should look like:

    {
        "./datasets/playlist name/wavs/0001.wav": "그래서 사람들도 날 핍이라고 불렀다.",
        "./datasets/playlist name/wavs/0002.wav": "크리스마스 덕분에 부엌에 먹을게 가득했다.",
        "./datasets/playlist name/wavs/0003.wav": "조가 자신이 그 사람이라고 나섰다.",
        ...
    }

