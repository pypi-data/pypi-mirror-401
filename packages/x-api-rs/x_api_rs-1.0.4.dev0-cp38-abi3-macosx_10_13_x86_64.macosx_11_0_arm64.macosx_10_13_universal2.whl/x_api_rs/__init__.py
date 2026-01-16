"""
x_api_rs - Twitter/X API Python 绑定

快速开始:
    >>> from x_api_rs import Twitter
    >>> client = Twitter(cookies)
    >>> result = await client.dm.send_message("user_id", "Hello!")

模块化设计，支持两种 API 风格：

## 风格 1: 子模块属性访问（推荐）
```python
from x_api_rs import Twitter

client = Twitter(cookies)
result = await client.dm.send_message("123", "Hello")
result = await client.user.get_profile("elonmusk")
result = await client.upload.image(image_bytes, "dm_image")
result = await client.inbox.get_user_updates()
```

## 风格 2: 直接导入常用类型
```python
from x_api_rs import Twitter, DMResult, UploadResult, UserResp

client = Twitter(cookies)
result = await client.dm.send_message("123", "Hello")
print(result.success)
```

## 风格 3: 子模块高级功能
```python
from x_api_rs.dm import encode_message, decode_message, MediaInput
from x_api_rs.fingerprint import configure, get_random_fingerprint
```

## 模块列表

- `dm`: 私信发送模块
- `upload`: 图片/视频上传模块
- `inbox`: 收件箱查询模块
- `user`: 用户资料模块
- `posts`: 帖子操作模块
- `fingerprint`: 浏览器指纹管理模块
"""

# 从原生模块导入核心类
from .x_api_rs import (
    Twitter,
    AuthTokenResult,
    __version__,
)

# ========== DM 模块类型 ==========
from .dm import (
    DMClient,
    DMResult,
    BatchDMResult,
    MediaAttachment,
    DecodedMessage,
    MediaInput,
    encode_message,
    decode_message,
)

# ========== Upload 模块类型 ==========
from .upload import (
    UploadClient,
    UploadResult,
    BatchUploadResult,
)

# ========== Inbox 模块类型 ==========
from .inbox import (
    InboxClient,
    UserUpdatesResult,
)

# ========== User 模块类型 ==========
from .user import (
    UserClient,
    UserResp,
    AboutAccountResult,
    EditUserParams,
    EditUserResult,
    ChangeProfileImageResult,
    ChangeBannerResult,
)

# ========== Posts 模块类型 ==========
from .posts import (
    PostsClient,
    CreateTweetParams,
    TweetResult,
    DeleteTweetResult,
    LikeResult,
    RetweetResult,
    TweetInfo,
    GetTweetsResult,
    GetLikesResult,
)

# ========== 子模块（高级用法）==========
from . import dm
from . import upload
from . import inbox
from . import user
from . import posts
from . import fingerprint

# ========== 公开 API 声明 ==========
__all__ = [
    # 核心客户端
    "Twitter",
    "AuthTokenResult",
    "__version__",

    # DM 模块
    "DMClient",
    "DMResult",
    "BatchDMResult",
    "MediaAttachment",
    "DecodedMessage",
    "MediaInput",
    "encode_message",
    "decode_message",

    # Upload 模块
    "UploadClient",
    "UploadResult",
    "BatchUploadResult",

    # Inbox 模块
    "InboxClient",
    "UserUpdatesResult",

    # User 模块
    "UserClient",
    "UserResp",
    "AboutAccountResult",
    "EditUserParams",
    "EditUserResult",
    "ChangeProfileImageResult",
    "ChangeBannerResult",

    # Posts 模块
    "PostsClient",
    "CreateTweetParams",
    "TweetResult",
    "DeleteTweetResult",
    "LikeResult",
    "RetweetResult",
    "TweetInfo",
    "GetTweetsResult",
    "GetLikesResult",

    # 子模块
    "dm",
    "upload",
    "inbox",
    "user",
    "posts",
    "fingerprint",
]
