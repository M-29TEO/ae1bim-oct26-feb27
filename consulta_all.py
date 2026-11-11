# consulta_all.py
# Uso de all(): presentar las Clínicas y, por cada una, el número
# de Historias Clínicas asociadas.
#
# Una historia no se relaciona directamente con la clínica, sino por el camino:
#   Clinica -> Consultorio -> Veterinario -> HistoriaClinica

from sqlalchemy.orm import sessionmaker

from crear_base_entidades import engine, Clinica

Session = sessionmaker(bind=engine)
session = Session()

# all() ejecuta la consulta y devuelve una LISTA con todos los registros.
clinicas = session.query(Clinica).all()

print("Clínicas y número de historias clínicas asociadas")
print("-" * 60)
for clinica in clinicas:
    # Se recorren las relaciones definidas con relationship()
    # sumando las historias de cada veterinario de cada consultorio.
    total_historias = 0
    for consultorio in clinica.consultorios:
        for veterinario in consultorio.veterinarios:
            total_historias += len(veterinario.historias)

    print(clinica)
    print(f"   Número de historias clínicas: {total_historias}")

session.close()
