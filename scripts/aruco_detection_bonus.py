import cv2 as cv
from aruco_library import *

# access the camera and start video
vid = cv.VideoCapture(0)

# for saving the video
fourcc = cv.VideoWriter_fourcc(*'MP4V')
out = cv.VideoWriter('SS_1839_Task1_bonus.mp4', fourcc, vid.get(
    cv.CAP_PROP_FPS), (int(vid.get(3)),  int(vid.get(4))))

# check whether the camera was opened or not
if not vid.isOpened():
    print("Camera could not be opened!!")
    exit()

# loop while the user doesn't press esc
print("Press the 'esc' key to close the program and camera.")
while True:
    # read the current frame
    ret, frame = vid.read()

    # check whether the frame was read successfully or not
    if not ret:
        print("Frame could not be read!!")
        break

    # detect aruco markers and mark the frames accordingly with their ids, angles and corresponding corners
    # and then display the changes on camera itself
    Detected_ArUco_Markers = detect_ArUco(frame)
    angle = Calculate_orientation_in_degree(Detected_ArUco_Markers)
    img = mark_ArUco(frame, Detected_ArUco_Markers, angle)
    cv.imshow('frame', img)

    # save to the file
    out.write(img)

    # wait for the user to press the esc key
    k = cv.waitKey(10) & 0xFF
    if k == 27:
        break

# necessary to close the frame windows opened during runtime
cv.destroyAllWindows()
