"""文本处理器 - 处理换行符和emoji编解码

保持与原有业务逻辑完全一致：
- 千寻框架 sendText API 的换行符处理：
  - \n 会显示为两行（有空行/段落间距）
  - \r 会显示为单行换行（无空行）
- Emoji 使用 \\uXXXX 格式编码（含 surrogate pair）
"""
import re
import logging

logger = logging.getLogger(__name__)


class TextProcessor:
    """文本处理器 - 保持原有逻辑"""
    
    @staticmethod
    def encode_for_qianxun(text: str) -> str:
        """编码文本用于发送到千寻框架
        
        换行符处理（保持原逻辑）：
        - \n 会显示为两行（有空行）
        - \r 会显示为单行换行（无空行）
        
        处理步骤：
        1. 先统一所有换行符为 \n
        2. 临时标记双换行（空行）
        3. 单换行 → \r
        4. 双换行（空行）→ \n
        5. emoji编码
        
        Args:
            text: 原始文本
            
        Returns:
            编码后的文本，可直接发送到千寻框架
        """
        # 先统一为 \n
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        # 临时标记双换行（空行）
        text = text.replace('\n\n', '\x00')
        # 单换行 → \r
        text = text.replace('\n', '\r')
        # 双换行（空行）→ \n（千寻会显示为两行）
        text = text.replace('\x00', '\n')
        # emoji编码
        text = TextProcessor.encode_emoji(text)
        return text
    
    @staticmethod
    def encode_emoji(text: str) -> str:
        """把emoji等非BMP字符转换为\\uXXXX格式
        
        千寻框架需要 \\uXXXX 格式的 emoji 转义
        非 BMP 字符（emoji 等）需要转换为 surrogate pair
        
        Args:
            text: 原始文本
            
        Returns:
            编码后的文本
        """
        result = []
        for char in text:
            code = ord(char)
            # 非 BMP 字符（emoji 等）需要转换为 surrogate pair
            if code > 0xFFFF:
                code -= 0x10000
                high = 0xD800 + (code >> 10)
                low = 0xDC00 + (code & 0x3FF)
                result.append(f'\\u{high:04X}\\u{low:04X}')
            else:
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def decode_emoji(text: str) -> str:
        """解码\\uXXXX格式为真正的字符
        
        处理两种情况：
        1. surrogate pair 格式的 emoji: \\uD83D\\uDE00 -> 😀
        2. 普通 Unicode 转义: \\u4F60 -> 你
        
        Args:
            text: 包含\\uXXXX格式的文本
            
        Returns:
            解码后的文本
        """
        if not text or '\\u' not in text:
            return text
        
        try:
            # 先处理 surrogate pair 格式的 emoji
            def replace_surrogate(match):
                try:
                    high = int(match.group(1), 16)
                    low = int(match.group(2), 16)
                    # 验证是否是有效的 surrogate pair
                    if 0xD800 <= high <= 0xDBFF and 0xDC00 <= low <= 0xDFFF:
                        # 转换为真正的 Unicode 字符
                        code_point = 0x10000 + ((high - 0xD800) << 10) + (low - 0xDC00)
                        return chr(code_point)
                    return match.group(0)
                except:
                    return match.group(0)
            
            # 匹配 \uXXXX\uXXXX 格式的 surrogate pair
            surrogate_pattern = r'\\u([dD][89aAbB][0-9a-fA-F]{2})\\u([dD][cCdDeEfF][0-9a-fA-F]{2})'
            result = re.sub(surrogate_pattern, replace_surrogate, text)
            
            # 再处理剩余的普通 \uXXXX 格式（非 surrogate）
            def replace_unicode(match):
                try:
                    code = int(match.group(1), 16)
                    # 跳过 surrogate 范围（已经处理过了）
                    if 0xD800 <= code <= 0xDFFF:
                        return match.group(0)
                    return chr(code)
                except:
                    return match.group(0)
            
            unicode_pattern = r'\\u([0-9a-fA-F]{4})'
            result = re.sub(unicode_pattern, replace_unicode, result)
            
            return result
        except Exception as e:
            logger.debug(f"解码 Unicode 转义失败: {e}")
            return text
    
    @staticmethod
    def config_to_text(text: str) -> str:
        """配置文件中的\\n字符串转换为真正的换行符
        
        配置文件中存储的是字面量 \\n（两个字符），
        需要转换为真正的换行符 \n（一个字符）
        
        Args:
            text: 配置文件中的文本
            
        Returns:
            转换后的文本
        """
        return text.replace('\\n', '\n')
    
    @staticmethod
    def text_to_config(text: str) -> str:
        """文本中的换行符转换为配置文件格式
        
        将真正的换行符转换为字面量 \\n，用于保存到配置文件
        保留空行，只去除每行末尾空格
        
        Args:
            text: 原始文本
            
        Returns:
            配置文件格式的文本
        """
        # 统一换行符
        text = text.replace('\r\n', '\n').replace('\r', '')
        if '\n' in text:
            # 保留空行，只去除每行末尾空格
            lines = [line.rstrip() for line in text.split('\n')]
            return '\\n'.join(lines)
        return text
