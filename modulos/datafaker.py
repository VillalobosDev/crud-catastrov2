import sqlite3
from faker import Faker
import random
from datetime import date

# Initialize Faker with Spanish locale
fake = Faker('es_ES')

# Connect to the SQLite database
conn = sqlite3.connect('db.db')
cursor = conn.cursor()

# Generate random data for the "contribuyentes" table
def generate_contribuyentes(num_records):
    for _ in range(num_records):
        nombre = fake.first_name()
        apellido = fake.last_name()
        ci_contribuyente = fake.random_int(min=10000000, max=30000000)  # Ensure ci_contribuyente is a maximum of 8 digits and not above 30,000,000
        rif = ci_contribuyente  # Ensure rif is the same as ci_contribuyente
        telefono = f"+58 {random.choice(['0412', '0424', '0416', '0414'])} {fake.random_int(min=1000000, max=9999999)}"
        correo = f"{nombre.lower()}.{apellido.lower()}{fake.random_int(min=1, max=999)}@gmail.com"
        v_e = random.choice(['V', 'E'])
        j_c_g = random.choice(['J', 'C', 'G'])
        cursor.execute('''
            INSERT INTO contribuyentes (nombres, apellidos, ci_contribuyente, rif, telefono, correo, v_e, j_c_g)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, apellido, ci_contribuyente, rif, telefono, correo, v_e, j_c_g))

# Generate random data for the "sectores" table
def generate_sectores(num_records):
    for _ in range(num_records):
        nom_sector = fake.city()
        cod_sector = fake.random_int(min=100, max=999)
        image_path = fake.file_path(extension='jpg')
        cursor.execute('''
            INSERT INTO sectores (nom_sector, cod_sector, image_path)
            VALUES (?, ?, ?)
        ''', (nom_sector, cod_sector, image_path))

# Generate random data for the "inmuebles" table
def generate_inmuebles(num_records):
    cursor.execute('SELECT id_contribuyente FROM contribuyentes')
    contribuyentes_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute('SELECT id_sector FROM sectores')
    sectores_ids = [row[0] for row in cursor.fetchall()]

    start_date = date(2023, 1, 1)
    end_date = date(2025, 12, 31)

    for _ in range(num_records):
        nom_inmueble = fake.company()
        ubicacion = fake.address()
        cod_catastral = f"{fake.random_int(min=100, max=999)}-{fake.random_int(min=100, max=999)}-{fake.random_int(min=100, max=999)}-{fake.random_int(min=100, max=999)}"
        uso = random.choice(['Residencial', 'Comercial'])
        id_contribuyente = random.choice(contribuyentes_ids)
        id_sector = random.choice(sectores_ids)
        fecha_registro = fake.date_between(start_date=start_date, end_date=end_date).strftime("%d-%m-%Y")
        
        if uso == 'Residencial':
            cursor.execute('''
                INSERT INTO inmuebles (nom_inmueble, ubicacion, cod_catastral, uso, id_contribuyente, id_sector, fecha_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nom_inmueble, ubicacion, cod_catastral, uso, id_contribuyente, id_sector, fecha_registro))
        else:
            rif = fake.random_int(min=10000000, max=99999999)  # Ensure rif is a maximum of 8 digits
            j = random.choice(['J', 'C', 'G'])
            cursor.execute('''
                INSERT INTO inmuebles (nom_inmueble, ubicacion, cod_catastral, uso, id_contribuyente, id_sector, fecha_registro, rif, j)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nom_inmueble, ubicacion, cod_catastral, uso, id_contribuyente, id_sector, fecha_registro, rif, j))

# Generate random data for the "liquidaciones" table
def generate_liquidaciones(num_records):
    cursor.execute('SELECT id_inmueble FROM inmuebles')
    inmuebles_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute('SELECT id_contribuyente FROM contribuyentes')
    contribuyentes_ids = [row[0] for row in cursor.fetchall()]

    start_date = date(2023, 1, 1)
    end_date = date(2025, 12, 31)

    valid_solicitudes = [
        "Constancia de mensura y deslinde",
        "Constancia de info catastral (no propietarios)",
        "Cédula catastral (propietarios)",
        "Copia certificada cédula catastral",
        "Planos de ubicación",
        "Copia certificada constancia de mensura, deslinde",
        "Inscripción/modificación en el registro del inmueble"
    ]

    for _ in range(num_records):
        solicitud = random.choice(valid_solicitudes)
        monto_1 = round(random.uniform(1000, 5000), 2)
        monto_2 = round(random.uniform(1000, 5000), 2)
        monto_3 = round(random.uniform(1000, 5000), 2)
        fecha_Liquidacion_1 = fake.date_between(start_date=start_date, end_date=end_date).strftime("%d-%m-%Y")
        
        # Randomly decide whether to include fecha_Liquidacion_2 and fecha_Liquidacion_3
        if random.choice([True, False]):
            fecha_Liquidacion_2 = fake.date_between(start_date=start_date, end_date=end_date).strftime("%d-%m-%Y")
            fecha_Liquidacion_3 = fake.date_between(start_date=start_date, end_date=end_date).strftime("%d-%m-%Y")
        else:
            fecha_Liquidacion_2 = None
            fecha_Liquidacion_3 = None
        
        id_inmueble = random.choice(inmuebles_ids)
        id_contribuyente = random.choice(contribuyentes_ids)
        
        cursor.execute('''
            INSERT INTO liquidaciones (solicitud, monto_1, monto_2, monto_3, fecha_Liquidacion_1, fecha_Liquidacion_2, fecha_Liquidacion_3, id_inmueble, id_contribuyente)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (solicitud, monto_1, monto_2, monto_3, fecha_Liquidacion_1, fecha_Liquidacion_2, fecha_Liquidacion_3, id_inmueble, id_contribuyente))

# Generate data
generate_contribuyentes(50)
generate_sectores(50)
generate_inmuebles(50)
generate_liquidaciones(50)
print("Data generation complete.")

# Commit changes and close the connection
conn.commit()
conn.close()
# Generate data
generate_contribuyentes(50)
generate_sectores(50)
generate_inmuebles(50)
generate_liquidaciones(50)
print("Data generation complete.")

# Commit changes and close the connection
conn.commit()
conn.close()