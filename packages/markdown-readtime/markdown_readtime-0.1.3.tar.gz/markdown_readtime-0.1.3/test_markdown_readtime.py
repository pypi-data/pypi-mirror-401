"""
markdown_readtime 库的测试文件
"""
import unittest

try:
    from markdown_readtime import estimate, estimate_with_speed, ReadSpeed, minutes, words, formatted
except ImportError:
    print("请先安装 markdown-readtime 库:")
    print("pip install markdown-readtime")
    exit(1)


class TestMarkdownReadtime(unittest.TestCase):
    """
    markdown_readtime 库的测试类
    """

    def test_basic_estimate(self):
        """测试基本的阅读时间估算功能"""
        markdown_content = """
# 标题
## 子标题
### 子子标题
1. 列表1
2. 列表2
"""
        result = estimate(markdown_content.strip())
        
        # 验证返回对象包含必要的属性
        self.assertIsInstance(result.total_seconds, int)
        self.assertIsInstance(result.formatted, str)
        self.assertIsInstance(result.word_count, int)
        self.assertIsInstance(result.image_count, int)
        self.assertIsInstance(result.code_block_count, int)
        
        # 验证基本逻辑
        self.assertGreaterEqual(result.total_seconds, 0)
        self.assertGreaterEqual(result.word_count, 0)
        self.assertGreaterEqual(result.image_count, 0)
        self.assertGreaterEqual(result.code_block_count, 0)

    def test_empty_content(self):
        """测试空内容的处理"""
        result = estimate("")
        
        self.assertEqual(result.total_seconds, 0)
        self.assertEqual(result.word_count, 0)
        self.assertEqual(result.image_count, 0)
        self.assertEqual(result.code_block_count, 0)
        self.assertEqual(result.formatted, "0秒")

    def test_with_images(self):
        """测试包含图片的 Markdown 内容"""
        markdown_with_images = """
# 标题

这是一个包含图片的文档。

![图片1](image1.jpg)

这里是另一张图片：

![图片2](image2.png)
"""
        result = estimate(markdown_with_images)
        
        self.assertGreaterEqual(result.image_count, 2)
        self.assertGreaterEqual(result.total_seconds, 0)

    def test_with_code_blocks(self):
        """测试包含代码块的 Markdown 内容"""
        markdown_with_code = """
# 标题

这是一个包含代码的文档。

```python
def hello():
    print("Hello, world!")
```

另一个代码块：

```javascript
function greet() {
    console.log("Hello!");
}
```
"""
        result = estimate(markdown_with_code)
        
        self.assertGreaterEqual(result.code_block_count, 2)
        self.assertGreaterEqual(result.total_seconds, 0)

    def test_custom_speed(self):
        """测试自定义阅读速度配置"""
        markdown_content = """
# 测试标题

这是一个测试内容。

- 列表项1
- 列表项2

```python
def test_func():
    pass
```

![图片](pic.jpg)
"""
        
        # 使用默认速度
        default_result = estimate(markdown_content)
        
        # 使用自定义速度（较慢的阅读速度）
        slow_speed = ReadSpeed(100.0, 15.0, 25.0, True, True)
        slow_result = estimate_with_speed(markdown_content, slow_speed)
        
        # 使用自定义速度（较快的阅读速度）
        fast_speed = ReadSpeed(400.0, 5.0, 10.0, True, True)
        fast_result = estimate_with_speed(markdown_content, fast_speed)
        
        # 检查所有结果都有效
        self.assertIsInstance(default_result, type(slow_result))
        self.assertIsInstance(fast_result, type(slow_result))

    def test_minutes_function(self):
        """测试 minutes 函数"""
        markdown_content = "# 测试\n\n这是一些内容。" * 10
        mins = minutes(markdown_content)
        
        self.assertIsInstance(mins, int)
        self.assertGreaterEqual(mins, 0)

    def test_words_function(self):
        """测试 words 函数"""
        markdown_content = "# 测试\n\n这是一些内容。" * 5
        word_count = words(markdown_content)
        
        self.assertIsInstance(word_count, int)
        self.assertGreaterEqual(word_count, 0)

    def test_formatted_function(self):
        """测试 formatted 函数"""
        markdown_content = "# 测试\n\n这是一些内容。"
        formatted_time = formatted(markdown_content)
        
        self.assertIsInstance(formatted_time, str)
        self.assertIn("秒", formatted_time)  # 至少应该包含秒单位

    def test_chinese_vs_english_mode(self):
        """测试中英文模式差异"""
        # 简单的英文内容
        english_content = "# Title\n\nThis is some English text content."
        
        # 中文模式（默认）
        chinese_result = estimate(english_content)
        
        # 英文模式
        english_speed = ReadSpeed(200.0, 12.0, 20.0, True, False)
        english_result = estimate_with_speed(english_content, english_speed)
        
        # 两个结果都应该有效
        self.assertIsNotNone(chinese_result)
        self.assertIsNotNone(english_result)
        
        # 验证它们都有正确的属性
        self.assertIsInstance(chinese_result.total_seconds, int)
        self.assertIsInstance(english_result.total_seconds, int)

    def test_emoji_handling(self):
        """测试表情符号处理（如果库支持的话）"""
        markdown_with_emojis = """
# 测试表情符号

这是一个包含表情符号的文档 😊 🚀 📊
"""
        # 测试开启表情符号计数
        speed_with_emoji = ReadSpeed(200.0, 12.0, 20.0, True, True)
        result_with_emoji = estimate_with_speed(markdown_with_emojis, speed_with_emoji)
        
        # 测试关闭表情符号计数
        speed_without_emoji = ReadSpeed(200.0, 12.0, 20.0, False, True)
        result_without_emoji = estimate_with_speed(markdown_with_emojis, speed_without_emoji)
        
        # 两个结果都应该是有效的 ReadTime 对象
        self.assertIsNotNone(result_with_emoji)
        self.assertIsNotNone(result_without_emoji)

    def test_method_chaining(self):
        """测试 ReadSpeed 方法链式调用"""
        speed = ReadSpeed(200.0, 12.0, 20.0, True, True) \
            .wpm(150.0) \
            .image_time(10.0) \
            .code_block_time(30.0) \
            .emoji(False) \
            .chinese(True)
        
        markdown_content = "# 测试\n\n内容"
        result = estimate_with_speed(markdown_content, speed)
        
        # 验证结果有效
        self.assertIsNotNone(result)
        self.assertIsInstance(result.total_seconds, int)


def run_tests():
    """运行所有测试"""
    unittest.main()


if __name__ == '__main__':
    print("开始运行 markdown_readtime 库的测试...")
    run_tests()