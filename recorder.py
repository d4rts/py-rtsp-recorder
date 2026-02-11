import subprocess
import time
import os
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

RTSP_URL = os.getenv("RTSP_URL")
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "recordings"))
RECORD_DAYS = int(os.getenv("RECORD_DAYS", 3))
SEGMENT_SECONDS = int(os.getenv("SEGMENT_SECONDS", 600))
OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT", "mp4")

if not RTSP_URL:
    raise ValueError("RTSP_URL manquant dans le .env")

DURATION = timedelta(days=RECORD_DAYS)


def run_ffmpeg(output_pattern: str):
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "warning",
        "-rtsp_transport", "tcp",
        "-fflags", "+genpts",
        "-i", RTSP_URL,
        "-c", "copy",
        "-f", "segment",
        "-segment_time", str(SEGMENT_SECONDS),
        "-reset_timestamps", "1",
        "-strftime", "1",
        output_pattern,
    ]
    return subprocess.Popen(cmd)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    end_time = datetime.now() + DURATION

    output_pattern = str(
        OUTPUT_DIR / f"cam_%Y-%m-%d_%H-%M-%S.{OUTPUT_FORMAT}"
    )

    proc = None
    backoff = 2

    while datetime.now() < end_time:
        if proc is None or proc.poll() is not None:
            print("Lancement ffmpeg...")
            proc = run_ffmpeg(output_pattern)
            backoff = 2

        time.sleep(2)

        if proc.poll() is not None:
            print("Flux coupé, tentative de reconnexion...")
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)

    if proc and proc.poll() is None:
        proc.terminate()
        proc.wait()


if __name__ == "__main__":
    main()
