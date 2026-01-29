"""
Nacos配置管理器 (v2异步版本)
===========================

负责与Nacos服务端交互，获取配置并监听变更
适配 nacos-sdk-python 3.x (v2) 异步API
"""

import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional, Set, Union
from types import ModuleType

try:
    from v2.nacos import NacosConfigService, ConfigParam, ClientConfigBuilder, GRPCConfig
except ImportError:
    raise ImportError(
        "请安装nacos-sdk-python 3.x: pip install nacos-sdk-python>=3.0.0"
    )

from .adapters import SettingsAdapter, ModuleAdapter
from .parsers import parse_config

logger = logging.getLogger(__name__)


class NacosConfigManager:
    """
    Nacos配置管理器 (异步版本)
    
    提供配置获取和监听功能，支持两种低侵入性的配置更新方式：
    1. pydantic_settings的Settings实例
    2. Python模块变量
    
    Example:
    --------
    ```python
    import asyncio
    from nacos_sdk import NacosConfigManager
    
    async def main():
        # 初始化管理器
        manager = NacosConfigManager(
            server_addresses="127.0.0.1:8848",
            namespace="public",
            data_id="app-config",
            group="DEFAULT_GROUP"
        )
        
        # 监听pydantic settings
        manager.watch_settings(settings, keys=["APP_NAME", "DEBUG"])
        
        # 启动监听
        await manager.start()
        
        # ... 你的应用代码 ...
        
        # 停止监听
        await manager.stop()
    
    asyncio.run(main())
    ```
    """
    
    def __init__(
        self,
        server_addresses: str,
        namespace: str = "public",
        data_id: str = "",
        group: str = "DEFAULT_GROUP",
        username: Optional[str] = None,
        password: Optional[str] = None,
        config_format: str = "properties",
        grpc_timeout: int = 5000,
        log_level: str = "INFO",
    ):
        """
        初始化Nacos配置管理器
        
        Parameters
        ----------
        server_addresses : str
            Nacos服务地址，格式: "host:port" 或 "host1:port1,host2:port2"
        namespace : str
            命名空间ID，默认为"public"
        data_id : str
            配置的data_id
        group : str
            配置分组，默认为"DEFAULT_GROUP"
        username : str, optional
            Nacos用户名
        password : str, optional
            Nacos密码
        config_format : str
            配置格式: "properties", "yaml", "json"，默认为"properties"
        grpc_timeout : int
            gRPC超时时间（毫秒），默认5000
        log_level : str
            日志级别，默认"INFO"
        """
        self.server_addresses = server_addresses
        self.namespace = namespace
        self.data_id = data_id
        self.group = group
        self.config_format = config_format
        self.username = username
        self.password = password
        self.grpc_timeout = grpc_timeout
        self.log_level = log_level
        
        # Nacos客户端（延迟初始化）
        self._client: Optional[NacosConfigService] = None
        
        # 适配器列表
        self._settings_adapters: List[SettingsAdapter] = []
        self._module_adapters: List[ModuleAdapter] = []
        
        # 自定义回调
        self._callbacks: List[Callable[[Dict[str, Any]], Any]] = []
        
        # 监听状态
        self._is_watching = False
        self._lock = asyncio.Lock()
        
        # 当前配置缓存
        self._current_config: Dict[str, Any] = {}
    
    def _build_client_config(self):
        """构建客户端配置"""
        builder = ClientConfigBuilder()
        builder.server_address(self.server_addresses)
        builder.log_level(self.log_level)
        builder.grpc_config(GRPCConfig(grpc_timeout=self.grpc_timeout))
        
        if self.namespace:
            builder.namespace_id(self.namespace)
        if self.username:
            builder.username(self.username)
        if self.password:
            builder.password(self.password)
        
        return builder.build()
    
    async def _ensure_connected(self):
        """确保已连接到Nacos服务器"""
        if self._client is None:
            client_config = self._build_client_config()
            logger.info(f"正在连接Nacos服务器: {self.server_addresses}")
            self._client = await NacosConfigService.create_config_service(client_config)
            logger.info("Nacos连接成功")
    
    async def get_config(self) -> str:
        """
        获取原始配置内容
        
        Returns
        -------
        str
            配置原始内容
        """
        await self._ensure_connected()
        return await self._client.get_config(ConfigParam(
            data_id=self.data_id,
            group=self.group
        ))
    
    async def get_config_parsed(self) -> Dict[str, Any]:
        """
        获取解析后的配置字典
        
        Returns
        -------
        Dict[str, Any]
            解析后的配置字典
        """
        raw_config = await self.get_config()
        return parse_config(raw_config, self.config_format)
    
    async def publish_config(self, content: str) -> bool:
        """
        发布配置
        
        Parameters
        ----------
        content : str
            配置内容
            
        Returns
        -------
        bool
            是否发布成功
        """
        await self._ensure_connected()
        return await self._client.publish_config(ConfigParam(
            data_id=self.data_id,
            group=self.group,
            content=content
        ))
    
    def watch_settings(
        self,
        settings: Any,
        keys: Optional[List[str]] = None,
        key_mapping: Optional[Dict[str, str]] = None,
    ) -> "NacosConfigManager":
        """
        监听pydantic_settings的Settings实例
        
        当Nacos配置变更时，自动更新Settings实例中指定的字段
        
        Parameters
        ----------
        settings : BaseSettings
            pydantic_settings的Settings实例
        keys : List[str], optional
            要监听的配置键列表，如果为None则监听所有可变字段
        key_mapping : Dict[str, str], optional
            Nacos配置键到Settings字段的映射关系
            例如: {"nacos.app.name": "APP_NAME"}
            
        Returns
        -------
        NacosConfigManager
            返回self，支持链式调用
            
        Example
        -------
        ```python
        class Settings(BaseSettings):
            APP_NAME: str = "myapp"
            DEBUG: bool = False
            
        settings = Settings()
        
        manager.watch_settings(
            settings, 
            keys=["APP_NAME", "DEBUG"],
            key_mapping={"app.name": "APP_NAME", "app.debug": "DEBUG"}
        )
        ```
        """
        # 如果没有指定keys，默认监听Settings的所有字段
        if keys is None and hasattr(settings, "model_fields"):
            keys = list(settings.model_fields.keys())
            
        adapter = SettingsAdapter(settings, keys, key_mapping)
        self._settings_adapters.append(adapter)
        return self
    
    def watch_module(
        self,
        module: ModuleType,
        keys: Optional[List[str]] = None,
        key_mapping: Optional[Dict[str, str]] = None,
    ) -> "NacosConfigManager":
        """
        监听Python模块中的变量
        
        当Nacos配置变更时，自动更新模块中指定的变量
        
        Parameters
        ----------
        module : ModuleType
            Python模块对象
        keys : List[str], optional
            要监听的变量名列表
        key_mapping : Dict[str, str], optional
            Nacos配置键到模块变量名的映射关系
            
        Returns
        -------
        NacosConfigManager
            返回self，支持链式调用
            
        Example
        -------
        ```python
        # config.py
        APP_NAME = "myapp"
        DEBUG = False
        
        # main.py
        import config
        manager.watch_module(
            config, 
            keys=["APP_NAME", "DEBUG"],
            key_mapping={"app.name": "APP_NAME"}
        )
        ```
        """
        # 如果没有指定keys，默认监听模块中所有的公开变量（不以_开头）
        if keys is None:
            keys = [
                name for name in dir(module) 
                if not name.startswith("_") and not callable(getattr(module, name))
            ]
            
        adapter = ModuleAdapter(module, keys, key_mapping)
        self._module_adapters.append(adapter)
        return self
    
    def add_callback(
        self, 
        callback: Callable[[Dict[str, Any]], Any]
    ) -> "NacosConfigManager":
        """
        添加自定义配置变更回调
        
        Parameters
        ----------
        callback : Callable[[Dict[str, Any]], Any]
            配置变更时的回调函数，接收解析后的配置字典
            支持同步和异步函数
            
        Returns
        -------
        NacosConfigManager
            返回self，支持链式调用
        """
        self._callbacks.append(callback)
        return self
    
    async def _on_config_change(
        self, 
        tenant: str, 
        data_id: str, 
        group: str, 
        content: str
    ) -> None:
        """
        配置变更回调处理（v2 API格式）
        
        Parameters
        ----------
        tenant : str
            命名空间ID
        data_id : str
            配置的Data ID
        group : str
            配置分组
        content : str
            配置内容
        """
        try:
            new_config = parse_config(content, self.config_format)
            
            async with self._lock:
                old_config = self._current_config.copy()
                self._current_config = new_config
            
            # 找出变更的配置
            changed_keys = self._get_changed_keys(old_config, new_config)
            
            if changed_keys:
                logger.info(f"检测到配置变更，变更的键: {changed_keys}")
                
                # 更新所有Settings适配器
                for adapter in self._settings_adapters:
                    try:
                        adapter.update(new_config, changed_keys)
                    except Exception as e:
                        logger.error(f"更新Settings适配器失败: {e}")
                
                # 更新所有模块适配器
                for adapter in self._module_adapters:
                    try:
                        adapter.update(new_config, changed_keys)
                    except Exception as e:
                        logger.error(f"更新模块适配器失败: {e}")
                
                # 执行自定义回调
                for callback in self._callbacks:
                    try:
                        result = callback(new_config)
                        # 如果是协程，等待它完成
                        if asyncio.iscoroutine(result):
                            await result
                    except Exception as e:
                        logger.error(f"执行配置变更回调失败: {e}")
                        
        except Exception as e:
            logger.error(f"处理配置变更失败: {e}")
    
    def _get_changed_keys(
        self, 
        old_config: Dict[str, Any], 
        new_config: Dict[str, Any]
    ) -> Set[str]:
        """
        获取变更的配置键
        """
        changed = set()
        all_keys = set(old_config.keys()) | set(new_config.keys())
        
        for key in all_keys:
            old_value = old_config.get(key)
            new_value = new_config.get(key)
            if old_value != new_value:
                changed.add(key)
                
        return changed
    
    async def start(self) -> None:
        """
        启动配置监听
        
        会先获取一次当前配置并应用到所有适配器，然后开始监听变更
        """
        if self._is_watching:
            logger.warning("配置监听已经启动")
            return
        ## 打印nacos配置
        print(f"nacos地址: {self.server_addresses}")
        print(f"nacos配置: {self.data_id}/{self.group}")
        await self._ensure_connected()
            
        # 首次获取配置
        try:
            self._current_config = await self.get_config_parsed()
            logger.info(f"获取初始配置成功: {self.data_id}/{self.group}")
            
            # 应用初始配置到所有适配器
            all_keys = set(self._current_config.keys())
            
            for adapter in self._settings_adapters:
                adapter.update(self._current_config, all_keys)
                
            for adapter in self._module_adapters:
                adapter.update(self._current_config, all_keys)
                
        except Exception as e:
            logger.error(f"获取初始配置失败: {e}")
            raise
        
        # 添加监听器
        await self._client.add_listener(
            data_id=self.data_id,
            group=self.group,
            listener=self._on_config_change
        )
        self._is_watching = True
        logger.info(f"配置监听已启动: {self.data_id}/{self.group}")
    
    async def stop(self) -> None:
        """
        停止配置监听并关闭连接
        """
        if not self._is_watching:
            return
        
        try:
            if self._client:
                await self._client.shutdown()
                self._client = None
        except Exception as e:
            logger.warning(f"关闭Nacos客户端失败: {e}")
            
        self._is_watching = False
        logger.info("配置监听已停止")
    
    async def __aenter__(self) -> "NacosConfigManager":
        """支持异步上下文管理器"""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """支持异步上下文管理器"""
        await self.stop()
