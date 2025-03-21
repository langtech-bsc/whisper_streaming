import gradio as gr
import app_whisper_online_mic
import app_whisper_online


def main():

    demo = gr.TabbedInterface([app_whisper_online_mic.create_app(), app_whisper_online.create_app()], 
                            ["Real Time ASR demo with whisper streaming", "Simulation of Real Time ASR demo with whisper streaming"])

    demo.launch()

if __name__ == "__main__":
    main()