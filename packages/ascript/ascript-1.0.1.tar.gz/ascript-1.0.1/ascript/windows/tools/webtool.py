import base64
import io

import eel
import os
import sys

from ..window import Selector
from..window import Window
import uiautomation as auto

# 1. 暴露函数建议放在函数外（或者确保在函数内时，函数被调用）
@eel.expose
def get_ui_tree():
    # 这里最终会放你的 Selector 逻辑
    print("JS 调用了 Python: get_ui_tree")
    return {"status": "ok", "data": "Tree Data Here"}


@eel.expose
def get_online_windows():
    """获取所有可见窗口并返回给前端"""
    try:
        # 调用你的类方法
        windows = Window.find_all(visible_only=True)

        # 转换为前端易读的格式：名称 [句柄]
        # 同时保留 hwnd 以便后续探测指定窗口
        output = []
        for win in windows:
            if win.title:  # 过滤掉无标题的背景窗口
                output.append({
                    "display": f"{win.title} [{win.hwnd}]",
                    "hwnd": win.hwnd,
                    "title": win.title
                })
        return {"status": "success", "data": output}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@eel.expose
def get_ui_tree_data(hwnd, max_depth=0):
    """
    JS 调用：传入句柄和深度，返回全量 UI 树字典
    :param hwnd: 窗口句柄 (int)
    :param max_depth: 探测深度 (int), 0 为不限
    """
    try:
        # 1. 确保 hwnd 是整数类型
        hwnd = int(hwnd)
        max_depth = int(max_depth)

        if max_depth==0:
            max_depth = 0xFFFFFFFF

        # 2. 构造 Window 对象
        target_win = Window(hwnd)
        if not target_win.title:
            return {"status": "error", "message": "无效的窗口句柄或窗口已关闭"}

        target_win.activate()

        # 3. 初始化 Selector (假设你的 Selector 接收 window 和 max_depth)
        # 这里演示你的 get_uielement_tree 逻辑
        # 注意：如果你的 Selector 类还没写好，这里直接调用你提供的函数逻辑
        selector = Selector(target_win, depth=max_depth)

        print(f"开始探测窗口 [{target_win.title}]，深度: {max_depth}...")

        # 4. 获取树状结构（调用你写的那个逻辑）
        root_element = selector.get_uielement_tree()

        if not root_element:
            return {"status": "empty", "message": "未能获取到任何 UI 元素"}

        # 5. 转换为字典（递归调用 UIElement.to_dict）
        tree_dict = root_element.to_dict()

        return {
            "status": "success",
            "data": tree_dict
        }

    except Exception as e:
        import traceback
        print(f"探测失败: {e}")
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


@eel.expose
def test_selector(selector_str: str):
    print(f"\n[Python Receive] 收到指令: {selector_str}")
    try:
        # 1. 准备环境
        safe_vars = {'Selector': Selector, 'auto': auto}

        # 2. 执行 eval
        print("[Python Debug] 开始执行 eval...")
        results = eval(selector_str, {"__builtins__": None}, safe_vars)

        # 3. 核心修复逻辑：自动补全与类型统一
        # 情况 A: 如果返回的是 Selector 实例（用户忘了写 .find()）
        if hasattr(results, 'find'):
            print("[Python Debug] 检测到未执行 find，自动调用 .find()")
            results = results.find()

        # 情况 B: 统一转换为列表 (处理 find_first 返回单个对象的情况)
        if results is None:
            final_list = []
        elif isinstance(results, list):
            final_list = results
        else:
            # 说明是单个 UIElement 对象
            final_list = [results]

        print(f"[Python Debug] 最终待处理结果数量: {len(final_list)}")

        # 4. 序列化
        tree_dict = [el.to_dict() for el in final_list]

        return {
            "status": "success",
            "data": tree_dict
        }

    except Exception as e:
        import traceback
        error_stack = traceback.format_exc()
        print(f"[Python Error] 详细报错如下:\n{error_stack}")
        return {
            "status": "error",
            "message": str(e),
            "data": []
        }

@eel.expose
def get_screenshot(hwnd):
    try:
        hwnd = int(hwnd)
        # 3. 截图 (注意：ImageGrab 在高 DPI 屏幕下可能需要处理缩放)
        img = Window(hwnd).capture()

        # 4. 将图片转为内存二进制流并压缩 (JPEG 格式能显著减小传输体积)
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=70)  # 质量 70 足够探测使用了

        # 5. 编码为 Base64
        img_str = base64.b64encode(buffer.getvalue()).decode()

        # 返回 Data URL 格式，前端 <img> 标签可以直接识别
        return {
            "status": "success",
            "data": f"data:image/jpeg;base64,{img_str}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def start_vtree(hwnd:str = None,window_title:str = None):
    # 2. 路径处理
    if getattr(sys, 'frozen', False):
        web_folder = os.path.join(sys._MEIPASS, 'web')
    else:
        # 建议使用绝对路径防止执行路径不一致的问题
        web_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web')

    if not os.path.exists(web_folder):
        print(f"错误：找不到 web 文件夹: {web_folder}")
        return

    if window_title:
        temp_window = Window.find(window_title)
        hwnd = temp_window.hwnd

    # print(temp_window.hwnd)

    # 初始化 Eel
    eel.init(web_folder)

    # 3. 启动应用
    # cmdline_args 可以添加一些浏览器优化参数
    eel_kwargs = {
        'mode': 'chrome',                   # 优先使用 chrome
        'port': 0,                          # 0 表示随机选择可用端口，避免端口冲突
        'cmdline_args': ['--start-maximized', '--incognito'] # 最大化，无痕模式
    }

    print("正在启动 UI 探测器...")
    try:
        # 这一行搞定：如果有 hwnd 则拼接参数，否则为空字符串
        url = f"vtree.html?hwnd={hwnd}" if hwnd else "vtree.html"

        eel.start(url, **eel_kwargs)
    except (SystemExit, MemoryError, KeyboardInterrupt):
        # 正常退出
        pass

if __name__ == '__main__':
    start_vtree()