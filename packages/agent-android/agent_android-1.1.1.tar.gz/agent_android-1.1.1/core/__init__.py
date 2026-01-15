"""
agent-android Core Module

Android ADB 自动化核心模块
"""

from .android import AndroidDeviceManager, create_android_device
from .adb_config import ADBConfig
from .icon_helper import IconHelper
from .nlp_icon_helper import NLPIconHelper
from .multi_device import MultiDeviceManager, create_multi_device_manager

__all__ = [
    'AndroidDeviceManager',
    'create_android_device',
    'ADBConfig',
    'IconHelper',
    'NLPIconHelper',
    'MultiDeviceManager',
    'create_multi_device_manager',
]

__version__ = '1.0.0'
