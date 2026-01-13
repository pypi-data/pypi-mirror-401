# SPDX-FileCopyrightText: 2025 QinHan
# SPDX-License-Identifier: MPL-2.0
"""
Simple Tokenizer - 替代 tiktoken 的轻量级 token 估算器

Token 估算规则:
1. 英文单词: 约 4 字符 = 1 token
2. 中文字符: 约 1-2 字符 = 1 token
3. 标点符号和空格也算 token

使用正则表达式匹配各种语言和符号单元进行估算。
"""

import re
from typing import List


class SimpleTokenizer:
    """
    轻量级 Token 估算器
    使用正则表达式匹配不同类型的文本单元来估算 token 数量
    """

    # 匹配模式（按优先级从高到低）
    # 1. 连续的中文字符
    # 2. 连续的英文/数字/常见符号
    # 3. 标点符号
    # 4. 空白字符
    PATTERNS: List[tuple[str, float]] = [
        # 中文汉字 (每个汉字约 1.5 token)
        (r'[\u4e00-\u9fa5]+', 1.5),
        # 日文/韩文 (每个字符约 1.5 token)
        (r'[\uac00-\ud7ff\u3040-\u309f\u30a0-\u30ff]+', 1.5),
        # 连续的英文单词 (每 4 字符约 1 token)
        (r'[a-zA-Z]+', 0.25),
        # 连续的数字 (每 4 字符约 1 token)
        (r'[0-9]+', 0.25),
        # URL
        (r'https?://[^\s]+', 0.25),
        # 邮箱
        (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', 0.25),
        # 单个 ASCII 可打印字符 (每个约 1 token)
        (r'[\x20-\x7e]', 1.0),
    ]

    def __init__(self):
        # 预编译正则表达式
        self._pattern = re.compile('|'.join(f'(?P<{name}>{pattern})' for pattern, _ in self.PATTERNS))

    def encode(self, text: str) -> List[str]:
        """
        将文本编码为 token 列表

        Args:
            text: 输入文本

        Returns:
            token 列表
        """
        if not text:
            return []

        tokens = []
        last_end = 0

        for match in self._pattern.finditer(text):
            # 记录被跳过的字符
            if match.start() > last_end:
                skipped = text[last_end:match.start()]
                # 将跳过的字符按单个字符处理
                for char in skipped:
                    if char.strip():
                        tokens.append(char)

            # 记录匹配的 token
            for name, pattern in self.PATTERNS:
                if match.group(name):
                    tokens.append(match.group(name))
                    break

            last_end = match.end()

        # 处理末尾剩余的字符
        if last_end < len(text):
            remaining = text[last_end:]
            for char in remaining:
                if char.strip():
                    tokens.append(char)

        return tokens

    def estimate_tokens(self, text: str) -> int:
        """
        估算文本的 token 数量

        Args:
            text: 输入文本

        Returns:
            估算的 token 数量
        """
        if not text:
            return 0

        tokens = self.encode(text)
        return len(tokens)

    def estimate_tokens_fast(self, text: str) -> int:
        """
        快速估算 token 数量（使用字符数除以系数）

        Args:
            text: 输入文本

        Returns:
            估算的 token 数量
        """
        if not text:
            return 0

        # 简单估算：中文约 2 char/token，英文约 4 char/token
        # 混合文本取平均值
        chinese_count = len(re.findall(r'[\u4e00-\u9fa5]', text))
        total_count = len(text)

        if chinese_count > total_count * 0.5:
            # 以中文为主
            return len(text) // 2
        else:
            # 以英文为主
            return len(text) // 4


# 全局默认 tokenizer 实例
_default_tokenizer: SimpleTokenizer | None = None


def get_tokenizer() -> SimpleTokenizer:
    """获取全局默认的 SimpleTokenizer 实例"""
    global _default_tokenizer
    if _default_tokenizer is None:
        _default_tokenizer = SimpleTokenizer()
    return _default_tokenizer


def estimate_tokens(text: str) -> int:
    """
    便捷函数：快速估算文本的 token 数量

    Args:
        text: 输入文本

    Returns:
        估算的 token 数量
    """
    return get_tokenizer().estimate_tokens(text)


def estimate_tokens_fast(text: str) -> int:
    """
    便捷函数：快速估算 token 数量（使用字符数除以系数）

    Args:
        text: 输入文本

    Returns:
        估算的 token 数量
    """
    return get_tokenizer().estimate_tokens_fast(text)
