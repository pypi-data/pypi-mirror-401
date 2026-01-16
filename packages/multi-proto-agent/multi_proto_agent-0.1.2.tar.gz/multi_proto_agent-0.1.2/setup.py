from setuptools import setup, find_packages
 
setup(
    # name 和 version: 包的名称和版本，是包的唯一标识
    name='multi-proto-agent',
    version='0.1.2',
    # packages: 使用 find_packages() 自动找到所有应该包含的包
    packages=find_packages(),
    install_requires=[
        # 核心依赖 - 代码中直接使用的包
        'protobuf>=5.28.3',
        'PyYAML>=6.0.2',
        'jsonpath-ng>=1.7.0',
        'websocket-client>=1.9.0',
        'paramiko>=4.0.0',
        'requests>=2.32.3',
        'gevent>=25.9.1',
        # requests的依赖
        'certifi>=2024.7.4',
        'charset-normalizer>=3.3.2',
        'idna>=3.7',
        'urllib3>=2.2.2',
        # paramiko的依赖
        'bcrypt>=5.0.0',
        'cryptography>=46.0.1',
        'PyNaCl>=1.6.0',
        'cffi>=2.0.0',
        'pycparser>=2.23',
        # gevent的依赖
        'greenlet>=3.2.4',
        'zope.event>=6.0',
        'zope.interface>=8.0',
        # websocket-client的依赖
        'six>=1.16.0',
        # jsonpath-ng的依赖
        'ply>=3.11',
        'decorator>=5.1.1',
        # pytest相关 - 用于测试
        'pytest>=8.3.3',
        'pytest-html>=4.1.1',
        'pytest-metadata>=3.1.1',
        'pytest-order>=1.3.0',
        'pytest-ordering>=0.6',
        'pytest-repeat>=0.9.4',
        'pytest-timeout>=2.3.1',
        'pytest-xdist>=3.6.1',
        # pytest的依赖
        'attrs>=24.2.0',
        'iniconfig>=2.0.0',
        'pluggy>=1.5.0',
        'py>=1.11.0',
        'packaging>=25.0',
        'colorama>=0.4.6',
        # allure相关 - 用于测试报告
        'allure-pytest>=2.13.5',
        'allure-python-commons>=2.13.5',
        # allure的依赖
        'lxml>=5.3.0',
        # 其他工具依赖
        'execnet>=2.1.1',
        'python-dateutil>=2.9.0.post0',
        'pytz>=2024.2',
        'tzdata>=2024.2',
    ],
    entry_points={
        # 可执行脚本
    },
    author='Shi Feng',
    author_email='330550850@qq.com',
    # description 和 long_description: 简短和详细的包描述
    description='旨在简化基于多种协议的消息通信,内置了对JSON和Protobuf的序列化、反序列化支持，并设计为线程安全，让你可以轻松创建和管理成百上千个并发通信代理。',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://gitee.com/flinttina/multi-proto-agent',
    # classifiers: 提供关于包的元数据
    classifiers=[
        # 包的分类列表
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # python_requires: 指定项目所需的 Python 版本
    python_requires='>=3.8',
)