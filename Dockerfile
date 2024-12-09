# Use a regular Python image to install packages
FROM python:3.12-slim as builder

# Install the required packages
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org boto3

# Switch to the distroless image w/ non-root config loaded
# USER: nonroot
# WORKDIR: /home/nonroot/
FROM gcr.io/distroless/python3-debian12:nonroot

# Copy the installed packages
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application
COPY ./recycler.py /home/nonroot/recycler.py

# Set command to run at startup
# ENTRYPOINT is already set to the python3 binary, so we don't need to add it!
CMD ["-u", "/home/nonroot/recycler.py"]