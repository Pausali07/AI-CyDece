FROM python:3.13-slim
WORKDIR /app
COPY . /app
# minimal image: installs nothing extra; Python stdlib sufficient for socket code
RUN mkdir -p /var/honeypot/logs && chmod 0777 /var/honeypot/logs
ENV HP_PORT=2222 HP_LOG_DIR=/var/honeypot/logs
EXPOSE 2222
CMD ["python", "/app/app.py"]
