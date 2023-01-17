#Importando  flask y algunos paquetes
from flask import Flask, render_template, request, redirect, url_for, jsonify

from datetime import date
from conexionBD import *  #Importando conexion BD


#Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
app = Flask(__name__)
application = app

app.secret_key = 'clave12223'


@app.route('/', methods=['GET', 'POST'])
def  inicio():
    return render_template('public/index.html')    


#Creand un decorador para mi ruta que recibe el codigo QR leido
@app.route('/qr', methods=['POST'])
def dataQR():
    
    if request.method == 'POST':
        idQR        = request.json['datoqr']
        print(idQR)
        return render_template('public/vista_resultado.html', miData = buscarAlumno(idQR))
    

def buscarAlumno(idAlumno=''):
    
    conexion_MySQLdb = connectionBD() #Hago instancia a mi conexion desde la funcion
    mycursor            = conexion_MySQLdb.cursor(dictionary=True)
    querySQL  = ("SELECT * FROM alumnos WHERE id='%s' LIMIT 1"  % (idAlumno,))
    mycursor.execute(querySQL)
    resultadoBD = mycursor.fetchone()
    #resultadoBD = mycursor.fetchall() 
    #fetchall () Obtener todos los registros, por si desean obtener mas de 1 registro, ademas en la
    #consulta se debe quitar el LIMIT 1

    totalResulBD = mycursor.rowcount #Total de resultados
    
    mycursor.close() #cerrrando conexion SQL
    conexion_MySQLdb.close() #cerrando conexion de la BD
    return resultadoBD




#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
        return redirect(url_for('inicio'))
    
              
            
if __name__ == "__main__":
    app.run(debug=True, port=8001)