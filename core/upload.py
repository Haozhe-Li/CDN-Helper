"""
This code is inspired by the blog post:
Mastering GitHub Actions for ARM Servers: A Comprehensive Guide by Dipankar
https://www.desinerd.com/p/mastering-file-uploads-cloudflare-r2-python-comprehensive-guide/
"""

import boto3
from botocore.config import Config
import os
from typing import Optional

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("CF_API_URL"),
    aws_access_key_id=os.getenv("CF_API_KEY_ID"),
    aws_secret_access_key=os.getenv("CF_API_KEY_SECRET"),
    config=Config(signature_version="s3v4"),
)

BUCKET_FREE_NAME = os.getenv("CF_FREE_BUCKET")
VIP_BUCKET_NAME = os.getenv("CF_VIP_BUCKET")
CLOUDFLARE_FREE_URL = "https://cdn-free.haozheli.com/"
CLOUDFLARE_VIP_URL = "https://cdn.haozheli.com/"
VIP_CODE = os.getenv("VIP_CODE")


def upload_to_cloudflare(
    file_path: str, vipcode: str, object_name: Optional[str] = None
) -> str:
    """
    Uploads a file to Cloudflare R2, returns the public URL, and deletes the local file.

    :param file_path: Path to the file to be uploaded
    :param vipcode: VIP code to determine the bucket
    :param object_name: S3 object name. If not specified, the base name of file_path is used
    :return: Public URL of the uploaded file
    """
    # Determine the bucket name and public URL based on the VIP code
    bucket_name = BUCKET_FREE_NAME if vipcode != VIP_CODE else VIP_BUCKET_NAME
    cloudflare_public_url = (
        CLOUDFLARE_FREE_URL if vipcode != VIP_CODE else CLOUDFLARE_VIP_URL
    )

    # Use the base name of the file_path if object_name is not specified
    if object_name is None:
        object_name = os.path.basename(file_path)

    # Upload the file to the specified bucket
    s3.upload_file(file_path, bucket_name, object_name)

    # Generate the public URL for the uploaded file
    url = f"{cloudflare_public_url}{object_name}"

    # Delete the local file
    os.remove(file_path)

    return url
