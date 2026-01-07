FROM zeek/zeek:latest

WORKDIR /pcaps
VOLUME [ "/pcaps", "/zeek_logs" ]

# ensure /zeek_logs exists and is writable
RUN mkdir -p /zeek_logs && chmod 0777 /zeek_logs

# keep container alive for debugging/exec
CMD ["tail", "-f", "/dev/null"]
