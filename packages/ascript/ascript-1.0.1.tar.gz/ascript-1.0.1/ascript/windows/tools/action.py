import os
import sys

import eel
import flet as ft
import win32gui
import asyncio
from ctypes import windll, byref, sizeof
from ctypes.wintypes import RECT, MSG
import win32con
import win32clipboard

# 强制 DPI 感知
try:
    windll.shcore.SetProcessDpiAwareness(1)
except:
    windll.user32.SetProcessDPIAware()


def catch_xy_flet_mini():
    async def main(page: ft.Page):
        page.title = "坐标捕获器-AScript"

        # --- 窗口尺寸设置 ---
        w, h = 320, 500
        if hasattr(page, "window"):
            page.window.width = w
            page.window.height = h
            page.window.min_width = w - 20
            page.window.min_height = h - 20
            page.window.resizable = True
            page.window.always_on_top = True
        else:
            page.window_width = w
            page.window_height = h
            page.window_min_width = w - 20
            page.window_min_height = h - 20
            page.window_resizable = True
            page.window_always_on_top = True

        page.padding = 10
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = ft.Colors.BLACK

        # --- UI 组件 ---
        win_info = ft.Text("窗口: -", size=14, weight="bold", color=ft.Colors.CYAN_300,
                           max_lines=1, overflow=ft.TextOverflow.ELLIPSIS)

        abs_text = ft.Text("0, 0", size=16, weight="bold")
        rel_text = ft.Text("0, 0", size=16, weight="bold", color=ft.Colors.GREEN_400)

        # --- UI 布局：屏幕和窗口坐标在同一个框内 ---
        window_section_box = ft.Container(
            content=ft.Column([
                # 屏幕行
                ft.Row([
                    ft.Radio(value="abs", label="屏幕"),
                    abs_text
                ], alignment=ft.MainAxisAlignment.START, spacing=10),

                # 屏幕与窗口之间的分割线
                ft.Divider(height=1, color=ft.Colors.GREY_800),

                # 窗口行
                ft.Row([
                    ft.Radio(value="rel", label="窗口"),
                    rel_text
                ], alignment=ft.MainAxisAlignment.START, spacing=10),

                # --- 调整部分：给图标左侧增加间距 ---
                ft.Row([
                    ft.Container(width=1), # 这里控制图标距离左边的距离
                    # ft.Icon(ft.icons.Icons.CHEVRON_RIGHT_ROUNDED, size=20, color=ft.Colors.CYAN_300),
                    win_info
                ], spacing=5)
            ], spacing=8),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_800),
            border_radius=8,
            bgcolor=ft.Colors.GREY_900
        )

        # 单选框组
        radio_group = ft.RadioGroup(
            content=ft.Column([
                window_section_box
            ], spacing=10),
            value="abs"
        )

        # --- 历史记录功能区 ---
        history_list = ft.ListView(expand=True, spacing=5, padding=5)

        def clear_history(e):
            history_list.controls.clear()
            history_list.update()

        history_header = ft.Row(
            controls=[
                ft.Text("历史记录:", size=11, color=ft.Colors.GREY_500),
                ft.IconButton(
                    icon=ft.icons.Icons.DELETE_SWEEP,
                    icon_size=18,
                    icon_color=ft.Colors.RED_400,
                    tooltip="清空全部",
                    on_click=clear_history,
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        def copy_to_clipboard(text):
            try:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(text)
                win32clipboard.CloseClipboard()
            except:
                pass

        def add_history_item(val):
            item = ft.Container(
                content=ft.Text(f"复制: {val}", size=12),
                padding=8,
                bgcolor=ft.Colors.GREY_900,
                border_radius=5,
                on_click=lambda _, v=val: copy_to_clipboard(v),
                ink=True
            )
            history_list.controls.insert(0, item)
            if len(history_list.controls) > 50:
                history_list.controls.pop()
            history_list.update()

        content_view = ft.Column([
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            radio_group,
            ft.Divider(height=1, color=ft.Colors.GREY_800),
            history_header,
            history_list,
            ft.Text("Alt+A 记录", size=10, italic=True, color=ft.Colors.GREY_600)
        ], expand=True)

        page.add(content_view)

        # --- 窗口拖拽 ---
        def on_pan_update(e: ft.DragUpdateEvent):
            if hasattr(page, "window"):
                page.window.left += e.delta_x
                page.window.top += e.delta_y
            else:
                page.window_left += e.delta_x
                page.window_top += e.delta_y
            page.update()

        content_view.on_pan_start = lambda _: None
        content_view.on_pan_update = on_pan_update

        # --- 热键注册 (Alt+A) ---
        hotkey_id = 1
        try:
            windll.user32.RegisterHotKey(None, hotkey_id, win32con.MOD_ALT, ord('A'))
        except:
            pass

        def get_root_hwnd(hwnd):
            while True:
                parent = win32gui.GetParent(hwnd)
                if not parent or not win32gui.IsWindow(parent): break
                hwnd = parent
            return hwnd

        while True:
            try:
                x, y = win32gui.GetCursorPos()
                raw_hwnd = win32gui.WindowFromPoint((x, y))
                root_hwnd = get_root_hwnd(raw_hwnd)

                title, rx, ry = "-", 0, 0
                if root_hwnd and win32gui.IsWindow(root_hwnd):
                    title = win32gui.GetWindowText(root_hwnd) or "Unknown"
                    rect = RECT()
                    windll.dwmapi.DwmGetWindowAttribute(root_hwnd, 9, byref(rect), sizeof(rect))
                    rx, ry = x - rect.left, y - rect.top

                abs_text.value = f"{x}, {y}"
                rel_text.value = f"{rx}, {ry}"
                win_info.value = f"{title}"

                abs_text.update()
                rel_text.update()
                win_info.update()

                # 热键监听
                msg = MSG()
                if windll.user32.PeekMessageW(byref(msg), None, win32con.WM_HOTKEY, win32con.WM_HOTKEY,
                                              win32con.PM_REMOVE):
                    if msg.wParam == hotkey_id:
                        res = f"{x}, {y}" if radio_group.value == "abs" else f"{rx}, {ry}"
                        copy_to_clipboard(res)
                        add_history_item(res)
            except:
                pass
            await asyncio.sleep(0.05)

    ft.app(target=main)


if __name__ == "__main__":
    catch_xy_flet_mini()