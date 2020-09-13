import asyncio
import datetime
import random
import websockets
import cv2, time
import base64
import numpy as np
import io


async def video_transmit(websocket, path):
    camera_port = 0

    video = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)
    globals()['video'] = video
    a = 0
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    while True:
        try:
            a +=1
            check, frame = video.read()

            # print(check)
            # print(frame)

            # bytestring = cv2.imencode('.jpg', flippedFrame, )[1].tostring()
            # image = io.BytesIO(flippedFrame)
            # print(image)
            # image = np.load(image,  allow_pickle=True)
            # image = image
            # bytestring = cv2.imencode('.jpg', flippedFrame, encode_param)[1].tostring()

            flippedFrame = cv2.flip(frame, 1)
            encoded, buffer = cv2.imencode('.jpg', flippedFrame, encode_param)
            jpg_as_text = str(base64.b64encode(buffer))
            string2 = jpg_as_text[2:-1]

            # image = base64.b64encode(flippedFrame)

            # print(string2)
            await websocket.send(string2)
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # cv2.imshow("Capturing", flippedFrame)

            # cv2.waitKey(0)
            # key = cv2.waitKey(1)

            # if key == ord('q'):
            #

            print(a)
            # now = datetime.datetime.utcnow().isoformat() + "Z"
            # await websocket.send(now)
            # await asyncio.sleep(random.random() * 3)
        except:
            print('nu sho j takoe')



start_server = websockets.serve(video_transmit, "127.0.0.1", 8686)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

# camera_port = 0
# video = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)
# a = 0
#
# while True:
#     a = a + 1
#
#     check, frame = video.read()
#
#     print(check)
#     print(frame)
#
#     flippedFrame = cv2.flip(frame, 1)
#
#     # image = io.BytesIO(flippedFrame)
#     # image = np.load(image)
#     # image = base64.b64encode(image)
#
#     bytestring = cv2.imencode('.jpg', flippedFrame)[1].tostring()
#     print(bytestring)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     # cv2.imshow("Capturing", flippedFrame)
#
#     # cv2.waitKey(0)
#     key = cv2.waitKey(1)
#
#     if key == ord('q'):
#         break
#
# print(a)


global video
video.release()
cv2.destroyAllWindows()
