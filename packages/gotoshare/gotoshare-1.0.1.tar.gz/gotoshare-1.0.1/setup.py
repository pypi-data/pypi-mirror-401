from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as f: long_description = f.read()
setup(
    name='gotoshare',
    version='1.0.1',
    description='GotoShare SDK - A股数据自托管服务客户端，与tushare接口兼容',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='GotoShare',
    author_email='gotoshare@example.com',
    url='https://github.com/gotoshare/gotoshare',
    packages=find_packages(),
    install_requires=['httpx>=0.24.0', 'pandas>=1.5.0'],
    python_requires='>=3.8',
    keywords=['stock', 'finance', 'tushare', 'A股', '量化'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Office/Business :: Financial :: Investment',
    ],
)
