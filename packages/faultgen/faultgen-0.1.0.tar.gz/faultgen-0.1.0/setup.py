from setuptools import setup

setup(
    name="faultgen",
    version="0.1.0",
    long_description="FaultGen",
    long_description_content_type="text/markdown",
    packages=["faultgen"],
    install_requires=["numpy",  "h5py", "matplotlib", "pandas"],
)
