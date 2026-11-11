# consulta_or.py
# Uso de or_(): historias clínicas cuyo diagnóstico contiene "Otitis"
# O cuyo diagnóstico contiene "Gastroenteritis".
# Basta con que se cumpla UNA de las condiciones.

from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker

from crear_base_entidades import engine, HistoriaClinica

Session = sessionmaker(bind=engine)
session = Session()

# like("%texto%") busca el texto en cualquier parte de la cadena.
historias = (session.query(HistoriaClinica)
             .filter(or_(HistoriaClinica.diagnostico.like("%Otitis%"),
                         HistoriaClinica.diagnostico.like("%Gastroenteritis%")))
             .all())

print("Historias con diagnóstico de Otitis o Gastroenteritis")
print("-" * 60)
for h in historias:
    print(h)

session.close()
