#!/usr/bin/env python3
############## Task1.1 - ArUco Detection ##############

import numpy as np
import cv2
import cv2.aruco as aruco
import sys
import math
import time


def detect_ArUco(img):
    # convert the image first into grayscale and then apply binary thresholding for better results
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    cv2.imwrite("gray.png", gray)

    # generate the aruco dictionary and then detect the aruco markers in the current frame/image
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_1000)
    parameters = aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(
        gray, aruco_dict, parameters=parameters)

    # Create and return the dictionary with ids as keys and corners as values
    Detected_ArUco_markers = {}
    if ids is not None:
        for i in range(len(ids)):
            Detected_ArUco_markers[ids[i][0]] = corners[i]

    return Detected_ArUco_markers


def Calculate_orientation_in_degree(Detected_ArUco_markers):
    ArUco_marker_angles = {}
    # loop through all the detected markers
    for key, val in Detected_ArUco_markers.items():
        if val[0][1][0]-val[0][2][0] != 0:
            angle = np.arctan((val[0][2][1]-val[0][1][1])/(val[0][1][0]-val[0][2][0]))
        else:
            angle = np.pi/2
        angle = np.degrees(angle)

        # change the angle to be in between 0 and 359 rather than -90 and 90
        if angle < 0:
            if val[0][2][1] <= val[0][1][1]:
                angle += 360
            else:
                angle += 180
        else:
            if val[0][2][1] == val[0][1][1]:
                if val[0][2][0] < val[0][1][0]:
                    pass
                else:
                    angle += 180
            elif val[0][2][1] < val[0][1][1]:
                angle += 180
            else:
                pass
        ArUco_marker_angles[key] = angle
    return ArUco_marker_angles


def mark_ArUco(img, Detected_ArUco_markers, ArUco_marker_angles):
    for key, val in Detected_ArUco_markers.items():
        # mark the four corners with respective colours
        cv2.circle(img, np.int32(val[0][0]), 5, (125, 125, 125), -1)
        cv2.circle(img, np.int32(val[0][1]), 5, (0, 255, 0), -1)
        cv2.circle(img, np.int32(val[0][2]), 5, (180, 105, 255), -1)
        cv2.circle(img, np.int32(val[0][3]), 5, (255, 0, 0), -1)

        # find the center and put the line joining center and midpoint of
        # top side
        center = np.int32((val[0][3]+val[0][1])/2)
        topCenter = np.int32((val[0][1]+val[0][0])/2)
        cv2.circle(img, center, 5, (0, 0, 255), -1)
        cv2.line(img, center, topCenter, (255, 0, 0), 2)

        # put the texts on the image/frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(key), center +
                    np.int32([20, 0]), font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
        angle = round(ArUco_marker_angles[key])
        cv2.putText(img, str(angle), center -
                    np.int32([100, 0]), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(
            img, "SS#1839", (img.shape[1]-100, 10), font, 0.3, (0, 0, 255), 1, cv2.LINE_AA)
    return img
