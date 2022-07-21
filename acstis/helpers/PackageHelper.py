import os
import re

import pkg_resources


class PackageHelper:
    """The Package class contains all the package related information (like the version number).

    _name (str): Cached package name.
    _description (str): Cached package description.
    _alias (str): Cached package alias.
    _version (str): Cached package version number (if initialized).

    """

    _name = "ACSTIS"

    _description = "Automated client-side template injection (sandbox escape/bypass) detection for AngularJS."

    _alias = "acstis"

    _version = None

    @staticmethod
    def get_name():
        """Get the name of this package.

        Returns:
            str: The name of this package.

        """

        return PackageHelper._name

    @staticmethod
    def get_description():
        """Get the description of this package.

        Returns:
            str: The description of this package.

        """

        return PackageHelper._description

    @staticmethod
    def get_alias():
        """Get the alias of this package.

        Returns:
            str: The alias of this package.

        """

        return PackageHelper._alias

    @staticmethod
    def get_version():
        """Get the version number of this package.

        Returns:
            str: The version number (marjor.minor.patch).

        Note:
            When this package is installed, the version number will be available through the
            package resource details. Otherwise this method will look for a ``.semver`` file.

        Note:
            In rare cases corrupt installs can cause the version number to be unknown. In this case
            the version number will be set to the string "Unknown".

        """

        if PackageHelper._version:
            return PackageHelper._version

        PackageHelper._version = "Unknown"

        # If this is a GIT clone without install, use the ``.semver`` file.
        file = os.path.realpath(__file__)
        folder = os.path.dirname(file)

        try:
            with open(f"{folder}/../../.semver", "r") as semver:
                PackageHelper._version = semver.read().rstrip()
            return PackageHelper._version
        except Exception as e:
            print(e)

        # If the package was installed, get the version number via Python's distribution details.
        try:
            distribution = pkg_resources.get_distribution(PackageHelper.get_alias())
            if distribution.version:
                PackageHelper._version = distribution.version
            return PackageHelper._version
        except Exception as e:
            print(e)

        return PackageHelper._version

    @staticmethod
    def rst_to_pypi(contents):
        """
        Convert the given GitHub RST contents to PyPi RST contents
        (since some RST directives are not available in PyPi).

        Args:
            contents (str): The GitHub compatible RST contents.

        Returns:
            str: The PyPi compatible RST contents.

        """

        # The PyPi description does not support the SVG file type.
        contents = contents.replace(".svg?pypi=png.from.svg", ".png")

        # Convert ``<br class="title">`` to a H1 title
        asterisks_length = len(PackageHelper.get_name())
        asterisks = "*" * asterisks_length
        title = asterisks + "\n" + PackageHelper.get_name() + "\n" + asterisks

        contents = re.sub(r"(\.\. raw:: html\n)(\n {2,4})(<br class=\"title\">)", title, contents)

        # The PyPi description does not support raw HTML
        contents = re.sub(r"(\.\. raw:: html\n)((\n {2,4})([A-Za-z\d<> =\"/])*)*", "", contents)

        return contents
