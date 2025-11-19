from setuptools import setup, find_packages

setup(
    name="loja-online",
    version="1.0.0",
    description="Sistema simples de loja online",
    author="Equipe TP1",
    author_email="equipe@exemplo.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "loja-online=loja_online.main:main",
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
)