from setuptools import find_packages, setup

#using readme file to populate description
with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="RollOutGui",
    version="0.0.1",
    description="A graphical user interface that analyzes eye movements per video frame",
    package_dir={"":"app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thebearslab/VReyetrack",
    author="FevroniaVanSickle",
    license="MIT",
    classifiers=[
                "License :: OSI Approved :: MIT License"
                "Programming Language :: Python :: 3.11",
                "Operating System :: OS Independent"],
    install_requires=["matplotlib", "opencv-python", "shapely", "Pillow"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"]
    },
    python_requires=">=3.10"

)