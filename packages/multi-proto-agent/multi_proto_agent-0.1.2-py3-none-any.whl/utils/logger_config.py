"""
日志配置模块
提供统一的logging配置，保持与原有log_print相同的时间格式
"""
import logging
import sys
import os
from datetime import datetime


class CustomFormatter(logging.Formatter):
    """自定义Formatter，保持原有log_print的时间格式：[yyyy-mm-dd HH:MM:SS.fff][级别]"""
    
    def format(self, record):
        # 获取当前时间并格式化为 yyyy-mm-dd HH:MM:SS.fff
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        # 获取日志级别名称
        level_name = record.levelname
        
        # 格式化日志消息：[时间][级别]消息内容
        message = super().format(record)
        formatted_message = f"[{formatted_time}][{level_name}]{message}"
        
        return formatted_message


def get_log_level_from_string(level_str):
    """
    从字符串转换为日志等级
    
    Args:
        level_str: 日志等级字符串（如 "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"）
    
    Returns:
        logging 日志等级常量
    
    Raises:
        ValueError: 如果字符串无效
    """
    if level_str is None:
        return logging.INFO
    
    level_str = level_str.upper().strip()
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }
    
    if level_str not in level_map:
        raise ValueError(f"无效的日志等级: {level_str}。支持的等级: {', '.join(level_map.keys())}")
    
    return level_map[level_str]


def setup_logging(level=None, log_dir="./logs"):
    """
    配置logging系统
    
    Args:
        level: 日志级别，默认为INFO。如果为None，则从环境变量LOG_LEVEL读取
        log_dir: 日志文件保存目录，默认为"./logs"
    """
    # 如果level为None，尝试从环境变量读取
    if level is None:
        env_level = os.getenv('LOG_LEVEL')
        if env_level:
            level = get_log_level_from_string(env_level)
        else:
            level = logging.INFO
    
    # 获取root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # 清除已有的handlers，避免重复添加
    root_logger.handlers.clear()
    
    # 设置自定义Formatter
    formatter = CustomFormatter()
    
    # 1. 创建StreamHandler，输出到stdout（确保pytest的--capture=sys能捕获，不影响allure）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 2. 创建FileHandler，输出到文件
    try:
        # 确保日志目录存在
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        # 生成日志文件名：test_YYYYMMDD_HHMMSS.log
        current_time = datetime.now()
        log_filename = f"test_{current_time.strftime('%Y%m%d_%H%M%S')}.log"
        log_file_path = os.path.join(log_dir, log_filename)
        
        # 创建文件handler
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        # 如果文件输出失败，不影响控制台输出和allure捕获
        # 只在控制台输出警告信息
        print(f"[警告] 无法创建日志文件: {e}", file=sys.stderr)
    
    # 确保编码支持UTF-8（Windows环境）
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def get_logger(name=None):
    """
    获取logger实例
    
    Args:
        name: logger名称，如果为None则使用调用模块的名称
    
    Returns:
        logging.Logger实例
    """
    if name is None:
        import inspect
        # 获取调用者的模块名
        frame = inspect.currentframe().f_back
        module_name = frame.f_globals.get('__name__', 'root')
        name = module_name
    
    # 确保logging已配置
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        setup_logging()
    
    return logging.getLogger(name)
