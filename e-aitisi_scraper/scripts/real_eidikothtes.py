#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
'''
fill Real_eidikothtes table
'''

import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from db_init_eidikothtes_dev import Base, Real_eidikothta, Klados

engine = create_engine('sqlite:///talaiporosanaplirotis_eidikothtes_dev.sqlite')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


real_eidikothtes = []
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ60',
                                        lektiko_real_eidikothtas = 'ΝΗΠΙΑΓΩΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ70',
                                        lektiko_real_eidikothtas = 'ΔΑΣΚΑΛΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ01.00',
                                        lektiko_real_eidikothtas = 'ΘΕΟΛΟΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ02.00',
                                        lektiko_real_eidikothtas = 'ΦΙΛΟΛΟΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ03.00',
                                        lektiko_real_eidikothtas = 'ΜΑΘΗΜΑΤΙΚΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ04.01',
                                        lektiko_real_eidikothtas = 'ΦΥΣΙΚΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ04.02',
                                        lektiko_real_eidikothtas = 'ΧΗΜΙΚΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ04.04',
                                        lektiko_real_eidikothtas = 'ΒΙΟΛΟΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ04.05',
                                        lektiko_real_eidikothtas = 'ΓΕΩΛΟΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ05.00',
                                        lektiko_real_eidikothtas = 'ΓΑΛΛΙΚΗΣ ΦΙΛΟΛΟΓΙΑΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ06.00',
                                        lektiko_real_eidikothtas = 'ΑΓΓΛΙΚΗΣ ΦΙΛΟΛΟΓΙΑΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ07.00',
                                        lektiko_real_eidikothtas = 'ΓΕΡΜΑΝΙΚΗΣ ΦΙΛΟΛΟΓΙΑΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ08.00',
                                        lektiko_real_eidikothtas = 'ΚΑΛΩΝ ΤΕΧΝΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ09.00',
                                        lektiko_real_eidikothtas = 'ΟΙΚΟΝΟΜΟΛΟΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ10.00',
                                        lektiko_real_eidikothtas = 'ΚΟΙΝΩΝΙΟΛΟΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ11.00',
                                        lektiko_real_eidikothtas = 'ΦΥΣΙΚΗΣ ΑΓΩΓΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ12.01',
                                        lektiko_real_eidikothtas = 'ΠΟΛΙΤΙΚΟΙ ΜΗΧΑΝΙΚΟΙ-ΑΡΧΙΤΕΚΤΟΝΕΣ-ΤΟΠΟΓΡΑΦΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ12.04',
                                        lektiko_real_eidikothtas = 'ΜΗΧΑΝΟΛΟΓΟΙ-ΜΗΧΑΝΙΚΟΙ ΠΑΡΑΓΩΓΗΣ ΚΑΙ ΔΙΟΙΚΗΣΗΣ-ΝΑΥΠΗΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ12.05',
                                        lektiko_real_eidikothtas = 'ΗΛΕΚΤΡΟΛΟΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ12.06',
                                        lektiko_real_eidikothtas = 'ΗΛΕΚΤΡΟΛΟΓΟΙ ΜΗΧΑΝΙΚΟΙ-ΦΥΣΙΚΟΙ ΡΑΔΙΟΗΛΕΚΤΡΟΛΟΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ12.08',
                                        lektiko_real_eidikothtas = 'ΧΗΜΙΚΟΙ ΜΗΧΑΝΙΚΟΙ-ΜΕΤΑΛΛΕΙΟΛΟΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ12.13',
                                        lektiko_real_eidikothtas = 'ΠΕΡΙΒΑΛΛΟΝΤΟΛΟΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ13.00',
                                        lektiko_real_eidikothtas = 'ΝΟΜΙΚΗΣ-ΠΟΛΙΤΙΚΩΝ ΕΠΙΣΤΗΜΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ14.01',
                                        lektiko_real_eidikothtas = 'ΙΑΤΡΟΙ-ΟΔΟΝΤΙΑΤΡΟΙ-ΦΑΡΜΑΚΟΠΟΙΟΙ-ΝΟΣΗΛΕΥΤΕΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ14.04',
                                        lektiko_real_eidikothtas = 'ΓΕΩΠΟΝΟΙ-ΔΑΣΟΛΟΓΙΑΣ ΚΑΙ ΦΥΣ.ΠΕΡ/ΝΤΟΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ15.00',
                                        lektiko_real_eidikothtas = 'ΟΙΚΙΑΚΗΣ ΟΙΚΟΝΟΜΙΑΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ16.01',
                                        lektiko_real_eidikothtas = 'ΜΟΥΣΙΚΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ16.00',
                                        lektiko_real_eidikothtas = 'ΜΟΥΣΙΚΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ17.01',
                                        lektiko_real_eidikothtas = 'ΠΟΛΙΤΙΚΟΙ-ΤΟΠΟΓΡΑΦΟΙ ΑΣΕΤΕΜ-ΤΕΙ-ΚΑΤΕΕ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ17.02',
                                        lektiko_real_eidikothtas = 'ΜΗΧΑΝΟΛΟΓΟΙ-ΝΑΥΠ.ΕΜΠ.Ν. ΑΣΕΤΕΜ-ΤΕΙ-ΚΑΤΕΕ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ17.03',
                                        lektiko_real_eidikothtas = 'ΗΛΕΚΤΡΟΛΟΓΟΙ ΑΣΕΤΕΜ-ΤΕΙ-ΚΑΤΕΕ-ΤΕΧΝΟΛΟΓΟΙ ΕΝΕΡΓΕΙΑΚΗΣ ΤΕΧΝΙΚΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ17.04',
                                        lektiko_real_eidikothtas = 'ΗΛΕΚΤΡΟΝΙΚΟΙ ΑΣΕΤΕΜ-ΤΕΙ-ΚΑΤΕΕ-ΤΕΧΝΟΛΟΓΟΙ ΙΑΤΡΙΚΩΝ ΟΡΓΑΝΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ17.09',
                                        lektiko_real_eidikothtas = 'ΤΕΧΝΙΚΟΙ ΙΑΤΡΙΚΩΝ ΟΡΓΑΝΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ17.12',
                                        lektiko_real_eidikothtas = 'ΤΕΧΝΟΛΟΓΟΙ ΠΕΤΡΕΛΑΙΟΥ ΚΑΙ ΦΥΣΙΚΟΥ ΑΕΡΙΟΥ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.01',
                                        lektiko_real_eidikothtas = 'ΓΡΑΦΙΚΩΝ ΤΕΧΝΩΝ-ΓΡΑΦΙΣΤΙΚΗΣ-ΔΙΑΚΟΣΜΗΤΙΚΗΣ-ΣΥΝΤΗΡΗΤΕΣ ΕΡΓ. ΤΕΧΝΗΣ ΚΑΙ ΑΡΧ. ΕΥΡΗΜΑΤΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.02',
                                        lektiko_real_eidikothtas = 'ΔΙΟΙΚΗΣΗΣ ΕΠΙΧΕΙΡΗΣΕΩΝ-ΛΟΓΙΣΤΙΚΗΣ-ΤΟΥΡΙΣΤΙΚΩΝ ΕΠΙΧΕΙΡΗΣΕΩΝ-ΕΜΠΟΡΙΑΣ ΚΑΙ ΔΙΑΦΗΜΙΣΗΣ (MARKETING)'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.04',
                                        lektiko_real_eidikothtas = 'ΑΙΣΘΗΤΙΚΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.07',
                                        lektiko_real_eidikothtas = 'ΙΑΤΡΙΚΩΝ ΕΡΓΑΣΤΗΡΙΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.08',
                                        lektiko_real_eidikothtas = 'ΟΔΟΝΤΟΤΕΧΝΙΚΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.09',
                                        lektiko_real_eidikothtas = 'ΚΟΙΝΩΝΙΚΗΣ ΕΡΓΑΣΙΑΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.10',
                                        lektiko_real_eidikothtas = 'ΝΟΣΗΛΕΥΤΙΚΗΣ-ΜΑΙΕΥΤΙΚΗΣ-ΕΠΙΣΚΕΠΤΕΣ ΥΓΕΙΑΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.12',
                                        lektiko_real_eidikothtas = 'ΦΥΤΙΚΗΣ ΠΑΡΑΓΩΓΗΣ-ΖΩΙΚΗΣ ΠΑΡΑΓΩΓΗΣ-ΙΧΘΥΟΚΟΜΙΑΣ-ΑΛΙΕΙΑΣ-ΓΕΩΡΓ.ΜΗΧΑΝΩΝ ΚΑΙ ΑΡΔΕΥΣΕΩΝ-ΔΑΣΟΠΟΝΙΑΣ-ΔΙΟΙΚΗΣΗΣ ΓΕΩΡΓ. ΕΚΜΕΤΑΛ-ΘΕΡΜΟΚΗΠ. ΚΑΛΛΙΕΡΓΕΙΩΝ ΚΑΙ ΑΝΘ/ΜΙΑΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.18',
                                        lektiko_real_eidikothtas = 'ΟΧΗΜΑΤΩΝ ΤΕΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.20',
                                        lektiko_real_eidikothtas = 'ΚΛΩΣΤΟΫΦΑΝΤΟΥΡΓΙΑΣ-ΣΧΕΔΙΑΣΜΟΥ ΚΑΙ ΠΑΡΑΓΩΓΗΣ ΕΝΔΥΜΑΤΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.21',
                                        lektiko_real_eidikothtas = 'ΡΑΔΙΟΛΟΓΙΑΣ-ΑΚΤΙΝΟΛΟΓΙΑΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.22',
                                        lektiko_real_eidikothtas = 'ΜΕΤΑΛΛΕΙΟΛΟΓΟΙ-ΤΕΧΝΟΛΟΓΟΙ ΟΡΥΧΕΙΩΝ-ΤΕΧΝΟΛΟΓΟΙ ΓΕΩΤΕΧΝΟΛΟΓΙΑΣ ΚΑΙ ΠΕΡΙΒΑΛΛΟΝΤΟΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.23',
                                        lektiko_real_eidikothtas = 'ΝΑΥΤ.ΜΑΘ.(ΠΛΟΙΑΡΧΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.24',
                                        lektiko_real_eidikothtas = 'ΕΡΓΑΣΙΟΘΕΡΑΠ.-ΦΥΣΙΟΘΕΡΑΠ.'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.29',
                                        lektiko_real_eidikothtas = 'ΦΩΤΟΓΡΑΦΙΑΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.31',
                                        lektiko_real_eidikothtas = 'ΜΗΧΑΝ.ΕΜΠΟΡ.ΝΑΥΤΙΚΟΥ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.32',
                                        lektiko_real_eidikothtas = 'ΜΗΧΑΝΟΣΥΝΘ.ΑΕΡΟΣΚΑΦΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.33',
                                        lektiko_real_eidikothtas = 'ΒΡΕΦΟΝΗΠΙΟΚΟΜΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.36',
                                        lektiko_real_eidikothtas = 'ΤΕΧΝΟΛΟΓΙΑΣ ΤΡΟΦΙΜΩΝ-ΔΙΑΤΡΟΦΗΣ-ΟΙΝΟΛΟΓΙΑΣ ΚΑΙ ΤΕΧΝ. ΠΟΤΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.37',
                                        lektiko_real_eidikothtas = 'ΔΗΜΟΣΙΑΣ ΥΓΙΕΙΝΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.38',
                                        lektiko_real_eidikothtas = 'ΚΕΡΑΜΙΚΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.41',
                                        lektiko_real_eidikothtas = 'ΔΡΑΜΑΤΙΚΗΣ ΤΕΧΝΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ18.44',
                                        lektiko_real_eidikothtas = 'ΣΧΕΔΙΑΣΜΟΥ ΚΑΙ ΤΕΧΝΟΛΟΓΙΑΣ ΞΥΛΟΥ ΚΑΙ ΕΠΙΠΛΟΥ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ19.00',
                                        lektiko_real_eidikothtas = 'ΠΛΗΡΟΦΟΡΙΚΗΣ ΑΕΙ-ΤΕΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ32.00',
                                        lektiko_real_eidikothtas = 'ΘΕΑΤΡΙΚΩΝ ΣΠΟΥΔΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ33.00',
                                        lektiko_real_eidikothtas = 'ΜΕΘΟΔΟΛΟΓΙΑΣ ΙΣΤΟΡΙΑΣ ΚΑΙ ΘΕΩΡΙΑΣ ΤΗΣ ΕΠΙΣΤΗΜΗΣ (ΜΙΘΕ)'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ34.00',
                                        lektiko_real_eidikothtas = 'ΙΤΑΛΙΚΗΣ ΦΙΛΟΛΟΓΙΑΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΠΕ40.00',
                                        lektiko_real_eidikothtas = 'ΙΣΠΑΝΙΚΗΣ ΦΙΛΟΛΟΓΙΑΣ'))

real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.01',
                                        lektiko_real_eidikothtas = 'ΣΧΕΔΙΑΣΤΕΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.02',
                                        lektiko_real_eidikothtas = 'ΜΗΧΑΝΟΛΟΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.03',
                                        lektiko_real_eidikothtas = 'ΜΗΧΑΝ. ΑΥΤΟΚΙΝΗΤΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.04',
                                        lektiko_real_eidikothtas = 'ΨΥΚΤΙΚΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.05',
                                        lektiko_real_eidikothtas = 'ΔΟΜΙΚΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.06',
                                        lektiko_real_eidikothtas = 'ΗΛΕΚΤΡΟΛΟΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.07',
                                        lektiko_real_eidikothtas = 'ΗΛΕΚΤΡΟΝΙΚΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.08',
                                        lektiko_real_eidikothtas = 'ΧΗΜΙΚΟΙ ΕΡΓΑΣΤΗΡΙΩΝ-ΜΕΤΑΛΛΕΙΟΛΟΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.10',
                                        lektiko_real_eidikothtas = 'ΥΠΑΛΛΗΛΟΙ ΓΡΑΦΕΙΟΥ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.11',
                                        lektiko_real_eidikothtas = 'ΥΠΑΛΛΗΛΟΙ ΛΟΓΙΣΤΗΡΙΟΥ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.12',
                                        lektiko_real_eidikothtas = 'ΔΙΑΚΟΣΜΗΤΙΚΗΣ-ΓΡΑΦΙΚΩΝ ΤΕΧΝΩΝ-ΨΗΦΙΔΟΓΡΑΦΟΙ-ΥΑΛΟΓΡΑΦΟΙ-ΣΥΝΤΗΡΗΤΕΣ ΕΡΓΩΝ ΤΕΧΝΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.13',
                                        lektiko_real_eidikothtas = 'ΠΡΟΓΡΑΜΜΑΤΙΣΤΕΣ Η/Υ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.15',
                                        lektiko_real_eidikothtas = 'ΨΗΦΙΔΟΓΡΑΦΟΙ-ΥΑΛΟΓΡΑΦΟΙ-ΣΥΝΤΗΡΗΤΕΣ ΕΡΓΩΝ ΤΕΧΝΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.19',
                                        lektiko_real_eidikothtas = 'ΚΟΜΜΩΤΙΚΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.20',
                                        lektiko_real_eidikothtas = 'ΑΙΣΘΗΤΙΚΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.23',
                                        lektiko_real_eidikothtas = 'ΜΕΤΑΛΛΕΙΟΛΟΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.25',
                                        lektiko_real_eidikothtas = 'ΑΡΓΥΡΟΧΡΥΣΟΧΟΪΑΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.26',
                                        lektiko_real_eidikothtas = 'ΟΔΟΝΤΟΤΕΧΝΙΚΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.28',
                                        lektiko_real_eidikothtas = 'ΜΗΧΑΝΟΣΥΝΘΕΤΕΣ ΑΕΡΟΣΚΑΦΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.29',
                                        lektiko_real_eidikothtas = 'ΒΟΗΘ.ΙΑΤΡ. ΚΑΙ ΒΙΟΛΟΓ. ΕΡΓΑΣΤΗΡΙΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.30',
                                        lektiko_real_eidikothtas = 'ΒΟΗΘΟΙ ΠΑΙΔΟΚΟΜΟΙ-ΒΡΕΦΟΚΟΜΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.32',
                                        lektiko_real_eidikothtas = 'ΑΝΘΟΚΟΜΙΑΣ ΚΑΙ ΚΗΠΟΤΕΧΝΙΑΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.33',
                                        lektiko_real_eidikothtas = 'ΦΥΤΙΚΗΣ ΠΑΡΑΓΩΓΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.34',
                                        lektiko_real_eidikothtas = 'ΖΩΙΚΗΣ ΠΑΡΑΓΩΓΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.36',
                                        lektiko_real_eidikothtas = 'ΑΓΡΟΤΙΚΩΝ ΣΥΝΕΤΑΙΡΙΣΜΩΝ ΚΑΙ ΕΚΜΕΤΑΛΛΕΥΣΕΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΤΕ01.37',
                                        lektiko_real_eidikothtas = 'ΚΟΠΤΙΚΗΣ-ΡΑΠΤΙΚΗΣ-ΚΛΩΣΤΟΫΦΑΝΤΟΥΡΓΙΑΣ'))

real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΔΕ01.01',
                                        lektiko_real_eidikothtas = 'ΗΛΕΚΤΡΟΤΕΧΝΙΤΕΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΔΕ01.02',
                                        lektiko_real_eidikothtas = 'ΜΗΧΑΝΟΤΕΧΝΙΤΕΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΔΕ01.04',
                                        lektiko_real_eidikothtas = 'ΗΛΕΚΤΡΟΝΙΚΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΔΕ01.10',
                                        lektiko_real_eidikothtas = 'ΤΕΧΝΙΤΕΣ ΑΥΤΟΚΙΝΗΤΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΔΕ01.11',
                                        lektiko_real_eidikothtas = 'ΤΕΧΝΙΤΕΣ ΨΥΞΕΩΣ (ΨΥΚΤΙΚΟΙ)'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΔΕ01.12',
                                        lektiko_real_eidikothtas = 'ΥΔΡΑΥΛΙΚΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΔΕ01.13',
                                        lektiko_real_eidikothtas = 'ΞΥΛΟΥΡΓΟΙ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΔΕ01.14',
                                        lektiko_real_eidikothtas = 'ΚΟΠΤΙΚΗΣ ΡΑΠΤΙΚΗΣ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΔΕ01.16',
                                        lektiko_real_eidikothtas = 'ΤΕΧΝ. ΑΜΑΞΩΜΑΤΩΝ'))
real_eidikothtes.append(Real_eidikothta(kodikos_real_eidikothtas = 'ΔΕ01.17',
                                        lektiko_real_eidikothtas = 'ΚΟΜΜΩΤΙΚΗΣ'))

for real_eidikothta in real_eidikothtes:
    session.add(real_eidikothta)

session.commit()