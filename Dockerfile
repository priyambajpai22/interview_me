FROM ubuntu:latest

# Install required packages
RUN apt-get update && apt-get install -y wget
RUN  apt-get update && apt-get install -y gnupg2
RUN  apt-get update && apt install libgl1-mesa-glx
RUN apt-get update && apt install libgl1-mesa-glx:i386

# Download and install Sublime Text
RUN wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | apt-key add -
RUN echo "deb https://download.sublimetext.com/ apt/stable/" | tee /etc/apt/sources.list.d/sublime-text.list
RUN apt-get update && apt-get install -y sublime-text

# Set the entry point
ENTRYPOINT ["subl"]
