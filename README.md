# s3-recycler
[![DockerHub Link](https://img.shields.io/docker/pulls/tweedge/s3-recycler)](https://hub.docker.com/repository/docker/tweedge/s3-recycler)
[![License](https://img.shields.io/github/license/tweedge/s3-recycler)](https://github.com/tweedge/s3-recycler)
[![Written By](https://img.shields.io/badge/written%20by-some%20nerd-red.svg)](https://chris.partridge.tech)
[![Author Also Writes On](https://img.shields.io/mastodon/follow/108210086817505115?domain=https%3A%2F%2Fcybersecurity.theater)](https://cybersecurity.theater/@tweedge)

Not all S3 providers have automatic deletion capabilities, so this is an inefficient little sidecar to list out and delete all files in an S3 bucket periodically. It's also a little playground I used to learn about building distroless images.

## Config

**Required** environment variables to set are:

* `S3_BUCKET` - ex. `mybucket`, what the name of your bucket is
* `S3_REGION` - ex. `us-east-1`, what region your bucket is in
* `S3_ENDPOINT_URL` - ex. `https://s3.us-east-1.amazonaws.com`, your S3 provider's API
* `S3_ACCESS_KEY_ID` - ex. `AKIA...`, your access key ID
* `S3_SECRET_KEY` - ex. `wJal...`, your secret key
* `RECYCLER_SLEEP` - ex. `3600`, how long to sleep (in seconds) before deleting all known objects

**Optional** environment variables to set are:

* `RECYCLER_STARTUP_HOLD` - ex. `60`, how long to sleep (in seconds) when the container first starts