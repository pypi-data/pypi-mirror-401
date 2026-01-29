"""
Nacos配置中心SDK (v2异步版本)
============================

提供两种低侵入性的配置监听方式：
1. 支持pydantic_settings的Settings类
2. 支持普通变量模块

适配 nacos-sdk-python 3.x (v2) 异步API

Usage:
------
    import asyncio
    from nacos_sdk import NacosConfigManager
    
    async def main():
        # 初始化
        manager = NacosConfigManager(
            server_addresses="127.0.0.1:8848",
            namespace="public",
            data_id="your-config",
            group="DEFAULT_GROUP"
        )
        
        # 方式1: 监听pydantic_settings
        from your_app.config import settings
        manager.watch_settings(settings, keys=["APP_NAME", "APP_VERSION"])
        
        # 方式2: 监听模块变量
        import your_app.config as config_module
        manager.watch_module(config_module, keys=["APP_NAME", "APP_VERSION"])
        
        # 启动监听
        await manager.start()
        
        # ... 应用代码 ...
        
        # 停止监听
        await manager.stop()
    
    asyncio.run(main())
"""

from .client import NacosConfigManager
from .adapters import SettingsAdapter, ModuleAdapter

__version__ = "0.2.0"
__all__ = [
    "NacosConfigManager",
    "SettingsAdapter",
    "ModuleAdapter",
]
