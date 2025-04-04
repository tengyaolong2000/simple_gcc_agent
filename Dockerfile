FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99

# 1) Install GUI, dev tools, and remove unwanted power/screen stuff
RUN apt-get update && apt-get install -y \
    xfce4 xfce4-goodies \
    x11vnc xvfb xdotool \
    imagemagick x11-apps \
    sudo curl gnupg ca-certificates git \
    software-properties-common wget apt-transport-https \
    procps \
 && apt-get remove -y light-locker xfce4-screensaver xfce4-power-manager || true \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2) Install Firefox ESR
RUN add-apt-repository ppa:mozillateam/ppa \
 && apt-get update \
 && apt-get install -y --no-install-recommends firefox-esr \
 && update-alternatives --set x-www-browser /usr/bin/firefox-esr \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# 3) Install Node.js as root
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
 && apt-get update && apt-get install -y nodejs \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# 4) Create non-root user
RUN useradd -ms /bin/bash myuser && echo "myuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 5) Switch to user and setup controller
USER myuser
WORKDIR /home/myuser

# Fix npm cache to avoid EACCES errors
ENV npm_config_cache=/home/myuser/.npm-cache

# Setup Playwright
RUN mkdir -p /home/myuser/playwright && cd /home/myuser/playwright \
 && npm init -y \
 && npm install express \
 && npm install -D playwright \
 && npx playwright install --with-deps chromium

# Copy controller and fix permissions
COPY controller.js /home/myuser/playwright/controller.js
USER root
RUN chown -R myuser:myuser /home/myuser/playwright
USER myuser

# 6) Set VNC password
RUN mkdir -p /home/myuser/.vnc && x11vnc -storepasswd secret /home/myuser/.vncpass

# 7) Expose ports
EXPOSE 5900 3000

# 8) Create a startup script
USER root
RUN echo '#!/bin/bash\n\
# Remove any stale X server lock files\n\
rm -f /tmp/.X*-lock /tmp/.X11-unix/* || true\n\
\n\
# Start X virtual framebuffer\n\
Xvfb :99 -screen 0 1280x800x24 -ac &\n\
sleep 3\n\
\n\
# Start VNC server\n\
x11vnc -display :99 -forever -rfbauth /home/myuser/.vncpass -listen 0.0.0.0 -rfbport 5900 &\n\
sleep 2\n\
\n\
# Start Xfce desktop\n\
startxfce4 &\n\
sleep 3\n\
\n\
# Run Playwright controller\n\
cd /home/myuser/playwright\n\
sudo -u myuser node controller.js\n\
' > /start.sh && chmod +x /start.sh

# 9) Run everything
CMD ["/start.sh"]