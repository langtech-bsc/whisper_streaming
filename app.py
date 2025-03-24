import spaces
import gradio as gr
import whisper_online as wo
import app_whisper_online_mic
import app_whisper_online
import app_utils

@spaces.GPU
def prepare():
    print("app.py::prepare(): warmup ASR")

    args = app_utils.ARGS()
    _, _, _, _, _, asr, _ = wo.prepare(args)
    wo.asr_warmup(asr)

prepare()

def main():

    title="Speech 2 speech translation project demos\nwith whisper_streaming"
    interface_list = [app_whisper_online_mic.create_app(), app_whisper_online.create_app()]
    tabs_names = ["Real Time ASR demo", "Simulation of Real Time ASR demo"]

    demo = gr.TabbedInterface(interface_list, tabs_names, title = title)

    demo.launch()

if __name__ == "__main__":
    main()