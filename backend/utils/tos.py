import tos

import env


def generate_download_url(file_name: str):
    """生成文件下载 URL"""
    tos_client = tos.TosClient(
        tos.Auth(env.TOS_ACCESS_KEY, env.TOS_SECRET_KEY, env.TOS_REGION),
        env.TOS_ENDPOINT,
    )
    return tos_client.generate_presigned_url(
        Method="GET", Bucket=env.TOS_BUCKET, Key=file_name, ExpiresIn=3600
    )
