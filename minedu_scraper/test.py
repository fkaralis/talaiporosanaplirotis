#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#### 30/3/2017
### test


import pandas as pd
import re
import os
import sys
import requests
import datetime
import gzip
import shutil
from pathlib import PurePosixPath
from pathlib import Path

import sqlalchemy
from sqlalchemy import and_
from sqlalchemy import or_

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app import db

from app.models import Athlima, Athlima_greeklish, Hmeromhnia, Kathgoria,\
Klados, Mousiko_organo, Mousiko_organo_greeklish, Perioxh, Perioxh_greeklish,\
Pinakas, Real_eidikothta, Smeae_kathgoria, Smeae_kathgoria_greeklish,\
Smeae_pinakas, Sxoliko_etos

app = create_app(os.getenv('TALAIPANAP_CONFIG') or 'default')

# talaiporosanaplirotis path
basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
datapath = os.path.join(os.path.dirname(basedir), 'app', 'static')

#kathgories = session.query(Kathgoria).filter_by().all()
print(datapath)
count = 0

kathgories = Kathgoria.query.all()

for kathgoria in kathgories:
    print(kathgoria.lektiko_kathgorias)

