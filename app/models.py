from . import db

from sqlalchemy import Column, Integer, Float, String, Text, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = Column("id", Integer, primary_key=True, nullable=False)
    email = Column("email", String, unique=True, nullable=False)
    onoma = Column("onoma", String, nullable=False)

    def __repr__(self):
        return '<User id %r email %r onoma %r>' % (self.id, self.email, self.onoma)




class Kathgoria(db.Model):
    __tablename__ = "kathgoria"

    id = Column("kathgoria_id", Integer, primary_key=True)
    lektiko_kathgorias = Column("lektiko_kathgorias", String, nullable=False, unique=True)
    greek_lektiko_kathgorias = Column("greek_lektiko_kathgorias", String)

    # relationships
    pinakes = relationship("Pinakas", back_populates="kathgoria")

    def __repr__(self):
        return '\nΚατηγορία id %r\nλεκτικό %r' %\
            (self.id, self.lektiko_kathgorias)



class Real_eidikothta(db.Model):
    __tablename__ = "real_eidikothta"

    id = Column("real_eidikothta_id", Integer, primary_key=True)
    kodikos_real_eidikothtas = Column("kodikos_real_eidikothtas", String, nullable=False, unique=True)
    lektiko_real_eidikothtas = Column("lektiko_real_eidikothtas", String, nullable=False)

    def __repr__(self):
        return '\nΠραγματική ειδικότητα\nid %r\nκωδικός %r\nλεκτικό %r' %\
            (self.id, self.kodikos_real_eidikothtas, self.lektiko_real_eidikothtas)



class Klados(db.Model):
    __tablename__ = "klados"

    id = Column("klados_id", Integer, primary_key=True)
    kodikos_kladoy = Column("kodikos_kladoy", String, nullable=False, unique=True)
    lektiko_kladoy = Column("lektiko_kladoy", String, nullable=False)
    real_eidikothta_id = Column(Integer, ForeignKey('real_eidikothta.real_eidikothta_id'))

    # relationships
    #pinakes = relationship("Pinakas", back_populates="klados")

    def __repr__(self):
        return '\nΚλάδος id %r\nκωδικός %r\nλεκτικό %r\nreal %r' %\
            (self.id, self.kodikos_kladoy, self.lektiko_kladoy, self.real_eidikothta_id)



class Sxoliko_etos(db.Model):
    __tablename__ = "sxoliko_etos"

    id = Column("sxoliko_etos_id", Integer, primary_key=True)
    lektiko_sxolikoy_etoys = Column("lektiko_sxolikoy_etoys", String, nullable=False, unique=True)

    # relationships
    pinakes = relationship("Pinakas", back_populates="sxoliko_etos")

    def __repr__(self):
        return '\nΣχολικό έτος\nid %r\nλεκτικό %r' %\
            (self.id, self.lektiko_sxolikoy_etoys)



class Hmeromhnia(db.Model):
    __tablename__ = "hmeromhnia"

    id = Column("hmeromhnia_id", Integer, primary_key=True)
    lektiko_hmeromhnias = Column("lektiko_hmeromhnias", String, nullable=False, unique=True)
    real_hmeromhnia = Column("real_hmeromhnia", Date, nullable=False, unique=True)

    # relationships
    #pinakes = relationship("Pinakas", back_populates="hmeromhnia")

    def __repr__(self):
        return '\nΗμερομηνία id %r\nλεκτικό %r\nπρ. ημ/νία %r' %\
            (self.id, self.lektiko_hmeromhnias, self.real_hmeromhnia)



class Smeae_pinakas(db.Model):
    __tablename__ = "smeae_pinakas"

    id = Column("id", Integer, primary_key=True)
    lektiko = Column("lektiko", String, nullable=False, unique=True)

    def __repr__(self):
        return '\nΣΜΕΑΕ Πίνακας\nid %r\nλεκτικό %r' %\
            (self.id, self.lektiko)



class Smeae_kathgoria(db.Model):
    __tablename__ = "smeae_kathgoria"

    id = Column("id", Integer, primary_key=True)
    lektiko = Column("lektiko", String, nullable=False, unique=True)

    def __repr__(self):
        return '\nΣΜΕΑΕ Κατηγορία\nid %r\nλεκτικό %r' %\
            (self.id, self.lektiko)



class Smeae_kathgoria_greeklish(db.Model):
    __tablename__ = "smeae_kathgoria_greeklish"

    id = Column("id", Integer, primary_key=True)
    lektiko = Column("lektiko", String, nullable=False, unique=True)
    smeae_kathgoria_id = Column(Integer, ForeignKey('smeae_kathgoria.id'))

    def __repr__(self):
        return '\nΣΜΕΑΕ Κατηγορία grklsh\nid %r\nλεκτικό %r\nΣΜΕΑΕ κατηγορία id' %\
            (self.id, self.lektiko, self.smeae_kathgoria_id)



class Perioxh(db.Model):
    __tablename__ = "perioxh"

    id = Column("id", Integer, primary_key=True)
    lektiko = Column("lektiko", String, nullable=False, unique=True)

    def __repr__(self):
        return '\nΣΜΕΑΕ Περιοχή\nid %r\nλεκτικό %r' %\
            (self.id, self.lektiko)



class Perioxh_greeklish(db.Model):
    __tablename__ = "perioxh_greeklish"

    id = Column("id", Integer, primary_key=True)
    lektiko = Column("lektiko", String, nullable=False, unique=True)
    perioxh_id = Column(Integer, ForeignKey('perioxh.id'))

    def __repr__(self):
        return '\nΠεριοχή grklsh\nid %r\nλεκτικό %r\nΠεριοχή id' %\
            (self.id, self.lektiko, self.perioxh_id)



class Mousiko_organo(db.Model):
    __tablename__ = "mousiko_organo"

    id = Column("id", Integer, primary_key=True)
    lektiko = Column("lektiko", String, nullable=False, unique=True)

    def __repr__(self):
        return '\nΜουσικό όργανο\nid %r\nλεκτικό %r' %\
            (self.id, self.lektiko)



class Mousiko_organo_greeklish(db.Model):
    __tablename__ = "mousiko_organo_greeklish"

    id = Column("id", Integer, primary_key=True)
    lektiko = Column("lektiko", String, nullable=False, unique=True)
    mousiko_organo_id = Column(Integer, ForeignKey('mousiko_organo.id'))

    def __repr__(self):
        return '\Μουσικό όργανο grklsh\nid %r\nλεκτικό %r\nΜουσικό όργανο id' %\
            (self.id, self.lektiko, self.mousiko_organo_id)



class Athlima(db.Model):
    __tablename__ = "athlima"

    id = Column("id", Integer, primary_key=True)
    lektiko = Column("lektiko", String, nullable=False, unique=True)

    def __repr__(self):
        return '\nΆθλημα\nid %r\nλεκτικό %r' %\
            (self.id, self.lektiko)



class Athlima_greeklish(db.Model):
    __tablename__ = "athlima_greeklish"

    id = Column("id", Integer, primary_key=True)
    lektiko = Column("lektiko", String, nullable=False, unique=True)
    athlima_id = Column(Integer, ForeignKey('athlima.id'))

    def __repr__(self):
        return '\nΆθλημα grklsh\nid %r\nλεκτικό %r\Άθλημα id' %\
            (self.id, self.lektiko, self.athlima_id)



class Pinakas(db.Model):
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

    size = Column("size", Integer, nullable=False, default=0)

    sxoliko_etos = relationship("Sxoliko_etos", back_populates="pinakes")
    kathgoria = relationship("Kathgoria", back_populates="pinakes")
    #hmeromhnia = relationship("Hmeromhnia", back_populates="pinakes")
    #klados = relationship("Klados", back_populates="pinakes")


    def __repr__(self):
        return '\nΠίνακας id %r\nλεκτικό %r\nσχ.έτος %r\nκατηγορία %r\nκλάδος %r\nημ/νια %r\npath %r\nurl %r' %\
            (self.id, self.lektiko_pinaka, self.sxoliko_etos_id, self.kathgoria_id, \
             self.klados_id, self.hmeromhnia_id, self.path_pinaka, self.url_pinaka)







