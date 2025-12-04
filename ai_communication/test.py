import asyncio
import websockets

async def test_audio():
    uri = "ws://localhost:8000/ws/audio/"

    async with websockets.connect(uri) as ws:
        print("Connected!")

        # load audio
        with open("test_audio.wav", "rb") as f:
            audio_bytes = f.read()

        # send audio bytes
        await ws.send(audio_bytes)

        # wait for AI result
        response = await ws.recv()
        print("Response:", response)

asyncio.run(test_audio())
