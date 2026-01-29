"""
配置适配器
=========

提供两种适配器，用于将Nacos配置更新到不同类型的目标：
1. SettingsAdapter - 适配pydantic_settings
2. ModuleAdapter - 适配Python模块变量
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set
from types import ModuleType

logger = logging.getLogger(__name__)


class BaseAdapter(ABC):
    """
    适配器基类
    """
    
    def __init__(
        self,
        keys: Optional[List[str]] = None,
        key_mapping: Optional[Dict[str, str]] = None,
    ):
        """
        Parameters
        ----------
        keys : List[str], optional
            要监听的配置键列表
        key_mapping : Dict[str, str], optional
            Nacos配置键到目标字段/变量的映射关系
        """
        self.keys = set(keys) if keys else None
        self.key_mapping = key_mapping or {}
        # 反向映射：目标名 -> nacos键
        self._reverse_mapping = {v: k for k, v in self.key_mapping.items()}
        
    def _get_target_key(self, nacos_key: str) -> str:
        """
        获取目标键名
        
        如果有映射关系则使用映射，否则使用原始键名
        """
        return self.key_mapping.get(nacos_key, nacos_key)
    
    def _should_update(self, nacos_key: str, target_key: str) -> bool:
        """
        判断是否应该更新该配置
        """
        if self.keys is None:
            return True
        # 检查nacos键或目标键是否在监听列表中
        return nacos_key in self.keys or target_key in self.keys
    
    @abstractmethod
    def update(
        self, 
        config: Dict[str, Any], 
        changed_keys: Set[str]
    ) -> None:
        """
        更新配置
        
        Parameters
        ----------
        config : Dict[str, Any]
            完整的配置字典
        changed_keys : Set[str]
            变更的配置键集合
        """
        pass


class SettingsAdapter(BaseAdapter):
    """
    pydantic_settings适配器
    
    用于将Nacos配置更新到pydantic_settings的Settings实例
    
    Example
    -------
    ```python
    from pydantic_settings import BaseSettings
    
    class Settings(BaseSettings):
        APP_NAME: str = "myapp"
        DEBUG: bool = False
        
    settings = Settings()
    
    adapter = SettingsAdapter(
        settings, 
        keys=["APP_NAME", "DEBUG"],
        key_mapping={"app.name": "APP_NAME"}
    )
    
    adapter.update({"app.name": "newapp", "app.debug": True}, {"app.name"})
    print(settings.APP_NAME)  # "newapp"
    ```
    """
    
    def __init__(
        self,
        settings: Any,
        keys: Optional[List[str]] = None,
        key_mapping: Optional[Dict[str, str]] = None,
    ):
        """
        Parameters
        ----------
        settings : BaseSettings
            pydantic_settings的Settings实例
        keys : List[str], optional
            要监听的Settings字段名列表
        key_mapping : Dict[str, str], optional
            Nacos配置键到Settings字段名的映射关系
        """
        super().__init__(keys, key_mapping)
        self.settings = settings
        
        # 验证settings是否为pydantic模型
        if not hasattr(settings, "model_fields"):
            raise TypeError(
                "settings必须是pydantic BaseModel或pydantic_settings BaseSettings的实例"
            )
        
        # 获取所有可用字段
        self._available_fields = set(settings.model_fields.keys())
        
        # 构建字段名映射：小写 -> 实际字段名（用于大小写不敏感匹配）
        self._field_name_mapping: Dict[str, str] = {
            field.lower(): field for field in self._available_fields
        }
        
        # 构建小写的 keys 集合（用于大小写不敏感匹配）
        self._keys_lower: Set[str] = {
            k.lower() for k in self.keys
        } if self.keys else set()
        
        # 验证keys是否都是有效字段
        if keys:
            invalid_keys = set(keys) - self._available_fields
            if invalid_keys:
                logger.warning(
                    f"以下keys在Settings中不存在: {invalid_keys}"
                )
    
    def _should_update(self, nacos_key: str, target_key: str) -> bool:
        """
        判断是否应该更新该配置（大小写不敏感匹配）
        
        覆盖父类方法，支持大小写不敏感匹配
        """
        if self.keys is None:
            return True
        # 大小写不敏感匹配
        nacos_key_lower = nacos_key.lower()
        target_key_lower = target_key.lower()
        return nacos_key_lower in self._keys_lower or target_key_lower in self._keys_lower
    
    def _resolve_field_name(self, key: str) -> Optional[str]:
        """
        解析字段名（支持大小写不敏感匹配）
        
        Parameters
        ----------
        key : str
            配置键名
            
        Returns
        -------
        Optional[str]
            匹配到的实际字段名，如果没有匹配则返回None
        """
        # 直接匹配
        if key in self._available_fields:
            return key
        # 大小写不敏感匹配
        key_lower = key.lower()
        if key_lower in self._field_name_mapping:
            return self._field_name_mapping[key_lower]
        return None
    
    def update(
        self, 
        config: Dict[str, Any], 
        changed_keys: Set[str]
    ) -> None:
        """
        更新Settings实例中的配置
        """
        if not changed_keys:
            return
            
        for nacos_key in changed_keys:
            target_key = self._get_target_key(nacos_key)
            
            if not self._should_update(nacos_key, target_key):
                continue
            
            # 解析实际的字段名（支持大小写不敏感匹配）
            resolved_key = self._resolve_field_name(target_key)
            if resolved_key is None:
                # 尝试使用nacos_key作为目标键
                resolved_key = self._resolve_field_name(nacos_key)
                if resolved_key is None:
                    continue
            target_key = resolved_key
            
            if nacos_key in config:
                new_value = config[nacos_key]
                
                # 如果值为空则跳过更新
                if new_value is None or new_value == "":
                    continue
                
                try:
                    # 获取字段类型信息进行类型转换
                    field_info = self.settings.model_fields.get(target_key)
                    if field_info:
                        new_value = self._convert_type(
                            new_value, 
                            field_info.annotation
                        )
                    
                    # 直接设置属性值
                    # 注意：pydantic v2使用model_config来控制是否允许修改
                    object.__setattr__(self.settings, target_key, new_value)
                    logger.info(
                        f"已更新Settings.{target_key} = {new_value}"
                    )
                except Exception as e:
                    logger.error(
                        f"更新Settings.{target_key}失败: {e}"
                    )
    
    def _convert_type(self, value: Any, target_type: Any) -> Any:
        """
        将值转换为目标类型
        """
        if target_type is None or value is None:
            return value
            
        # 获取实际类型（处理Optional等）
        origin = getattr(target_type, "__origin__", None)
        if origin is not None:
            # 处理Union类型（包括Optional）
            args = getattr(target_type, "__args__", ())
            if args:
                # 尝试使用第一个非None类型
                for arg in args:
                    if arg is not type(None):
                        target_type = arg
                        break
        
        # 如果已经是目标类型则直接返回
        if isinstance(value, target_type):
            return value
        
        # 类型转换
        try:
            if target_type == bool:
                if isinstance(value, str):
                    return value.lower() in ("true", "1", "yes", "on")
                return bool(value)
            elif target_type == int:
                return int(value)
            elif target_type == float:
                return float(value)
            elif target_type == str:
                return str(value)
            elif target_type == list:
                if isinstance(value, str):
                    return [v.strip() for v in value.split(",")]
                return list(value)
            else:
                return target_type(value)
        except (ValueError, TypeError):
            return value


class ModuleAdapter(BaseAdapter):
    """
    模块变量适配器
    
    用于将Nacos配置更新到Python模块中的变量
    
    Example
    -------
    ```python
    # config.py
    APP_NAME = "myapp"
    DEBUG = False
    
    # main.py
    import config
    
    adapter = ModuleAdapter(
        config, 
        keys=["APP_NAME", "DEBUG"]
    )
    
    adapter.update({"APP_NAME": "newapp"}, {"APP_NAME"})
    print(config.APP_NAME)  # "newapp"
    ```
    """
    
    def __init__(
        self,
        module: ModuleType,
        keys: Optional[List[str]] = None,
        key_mapping: Optional[Dict[str, str]] = None,
    ):
        """
        Parameters
        ----------
        module : ModuleType
            Python模块对象
        keys : List[str], optional
            要监听的变量名列表
        key_mapping : Dict[str, str], optional
            Nacos配置键到模块变量名的映射关系
        """
        super().__init__(keys, key_mapping)
        self.module = module
        
        # 记录原始值的类型，用于类型转换
        self._original_types: Dict[str, type] = {}
        if keys:
            for key in keys:
                if hasattr(module, key):
                    self._original_types[key] = type(getattr(module, key))
    
    def update(
        self, 
        config: Dict[str, Any], 
        changed_keys: Set[str]
    ) -> None:
        """
        更新模块中的变量
        """
        if not changed_keys:
            return
            
        for nacos_key in changed_keys:
            target_key = self._get_target_key(nacos_key)
            
            if not self._should_update(nacos_key, target_key):
                continue
            
            # 检查模块是否有该属性
            if not hasattr(self.module, target_key):
                # 尝试使用nacos_key作为目标键
                if hasattr(self.module, nacos_key):
                    target_key = nacos_key
                else:
                    continue
            
            if nacos_key in config:
                new_value = config[nacos_key]
                
                # 如果值为空则跳过更新
                if new_value is None or new_value == "":
                    continue
                
                try:
                    # 类型转换
                    if target_key in self._original_types:
                        new_value = self._convert_type(
                            new_value, 
                            self._original_types[target_key]
                        )
                    
                    setattr(self.module, target_key, new_value)
                    logger.info(
                        f"已更新{self.module.__name__}.{target_key} = {new_value}"
                    )
                except Exception as e:
                    logger.error(
                        f"更新{self.module.__name__}.{target_key}失败: {e}"
                    )
    
    def _convert_type(self, value: Any, target_type: type) -> Any:
        """
        将值转换为目标类型
        """
        if isinstance(value, target_type):
            return value
            
        try:
            if target_type == bool:
                if isinstance(value, str):
                    return value.lower() in ("true", "1", "yes", "on")
                return bool(value)
            elif target_type == int:
                return int(value)
            elif target_type == float:
                return float(value)
            elif target_type == str:
                return str(value)
            elif target_type == list:
                if isinstance(value, str):
                    return [v.strip() for v in value.split(",")]
                return list(value)
            else:
                return target_type(value)
        except (ValueError, TypeError):
            return value

