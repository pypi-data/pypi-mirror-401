# 这个文件存在是为了让 Maturin 能够找到正确的源码位置
# 实际的扩展模块将由 Rust 编译生成，Python 会自动导入

try:
    # 尝试从同名模块导入所有公开接口
    from .markdown_readtime import (
        ReadSpeed,
        ReadTime,
        estimate,
        minutes,
        seconds,
        words,
    )
    
    __all__ = ["ReadSpeed", "ReadTime", "estimate", "minutes", "seconds", "words"]
except ImportError:
    # 如果无法导入，可能是扩展模块尚未构建
    import warnings
    warnings.warn("Rust extension module not found. Run 'maturin develop' to build it.")