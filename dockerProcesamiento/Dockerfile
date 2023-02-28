FROM python:3.10

RUN pip install pika mediapipe opencv-python && \
    apt-get update && apt-get install -y libgl1-mesa-glx && \
    pip cache purge

COPY server.py helloworld.py .

EXPOSE 8080

CMD ["python3", "server.py"]
