import json
from dtsdance.bytecloud import ByteCloudClient
from dtsdance.spacex import GatewayInfo, SpaceXClient
from config import load_site_configs

site = "boe"
site_configs = load_site_configs([site])
bytecloud_client = ByteCloudClient(site_configs)
spacex = SpaceXClient(bytecloud_client)


# pytest tests/test_spacex.py::test_list_mgr -s
def test_list_mgr():
    mgr_list = spacex.list_mgr(site)
    print(f"mgr_list: {json.dumps(mgr_list, indent=2, ensure_ascii=False)}")


# pytest tests/test_spacex.py::test_register_gateway -s
def test_register_gateway():
    gateway_info = GatewayInfo(
        mgr_env="boe",
        ctrl_name="boe_halo_test",
        gateway_endpoint="volc.dts.gateway.service.boe:cluster:boe_halo_test:family:v6",
        auth_user="bytedts_backend",
        auth_password="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJieXRlZHRzX2JhY2tlbmQiLCJleHAiOjQ4OTEzMzQ0MDAsImRvbWFpbiI6IioifQ.D_87X-JCQn1CU9ru3PpeM1lmlOgVki6bVHo-kQ60eio",
        root_secret_key="97oscH5k",
        gw_meta_db="bytedts_sre_halo",
    )
    result = spacex.register_gateway(site, gateway_info)
    print(f"result: {result}")
