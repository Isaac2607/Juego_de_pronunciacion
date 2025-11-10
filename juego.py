# -*- coding: utf-8 -*-
import speech_recognition as sr
from random import choice
import time
import unicodedata

niveles = {
    "fácil": ["agenda", "ami", "souris"],
    "intermedio": ["ordinateur", "algorithme", "développeur"],
    "difícil": ["réseau neuronal", "apprentissage automatique", "intelligence artificielle"]
}

def quitar_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Habla ahora...")
        audio = recognizer.listen(source)
    try:
        texto = recognizer.recognize_google(audio, language="fr-FR")
        print(f"Reconocido: {texto}")
        return texto.lower().strip()
    except sr.UnknownValueError:
        print("No se entendió lo que dijiste.")
        return ""
    except sr.RequestError:
        print("Error al conectar con el servicio de reconocimiento.")
        return ""

def jugar(nivel):
    palabras = niveles.get(nivel, [])
    if not palabras:
        print("Nivel de dificultad incorrecto.")
        return

    puntuacion = 0
    for _ in range(len(palabras)):
        palabra_aleatoria = choice(palabras)
        print(f"\nPor favor, pronuncie la palabra: {palabra_aleatoria}")
        palabra_reconocida = speech()

        if quitar_acentos(palabra_aleatoria.lower()) == quitar_acentos(palabra_reconocida.lower()):
            print("✅ ¡Eso es correcto!")
            puntuacion += 1
        else:
            print(f"❌ Algo va mal. La palabra era: {palabra_aleatoria}")
        time.sleep(2)

    print(f"\n¡Se acabó el juego! Tu puntuación es: {puntuacion}/{len(palabras)}")
    if puntuacion >= 3:
       print("Excelente, eres un maestro con las palabras")
    elif puntuacion >= 2:
        print("Buen hecho, pero podrias mejorar")
    elif puntuacion >= 1:
        print("Buen intento, pero aun tienes mucho por mejorar.")
    elif puntuacion == 0:
        print("Buen intento, pero aun tienes mucho por mejorar.")
if __name__ == "__main__":
    nivel_seleccionado = input("Seleccione el nivel de dificultad (fácil/intermedio/difícil): ").lower()
    # Normalizamos para que 'facil' coincida con 'fácil'
    nivel_normalizado = ""
    for clave in niveles.keys():
        if quitar_acentos(clave) == quitar_acentos(nivel_seleccionado):
            nivel_normalizado = clave
            break
    jugar(nivel_normalizado)
