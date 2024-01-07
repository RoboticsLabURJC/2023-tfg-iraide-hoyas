from django.shortcuts import render
from plotly.offline import plot
from .models import usuario
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
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
    for i in dat:
        n = edad.count(i)
        cantidad.append(n)
    print(dat)
    print(cantidad)
    return dat, cantidad

def datos_genero():
    usuarios = usuario.objects.all()
    fem = 0
    masc = 0
    for user in usuarios:
        if user.sexo == "F":
            fem += 1
        elif user.sexo == "M":
            masc += 1
    return [fem, masc]

def datos_ssoo():
    usuarios = usuario.objects.all()
    l = 0
    m = 0
    w = 0
    otro = 0
    for user in usuarios:
        if user.so == "Linux":
            l += 1
        elif user.so == "Mac":
            m += 1
        elif user.so == "Windows":
            w += 1
        else:
            otro += 1
    return [l, m, w, otro]

def datos_pais():
    usuarios = usuario.objects.all()
    loc = Nominatim(user_agent="GetLoc")
    latitudes = []
    longitudes = []
    for user in usuarios:
        localizacion = loc.geocode(user.pais, timeout=20)
        latitudes.append(localizacion.latitude)
        longitudes.append(localizacion.longitude)
    return latitudes, longitudes

def index(request):
    #DASHBOARD DE LA EDADES
    dat, cantidad = datos_edad()
    fig = go.Scatter(x=dat, y=cantidad, mode='markers', line=dict(color='red'))
    layout = dict(title='EDAD')
    f = go.Figure(data=[fig], layout=layout)
    plot_div = plot(f, output_type='div', include_plotlyjs=False)

    #DASHBOARD DE LOS GENEROS
    dat_gen = datos_genero()
    valores = ["Femenino", "Masculino"]
    fig1 = go.Bar(x=valores,y=dat_gen, width=0.5)
    layout = dict(title='GÉNERO')
    f1 = go.Figure(data=[fig1], layout=layout)
    plot_div1 = plot(f1, output_type='div', include_plotlyjs=False)

    #DASHBOARD DEL SSOO
    dat = datos_ssoo()
    val = ["Linux", "Mac", "Windows", "Otro"]
    fig2 = go.Pie(labels=val,values=dat)
    layout = dict(title='SISTEMA OPERATIVO')
    f2= go.Figure(data=[fig2], layout=layout)
    plot_div2 = plot(f2, output_type='div', include_plotlyjs=False)

    #DASBOARD DE PAISES
    latitudes, longitudes = datos_pais()
    fig3 = go.Scattergeo(lon=longitudes, lat=latitudes)
    layout = dict(title='PAISES')
    f3 = go.Figure(data=[fig3], layout=layout)
    plot_div3 = plot(f3, output_type='div', include_plotlyjs=False)


    context = {
        'plot': plot_div,
        'plot1': plot_div1,
        'plot2': plot_div2,
        'plot3': plot_div3
    }
    return render(request, 'prueba.html',context)