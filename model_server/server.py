from argparse import Namespace
from vllm.entrypoints.openai.api_server import build_app
from uvicorn import run
from .config import MODEL_PATH, PORT

if __name__ == "__main__":
    args = Namespace(
        model=MODEL_PATH,
        host="0.0.0.0",
        port=PORT,
        # 支持 /v1/chat/completions 等 OpenAI 兼容端点
        # 可根据需要添加其他参数，如 api_key 等
    )
    
    app = build_app(args)
    run(app, host="0.0.0.0", port=PORT)