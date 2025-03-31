import spaces
import gradio as gr
import whisper_online as wo
import app_whisper_online_mic
import app_whisper_online
import app_utils

# from: https://huggingface.co/ericmattmann/whisperX-endpoint/commit/2ab62e6332db51ccba1d6c1e1c1b46a8ca2fcbd0
import nvidia.cublas.lib
import nvidia.cudnn.lib
import os

os.environ["LD_LIBRARY_PATH"] = (
    os.path.dirname(nvidia.cublas.lib.__file__) + ":" + os.path.dirname(nvidia.cudnn.lib.__file__)
)

@spaces.GPU(duration=60 * 2)
def prepare():
    print("app.py::prepare(): warmup ASR")

    args = app_utils.ARGS()
    # _, _, _, _, _, asr, _ = wo.prepare(args)
    logfile, online, asr = wo.prepare(args)

    wo.asr_warmup(asr)

    return logfile, online

def main():

    logfile, online = prepare()
    
    title="Speech 2 speech translation project demos"
    interface_list = [app_whisper_online_mic.create_app(), app_whisper_online.create_app(logfile, online)]
    tabs_names = ["Real Time ASR demo", "Simulation of Real Time ASR demo"]

    demo = gr.TabbedInterface(interface_list, tabs_names, title = title)

    demo.queue().launch(server_port=8080)

if __name__ == "__main__":
    main()