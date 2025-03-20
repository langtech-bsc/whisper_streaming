# from whisper_online import *
import whisper_online as wo
import librosa
import datetime
import spaces
import torch
import sys

class ARGS():
    audio_path = None
    min_chunk_size = 1.0
    model = "large-v2"
    model_cache_dir = None
    model_dir = None
    lan = "es"
    task = "transcribe"
    backend = "faster-whisper"
    vac = False
    vac_chunk_size = 0.04
    vad = False
    buffer_trimming = "segment"
    buffer_trimming_sec = 15
    log_level = "DEBUG"
    start_at = 0.0
    offline = False
    comp_unaware = False    
    
args = ARGS()

print(torch.cuda.is_available())

# logfile, audio_path, duration, online, min_chunk, asr, out_lines = wo.prepare(args)
# start, beg = wo.asr_warmup(asr)


#################################################################################################

# src_lan = "en"  # source language
# tgt_lan = "en"  # target language  -- same as source for ASR, "en" if translate task is used

# asr = wo.FasterWhisperASR("ca", "large-v2")  # loads and wraps Whisper model
# # set options:
# # asr.set_translate_task()  # it will translate from lan into English
# # asr.use_vad()  # set using VAD
# logger.info("(logger) ASR model loaded")
# print("(print) ASR model loaded")

# online = wo.OnlineASRProcessor(asr)  # create processing object with default buffer trimming option
# logger.info("(logger) OnlineASRProcessor loaded")
# print("(print) OnlineASRProcessor loaded")

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

# @spaces.GPU
# def transcribe(stream, new_chunk):

#     print(f"transcribe cuda available: {torch.cuda.is_available()}")

#     sr, y = new_chunk
#     print(f"transcribe() called: {sr}")


#     # Convert to mono if stereo
#     if y.ndim > 1:
#         y = y.mean(axis=1)

#     y = y.astype(np.float32)
#     # y /= np.max(np.abs(y))

#     print(type(y))
#     if sr != 16000:
#             print(f"resampling() called")
#             y = librosa.resample(y=y, orig_sr=sr, target_sr=16000)

#     #print(f"[app ASR RT] info: sr={sr}\tlen(y)={len(y)}")
#     # 

#     if stream is not None:
#         stream = np.concatenate([stream, y])
#     else:
#         stream = y

#     # online.insert_audio_chunk(stream)
#     # o = online.process_iter()

#     return stream, datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") # o



@spaces.GPU
def transcribe(mic=None, file=None):

    if mic is not None:
        audio = mic
    elif file is not None:
        audio = file
    else:
        return "You must either provide a mic recording or a file"
    


def create_app():

    with gr.Blocks() as demo:
        gr.Markdown(
            """
            # Real Time ASR demo
            Speak and transcribe your speech
            """
        )
        # gr.Interface(
        #     transcribe,
        #     ["state", gr.Audio(sources=["microphone"], streaming=True)],
        #     ["state", "text"],
        #     live=True,
        # )
        gr.Interface(
            fn=transcribe,
            inputs=[
                gr.Audio(sources="microphone", type="filepath"),
                gr.Audio(sources="upload", type="filepath"),
            ],
            outputs="text",
            live=True,
        )

    return demo

def main():
    
    app = create_app()
    app.launch(debug=True)

    
if __name__ == "__main__":
    main()