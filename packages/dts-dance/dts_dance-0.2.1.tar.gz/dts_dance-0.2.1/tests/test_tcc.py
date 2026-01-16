from config import load_site_configs
from dtsdance.bytecloud import ByteCloudClient
from dtsdance.tcc_open import TCCClient
from dtsdance.tcc_inner import TCCInnerClient

site_configs = load_site_configs(["boe", "us-ttp"])
bytecloud_client = ByteCloudClient(site_configs)
client_inner = TCCInnerClient(bytecloud_client)


# pytest tests/test_tcc.py::test_get_config -s
def test_get_config():
    site_info = site_configs["boe"]
    client_open = TCCClient(site_info.svc_account, site_info.svc_secret, endpoint=site_info.endpoint)
    config_ctrl_env = client_open.get_config(ns_name="bytedts.mgr.api", region="China-BOE", dir="/default", conf_name="ctrl_env1")
    print(f"ctrl_env: {config_ctrl_env}")


# pytest tests/test_tcc.py::test_list_configs -s
def test_list_configs():
    configs = client_inner.list_configs(site="us-ttp", ns_name="bytedts.mgr.api", region="US-TTP", dir="/default", conf_name="ctrl_env")
    print(f"configs: {configs}")
