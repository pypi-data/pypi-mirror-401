"""
markdown_readtime 库的使用示例
"""

# 首先需要安装并导入库
# pip install markdown-readtime
try:
    from markdown_readtime import estimate, estimate_with_speed, ReadSpeed, minutes, words, formatted
except ImportError:
    print("请先安装 markdown-readtime 库:")
    print("pip install markdown-readtime")


def basic_usage_example():
    """
    基本用法示例
    """
    print("=== 基本用法示例 ===")
    
    markdown_content = """
# 我的第一篇博客文章

这是一些示例内容，用来演示如何使用 markdown-readtime 库。

## 子标题

我们还可以添加一些列表:
- 第一项
- 第二项
- 第三项

```python
def hello_world():
    print("Hello, world!")
```

还有 ![一张图片](image.jpg) 在这里。
"""

    # 获取完整的阅读时间信息
    read_time = estimate(markdown_content)
    print(f"总阅读时间: {read_time.total_seconds}秒")
    print(f"格式化时间: {read_time.formatted}")
    print(f"字数统计: {read_time.word_count}")
    print(f"图片数量: {read_time.image_count}")
    print(f"代码块数量: {read_time.code_block_count}")

    # 或者使用快捷函数
    print(f"预计需要 {minutes(markdown_content)} 分钟读完")
    print(f"大约有 {words(markdown_content)} 个字")
    print(f"阅读时间: {formatted(markdown_content)}")
    print()


def custom_speed_example():
    """
    自定义阅读速度示例
    """
    print("=== 自定义阅读速度示例 ===")
    
    markdown_content = """# 示例文章

这是用来测试的文章内容。

- 列表项1
- 列表项2

```rust
fn main() {
    println!("Hello, world!");
}
```

![图片](pic.png)"""

    # 创建自定义阅读速度配置
    # wpm: 每分钟阅读单词数
    # seconds_per_image: 每张图片额外时间（秒）
    # seconds_per_code_block: 每个代码块额外时间（秒）
    # count_emoji: 是否考虑emoji
    # chinese: 是否中文模式
    speed = ReadSpeed(180.0, 15.0, 25.0, True, True)
    
    # 使用自定义配置计算阅读时间
    read_time = estimate_with_speed(markdown_content, speed)
    print(f"自定义配置下的阅读时间: {read_time.total_seconds}秒")
    print(f"格式化显示: {read_time.formatted}")
    print(f"字数: {read_time.word_count}")
    print(f"图片数: {read_time.image_count}")
    print(f"代码块数: {read_time.code_block_count}")
    print()


def english_text_example():
    """
    英文文本处理示例
    """
    print("=== 英文文本处理示例 ===")
    
    english_markdown = """
# Sample Article

This is a sample article to demonstrate reading time estimation.

## Section 1

Here's some content in English:
- First point
- Second point

```javascript
function greet(name) {
    console.log(`Hello, ${name}!`);
}
```

![An image](image.png)
"""

    # 默认配置（中文模式）
    print("使用中文模式处理英文文本:")
    read_time_chinese = estimate(english_markdown)
    print(f"  阅读时间: {read_time_chinese.formatted}, 字数: {read_time_chinese.word_count}")

    # 使用英文模式
    print("使用英文模式处理英文文本:")
    speed_english = ReadSpeed(200.0, 12.0, 20.0, True, False)  # 最后一个参数设为 False 表示英文模式
    read_time_english = estimate_with_speed(english_markdown, speed_english)
    print(f"  阅读时间: {read_time_english.formatted}, 字数: {read_time_english.word_count}")
    print()


def builder_pattern_example():
    """
    构建器模式示例
    """
    print("=== 构建器模式示例 ===")
    
    # 使用构建器模式创建 ReadSpeed 对象（虽然 Python 中没有直接的构建器模式，
    # 但可以通过连续调用方法来实现类似效果）
    speed = ReadSpeed(200.0, 12.0, 20.0, True, True) \
        .wpm(150.0) \
        .image_time(10.0) \
        .code_block_time(30.0) \
        .emoji(False) \
        .chinese(True)
    
    markdown_content = """
# 测试标题

这是一个测试内容。

![图片1](img1.jpg)

```python
def test_func():
    pass
```

![图片2](img2.jpg)
"""
    
    read_time = estimate_with_speed(markdown_content, speed)
    print(f"使用自定义配置的阅读时间: {read_time.formatted}")
    print(f"字数: {read_time.word_count}")
    print(f"图片数: {read_time.image_count}")
    print(f"代码块数: {read_time.code_block_count}")
    print()


def comparison_example():
    """
    不同配置比较示例
    """
    print("=== 不同配置比较示例 ===")
    
    markdown_content = """
# 比较测试

这是一个用于比较不同配置的测试文档。

- 列表项1
- 列表项2
- 列表项3

```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::new();
    map.insert("key", "value");
    println!("{:?}", map);
}
```

![图片](image.jpg)

更多内容...
"""

    # 快速阅读者配置
    fast_reader = ReadSpeed(300.0, 8.0, 15.0, True, True)
    fast_time = estimate_with_speed(markdown_content, fast_reader)
    
    # 慢速阅读者配置
    slow_reader = ReadSpeed(100.0, 20.0, 30.0, True, True)
    slow_time = estimate_with_speed(markdown_content, slow_reader)
    
    # 默认配置
    default_time = estimate(markdown_content)
    
    print(f"快速阅读者: {fast_time.formatted} ({fast_time.total_seconds}秒)")
    print(f"慢速阅读者: {slow_time.formatted} ({slow_time.total_seconds}秒)")
    print(f"默认配置: {default_time.formatted} ({default_time.total_seconds}秒)")
    print()


if __name__ == "__main__":
    print("markdown_readtime 库使用示例\n")
    
    basic_usage_example()
    custom_speed_example()
    english_text_example()
    builder_pattern_example()
    comparison_example()
    
    print("=== 完整示例结束 ===")
    print("这些示例展示了 markdown_readtime 库的主要功能:")
    print("- 基本阅读时间估算")
    print("- 自定义阅读速度配置")
    print("- 中英文文本处理")
    print("- 构建器模式配置")
    print("- 不同阅读习惯对比")