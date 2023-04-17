import csv
import os


import getpass

# Diccionario de usuarios y contraseñas
usuarios = {
    'dilan': 'cisco123',
    'admin': 'cisco123'
}

def login():
    usuario = input("Ingrese su nombre de usuario: ")
    contraseña = getpass.getpass("Ingrese su contraseña: ")

    if usuario in usuarios and usuarios[usuario] == contraseña:
        print("Inicio de sesión exitoso!")
        return True
    else:
        print("Nombre de usuario o contraseña incorrectos.")
        return False

# Ejemplo de uso
while not login():
    pass

def agregar_dispositivo():
    nombre = input("Ingrese el nombre del dispositivo: ")
    campus = input("Ingrese el campus al que pertenece el dispositivo: ")
    tipo = input("Ingrese el tipo de dispositivo: ")
    ip = input("Ingrese la dirección IP del dispositivo: ")
    mascara = input("Ingrese la máscara de subred del dispositivo: ")
    vlans = input("Ingrese la la vlan correspondiente: ")
    modelo_jerarquico = input("Ingrese al modelo jerarquico el cual pertenece: ")
    red_comprometido = input("Ingrese el Servicio de red comprometido: ")
    # Lee el archivo CSV de dispositivos y campus existentes
    with open('dispositivos.csv', mode='r') as archivo_dispositivos:
        lector_csv = csv.DictReader(archivo_dispositivos)
        # Revisa si el dispositivo ya existe en el archivo
        for row in lector_csv:
            if 'nombre' in row and row['nombre'] == nombre and row['campus'] == campus:
                print("El dispositivo ya existe en el campus especificado.")
                return
    # Si el dispositivo no existe, agrega una nueva entrada al archivo
    with open('dispositivos.csv', mode='a', newline='') as archivo_dispositivos:
        campos = ['nombre', 'campus', 'tipo', 'ip', 'mascara', 'Vlan', 'modelo jerarquico', 'red comprometido']
        writer = csv.DictWriter(archivo_dispositivos, fieldnames=campos)
        # Mueve el cursor al final del archivo para agregar una nueva línea
        archivo_dispositivos.seek(0, 2)
        writer.writerow({'nombre': nombre, 'campus': campus, 'tipo': tipo, 'ip': ip, 'mascara': mascara, 'Vlan': vlans, 'modelo jerarquico': modelo_jerarquico, 'red comprometido':red_comprometido})
    print("El dispositivo ha sido agregado exitosamente.")

def agregar_campus():
    # Solicita el nombre del campus
    campus = input("Ingrese el nombre del campus: ")

    # Abre el archivo CSV de campus para leerlo
    with open('campus.csv', mode='r', newline='') as archivo_campus:
        lector_csv = csv.reader(archivo_campus)
        campus_existente = list(lector_csv)

    # Busca si el campus ya existe en el archivo CSV
    for i in range(len(campus_existente)):
        if campus_existente[i][0] == campus:
            print(f"El campus {campus} ya existe.")
            opcion = input("¿Desea sobrescribirlo? (s/n): ")
            if opcion == "s":
                campus_existente[i][0] = campus
                # Guarda los cambios en el archivo CSV
                with open('campus.csv', mode='w', newline='') as archivo_campus:
                    escritor_csv = csv.writer(archivo_campus)
                    escritor_csv.writerows(campus_existente)
                print(f"El campus {campus} fue actualizado correctamente.")
            return

    # Agrega el campus al archivo CSV
    with open('campus.csv', mode='a', newline='') as archivo_campus:
        escritor_csv = csv.writer(archivo_campus)
        escritor_csv.writerow([campus])
    print(f"El campus {campus} fue agregado correctamente.")

def eliminar_dispositivo():
    nombre = input("Ingrese el nombre del dispositivo que desea eliminar: ")
    campus = input("Ingrese el campus al que pertenece el dispositivo: ")
    ip = input("Ingrese la dirección IP del dispositivo que desea eliminar: ")
    # Lee el archivo CSV de dispositivos y campus existentes
    with open('dispositivos.csv', mode='r') as archivo_dispositivos:
        lector_csv = csv.DictReader(archivo_dispositivos)
        # Crea una lista para almacenar las filas que no deben eliminarse
        filas_no_eliminadas = []
        # Recorre todas las filas del archivo y agrega las filas no eliminadas a la lista
        for row in lector_csv:
            if 'nombre' in row and row['nombre'] == nombre and row['campus'] == campus and row['ip'] == ip:
                # Si el nombre y la dirección IP del dispositivo coinciden con los proporcionados, no agrega la fila a la lista
                print("El dispositivo ha sido eliminado exitosamente.")
            else:
                # Si el nombre y/o la dirección IP del dispositivo no coinciden con los proporcionados, agrega la fila a la lista
                filas_no_eliminadas.append(row)
    # Abre el archivo CSV en modo de escritura y escribe las filas no eliminadas
    with open('dispositivos.csv', mode='w', newline='') as archivo_dispositivos:
        campos = ['nombre', 'campus', 'tipo', 'ip', 'mascara', 'Vlan', 'modelo jerarquico', 'red comprometido']
        writer = csv.DictWriter(archivo_dispositivos, fieldnames=campos)
        writer.writeheader()
        for row in filas_no_eliminadas:
            # Filtra las claves que no pertenecen al archivo CSV para evitar el error de 'ValueError'
            row = {key: value for key, value in row.items() if key in campos}
            writer.writerow(row)

def eliminar_campus():
    # Solicita el nombre del campus que desea eliminar
    campus = input("Ingrese el nombre del campus que desea eliminar: ")

    # Abre el archivo CSV de campus para leerlo
    with open('campus.csv', mode='r', newline='') as archivo_campus:
        lector_csv = csv.reader(archivo_campus)
        campus_existente = list(lector_csv)

    # Busca el campus que desea eliminar y elimina su entrada del archivo CSV
    eliminado = False
    for i in range(len(campus_existente)):
        if campus_existente[i][0] == campus:
            del campus_existente[i]
            eliminado = True
            # Guarda los cambios en el archivo CSV
            with open('campus.csv', mode='w', newline='') as archivo_campus:
                escritor_csv = csv.writer(archivo_campus)
                escritor_csv.writerows(campus_existente)
            print(f"El campus {campus} fue eliminado correctamente.")
            break

    # Si el campus no se encontró en el archivo CSV, muestra un mensaje de error
    if not eliminado:
        print(f"El campus {campus} no fue encontrado en el archivo.")

def visualizar_campus():
    # Abre el archivo CSV
    with open('campus.csv', mode='r', newline='') as archivo_campus:
        lector_csv = csv.reader(archivo_campus)
        # Imprime los campus existentes
        print("""
        Lista de campus existentes:
        """)
        for row in lector_csv:
            print(f"- {row[0]}")

def visualizar_archivo_dispositivos(dispositivos):
    with open('dispositivos.csv', mode='r', newline='') as archivo_dispositivos:
        lector_csv = csv.reader(archivo_dispositivos)
        # Imprime los dispositivos existentes
        print("""
        Lista de dispositivos existentes:
        """)
        for row in lector_csv:
            print(f"-  Nombre: {row[0]}")
            print(f"-  Campus: {row[1]}")
            print(f"-  Tipo: {row[2]}")
            print(f"-  Dirección IP: {row[3]}")
            print(f"-  Máscara de subred: {row[4]}")
            print(f"-  VLAN: {row[5]}")
            print(f"-  Modelo jerárquico: {row[6]}")
            print(f"-  Servicio de red comprometido: {row[7]}")
            print("-------------------------------------------------------------")

def menu():
    while True:
        print ("""
        Bienvenido al sistema de gestión de dispositivos.
        """)
        print("""
        Menú de opciones:
        1. Agregar dispositivo
        2. Agregar campus
        3. Visualizar dispositivos
        4. Visualizar campus
        5. Eliminar campus
        6. Eliminar dispositivo
        7. Salir
        """)

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            os.system("clear")
            agregar_dispositivo()
        elif opcion == "2":
            os.system("clear")
            agregar_campus()
        elif opcion == "3":
            os.system("clear")
            visualizar_archivo_dispositivos('dispositivos')
        elif opcion == "4":
            os.system("clear")
            visualizar_campus()
        elif opcion == "5":
            os.system("clear")
            eliminar_campus()
        elif opcion == "6":
            os.system("clear")
            eliminar_dispositivo()
        elif opcion == "7":
            os.system("clear")
            print("Gracias por utilizar el sistema de administración de dispositivos.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
# Ejemplo de uso del script
if __name__ == '__main__':
    menu()
