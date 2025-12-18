import os
from pathlib import Path

cache_dir = Path.home() / '.cache' / 'modelscope' / 'hub'

class modelManager:
    def __init__(self):
        self.models = {}

    def get_modelscope_hub_dir(self):
        """
        获取 ModelScope 模型缓存的 hub 目录。
        这是 ModelScope 官方认可的缓存位置解析逻辑：
        - 优先读取环境变量 MODELSCOPE_CACHE
        - 否则使用默认路径 ~/.cache/modelscope
        参考: https://modelscope.cn/docs
        """
        cache_root = os.getenv('MODELSCOPE_CACHE')
        if cache_root is None:
            cache_root = Path.home() / '.cache' / 'modelscope'
        else:
            cache_root = Path(cache_root)
        return cache_root / 'hub/models'
    
    def list_downloaded_models(self):
        """
        列出所有已下载（缓存）的 ModelScope 模型。
        判断标准：目录下存在 'configuration.json' (ModelScope 标准) 或 'config.json' (HF 兼容)。
        """
        hub_dir = self.get_modelscope_hub_dir()
        
        if not hub_dir.exists():
            return []

        models = []
        for author in hub_dir.iterdir():
            if not author.is_dir() or author.name.startswith('.'):
                continue
            for model in author.iterdir():
                if not model.is_dir() or model.name.startswith('.'):
                    continue
                # ModelScope 模型必须包含 configuration.json 或 config.json
                if (model / 'configuration.json').exists() or (model / 'config.json').exists():
                    models.append(f"{author.name}/{model.name}")
        
        sorted(models)
        if models:
            for m in models:
                print(m)
        else:
            print("未找到任何有效的已缓存模型。")
