from whisper_online import *
import librosa
import datetime
import spaces
import torch

# src_lan = "en"  # source language
# tgt_lan = "en"  # target language  -- same as source for ASR, "en" if translate task is used

asr = FasterWhisperASR("ca", "large-v2")  # loads and wraps Whisper model
# set options:
# asr.set_translate_task()  # it will translate from lan into English
# asr.use_vad()  # set using VAD
logger.info("(logger) ASR model loaded")
print("(print) ASR model loaded")

online = OnlineASRProcessor(asr)  # create processing object with default buffer trimming option
logger.info("(logger) OnlineASRProcessor loaded")
print("(print) OnlineASRProcessor loaded")

# while audio_has_not_ended:   # processing loop:
# 	a = # receive new audio chunk (and e.g. wait for min_chunk_size seconds first, ...)
# 	online.insert_audio_chunk(a)
# 	o = online.process_iter()
# 	print(o) # do something with current partial output
# # at the end of this audio processing
# o = online.finish()
# print(o)  # do something with the last output


# online.init()  # refresh if you're going to re-use the object for the next audio

###############################################################

import gradio as gr

@spaces.GPU
def transcribe(stream, new_chunk):

    print(f"transcribe cuda available: {torch.cuda.is_available()}")

    sr, y = new_chunk
    print(f"transcribe() called: {sr}")


    # Convert to mono if stereo
    if y.ndim > 1:
        y = y.mean(axis=1)

    y = y.astype(np.float32)
    # y /= np.max(np.abs(y))

    print(type(y))
    if sr != 16000:
            print(f"resampling() called")
            y = librosa.resample(y=y, orig_sr=sr, target_sr=16000)

    #print(f"[app ASR RT] info: sr={sr}\tlen(y)={len(y)}")
    # 

    if stream is not None:
        stream = np.concatenate([stream, y])
    else:
        stream = y

    # online.insert_audio_chunk(stream)
    # o = online.process_iter()

    return stream, datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") # o

def create_app():

    with gr.Blocks() as demo:
        gr.Markdown(
            """
            # Real Time ASR demo
            Speak and transcribe your speech
            """
        )
        gr.Interface(
            transcribe,
            ["state", gr.Audio(sources=["microphone"], streaming=True)],
            ["state", "text"],
            live=True,
        )

    return demo

def main():
    
    app = create_app()
    app.launch(debug=True)

    
if __name__ == "__main__":
    main()