# ThankUNext

ThankUNext is a Python tool, based on the [thankunext](https://github.com/c3l3si4n/thankunext) tool created by [c3l3si4n](https://github.com/c3l3si4n), for easily gathering all routes related to a Next.js application through parsing of _buildManifest.js.

## Installation

You can install ThankUNext via pip:

```bash
pip install thankunext
```

## Usage

```bash
thankunext <url>
```

Replace `<url>` with the URL of the Next.js application you want to scan.

Example:

```bash
thankunext https://example.com
```

## Features

- Fetches the content of the specified Next.js application page.
- Extracts the path to the build manifest file (_buildManifest.js) from the page content.
- Fetches the content of the build manifest file.
- Parses the build manifest content and extracts paths related to the Next.js application routes.
- Prints the extracted paths.

## Dependencies

ThankUNext relies on the following dependencies:

- Python >= 3.8
- requests >= 2.26.0

These dependencies will be automatically installed when you install ThankUNext via pip.

## Contributing

If you find any bugs or have suggestions for improvements, please feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/cowsecurity/thankunext). Your contributions are welcome!

## License

ThankUNext is licensed under the [MIT License](LICENSE), originally developed by [c3l3si4n](https://github.com/c3l3si4n).
