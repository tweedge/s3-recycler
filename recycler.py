from os import getenv
from time import sleep, time

import boto3

try:
    s3_bucket = getenv("S3_BUCKET")
    s3_region = getenv("S3_REGION")
    s3_endpoint_url = getenv("S3_ENDPOINT_URL")
    s3_access_key_id = getenv("S3_ACCESS_KEY_ID")
    s3_secret_key = getenv("S3_SECRET_KEY")
    recycler_sleep = getenv("RECYCLER_SLEEP")
except Exception as e:
    print("RECYCLER: Not all required environment keys are set, see README, quitting")
    exit(1)

if not (
    s3_region
    and s3_endpoint_url
    and s3_access_key_id
    and s3_secret_key
    and s3_bucket
    and recycler_sleep
    and int(recycler_sleep) > 0
):
    print("RECYCLER: At least one environment key was falsey, see README, quitting")
    exit(1)

recycler_sleep = int(recycler_sleep)

try:
    recycler_startup_hold = int(getenv("RECYCLER_STARTUP_HOLD"))
except Exception:
    recycler_startup_hold = 10

try:
    recycler_skip_n_items = int(getenv("RECYCLER_SKIP_N_ITEMS"))
except Exception:
    recycler_skip_n_items = 0

if recycler_sleep > 60 * 60 * 5:
    sleep_text = f"{round(recycler_sleep / (60 * 60), 3)}h"
elif recycler_sleep > 60 * 5:
    sleep_text = f"{round(recycler_sleep / 60, 3)}m"
else:
    sleep_text = f"{recycler_sleep}s"

print(f"RECYCLER: Booted, will sleep for {recycler_startup_hold}s before starting")
while True:
    sleep(recycler_startup_hold)

    print("RECYCLER: Setting up new boto3 session to list all objects")
    boto3_session = boto3.session.Session()
    s3 = boto3_session.client(
        "s3",
        region_name=s3_region,
        endpoint_url=s3_endpoint_url,
        aws_access_key_id=s3_access_key_id,
        aws_secret_access_key=s3_secret_key,
    )

    s3_paginator = s3.get_paginator("list_objects")
    s3_params = {"Bucket": s3_bucket}

    print("RECYCLER: Listing all current objects in the bucket ...")
    objects = []
    iterator = s3_paginator.paginate(**s3_params)
    for page in iterator:
        if not "Contents" in page.keys():
            break
        for s3_object in page["Contents"]:
            objects.append(s3_object["Key"])

    todo = len(objects)
    if todo == 0:
        print(
            f"RECYCLER: No objects to delete, going to sleep {sleep_text} before looking again"
        )
        sleep(recycler_sleep)
        continue

    print(
        f"RECYCLER: Found {todo} objects to delete after sleeping {sleep_text}"
    )
    sleep(recycler_sleep)

    print("RECYCLER: Setting up new boto3 session to delete tracked objects")
    boto3_session = boto3.session.Session()
    s3 = boto3_session.client(
        "s3",
        region_name=s3_region,
        endpoint_url=s3_endpoint_url,
        aws_access_key_id=s3_access_key_id,
        aws_secret_access_key=s3_secret_key,
    )

    if recycler_skip_n_items < 1:
        print("RECYCLER: Deleting items from the bucket ...")
    else:
        print(f"RECYCLER: Deleting items from the bucket (will log every {recycler_skip_n_items} deleted items)...")
    
    n = 0
    done = 0

    for s3_object_key in objects:
        s3.delete_object(Bucket=s3_bucket, Key=s3_object_key)
        n += 1
        done += 1

        if n >= recycler_skip_n_items:
            n = 0
            print(f"RECYCLER: Deleted {s3_object_key} ({done}/{todo})")

    print("RECYCLER: Deleted all tracked items!")
