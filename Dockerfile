FROM ubuntu:latest
ENV LC_CTYPE C.UTF-8
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt-get dist-upgrade -y
RUN apt install -y apt-utils
RUN apt install -y git wget unzip gnupg2 python3 python3-pip
RUN pip3 install selenium
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt update && apt install -y google-chrome-stable
RUN wget https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/
RUN rm chromedriver_linux64.zip
RUN git clone https://github.com/delta-12/gimkit_bot.git
WORKDIR /gimkit_bot
ENV LINE='options.add_argument("--headless")'
ENV INSERT='options.add_argument("--no-sandbox")\noptions.add_argument("--disable-dev-shm-usage")'
ENV FILE='gimkit.py'
RUN sed -i "s/$LINE/$LINE\n$INSERT/" $FILE
RUN chmod +x bot.py
ENTRYPOINT [ "./bot.py" ]