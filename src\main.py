import argparse
import os
import sys
import hashlib
from collections import defaultdict

def parse_size(size_str):
    size_str = size_str.strip().upper()
    if not size_str:
        raise ValueError("empty size")
    multipliers = {
        'TB': 1024**4, 'T': 1024**4,
        'GB': 1024**3, 'G': 1024**3,
        'MB': 1024**2, 'M': 1024**2,
        'KB': 1024,    'K': 1024,
        'B': 1,
    }
    suffixes = sorted(multipliers, key=len, reverse=True)
    for suffix in suffixes:
        if size_str.endswith(suffix):
            num_str = size_str[:-len(suffix)].strip()
            if not num_str:
                continue
            try:
                num = float(num_str)
                if num < 0:
                    raise ValueError("negative size")
                return int(num * multipliers[suffix])
            except ValueError:
                continue
    try:
        num = float(size_str)
        if num < 0:
            raise ValueError("negative size")
        return int(num)
    except ValueError:
        raise ValueError(f"Invalid size string: '{size_str}'")

def get_file_hash(filepath):
    hash_sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except (OSError, PermissionError):
        return None

def find_duplicates(root_path, recursive, min_size_bytes):
    hash_to_files = defaultdict(list)
    if recursive:
        for root, dirs, files in os.walk(root_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    size = os.path.getsize(filepath)
                    if size >= min_size_bytes:
                        file_hash = get_file_hash(filepath)
                        if file_hash is not None:
                            hash_to_files[file_hash].append((filepath, size))
                except (OSError, PermissionError):
                    pass
    else:
        try:
            items = os.listdir(root_path)
        except OSError:
            return {}
        for filename in items:
            filepath = os.path.join(root_path, filename)
            if os.path.isfile(filepath):
                try:
                    size = os.path.getsize(filepath)
                    if size >= min_size_bytes:
                        file_hash = get_file_hash(filepath)
                        if file_hash is not None:
                            hash_to_files[file_hash].append((filepath, size))
                except (OSError, PermissionError):
                    pass
    duplicates = {h: paths for h, paths in hash_to_files.items() if len(paths) > 1}
    return duplicates

def main():
    parser = argparse.ArgumentParser(
        description="CLI tool to find duplicate files by hashing contents in directories."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Directory path to scan (default: current directory)"
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Scan directories recursively"
    )
    parser.add_argument(
        "--min-size",
        default="0",
        help="Minimum file size to consider (e.g., 1KB, 1MB, 10M). Default: 0"
    )
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.path):
        print(f"Error: '{args.path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    try:
        min_size_bytes = parse_size(args.min_size)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    duplicates = find_duplicates(args.path, args.recursive, min_size_bytes)

    if not duplicates:
        print("No duplicate files found.")
        return

    print(f"Found {len(duplicates)} group(s) of duplicates:")
    total_files = 0
    total_size = 0
    for hash_val, fileinfos in sorted(
        duplicates.items(),
        key=lambda x: sum(size for _, size in x[1]),
        reverse=True
    ):
        print(f"\nDuplicate files (SHA256: {hash_val[:16]}...):")
        for filepath, size in sorted(fileinfos, key=lambda x: x[0]):
            print(f"  {filepath} ({size:,} bytes)")
        group_size = sum(size for _, size in fileinfos)
        total_files += len(fileinfos)
        total_size += group_size
    print(f"\nTotal: {total_files} duplicate files across {len(duplicates)} groups, total size {total_size:,} bytes")

if __name__ == "__main__":
    main()
