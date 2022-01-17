import cv2
import time
import pickle
import numpy as np
import pyttsx3
import mediapipe as mp
import ray

ray.init()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
drawing_styles = mp.solutions.drawing_styles

mod = pickle.load(open('D:/Studies/Projects/Sign Language Detection/XGBoost.sav', 'rb'))
le = pickle.load(open('D:/Studies/Projects/Sign Language Detection/XEncoder1.sav', 'rb'))
word = ' '

@ray.remote(num_cpus = 0.5)
def play_voice(mytext):
    
    converter = pyttsx3.init()
    converter.setProperty('rate', 120)
    # Set volume 0-1
    converter.setProperty('volume', 1.0)
    converter.say(mytext)
    converter.runAndWait()


def detect_hand():

    global word
    cap = cv2.VideoCapture(0)
    prev = time.time()
    with mp_hands.Hands(min_detection_confidence=0.55, min_tracking_confidence=0.65) as hands:
        while cap.isOpened():
            curr = time.time()
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            #image = cv2.resize(image,(600,600),interpolation=cv2.INTER_CUBIC)
            if results.multi_hand_landmarks:
                lst = []
                for coords in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, coords, mp.solutions.hands.HAND_CONNECTIONS,
                        drawing_styles.get_default_hand_landmarks_style(),
                        drawing_styles.get_default_hand_connections_style())
                for crd in coords.landmark:
                    lst.append(crd.x)
                    lst.append(crd.y)
                    lst.append(crd.z)
                lst = np.asarray(lst).reshape(1,-1)
                if (curr-prev) >= 4:
                    prev = time.time()
                    txt = predict.remote(lst)
                    txt = ray.get(txt)
                    if txt=='del': word = word[:-1]
                    elif txt == 'space': word += ' '
                    else: word+=txt
                    print(f'{txt} ---- {word}')
                    play_voice.remote(word)
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()


@ray.remote(num_cpus = 0.5)
def predict(coords):

    tmp = mod.predict(coords)
    txt = str(le.inverse_transform(tmp)).strip("'][")
    return txt

if __name__ == '__main__':
    detect_hand()
