#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# module: app/main/utils.py
import os
import gzip
from pathlib import Path
def unzip_rename(filename, path_pinaka, data_path, temp_path):
    # unzip file in temp folder
    # rename unzipped file
    # returns temp_file

    file_path = os.path.join(data_path, path_pinaka, filename)
    temp_file_path = Path(temp_path + '/' + path_pinaka + filename[:-3])
    temp_file_path.parent.mkdir(parents=True, exist_ok=True)

    print(file_path, temp_file_path)

    with gzip.open(file_path, 'rb') as infile:
        with open(str(temp_file_path), 'wb') as outfile:
            for line in infile:
                outfile.write(line)

    return(temp_file_path)