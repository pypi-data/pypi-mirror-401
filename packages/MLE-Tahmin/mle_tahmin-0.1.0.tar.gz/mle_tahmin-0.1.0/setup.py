from setuptools import setup, find_packages

setup(
    name="MLE-Tahmin",           # Paket adı
    version="0.1.0",             # Sürüm
    author="Melih Karagülmez",
    author_email="melih282004@gmail.com",  # istersen e-posta
    description="Aktüerya MLE parametre tahmin sistemi (Gamma, Pareto, Lomax)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/melih2861/MLE-Tahmin",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pandas",
        "numpy",
        "scipy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "mle-tahmin=main:main",  # Eğer main.py’de main() fonksiyonunu tanımlarsan
        ],
    },
)
