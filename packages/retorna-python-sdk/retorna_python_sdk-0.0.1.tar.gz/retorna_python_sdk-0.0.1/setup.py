from pathlib import Path

from setuptools import find_packages, setup

LIBRARY_VERSION: str = "0.0.1"


def load_requirements(filename: str):
    """Reads dependencies from a file, ignoring comments and empty lines."""
    filepath = Path(filename)
    if not filepath.exists():
        return []

    return [
        line.strip()
        for line in filepath.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]


setup(
    name="retorna-python-sdk",
    version=LIBRARY_VERSION,
    description="SDK de Retorna para Python que permite integrar pagos, cobros y servicios B2B.",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Ulises Navarrete",
    author_email="unavarrete@retorna.app",
    url="https://github.com/retorna-tech/retorna-python-sdk",
    python_requires=">=3.9",
    classifiers=["Programming Language :: Python :: 3"],
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["tests", "tests.*"]),
    package_data={"retorna_sdk": ["py.typed"]},
    include_package_data=True,
    install_requires=load_requirements("requirements.txt"),
    zip_safe=False,
)
