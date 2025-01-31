import boto3
from botocore.config import Config
import os
from typing import Optional
import os

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
    将文件上传到Cloudflare R2，返回公共URL，并删除本地文件。

    :param file_path: 要上传的文件路径
    :param object_name: S3对象名称。如果未指定，则使用file_path的基本名称
    :return: 上传文件的公共URL
    """
    # 如果未指定S3对象名称，则使用file_path的基本名称

    BUCKET_NAME = BUCKET_FREE_NAME if vipcode != VIP_CODE else VIP_BUCKET_NAME
    CLOUDFLARE_PUBLIC_URL = (
        CLOUDFLARE_FREE_URL if vipcode != VIP_CODE else CLOUDFLARE_VIP_URL
    )

    if object_name is None:
        object_name = os.path.basename(file_path)

    print(f"上传文件到 {BUCKET_NAME}：{object_name}")
    # 上传文件
    s3.upload_file(file_path, BUCKET_NAME, object_name)

    # 为上传的文件生成公共URL
    url = f"{CLOUDFLARE_PUBLIC_URL}{object_name}"
    print(url)

    # 删除本地文件
    os.remove(file_path)

    return url
