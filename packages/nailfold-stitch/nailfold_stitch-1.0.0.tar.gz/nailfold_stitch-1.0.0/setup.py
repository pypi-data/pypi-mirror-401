# 导入打包必需的库
from setuptools import setup, find_packages


# 核心配置
setup(
    # 1. 基础信息【必填，重点修改】
    name="nailfold_stitch",          # 你的SDK包名，pip install 安装时用这个名字，建议和主包目录名一致/相近
    version="1.0.0",          # SDK版本号，比如1.0.0、1.0.1，更新时修改版本号即可
    author="Jianan Lin",         # 作者名
    author_email="1614875545@qq.com",   # 作者邮箱（可选）
    description="This is my first Python SDK, intended for testing packaging.", # 简短描述
    # long_description="详细的SDK介绍，可以写功能说明、使用方法等", # 详细描述（可选）
    url="https://github.com/你的仓库地址", # 项目地址（可选，比如github/gitlab）

    # 2. 打包配置【必填，无需修改，通用配置】
    packages=find_packages(),  # 自动查找项目中所有的Python包（含子模块），完美适配所有目录结构
    include_package_data=True, # 是否包含包中的静态资源文件（比如配置、图片），建议开启
    python_requires=">=3.4",   # 支持的Python版本，根据你的项目修改（比如>=3.6）

    # 3. 依赖库配置【按需修改，超级重要】
    # 你的SDK运行时需要的第三方库，比如需要requests、pandas，就写在这里
    # 格式：包名==版本号 （指定版本） 或 包名>=版本号 （兼容更高版本）
    install_requires=[
        "requests>=2.28.0",
        "pandas>=1.1.5",
        "numpy>=1.19.5"
    ],

    # 4. 可选配置（默认即可，不用改）
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)