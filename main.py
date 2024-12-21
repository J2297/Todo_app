from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

# Mapeo de la tabla
class Villancico(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100))
    state = db.Column(db.Boolean)

# Crear la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    villancicos = Villancico.query.all()
    return render_template('index.html', villancicos=villancicos)

@app.route('/add', methods=['POST'])
def add():
    # Lista de villancicos iniciales
    villancicos_titulo = [
        "Noche de Paz", "Feliz Navidad", "Campana sobre campana", 
        "Los peces en el río", "El tamborilero", "Cascabeles", 
        "Mi burrito sabanero", "El niño del tambor", "Ven a mi casa esta Navidad", 
        "Ya vienen los Reyes Magos"
    ]
    
    for title in villancicos_titulo:
        # Solo agregar villancicos si no existen en la base de datos
        if not Villancico.query.filter_by(title=title).first():
            new_villancico = Villancico(title=title, state=False)
            db.session.add(new_villancico)
    
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_custom', methods=['POST'])
def add_custom():
    # Agregar un villancico personalizado
    title = request.form.get('title')
    if title:
        new_villancico = Villancico(title=title, state=False)
        db.session.add(new_villancico)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    villancico = Villancico.query.get(id)
    if villancico:
        villancico.state = not villancico.state
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    villancico = Villancico.query.get(id)
    if villancico:
        db.session.delete(villancico)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
