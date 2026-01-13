import setuptools

setuptools.setup(
    name="loadmemory",

    description="tools",
    long_description="tools",
    author="zhouwe1",
    author_email="zhouwei@live.it",
    url="https://github.com/zhouwe1/loadmemory_util",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    packages=setuptools.find_packages(),
    python_requires=">=3.10",
    package_data={
        "loadmemory": [
            "excel/*",
            "utils/*",
            "db/*"
        ]
    }
)
