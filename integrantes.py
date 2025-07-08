integrantes = [
    {"nombre": "Nombre1", "apellido": "Apellido1"},
    {"nombre": "Nombre2", "apellido": "Apellido2"}
]

print("Integrantes del grupo:")
for i, integrante in enumerate(integrantes, 1):
    print(f"{i}. {integrante['nombre']} {integrante['apellido']}")
