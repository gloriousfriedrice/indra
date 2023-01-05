#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import time
import copy
import argparse
import cv2 as cv
import numpy as np
import configparser
import os
import sys
import _thread as thread
import syslog

from hashlib import pbkdf2_hmac


from model.yolox.yolox_onnx import YoloxONNX
from playsound import playsound

PATH = os.path.abspath(__file__ + "/..")
MODELPATH = PATH + "/model/yolox/yolox_nano.onnx"
LABELPATH = PATH + "/setting/labels.csv"
SOUNDPATH = PATH + "/sound/sound_effect_1.mp3"
LABELPATH = PATH + "/setting/labels.csv"
SHADOWPATH = "/usr/lib/security/indra/shadow"


def init_detector(lock):
    if not os.path.isfile(MODELPATH):
        syslog.syslog(
            syslog.LOG_ERR, "Model file has not been downloaded, please run the following commands:")
        lock.release()
        sys.exit(1)


def encrypt(passwd):
    return pbkdf2_hmac('sha256', bytes(passwd, 'utf-8'), bytes(user, 'utf-8'), 50505).hex()


# main program
# Make sure we were given an username to test against
if len(sys.argv) < 2:
    sys.exit(12)

user = sys.argv[1]


syslog.syslog(syslog.LOG_NOTICE, "authlog.py is being executed")
# Read config from disk
config = configparser.ConfigParser()
config.read(PATH + "/config.ini")

# Get all config values needed
certainty = config.getint("video", "certainty", fallback=8)/10
timeout = config.getint("video", "timeout", fallback=5)


# Start threading and wait for init to finish
lock = thread.allocate_lock()
lock.acquire()
thread.start_new_thread(init_detector, (lock, ))

cap_device = config.get
cap_width = 960
cap_height = 540
skip_frame = 0
score_th = 0.75

fps = 30
model_path = MODELPATH
input_shape = tuple(map(int, [416, 416]))
nms_th = 0.45
nms_score_th = 0.1
frame_count = 0

with open(SHADOWPATH) as f:
    lines = f.readlines()
    for line in lines:
        if user in line:
            hashed = line.split(":")[1]
            lenhashed = int(line.split(":")[2])
            break

password = []

# List all available video device
devices = os.listdir("/dev")
cameras = [camera for camera in devices if camera.startswith("video")]
cap = None

# Try to capture all available video device
for camera in cameras:
    idx = int(camera.replace("video", ""))

    cap = cv.VideoCapture(idx)
    if cap.isOpened():
        syslog.syslog(syslog.LOG_NOTICE,
                      f"Capturing video on {camera} device using index {idx}")
        break

syslog.openlog("[Indra]", 0, syslog.LOG_AUTH)
# Exit authentication as camera is not opened
if not cap.isOpened():
    syslog.syslog(syslog.LOG_NOTICE,
                  f"Unable to capture video, no camera is opened")
    cap.release()
    sys.exit(9)

cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

syslog.syslog(syslog.LOG_NOTICE,
              "Loading models")
yolox = YoloxONNX(
    model_path=model_path,
    input_shape=input_shape,
    class_score_th=score_th,
    nms_th=nms_th,
    nms_score_th=nms_score_th,
)

with open(LABELPATH, encoding='utf8') as f:
    labels = csv.reader(f)
    labels = [row for row in labels]

playsound(PATH+"/sound/login.mp3")
perform_time = time.time()
while True:
    start_time = time.time()
    ret, frame = cap.read()
    if not ret:
        continue
    # debug_image = copy.deepcopy(frame)
    frame_count += 1
    if (frame_count % (skip_frame + 1)) != 0:
        continue
    bboxes, scores, class_ids = yolox.inference(frame)
    for bbox, score, class_id in zip(bboxes, scores, class_ids):
        class_id = int(class_id) + 1
        if class_id < 1 or class_id > 13:
            continue
        if score < score_th:
            continue
        x1, y1 = int(bbox[0]), int(bbox[1])
        x2, y2 = int(bbox[2]), int(bbox[3])
        sign = "".join(labels[class_id])
        if score > certainty:
            if len(password) == 0:
                playsound(SOUNDPATH)
                password.append(sign)
                time.sleep(0.5)
            else:
                if password[-1] != sign:
                    playsound(SOUNDPATH)
                    password.append(sign)
                    time.sleep(0.5)

            if hashed == encrypt("".join(password)):
                authenticated_user = True
                cap.release()
                sys.exit(0)
            if len(password) > lenhashed+2:
                cap.release()
                syslog.syslog(syslog.LOG_NOTICE,
                              f'Wrong hand sign')

                sys.exit(12)
    elapsed_time = time.time() - start_time
    sleep_time = max(0, ((1.0 / fps) - elapsed_time))
    time.sleep(sleep_time)
    # Check if the authentication duration has exceed the time limit
    if time.time()-perform_time > timeout:
        syslog.syslog(syslog.LOG_NOTICE,
                      f'Attempted password is{"".join(password)}')
        cap.release()
        sys.exit(11)
