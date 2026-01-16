"""
markdown_readtime 模块提供了估算 Markdown 内容阅读时间的功能。

功能特性:
- 📊 准确估算 Markdown 文本的阅读时间
- 🌍 支持中英文文本
- 😊 Emoji 处理支持
- 🖼️ 图片阅读时间计算
- 💻 代码块阅读时间计算
- ⚙️ 可自定义阅读速度参数
"""

class ReadTime:
    """
    阅读时间估算结果
    
    Attributes:
        total_seconds (int): 总阅读时间（秒），向上取整后的总秒数，包括文本阅读时间、图片额外时间和代码块额外时间
        formatted (str): 格式化后的阅读时间字符串，将秒数转换为人类友好的格式，例如 "30秒"、"5分钟" 或 "2分30秒"
        word_count (int): 单词数量，根据是否为中文文本，分别采用不同的计数方式：
                          - 中文：计算非空白字符数
                          - 英文：计算空格分隔的单词数
        image_count (int): 图片数量，Markdown 中 `![alt text](image_url)` 格式的图片数量
        code_block_count (int): 代码块数量，Markdown 中 ```code``` 格式的代码块数量
    """
    
    total_seconds: int
    formatted: str
    word_count: int
    image_count: int
    code_block_count: int


class ReadSpeed:
    """
    阅读速度配置
    
    允许自定义各种影响阅读时间的因素。
    """
    
    def __init__(self, wpm: float, seconds_per_image: float, seconds_per_code_block: float, count_emoji: bool = True, chinese: bool = True):
        """
        初始化阅读速度配置
        
        Args:
            wpm: 每分钟阅读单词数（默认：200），这是阅读速度的核心参数，用于计算文本的基础阅读时间
            seconds_per_image: 每张图片额外时间（秒，默认：12），每发现一张图片就会增加相应的时间，因为读者通常需要额外时间查看图片
            seconds_per_code_block: 每个代码块额外时间（秒，默认：20），每发现一个代码块就会增加相应的时间，因为代码通常需要更仔细的阅读
            count_emoji: 是否考虑emoji（默认：True），当启用时，emoji 会被单独计数，影响总的阅读时间估算
            chinese: 是否中文（默认：True），决定使用哪种文本计数方式：
                     - True: 使用中文计数方式（计算字符数）
                     - False: 使用英文计数方式（计算单词数）
        """
        ...

    # 每分钟阅读单词数（默认：200）
    #
    # 这是阅读速度的核心参数，用于计算文本的基础阅读时间。
    words_per_minute: float
    
    # 每张图片额外时间（秒，默认：12）
    #
    # 每发现一张图片就会增加相应的时间，因为读者通常需要额外时间查看图片。
    seconds_per_image: float
    
    # 每个代码块额外时间（秒，默认：20）
    #
    # 每发现一个代码块就会增加相应的时间，因为代码通常需要更仔细的阅读。
    seconds_per_code_block: float
    
    # 是否考虑emoji（默认：True）
    #
    # 当启用时，emoji 会被单独计数，影响总的阅读时间估算。
    count_emoji: bool
    
    # 是否中文（默认：True）
    #
    # 决定使用哪种文本计数方式：
    # - True: 使用中文计数方式（计算字符数）
    # - False: 使用英文计数方式（计算单词数）
    chinese: bool

    def wpm(self, wpm: float) -> 'ReadSpeed':
        """
        设置每分钟阅读单词数
        
        Args:
            wpm: 每分钟阅读单词数
            
        Returns:
            ReadSpeed: 返回自身，支持链式调用
        """
        ...

    def image_time(self, seconds: float) -> 'ReadSpeed':
        """
        设置每张图片的额外时间
        
        Args:
            seconds: 每张图片的额外时间（秒）
            
        Returns:
            ReadSpeed: 返回自身，支持链式调用
        """
        ...

    def code_block_time(self, seconds: float) -> 'ReadSpeed':
        """
        设置每个代码块的额外时间
        
        Args:
            seconds: 每个代码块的额外时间（秒）
            
        Returns:
            ReadSpeed: 返回自身，支持链式调用
        """
        ...

    def emoji(self, count: bool) -> 'ReadSpeed':
        """
        设置是否考虑emoji
        
        Args:
            count: 是否考虑emoji
            
        Returns:
            ReadSpeed: 返回自身，支持链式调用
        """
        ...

    def chinese(self, is_chinese: bool) -> 'ReadSpeed':
        """
        设置是否中文模式
        
        Args:
            is_chinese: 是否中文模式
            
        Returns:
            ReadSpeed: 返回自身，支持链式调用
        """
        ...


def estimate(markdown_txt: str) -> ReadTime:
    """
    使用默认的阅读速度配置来估算给定 Markdown 文本的阅读时间
    
    Args:
        markdown_txt: 需要估算阅读时间的 Markdown 文本
        
    Returns:
        ReadTime: 包含阅读时间信息的对象
    """


def estimate_with_speed(markdown: str, speed: ReadSpeed) -> ReadTime:
    """
    使用指定的阅读速度配置来估算给定 Markdown 文本的阅读时间
    
    Args:
        markdown: 需要估算阅读时间的 Markdown 文本
        speed: 自定义的阅读速度配置
        
    Returns:
        ReadTime: 包含阅读时间信息的对象
    """


def minutes(markdown: str) -> int:
    """
    估算阅读时间并向上去整到最近的分钟数
    
    Args:
        markdown: 需要估算阅读时间的 Markdown 文本
        
    Returns:
        int: 向上取整后的分钟数
    """


def words(markdown: str) -> int:
    """
    计算 Markdown 文本中的单词数量
    
    Args:
        markdown: 需要计算单词数的 Markdown 文本
        
    Returns:
        int: 单词数量
    """


def formatted(markdown: str) -> str:
    """
    获取格式化后的阅读时间字符串
    
    Args:
        markdown: 需要估算阅读时间的 Markdown 文本
        
    Returns:
        str: 格式化后的阅读时间字符串，例如 "30秒"、"5分钟" 或 "2分30秒"
    """