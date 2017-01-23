#!/usr/bin/env python3
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
    greek_lektiko_kathgorias = Column("greek_lektiko_kathgorias", String)

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
    #pinakes = relationship("Pinakas", back_populates="klados")


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

class Smeae_pinakas(Base):
    __tablename__ = "smeae_pinakas"

    id = Column("id", Integer, primary_key=True)
    lektiko = Column("lektiko", String, nullable=False, unique=True)

class Smeae_kathgoria(Base):
    __tablename__ = "smeae_kathgoria"

    id = Column("id", Integer, primary_key=True)
    lektiko = Column("lektiko", String, nullable=False, unique=True)

class Perioxh(Base):
    __tablename__ = "perioxh"

    id = Column("id", Integer, primary_key=True)
    lektiko = Column("lektiko", String, nullable=False, unique=True)

class Mousiko_organo(Base):
    __tablename__ = "mousiko_organo"

    id = Column("id", Integer, primary_key=True)
    lektiko = Column("lektiko", String, nullable=False, unique=True)

class Athlima(Base):
    __tablename__ = "athlima"

    id = Column("id", Integer, primary_key=True)
    lektiko = Column("lektiko", String, nullable=False, unique=True)


class Pinakas(Base):
    __tablename__ = "pinakas"

    id = Column("pinakas_id", Integer, primary_key=True)
    lektiko_pinaka = Column("lektiko_pinaka", String, nullable=True)

    sxoliko_etos_id = Column(Integer, ForeignKey('sxoliko_etos.sxoliko_etos_id'))
    kathgoria_id = Column(Integer, ForeignKey('kathgoria.kathgoria_id'))
    hmeromhnia_id = Column(Integer, ForeignKey('hmeromhnia.hmeromhnia_id'))
    klados_id = Column("klados_id", String, nullable=True)

    path_pinaka = Column("path_pinaka", String, nullable=False)
    url_pinaka = Column("url_pinaka", String, nullable=False, unique=True)

    smeae_pinakas_id = Column(Integer, ForeignKey('smeae_pinakas.id'))
    smeae_kathgoria_id = Column(Integer, ForeignKey('smeae_kathgoria.id'))
    perioxh_id = Column(Integer, ForeignKey('perioxh.id'))
    mousiko_organo_id = Column(Integer, ForeignKey('mousiko_organo.id'))
    athlima_id = Column(Integer, ForeignKey('athlima.id'))

    sxoliko_etos = relationship("Sxoliko_etos", back_populates="pinakes")
    kathgoria = relationship("Kathgoria", back_populates="pinakes")
    #hmeromhnia = relationship("Hmeromhnia", back_populates="pinakes")
    #klados = relationship("Klados", back_populates="pinakes")


__all__ = [
    "Kathgoria",
    "Real_eidikothta",
    "Klados",
    "Sxoliko_etos",
    "Hmeromhnia",
    "Pinakas",
    "Smeae_pinakas",
    "Smeae_kathgoria",
    "Perioxh",
    "Mousiko_organo",
    "Athlima",
]

