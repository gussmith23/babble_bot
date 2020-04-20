FROM python:3.4

# Set up Python
RUN pip3 install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

## Set up example script
WORKDIR /root
COPY ./babble_bot.cfg ./babble_bot.cfg
COPY ./babble_bot.py ./babble_bot.py
COPY ./mangle.py ./mangle.py

CMD ["python3", "babble_bot.py"]
