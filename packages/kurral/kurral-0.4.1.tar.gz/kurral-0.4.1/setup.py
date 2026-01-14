"""
Kurral Security Modules - Private Package Setup
"""

from setuptools import setup, find_packages

setup(
    name="kurral-security",
    version="0.4.0",
    description="Proprietary security assessment and monitoring for Kurral platform",
    author="Kurral Team",
    author_email="team@kurral.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "kurral>=0.3.0",  # Requires public Kurral package
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    private=True,  # Mark as private
)
