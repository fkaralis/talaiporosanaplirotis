#!/usr/bin/env python
# -*- coding: utf-8 -*-
# module:

"""

"""

from sqlalchemy import Column, Integer, Float, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Kathgoria(Base):
    __tablename__ = "kathgoria"

    id = Column("kathgoria_id", Integer, primary_key=True)
    lektiko_kathgorias = Column("lektiko_kathgorias", String, nullable=False, unique=True)

    # relationships
    pinakes = relationship("Pinakas", back_populates="kathgoria")


class Real_eidikothta(Base):
    __tablename__ = "real_eidikothta"

    id = Column("real_eidikothta_id", Integer, primary_key=True)
    kodikos_real_eidikothtas = Column("kodikos_real_eidikothtas", String, nullable=False, unique=True)
    lektiko_real_eidikothtas = Column("lektiko_real_eidikothtas", String, nullable=False)


class Klados(Base):
    __tablename__ = "klados"

    id = Column("klados_id", Integer, primary_key=True)
    kodikos_kladoy = Column("kodikos_kladoy", String, nullable=False, unique=True)
    lektiko_kladoy = Column("lektiko_kladoy", String, nullable=False)
    real_eidikothta_id = Column(Integer, ForeignKey('real_eidikothta.real_eidikothta_id'))

    # relationships
    #eidikothtes = relationship("Eidikothta", back_populates="real_eidikothta_id")
    #pinakes = relationship("Pinakas", back_populates="eidikothta")

class Eidikothta(Base):
    __tablename__ = "eidikothta"

    id = Column("eidikothta_id", Integer, primary_key=True)
    kodikos_eidikothtas = Column("kodikos_eidikothtas", String, nullable=False, unique=True)
    lektiko_eidikothtas = Column("lektiko_eidikothtas", String, nullable=True)

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
    lektiko_hmeromhnias = Column("lektiko_hmeromhnias", String, nullable=False, unique=True)
    real_hmeromhnia = Column("real_hmeromhnia", Date, nullable=False, unique=True)


    # relationships
    #pinakes = relationship("Pinakas", back_populates="hmeromhnia")


class Pinakas(Base):
    __tablename__ = "pinakas"

    id = Column("pinakas_id", Integer, primary_key=True)
    lektiko_pinaka = Column("lektiko_pinaka", String, nullable=True)

    sxoliko_etos_id = Column(Integer, ForeignKey('sxoliko_etos.sxoliko_etos_id'))
    kathgoria_id = Column(Integer, ForeignKey('kathgoria.kathgoria_id'))
    eidikothta_id = Column(Integer, ForeignKey('eidikothta.eidikothta_id'))
    hmeromhnia_id = Column(Integer, ForeignKey('hmeromhnia.hmeromhnia_id'))

    path_pinaka = Column("path_pinaka", String, nullable=False)
    url_pinaka = Column("url_pinaka", String, nullable=False, unique=True)

    sxoliko_etos = relationship("Sxoliko_etos", back_populates="pinakes")
    kathgoria = relationship("Kathgoria", back_populates="pinakes")
    eidikothta = relationship("Eidikothta", back_populates="pinakes")
    #hmeromhnia = relationship("Hmeromhnia", back_populates="pinakes")


__all__ = [
    "Kathgoria",
    "Real_eidikothta",
    "Klados",
    "Eidikothta",
    "Sxoliko_etos",
    "Hmeromhnia",
    "Pinakas",
]

