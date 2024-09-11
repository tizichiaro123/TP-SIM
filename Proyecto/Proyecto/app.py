from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

def generar_uniforme(a, b, N):
    return a + (b - a) * np.random.rand(N)

def generar_exponencial(lambd, N):
    return -np.log(1 - np.random.rand(N)) / lambd

def generar_normal(media, desviacion, N):
    u1 = np.random.rand(N)
    u2 = np.random.rand(N)
    z1 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
    return media + desviacion * z1

def generar_histograma(datos, bins):
    plt.hist(datos, bins=bins, edgecolor='black')
    plt.xlabel('Intervalos')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de frecuencias')
    plt.show()
    plt.close()  # Cierra la figura para liberar memoria

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            N = int(request.form['N'])
            distribucion = request.form['distribucion']
            intervalos = int(request.form['intervalos'])
            a = float(request.form['a'])
            b = float(request.form['b'])
            lambd = float(request.form['lambd'])
            media = float(request.form['media'])
            desviacion = float(request.form['desviacion'])

            if distribucion == 'uniforme':
                datos = generar_uniforme(a, b, N)
            elif distribucion == 'exponencial':
                datos = generar_exponencial(lambd, N)
            elif distribucion == 'normal':
                datos = generar_normal(media, desviacion, N)
            else:
                return "Distribución no válida", 400

            generar_histograma(datos, intervalos)

            # Convertir los datos en una lista de listas para pasar a la plantilla
            datos_tabla = list(enumerate(datos, start=1))

        except ValueError:
            return "Error en los datos ingresados", 400

        return render_template('resultado.html', datos_tabla=datos_tabla)

    return render_template('formulario.html')

if __name__ == '__main__':
    # Asegúrate de que la carpeta 'static' exista
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
