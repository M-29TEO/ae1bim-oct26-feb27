
# Inserta datos de ejemplo en las entidades de la base de datos.

from datetime import date

from sqlalchemy.orm import sessionmaker

# Se reutilizan el engine y las clases definidas en crear_base_entidades.py
from crear_base_entidades import engine, Clinica, Consultorio, Veterinario, HistoriaClinica

# La sesión es la "conversación" con la base: acumula cambios
# y los envía todos juntos al hacer commit().
Session = sessionmaker(bind=engine)
session = Session()

# Evita duplicar datos si el script se ejecuta más de una vez.
if session.query(Clinica).count() > 0:
    print("La base ya tiene datos. Borre clinicas_veterinarias.db y vuelva a crearla si desea repoblar.")
    session.close()
    raise SystemExit

#  Clínicas 
c1 = Clinica(nombre="VetSalud Loja", direccion="Av. Universitaria y 10 de Agosto, Loja",
veterinario_responsable="Dra. Paola Jaramillo")
c2 = Clinica(nombre="Huellitas Quito", direccion="Av. Amazonas N24-56, Quito",
veterinario_responsable="Dr. Andrés Villacís")
c3 = Clinica(nombre="PetCare Cuenca", direccion="Calle Larga 8-45, Cuenca",
veterinario_responsable="Dra. María Ordóñez")

# Consultorios 
# Al asignar clinica=c1, SQLAlchemy completa clinica_id automáticamente.
co1 = Consultorio(nombre="Consultorio 101", especialidad="Medicina general", clinica=c1)
co2 = Consultorio(nombre="Consultorio 102", especialidad="Cirugía", clinica=c1)
co3 = Consultorio(nombre="Consultorio A", especialidad="Dermatología", clinica=c2)
co4 = Consultorio(nombre="Consultorio B", especialidad="Medicina general", clinica=c2)
co5 = Consultorio(nombre="Sala 1", especialidad="Cirugía", clinica=c3)
co6 = Consultorio(nombre="Sala 2", especialidad="Odontología", clinica=c3)

# Veterinarios 
v1 = Veterinario(nombres="Luis", apellidos="Torres Cueva", correo="ltorres@vetsalud.ec",
licencia="LIC-1001", consultorio=co1)
v2 = Veterinario(nombres="Ana", apellidos="Paredes Ruiz", correo="aparedes@vetsalud.ec",
licencia="LIC-1002", consultorio=co2)
v3 = Veterinario(nombres="Carlos", apellidos="Mena Salazar", correo="cmena@huellitas.ec",
licencia="LIC-2001", consultorio=co3)
v4 = Veterinario(nombres="Sofía", apellidos="Andrade León", correo="sandrade@huellitas.ec",
licencia="LIC-2002", consultorio=co4)
v5 = Veterinario(nombres="Diego", apellidos="Vintimilla Paz", correo="dvintimilla@petcare.ec",
licencia="LIC-3001", consultorio=co5)
v6 = Veterinario(nombres="Gabriela", apellidos="Cordero Mora", correo="gcordero@petcare.ec",
licencia="LIC-3002", consultorio=co6)
v7 = Veterinario(nombres="Jorge", apellidos="Ríos Castro", correo="jrios@vetsalud.ec",
 licencia="LIC-1003", consultorio=co1)

# Historias clínicas 
historias = [
    HistoriaClinica(fecha_atencion=date(2026, 9, 2), diagnostico="Gastroenteritis",
     tratamiento="Dieta blanda y metronidazol 7 días", nombre_mascota="Max", veterinario=v1),
    HistoriaClinica(fecha_atencion=date(2026, 9, 10), diagnostico="Otitis externa",
     tratamiento="Limpieza auricular y gotas óticas", nombre_mascota="Luna", veterinario=v1),
    HistoriaClinica(fecha_atencion=date(2026, 9, 15), diagnostico="Fractura de radio",
     tratamiento="Osteosíntesis con placa", nombre_mascota="Rocky", veterinario=v2),
    HistoriaClinica(fecha_atencion=date(2026, 10, 1), diagnostico="Esterilización programada",
     tratamiento="Ovariohisterectomía y analgésicos", nombre_mascota="Mía", veterinario=v2),
    HistoriaClinica(fecha_atencion=date(2026, 10, 3), diagnostico="Vacunación anual",
     tratamiento="Vacuna séxtuple y desparasitación", nombre_mascota="Toby", veterinario=v7),
    HistoriaClinica(fecha_atencion=date(2026, 9, 20), diagnostico="Dermatitis alérgica",
     tratamiento="Antihistamínico y champú medicado", nombre_mascota="Nala", veterinario=v3),
    HistoriaClinica(fecha_atencion=date(2026, 10, 12), diagnostico="Sarna sarcóptica",
     tratamiento="Ivermectina y baños medicados", nombre_mascota="Coco", veterinario=v3),
    HistoriaClinica(fecha_atencion=date(2026, 10, 18), diagnostico="Otitis media",
     tratamiento="Antibiótico oral 10 días", nombre_mascota="Bruno", veterinario=v4),
    HistoriaClinica(fecha_atencion=date(2026, 9, 25), diagnostico="Cuerpo extraño gástrico",
     tratamiento="Gastrotomía y fluidoterapia", nombre_mascota="Simba", veterinario=v5),
    HistoriaClinica(fecha_atencion=date(2026, 10, 22), diagnostico="Enfermedad periodontal",
     tratamiento="Profilaxis dental y antibiótico", nombre_mascota="Kira", veterinario=v6),
    HistoriaClinica(fecha_atencion=date(2026, 11, 2), diagnostico="Gastroenteritis",
     tratamiento="Suero oral y probióticos", nombre_mascota="Lola", veterinario=v4),
]

# add_all agrega todos los objetos a la sesión. Basta con agregar las
# clínicas e historias: por las relaciones (cascade por defecto
# "save-update"), SQLAlchemy también guarda consultorios y veterinarios.
session.add_all([c1, c2, c3])
session.add_all(historias)

# commit() ejecuta los INSERT y confirma la transacción
session.commit()
print("Datos insertados correctamente.")
session.close()
