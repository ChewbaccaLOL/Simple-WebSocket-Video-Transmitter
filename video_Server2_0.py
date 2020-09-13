import asyncio
import random
import websockets
import cv2, time
import base64
import numpy as np
import threading



STATE = {"value": 0}
USERS = set()

connected = set()

async def handler(websocket, path):
    # Register.
    connected.add(websocket)
    try:
        # Implement logic here.
        await asyncio.wait([ws.send("Hello!") for ws in connected])
        await asyncio.sleep(10)
    finally:
        # Unregister.
        connected.remove(websocket)


async def video_transmit(websocket, path):
    camera_port = 0
    video = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)
    globals()['video'] = video
    a = 0
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    connected.add(websocket)
    while True:
        try:
            a += 1
            check, frame = video.read()
            flippedFrame = cv2.flip(frame, 1)
            encoded, buffer = cv2.imencode('.jpg', flippedFrame, encode_param)
            jpg_as_text = str(base64.b64encode(buffer))
            string2 = jpg_as_text[2:-1]
            for ws in connected:
                await ws.send(string2)
                await ws.recv()
            print(a)
        except:
            print('nu sho j takoe')
            connected.remove(websocket)
            # break
        finally:
            connected.remove(websocket)
            pass


start_server = websockets.serve(video_transmit, "127.0.0.1", 8686)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

global video
video.release()
cv2.destroyAllWindows()
