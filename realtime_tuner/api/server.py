from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
import asyncio
import os
import json

# Import từ các module của cậu (đảm bảo đúng đường dẫn package)
from realtime_tuner.audio.audio_stream import start_stream, get_frame
from realtime_tuner.core.pitch import detect_pitch
from realtime_tuner.core.note_mapper import freq_to_note
from realtime_tuner.core.comparator import compare_pitch

app = FastAPI()

# Khởi tạo luồng âm thanh
stream = start_stream()


@app.get("/")
async def get_index():
    # Trả về giao diện HTML
    return FileResponse('realtime_tuner/static/index.html', media_type='text/html')

@app.post("/tune")
def tune(audio: list, target: str):

    import numpy as np

    signal = np.array(audio)

    pitch = detect_pitch(signal)

    if pitch is None:
        return {"status": "no pitch"}

    result = compare_pitch(pitch, target)

    return result

@app.websocket("/ws/tuner")
async def tuner(ws: WebSocket):

    await ws.accept()

    target_note = "G3"

    try:

        while True:

            # nhận message frontend (non blocking)
            try:

                msg = await asyncio.wait_for(ws.receive_text(), timeout=0.001)
                data = json.loads(msg)

                if data["type"] == "target":
                    target_note = data["note"]

            except asyncio.TimeoutError:
                pass

            frame = get_frame()

            if frame is None:
                await asyncio.sleep(0.005)
                continue

            pitch = detect_pitch(frame)
            # print("pitch:", pitch)
            if frame is None:
                continue

            if pitch is None:
                # pitch = 196.0
                continue

            note, cents = freq_to_note(pitch)

            cents_target, status = compare_pitch(pitch, target_note)

            await ws.send_json({

                "note": note,
                "hz": pitch,
                "cents": cents,
                "target": target_note,
                "target_cents": cents_target,
                "status": status

            })

            await asyncio.sleep(0.01)

    except WebSocketDisconnect:

        print("Client disconnected")
