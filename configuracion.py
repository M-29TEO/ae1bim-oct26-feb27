# configuracion.py
# Información de conexión a la base de datos.
# Se centraliza aquí para que todos los scripts usen la misma base.
#
# Formato de la cadena de conexión de SQLAlchemy para SQLite:
#   sqlite:///<ruta_del_archivo>
# Con tres barras la ruta es relativa a la carpeta donde se ejecuta el script.

cadena_base_datos = "sqlite:///clinicas_veterinarias.db"
