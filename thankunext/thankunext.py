import argparse
import requests
import re

class ThankUNext:
    """Class for gathering routes related to a NextJs application."""

    def __init__(self):
        """Initialize the ThankUNext class."""
        self.parser = self._create_parser()

    def _create_parser(self):
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(description='Easily gather all routes related to a NextJs application through parsing of _buildManifest.js')
        parser.add_argument('url', help='URL to scan e.g. thankunext example.com')
        return parser

    def parse_url(self, url):
        """Parse and validate the URL.

        Args:
            url (str): The URL to parse and validate.

        Returns:
            str: The validated URL or None if invalid.
        """
        if not url.startswith('http://') and not url.startswith('https://'):
            print("Please include the protocol (http:// or https://) in the URL.")
            return None
        return url

    def get_page_content(self, url):
        """Fetch the content of the page at the given URL.

        Args:
            url (str): The URL of the page to fetch.

        Returns:
            str: The content of the page, or None if an error occurs.
        """
        try:
            headers = {'user-agent': 'thankunext/1.0'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error when accessing the URL: {e}")
            return None

    def get_build_manifest_path(self, body_content):
        """Extract the path to the build manifest file from the page content.

        Args:
            body_content (str): The content of the page.

        Returns:
            str: The path to the build manifest file, or None if not found.

        Explanation:
        The regular expression used to extract the path to the build manifest file is:
        r'(?m)/_next/static/[\w-]+/_buildManifest\.js'

        - r'(?m ... )': This denotes a raw string literal with the `MULTILINE` flag enabled. It allows the '^' and '$' anchors to match the start and end of each line in addition to the start and end of the string.
        - '/_next/static/': Matches the literal string '/_next/static/', which is the common prefix for the build manifest file path in Next.js applications.
        - '[\w-]+': Matches one or more occurrences of any word character (alphanumeric character or underscore) or hyphen. This matches the version hash or other characters in the path.
        - '/_buildManifest\.js': Matches the literal string '/_buildManifest.js'. The backslash before the dot escapes it, ensuring it matches a literal dot.

        The overall pattern matches paths to the build manifest file in the page content, considering the multi-line nature of the content. If a match is found, it returns the matched string representing the path to the build manifest file; otherwise, it returns None.
        """
        re_pattern = r'(?m)/_next/static/[\w-]+/_buildManifest\.js'
        match = re.search(re_pattern, body_content)
        if match:
            return match.group()
        return None

    def get_build_manifest_content(self, build_manifest_url):
        """Fetch the content of the build manifest file.

        Args:
            build_manifest_url (str): The URL of the build manifest file.

        Returns:
            str: The content of the build manifest file, or None if an error occurs.
        """
        try:
            headers = {'user-agent': 'thankunext/1.0'}
            response = requests.get(build_manifest_url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error accessing buildManifest content: {e}")
            return None

    def parse_build_manifest_content(self, build_manifest_content):
        """Parse the content of the build manifest file and extract paths.

        Args:
            build_manifest_content (str): The content of the build manifest file.

        Returns:
            set: A set of paths extracted from the build manifest content.

        Explanation:
        The regular expression used to extract paths from the build manifest content is:
        r'"(/[a-zA-Z0-9_/\[\]\.-]+)"'

        - r'(? ... )': This denotes a raw string literal, which is used to represent regular expressions.
        - '/': Matches the forward slash character, which is the delimiter for paths in URLs.
        - '[a-zA-Z0-9_/': Matches any alphanumeric character (lowercase and uppercase), underscores, and forward slashes.
        - '\[\]': Matches square brackets literally. Since square brackets have special meaning in regular expressions, they need to be escaped with backslashes to be treated as literals.
        - '\.': Matches the period (dot) character literally. Again, the dot has special meaning in regular expressions, so it needs to be escaped to match a literal dot.
        - '+': Matches one or more occurrences of the preceding pattern. This ensures that paths consisting of multiple characters are matched.

        The overall pattern matches strings that start with a double quote, followed by a forward slash and a sequence of characters (alphanumeric, underscores, forward slashes, square brackets, and periods), and ends with another double quote. These strings are considered paths and are extracted from the build manifest content.
        """
        re_pattern = r'"(/[a-zA-Z0-9_/\[\]\.-]+)"'
        paths = set(re.findall(re_pattern, build_manifest_content))
        return paths

    def start(self):
        """Main method to coordinate the execution flow."""
        args = self.parser.parse_args()
        url = self.parse_url(args.url)
        if not url:
            return
        page_content = self.get_page_content(url)
        if not page_content:
            return
        build_manifest_path = self.get_build_manifest_path(page_content)
        if not build_manifest_path:
            print("_buildManifest.js wasn't found. Is this site really running Next.js?")
            return
        build_manifest_url = url + build_manifest_path
        build_manifest_content = self.get_build_manifest_content(build_manifest_url)
        if not build_manifest_content:
            return
        paths = self.parse_build_manifest_content(build_manifest_content)
        print("\n".join(paths))


