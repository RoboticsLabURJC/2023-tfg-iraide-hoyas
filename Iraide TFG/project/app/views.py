from django.shortcuts import render
from plotly.offline import plot
from .models import usuario
import plotly.graph_objects as go
import plotly.express as px
import psycopg2

# Create your views here.
def datos_edad():
    edad = []
    cantidad =[]
    dat = []
    usuarios = usuario.objects.all()
    for user in usuarios:
        edad.append(user.edad)
    for i in edad:
        if i not in dat:
            dat.append(i)
    for i in edad:
        n = edad.count(i)
        cantidad.append(n)
    return dat, cantidad

def index(request):
    dat, cantidad = datos_edad()
    fig = go.Scatter(x=dat, y=cantidad)
    layout = dict(title='EDAD')
    f = go.Figure(data=[fig], layout=layout)
    plot_div = plot(f, output_type='div', include_plotlyjs=False)
    context = {
        'plot': plot_div
    }
    return render(request, 'prueba.html',context)