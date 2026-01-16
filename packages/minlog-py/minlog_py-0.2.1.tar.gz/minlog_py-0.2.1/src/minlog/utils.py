import json
import textwrap
from logging import Logger
from typing import Dict, List, Union


# 新增一个辅助函数用于处理长字符串的换行
def _wrap_long_string(s: str, width: int) -> List[str]:
    """如果字符串很长，使用 textwrap.wrap 进行分行"""
    if width <= 0:
        return [s]
    return textwrap.wrap(s, width=width)


def log_box(logger: Logger, title: str, data: Union[Dict, List[Dict], str], max_width: int = 120):
    """
    title: 标题
    data: 字典、字典列表或字符串。对长内容进行自动换行。
    max_width: 方框的最大宽度（默认 120）。
    """
    rows = []

    # 临时设定内容最大宽度，用于换行处理 (减去边框和左右空格)
    # 最终的 inner width 会基于实际内容动态调整，但换行时需要一个最大约束
    TEMP_MAX_CONTENT_WIDTH = max_width - 4

    # --- 1. 数据内容处理 ---
    if isinstance(data, dict):
        if not data:
            rows = ["(Empty Dict)"]
        else:
            for k, v in data.items():
                k_str = str(k)
                v_str = str(v)

                # 计算值的可用宽度
                available_width = TEMP_MAX_CONTENT_WIDTH - len(k_str) - 2  # 减去 "key: " 的长度

                # 对字典的值进行换行处理
                wrapped_lines = _wrap_long_string(v_str, available_width)

                # 第一行：包含 key
                rows.append(f"{k_str}: {wrapped_lines[0]}")
                # 剩余行：只包含 value，并用空格填充 key 的宽度
                key_padding = " " * (len(k_str) + 2)
                for line in wrapped_lines[1:]:
                    rows.append(f"{key_padding}{line}")

    elif isinstance(data, list):
        if not data:
            rows = ["(Empty List)"]
        else:
            for i, item in enumerate(data):
                if i > 0:
                    rows.append("---SEPARATOR---")
                if isinstance(item, dict):
                    # 处理字典项，支持嵌套字典的换行
                    # 使用与顶层字典相同的逻辑
                    sub_rows = []
                    for k, v in item.items():
                        k_str = str(k)
                        v_str = str(v)
                        available_width = TEMP_MAX_CONTENT_WIDTH - len(k_str) - 2
                        wrapped_lines = _wrap_long_string(v_str, available_width)
                        sub_rows.append(f"{k_str}: {wrapped_lines[0]}")
                        key_padding = " " * (len(k_str) + 2)
                        for line in wrapped_lines[1:]:
                            sub_rows.append(f"{key_padding}{line}")
                    rows.extend(sub_rows)
                else:
                    # 对列表中的字符串元素进行换行处理
                    wrapped_lines = _wrap_long_string(str(item), TEMP_MAX_CONTENT_WIDTH)
                    rows.extend(wrapped_lines)

    elif isinstance(data, str):
        # 尝试解析JSON字符串
        try:
            parsed_data = json.loads(data)
            if isinstance(parsed_data, dict):
                # 如果是JSON对象，递归调用处理字典
                temp_rows = []
                for k, v in parsed_data.items():
                    k_str = str(k)
                    v_str = str(v)
                    available_width = TEMP_MAX_CONTENT_WIDTH - len(k_str) - 2
                    wrapped_lines = _wrap_long_string(v_str, available_width)
                    temp_rows.append(f"{k_str}: {wrapped_lines[0]}")
                    key_padding = " " * (len(k_str) + 2)
                    for line in wrapped_lines[1:]:
                        temp_rows.append(f"{key_padding}{line}")
                rows.extend(temp_rows)
            else:
                # 其他JSON类型，直接转换为字符串
                rows.extend(_wrap_long_string(str(parsed_data), TEMP_MAX_CONTENT_WIDTH))
        except json.JSONDecodeError:
            # 不是JSON，按普通字符串处理
            rows.extend(_wrap_long_string(data, TEMP_MAX_CONTENT_WIDTH))

    else:
        rows = [str(data)]

    # --- 2. 计算宽度逻辑 ---

    # A. 计算内容的最大宽度
    content_rows = [r for r in rows if r != "---SEPARATOR---"]
    max_content_len = max(len(r) for r in content_rows) if content_rows else 0

    # B. 确定标题折行的宽度
    # 逻辑：标题的折行宽度不能小于内容的宽度，但也不能超过用户设定的 max_width。
    wrap_width = max(max_content_len, min(len(title), max_width))

    # C. 对标题进行折行处理
    title_lines = textwrap.wrap(title, width=wrap_width)

    # D. 最终确定方框宽度 (取 标题折行后的最长行 和 内容最长行 的最大值)
    final_inner_width = max(max_content_len, max(len(line) for line in title_lines))
    width = final_inner_width + 2  # 左右各留 1 空格

    # --- 3. 绘制输出 ---

    logger.info(f"┌{'─' * width}┐")

    # 逐行打印标题
    for t_line in title_lines:
        logger.info(f"│ {t_line.ljust(width - 1)}│")

    logger.info(f"├{'─' * width}┤")

    for row in rows:
        if row == "---SEPARATOR---":
            logger.info(f"├{'─' * width}┤")
        else:
            logger.info(f"│ {row.ljust(width - 1)}│")

    logger.info(f"└{'─' * width}┘")
