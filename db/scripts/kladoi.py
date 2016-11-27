
import pandas as pd
from os import listdir
from os.path import isfile, isdir, join

import sqlalchemy
import pandas

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from db_init_eidikothtes_dev import Base, Klados, Real_eidikothta

engine = create_engine('sqlite:///talaiporosanaplirotis_eidikothtes_dev.sqlite')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

path = '../data/2016-2017/eniaios_smea_anap_16/'
#path = 'test/'
directories = sorted([d for d in listdir(path) if isdir(join(path,d))])

for dir in directories:
    filepath = join(path,dir) + '/'
    print(filepath)

    files = sorted([(filepath + f) for f in listdir(filepath) if isfile(join(filepath, f))])

    for f in files:
        kodikoi_kladwn = []
        kladoi = []
        print(f)

        try:
            df = pd.read_excel(f, header=0)
            for row in df.iterrows():
                #count = row[1]['Α/Α']
                kodikos_kladoy = row[1]['ΚΛΑΔΟΣ']
                try:
                    # klados already in DB
                    session.query(Klados).filter(Klados.kodikos_kladoy == kodikos_kladoy).one()
                    #print('klados', kodikos_kladoy, 'already there')
                except sqlalchemy.orm.exc.NoResultFound:
                    # klados not in DB
                    if kodikos_kladoy not in kodikoi_kladwn:
                        # new klados found in file
                        kodikoi_kladwn.append(kodikos_kladoy)

                        if kodikos_kladoy.endswith('.50'):
                            # ΣΜΕΑ
                            try:
                                lektiko_kladoy = session.query(Klados).filter(Klados.kodikos_kladoy
                                                                          == kodikos_kladoy[:-3]).one().lektiko_kladoy + ' ΕΑΕ'
                            except Exception:
                                print('SMEA', kodikos_kladoy, 'not found')
                                lektiko_kladoy = kodikos_kladoy

                            try:
                                kodikos_real_eidikothtas = row[1]['ΟΜΑΔΟΠΟΙΗΜΕΝΗ ΕΙΔΙΚΟΤΗΤΑ']
                            except KeyError as e:
                                print(e, 'column not found')
                        else:
                            # Ενιαίος πίνακας
                            try:
                                lektiko_kladoy = row[1]['ΛΕΚΤΙΚΟ ΚΛΑΔΟΥ']
                            except KeyError as e:
                                print(e, 'column not found')
                                lektiko_kladoy = kodikos_kladoy

                            try:
                                kodikos_real_eidikothtas = row[1]['ΕΙΔΙΚΟΤΗΤΑ']
                            except KeyError as e:
                                print(e, 'column not found')

                        try:
                            real_eidikothta_id = session.query(Real_eidikothta).filter(Real_eidikothta.kodikos_real_eidikothtas
                                                                                == kodikos_real_eidikothtas).one().id
                        except Exception:
                            print('real eidikothta not found, setting to 0')
                            real_eidikothta_id = 0


                        new_klados = Klados(kodikos_kladoy = kodikos_kladoy,
                                            lektiko_kladoy = lektiko_kladoy,
                                            real_eidikothta_id = real_eidikothta_id)

                        kladoi.append(new_klados)

            for klados in kladoi:
                print(filepath, klados.kodikos_kladoy, klados.lektiko_kladoy, klados.real_eidikothta_id)
                session.add(klados)

            session.commit()

        except Exception as e:
            print(e)



