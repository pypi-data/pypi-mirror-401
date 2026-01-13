from setuptools import setup, find_packages

# For backward compatibility with older pip versions
# Main configuration is in pyproject.toml

setup(
    name="vc-web-email",
    version="1.0.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
    install_requires=[
        "PyYAML>=6.0",
    ],
    extras_require={
        "sendgrid": ["sendgrid>=6.0"],
        "aws": ["boto3>=1.26"],
        "all": [
            "sendgrid>=6.0",
            "boto3>=1.26",
        ],
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
    },
)
