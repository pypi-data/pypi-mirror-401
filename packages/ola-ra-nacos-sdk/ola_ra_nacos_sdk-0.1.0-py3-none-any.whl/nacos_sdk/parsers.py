"""
配置解析器
=========

支持多种配置格式的解析：
- properties
- yaml
- json
"""

import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def parse_config(raw_content: str, config_format: str = "properties") -> Dict[str, Any]:
    """
    解析配置内容
    
    Parameters
    ----------
    raw_content : str
        原始配置内容
    config_format : str
        配置格式: "properties", "yaml", "json"
        
    Returns
    -------
    Dict[str, Any]
        解析后的配置字典
    """
    if not raw_content:
        return {}
        
    config_format = config_format.lower()
    
    if config_format == "properties":
        return parse_properties(raw_content)
    elif config_format in ("yaml", "yml"):
        return parse_yaml(raw_content)
    elif config_format == "json":
        return parse_json(raw_content)
    else:
        logger.warning(f"未知的配置格式: {config_format}，尝试使用properties格式解析")
        return parse_properties(raw_content)


def parse_properties(content: str) -> Dict[str, Any]:
    """
    解析properties格式配置
    
    支持的格式：
    - key=value
    - key = value
    - # 注释行
    - 空行
    
    Parameters
    ----------
    content : str
        properties格式的配置内容
        
    Returns
    -------
    Dict[str, Any]
        解析后的配置字典
    """
    result = {}
    
    for line in content.splitlines():
        line = line.strip()
        
        # 跳过空行和注释
        if not line or line.startswith("#") or line.startswith("!"):
            continue
        
        # 查找分隔符位置
        sep_idx = -1
        for i, char in enumerate(line):
            if char in ("=", ":"):
                # 检查是否被转义
                if i > 0 and line[i-1] == "\\":
                    continue
                sep_idx = i
                break
        
        if sep_idx == -1:
            continue
            
        key = line[:sep_idx].strip()
        value = line[sep_idx + 1:].strip()
        
        # 处理转义字符
        value = value.replace("\\=", "=").replace("\\:", ":")
        
        # 尝试自动类型转换
        result[key] = auto_convert(value)
        
    return result


def parse_yaml(content: str) -> Dict[str, Any]:
    """
    解析YAML格式配置
    
    Parameters
    ----------
    content : str
        YAML格式的配置内容
        
    Returns
    -------
    Dict[str, Any]
        解析后的配置字典
    """
    try:
        import yaml
    except ImportError:
        raise ImportError("请安装PyYAML: pip install pyyaml")
    
    try:
        result = yaml.safe_load(content)
        if result is None:
            return {}
        if not isinstance(result, dict):
            logger.warning("YAML内容不是字典格式，将其包装为{'value': content}")
            return {"value": result}
        # 展平嵌套字典
        return flatten_dict(result)
    except yaml.YAMLError as e:
        logger.error(f"解析YAML失败: {e}")
        return {}


def parse_json(content: str) -> Dict[str, Any]:
    """
    解析JSON格式配置
    
    Parameters
    ----------
    content : str
        JSON格式的配置内容
        
    Returns
    -------
    Dict[str, Any]
        解析后的配置字典
    """
    try:
        result = json.loads(content)
        if not isinstance(result, dict):
            logger.warning("JSON内容不是字典格式，将其包装为{'value': content}")
            return {"value": result}
        # 展平嵌套字典
        return flatten_dict(result)
    except json.JSONDecodeError as e:
        logger.error(f"解析JSON失败: {e}")
        return {}


def flatten_dict(
    d: Dict[str, Any], 
    parent_key: str = "", 
    sep: str = "."
) -> Dict[str, Any]:
    """
    展平嵌套字典
    
    将嵌套的字典展平为单层字典，使用点号连接键名
    
    Example
    -------
    {"app": {"name": "test"}} -> {"app.name": "test"}
    
    Parameters
    ----------
    d : Dict[str, Any]
        要展平的字典
    parent_key : str
        父键前缀
    sep : str
        键名分隔符
        
    Returns
    -------
    Dict[str, Any]
        展平后的字典
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def auto_convert(value: str) -> Any:
    """
    自动类型转换
    
    尝试将字符串值转换为适当的Python类型
    
    Parameters
    ----------
    value : str
        要转换的字符串值
        
    Returns
    -------
    Any
        转换后的值
    """
    if not isinstance(value, str):
        return value
        
    # 布尔值
    lower_value = value.lower()
    if lower_value in ("true", "yes", "on"):
        return True
    if lower_value in ("false", "no", "off"):
        return False
    
    # null/none
    if lower_value in ("null", "none", ""):
        return None
    
    # 整数
    try:
        return int(value)
    except ValueError:
        pass
    
    # 浮点数
    try:
        return float(value)
    except ValueError:
        pass
    
    # 保持原始字符串
    return value

