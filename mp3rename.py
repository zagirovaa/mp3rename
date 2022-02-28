# -*- coding: utf-8 -*-


from __future__ import annotations
import logging
import os
import sys
import argparse
import glob
import uuid


MODES: Tuple[str, str] = ("byuuid", "bycode")
EXTENSION: str = ".mp3"
TEMPLATE: str = "*{}".format(EXTENSION)
DESCRIPTION: str = "The main task of this script is to rename mp3 files using random names."

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s [%(threadName)s] [%(levelname)s] - %(message)s",
    handlers = [
        logging.FileHandler("{0}/{1}.log".format(os.getcwd(), "mp3rename")),
        logging.StreamHandler(sys.stdout)
    ]
)


def get_args():
    """
    Returns the arguments passed to the application
    """

    parser: Object = argparse.ArgumentParser(description = DESCRIPTION)
    parser.add_argument('folder', 
                        metavar = "FOLDER", 
                        type = str, 
                        nargs = "?", 
                        default = os.getcwd(), 
                        help = "Folder with mp3 files.")
    parser.add_argument('mode', 
                        metavar = "MODE", 
                        type = str, 
                        nargs = "?", 
                        default = "byuuid", 
                        help = "Renaming mode (byuuid, bycode).")
    return parser.parse_args()


def main():
    """
    Aplication entry point
    """

    args: List[str] = get_args()
    # Folder name must end with a separator
    if args.folder[-1] is not os.sep:
        args.folder += os.sep
    if os.path.isdir(args.folder) and args.mode in MODES:
        list_of_files: List[str] = glob.glob(args.folder + TEMPLATE)
        # There have to be at least one file
        if list_of_files:
            # ByUUID
            if args.mode == MODES[0]:
                for old_file in list_of_files:
                    new_name: str = args.folder + str(uuid.uuid4()) + EXTENSION
                    try:
                        os.rename(old_file, new_name)
                        logging.info("File {} has been renamed to {}".format(old_file, new_name))
                    except Exception as error:
                        logging.error("Could not rename file {} using {} mode.".format(old_file, args.mode))
                        logging.error(error)
            # ByCode
            else:
                new_name: str = ""
                for old_file in list_of_files:
                    for symbol in os.path.splitext(os.path.basename(old_file))[0]:
                        new_name += str(ord(symbol))
                    new_name += EXTENSION
                    try:
                        os.rename(old_file, new_name)
                        logging.info("File {} has been renamed to {}".format(old_file, new_name))
                    except Exception as error:
                        logging.error("Could not rename file {} using {} mode.".format(old_file, args.mode))
                        logging.error(error)
        else:
            logging.error("Files not found.")
    else:
        logging.error("Error in passed parameters.")

if __name__ == "__main__":
    main()
