
"""Model Adapter — Track E3, nhóm DTMD.

Kết nối LLM thật theo hướng dẫn của BTC.

Contract:
    call_model(system: str, user: str) -> dict

Output:
    text: nội dung model trả về
    model: tên model thực tế
    tokens_in: số token đầu vào thực tế
    tokens_out: số token đầu ra thực tế

Decorator @model_call tự ghi thông tin vào trace.

Hỗ trợ:
    fake: kiểm thử local, không gọi API.
    openai: gọi OpenAI Chat Completions API.
"""

import os
import json
import urllib.error
import urllib.request

from pathlib import Path

if __package__:
    from .tracing import model_call
else:
    from tracing import model_call


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

URL_OPENAI = (
    "https://api.openai.com/v1/chat/completions"
)

SHOW_RAW = False


def load_env():
    """Đọc cấu hình .env tại thư mục gốc."""

    env_path = ROOT / ".env"

    if not env_path.is_file():
        return

    with env_path.open(
        "r",
        encoding="utf-8-sig",
    ) as file:

        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)

            key = key.strip()
            value = value.strip()

            if (
                len(value) >= 2
                and value[0] == value[-1]
                and value[0] in ('"', "'")
            ):
                value = value[1:-1]

            os.environ.setdefault(key, value)


load_env()

MODEL_PROVIDER = (
    os.environ.get("MODEL_PROVIDER") or "fake"
).strip().lower()

MODEL_NAME = (
    os.environ.get("MODEL_NAME") or ""
).strip()

API_KEY = (
    os.environ.get("API_KEY") or ""
).strip()


# ============================================================
# HTTP CLIENT
# ============================================================

def post_json(
    url: str,
    headers: dict,
    body: dict,
    timeout: int = 60,
) -> dict:
    """Gửi HTTP POST và nhận phản hồi JSON."""

    request_headers = {
        "Content-Type": "application/json",
        **headers,
    }

    request = urllib.request.Request(
        url=url,
        data=json.dumps(
            body,
            ensure_ascii=False,
        ).encode("utf-8"),
        headers=request_headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.HTTPError as exc:
        # Không ghi raw response hoặc API key vào trace.
        raise RuntimeError(
            f"OpenAI API HTTP {exc.code}"
        ) from exc

    except urllib.error.URLError as exc:
        raise RuntimeError(
            "Cannot connect to OpenAI API"
        ) from exc

    except TimeoutError as exc:
        raise RuntimeError(
            "OpenAI API request timed out"
        ) from exc

    if not isinstance(data, dict):
        raise RuntimeError(
            "Invalid OpenAI API response"
        )

    if SHOW_RAW:
        print(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            )[:3000]
        )

    return data


# ============================================================
# OPENAI PROVIDER
# ============================================================

def call_openai(
    system: str,
    user: str,
) -> dict:
    """Gọi đúng một lần OpenAI Chat Completions API."""

    if not API_KEY:
        raise RuntimeError(
            "Missing API_KEY in .env"
        )

    if not MODEL_NAME:
        raise RuntimeError(
            "Missing MODEL_NAME in .env"
        )

    messages = []

    if system:
        messages.append({
            "role": "system",
            "content": system,
        })

    messages.append({
        "role": "user",
        "content": user,
    })

    body = {
        "model": MODEL_NAME,
        "messages": messages,
        "store": False,
        "max_completion_tokens": 1024,
    }

    data = post_json(
        url=URL_OPENAI,
        headers={
            "Authorization": f"Bearer {API_KEY}",
        },
        body=body,
    )

    choices = data.get("choices")

    if not choices:
        raise RuntimeError(
            "OpenAI returned no choices"
        )

    message = choices[0].get("message", {})

    text = message.get("content")

    if not isinstance(text, str):
        text = ""

    usage = data.get("usage")

    if not isinstance(usage, dict):
        raise RuntimeError(
            "OpenAI response missing token usage"
        )

    if (
        "prompt_tokens" not in usage
        or "completion_tokens" not in usage
    ):
        raise RuntimeError(
            "OpenAI response missing token counts"
        )

    return {
        "text": text.strip(),
        "model": data.get("model") or MODEL_NAME,
        "tokens_in": int(
            usage["prompt_tokens"]
        ),
        "tokens_out": int(
            usage["completion_tokens"]
        ),
    }


# ============================================================
# PUBLIC MODEL CONTRACT
# ============================================================

@model_call
def call_model(
    system: str,
    user: str,
) -> dict:
    """Gọi model theo cấu hình provider.

    Không thực thi công cụ.
    Không quyết định quyền giao dịch.
    Không thay thế Policy Engine.
    """

    # --------------------------------------------------------
    # Fake model — phục vụ kiểm thử local
    # --------------------------------------------------------

    if MODEL_PROVIDER == "fake":

        fake_response = {
            "classification": "unclear",
            "facts": {},
        }

        return {
            "text": json.dumps(
                fake_response,
                ensure_ascii=False,
            ),
            "model": "fake",
            "tokens_in": 0,
            "tokens_out": 0,
        }

    # --------------------------------------------------------
    # OpenAI — model thật
    # --------------------------------------------------------

    if MODEL_PROVIDER == "openai":
        return call_openai(
            system=system,
            user=user,
        )

    # --------------------------------------------------------
    # Unsupported provider
    # --------------------------------------------------------

    raise RuntimeError(
        f"Unsupported provider: {MODEL_PROVIDER}"
    )
