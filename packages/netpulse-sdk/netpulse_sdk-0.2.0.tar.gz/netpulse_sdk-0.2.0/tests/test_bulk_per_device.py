"""
测试 Bulk API 的每设备不同命令特性
"""

import pytest
from unittest.mock import Mock, patch
from netpulse_sdk import NetPulse


class TestBulkPerDeviceCommands:
    """测试每设备不同命令的功能"""

    def setup_method(self):
        """初始化测试客户端"""
        self.client = NetPulse(
            base_url="http://localhost:9000",
            api_key="test-api-key",
            driver="netmiko",
            default_connection_args={
                "device_type": "huawei",
                "username": "admin",
                "password": "admin",
            },
        )

    @patch('netpulse_sdk.transport.http.HTTPClient.post')
    def test_mixed_devices_with_and_without_command(self, mock_post):
        """测试混合使用：部分设备有命令，部分没有"""
        # 模拟 API 响应
        mock_post.return_value = {
            "code": 0,
            "message": "success",
            "data": {
                "succeeded": [
                    {"job_id": "job-1", "connection_args": {"host": "10.1.1.1"}},
                    {"job_id": "job-2", "connection_args": {"host": "10.1.1.2"}},
                    {"job_id": "job-3", "connection_args": {"host": "10.1.1.3"}},
                ],
                "failed": []
            }
        }

        # 调用 SDK
        job = self.client.collect(
            devices=[
                "10.1.1.1",  # 字符串格式，使用 base 命令
                {"host": "10.1.1.2", "command": "display power"},  # 覆盖命令
                {"host": "10.1.1.3", "command": "display device"},  # 覆盖命令
            ],
            commands="display version",  # base 命令
        )

        # 验证调用参数
        assert mock_post.called
        call_args = mock_post.call_args
        payload = call_args[1]['json']

        # 验证 payload 结构
        assert payload['driver'] == 'netmiko'
        assert payload['command'] == ['display version']  # base 命令
        assert len(payload['devices']) == 3

        # 验证第一个设备（字符串格式，转换为字典）
        assert payload['devices'][0] == {"host": "10.1.1.1"}

        # 验证第二个设备（保留 command 字段）
        assert payload['devices'][1]['host'] == "10.1.1.2"
        assert payload['devices'][1]['command'] == "display power"

        # 验证第三个设备（保留 command 字段）
        assert payload['devices'][2]['host'] == "10.1.1.3"
        assert payload['devices'][2]['command'] == "display device"

    @patch('netpulse_sdk.transport.http.HTTPClient.post')
    def test_all_devices_with_commands(self, mock_post):
        """测试所有设备都指定命令"""
        mock_post.return_value = {
            "code": 0,
            "message": "success",
            "data": {
                "succeeded": [
                    {"job_id": "job-1", "connection_args": {"host": "10.1.1.1"}},
                    {"job_id": "job-2", "connection_args": {"host": "10.1.1.2"}},
                ],
                "failed": []
            }
        }

        job = self.client.collect(
            devices=[
                {"host": "10.1.1.1", "command": "display version"},
                {"host": "10.1.1.2", "command": "display power"},
            ],
            commands="display version",
        )

        call_args = mock_post.call_args
        payload = call_args[1]['json']

        # 验证所有设备都保留了 command 字段
        assert payload['devices'][0]['command'] == "display version"
        assert payload['devices'][1]['command'] == "display power"

    @patch('netpulse_sdk.transport.http.HTTPClient.post')
    def test_config_per_device(self, mock_post):
        """测试每设备不同配置"""
        mock_post.return_value = {
            "code": 0,
            "message": "success",
            "data": {
                "succeeded": [
                    {"job_id": "job-1", "connection_args": {"host": "10.1.1.1"}},
                    {"job_id": "job-2", "connection_args": {"host": "10.1.1.2"}},
                ],
                "failed": []
            }
        }

        job = self.client.run(
            devices=[
                "10.1.1.1",  # 使用 base 配置
                {"host": "10.1.1.2", "config": "sysname Router-02"},  # 覆盖配置
            ],
            config="sysname Router-Default",
        )

        call_args = mock_post.call_args
        payload = call_args[1]['json']

        # 验证 payload
        assert payload['config'] == ['sysname Router-Default']  # base 配置
        assert payload['devices'][0] == {"host": "10.1.1.1"}
        assert payload['devices'][1]['host'] == "10.1.1.2"
        assert payload['devices'][1]['config'] == "sysname Router-02"

    @patch('netpulse_sdk.transport.http.HTTPClient.post')
    def test_command_list_per_device(self, mock_post):
        """测试每设备不同的命令列表"""
        mock_post.return_value = {
            "code": 0,
            "message": "success",
            "data": {
                "succeeded": [
                    {"job_id": "job-1", "connection_args": {"host": "10.1.1.1"}},
                    {"job_id": "job-2", "connection_args": {"host": "10.1.1.2"}},
                ],
                "failed": []
            }
        }

        job = self.client.collect(
            devices=[
                "10.1.1.1",
                {
                    "host": "10.1.1.2",
                    "command": ["display power", "display fan"]
                },
            ],
            commands=["display version", "display device"],
        )

        call_args = mock_post.call_args
        payload = call_args[1]['json']

        # 验证命令列表
        assert payload['command'] == ["display version", "display device"]
        assert payload['devices'][1]['command'] == ["display power", "display fan"]

    @patch('netpulse_sdk.transport.http.HTTPClient.post')
    def test_device_with_extra_fields(self, mock_post):
        """测试设备字典包含额外字段（如 connection_args）"""
        mock_post.return_value = {
            "code": 0,
            "message": "success",
            "data": {
                "succeeded": [
                    {"job_id": "job-1", "connection_args": {"host": "10.1.1.1"}},
                ],
                "failed": []
            }
        }

        # 使用 run 方法并指定 mode="bulk" 来强制使用 bulk API
        job = self.client.run(
            devices=[
                {
                    "host": "10.1.1.1",
                    "command": "display power",
                    "port": 22,
                    "device_type": "huawei_vrpv8",
                },
            ],
            commands="display version",
            mode="bulk",  # 强制使用 bulk 模式
        )

        call_args = mock_post.call_args
        payload = call_args[1]['json']

        # 验证所有字段都被保留
        device = payload['devices'][0]
        assert device['host'] == "10.1.1.1"
        assert device['command'] == "display power"
        assert device['port'] == 22
        assert device['device_type'] == "huawei_vrpv8"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

