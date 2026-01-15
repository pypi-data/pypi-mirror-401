"""
自然语言图标助手

使用自然语言描述来查找和点击图标
支持中文描述，例如："点击右上角的设置按钮"
"""

import re
import logging
from typing import Optional, Dict, Any, List
from .icon_helper import IconHelper

logger = logging.getLogger(__name__)


class NLPIconHelper:
    """自然语言图标助手"""

    def __init__(self, device):
        """
        初始化 NLP 图标助手

        Args:
            device: AndroidDeviceManager 实验实例
        """
        self.device = device
        self.helper = IconHelper(device)

        # 关键词映射
        self.position_keywords = {
            '左上': {'x_range': (0, 400), 'y_range': (0, 400)},
            '右上': {'x_range': (800, 1080), 'y_range': (0, 400)},
            '左下': {'x_range': (0, 400), 'y_range': (1800, 2264)},
            '右下': {'x_range': (800, 1080), 'y_range': (1800, 2264)},
            '顶部': {'y_range': (0, 600)},
            '底部': {'y_range': (1800, 2264)},
            '左侧': {'x_range': (0, 400)},
            '右侧': {'x_range': (800, 1080)},
            '中间': {'x_range': (400, 800), 'y_range': (600, 1800)},
            '中央': {'x_range': (400, 800), 'y_range': (600, 1800)},
        }

        self.type_keywords = {
            '图标': ['ImageView', 'ImageButton'],
            '按钮': ['Button', 'ImageButton', 'FrameLayout'],
            '文字': ['TextView', 'EditText'],
            '输入框': ['EditText'],
        }

    def parse_description(self, description: str) -> Dict[str, Any]:
        """
        解析自然语言描述

        Args:
            description: 自然语言描述，例如："点击右上角的设置按钮"

        Returns:
            解析结果字典，包含位置、类型、文本等
        """
        result = {
            'action': '点击',
            'position': None,
            'type': None,
            'text': None,
            'description': None,
            'id': None,
        }

        # 解析动作
        if '点击' in description:
            result['action'] = '点击'
        elif '长按' in description:
            result['action'] = '长按'
        elif '滑动' in description:
            result['action'] = '滑动'

        # 解析位置关键词
        for pos_name, pos_range in self.position_keywords.items():
            if pos_name in description:
                result['position'] = pos_name
                result['position_range'] = pos_range
                break

        # 解析类型关键词
        for type_name, type_classes in self.type_keywords.items():
            if type_name in description:
                result['type'] = type_name
                result['type_classes'] = type_classes
                break

        # 解析文本内容（使用引号或直接提取）
        # 查找引号中的内容
        quoted_texts = re.findall(r'["\"](.*?)["\"]', description)
        if quoted_texts:
            result['text'] = quoted_texts[0]
        else:
            # 查找常见关键词后面的内容
            for keyword in ['名为', '叫做', '显示', '内容是', '文字是']:
                if keyword in description:
                    parts = description.split(keyword)
                    if len(parts) > 1:
                        result['text'] = parts[1].strip().split(' ')[0].strip('的，。')
                        break

        # 解析描述性关键词（content-desc）
        desc_keywords = ['设置', '搜索', '返回', '菜单', '首页', '我的', '收藏', '分享', '删除', '编辑']
        for keyword in desc_keywords:
            if keyword in description and result['text'] is None:
                result['description'] = keyword
                break

        return result

    def find_icon_by_nlp(self, description: str) -> Optional[Dict[str, Any]]:
        """
        根据自然语言描述查找图标

        Args:
            description: 自然语言描述

        Returns:
            匹配的图标元素，如果未找到返回 None
        """
        parsed = self.parse_description(description)

        logger.info(f"解析结果: {parsed}")

        # 策略1: 如果有明确的文本描述，优先使用文本查找
        if parsed['text']:
            logger.info(f"通过文本查找: {parsed['text']}")
            icon = self.helper.find_icon_by_text(parsed['text'])
            if icon:
                return icon

        # 策略2: 如果有描述关键词，使用描述查找
        if parsed['description']:
            logger.info(f"通过描述查找: {parsed['description']}")
            icon = self.helper.find_icon_by_description(parsed['description'])
            if icon:
                return icon

        # 策略3: 根据位置和类型筛选
        candidates = []

        # 获取所有可点击图标
        if parsed.get('type') == '图标':
            icons = self.helper.find_all_icons('ImageView')
        elif parsed.get('type') == '按钮':
            icons = self.helper.find_clickable_icons()
        else:
            icons = self.helper.find_clickable_icons()

        # 根据位置筛选
        if parsed.get('position'):
            pos_range = parsed['position_range']

            for icon in icons:
                center = icon.get('center', {})
                x, y = center.get('x', 0), center.get('y', 0)

                # 检查是否在位置范围内
                in_range = True

                if 'x_range' in pos_range:
                    x_min, x_max = pos_range['x_range']
                    if not (x_min <= x <= x_max):
                        in_range = False

                if 'y_range' in pos_range:
                    y_min, y_max = pos_range['y_range']
                    if not (y_min <= y <= y_max):
                        in_range = False

                if in_range:
                    candidates.append(icon)
        else:
            candidates = icons

        # 返回第一个候选
        if candidates:
            logger.info(f"找到 {len(candidates)} 个候选图标，返回第一个")
            return candidates[0]

        logger.warning("未找到匹配的图标")
        return None

    def tap_by_nlp(self, description: str) -> bool:
        """
        根据自然语言描述点击图标

        Args:
            description: 自然语言描述，例如："点击右上角的设置按钮"

        Returns:
            是否成功点击
        """
        print(f"\n🔍 解析描述: \"{description}\"")

        icon = self.find_icon_by_nlp(description)

        if icon:
            # 显示图标信息
            text = icon.get('text', '')
            desc = icon.get('content_desc', '')
            res_id = icon.get('resource_id', '').split('/')[-1]
            center = icon.get('center', {})

            print(f"✅ 找到图标:")
            if text:
                print(f"   文本: \"{text}\"")
            if desc:
                print(f"   描述: \"{desc}\"")
            if res_id:
                print(f"   ID: ...{res_id}")
            print(f"   位置: ({center.get('x', 0)}, {center.get('y', 0)})")

            # 点击
            success = self.helper.tap_icon(icon)

            if success:
                print(f"✅ 成功点击")
            else:
                print(f"❌ 点击失败")

            return success
        else:
            print(f"❌ 未找到匹配的图标")
            return False

    def batch_tap_by_nlp(self, descriptions: List[str]) -> List[bool]:
        """
        批量执行自然语言描述的点击操作

        Args:
            descriptions: 描述列表

        Returns:
            结果列表
        """
        results = []

        for desc in descriptions:
            result = self.tap_by_nlp(desc)
            results.append(result)

            import time
            time.sleep(1)  # 等待操作完成

        return results

    def interactive_mode(self):
        """交互式模式：让用户输入描述并执行"""
        print("\n" + "=" * 60)
        print("自然语言图标点击 - 交互式模式")
        print("=" * 60)
        print("\n输入描述来点击图标，例如：")
        print("  - 点击设置按钮")
        print("  - 点击右上角的菜单图标")
        print("  - 点击底部的学习标签")
        print("  - 点击返回按钮")
        print("\n输入 'quit' 退出\n")

        while True:
            try:
                user_input = input("请输入描述: ").strip()

                if user_input.lower() in ['quit', 'exit', 'q', '退出']:
                    print("\n退出交互模式")
                    break

                if not user_input:
                    continue

                self.tap_by_nlp(user_input)

                import time
                time.sleep(1)

            except KeyboardInterrupt:
                print("\n\n退出交互模式")
                break
            except Exception as e:
                print(f"\n❌ 错误: {e}")


# 演示和测试
if __name__ == '__main__':
    import sys
    sys.path.insert(0, '.')

    from rpa_core.android import create_android_device
    import time

    device = create_android_device()
    nlp_helper = NLPIconHelper(device)

    print("=" * 60)
    print("自然语言图标点击演示")
    print("=" * 60)

    # 测试用例
    test_descriptions = [
        "点击学习标签",
        "点击设置按钮",
        "点击返回按钮",
        "点击右上角的菜单图标",
        "点击底部的我的标签",
    ]

    print("\n执行测试用例:\n")

    for desc in test_descriptions:
        print(f"\n描述: {desc}")
        print("-" * 40)

        parsed = nlp_helper.parse_description(desc)
        print(f"解析: {parsed}")

        icon = nlp_helper.find_icon_by_nlp(desc)
        if icon:
            print("✅ 找到图标")
            # 不实际点击，只演示
        else:
            print("❌ 未找到图标")

    # 交互式模式
    print("\n\n" + "=" * 60)
    nlp_helper.interactive_mode()

    device.close()
