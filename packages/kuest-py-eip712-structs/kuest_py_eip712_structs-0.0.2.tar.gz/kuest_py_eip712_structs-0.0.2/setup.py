import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kuest-py-eip712-structs",
    version="0.0.2",
    author="Kuest Engineering",
    author_email="engineering@kuest.com",
    maintainer="Kuest Engineering",
    maintainer_email="engineering@kuest.com",
    description="A python library for EIP712 objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kuestcom/py-eip712-structs",
    install_requires=[
        "eth-utils>=4.1.1",
        "pycryptodome>=3.20.0",
        "pytest"
    ],
    package_data={
        "py_order_utils": [
            "abi/*.json",
        ],
    },
    project_urls={
        "Bug Tracker": "https://github.com/kuestcom/py-eip712-structs",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9.10",
)
