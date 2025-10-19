import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import streamlit as st
from cvzone.HandTrackingModule import HandDetector

# Function to perform hand tracking and virtual mouse
def perform_hand_tracking():
    # Streamlit UI
    st.title("The Result of code - Real time Virtual Mouse ")
     # Code of Placeholder for the webcam feed and Mediapipe Hands zith pyGUI .....
# Initialize the webcam
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)
# Webcam resolution
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

# Screen width and height
screenW, screenH = pyautogui.size()

# Frame reduction to make the detection area smaller than the full screen
frameR = 100

# Smoothing values
smoothening = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0

while True:
    # Read the webcam image
    success, img = cap.read()

    # Find the hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points

        # Get the tip of the index and middle fingers
        x1, y1 = lmList1[8][0], lmList1[8][1]  # Index Finger
        x2, y2 = lmList1[12][0], lmList1[12][1]  # Middle Finger

        # Check which fingers are up
        fingers = detector.fingersUp(hand1)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # Adjusted Detection Area (Zoom in)
        xMin, xMax = frameR + 100, wCam - frameR - 100  # Further reduce frame width
        yMin, yMax = frameR + 100, hCam - frameR - 100  # Further reduce frame height
        cv2.rectangle(img, (xMin, yMin), (xMax, yMax), (0, 255, 0), 2)  # Visualize adjusted area

        if fingers[1] == 1 and fingers[2] == 0:
            # Convert Coordinates within the adjusted detection area
            x3 = np.interp(x1, (xMin, xMax), (0, screenW))
            y3 = np.interp(y1, (yMin, yMax), (0, screenH))
            # Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # Move Mouse
            pyautogui.moveTo(screenW - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # Both Index and Middle fingers are up: Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            # Find distance between Index and Middle fingers
            length, _, _ = detector.findDistance((x1, y1), (x2, y2), img)
            if length < 30:  # Experiment with this value depending on your camera and hand size
                cv2.circle(img, ((x1+x2)//2, (y1+y2)//2), 15, (0, 255, 0), cv2.FILLED)
                # Click mouse if distance short
                pyautogui.click()

    # Display the image
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
def main():
    st.sidebar.image("fpos.jpg")  # Adjust the width as needed
     
    activities = ["About","Mouse Tracking"]
    choice = st.sidebar.selectbox("Select Activity", activities)
    if choice == "About":
        st.image("fpo.jpg")  # Adjust the width as needed   
        st.sidebar.markdown(
        """
        **Directed by:**
        - Saber Lahcini
        - Hassan Tamould
        - Nohyla Lahcini
        - Mona Azelmad
       
        **Supervisor:**
        - Prof. Abdelbasset BOUKDIR
        
        **2023-2024**
        """
        )
        
        
        html_temp4 = """
        <div style="border:1px solid;padding:10px">
                                            <h4 style="text-align:center;">
                                           Real-Time Cursor Control using AI: Voice and Gesture
Screen Navigation </h4>
                                            </div>
                                            <br>
                                             """

        st.markdown(html_temp4, unsafe_allow_html=True)
        
    elif choice == "Mouse Tracking":
        perform_hand_tracking()
if __name__ == "__main__":
    main()

