# Duplicate File Finder

A lightweight CLI tool to scan directories for duplicate files by computing SHA256 hashes of file contents. It supports recursive scanning, minimum file size filtering with human-readable units (e.g., 1KB, 1MB), and efficient chunked hashing. Gracefully skips inaccessible files and provides clear output on matches.

## Installation

1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd duplicate-file-finder
   ```
2. No external dependencies required (uses Python standard library only).
3. Run directly:
   ```
   python src/main.py [OPTIONS] [PATH]
   ```

## Usage

```
usage: main.py [-h] [-r] [--min-size MIN_SIZE] [path]

CLI tool to find duplicate files by hashing contents in directories.

positional arguments:
  path                 Directory path to scan (default: current directory)

options:
  -h, --help           show this help message and exit
  -r, --recursive      Scan directories recursively
  --min-size MIN_SIZE  Minimum file size to consider (e.g., 1KB, 1MB, 10M).
                       Default: 0
```

### Examples

- Show help:
  ```
  python src/main.py --help
  ```

- Scan current directory (non-recursive):
  ```
  python src/main.py
  ```
  Output (if no duplicates): `No duplicate files found.`

- Scan specific directory recursively:
  ```
  python src/main.py --recursive /path/to/dir
  ```

- Scan with minimum file size:
  ```
  python src/main.py --min-size 1MB /path/to/dir
  ```

## Features

- Recursive or non-recursive directory scanning
- Flexible minimum file size filtering (supports KB, MB, GB, TB suffixes; defaults to 0)
- SHA256 content hashing with efficient 4KB chunking
- Groups duplicates by hash with file paths and sizes
- Robust error handling (skips permission/errors without crashing)
- Sorted, informative console output

## Dependencies

Python 3.x standard library only:
- `argparse`
- `os`
- `sys`
- `hashlib`
- `collections`

## License

MIT License - see [LICENSE](LICENSE) for details.