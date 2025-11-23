# -*- coding: UTF-8 -*-
import boto3
from botocore.client import Config

import env


def get_s3_client():
    """获取 S3 客户端实例"""
    # 确保 endpoint 包含协议前缀
    endpoint = env.STORAGE_ENDPOINT
    if not endpoint.startswith(("http://", "https://")):
        endpoint = f"https://{endpoint}"

    return boto3.client(
        "s3",
        aws_access_key_id=env.STORAGE_ACCESS_KEY,
        aws_secret_access_key=env.STORAGE_SECRET_KEY,
        endpoint_url=endpoint,
        region_name=env.STORAGE_REGION,
        use_ssl=True,
        verify=True,
        config=Config(
            signature_version="s3v4",
            s3={"addressing_style": "virtual"},  # TOS 要求使用 Virtual-Hosted-Style
            retries={"max_attempts": 3, "mode": "standard"},
        ),
    )


def generate_download_url(file_name: str):
    """生成文件下载 URL (使用 S3 兼容协议)"""
    s3_client = get_s3_client()

    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": env.STORAGE_BUCKET, "Key": file_name},
        ExpiresIn=3600,
    )


def generate_upload_url(file_name: str):
    """生成文件上传 URL (使用 S3 兼容协议)"""
    s3_client = get_s3_client()

    return s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": env.STORAGE_BUCKET, "Key": file_name},
        ExpiresIn=3600,
    )
