#!/bin/bash

# start_webcam.sh
# Script to set up v4l2loopback and pipe gphoto2 output to it.
# Usage: ./start_webcam.sh

# Exit on error
set -e

echo "Starting Canon EOS R8 Webcam setup..."

# 1. Ensure gphoto2, v4l2loopback-dkms, and ffmpeg are installed
if ! command -v gphoto2 &> /dev/null; then
    echo "gphoto2 is not installed. Please install it first."
    exit 1
fi

if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg is not installed. Please install it first."
    exit 1
fi

# 2. Check if v4l2loopback module is loaded
if ! lsmod | grep -q v4l2loopback; then
    echo "Loading v4l2loopback module..."
    # You might need sudo privileges for this
    sudo modprobe v4l2loopback exclusive_caps=1 max_buffers=2
    if [ $? -ne 0 ]; then
        echo "Failed to load v4l2loopback. Is the module installed?"
        exit 1
    fi
fi

# Find the loopback device (usually /dev/video0 or /dev/video1 etc)
# Let's assume /dev/video0 for simplicity, or find the one managed by v4l2loopback
# We will just try /dev/video0 or the first one we find that is a loopback device
LOOPBACK_DEV=$(v4l2-ctl --list-devices | grep -A 1 "Dummy video device" | grep /dev/video | awk '{print $1}')
if [ -z "$LOOPBACK_DEV" ]; then
    # Fallback to /dev/video0 if not found via v4l2-ctl
    LOOPBACK_DEV="/dev/video0"
fi

echo "Using video device: $LOOPBACK_DEV"

# 3. Kill any PTP processes that might be locking the camera (like gvfs)
echo "Killing any processes locking the camera..."
pkill -f gvfs-gphoto2-volume-monitor || true
pkill -f ptp2 || true

# 4. Start routing the movie output to the loopback device
echo "Starting video feed. Press Ctrl+C to stop."
gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 $LOOPBACK_DEV

echo "Webcam feed stopped."
