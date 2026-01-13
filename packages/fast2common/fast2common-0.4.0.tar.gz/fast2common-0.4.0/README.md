# Fast2 Common

Fast2 Common 是一个强大的 Android 自动化测试和 UI 交互工具包，提供了一系列可复用的模块，用于简化 Android 应用的自动化测试开发。

## 功能特性

- **ADB 控制器 (ADBController)**: 封装了常用的 ADB 命令，提供简洁的 Python API
- **UI 分析器 (UIAnalyzer)**: 分析 UI 层级结构，提取元素信息
- **UI 交互工具 (UIInteraction)**: 提供点击、滑动等 UI 交互功能
- **AI Tab 管理器 (TabManager)**: 智能管理和切换底部导航栏
- **探索策略 (ExplorationStrategy)**: 自动化应用探索策略
- **AI 客户端 (AIClient)**: 集成智谱 AI，提供智能分析能力
- **元素定位器 (ElementLocator)**: 通过文字查找元素坐标
- **图标定位器 (IconLocator)**: 基于视觉识别的图标定位
- **文字定位器 (TextLocator)**: 智能文字匹配和定位
- **动画检测器 (AnimationDetector)**: 检测 UI 动画状态
- **坐标转换器 (CoordinateConverter)**: 屏幕坐标转换工具
- **UI 变化检测器 (UIChangeDetector)**: 检测 UI 界面变化
- **断言工具 (UIAssertions)**: UI 状态断言验证

## 安装

```bash
pip install fast2common
```

## 快速开始

```python
from fast2common import ADBController, UIAnalyzer, UIInteraction

# 初始化 ADB 控制器
adb = ADBController(device_id="your_device_id")

# 获取当前 UI 层级
xml_content = adb.dump_ui_hierarchy()

# 分析 UI
analyzer = UIAnalyzer()
elements = analyzer.parse_xml(xml_content)

# 点击元素
interaction = UIInteraction(adb)
interaction.click_element_by_bounds(bounds)
```

## 模块说明

### ADBController

ADB 命令控制器，封装了常用的 ADB 操作：

```python
from fast2common import ADBController

adb = ADBController(device_id="emulator-5554")
screenshot = adb.take_screenshot()
xml_content = adb.dump_ui_hierarchy()
adb.tap(x, y)
```

### ElementLocator

通过文字查找元素坐标：

```python
from fast2common import ElementLocator

locator = ElementLocator(adb)
coordinates = locator.find_element_by_text("设置")
```

### IconLocator

基于视觉识别的图标定位：

```python
from fast2common import IconLocator

icon_locator = IconLocator(adb)
coordinates = icon_locator.find_icon_by_description("搜索图标")
```

### TabManager

AI 驱动的底部导航管理：

```python
from fast2common import TabManager

tab_manager = TabManager(adb)
tab_manager.switch_to_tab("首页")
```

## 依赖

- Python >= 3.8
- zhipuai >= 1.0.0
- Pillow >= 9.0.0

## 开发安装

```bash
git clone https://github.com/fast2/fast2common.git
cd fast2common
pip install -e ".[dev]"
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- 项目主页: https://github.com/fast2/fast2common
- 问题反馈: https://github.com/fast2/fast2common/issues
