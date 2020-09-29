from setuptools import setup

packages = [
    'crf_helper',
    'data_utils',
    'trie',
    'term_weight',
    'language_model'
]

setup(
    name='hammer',

    version='0.1',
    packages=packages,
    url='https://github.com/yydai/hammer',
    author='yydai',
    author_email='yingdai@zju.edu.cn',

    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.6'
    ],
    keywords=['crf', 'data', 'language model', 'term weight'],
    install_requires=[
        'requests>=1.0',
        'numpy',
        'jieba>=0.42.1',
        'nltk'
    ]
)
