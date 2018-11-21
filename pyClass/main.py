from pyClass import Class
from config import config
from pprint import pprint
import os
import json

if __name__ == "__main__":
    file_list = [config.apdBase, config.apdDriver]
    OUTDIR = "defnData"
    for each_file in file_list:
        out_filename = os.path.join('.', OUTDIR ,os.path.basename(each_file)[:-2]+"json")
        class_defn = Class(config.apdReport)
        with open(out_filename, 'w') as outfp:
            json.dump(class_defn.get_classes(), outfp)