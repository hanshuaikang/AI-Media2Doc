# -*- coding: UTF-8 -*-
"""TwelveLabs Pegasus 视觉理解接口的聚焦测试。

运行方式 (在 backend 目录下):
    pip install pytest fastapi[all]
    pytest tests/test_video_visual_analysis.py

- test_disabled_without_key: 无网络。未配置 TWELVELABS_API_KEY 时, 接口必须明确返回
  "未启用", 证明该能力默认关闭、不影响现有 ASR 流程。
- test_live_visual_analysis: 仅当设置了 TWELVELABS_API_KEY 时运行, 真实调用一次 Pegasus。
"""
import os
import sys

import pytest

# 让测试能从 backend 根目录导入 app 模块 (与现有代码的导入风格一致)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _client():
    from fastapi.testclient import TestClient
    import app

    return TestClient(app.app)


def test_disabled_without_key(monkeypatch):
    """无网络: 未配置 key 时, 接口返回明确的未启用错误, 原有流程不受影响。"""
    import env

    monkeypatch.setattr(env, "TWELVELABS_API_KEY", None)

    resp = _client().post(
        "/api/v1/video/visual-analysis", json={"filename": "demo.mp4"}
    )

    # BusinessException -> 400, 统一响应结构中 success=False
    assert resp.status_code == 400
    body = resp.json()
    assert body["success"] is False
    assert "TWELVELABS_API_KEY" in body["error"]["message"]


@pytest.mark.skipif(
    not os.getenv("TWELVELABS_API_KEY"),
    reason="需要 TWELVELABS_API_KEY 才能做真实的 Pegasus 调用",
)
def test_live_visual_analysis():
    """真实调用: 给定公网视频 URL, Pegasus 返回非空画面描述文本。"""
    from twelvelabs import TwelveLabs
    from twelvelabs.types import VideoContext_Url

    from twelvelabs.errors.bad_request_error import BadRequestError

    client = TwelveLabs(api_key=os.environ["TWELVELABS_API_KEY"])
    url = os.getenv(
        "TWELVELABS_TEST_VIDEO_URL",
        "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBigBuckBunny.mp4",
    )
    try:
        resp = client.analyze(
            model_name=os.getenv("TWELVELABS_MODEL_NAME", "pegasus1.5"),
            video=VideoContext_Url(url=url),
            prompt="In one sentence, describe what is visually shown.",
            max_tokens=512,
        )
    except BadRequestError as e:
        # 部分网络环境无法让 Twelve Labs 拉取该公网测试视频; 这与接口本身无关。
        # 用自己的 TWELVELABS_TEST_VIDEO_URL 指向一个可达的视频即可真实验证。
        pytest.skip(
            f"Test video URL not fetchable by Twelve Labs in this environment: {e}"
        )

    assert isinstance(resp.data, str) and len(resp.data) > 0
