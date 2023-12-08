import time
import asyncio
import random
import requests
import webbrowser
import string
from cryptography.fernet import Fernet
import os
import json
import base64
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading

# Contador de bloques completados
bloques_completados = 0

# Variables para indicar el estado de la página y el contador
pagina_cerrada = False
contador_finalizado = False

# Clave de cifrado
clave_cifrado = Fernet.generate_key()
cipher_suite = Fernet(clave_cifrado)

def abrir_google():
    url = 'https://www.google.com'
    inicio_tiempo = time.time()  # Capturamos el tiempo de inicio
    webbrowser.open(url)
    tiempo_transcurrido = time.time() - inicio_tiempo  # Calculamos el tiempo transcurrido
    print(f'Tiempo transcurrido: {tiempo_transcurrido} segundos')

# Función para guardar el número de bloques completados cifrado en un archivo
def guardar_bloques_completados(bloques_completados):
    bloques_completados_cifrado = cipher_suite.encrypt(str(bloques_completados).encode())
    with open("bloques_completados.dat", "wb") as file:
        file.write(bloques_completados_cifrado)

# Función para cargar el número de bloques completados desde un archivo cifrado
def cargar_bloques_completados():
    try:
        with open("bloques_completados.dat", "rb") as file:
            bloques_completados_cifrado = file.read()
            bloques_completados = int(cipher_suite.decrypt(bloques_completados_cifrado).decode())
            return bloques_completados
    except (FileNotFoundError, ValueError):
        return 0  # Devolver 0 si el archivo no existe o está dañado

# Función para obtener o solicitar el nombre público del usuario
def obtener_nombre_publico():
    nombre_usuario_path = "nombre_usuario.txt"

    if not os.path.exists(nombre_usuario_path):
        nombre_usuario = input("Introduce tu nombre público: ")
        with open(nombre_usuario_path, "w") as nombre_usuario_file:
            nombre_usuario_file.write(nombre_usuario)
    else:
        with open(nombre_usuario_path, "r") as nombre_usuario_file:
            nombre_usuario = nombre_usuario_file.read()

    return nombre_usuario

# Función para generar o cargar clave privada
def obtener_clave_privada():
    clave_privada_path = "clave_privada.key"

    if not os.path.exists(clave_privada_path):
        nombre_usuario = input("Introduce tu nombre de usuario: ")
        clave_privada = Fernet.generate_key()

        # Guardar la clave privada y el nombre de usuario
        with open(clave_privada_path, "wb") as clave_privada_file:
            clave_privada_file.write(clave_privada)

        with open("nombre_usuario.txt", "w") as nombre_usuario_file:
            nombre_usuario_file.write(nombre_usuario)
    else:
        with open(clave_privada_path, "rb") as clave_privada_file:
            clave_privada = clave_privada_file.read()

    return Fernet(clave_privada)

# Función para obtener la clave pública
def obtener_clave_publica():
    clave_publica_path = "clave_publica.txt"

    if not os.path.exists(clave_publica_path):
        nombre_usuario = input("Introduce tu nombre de usuario: ")
        clave_publica = Fernet.generate_key()
        clave_publica_encoded = base64.urlsafe_b64encode(clave_publica)

        # Guardar la clave pública y el nombre de usuario
        with open(clave_publica_path, "wb") as clave_publica_file:
            clave_publica_file.write(clave_publica_encoded)

        with open("nombre_usuario.txt", "w") as nombre_usuario_file:
            nombre_usuario_file.write(nombre_usuario)
    else:
        with open(clave_publica_path, "rb") as clave_publica_file:
            clave_publica_encoded = clave_publica_file.read()

    return Fernet(base64.urlsafe_b64decode(clave_publica_encoded))

# Función para generar un ID aleatorio
def generar_id_aleatorio():
    longitud = 128
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

# Función para abrir una página en el navegador y realizar interacciones
def abrir_pagina(urls):
    url_seleccionada = random.choice(urls)
    print(f"Abriendo la página: {url_seleccionada}. Espera unos momentos...")

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url_seleccionada)

    tiempo_restante = 30  # Inicializar el tiempo restante

    try:
        while tiempo_restante > 0:
            print(f"El bloque comenzará en {tiempo_restante} segundos.")
            time.sleep(1)  # Esperar 1 segundo
            tiempo_restante -= 1
            driver.title  # Comprobar si la ventana del navegador sigue abierta
    except NoSuchWindowException:
        print("La ventana del navegador se ha cerrado o está en segundo plano. El contador se ha detenido.")

    driver.quit()  # Cerrar la ventana del navegador al finalizar el contador

# Función para abrir la página en un hilo separado
def abrir_pagina_en_hilo(url):
    global pagina_cerrada
    abrir_pagina(url)

    # Informar al hilo principal que la página se ha cerrado
    pagina_cerrada = True

# Función para realizar bloques de forma automática
def realizar_bloques_automaticos():
    global bloques_completados, pagina_cerrada, contador_finalizado

    # Cargar el número de bloques completados desde el archivo cifrado
    bloques_completados = cargar_bloques_completados()

    while True:
        # Configuración del bloque automático
        id_bloque = generar_id_aleatorio()
        numero_problemas_por_bloque = random.randint(1000, 1000000)
        recompensa_por_problema = 0.0000000000000001

        # Lista de URLs de páginas
        lista_urls = ["https://cuty.io/NN8YMoGVlA", "https://otra-pagina.com"]

        # Verificar si la página debe abrirse antes de este bloque
        if bloques_completados > 0 and bloques_completados % 3 == 0:
            abrir_pagina(lista_urls)
            tiempo_restante = 30

            # Mostrar el tiempo restante antes de iniciar el bloque
            while tiempo_restante > 0:
                print(f"El bloque comenzará en {tiempo_restante} segundos.")
                time.sleep(1)  # Esperar 1 segundo
                tiempo_restante -= 1

        # Procesar el bloque
        nombre_publico = obtener_nombre_publico()
        thread_proceso = threading.Thread(target=procesar_bloque, args=(id_bloque, numero_problemas_por_bloque, recompensa_por_problema, nombre_publico))
        thread_proceso.start()
        thread_proceso.join()

        bloques_completados += 1  # Incrementar el contador de bloques
        guardar_bloques_completados(bloques_completados)  # Guardar el número de bloques completados cifrado en el archivo

        # Verificar si la página se cerró antes de que terminara el contador
        if pagina_cerrada and not contador_finalizado:
            print("La página se ha cerrado antes de que terminara el contador. Reiniciando el contador.")
            
            # Reiniciar el contador y abrir la página solo en bloques múltiplos de 3 a partir del bloque 2
            if bloques_completados > 0 and bloques_completados % 3 == 0:
                abrir_pagina(lista_urls)
                time.sleep(30)

            contador_finalizado = False  # Reiniciar el indicador del contador finalizado 

# Generar o cargar clave para cifrado
clave_path = "clave.key"

if not os.path.exists(clave_path):
    clave = Fernet.generate_key()
    with open(clave_path, "wb") as clave_file:
        clave_file.write(clave)
else:
    with open(clave_path, "rb") as clave_file:
        clave = clave_file.read()

cipher_suite = Fernet(clave)

# Función para cargar el balance cifrado
def cargar_balance():
    balance_path = "balance.dat"
    if os.path.exists(balance_path):
        with open(balance_path, "rb") as balance_file:
            balance_cifrado = balance_file.read()
        balance_descifrado = cipher_suite.decrypt(balance_cifrado)
        return json.loads(balance_descifrado)
    else:
        return {"recompensa_total": 0}
    
# Función para guardar el balance cifrado
def guardar_balance(balance):
    balance_path = "balance.dat"
    balance_serializado = json.dumps(balance).encode()
    balance_cifrado = cipher_suite.encrypt(balance_serializado)
    with open(balance_path, "wb") as balance_file:
        balance_file.write(balance_cifrado)

# Función para resolver problemas matemáticos aleatorios
def resolver_problema_matematico(numero_problema, total_problemas):
    # Simulamos una operación matemática complicada
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    resultado = num1 * num2

    # Simulamos el tiempo de procesamiento en la GPU
    # (Esto es solo una simulación y no afectará el tiempo total)
    tiempo_transcurrido = random.uniform(0.1, 1.0)

    print(f"Problema {numero_problema} de {total_problemas} completado")
    return tiempo_transcurrido

# Función para realizar un retiro
def realizar_retiro(balance, clave_privada):
    print(f"Tienes ${balance['recompensa_total']:.16f} actualmente")
    print("El mínimo para retirar es de 0.05$")
    print("Se retirará en Robux > 0.05$ = 5R$ (robux)")

    # Solicitar la cantidad a retirar
    while True:
        try:
            cantidad_retiro = float(input("\nElige la cantidad a retirar (en $): "))
            if cantidad_retiro < 0.05:
                print("La cantidad mínima para retirar es de 0.05$. Inténtalo de nuevo.")
            elif cantidad_retiro > balance['recompensa_total']:
                print("No tienes suficiente saldo para realizar este retiro. Inténtalo de nuevo.")
            else:
                break
        except ValueError:
            print("Por favor, ingresa un número válido.")

    # Confirmar el retiro
    confirmacion = input(f"\n¿Seguro que quieres realizar el retiro de ${cantidad_retiro:.16f}? (s/n) ").lower()

    if confirmacion == 's':
        # Procesar el retiro
        clave_retiro = generar_id_aleatorio()
        cantidad_robux = cantidad_retiro / 0.05 * 5

        # Actualizar el balance
        balance["recompensa_total"] -= cantidad_retiro
        guardar_balance(balance)

        # Enviar mensaje al webhook
        nombre_publico = obtener_nombre_publico()
        enviar_mensaje_retiro(clave_retiro, cantidad_retiro, cantidad_robux, clave_privada, nombre_publico)

        # Abrir la página solo si es la primera vez o después de cada 3 bloques
        if balance.get("bloques_completados", 0) == 0 or balance["bloques_completados"] % 3 == 0:
            abrir_pagina("https://cuty.io/NN8YMoGVlA")

        print("\n¡Retiro exitoso! Se ha enviado la solicitud para procesar el retiro.")
    else:
        print("\nRetiro cancelado.")



# Función para enviar mensajes a través de un webhook de Discord
def enviar_mensaje_discord(id_bloque, recompensa, cantidad_problemas, tiempo_total_total):
    webhook_url = "https://discord.com/api/webhooks/1182429469693186099/2IeNbxd4WTyEq_KBtt0UNlnoE5Q1AFmJNlVk7jeZGq748uLoblyZkVvPEKvsFGZVzhhf"

    nombre_publico = obtener_nombre_publico()

    mensaje = (
        f"**¡Bloque completado!**\n"
        f"ID del bloque: {id_bloque}\n"
        f"Recompensa: ${recompensa:.16f}\n"
        f"Cantidad de problemas: {cantidad_problemas}\n"
        f"Tiempo total total: {tiempo_total_total:.2f} segundos\n"
        f"Completado por: {nombre_publico}"
    )
    payload = {"content": mensaje}
    requests.post(webhook_url, json=payload)

# Función para enviar mensaje de retiro al webhook de Discord
def enviar_mensaje_retiro(clave_retiro, cantidad_retiro, cantidad_robux, clave_privada, nombre_publico):
    clave_publica = obtener_clave_publica()

    webhook_url = "https://discord.com/api/webhooks/1182473622112182392/fEr-hhxD0SNPU9HDk7rN2NlCTFTVxBdIBY6EJxLsaFVaeqfSURDNf5r1VcFYKuzofZMn"
    mensaje = (
        f"**¡Nuevo retiro!**\n"
        f"Clave: {clave_retiro}\n"
        f"Balance a retirar: ${cantidad_retiro:.16f}\n"
        f"Conversión a Robux: {cantidad_robux:.2f}R$ (robux)\n"
        f"Nombre del completador: {nombre_publico}"
    )
    payload = {"content": mensaje}
    requests.post(webhook_url, json=payload)

# Función para procesar un bloque de problemas
def procesar_bloque(id_bloque, numero_problemas_por_bloque, recompensa_por_problema, nombre_publico):
    inicio_tiempo_total = time.time()  # Capturamos el tiempo de inicio total
    tiempo_total = 0

    for i in range(1, numero_problemas_por_bloque + 1):
        tiempo_problema = resolver_problema_matematico(i, numero_problemas_por_bloque)
        tiempo_total += tiempo_problema

    recompensa = numero_problemas_por_bloque * recompensa_por_problema
    tiempo_total_total = time.time() - inicio_tiempo_total  # Calculamos el tiempo total total

    # Procesamos el bloque y enviamos el mensaje del webhook
    enviar_mensaje_discord(id_bloque, recompensa, numero_problemas_por_bloque, tiempo_total_total)

    # Actualizamos el balance
    balance = cargar_balance()
    balance["recompensa_total"] += recompensa
    guardar_balance(balance)

    # Mostramos los resultados en la consola
    print(f"ID del bloque completado: {id_bloque}")
    print(f"Recompensa: ${recompensa:.16f}")
    print(f"Tiempo total total: {tiempo_total_total:.2f} segundos")
    print(f"Recompensa total acumulada: ${balance['recompensa_total']:.16f}")

# Main
while True:
    opcion = input('Escribe 1 para abrir Google, 2 para resolver un problema matemático, '
                   '3 para procesar un bloque, "retirar" para realizar un retiro, "auto" para realizar bloques automáticos (o "salir" para cerrar el programa): ')
    
    if opcion == '1':
        abrir_google()
    elif opcion == '2':
        resolver_problema_matematico(1, 1)  # La función ahora recibe dos parámetros
    elif opcion == '3':
        # Configuración del bloque
        id_bloque = generar_id_aleatorio()
        numero_problemas_por_bloque = random.randint(1000, 1000000)
        recompensa_por_problema = 0.0000000000000001

        # Procesar el bloque
        nombre_publico = obtener_nombre_publico()
        procesar_bloque(id_bloque, numero_problemas_por_bloque, recompensa_por_problema, nombre_publico)
    elif opcion.lower() == 'retirar':
        # Realizar un retiro
        balance = cargar_balance()
        clave_privada = obtener_clave_privada()
        realizar_retiro(balance, clave_privada)
    elif opcion.lower() == 'auto':
        # Realizar bloques automáticamente
        realizar_bloques_automaticos()
    elif opcion.lower() == 'salir':
        print('Saliendo del programa. ¡Hasta luego!')
        break
    else:
        print('Opción no válida. Inténtalo de nuevo.')