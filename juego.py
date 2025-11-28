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

INTENTOS_POR_PALABRA = 3   # -----------------------> Puedes cambiar el número de intentos

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

    for palabra_aleatoria in palabras:
        print(f"\nPor favor, pronuncie la palabra: {palabra_aleatoria}")

        acierto = False

        for intento in range(1, INTENTOS_POR_PALABRA + 1):
            print(f"🔄 Intento {intento}/{INTENTOS_POR_PALABRA}")
            palabra_reconocida = speech()

            if quitar_acentos(palabra_aleatoria.lower()) == quitar_acentos(palabra_reconocida.lower()):
                print("✅ ¡Correcto!")
                puntuacion += 1
                acierto = True
                break
            else:
                print("❌ No coincide.")
                if intento < INTENTOS_POR_PALABRA:
                    print("Inténtalo de nuevo...\n")
                time.sleep(1)

        if not acierto:
            print(f"❌ No lograste decir la palabra. La correcta era: {palabra_aleatoria}")

        time.sleep(1)

    print(f"\n🎉 ¡Se acabó el juego! Tu puntuación es: {puntuacion}/{len(palabras)}")

    if puntuacion >= 3:
        print("Excelente, eres un maestro con las palabras.")
    elif puntuacion >= 2:
        print("Buen hecho, pero podrías mejorar.")
    elif puntuacion >= 1:
        print("Buen intento, pero aún tienes mucho por mejorar.")
    else:
        print("No te preocupes, ¡sigue practicando!")

if __name__ == "__main__":
    nivel_seleccionado = input("Seleccione el nivel de dificultad (fácil/intermedio/difícil): ").lower()

    # Normalizamos para permitir "facil" = "fácil"
    nivel_normalizado = ""
    for clave in niveles.keys():
        if quitar_acentos(clave) == quitar_acentos(nivel_seleccionado):
            nivel_normalizado = clave
            break

    jugar(nivel_normalizado)
