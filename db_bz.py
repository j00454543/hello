#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
from sqlalchemy import create_engine
# from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import ClauseElement
engine = None


def getDBConf():
    '''
    >>> getDBConf()
    <Section: db>
    '''
    config = configparser.ConfigParser()
    config.read('conf/db.ini')
    return config['db']


def getEngine():
    '''
    >>> getEngine()
    Engine(...
    '''

    global engine
    if engine is not None:
        return engine

    db_conf = getDBConf()
    connect_str = "postgresql+psycopg2://%s:%s@%s:%s/%s" % (
        db_conf['user'],
        db_conf['password'],
        db_conf['host'],
        db_conf['port'],
        db_conf['db_name'],
    )
    engine = create_engine(connect_str, echo=False)

    return engine


def getSession():
    '''
    >>> getSession()
    <sqlalchemy.orm.session.Session object at ...
    '''
    engine = getEngine()
    Session = sessionmaker(bind=engine)
    return Session()


def getOrInsert(session, model, defaults=None, **kwargs):
    '''
    不存在就 insert 附加 true, 存在就取出 附加 false
    >>> import model_bz
    >>> session = getSession()
    >>> oauth_info = {'out_id': '1', 'type': 'twitter', 'name': 'test', 'avatar': 'test'}
    >>> getOrInsert(session, model_bz.OauthInfo, oauth_info, id=1)
    (<model_bz.OauthInfo object at ...
    '''
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


if __name__ == '__main__':

    import doctest
    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
