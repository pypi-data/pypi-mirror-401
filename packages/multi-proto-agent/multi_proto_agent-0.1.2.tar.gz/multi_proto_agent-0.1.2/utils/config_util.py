import os
import sys
import yaml
from utils.logger_config import get_logger

logger = get_logger(__name__)


def find_root_directory(start_file=None, root_marker='i_am_the_root.md'):
    """
    通过查找 i_am_the_root.md 文件来定位项目根目录
    
    Args:
        start_file: 起始文件路径（通常是 __file__），如果为None则使用当前工作目录
        root_marker: 根目录标记文件名，默认是 i_am_the_root.md
    Returns:
        项目根目录的绝对路径
    """
    if start_file is None:
        # 如果没有指定起始文件，使用当前工作目录
        start_path = os.getcwd()
    else:
        # 如果是文件路径，获取其所在目录
        if os.path.isfile(start_file):
            start_path = os.path.dirname(os.path.abspath(start_file))
        else:
            start_path = os.path.abspath(start_file)
    
    # 从起始路径开始向上查找，直到找到包含 i_am_the_root.md 的目录
    search_dir = start_path
    while True:
        root_marker = os.path.join(search_dir, root_marker)
        if os.path.exists(root_marker):
            return search_dir
        parent_dir = os.path.dirname(search_dir)
        # 如果已经到达文件系统根目录，停止查找
        if parent_dir == search_dir:
            raise FileNotFoundError(f"无法找到项目根目录（未找到 {root_marker} 文件）")
        search_dir = parent_dir


def add_python_protos_to_path(python_protos_path=None):
    """
    将python_protos目录及其所有子目录添加到Python路径中
    Args:
        python_protos_path: python_protos目录路径，如果为None则抛出异常
    """
    if python_protos_path is None:
        logger.error("python_protos_path 不能为空")
        raise ValueError("python_protos_path 不能为空")
    logger.info(f"将{python_protos_path}目录及其所有子目录添加到Python路径中")
    if os.path.exists(python_protos_path):
        # 添加python_protos根目录
        sys.path.append(python_protos_path)
        # 遍历python_protos下的所有子目录并添加到路径
        for item in os.listdir(python_protos_path):
            item_path = os.path.join(python_protos_path, item)
            if os.path.isdir(item_path):
                sys.path.append(item_path)

#这个方法用于读取protos_config.yaml文件，将其中的键值对设置为环境变量
def set_protos_config(config_path=None):
    """
    读取protos_config.yaml文件，将其中的键值对设置为环境变量
    Args:
        config_path: protos_config.yaml文件路径，如果为None则抛出异常
    """
    if config_path is None:
        logger.error("config_path 不能为空")
        raise ValueError("config_path 不能为空")
    if not os.path.exists(config_path):
        logger.error(f"config_path {config_path} 不存在")
        raise FileNotFoundError(f"config_path {config_path} 不存在")
    with open(config_path, 'r', encoding='utf-8') as f:
        protos_config_data = yaml.safe_load(f)
    for key, value in protos_config_data.items():
        os.environ[key] = value

def get_env_options(config_path=None):
    """获取环境选项列表，用于data_factory前端选择执行环境
    返回格式: [{"value": "env_key", "label": "env_name"}, ...]
    """
    if config_path is None:
        logger.error("config_path 不能为空")
        raise ValueError("config_path 不能为空")
    if not os.path.exists(config_path):
        logger.error(f"config_path {config_path} 不存在")
        raise FileNotFoundError(f"config_path {config_path} 不存在")
    with open(config_path, 'r', encoding='utf-8') as f:
        env_data = yaml.safe_load(f)
    if not env_data or 'env' not in env_data:
        logger.error("env_data 格式不正确，env_data: {env_data}")
        raise ValueError(f"env_data 格式不正确，env_data: {env_data}")
    options = []
    for env_key, env_config in env_data['env'].items():
        env_name = env_config.get('env_name', env_key)
        options.append({"value": env_key, "label": env_name})
    return options

def set_config(env_type, config_path=None):
    """
    设置测试环境信息
    Args:
        env_type: 环境类型
        config_path: env_config.yaml文件路径，如果为None则抛出异常
    """
    # 设置测试环境信息
    if config_path is None:
        logger.error("config_path 不能为空")
        raise ValueError("config_path 不能为空")
    if not os.path.exists(config_path):
        logger.error(f"config_path({config_path}) 不存在")
        raise FileNotFoundError(f"config_path({config_path}) 不存在")
    with open(config_path, 'r', encoding='utf-8') as f:
        env_data = yaml.safe_load(f)
    if not env_type or env_type == "" or not env_data['env'].get(env_type):
        logger.error("不是接口测试覆盖的环境，终止测试！")
        exit(0)
    # os.environ['env_type'] = env_type
    # 遍历cmd_env下的所有属性，并设置环境变量
    for key, value in env_data['env'][env_type].items():
        os.environ[key] = str(value)  # 确保值是字符串类型