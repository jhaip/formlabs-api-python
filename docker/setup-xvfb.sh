#!/bin/sh

# Start Xvfb
echo "Starting Xvfb"

echo "removing potentialy left over lock file, can we use -nolock instead?"
rm -f /tmp/.X99-lock

Xvfb ${DISPLAY} -ac -screen 0 "1920x1080x24" -nolisten tcp +extension GLX +render -noreset  &
echo "Waiting for Xvfb to be ready..."
while ! xdpyinfo -display "${DISPLAY}" > /dev/null 2>&1; do
    sleep 0.1
done
echo "Xvfb is running."
