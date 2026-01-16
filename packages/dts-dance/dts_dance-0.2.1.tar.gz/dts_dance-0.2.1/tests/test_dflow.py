from dtsdance.dflow import DFlowClient
from dtsdance.bytecloud import ByteCloudClient

from config import load_site_configs

site_configs = load_site_configs(["boe", "cn"])
bytecloud_client = ByteCloudClient(site_configs)
dflow_client = DFlowClient(bytecloud_client)


# pytest tests/test_dflow.py::test_get_task_info -s
def test_get_task_info():
    info = dflow_client.get_task_info("cn", "106037095986690")
    print(f"DFlow Info: {info}")

# pytest tests/test_dflow.py::test_get_dflow_info -s
def test_get_dflow_info():
    info = dflow_client.get_dflow_info("cn", "106029334786818")
    print(f"DFlow Info: {info}")
