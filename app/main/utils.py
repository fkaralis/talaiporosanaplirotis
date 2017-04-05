#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# module: app/main/utils.py
from flask import after_this_request

import re
import os
import gzip
from pathlib import Path
import pandas as pd


def match_klados(field, klados_id, pinakas_klados_id):
	print('in match klados', field, klados_id)
	if re.match('^' + klados_id +'$', pinakas_klados_id) or re.match('^' + klados_id + '\s(.)*$', pinakas_klados_id) or re.match('^(.)*\s' + klados_id + '$', pinakas_klados_id) or re.match('^(.)*\s' + klados_id + '\s(.)*$', pinakas_klados_id):
		return True
	else:
		return False


def unzip_to_df(filename, path_pinaka, data_path, temp_path):
    # unzip file in temp folder
    # rename unzipped file
    # returns data frame

    file_path = os.path.join(data_path, path_pinaka, filename)
    csv_temp_file_path = Path(temp_path + '/' + path_pinaka + filename[:-3])
    csv_temp_file_path.parent.mkdir(parents=True, exist_ok=True)

    #print(file_path, csv_temp_file_path)

    #gz to csv
    with gzip.open(file_path, 'rb') as infile:
        with open(str(csv_temp_file_path), 'wb') as outfile:
            for line in infile:
                outfile.write(line)

    #csv to df
    df = pd.read_csv(str(csv_temp_file_path))

    #fix row index
    try:
        df.set_index(['Α/Α'], inplace=True)
    except Exception as e:
        print(e)
        try:
            df.set_index(['α/α'], inplace=True)
        except Exception as e:
            print(e)
            try:
                df.set_index(['ΣΕΙΡΑ ΠΙΝΑΚΑ'], inplace=True)
            except Exception as e:
                print(e)
                df.index += 1
    df.index.name=None
    df = df.drop(['Unnamed: 0'], axis=1)

    @after_this_request
    def delete_file(response):
        # remove temp csv file
        try:
            os.remove(str(csv_temp_file_path))
        except Exception as e:
            print(e)
        return response

    return(df)
