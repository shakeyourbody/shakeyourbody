#!/bin/bash

# Install processing libs
# For the processig IDE use the intern tools, this script works only from cli
# Pietro Jomini

# Paths
BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. >/dev/null 2>&1 && pwd )"
LIBS="$BASEDIR/src/libraries"
[[ ! -d "$LIBS" ]] && mkdir -p "$LIBS"

# OpenCV
# https://github.com/atduskgreg/opencv-processing
# CV_RELEASE=https://docs.google.com/uc?export=download&id=1mVyLZqZAzvXLCXr82H_IzaNDflxAfMCo
CV_PATH="$LIBS/CVImage"
if [[ ! -d "$CV_PATH" ]]; then

    # Download file
    # wget -O "$LIBS/cv.zip" "$CV_RELEASE"
    # may thanks to https://medium.com/@acpanjan/download-google-drive-files-using-wget-3c2c025a8b99
    wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1mVyLZqZAzvXLCXr82H_IzaNDflxAfMCo' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1mVyLZqZAzvXLCXr82H_IzaNDflxAfMCo" -O "$LIBS/cv.zip" && rm -rf /tmp/cookies.txt

    # Unzip & cleanup
    unzip "$LIBS/cv.zip" -d "$LIBS"
    rm "$LIBS/cv.zip"
fi

# Video
# https://github.com/processing/processing-video
VIDEO_RELEASE=https://github.com/processing/processing-video/releases/download/r6-v2.0-beta4/video-2.0-beta4.zip
VIDEO_PATH="$LIBS/video"
if [[ ! -d "$VIDEO_PATH" ]]; then

    # Download file
    wget -O "$LIBS/video.zip" "$VIDEO_RELEASE"

    # Unzip & cleanup
    unzip "$LIBS/video.zip" -d "$LIBS"
    rm "$LIBS/video.zip"
fi