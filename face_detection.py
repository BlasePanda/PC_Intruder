import logging
import requests
import threading
import cv2
from deepface import DeepFace
import asyncio
import os
import time

# Set up logging
logging.basicConfig(filename='startup_script.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


TELEGRAM_BOT_TOKEN = "<TELEGRAM TOKEN>"
TELEGRAM_CHAT_ID = "<CHAT ID>"

message = "Someone is on your PC!"
image_filename = "screenshot.png"

# Load VGG-Face model
model = DeepFace.build_model("VGG-Face")


counter = 0
face_match = False
reference_img = cv2.imread("<IMAGE OF YOU>")
camera_detected = False


async def check_camera_detection():
    global camera_detected
    for _ in range(60):
        cap_1 = cv2.VideoCapture(0)
        print("Checking camera...")
        if cap_1.isOpened():
            camera_detected = True
            print("Camera detected!")
            return
        else:
            print(f"Camera 0 not detected. Retrying...")
            cv2.waitKey(1000)
        await asyncio.sleep(1)
    print("Camera not detected. Exiting program.")


def check_face(i):
    global face_match
    try:
        if DeepFace.verify(i, reference_img.copy())["verified"]:
            face_match = True
            return True
        else:
            face_match = False
        logging.debug("Face verification completed.")
    except ValueError:
        face_match = False
        logging.debug("Face verification failed.")


def send_notification_with_screenshot():
    image_path = os.path.abspath(image_filename)
    send_telegram_message_with_photo(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message, image_path)


def send_telegram_message_with_photo(bot_token, chat_id, msg, photo_path):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    files = {"photo": open(photo_path, "rb")}
    params = {"chat_id": chat_id, "caption": msg}
    response = requests.post(url, files=files, params=params)
    if response.status_code != 200:
        print("Error sending message with photo via Telegram.")


def start_face_detection():
    face_m = 0
    global counter
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(check_camera_detection())
    if camera_detected:
        print("Checking..")
        cap = cv2.VideoCapture(0)
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > 10 and face_match is False:
                _, frm = cap.read()
                cv2.imwrite(image_filename, frm)
                send_notification_with_screenshot()
                break
            ret, frame = cap.read()


            if ret:
                if counter % 30 == 0:
                    threading.Thread(target=check_face, args=(frame.copy(),)).start()

                counter += 1
                if face_match:
                    cv2.putText(frame, "MATCH", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                    logging.debug("Face matched.")
                    face_m +=1
                    if face_m > 50:
                        print("Authorized user detected!")
                        break
                else:
                    cv2.putText(frame, "NO MATCH", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                    logging.debug("Face not matched.")
#commented out beacuse it may cause issues with script
#                cv2.imshow("video", frame)
#
            #key = cv2.waitKey(1)
            #if key == ord("q"):
            #    break

    cap.release()
    cv2.destroyAllWindows()




face_detection_thread = threading.Thread(target=start_face_detection)
face_detection_thread.start()




