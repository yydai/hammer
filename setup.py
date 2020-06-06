from setuptools import setup

setup(
    name='crf-helper',

    version='0.1',
    packages=['crf_helper', 'data_utils'],

    # The project's main homepage.
    url='https://github.com/yydai/crf-helper',
    author='yydai',
    author_email='yingdai@zju.edu.cn',

    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.6'
    ],
    keywords=['crf', 'data'],
    install_requires=[
        'requests>=1.0',
        'numpy'
    ]
)
