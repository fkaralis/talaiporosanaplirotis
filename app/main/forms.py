from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SelectField
from wtforms import SelectMultipleField
from wtforms import SubmitField
from wtforms.validators import Required
from wtforms.validators import DataRequired
from .. import db
from ..models import User, Kathgoria, Real_eidikothta, Klados, Sxoliko_etos, Hmeromhnia,\
Pinakas, Smeae_pinakas, Smeae_kathgoria, Perioxh, Mousiko_organo, Athlima,\
Smeae_kathgoria_greeklish, Perioxh_greeklish, Mousiko_organo_greeklish, Athlima_greeklish

# main page form
#
## gather choices
choices_sxolika_eth = []
choices_kathgories = []
choices_kladoi = []
choices_hmeromhnies = []
choices_smeae_pinakes = []
choices_smeae_kathgories = []
choices_perioxes = []
choices_mousika_organa = []
choices_athlimata = []

sxolika_eth = Sxoliko_etos.query.all()
kathgories = Kathgoria.query.all()
kladoi = Klados.query.all()
hmeromhnies = Hmeromhnia.query.all()
smeae_pinakes = Smeae_pinakas.query.all()
smeae_kathgories = Smeae_kathgoria.query.all()
perioxes = Perioxh.query.all()
mousika_organa = Mousiko_organo.query.all()
athlimata = Athlima.query.all()

for sxoliko_etos in sxolika_eth:
    choice = (sxoliko_etos.id, sxoliko_etos.lektiko_sxolikoy_etoys)
    choices_sxolika_eth.append(choice)
choices_sxolika_eth = sorted(choices_sxolika_eth)[:5] # up to 2012-13
choices_sxolika_eth.insert(0, (0, '--Επιλογή σχ. έτους--'))

for kathgoria in kathgories:
    choice = (kathgoria.id, kathgoria.greek_lektiko_kathgorias)
    choices_kathgories.append(choice)
choices_kathgories = sorted(choices_kathgories, key=lambda x: x[1]) # sort alphabetically
choices_kathgories.insert(0, (0, '--Επιλογή κατηγορίας--'))

for klados in kladoi:
    choice = (klados.id, klados.kodikos_kladoy+' '+klados.lektiko_kladoy)
    choices_kladoi.append(choice)
choices_kladoi = sorted(choices_kladoi, key=lambda x: x[1]) # sort alphabetically
choices_kladoi.insert(0, (0, '--Επιλογή κλάδου--'))

for hmeromhnia in hmeromhnies:
    choice = (hmeromhnia.id, hmeromhnia.real_hmeromhnia)
    choices_hmeromhnies.append(choice)
choices_hmeromhnies = sorted(choices_hmeromhnies, key=lambda x: x[1], reverse=True)  # sort alphabetically decr.

# fix hmeromhnia format (e.g. 10-Οκτ-2016)
for i, choice in enumerate(choices_hmeromhnies):
    choice_list = list(choices_hmeromhnies[i])
    choice_list[1] = '{:%d-%b-%Y}'.format(choice_list[1])
    choices_hmeromhnies[i] = tuple(choice_list)
choices_hmeromhnies.insert(0, (0, '--Επιλογή ημ/νίας--'))

for smeae_pinakas in smeae_pinakes:
    choice = (smeae_pinakas.id, smeae_pinakas.lektiko)
    choices_smeae_pinakes.append(choice)
choices_smeae_pinakes = sorted(choices_smeae_pinakes, key=lambda x: x[1]) # sort alphabetically
choices_smeae_pinakes.insert(0, (0, '--Επιλογή πίνακα ΣΜΕΑΕ--'))

for smeae_kathgoria in smeae_kathgories:
    choice = (smeae_kathgoria.id, smeae_kathgoria.lektiko)
    choices_smeae_kathgories.append(choice)
choices_smeae_kathgories.insert(0, (0, '--Επιλογή κατηγορίας ΣΜΕΑΕ--'))

for perioxh in perioxes:
    choice = (perioxh.id, perioxh.lektiko)
    choices_perioxes.append(choice)
choices_perioxes = sorted(choices_perioxes, key=lambda x: x[1]) # sort alphabetically
choices_perioxes.insert(0, (0, '--Επιλογή περιοχής--'))

for mousiko_organo in mousika_organa:
    choice = (mousiko_organo.id, mousiko_organo.lektiko)
    choices_mousika_organa.append(choice)
choices_mousika_organa = sorted(choices_mousika_organa, key=lambda x: x[1]) # sort alphabetically
choices_mousika_organa.insert(0, (0, '--Επιλογή μουσικού οργάνου--'))

for athlima in athlimata:
    choice = (athlima.id, athlima.lektiko)
    choices_athlimata.append(choice)
choices_athlimata = sorted(choices_athlimata, key=lambda x: x[1]) # sort alphabetically
choices_athlimata.insert(0, (0, '--Επιλογή αθλήματος--'))
## end choices


class MainForm(FlaskForm):
    sxoliko_etos = SelectField('Σχολικό έτος',\
                               choices=choices_sxolika_eth,\
                               validators=[DataRequired()],\
                               coerce=int,\
                               id='select_sxoliko_etos')
    kathgoria = SelectField('Κατηγορία',\
                            choices=choices_kathgories,\
                            validators=[DataRequired()],\
                            coerce=int,\
                            id='select_kathgoria')
    klados = SelectField('Κλάδος',\
                         choices=choices_kladoi,\
                         validators=[DataRequired()],\
                         coerce=int, id='select_klados')
    smeae_pinakas = SelectField('Πίνακας ΣΜΕΑΕ',\
                                choices=choices_smeae_pinakes,\
                                coerce=int,\
                                id='select_smeae_pinakas')
    smeae_kathgoria = SelectField('Κατηγορία για ΣΜΕΑΕ',\
                        choices=choices_smeae_kathgories,\
                        coerce=int,\
                        id='select_smeae_kathgoria')
    perioxh = SelectField('Περιοχή',\
                             choices=choices_perioxes,\
                             coerce=int,\
                             id='select_perioxh')
    mousiko_organo = SelectField('Mουσικό όργανο',\
                             choices=choices_mousika_organa,\
                             coerce=int,\
                             id='select_mousiko_organo')
    athlima = SelectField('Άθλημα',\
                             choices=choices_athlimata,\
                             coerce=int,\
                             id='select_athlima')
    hmeromhnia = SelectField('Ημερομηνία',\
                             choices=choices_hmeromhnies,\
                             coerce=int,\
                             id='select_hmeromhnia')
    submit = SubmitField('Yποβολή')
#
# MainForm end
