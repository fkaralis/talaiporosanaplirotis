#!/usr/bin/env python
# -*- coding: utf-8 -*-
# module:

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, Float, String, Text, Date, ForeignKey
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base


convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}


metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)


class Kathgoria(Base):
    __tablename__ = "kathgoria"

    id = Column("kathgoria_id", Integer, primary_key=True)
    lektiko_kathgorias = Column("lektiko_kathgorias", String, nullable=False, unique=True)

    # relationships
    pinakes = relationship("Pinakas", back_populates="kathgoria")
    
class Eidikothta(Base):
    __tablename__ = "eidikothta"

    id = Column("eidikothta_id", Integer, primary_key=True)
    kodikos_eidikothtas = Column("kodikos_eidikothtas", String, nullable=False)
    lektiko_eidikothtas = Column("lektiko_eidikothtas", String, nullable=False)

    # relationships
    pinakes = relationship("Pinakas", back_populates="eidikothta")
    
class Sxoliko_etos(Base):
    __tablename__ = "sxoliko_etos"
    
    id = Column("sxoliko_etos_id", Integer, primary_key=True)
    lektiko_sxolikoy_etoys = Column("lektiko_sxolikoy_etoys", String, nullable=False, unique=True)
    
    # relationships
    pinakes = relationship("Pinakas", back_populates="sxoliko_etos")
    
class Hmeromhnia(Base):
    __tablename__ = "hmeromhnia"
    
    id = Column("hmeromhnia_id", Integer, primary_key=True)
    lektiko_sxolikoy_etoys = Column("lektiko_hmeromhnias", String, nullable=False, unique=True)
    
    # relationships
    #pinakes = relationship("Pinakas", back_populates="hmeromhnia")

class Pinakas(Base):
    __tablename__ = "pinakas"

    id = Column("pinakas_id", Integer, primary_key=True)
    lektiko_pinaka = Column("lektiko_pinaka", String, nullable=True, unique=True)
    
    sxoliko_etos_id = Column(Integer, ForeignKey('sxoliko_etos.sxoliko_etos_id'))
    kathgoria_id = Column(Integer, ForeignKey('kathgoria.kathgoria_id'))
    eidikothta_id = Column(Integer, ForeignKey('eidikothta.eidikothta_id'))
    hmeromhnia_id = Column(Integer, ForeignKey('hmeromhnia.hmeromhnia_id'))
    
    path_pinaka = Column("path_pinaka", String, nullable=False, unique=True)
    
    sxoliko_etos = relationship("Sxoliko_etos", back_populates="pinakes")
    kathgoria = relationship("Kathgoria", back_populates="pinakes")
    eidikothta = relationship("Eidikothta", back_populates="pinakes")
    #hmeromhnia = relationship("Hmeromhnia", back_populates="pinakes")

    


#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///talaiporosanaplirotis.sqlite')
#Session = sessionmaker(bind=engine)
#session = Session()

Base.metadata.create_all(engine)
