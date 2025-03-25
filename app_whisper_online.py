# from whisper_online import *
import whisper_online as wo
import librosa
import datetime
import spaces
import torch
import sys
import time
import app_utils
import os

    
print(f"torch.cuda.is_available(): {torch.cuda.is_available()}")

# @spaces.GPU
# def prepare(args):
#     logfile, audio_path, duration, online, min_chunk, asr, out_lines = wo.prepare(args)
#     # start, beg = wo.asr_warmup(asr)

#     return logfile, audio_path, duration, online, min_chunk, asr, out_lines

# logfile, audio_path, duration, online, min_chunk, asr, out_lines = prepare()

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
def transcribe(file=None):

    if file is not None:
        audio = file
        print(f"processing audio file: {audio}")
    else:
        return "You must either provide a mic recording or a file"

    print(f"app_whisper_online.py - transcribe - torch.cuda.is_available(): {torch.cuda.is_available()}")
    if 'LD_LIBRARY_PATH' in os.environ:
        print(f"app_whisper_online.py - transcribe - LD_LIBRARY_PATH: {os.environ['LD_LIBRARY_PATH']}")
    else:
        print(f"app_whisper_online.py - transcribe - LD_LIBRARY_PATH: not found")

    args = app_utils.ARGS()
    logfile, audio_path, duration, online, min_chunk, asr, out_lines = wo.prepare(args)
    wo.asr_warmup(asr)

    beg = args.start_at
    start = time.time()-beg
    end = 0
    while True:
        now = time.time() - start
        if now < end+min_chunk:
            time.sleep(min_chunk+end-now)
        end = time.time() - start
        audio = wo.load_audio_chunk(audio_path,beg,end)
        beg = end

        len_before = len(out_lines)
        end, out_lines = wo.online_loop(online, start, end, audio, logfile, out_lines)
        if len(out_lines) != len_before:
            print(out_lines[-1])

        if end >= duration:
            break
    now = None

    o = online.finish()
    out = wo.output_transcript(o, now=now, start = start, logfile = logfile)
    if out != None:
        fields = out.split(" ")
        start_time = float(fields[1])
        end_time = float(fields[2])
        text = " ".join(fields[3:])
        out = {"start_time": start_time, "end_time": end_time, "text": text}
        print(out) 
        out_lines.append(out)

    return "\n".join(out_lines)

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
                gr.Audio(sources="upload", type="filepath"),
            ],
            outputs="text",
            live=True,
            # enable_queue=True
        )

    return demo

def main():
    
    app = create_app()
    app.launch(debug=True)

    
if __name__ == "__main__":
    main()