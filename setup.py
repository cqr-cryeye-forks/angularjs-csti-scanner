from setuptools import find_packages, setup

from acstis.helpers.PackageHelper import PackageHelper

with open("requirements.txt") as file:
    requirements = file.read().splitlines()

with open("README.rst") as file:
    readme = PackageHelper.rst_to_pypi(file.read())

setup(
    name=PackageHelper.get_alias(),
    version=PackageHelper.get_version(),
    description=PackageHelper.get_description(),
    long_description=readme,
    keywords=["vulnerability", "bug-bounty", "security", "angular", "csti", "client-side template injection",
              "scanner"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 2.7",
        "Topic :: Security"
    ],
    packages=find_packages(),
    package_data={
        "acstis": [
            "phantomjs/linux32-2.1.1",
            "phantomjs/linux64-2.1.1",
            "phantomjs/mac-2.1.1",
            "phantomjs/win-2.1.1.exe"
        ]
    },
    entry_points={
        'console_scripts': [
            'acstis = acstis_scripts.acstis_cli:main'
        ]
    },
    platforms=["any"],
    author="Tijme Gommers",
    author_email="acstis@finnwea.com",
    license="MIT",
    url="https://github.com/cqr-cryeye-forks/angularjs-csti-scanner",
    install_requires=[
        requirements,
        'nyawc @ git+https://github.com/cqr-cryeye-forks/not-your-average-web-crawler'
]
)
