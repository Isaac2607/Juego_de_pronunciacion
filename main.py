# Importar las bibliotecas necesarias de Flask
from flask import Flask, render_template, request, redirect, url_for
# Importar la biblioteca de bases de datos SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import os
from speech import speech_en, speech_fr, speech_es # Importar funciones de reconocimiento de voz en inglés y francés
from juego import niveles, jugar
# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Configurar la URI de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
# Desactivar el seguimiento de modificaciones de SQLAlchemy para mejorar el rendimiento
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crear una instancia de la base de datos SQLAlchemy
db = SQLAlchemy(app)

# Definir el modelo de la tabla de la base de datos
class Card(db.Model):
    # Creación de columnas
    # id
    id = db.Column(db.Integer, primary_key=True)
    # Título
    title = db.Column(db.String(100), nullable=False)
    # Descripción
    subtitle = db.Column(db.String(300), nullable=False)
    # Texto
    text = db.Column(db.Text, nullable=False)

    # Salida del objeto y del id
    def __repr__(self):
        return f'<Card {self.id}>'
    

#Asignación #1. Crear la tabla Usuario
class User(db.Model):
    # Creación de columnas
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Salida del objeto y del id
    def __repr__(self):
        return f'<User {self.id}>'

# Ejecutar la página de contenidos
@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']
            
            #Asignación #4. Aplicar la autorización
            user = User.query.filter_by(email=form_login, password=form_password).first()
            if user:
                return redirect(url_for('index'))
            else:
                error = 'Credenciales inválidas. Por favor, inténtelo de nuevo.'
                return render_template('login.html', error=error)
            
        else:
            return render_template('login.html')

@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        #Asignación #3. Hacer que los datos del usuario se registren en la base de datos.
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


# Ejecutar la página de contenidos
@app.route('/index')
def index():
    # Visualización de las entradas de la base de datos
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)

# Ejecutar la página con la entrada
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Ejecutar la página de creación de entradas
@app.route('/create')
def create():
    return render_template('create_card.html')

# El formulario de inscripción
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        # Creación de un objeto que se enviará a la base de datos
        card = Card(title=title, subtitle=subtitle, text=text)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

@app.route("/voz")
def voz():
    try:
        texto = speech_es()  # Intentar capturar texto en inglés usando reconocimiento de voz
    except:
        texto = "Algo salió mal..."  # Mensaje de error si ocurre un problema
    return render_template("crear_tarjeta.html", texto=texto)  # Renderizar la plantilla con el texto capturado


@app.route("/juego", methods=["POST"])
def juego():
    nivel = request.form["nivel"]  # Obtener el nivel seleccionado del formulario
    palabras = niveles.get(nivel, [])  # Obtener las palabras correspondientes al nivel
    if not palabras:
        return redirect("/")  # Redirigir a la página principal si el nivel no es válido

    puntuacion = 0
    for palabra in palabras:
        # Mostrar la palabra al usuario
        palabra_reconocida = speech_fr()  # Usar la función speech_fr para capturar la palabra
        if palabra == palabra_reconocida:
            puntuacion += 1

    # Redirigir a la página principal con los resultados del juego
    return render_template(
    "index.html",
    tarjetas=Card.query.order_by(Card.id).all(),  # <-- Cambiado Tarjeta por Card
    puntuacion=puntuacion,
    total=len(palabras)
    )




# Bloque principal para ejecutar la aplicación
if __name__ == "__main__":
    # Eliminar la base de datos existente si existe
    if os.path.exists('diary.db'):
        os.remove('diary.db')
    
    try:
        with app.app_context():  # Crear el contexto de la aplicación
            db.create_all()  # Crear todas las tablas en la base de datos
        print("Base de datos creada exitosamente.")  # Imprimir mensaje de éxito
    except Exception as e:
        print(f"Error al crear la base de datos: {e}")  # Imprimir mensaje de error si ocurre una excepción
    app.run(debug=True)  # Ejecutar la aplicación en modo de depuración



