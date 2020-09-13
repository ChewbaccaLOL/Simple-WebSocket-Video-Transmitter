import asyncio,  websockets, cv2, base64

camera_port = 0
video = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)
a = 0
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

async def video_transmit(websocket, path):
    try:
        while True:
            global a, video, encode_param
            a +=1
            check, frame = video.read()
            flippedFrame = cv2.flip(frame, 1)

            encoded, buffer = cv2.imencode('.jpg', flippedFrame, encode_param)
            jpg_as_text = str(base64.b64encode(buffer))
            string2 = jpg_as_text[2:-1]

            await websocket.send(string2)

    except websockets.WebSocketException as error:
        print(error)
    except:
        print(a)
        print('nu sho j takoe')



start_server = websockets.serve(video_transmit, "127.0.0.1", 8888)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



video.release()
cv2.destroyAllWindows()
