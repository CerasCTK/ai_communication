from openai import OpenAI
import base64

client = OpenAI(api_key="")

async def process_audio_with_openai(audio_bytes):

    audio_b64 = base64.b64encode(audio_bytes).decode()

    response = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        messages=[
            {"role": "system", "content": "You are an English teacher."},
            {"role": "user", "content": [
                {"type": "input_audio", "input_audio": audio_b64}
            ]}
        ]
    )

    return response.choices[0].message.content
