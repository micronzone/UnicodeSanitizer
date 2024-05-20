import os
import sys
import argparse
import unicodedata
import urllib.parse
import re
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def normalize_nfc(path):
    nfc_path = unicodedata.normalize('NFC', path)
    return nfc_path if path != nfc_path else None

def decode_url(path):
    decoded_path = urllib.parse.unquote(path)
    return decoded_path if path != decoded_path else None

def has_decomposed_korean(name):
    return any('ᄀ' <= char <= 'ᇿ' for char in name)

def fix_decomposed_chars(path):
    if has_decomposed_korean(path):
        composed_path = unicodedata.normalize('NFC', path)
        return composed_path if path != composed_path else None
    return None

def rename_file(old_path, new_path):
    try:
        if old_path == new_path:
            return new_path

        dirname, basename = os.path.split(new_path)
        filename, ext = os.path.splitext(basename)

        counter = 1
        while os.path.exists(new_path):
            if unicodedata.normalize('NFC', basename) == basename:
                os.rename(old_path, new_path)
                return new_path
            new_path = os.path.join(dirname, f"{filename}({counter}){ext}")
            counter += 1

        os.rename(old_path, new_path)
        return new_path
    except Exception as e:
        logger.error(f"Error renaming {old_path} to {new_path}: {e}")
        return None

def process_directory(directory, processor, ignore_nfc=False):
    changes = []
    for root, dirs, files in os.walk(directory):
        for name in files + dirs:
            old_path = os.path.join(root, name)
            if ignore_nfc and unicodedata.normalize('NFC', name) == name:
                continue
            new_path = processor(old_path)
            if new_path:
                changes.append((old_path, new_path))
    return changes

def confirm_and_execute(changes):
    if not changes:
        logger.info("No files to convert.")
        return

    logger.info("The following files will be renamed:")
    for old_path, new_path in changes:
        logger.info(f"{old_path} -> {new_path}")

    confirm = input("Proceed with renaming? (y/n): ")
    if confirm.lower() != 'y':
        logger.info("Renaming cancelled.")
        return

    total = len(changes)
    for idx, (old_path, new_path) in enumerate(changes, start=1):
        if rename_file(old_path, new_path):
            logger.info(f"Progress: {idx}/{total} ({(idx/total)*100:.2f}%) files renamed.")
        else:
            logger.error(f"Failed to rename: {old_path}")

    logger.info("File renaming completed.")

def execute_tasks(path, tasks):
    for task in tasks:
        changes = process_directory(path, task['processor'], ignore_nfc=task.get('ignore_nfc', False))
        confirm_and_execute(changes)

def main():
    parser = argparse.ArgumentParser(description="Smart script to normalize problematic file names")
    parser.add_argument("-a", action="store_true", help="Execute all options sequentially")
    parser.add_argument("-k", action="store_true", help="Convert filenames with Korean characters to NFC format")
    parser.add_argument("-u", action="store_true", help="Decode URL encoded filenames")
    parser.add_argument("-f", action="store_true", help="Fix decomposed characters in filenames")
    parser.add_argument("--debug", nargs='?', const=True, help="Enable debugging logs")
    parser.add_argument("path", type=str, nargs="?", default=".", help="Target directory path")

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG if args.debug is True else args.debug)
        logger.debug("Debugging logs enabled.")

    path = os.path.expanduser(args.path)

    tasks = []
    if args.a:
        tasks = [
            {'processor': normalize_nfc, 'ignore_nfc': True},
            {'processor': decode_url},
            {'processor': fix_decomposed_chars, 'ignore_nfc': True}
        ]
    else:
        if args.k:
            tasks.append({'processor': normalize_nfc, 'ignore_nfc': True})
        if args.u:
            tasks.append({'processor': decode_url})
        if args.f:
            tasks.append({'processor': fix_decomposed_chars, 'ignore_nfc': True})

    try:
        execute_tasks(path, tasks)
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

