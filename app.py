import gradio as gr
import app_whisper_online


def main():

    demo = gr.TabbedInterface([app_whisper_online.create_app()], 
                            ["Real Time ASR demo using whisper streaming project"])

    demo.launch()

if __name__ == "__main__":
    main()