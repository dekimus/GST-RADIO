#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
#Requiere gstreamer0.10-ffmpeg para los WMA
#

import pygst, gst
import time
from Tkinter import *

#Lista con las emisoras
emisoras = [("Cadena Ser Alicante   ", 1),("Radio  Paradise    96k ", 2),
             ("Radio Express  Marca   ", 3), ("Cadena Ser Elche [bug]", 4)]


emisorasUrl = [("Cadena Ser Alicante   ", 'http://playerservices.streamtheworld.com/api/livestream-redirect/SER_ALICANTE.mp3'),
              ("Radio  Paradise    96k ", 'http://stream-tx3.radioparadise.com/rp_96.ogg'),
              ("Radio Express  Marca   ", 'rtmp://teledifusion.tv/teleelxradio/teleelxradiolive'),
              ("Cadena Ser Elche [bug]", 'mms://94.127.190.245/radioelche')]

#emisora por defecto
streamUri = 'http://stream-tx3.radioparadise.com/rp_96.ogg'

#volumen inicial
volume = 1


#ventana principal de la aplicacion
ventana = Tk()
ventana.geometry("420x250")
ventana.title("GST-RADIO v1.2")
texto = Label(ventana, text="GST-RADIO ", font=('times', 15, "bold")).grid(row=0, column=0)




#funciones basicas del reproductor
def play():
    player.set_state(gst.STATE_PLAYING)

def stop():
    player.set_state(gst.STATE_NULL)

def pause():
    player.set_state(gst.STATE_PAUSED)

def vol_up():
    global volume

    if volume >= 0 and volume < 6:
        volume += 0.5
        player.set_property("volume", volume)

def vol_down():
    global volume

    if volume > 0:
        volume -= 0.5
        player.set_property("volume", volume)

def abrirurl():
    global urlV, newurl

    urlV = StringVar()
    newurl = Toplevel(ventana)
    newurl.title("Nueva Url")
    newurlTxt = Label(newurl, text="Introduce la nueva url...").grid()
    newurlEntry = Entry(newurl, width=50, textvariable=urlV).grid()
    accept = Button(newurl, text="Enviar", command=cargarUrl).grid()


def cargarUrl():

    global v, newurl, emisorasUrl
    newUri = urlV.get()
    player.set_state(gst.STATE_NULL)
    player.set_property("uri", newUri)
    player.set_state(gst.STATE_PLAYING)
    v.set(None)
    newurl.destroy()


def listaUrl(new):

    player.set_state(gst.STATE_NULL)
    player.set_property("uri", new)
    player.set_state(gst.STATE_PLAYING)

def on_tag(bus, msg):

    taglist = msg.parse_tag()
    print 'on_tag:'
    for key in taglist.keys():
       print '\t%s = %s' % (key, taglist[key])


#crea una lista de reproduccion de la Url
player = gst.element_factory_make("playbin", "player")
player.set_property('uri', streamUri)



#listen for tags on the message bus; tag event might be called more than once
bus = player.get_bus()
bus.enable_sync_message_emission()
bus.add_signal_watch()
bus.connect('message::tag', on_tag)

#Botones de la ventana principal

#Play
play = Button(ventana, text="Play", width=10, highlightcolor="red", command=play)
play.grid(row=1)

#Pause
pause = Button(ventana, text="Pause", width=10, highlightcolor="red", command=pause)
pause.grid(row=2)

#Stop
stop = Button(ventana, text="Stop", width=10, highlightcolor="red", command=stop)
stop.grid(row=3, column=0)

#Reloj
reloj = Label(ventana, font=('times', 30, 'bold'), bg='red')
reloj.grid(row=2, column=1)

#Vol up
volUp = Button(ventana, text="Vol Up", width=10, highlightcolor="red", command=vol_up)
volUp.grid(row=1, column=3)

#Vol down
volDown = Button(ventana, text="Vol Down", width=10, highlightcolor="red", command=vol_down)
volDown.grid(row=2, column=3)

txtVol = Label(ventana, font=('times', 10, "bold"))
txtVol.grid(row=0, column=3)

# barra principal
barraMenu = Menu(ventana)

# Menu archivo
menuArchivo = Menu(barraMenu, tearoff=0)
menuArchivo.add_command(label="Abrir Url", command=abrirurl)
menuArchivo.add_separator()
menuArchivo.add_command(label="Salir", command=ventana.quit)
barraMenu.add_cascade(label="Archivo", menu=menuArchivo)

# Menu Emisoras
menuEmisoras = Menu(barraMenu, tearoff=0)
for emi, url in emisorasUrl:
    menuEmisoras.add_command(label=emi+" :  " + url, command= lambda  i=url: listaUrl(i))

barraMenu.add_cascade(label="Emisoras", menu=menuEmisoras)

#funcion para actualizar la hora y el volumen.
def hora():
    """muestra la hora actual"""

    tiempo2 = time.strftime('%H:%M:%S')
    tiempo = ''
    if tiempo2 != tiempo:
        tiempo = tiempo2
        reloj.config(text=tiempo)
    txtVol.config(text="Volumen: "+str(volume))
    reloj.after(100, hora)

#funcion para la seleccion de emisoras
def select():
    player.set_state(gst.STATE_NULL)
    if v.get() == 1:
        streamUri = 'http://playerservices.streamtheworld.com/api/livestream-redirect/SER_ALICANTE.mp3'
        player.set_property('uri', streamUri)
        player.set_state(gst.STATE_PLAYING)
    elif v.get() == 2:
        streamUri = 'http://stream-tx3.radioparadise.com/rp_96.ogg'
        player.set_property('uri', streamUri)
        player.set_state(gst.STATE_PLAYING)
    elif v.get() == 3:
        streamUri = 'rtmp://teledifusion.tv/teleelxradio/teleelxradiolive'
        player.set_property('uri', streamUri)
        player.set_state(gst.STATE_PLAYING)
    elif v.get() == 4:
        streamUri = 'mms://94.127.190.245/radioelche'
        player.set_property('uri', streamUri)
        player.set_state(gst.STATE_PLAYING)


v = IntVar()



def __main__():
    for emi, nume in emisoras:
        Radiobutton(ventana, text=emi, variable=v, command=select, val=nume).grid(column=1)
    player.set_state(gst.STATE_PLAYING)
    hora()

    ventana.mainloop()

player.set_state(gst.STATE_PLAYING)
v.set(2)
ventana.config(menu=barraMenu)
__main__()
