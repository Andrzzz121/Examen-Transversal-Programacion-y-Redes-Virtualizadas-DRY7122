#!/usr/bin/env python3
"""
Script que calcula distancia entre ciudades de Chile y Argentina
Utiliza la API de OpenRouteService
"""

import requests
import json


API_KEY = "5b3ce3597851110001cf6248a7edefc370be4e04bb4b1ca054353625"  
BASE_URL = "https://api.openrouteservice.org/v2/directions/"

def obtener_coordenadas(ciudad, pais):
    """Obtiene coordenadas (lat, lon) de una ciudad usando geocoding"""
    geocode_url = f"https://api.openrouteservice.org/geocode/search?api_key={API_KEY}&text={ciudad}&boundary.country={pais}"
    try:
        response = requests.get(geocode_url)
        data = response.json()
        if data['features']:
            return data['features'][0]['geometry']['coordinates']
        else:
            print(f"No se encontró la ciudad: {ciudad} en {pais}")
            return None
    except Exception as e:
        print(f"Error al obtener coordenadas: {e}")
        return None

def calcular_ruta(origen, destino, transporte):
    """Calcula la ruta entre dos puntos"""
    transport_map = {
        '1': 'driving-car',
        '2': 'cycling-regular',
        '3': 'foot-walking'
    }
    profile = transport_map.get(transporte, 'driving-car')
    
    url = f"{BASE_URL}{profile}?api_key={API_KEY}&start={origen[0]},{origen[1]}&end={destino[0]},{destino[1]}"
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        print(f"Error al calcular ruta: {e}")
        return None

def mostrar_resultados(data, transporte):
    """Muestra los resultados de la ruta calculada"""
    if not data or 'features' not in data or not data['features']:
        print("No se pudo calcular la ruta.")
        return
    
    distancia_km = data['features'][0]['properties']['segments'][0]['distance'] / 1000
    distancia_millas = distancia_km * 0.621371
    duracion_min = data['features'][0]['properties']['segments'][0]['duration'] / 60
    
    transport_name = {
        'driving-car': 'auto',
        'cycling-regular': 'bicicleta',
        'foot-walking': 'caminando'
    }.get(transporte, 'auto')
    
    print("\n--- Resultados del Viaje ---")
    print(f"Distancia: {distancia_km:.2f} km ({distancia_millas:.2f} millas)")
    print(f"Duración estimada: {duracion_min:.1f} minutos ({duracion_min/60:.1f} horas) {transport_name}")
    
    
    print("\nNarrativa del viaje:")
    steps = data['features'][0]['properties']['segments'][0]['steps']
    for i, step in enumerate(steps[:5]):
        print(f"{i+1}. {step['instruction']} ({step['distance']/1000:.1f} km)")

def main():
    print("=== Calculador de Viajes Chile-Argentina ===")
    print("Presione 's' en cualquier momento para salir\n")
    
    while True:
        
        ciudad_origen = input("Ciudad de Origen (Chile): ").strip()
        if ciudad_origen.lower() == 's':
            break
            
        ciudad_destino = input("Ciudad de Destino (Argentina): ").strip()
        if ciudad_destino.lower() == 's':
            break
        
        
        coord_origen = obtener_coordenadas(ciudad_origen, "CL")
        if not coord_origen:
            continue
            
        coord_destino = obtener_coordenadas(ciudad_destino, "AR")
        if not coord_destino:
            continue
        
        
        print("\nSeleccione medio de transporte:")
        print("1. Auto")
        print("2. Bicicleta")
        print("3. Caminando")
        transporte = input("Opción (1-3): ").strip()
        if transporte.lower() == 's':
            break
        
        
        ruta_data = calcular_ruta(coord_origen, coord_destino, transporte)
        if ruta_data:
            mostrar_resultados(ruta_data, transporte)
        
        print("\n----------------------------------------")

if __name__ == "__main__":
    main()
