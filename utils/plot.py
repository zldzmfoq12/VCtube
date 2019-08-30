import os 
import matplotlib
from jamo import h2j, j2hcj
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
font_path = 'C:/Windows/Fonts/NanumGothic.ttf'
fontprop = fm.FontProperties(fname=font_path)
matplotlib.use('Agg')
#matplotlib.rc('font', family=font_name)
from text import PAD, EOS
from utils import add_postfix
from text.korean import normalize

def plot(alignment, info, text, isKorean=True):
    char_len, audio_len = alignment.shape # 145, 200

    fig, ax = plt.subplots(figsize=(char_len/5, 5))
    im = ax.imshow(
            alignment.T,
            aspect='auto',
            origin='lower',
            interpolation='none')

    xlabel = 'Encoder timestep'
    ylabel = 'Decoder timestep'

    if info is not None:
        xlabel += '\n{}'.format(info)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if text:
        if isKorean:
            jamo_text = j2hcj(h2j(normalize(text)))
        else:
            jamo_text=text
        pad = [PAD] * (char_len - len(jamo_text) - 1)

        plt.xticks(range(char_len),
                [tok for tok in jamo_text] + [EOS] + pad, fontproperties=fontprop)

    if text is not None:
        while True:
            if text[-1] in [EOS, PAD]:
                text = text[:-1]
            else:
                break
        plt.title(text, fontproperties=fontprop)

    plt.tight_layout()

def plot_alignment(
        alignment, path, info=None, text=None, isKorean=True):

    if text:
        tmp_alignment = alignment[:len(h2j(text)) + 2]

        plot(tmp_alignment, info, text, isKorean)
        plt.savefig(path, format='png')
    else:
        plot(alignment, info, text, isKorean)
        plt.savefig(path, format='png')

    print(" [*] Plot saved: {}".format(path))
