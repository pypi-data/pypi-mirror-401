from setuptools import setup, find_packages

# 读取 README.md 作为长描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="synbio-promoter-predictor",
    version="0.1.2", # ⚠️ 必须升级版本号！PyPI 不允许重复上传同版本
    author="Rong Fan",               # ← 改成你的真实姓名
    author_email="fandud@163.com",   # ← 改成你的邮箱（可虚构）
    description="A lightweight CLI tool for prokaryotic promoter prediction",  # ← 新增：一行简介
    long_description=long_description,  # ← 新增：完整描述
    long_description_content_type="text/markdown",  # ← 新增：告诉 PyPI 这是 Markdown
    license="MIT",  # ← 新增：许可证文本
    classifiers=[   # ← 新增：分类器（必须包含 License 和 Python 版本）
         "License :: OSI Approved :: MIT License",
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
         "Intended Audience :: Science/Research",
         "Topic :: Scientific/Engineering :: Bio-Informatics",
         ],
         # ========== 保留你原来的所有配置 ==========
    packages=find_packages(),
    install_requires=["pandas"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "promoter-predict=synbio_promoter.cli:main",
        ],
    },
)