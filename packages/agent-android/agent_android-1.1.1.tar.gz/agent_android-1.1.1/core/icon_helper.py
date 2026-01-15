"""
图标查找和点击工具类

提供多种方式定位和点击 Android 应用中的图标
"""

import re
import logging
from typing import Optional, Dict, Any, List
from xml.etree.ElementTree import Element

logger = logging.getLogger(__name__)


class IconHelper:
    """图标查找和点击助手"""

    def __init__(self, device):
        """
        初始化图标助手

        Args:
            device: AndroidDeviceManager 实例
        """
        self.device = device

    def find_icon_by_text(self, text: str, exact_match: bool = False) -> Optional[Dict[str, Any]]:
        """
        通过文本查找图标（推荐用于有文字的图标）

        Args:
            text: 图标文本
            exact_match: 是否精确匹配（False 为包含匹配）

        Returns:
            元素信息字典
        """
        strategy = "text" if exact_match else "text_contains"
        return self.device.find_element({"strategy": strategy, "value": text})

    def find_icon_by_description(self, description: str) -> Optional[Dict[str, Any]]:
        """
        通过 content-desc 查找图标（推荐）

        Args:
            description: 图标的内容描述

        Returns:
            元素信息字典
        """
        return self.device.find_element({
            "strategy": "content-desc",
            "value": description
        })

    def find_icon_by_id(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """
        通过 resource-id 查找图标

        Args:
            resource_id: 资源 ID

        Returns:
            元素信息字典
        """
        return self.device.find_element({
            "strategy": "id",
            "value": resource_id
        })

    def find_all_icons(self, icon_type: str = "ImageView") -> List[Dict[str, Any]]:
        """
        查找所有指定类型的图标

        Args:
            icon_type: 图标类型 (ImageView, ImageButton, FrameLayout 等)

        Returns:
            图标元素列表
        """
        ui_dump = self.device.get_ui_dump(force_refresh=True)
        icons = []

        for node in ui_dump.iter():
            class_name = node.get('class', '')

            if icon_type in class_name:
                element = self.device._parse_element_info(node)
                icons.append(element)

        return icons

    def find_clickable_icons(self) -> List[Dict[str, Any]]:
        """
        查找所有可点击的图标

        Returns:
            可点击图标列表
        """
        ui_dump = self.device.get_ui_dump(force_refresh=True)
        clickable_icons = []

        for node in ui_dump.iter():
            clickable = node.get('clickable', 'false') == 'true'
            class_name = node.get('class', '')

            # 检查是否是图标类型
            is_icon = any(t in class_name for t in ['ImageView', 'ImageButton', 'FrameLayout'])

            if is_icon and clickable:
                element = self.device._parse_element_info(node)
                clickable_icons.append(element)

        return clickable_icons

    def find_icon_by_position(self, x: int, y: int, tolerance: int = 50) -> Optional[Dict[str, Any]]:
        """
        通过坐标附近查找图标

        Args:
            x: X 坐标
            y: Y 坐标
            tolerance: 容差范围（像素）

        Returns:
            图标元素字典
        """
        ui_dump = self.device.get_ui_dump(force_refresh=True)

        for node in ui_dump.iter():
            bounds = node.get('bounds', '')
            if bounds:
                match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
                if match:
                    x1, y1, x2, y2 = map(int, match.groups())

                    # 检查坐标是否在 bounds 容差范围内
                    if (x1 - tolerance <= x <= x2 + tolerance and
                        y1 - tolerance <= y <= y2 + tolerance):

                        element = self.device._parse_element_info(node)
                        return element

        return None

    def find_icon_near_text(self, text: str, max_distance: int = 200) -> Optional[Dict[str, Any]]:
        """
        查找文本附近的图标（例如：文字旁边的图标按钮）

        Args:
            text: 参考文本
            max_distance: 最大距离（像素）

        Returns:
            图标元素字典
        """
        # 先找到文本元素
        text_element = self.find_icon_by_text(text)
        if not text_element:
            return None

        text_center = text_element.get('center', {})
        text_x, text_y = text_center.get('x', 0), text_center.get('y', 0)

        # 查找附近的图标
        ui_dump = self.device.get_ui_dump(force_refresh=True)

        closest_icon = None
        min_distance = float('inf')

        for node in ui_dump.iter():
            class_name = node.get('class', '')
            is_icon = any(t in class_name for t in ['ImageView', 'ImageButton'])

            if is_icon:
                element = self.device._parse_element_info(node)
                icon_center = element.get('center', {})
                icon_x, icon_y = icon_center.get('x', 0), icon_center.get('y', 0)

                # 计算距离
                distance = ((icon_x - text_x) ** 2 + (icon_y - text_y) ** 2) ** 0.5

                if distance < min_distance and distance <= max_distance:
                    min_distance = distance
                    closest_icon = element

        return closest_icon

    def tap_icon(self, icon: Dict[str, Any]) -> bool:
        """
        点击图标

        Args:
            icon: 图标元素字典

        Returns:
            是否成功
        """
        if not icon:
            logger.warning("图标元素为空，无法点击")
            return False

        center = icon.get('center', {})
        x, y = center.get('x', 0), center.get('y', 0)

        if x == 0 and y == 0:
            logger.warning("图标坐标无效，无法点击")
            return False

        return self.device.tap(x, y)

    def tap_icon_by_description(self, description: str) -> bool:
        """
        通过描述点击图标（便捷方法）

        Args:
            description: 图标描述

        Returns:
            是否成功
        """
        icon = self.find_icon_by_description(description)
        if icon:
            logger.info(f"通过描述点击图标: {description}")
            return self.tap_icon(icon)
        else:
            logger.warning(f"未找到描述为 '{description}' 的图标")
            return False

    def tap_icon_by_text(self, text: str) -> bool:
        """
        通过文本点击图标（便捷方法）

        Args:
            text: 图标文本

        Returns:
            是否成功
        """
        icon = self.find_icon_by_text(text)
        if icon:
            logger.info(f"通过文本点击图标: {text}")
            return self.tap_icon(icon)
        else:
            logger.warning(f"未找到文本为 '{text}' 的图标")
            return False

    def print_all_clickable_icons(self):
        """打印所有可点击的图标（调试用）"""
        icons = self.find_clickable_icons()

        print(f"\n找到 {len(icons)} 个可点击图标:\n")

        for i, icon in enumerate(icons, 1):
            text = icon.get('text', '')
            resource_id = icon.get('resource_id', '')
            content_desc = icon.get('content_desc', '')
            class_name = icon.get('class', '').split('.')[-1]
            center = icon.get('center', {})

            print(f"{i}. {class_name}")
            if text:
                print(f"   文本: \"{text}\"")
            if content_desc:
                print(f"   描述: \"{content_desc}\"")
            if resource_id:
                print(f"   ID: {resource_id}")
            print(f"   位置: ({center.get('x', 0)}, {center.get('y', 0)})")
            print()


if __name__ == '__main__':
    """测试图标助手"""
    import sys
    sys.path.insert(0, '.')

    from rpa_core.android import create_android_device
    import time

    device = create_android_device()
    helper = IconHelper(device)

    # 打印所有可点击图标
    helper.print_all_clickable_icons()

    device.close()
