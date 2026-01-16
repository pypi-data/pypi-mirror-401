import os
from typing import Any
import yaml
from dtsdance.bytecloud import SiteConfig


def load_site_configs(sites: list[str] | None = None) -> dict[str, SiteConfig]:
    """从配置文件加载配置

    Returns:
        dict[str, Any]: 应用配置字典

    Raises:
        ValueError: 配置文件加载错误
    """
    config_path = os.environ.get("CONFIG_PATH", "config.yaml")

    configs: dict[str, Any] = {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            configs = yaml.safe_load(f)

    except Exception as e:
        raise ValueError(f"加载配置失败: {e}")

    return {
        k: SiteConfig(k, v["endpoint"], v["svc_account"], v["svc_secret"], v.get("endpoint_bytedts_spacex", None))
        for k, v in configs["sites"].items()
        if k in sites
    }
