# Use a regular Python image to install packages
FROM python:3.11-slim as builder

# Install the required packages
RUN pip install --no-cache-dir boto3

# Ensure pip, setuptools, and wheel don't piggyback into our application container
RUN rm -r /usr/local/lib/python3.11/site-packages/pip* \
  /usr/local/lib/python3.11/site-packages/setuptools* \
  /usr/local/lib/python3.11/site-packages/wheel*

# Switch to the distroless image w/ non-root config loaded
# USER: nonroot
# WORKDIR: /home/nonroot/
FROM gcr.io/distroless/python3-debian12:nonroot

# Copy the packages we need from our build container
COPY --from=builder /usr/local/lib/python3.11/site-packages \
  /usr/local/lib/python3.11/site-packages

# Set environment variable so Python can find the installed packages
# Otherwise we'll get a "No module named 'boto3'" error when starting our application!
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages

# Copy in our application
COPY ./recycler.py /home/nonroot/recycler.py

# Set commands to run at startup
# ENTRYPOINT is already set to the python3 binary, CMD appends to that!
ENTRYPOINT ["python3", "-u", "/home/nonroot/recycler.py"]
