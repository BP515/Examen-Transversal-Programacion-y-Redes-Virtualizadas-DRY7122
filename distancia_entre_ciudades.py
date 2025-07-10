import requests
import urllib.parse

# Configuración
clave_api = "ab404e69-2ec4-4ab9-9f0d-d32565d8553b"
url_ruta = "https://graphhopper.com/api/1/route?"
url_geocodificacion = "https://graphhopper.com/api/1/geocode?"

# Opciones de transporte
vehiculos = {
    "1": ("Automóvil", "car"),
    "2": ("Bicicleta", "bike"),
    "3": ("A pie", "foot")
}

def geocodificar(ciudad):
    """Geocodifica una ciudad con la API de GraphHopper"""
    parametros = {
        "q": ciudad,
        "limit": 1,
        "key": clave_api
    }
    url = url_geocodificacion + urllib.parse.urlencode(parametros)
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        if respuesta.status_code == 200 and datos["hits"]:
            punto = datos["hits"][0]["point"]
            lat, lon = punto["lat"], punto["lng"]
            nombre = datos["hits"][0]["name"]
            pais = datos["hits"][0].get("country", "")
            region = datos["hits"][0].get("state", "")
            return True, lat, lon, f"{nombre}, {region}, {pais}".strip(", ")
        else:
            print(f"❌ No se encontró la ciudad '{ciudad}'")
            return False, None, None, ciudad
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False, None, None, ciudad

def formatear_duracion(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos = int(segundos % 60)
    return f"{horas:02d}h {minutos:02d}m {segundos:02d}s"

def mostrar_instrucciones(ruta):
    print("\n📍 Instrucciones de viaje:")
    for paso in ruta["paths"][0]["instructions"]:
        texto = paso["text"]
        distancia = paso["distance"] / 1000
        print(f"- {texto} ({distancia:.2f} km)")

def mostrar_resultado(origen, destino, distancia_km, duracion_seg):
    millas = distancia_km * 0.621371
    print("\n🧾 Resultado del viaje:")
    print(f"🔹 Desde: {origen}")
    print(f"🔹 Hasta: {destino}")
    print(f"📏 Distancia: {distancia_km:.2f} km | {millas:.2f} millas")
    print(f"⏱️ Duración estimada: {formatear_duracion(duracion_seg)}")

def seleccionar_transporte():
    print("\nSelecciona el medio de transporte:")
    for k, v in vehiculos.items():
        print(f"{k}. {v[0]}")
    opcion = input("Opción: ").strip()
    return vehiculos.get(opcion, vehiculos["1"])

def main():
    print("="*60)
    print("🚗 Calculador de viaje entre Chile y Argentina")
    print("="*60)
    print("Presiona 's' para salir en cualquier momento.")

    while True:
        origen = input("\n🏠 Ciudad de origen: ").strip()
        if origen.lower() == 's':
            break

        destino = input("🎯 Ciudad de destino: ").strip()
        if destino.lower() == 's':
            break

        transporte_nombre, transporte_api = seleccionar_transporte()

        ok1, lat1, lon1, origen_fmt = geocodificar(origen + ", Chile")
        ok2, lat2, lon2, destino_fmt = geocodificar(destino + ", Argentina")

        if not (ok1 and ok2):
            continue

        params = {
            "point": [f"{lat1},{lon1}", f"{lat2},{lon2}"],
            "vehicle": transporte_api,
            "locale": "es",
            "instructions": "true",
            "key": clave_api
        }
        url_final = url_ruta + urllib.parse.urlencode(params, doseq=True)

        try:
            respuesta = requests.get(url_final)
            datos = respuesta.json()
            if respuesta.status_code == 200:
                path = datos["paths"][0]
                distancia_km = path["distance"] / 1000
                duracion_seg = path["time"] / 1000

                mostrar_resultado(origen_fmt, destino_fmt, distancia_km, duracion_seg)
                mostrar_instrucciones(datos)
            else:
                print(f"❌ Error en la ruta: {datos.get('message', 'Desconocido')}")
        except Exception as e:
            print(f"❌ Error de conexión: {e}")

        seguir = input("\n¿Deseas calcular otra ruta? (s/n): ").strip().lower()
        if seguir != 's':
            break

    print("\n👋 ¡Gracias por usar el calculador de viajes!")

if __name__ == "__main__":
    main()