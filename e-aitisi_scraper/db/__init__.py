#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# module:
# author: Panagiotis Mavrogiorgos <pmav99,gmail>

"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

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

from .utils import get_one_or_create
from .models import Kathgoria, Real_eidikothta, Klados, Sxoliko_etos, Hmeromhnia,\
Pinakas, Smeae_pinakas, Smeae_kathgoria, Perioxh, Mousiko_organo, Athlima,\
Smeae_kathgoria_greeklish, Perioxh_greeklish, Mousiko_organo_greeklish, Athlima_greeklish

__all__ = [
    "metadata",
    "Base",
    "get_one_or_create",
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
    "Smeae_kathgoria_greeklish",
    "Perioxh_greeklish",
    "Mousiko_organo_greeklish",
    "Athlima_greeklish",
]
