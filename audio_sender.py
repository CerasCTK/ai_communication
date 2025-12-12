import threading

import numpy as np
import sounddevice as sd
import websocket

# WebSocket URL
WS_URL = "ws://localhost:8000/ws/audio/"

# Audio config
SAMPLE_RATE = 16000
CHUNK = 1024

# Create WebSocket object globally
ws = websocket.WebSocket()


def audio_callback(indata, frames, time, status):
    """Send audio chunks through WebSocket."""
    if status:
        print("Microphone error:", status)

    # Use ws.connected (correct for websocket-client)
    if ws.connected:
        pcm = (indata * 32767).astype(np.int16).tobytes()
        try:
            ws.send(pcm, opcode=websocket.ABNF.OPCODE_BINARY)
        except Exception as e:
            print("Send error:", e)
    else:
        print("⚠️ WebSocket not connected yet")


def start_audio_stream():
    """Start live microphone audio streaming."""
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        blocksize=CHUNK,
        callback=audio_callback,
    ):
        print("🎤 Đang thu âm và gửi âm thanh...")
        print("Nhấn Ctrl + C để dừng.")
        threading.Event().wait()  # Keep the thread alive


if __name__ == "__main__":
    print("🔌 Connecting WebSocket to:", WS_URL)

    try:
        ws.connect(WS_URL)
        print("✅ WebSocket connected OK")

        start_audio_stream()

    except KeyboardInterrupt:
        print("\n🛑 User stopped")

    except Exception as e:
        print("❌ Error:", e)

    finally:
        if ws:
            ws.close()
        print("🔒 WebSocket closed")
