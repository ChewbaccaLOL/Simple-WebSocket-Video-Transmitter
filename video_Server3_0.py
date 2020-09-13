import asyncio,  websockets, cv2, base64

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
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
            gray = cv2.cvtColor(flippedFrame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(flippedFrame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            encoded, buffer = cv2.imencode('.jpg', flippedFrame, encode_param)
            jpg_as_text = str(base64.b64encode(buffer))
            string2 = jpg_as_text[2:-1]
            # print(string2)

            await websocket.send(string2)

        # print(a)
    except websockets.WebSocketException as error:
        print(error)
    except:
        print(a)
        print('nu sho j takoe')



start_server = websockets.serve(video_transmit, "0.0.0.0", 8686)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



video.release()
cv2.destroyAllWindows()
