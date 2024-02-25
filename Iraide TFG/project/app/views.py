from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from plotly.offline import plot
from .models import usuario, clase, ejercicio, actividad
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
from datetime import datetime
import plotly.express as px
import psycopg2

# Create your views here.
def todos_usuarios():
    users = []
    usuarios = usuario.objects.all()
    for u in usuarios:
        users.append(u.user)
    return users

def index(request):
    if request.method == 'GET':
        return render(request, 'formulario.html',{'msg':''})
    elif request.method == "POST":
        if request.POST['boton'] == 'iniciar':
            users = todos_usuarios()
            user = request.POST['user']
            pwd = request.POST['pwd']
            if user in users:
                u = usuario.objects.get(user=user)
                if u.pwd == pwd:
                    response = redirect('/dash')
                    response.set_cookie("cookie", user)
                    return response
                else:
                    msg = 'Contraseña incorrecta'
                    context = {'msg': msg}
                    return render(request, 'formulario.html', context)
            else:
                msg = 'Usuario no registrado, registrese'
                context = {'msg': msg}
                return render(request, 'formulario.html', context)
        elif request.POST['boton'] == 'registrar':
            users = todos_usuarios()
            student = False
            teacher = False
            admin = False
            user = request.POST['user']
            if user in users:
                msg = 'Nombre de usuario no disponible, escoja otro'
                context = {'msg': msg}
                return render(request, 'formulario.html', context)
            pwd = request.POST['pwd']
            nombre = request.POST['nombre']
            edad = request.POST['edad']
            pais = request.POST['pais']
            sexo = request.POST['sexo']
            so = request.POST['so']
            rol = request.POST.getlist('rol[]')
            if (len(rol)==0) or ('student' in rol):
                student = True
            if 'teacher' in rol:
                teacher = True
            if 'admin' in rol:
                admin=True
            response = redirect('/dash')
            response.set_cookie("cookie", user)
            user = usuario.objects.create(user=user,pwd=pwd,nombre=nombre,edad=edad,pais=pais,sexo=sexo,
                                       so=so, is_student=student, is_teacher=teacher,is_admin=admin)
            user.save()
            return response

def obtener_clases(user):
    usuarios = []
    lista_clases = []
    clases = clase.objects.all()
    for cl in clases:
        lista_usuarios = cl.usuarios.all()
        for u in lista_usuarios:
            if u.user == user:
                lista_clases.append(cl)
    for cl in lista_clases:
        usuarios = cl.usuarios.exclude(user=user)
    return usuarios

def datos_edad(datos):
    edad = []
    cantidad = []
    dat = []
    usuarios = []
    if datos.is_admin:
        usuarios = usuario.objects.all()
    if datos.is_teacher:
        usuarios = obtener_clases(datos.user)
    for user in usuarios:
        edad.append(user.edad)
    for i in edad:
        if i not in dat:
            dat.append(i)
    for i in dat:
        n = edad.count(i)
        cantidad.append(n)
    return dat, cantidad

def datos_genero(datos):
    usuarios = []
    if datos.is_admin:
        usuarios = usuario.objects.all()
    if datos.is_teacher:
        usuarios = obtener_clases(datos.user)
    fem = 0
    masc = 0
    for user in usuarios:
        if user.sexo == "F":
            fem += 1
        elif user.sexo == "M":
            masc += 1
    return [fem, masc]

def datos_ssoo(datos):
    usuarios = []
    if datos.is_admin:
        usuarios = usuario.objects.all()
    if datos.is_teacher:
        usuarios = obtener_clases(datos.user)
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

def datos_pais(datos):
    usuarios = []
    if datos.is_admin:
        usuarios = usuario.objects.all()
    if datos.is_teacher:
        usuarios = obtener_clases(datos.user)
    loc = Nominatim(user_agent="GetLoc")
    latitudes = []
    longitudes = []
    for user in usuarios:
        localizacion = loc.geocode(user.pais, timeout=20)
        latitudes.append(localizacion.latitude)
        longitudes.append(localizacion.longitude)
    return latitudes, longitudes

def datos_actividad(user, datos_usuario, context):
    usuarios_clase =[]
    if datos_usuario.is_teacher:
        usuarios_clase = obtener_clases(user)
    if datos_usuario.is_admin:
        usuarios_clase = usuario.objects.all()
    if datos_usuario.is_student:
        usuarios_clase = usuario.objects.filter(user=user)
    graficas_act = []
    for u in usuarios_clase:
        act = actividad.objects.filter(usuario=u)
        lista_fecha = []
        lista_duracion = []
        lista_evento = []
        for a in act:
            fecha_inicio = a.fecha_inicio
            fecha_fin = a.fecha_fin
            evento = a.evento
            if evento=='0':
                ev = "Ingresa en la plataforma"
            else:
                ev = "Ejercicio "+evento
            fecha = fecha_inicio.strftime("%d/%m/%Y")
            duracion = str(fecha_fin - fecha_inicio)
            duracion = duracion.split(":")
            duracion = duracion[0]+"."+duracion[1]
            lista_fecha.append(fecha)
            lista_duracion.append(float(duracion))
            lista_evento.append(ev)
        fig = go.Scatter(x=lista_fecha, y=lista_duracion, line=dict(color='orange'),text=lista_evento,)
        layout = dict(title='Actividad ' + str(u.nombre),xaxis_title="Fecha",yaxis_title="Horas por dia")
        f = go.Figure(data=[fig], layout=layout)
        plot_div = plot(f, output_type='div', include_plotlyjs=False)
        graficas_act.append(plot_div)
    context['graficas_act'] = graficas_act

def dash(request):
    user = request.COOKIES.get('cookie')
    datos_usuario = usuario.objects.get(user=user)


    #DASHBOARD DE LA EDADES
    dat, cantidad = datos_edad(datos_usuario)
    fig = go.Scatter(x=dat, y=cantidad, mode='markers', line=dict(color='red'))
    layout = dict(title='EDAD')
    f = go.Figure(data=[fig], layout=layout)
    plot_div = plot(f, output_type='div', include_plotlyjs=False)

    #DASHBOARD DE LOS GENEROS
    dat_gen = datos_genero(datos_usuario)
    valores = ["Femenino", "Masculino"]
    fig1 = go.Bar(x=valores,y=dat_gen, width=0.5)
    layout = dict(title='GENERO')
    f1 = go.Figure(data=[fig1], layout=layout)
    plot_div1 = plot(f1, output_type='div', include_plotlyjs=False)

    #DASHBOARD DEL SSOO
    dat = datos_ssoo(datos_usuario)
    val = ["Linux", "Mac", "Windows", "Otro"]
    fig2 = go.Pie(labels=val,values=dat)
    layout = dict(title='SISTEMA OPERATIVO')
    f2= go.Figure(data=[fig2], layout=layout)
    plot_div2 = plot(f2, output_type='div', include_plotlyjs=False)

    #DASBOARD DE PAISES
    latitudes, longitudes = datos_pais(datos_usuario)
    fig3 = go.Scattergeo(lon=longitudes, lat=latitudes)
    layout = dict(title='PAISES')
    f3 = go.Figure(data=[fig3], layout=layout)
    plot_div3 = plot(f3, output_type='div', include_plotlyjs=False)

    context = {
        'nombre': datos_usuario.nombre
    }

    datos_actividad(user,datos_usuario,context)

    if datos_usuario.is_student:
        context['msg']= 'Eres estudiante solo puedes ver tus datos'
    if datos_usuario.is_teacher:
        context['plot']= plot_div
        context['plot1']= plot_div1
        context['plot2']= plot_div2
        context['plot3']= plot_div3
    if datos_usuario.is_admin:
        context['plot'] = plot_div
        context['plot1'] = plot_div1
        context['plot2'] = plot_div2
        context['plot3'] = plot_div3

    return render(request, 'prueba.html',context)

