
class ARGS():
    audio_path = None
    min_chunk_size = 1.0
    model = "large-v1"
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