import random
from datetime import datetime, timedelta
import pandas as pd

# Configuración de simulación
random.seed(42)
n_rutas = 100
n_pickups = 400

# 1. Tabla: Dimensión Rutas
regiones = ["AMBA Norte", "AMBA Sur", "AMBA Oeste", "CABA Central"]
choferes = [f"Chofer_{i}" for i in range(1, 21)]

rutas_data = []
for r_id in range(101, 101 + n_rutas):
    rutas_data.append(
        {
            "ruta_id": f"RUT-{r_id}",
            "region": random.choice(regiones),
            "chofer": random.choice(choferes),
            "capacidad_camion_paquetes": random.choice([300, 500, 800, 1000]),
            "fecha": (
                datetime(2026, 10, 1) + timedelta(days=random.randint(0, 3))
            ).strftime("%Y-%m-%d"),
        }
    )

df_rutas = pd.DataFrame(rutas_data)

# 2. Tabla: Hechos Pickups e Incidentes
tipos_incidentes = [
    "Ninguno",
    "Estacionamiento no disponible",
    "Falta de capacidad",
    "Vehiculo con puntos pendientes en cola",
    "Demora del Seller",
    "Direccion incorrecta",
]

# Pesos para simular frecuencia de problemas
pesos_incidentes = [0.70, 0.10, 0.08, 0.06, 0.04, 0.02]

pickups_data = []
for p_id in range(1001, 1001 + n_pickups):
    ruta = random.choice(rutas_data)
    incidente = random.choices(tipos_incidentes, weights=pesos_incidentes)[0]

    # Lógica de éxito según el incidente
    if incidente == "Ninguno":
        estado = "EXITOSO"
    elif incidente in ["Falta de capacidad", "Estacionamiento no disponible"]:
        estado = random.choices(["FALLIDO", "EXITOSO"], weights=[0.75, 0.25])[0]
    else:
        estado = random.choices(["FALLIDO", "EXITOSO"], weights=[0.40, 0.60])[0]

    paquetes_planeados = random.randint(20, 150)
    paquetes_recolectados = (
        paquetes_planeados
        if estado == "EXITOSO"
        else int(paquetes_planeados * random.uniform(0, 0.5))
    )

    pickups_data.append(
        {
            "pickup_id": f"PU-{p_id}",
            "ruta_id": ruta["ruta_id"],
            "seller_id": f"SEL-{random.randint(500, 599)}",
            "paquetes_planeados": paquetes_planeados,
            "paquetes_recolectados": paquetes_recolectados,
            "estado": estado,
            "incidente": incidente,
            "hora_llegada": f"{random.randint(8, 17):02d}:{random.choice([0, 15, 30, 45]):02d}",
        }
    )

df_pickups = pd.DataFrame(pickups_data)

# Guardar a CSV para subir a Google Sheets
df_rutas.to_csv("dim_rutas.csv", index=False)
df_pickups.to_csv("fact_pickups.csv", index=False)

print(
    "Archivos 'dim_rutas.csv' y 'fact_pickups.csv' creados con éxito para subir a Google Sheets."
)