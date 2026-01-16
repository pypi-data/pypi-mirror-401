"""
DM (私信) 模块

提供私信发送功能，支持单条发送和批量并发发送。

Example:
    ```python
    from x_api.dm import DMClient

    client = DMClient(cookies)
    result = await client.send_message("123456", "Hello!")

    # 批量发送
    result = await client.send_batch(["123", "456"], "批量消息")

    # 消息编解码
    from x_api.dm import encode_message, decode_message, MediaInput

    # 纯文本消息
    encoded = encode_message("Hello!")
    result = decode_message(encoded)
    print(result.text, result.media)

    # 带媒体的消息
    media = [MediaInput(media_id="1234567890", filename="test.jpg")]
    encoded = encode_message("Hello with image", media)
    ```
"""

from ..x_api import dm as _dm

# 客户端和结果类型
DMClient = _dm.DMClient
DMResult = _dm.DMResult
BatchDMResult = _dm.BatchDMResult

# 消息解码类型
MediaAttachment = _dm.MediaAttachment
DecodedMessage = _dm.DecodedMessage

# 消息编码类型
MediaInput = _dm.MediaInput

# 消息编解码函数
encode_message = _dm.encode_message
decode_message = _dm.decode_message

__all__ = [
    # 客户端
    "DMClient",
    # 结果类型
    "DMResult",
    "BatchDMResult",
    # 消息解码类型
    "MediaAttachment",
    "DecodedMessage",
    # 消息编码类型
    "MediaInput",
    # 消息编解码函数
    "encode_message",
    "decode_message",
]
