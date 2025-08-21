FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    git zip unzip openjdk-8-jdk \
    autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev libssl-dev \
    android-tools-adb android-tools-fastboot \
    wget curl \
    && apt-get clean

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# Create Android SDK directory
RUN mkdir -p $ANDROID_HOME

WORKDIR /app
COPY . /app

# Install Python dependencies
RUN python3 -m pip install buildozer cython==0.29.33

# Pre-configure buildozer to avoid interactive prompts
RUN echo 'y' | buildozer init || true

# Set environment variables to avoid interactive prompts
ENV BUILDOZER_WARN_ON_ROOT=1
ENV ANDROID_SDK_LICENSE_ACCEPT=yes

# Create script to handle build with proper input handling
RUN echo '#!/bin/bash\n\
echo "Starting Android build..."\n\
echo "y" | buildozer android debug --verbose\n\
echo "Build completed. Checking output..."\n\
ls -la bin/ || echo "No bin directory found"\n\
find . -name "*.apk" -type f 2>/dev/null || echo "No APK files found"' > /app/build.sh

RUN chmod +x /app/build.sh

CMD ["/app/build.sh"]