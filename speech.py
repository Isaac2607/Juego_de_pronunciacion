import speech_recognition as sr  # Importar la biblioteca speech_recognition
from random import choice  # Importar choice para seleccionar elementos aleatorios
import time  # Importar time para pausas

# Niveles de dificultad con palabras asociadas
niveles = {
    "facil": ["agenda", "ami", "souris"],
    "intermedio": ["ordinateur", "algorithme", "développeur"],
    "dificil": ["réseau neuronal", "apprentissage automatique", "intelligence artificielle"]
}

def speech():
    """Función para capturar y reconocer voz usando speech_recognition."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Habla ahora...")
        audio = recognizer.listen(source)
    try:
        texto = recognizer.recognize_google(audio, language="fr-FR")  # Cambia el idioma si lo necesitas
        print(f"Reconocido: {texto}")
        return texto.lower()
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
        print(f"Por favor, pronuncie la palabra {palabra_aleatoria}")
        palabra_reconocida = speech()
        if palabra_aleatoria == palabra_reconocida:
            print("¡Eso es correcto!")
            puntuacion += 1
        else:
            print(f"Algo va mal. La palabra era: {palabra_aleatoria}")
        time.sleep(2)

    print(f"¡Se acabó el juego! Tu puntuación es: {puntuacion}/{len(palabras)}")

if __name__ == "_main_":
    nivel_seleccionado = input("Seleccione el nivel de dificultad (facil/intermedio/dificil): ").lower()
    jugar(nivel_seleccionado)