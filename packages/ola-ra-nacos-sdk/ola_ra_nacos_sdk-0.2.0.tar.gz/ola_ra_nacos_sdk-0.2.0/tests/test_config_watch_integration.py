"""
Nacos配置监听集成测试
====================

连接真实Nacos环境，测试配置变更后能否正确监听并更新settings属性

使用 nacos-sdk-python 3.x (v2) 版本

使用方法：
---------
1. 设置环境变量（可选，默认值如下）：
   export NACOS_SERVER_ADDR=127.0.0.1:8848
   export NACOS_USERNAME=nacos
   export NACOS_PASSWORD=nacos
   export NACOS_NAMESPACE=public

2. 运行测试：
   cd nacos/python
   python -m pytest tests/test_config_watch_integration.py -v -s

3. 或者直接运行手动测试：
   python tests/test_config_watch_integration.py
"""

import os
import sys
import asyncio
import time
import logging
from typing import Optional, Dict, Any

import pytest
import pytest_asyncio
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nacos_sdk import NacosConfigManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================
# Nacos连接配置（从环境变量读取）
# ============================================================

NACOS_SERVER_ADDR = os.getenv('NACOS_SERVER_ADDR', '127.0.0.1:8848')
NACOS_USERNAME = os.getenv('NACOS_USERNAME', 'nacos')
NACOS_PASSWORD = os.getenv('NACOS_PASSWORD', 'nacos')
NACOS_NAMESPACE = os.getenv('NACOS_NAMESPACE', 'public')

# 测试用的配置
DATA_ID = "llm_model"
GROUP = "slp"


# ============================================================
# 测试用的Settings类
# ============================================================

class LLMModelSettings(BaseSettings):
    """LLM模型配置"""
    MODEL_NAME: str = "gpt-3.5-turbo"
    MODEL_VERSION: str = "1.0.0"
    MAX_TOKENS: int = 2048
    TEMPERATURE: float = 0.7
    DEBUG: bool = False
    API_ENDPOINT: str = "https://api.openai.com"
    
    model_config = ConfigDict(validate_assignment=True)


# ============================================================
# 测试类
# ============================================================

@pytest.mark.asyncio
class TestNacosConfigWatchIntegration:
    """Nacos配置监听集成测试"""
    
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self):
        """测试前置设置"""
        self.manager = NacosConfigManager(
            server_addresses=NACOS_SERVER_ADDR,
            namespace=NACOS_NAMESPACE,
            data_id=DATA_ID,
            group=GROUP,
            username=NACOS_USERNAME,
            password=NACOS_PASSWORD,
            config_format="properties",
        )
        
        # 保存原始配置
        try:
            await self.manager._ensure_connected()
            self.original_config = await self.manager.get_config()
        except Exception:
            self.original_config = None
        
        yield
        
        # 恢复原始配置
        if self.original_config:
            try:
                await self.manager.publish_config(self.original_config)
            except Exception:
                pass
        
        try:
            await self.manager.stop()
        except Exception:
            pass
    
    async def test_get_config(self):
        """测试获取配置"""
        content = await self.manager.get_config()
        
        logger.info(f"获取到的配置内容:\n{content}")
        
        assert content is not None, "配置不应为空"
        logger.info("✅ 获取配置测试通过")
    
    async def test_config_change_updates_settings(self):
        """测试配置变更时settings被正确更新"""
        # 发布初始配置
        initial_config = """MODEL_NAME=test-model-v1
MODEL_VERSION=1.0.0
MAX_TOKENS=1024
DEBUG=false"""
        
        await self.manager.publish_config(initial_config)
        await asyncio.sleep(1)
        
        # 创建settings
        settings = LLMModelSettings()
        watch_keys = ["MODEL_NAME", "MODEL_VERSION", "MAX_TOKENS", "DEBUG"]
        
        # 用于记录配置变更
        config_changed = asyncio.Event()
        
        def on_config_change(config: dict):
            logger.info(f"收到配置变更通知: {config}")
            config_changed.set()
        
        # 注册监听
        self.manager.watch_settings(settings, keys=watch_keys)
        self.manager.add_callback(on_config_change)
        
        # 启动监听
        await self.manager.start()
        
        logger.info(f"初始配置已加载: MODEL_NAME={settings.MODEL_NAME}")
        assert settings.MODEL_NAME == "test-model-v1"
        assert settings.MAX_TOKENS == 1024
        assert settings.DEBUG is False
        
        # 清除事件，准备检测新变更
        config_changed.clear()
        
        # 发布新配置
        new_config = """MODEL_NAME=test-model-v2
MODEL_VERSION=2.0.0
MAX_TOKENS=2048
DEBUG=true"""
        
        logger.info("正在发布新配置...")
        await self.manager.publish_config(new_config)
        
        # 等待配置变更回调
        try:
            await asyncio.wait_for(config_changed.wait(), timeout=30)
        except asyncio.TimeoutError:
            pytest.fail("等待配置变更超时")
        
        await asyncio.sleep(1)  # 额外等待确保更新完成
        
        # 验证settings已更新
        logger.info(f"配置变更后: MODEL_NAME={settings.MODEL_NAME}, DEBUG={settings.DEBUG}")
        
        assert settings.MODEL_NAME == "test-model-v2", f"期望 'test-model-v2', 实际 '{settings.MODEL_NAME}'"
        assert settings.MODEL_VERSION == "2.0.0"
        assert settings.MAX_TOKENS == 2048
        assert settings.DEBUG is True
        
        logger.info("✅ 配置变更更新settings测试通过")
    
    async def test_key_mapping(self):
        """测试key_mapping功能"""
        # 发布使用点号分隔的配置
        config = """llm.model.name=mapped-model
llm.model.debug=true
llm.model.max_tokens=4096"""
        
        await self.manager.publish_config(config)
        await asyncio.sleep(1)
        
        settings = LLMModelSettings()
        
        # 使用key_mapping映射配置键
        self.manager.watch_settings(
            settings,
            keys=["MODEL_NAME", "DEBUG", "MAX_TOKENS"],
            key_mapping={
                "llm.model.name": "MODEL_NAME",
                "llm.model.debug": "DEBUG",
                "llm.model.max_tokens": "MAX_TOKENS",
            }
        )
        
        await self.manager.start()
        
        # 验证映射后的配置
        logger.info(f"映射后: MODEL_NAME={settings.MODEL_NAME}, DEBUG={settings.DEBUG}, MAX_TOKENS={settings.MAX_TOKENS}")
        
        assert settings.MODEL_NAME == "mapped-model"
        assert settings.DEBUG is True
        assert settings.MAX_TOKENS == 4096
        
        logger.info("✅ key_mapping测试通过")
    
    async def test_multiple_config_changes(self):
        """测试多次配置变更"""
        settings = LLMModelSettings()
        watch_keys = ["MODEL_NAME", "DEBUG"]
        
        change_count = {"count": 0}
        config_changed = asyncio.Event()
        
        def on_config_change(config: dict):
            change_count["count"] += 1
            logger.info(f"第 {change_count['count']} 次配置变更: MODEL_NAME={config.get('MODEL_NAME')}")
            config_changed.set()
        
        self.manager.watch_settings(settings, keys=watch_keys)
        self.manager.add_callback(on_config_change)
        
        await self.manager.start()
        initial_count = change_count["count"]
        
        # 第一次变更
        config_changed.clear()
        await self.manager.publish_config("MODEL_NAME=multi-v1\nDEBUG=false")
        await asyncio.wait_for(config_changed.wait(), timeout=30)
        await asyncio.sleep(1)
        assert settings.MODEL_NAME == "multi-v1"
        
        # 第二次变更
        config_changed.clear()
        await self.manager.publish_config("MODEL_NAME=multi-v2\nDEBUG=true")
        await asyncio.wait_for(config_changed.wait(), timeout=30)
        await asyncio.sleep(1)
        assert settings.MODEL_NAME == "multi-v2"
        assert settings.DEBUG is True
        
        # 第三次变更
        config_changed.clear()
        await self.manager.publish_config("MODEL_NAME=multi-final\nDEBUG=false")
        await asyncio.wait_for(config_changed.wait(), timeout=30)
        await asyncio.sleep(1)
        assert settings.MODEL_NAME == "multi-final"
        
        logger.info(f"✅ 多次配置变更测试通过，共 {change_count['count'] - initial_count} 次变更")
    
    async def test_type_conversion(self):
        """测试类型转换"""
        settings = LLMModelSettings()
        watch_keys = ["MAX_TOKENS", "TEMPERATURE", "DEBUG"]
        
        config_changed = asyncio.Event()
        
        def on_change(config):
            config_changed.set()
        
        self.manager.watch_settings(settings, keys=watch_keys)
        self.manager.add_callback(on_change)
        
        # 发布包含各种类型的配置
        config = """MAX_TOKENS=4096
TEMPERATURE=0.9
DEBUG=yes"""
        
        await self.manager.publish_config(config)
        await self.manager.start()
        
        await asyncio.sleep(1)
        
        logger.info(f"MAX_TOKENS={settings.MAX_TOKENS} ({type(settings.MAX_TOKENS).__name__})")
        logger.info(f"TEMPERATURE={settings.TEMPERATURE} ({type(settings.TEMPERATURE).__name__})")
        logger.info(f"DEBUG={settings.DEBUG} ({type(settings.DEBUG).__name__})")
        
        assert isinstance(settings.MAX_TOKENS, int)
        assert settings.MAX_TOKENS == 4096
        
        assert isinstance(settings.TEMPERATURE, float)
        assert settings.TEMPERATURE == 0.9
        
        assert isinstance(settings.DEBUG, bool)
        assert settings.DEBUG is True
        
        logger.info("✅ 类型转换测试通过")
    
    async def test_async_callback(self):
        """测试异步回调函数"""
        settings = LLMModelSettings()
        
        async_callback_called = asyncio.Event()
        
        async def async_callback(config: dict):
            logger.info(f"异步回调被调用: {config}")
            await asyncio.sleep(0.1)  # 模拟异步操作
            async_callback_called.set()
        
        self.manager.watch_settings(settings, keys=["MODEL_NAME"])
        self.manager.add_callback(async_callback)
        
        await self.manager.publish_config("MODEL_NAME=async-test")
        await self.manager.start()
        
        # 验证异步回调被调用
        # 注意：初始加载时不会触发回调，需要等待配置变更
        
        # 发布变更触发回调
        async_callback_called.clear()
        await self.manager.publish_config("MODEL_NAME=async-test-v2")
        
        try:
            await asyncio.wait_for(async_callback_called.wait(), timeout=30)
            logger.info("✅ 异步回调测试通过")
        except asyncio.TimeoutError:
            pytest.fail("异步回调未被调用")


# ============================================================
# 手动交互测试
# ============================================================

async def run_manual_test():
    """
    手动运行测试，可以实时观察配置变更
    
    运行方式：
        python tests/test_config_watch_integration.py
    """
    print("=" * 60)
    print("🚀 Nacos配置监听集成测试 - 手动模式")
    print("=" * 60)
    print(f"  服务器地址: {NACOS_SERVER_ADDR}")
    print(f"  命名空间: {NACOS_NAMESPACE}")
    print(f"  Data ID: {DATA_ID}")
    print(f"  Group: {GROUP}")
    print("=" * 60)
    
    # 创建settings
    settings = LLMModelSettings()
    watch_keys = ["MODEL_NAME", "MODEL_VERSION", "MAX_TOKENS", "TEMPERATURE", "DEBUG", "API_ENDPOINT"]
    
    print(f"\n📋 初始settings值:")
    for key in watch_keys:
        print(f"  {key}: {getattr(settings, key)}")
    
    # 创建管理器
    manager = NacosConfigManager(
        server_addresses=NACOS_SERVER_ADDR,
        namespace=NACOS_NAMESPACE,
        data_id=DATA_ID,
        group=GROUP,
        username=NACOS_USERNAME,
        password=NACOS_PASSWORD,
        config_format="properties",
    )
    
    def on_config_change(config: dict):
        print("\n" + "=" * 60)
        print("🔔 配置变更通知!")
        print("=" * 60)
        print("  新配置内容:")
        for key, value in config.items():
            print(f"    {key}: {value}")
        print("-" * 40)
        print("  📋 更新后的settings值:")
        for key in watch_keys:
            print(f"    {key}: {getattr(settings, key)}")
        print("=" * 60)
    
    manager.watch_settings(settings, keys=watch_keys)
    manager.add_callback(on_config_change)
    
    try:
        print("\n👂 正在启动配置监听...")
        await manager.start()
        
        print(f"\n📥 从Nacos加载后的settings值:")
        for key in watch_keys:
            print(f"  {key}: {getattr(settings, key)}")
        
        print("\n" + "=" * 60)
        print("🎯 监听已启动!")
        print("   现在可以在Nacos控制台修改配置，观察变更效果")
        print("   按 Ctrl+C 退出程序")
        print("=" * 60)
        
        while True:
            await asyncio.sleep(10)
            print(f"\n[{time.strftime('%H:%M:%S')}] 监听中... MODEL_NAME={settings.MODEL_NAME}, DEBUG={settings.DEBUG}")
    
    except KeyboardInterrupt:
        print("\n\n⏹️ 收到退出信号...")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await manager.stop()
        print("👋 程序已退出")


def main():
    """主入口"""
    asyncio.run(run_manual_test())


if __name__ == "__main__":
    main()
