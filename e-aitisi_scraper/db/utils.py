#!/usr/bin/env python
# -*- coding: utf-8 -*-
# module: db/utils.py

"""

"""

import sqlalchemy
import sqlalchemy.orm


def get_one_or_create(session, model, create_method='', create_method_kwargs=None, **kwargs):
    """
    Return an existing record or create a new one.

    http://skien.cc/blog/2014/02/06/sqlalchemy-and-race-conditions-follow-up/

    """
    try:
        return session.query(model).filter_by(**kwargs).one(), True
    except sqlalchemy.orm.exc.NoResultFound:
        kwargs.update(create_method_kwargs or {})
        created = getattr(model, create_method, model)(**kwargs)
        try:
            session.add(created)
            session.flush()
            return created, False
        except sqlalchemy.exc.IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one(), True


__all__ = [
    "get_one_or_create",
]
