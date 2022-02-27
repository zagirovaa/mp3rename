import os
import sys
import glob
import uuid

MODES = ("byuuid", "bycode")
TEMPLATE = "*.mp3"
EXTENSION = ".mp3"
    

# Two parameters must be passed
# - folder with files
# - rename mode (byuuid, bycode)
if len(sys.argv) > 2:
    folder = sys.argv[1]
    mode = sys.argv[2]
    if os.path.isdir(folder) and mode in MODES:
        list_of_files = glob.glob(folder + TEMPLATE)
        # There have to be at least one file
        if list_of_files:
            # ByUUID
            if mode == MODES[0]:
                for old_file in list_of_files:
                    new_name = folder + str(uuid.uuid4()) + EXTENSION
                    os.rename(old_file, new_name)
                    print('--->>> File {} was renamed to {}'.format(old_file, new_name))
            # ByCode
            else:
                new_name = ''
                for old_file in list_of_files:
                    for symbol in os.path.splitext(os.path.basename(old_file))[0]:
                        new_name += str(ord(symbol))
                    new_name += EXTENSION
                    os.rename(old_file, new_name)
                    print('--->>> File {} was renamed to {}'.format(old_file, new_name))
        else:
            print('No file found.')
    else:
        print('Error in passed parameters.')
else:
    print('Pass all the necessary parameters.')
