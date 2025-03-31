import spaces
import whisper_online as wo
import torch
import time
import app_utils
import os
import gradio as gr

online = None
logfile = None
args = app_utils.ARGS()

@spaces.GPU
def transcribe(file=None):

    if file is not None:
        audio_path = file
        print(f"processing audio file: {audio_path}")
    else:
        return "You must either provide a mic recording or a file"

    print(f"app_whisper_online.py - transcribe - torch.cuda.is_available(): {torch.cuda.is_available()}")
    if 'LD_LIBRARY_PATH' in os.environ:
        print(f"app_whisper_online.py - transcribe - LD_LIBRARY_PATH: {os.environ['LD_LIBRARY_PATH']}")
    else:
        print(f"app_whisper_online.py - transcribe - LD_LIBRARY_PATH: not found")

    global online, logfile

    out_lines = []
    # logfile, audio_path, duration, online, min_chunk, asr, out_lines = wo.prepare(args)
    # logfile, online, asr, out_lines = wo.prepare(args)
    duration = wo.get_audio_duration(audio_path)
    min_chunk = wo.get_min_chunk(args)
    # wo.asr_warmup(asr)

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
            yield "\n".join([str(item) for item in out_lines])

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
        yield "\n".join([str(item) for item in out_lines])

    out_lines.append(["### DONE ###"])
    yield "\n".join([str(item) for item in out_lines])

    online.init()

def create_app(_logfile, _online):

    global logfile, online
    online = _online
    logfile = _logfile

    with gr.Blocks() as demo:
        gr.Markdown(
            """
            # Real Time ASR simulation demo
            Upload a file and transcribe its speech to text
            """
        )
        gr.Interface(
            fn=transcribe,
            inputs=[
                gr.Audio(sources="upload", type="filepath"),
            ],
            outputs="text",
            live=True,
        )

    return demo

def main():
    
    app = create_app()
    app.queue().launch(debug=True)
    
if __name__ == "__main__":
    main()