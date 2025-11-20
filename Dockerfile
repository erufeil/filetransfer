FROM python:3.11-slim
WORKDIR /app
COPY receiver.py .
COPY index.html . 
RUN pip install flask
VOLUME ["/uploads"]
EXPOSE 5000
CMD ["python", "receiver.py"]