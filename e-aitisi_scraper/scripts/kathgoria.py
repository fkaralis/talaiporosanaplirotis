#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from db import Base, get_one_or_create
from db import Kathgoria, Pinakas


engine = create_engine('sqlite:///talaiporosanaplirotis.sqlite')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


kathgories = session.query(Kathgoria).filter(Kathgoria.id>=24).all()

for kathgoria in kathgories:
    print(kathgoria.lektiko_kathgorias)

pinakes = session.query(Pinakas).filter(Pinakas.kathgoria_id>=24).all()

for pinakas in pinakes:
    if pinakas.kathgoria_id == 25:
        print(pinakas.id, pinakas.kathgoria_id)
        pinakas.kathgoria_id = 5
        print(pinakas.id, pinakas.kathgoria_id)

session.commit()
