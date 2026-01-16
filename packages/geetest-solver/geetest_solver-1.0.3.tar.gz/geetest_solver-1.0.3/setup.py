from setuptools import setup, find_packages
import os

setup(
    name="geetest-solver",
    version="1.0.3",
    author="kv",
    description="GeeTest v4 ICON CAPTCHA solver using YOLO + template matching",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/syncrain/geetest-solver.git",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "ultralytics>=8.0.0",
        "opencv-python>=4.8.0",
        "pillow>=10.0.0",
        "numpy>=1.24.0",
        "pycryptodome>=3.19.0",
        "scipy>=1.11.0",
        "matplotlib>=3.7.0"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "captcha_solver": ["best.pt"],
    },
    include_package_data=True,
)
