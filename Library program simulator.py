# Este código simula un programa de finanzas de una biblioteca (con dinero falso),incluyendo un juego de blackjack para entretenimiento.
# El precio de los libros es calculado en base al estado del libro (Bueno,Malo,No entregado) y método de pago (Tarjeta,Efectivo)

from sre_parse import State
from tkinter import PhotoImage, Label
import tkinter as tk  # Importacion de tkinter,la herramienta de interfaz grafica
import random

# Configuracion de ventana principal
app = tk.Tk()
app.attributes("-fullscreen", True)
app.title("Juego y Administracion") 
app.config(background="DarkSeaGreen")

# Creacion de listbox de info
listbox = tk.Listbox(app, width=80, height=15, background="black",fg="white" )
listbox.place(x=100,y=10) 

def blackjack(): # definicion de funcion blackjack para llamar despues
    ventana = tk.Toplevel(app)  # creacion de ventana de blackjack
    ventana.title("Blackjack") 
    dinero_blackjack = 1001

    label_blackjack = tk.Label(ventana,text=f"Dinero: {dinero_blackjack}")
    label_blackjack.grid(row=5, column=2)

    # estado (plantado/no plantado) de ambos
    total_jugad = 0  # puntos del jugador
    total_bot = 0  # puntos del bot
    jugador_plantado = False
    bot_plantado = False

    # creacion de labels que muestran los puntos y ultima accion del jugador y del bot
    num_jugad = tk.Label(ventana, text="Jugador: 0")
    num_jugad.grid(row=0, column=5)  # 

    num_bot = tk.Label(ventana, text="Bot: 0")
    num_bot.grid(row=0, column=3)

    acciones_bot = tk.Label(ventana, text="")
    acciones_bot.grid(row=1, column=3)

    acciones_jugad = tk.Label(ventana, text="")
    acciones_jugad.grid(row=2, column=3)

    estado = tk.Label(ventana, text="")
    estado.grid(row=0, column=2)

    # funcion de robar carta para jugador
    def robar_jugad():
        nonlocal total_jugad, dinero_blackjack # definicion de ambas variables como nonlocal para poder accederlas
        suma_carta_jugad = random.randint(1, 10)
        total_jugad += suma_carta_jugad  # suma la carta robada a los puntos del jugador
        num_jugad.config(text="Jugador: " + str(total_jugad))  # actualiza la label con un string cast del nuevo puntaje
        acciones_jugad.config(text=f"Jugador robo un {suma_carta_jugad}")

        # verifica si hay un ganador. si no,el bot sigue jugando
        if total_jugad > 21:
            estado.config(text="Perdiste. Te pasaste de 21")
            boton_robar.config(state="disabled")  
            boton_plantar.config(state="disabled")  
            dinero_blackjack = dinero_blackjack - 500
            label_blackjack.config(text=f"dinero: {dinero_blackjack}")
        elif total_jugad == 21:
            estado.config(text="Ganaste. Llegaste a 21")
            boton_robar.config(state="disabled")
            boton_plantar.config(state="disabled")
            dinero_blackjack = dinero_blackjack + 500
            label_blackjack.config(text=f"dinero: {dinero_blackjack}")

        else:
            jugada_bot()


    def plantar_jugad():
        nonlocal jugador_plantado, dinero_blackjack
        jugador_plantado = True
        estado.config(text=f"Te plantaste con {total_jugad}")
        boton_robar.config(state="disabled") 
        boton_plantar.config(state="disabled")
        boton_siguiente.grid(row=2, column=2)  # mostramos un boton para hacer al bot jugar a pesar de estar plantados
        acciones_jugad.config(text="Jugador se planto")
        if bot_plantado:  # si ambos estan plantados,evalua el ganador
            ganador = evaluar_ganador()
            estado.config(text=ganador)
            boton_siguiente.config(state="disabled")

    # Función para que el bot realice su jugada

    # definimos como juega el bot
    def jugada_bot():
        nonlocal total_bot, bot_plantado, dinero_blackjack
        if bot_plantado:  # Si el bot ya se ha plantado, no realiza ninguna acción
            return

        # Si el bot tiene una puntuación entre 18 y 21, se planta
        if 18 <= total_bot < 21:
            bot_plantado = True
            acciones_bot.config(text="Bot se planto")
            estado.config(text=f"Bot se planto con {total_bot}")
            boton_siguiente.config(state="disabled")
            if jugador_plantado and bot_plantado:# Si ambos se plantaron,evalua el ganador
                ganador = evaluar_ganador()
                estado.config(text=ganador)
            return
        # El bot roba una carta
        suma_carta_bot = random.randint(1, 10)
        total_bot += suma_carta_bot
        num_bot.config(text="Bot: " + str(total_bot))
        acciones_bot.config(text=f"Bot robo un {suma_carta_bot}")

        # termina el juego si el bot llega a 21 o se pasa
        if total_bot > 21:
            estado.config(text="Ganaste. Oponente se paso de 21")
            boton_siguiente.config(state="disabled")
            boton_robar.config(state="disabled")
            boton_plantar.config(state="disabled")
            dinero_blackjack = dinero_blackjack + 500
            label_blackjack.config(text=f"dinero: {dinero_blackjack}")
        elif total_bot == 21:
            estado.config(text="Perdiste. Oponente llego a 21")
            boton_siguiente.config(state="disabled")
            boton_robar.config(state="disabled")
            boton_plantar.config(state="disabled")
            bot_plantado = True
            dinero_blackjack = dinero_blackjack - 500
            label_blackjack.config(text=f"dinero: {dinero_blackjack}")

    # definimos como se evalua el ganador
    def evaluar_ganador():
        nonlocal dinero_blackjack
        dist_jugad = 21 - total_jugad if total_jugad <= 21 else 99  # calcula cuanto falta para llegar al 21. si se paso de 21 ponemos distancia 99
        dist_bot = 21 - total_bot if total_bot <= 21 else 99
        if dist_jugad < dist_bot:
            return f"Ganaste con un {total_jugad} contra {total_bot}"
            dinero_blackjack += 500
            label_blackjack.config(text=f"dinero: {dinero_blackjack}")
        elif dist_bot < dist_jugad:
            return f"Perdiste con un {total_jugad} contra {total_bot}"
            dinero_blackjack -= 500
            label_blackjack.config(text=f"dinero: {dinero_blackjack}")
        else:
            return f"Empate. Ambos con {total_jugad}"

    # funcion de reinicio
    def reiniciar_juego():
        nonlocal total_jugad, total_bot, jugador_plantado, bot_plantado
        total_jugad = 0  # reinicia los puntos de ambos
        total_bot = 0
        jugador_plantado = False  # desplanta a ambos si estaban plantados
        bot_plantado = False
        num_jugad.config(text="Jugador: 0")  # reiniciamos las labels al default
        num_bot.config(text="Bot: 0") 
        estado.config(text="")
        acciones_bot.config(text="")  
        acciones_jugad.config(text="")  
        boton_robar.config(state="normal")  # activamos el boton de robar y de plantarse
        boton_plantar.config(state="normal")
        boton_siguiente.grid_remove()  # removemos el boton de siguiente turno
        boton_siguiente.config(state="normal") 

    # creacion de botones del jugador
    boton_robar = tk.Button(ventana, text="Robar", command=robar_jugad)
    boton_robar.grid(row=3, column=2)

    boton_plantar = tk.Button(ventana, text="Plantarse", command=plantar_jugad)
    boton_plantar.grid(row=1, column=2)

    boton_siguiente = tk.Button(ventana, text="Siguiente", command=jugada_bot())

    boton_reiniciar = tk.Button(ventana, text="Reiniciar", command=reiniciar_juego)
    boton_reiniciar.grid(row=4, column=2)

    boton_robar = tk.Button(ventana, text="Robar", command=robar_jugad)
    boton_robar.grid(row=3, column=2)

    boton_plantar = tk.Button(ventana, text="Plantarse", command=plantar_jugad)
    boton_plantar.grid(row=1, column=2)

    boton_reiniciar = tk.Button(ventana, text="Reiniciar", command=reiniciar_juego)
    boton_reiniciar.grid(row=4, column=2)

# labels que muestran cuantos libros hay para prestar
cantlP1=0
label_cant1=tk.Label(app, text=cantlP1, background="papaya whip")
label_cant1.place(x=650, y=450)

cantlP2=0
label_cant2=tk.Label(app, text=cantlP2, background="papaya whip")
label_cant2.place(x=650, y=500)

cantlP3=3
label_cant3=tk.Label(app, text=cantlP3, background="papaya whip")
label_cant3.place(x=650, y=550)

cantlP4=5
label_cant4=tk.Label(app, text=cantlP4, background="papaya whip")
label_cant4.place(x=650, y=600)

# labels que muestran cuantos libros hay para vender
cantlV1=0
label_cantV1=tk.Label(app, text=cantlV1, background="papaya whip")
label_cantV1.place(x=1250, y=450)

cantlV2=0
label_cantV2=tk.Label(app, text=cantlV2, background="papaya whip")
label_cantV2.place(x=1250, y=500)

cantlV3=0
label_cantV3=tk.Label(app, text=cantlV3, background="papaya whip")
label_cantV3.place(x=1250, y=550)

cantlV4=1
label_cantV4=tk.Label(app, text=cantlV4, background="papaya whip")
label_cantV4.place(x=1250, y=600)


# labels de los nombres de categoria
label_cat1 = tk.Label(app, text="Nombre:", background="LemonChiffon2")
label_cat1.place(y=400, x=10)

label_cat2 = tk.Label(app, text="Estado:", background="LemonChiffon2")
label_cat2.place(y=400, x=150)

label_cat3 = tk.Label(app, text="Precio:", background="LemonChiffon2")
label_cat3.place(y=400, x=400)

label_cat4 = tk.Label(app, text="dias de prestamo:", background="LemonChiffon2")
label_cat4.place(y=400, x=275)

label_cat5 = tk.Label(app, text="cantidad de presta:", background="LemonChiffon2")
label_cat5.place(y=400, x=600)

label_cat6 = tk.Label(app, text="prestar libro:", background="LemonChiffon2")
label_cat6.place(y=400, x=710)

label_cat7 = tk.Label(app, text="forma de pago:", background="LemonChiffon2")
label_cat7.place(y=400, x=490)

label_cat8 = tk.Label(app, text="reponer libro:", background="LemonChiffon2")
label_cat8.place(y=400, x=800)

label_cat9 = tk.Label(app, text="precio a reponer:", background="LemonChiffon2")
label_cat9.place(y=400, x=900)

label_cat10 = tk.Label(app, text="vender libro:", background="LemonChiffon2")
label_cat10.place(y=400, x=1010)

label_cat11 = tk.Label(app, text="precio de venta:", background="LemonChiffon2")
label_cat11.place(y=400, x=1110)

label_cat12 = tk.Label(app, text="cantidad a vender:", background="LemonChiffon2")
label_cat12.place(y=400, x=1210)

dinero=1000

dinero_label=tk.Label(app, text=f"{dinero}$", background="green2")
dinero_label.place(x=100, y=300)

dinero_label_nom=tk.Label(app, text="tu dinero: ",  background="green2")
dinero_label_nom.place(x=20, y=300)

# labels que muestran los precios de prestamo de los libros
label_p1 = tk.Label(app, text="2000$xDIA", background="aquamarine2")
label_p1.place(x=400, y=450)

label_p2 = tk.Label(app, text="5000$xDIA", background="aquamarine2")
label_p2.place(x=400, y=500)

label_p3 = tk.Label(app, text="1500$xDIA", background="aquamarine2")
label_p3.place(x=400, y=550)

label_p4 = tk.Label(app, text="1000$xDIA", background="aquamarine2")
label_p4.place(x=400, y=600)

# labels que muestran cuanto cuesta reponer cada libro
label_com1=tk.Label(app, text="reponer: 20000$", background="indian red")
label_com1.place(x=900, y=450)

label_com2=tk.Label(app, text="reponer: 50000$", background="indian red")
label_com2.place(x=900, y=500)

label_com3=tk.Label(app, text="reponer: 15000$", background="indian red")
label_com3.place(x=900, y=550)

label_com4=tk.Label(app, text="reponer: 10000$", background="indian red")
label_com4.place(x=900, y=600)

# labels que muestran el precio de vender un libro
label_ven1=tk.Label(app, text="vender: 30000$", background="medium sea green")
label_ven1.place(x=1110, y=450)

label_ven2=tk.Label(app, text="vender: 60000$", background="medium sea green")
label_ven2.place(x=1110, y=500)

label_ven3=tk.Label(app, text="vender: 25000$", background="medium sea green")
label_ven3.place(x=1110, y=550)

label_ven4=tk.Label(app, text="vender: 20000$", background="medium sea green")
label_ven4.place(x=1110, y=600)

# variables del estado de los libros
estado1 = tk.StringVar(app)
estado1.set("Estado")

estado2 = tk.StringVar(app)
estado2.set("Estado")

estado3 = tk.StringVar(app)
estado3.set("Estado")

estado4 = tk.StringVar(app)
estado4.set("Estado")

# variables de metodo de pago
estado5 = tk.StringVar(app)
estado5.set("Pago")

estado6 = tk.StringVar(app)
estado6.set("Pago")

estado7 = tk.StringVar(app)
estado7.set("Pago")

estado8 = tk.StringVar(app)
estado8.set("Pago")

# menu para seleccionar metodo de pago
option_pago1 = tk.OptionMenu(app, estado5, "Efectivo", "Tarjeta")
option_pago1.place(x=500, y=450)
option_pago1.config(background="turquoise2", activebackground="turquoise4")

option_pago2 = tk.OptionMenu(app, estado6, "Efectivo", "Tarjeta")
option_pago2.place(x=500, y=500)
option_pago2.config(background="turquoise2", activebackground="turquoise4")

option_pago3 = tk.OptionMenu(app, estado7, "Efectivo", "Tarjeta")
option_pago3.place(x=500, y=550)
option_pago3.config(background="turquoise2", activebackground="turquoise4")

option_pago4 = tk.OptionMenu(app, estado8, "Efectivo", "Tarjeta")
option_pago4.place(x=500, y=600)
option_pago4.config(background="turquoise2", activebackground="turquoise4")

# menu para seleccionar el estado del libro
option_estado1 = tk.OptionMenu(app, estado1, "Bueno", "Malo", "No entregado")
option_estado1.place(x=150, y=450)
option_estado1.config(background="thistle3", activebackground="thistle3")

option_estado2 = tk.OptionMenu(app, estado2, "Bueno", "Malo", "No entregado")
option_estado2.place(x=150, y=500)
option_estado2.config(background="thistle3", activebackground="thistle3")

option_estado3 = tk.OptionMenu(app, estado3, "Bueno", "Malo", "No entregado")
option_estado3.place(x=150, y=550)
option_estado3.config(background="thistle3", activebackground="thistle3")

option_estado4 = tk.OptionMenu(app, estado4, "Bueno", "Malo", "No entregado")
option_estado4.place(x=150, y=600)
option_estado4.config(background="thistle3", activebackground="thistle3")

# labels de nombres de libros
label1 = tk.Label(app, text="La liga de los pelirrojos", background="salmon3")
label1.place(x=10, y=450)

label2 = tk.Label(app, text="La guerra de los yacares", background="salmon3")
label2.place(x=10, y=500)

label3 = tk.Label(app, text="El patito feo", background="salmon3")
label3.place(x=10, y=550)

label4 = tk.Label(app, text="El principito", background="salmon3")
label4.place(x=10, y=600)

# inputs de dias de prestamo
entry1 = tk.Entry(app, width=10)
entry1.place(x=300, y=450)

entry2 = tk.Entry(app, width=10)
entry2.place(x=300, y=500)

entry3 = tk.Entry(app, width=10)
entry3.place(x=300, y=550)

entry4 = tk.Entry(app, width=10)
entry4.place(x=300, y=600)

# guarda la posicion de cada libro en el listbox
libros_indices = {}

def reponer_libro1():
    global cantlV1, dinero
    cantlV1 = cantlV1 + 1
    dinero = dinero - 20000
    label_cantV1.config(text=cantlV1)
    dinero_label.config(text=dinero)

def reponer_libro2():
    global cantlV2, dinero
    cantlV2 = cantlV2 + 1
    dinero = dinero - 20000
    label_cantV2.config(text=cantlV2)
    dinero_label.config(text=dinero)

def reponer_libro3():
    global cantlV3, dinero
    cantlV3 = cantlV3 + 1
    dinero = dinero - 20000
    label_cantV3.config(text=cantlV3)
    dinero_label.config(text=dinero)

def reponer_libro4():
    global cantlV4, dinero
    cantlV4 = cantlV4 + 1
    dinero = dinero - 20000
    label_cantV4.config(text=cantlV4)
    dinero_label.config(text=dinero)

def vender_libro1():
    global cantlV1, dinero
    cantlV1 = cantlV1 - 1
    dinero = dinero + 30000
    label_cantV1.config(text=cantlV1)
    dinero_label.config(text=dinero)    


def vender_libro2():
    global cantlV2, dinero
    cantlV2 = cantlV2 - 1
    dinero = dinero + 30000
    label_cantV2.config(text=cantlV2)
    dinero_label.config(text=dinero)

def vender_libro3():
    global cantlV3, dinero
    cantlV3 = cantlV3 - 1
    dinero = dinero + 30000
    label_cantV3.config(text=cantlV3)
    dinero_label.config(text=dinero)

def vender_libro4():
    global cantlV4, dinero
    cantlV4 = cantlV4 - 1
    dinero = dinero + 30000
    label_cantV4.config(text=cantlV4)
    dinero_label.config(text=dinero)


# calculo de precio de libros
def guardar_libro1():
    global dinero, cantlP1
    if estado1.get() == "Estado":
        return
    if estado1.get() == "Bueno":
        preciot1 = 2000 * int(entry1.get()) if entry1.get().isdigit() else 0
    if estado1.get() == "No entregado":
        precio1 = 2000 * int(entry1.get()) if entry1.get().isdigit() else 0
        descuento1 = precio1 * 50 / 100
        preciot1 = 2000 * int(entry1.get()) - descuento1 if entry1.get().isdigit() else 0
    if estado1.get() == "Malo":
        precio1 = 2000 * int(entry1.get()) if entry1.get().isdigit() else 0
        descuento1 = precio1 * 10 / 100
        preciot1 = 2000 * int(entry1.get()) - descuento1 if entry1.get().isdigit() else 0
    if estado5.get() == "Tarjeta":
        descuentoP1 = preciot1 * 20 / 100
        precioPt1 = preciot1 - descuentoP1
    if estado5.get() == "Efectivo":
     precioPt1 = preciot1
    if estado5.get() == "Pago":
        return
    dinero += precioPt1
    dinero_label.config(text=dinero)
    cantlP1 = cantlP1 - 1
    label_cant1.config(text=cantlP1)
    texto = f"La liga de los pelirrojos - Estado: {estado1.get()} - dias de prestamo: {entry1.get()} - precio: {precioPt1}"
    listbox.insert(tk.END, texto)


def guardar_libro2():
    global dinero, cantlP2
    if estado2.get() == "Estado":
        return
    if estado2.get() == "Bueno":
        preciot2 = 5000 * int(entry2.get()) if entry2.get().isdigit() else 0
    if estado2.get() == "No entregado":
        precio2 = 5000 * int(entry2.get()) if entry2.get().isdigit() else 0
        descuento2 = precio2 * 50 / 100
        preciot2 = 5000 * int(entry2.get()) - descuento2 if entry2.get().isdigit() else 0
    if estado2.get() == "Malo":
        precio2 = 5000 * int(entry2.get()) if entry2.get().isdigit() else 0
        descuento2 = precio2 * 10 / 100
        preciot2 = 5000 * int(entry2.get()) - descuento2 if entry2.get().isdigit() else 0
    if estado6.get() == "Tarjeta":
        descuentoP2 = preciot2 * 20 / 100
        precioPt2 = preciot2 - descuentoP2
    if estado6.get() == "Efectivo":
     precioPt2 = preciot2
    if estado6.get() == "Pago":
        return
    dinero += precioPt2
    dinero_label.config(text=dinero)
    cantlP2 -= 1
    label_cant2.config(text=cantlP2)

    texto = f"La guerra de los yacares - Estado: {estado2.get()} - dias de prestamo: {entry2.get()} - precio: {precioPt2}"
    listbox.insert(tk.END, texto)

# Función para guardar la información del libro 3
def guardar_libro3():
    global dinero, cantlP3
    if estado3.get() == "Estado":
        return
    if estado3.get() == "Bueno":
        preciot3 = 1500 * int(entry3.get()) if entry3.get().isdigit() else 0
    if estado3.get() == "No entregado":
        precio3 = 1500 * int(entry3.get()) if entry3.get().isdigit() else 0
        descuento3 = precio3 * 50 / 100
        preciot3 = 1500 * int(entry3.get()) - descuento3 if entry3.get().isdigit() else 0
    if estado3.get() == "Malo":
        precio3 = 1500 * int(entry3.get()) if entry3.get().isdigit() else 0
        descuento3 = precio3 * 10 / 100
        preciot3 = 1500 * int(entry3.get()) - descuento3 if entry3.get().isdigit() else 0
    if estado7.get() == "Tarjeta":
        descuentoP3 = preciot3 * 20 / 100
        precioPt3 -= descuentoP3
    if estado7.get() == "Efectivo":
     precioPt3 = preciot3
    if estado7.get() == "Pago":
        return
    dinero+=precioPt3
    dinero_label.config(text=dinero)
    cantlP3 -= 1
    label_cant3.config(text=cantlP3)

    texto = f"El patito feo - Estado: {estado3.get()} - dias de prestamo: {entry3.get()} - precio: {precioPt3}"
    listbox.insert(tk.END, texto)


def guardar_libro4():
    global dinero, cantlP4
    if estado4.get() == "Estado":
        return
    if estado4.get() == "Bueno":
        preciot4 = 1000 * int(entry4.get()) if entry4.get().isdigit() else 0
    if estado4.get() == "No entregado":
        precio4 = 1000 * int(entry4.get()) if entry4.get().isdigit() else 0
        descuento4 = precio4 * 50 / 100
        preciot4 = 1000 * int(entry4.get()) - descuento4 if entry4.get().isdigit() else 0
    if estado4.get() == "Malo":
        precio4 = 1000 * int(entry4.get()) if entry4.get().isdigit() else 0
        descuento4 = precio4 * 10 / 100
        preciot4 = 1000 * int(entry4.get()) - descuento4 if entry4.get().isdigit() else 0
    if estado8.get() == "Tarjeta":
        descuentoP4 = preciot4 * 20 / 100
        precioPt4 = preciot4 - descuentoP4
    if estado8.get() == "Efectivo":
     precioPt4 = preciot4
    if estado8.get() == "Pago":
        return
    dinero+=precioPt4
    dinero_label.config(text=dinero)
    cantlP4 -= 1
    label_cant4.config(text=cantlP4)
    texto = f"El principito - Estado: {estado4.get()} - dias de prestamo: {entry4.get()} - precio: {precioPt4}"
    listbox.insert(tk.END, texto)

# Botones para guardar la información de cada libro
boton1 = tk.Button(app, text="Prestar libro 1", command=guardar_libro1, background="pale green")
boton1.place(x=700, y=450)

boton2 = tk.Button(app, text="Prestar libro 2", command=guardar_libro2, background="pale green")
boton2.place(x=700, y=500)

boton3 = tk.Button(app, text="Prestar libro 3", command=guardar_libro3, background="pale green")
boton3.place(x=700, y=550)

boton4 = tk.Button(app, text="Prestar libro 4", command=guardar_libro4, background="pale green")
boton4.place(x=700, y=600)

boton_com1=tk.Button(app, text="reponer libro 1", command=reponer_libro1, background="salmon1")
boton_com1.place(x=800, y=450)

boton_com2=tk.Button(app, text="reponer libro 2", command=reponer_libro2, background="salmon1")
boton_com2.place(x=800, y=500)

boton_com3=tk.Button(app, text="reponer libro 3", command=reponer_libro3, background="salmon1")
boton_com3.place(x=800, y=550)

boton_com4=tk.Button(app, text="reponer libro 4", command=reponer_libro4, background="salmon1")
boton_com4.place(x=800, y=600)

boton_ven1=tk.Button(app, text="vender libro 1", command=vender_libro1, background="green yellow")
boton_ven1.place(x=1010, y=450)

boton_ven2=tk.Button(app, text="vender libro 2", command=vender_libro2, background="green yellow")
boton_ven2.place(x=1010, y=500)

boton_ven3=tk.Button(app, text="vender libro 3", command=vender_libro3, background="green yellow")
boton_ven3.place(x=1010, y=550)

boton_ven4=tk.Button(app, text="vender libro 4", command=vender_libro4, background="green yellow")
boton_ven4.place(x=1010, y=600)

# labels para mostrar los descuentos
label_des = tk.Label(app, text="Descuento:", background="DarkOliveGreen2")
label_des.place(x=10, y=640)

label_desc1 = tk.Label(app, text="No entregado:50%", background="DarkOliveGreen2")
label_desc1.place(x=10, y=665)

label_desc2 = tk.Label(app, text="Malo:10%", background="DarkOliveGreen2")
label_desc2.place(x=10, y=690)

label_desc3 = tk.Label(app, text="Tarjeta:20%", background="DarkOliveGreen2")
label_desc3.place(x=10, y=715)

# funciones para pasar libros de venta a libros de prestamo
def venta_a_presta1():
    global cantlP1, cantlV1
    cantlV1=cantlV1 - 1
    cantlP1=cantlP1+1
    label_cant1.config(text=cantlP1)
    label_cantV1.config(text=cantlV1)

def venta_a_presta2():
    global cantlP2, cantlV2
    cantlV2=cantlV2 - 1
    cantlP2=cantlP2+1
    label_cant2.config(text=cantlP2)
    label_cantV2.config(text=cantlV2)

def venta_a_presta3():
    global cantlP3, cantlV3
    cantlV3=cantlV3 - 1
    cantlP3=cantlP3+1
    label_cant3.config(text=cantlP3)
    label_cantV3.config(text=cantlV3)

def venta_a_presta4():
    global cantlP4, cantlV4
    cantlV4=cantlV4 - 1
    cantlP4=cantlP4+1
    label_cant4.config(text=cantlP4)
    label_cantV4.config(text=cantlV4)

boton_presta_venta1=tk.Button(app, text="pasar a prestar", command=venta_a_presta1)
boton_presta_venta1.place(x=1280, y=450)

boton_presta_venta2=tk.Button(app, text="pasar a prestar", command=venta_a_presta2)
boton_presta_venta2.place(x=1280, y=500)

boton_presta_venta3=tk.Button(app, text="pasar a prestar", command=venta_a_presta3)
boton_presta_venta3.place(x=1280, y=550)

boton_presta_venta4=tk.Button(app, text="pasar a prestar", command=venta_a_presta4)
boton_presta_venta4.place(x=1280, y=600)

def revisar_dinero1():
    if dinero < 20000:
        boton_com1.config(state="disabled")  # si no hay suficiente dinero para reponer un libro,se desactiva el boton
    else:
        boton_com1.config(state="normal")  # si hay suficiente dinero,se reactiva
    app.after(1, revisar_dinero1)

def revisar_dinero2():
    if dinero < 50000:
        boton_com2.config(state="disabled") 
    else:
        boton_com2.config(state="normal")  
    app.after(1, revisar_dinero2)

def revisar_dinero3():
    if dinero < 15000:
        boton_com3.config(state="disabled") 
    else:
        boton_com3.config(state="normal")  
    app.after(1, revisar_dinero3)

def revisar_dinero4():
    if dinero < 10000:
        boton_com4.config(state="disabled") 
    else:
        boton_com4.config(state="normal")  
    app.after(1, revisar_dinero4)


def revisar_cant1():
    if cantlP1 < 1:
        boton1.config(state="disabled")  # si no hay libros,el boton de vender/prestar libros se desactiva
    else:
        boton1.config(state="normal")
    app.after(1, revisar_cant1)

def revisar_cant2():
    if cantlP2 < 1:
        boton2.config(state="disabled")  
    else:
        boton2.config(state="normal")
    app.after(1, revisar_cant2)

def revisar_cant3():
    if cantlP3 < 1:
        boton3.config(state="disabled")
    else:
        boton3.config(state="normal")
    app.after(1, revisar_cant3)

def revisar_cant4():
    if cantlP4 < 1:
        boton4.config(state="disabled")
    else:
        boton4.config(state="normal")
    app.after(1, revisar_cant4)


def revisar_cantV1():
    if cantlV1 < 1:
        boton_ven1.config(state="disabled")
        boton_presta_venta1.config(state="disabled")
    else:
        boton_ven1.config(state="normal")
        boton_presta_venta1.config(state="normal")
    app.after(3, revisar_cantV1)

def revisar_cantV2():
    if cantlV2 < 1:
        boton_ven2.config(state="disabled") 
        boton_presta_venta2.config(state="disabled")

    else:
        boton_ven2.config(state="normal")
        boton_presta_venta2.config(state="normal")
    app.after(3, revisar_cantV2)

def revisar_cantV3():
    if cantlV3 < 1:
        boton_ven3.config(state="disabled")
        boton_presta_venta3.config(state="disabled")
    else:
      boton_ven3.config(state="normal")
      boton_presta_venta3.config(state="normal")
    app.after(3, revisar_cantV3)

def revisar_cantV4():
    if cantlV4 < 1:
        boton_ven4.config(state="disabled")
        boton_presta_venta4.config(state="disabled")
    else:
        boton_ven4.config(state="normal")
        boton_presta_venta4.config(state="normal")
    app.after(3, revisar_cantV4)


# funcion para eliminar un elemento de la listbox
def eliminar_seleccionado():
    seleccion = listbox.curselection()
    if seleccion:
        idx = seleccion[0]
        listbox.delete(idx)

# definimos la funcion de pagar una mensualidad
def pagar_mensualidad():
    global dinero
    dinero= dinero - 400000
    dinero_label.config(text=dinero)

boton_pagar_m=tk.Button(app, text="Pagar mensualidad", command=pagar_mensualidad, background="gold2", activebackground="red3")
boton_pagar_m.place(x=875, y=350) 

label_pagar_m=tk.Label(app, text="Pagar mensualidad: 400000$", background="gold2")
label_pagar_m.place(x=1010, y=350) 


#boton para funcion eliminar seleccionado
boton_eliminar = tk.Button(app, text="Eliminar seleccionado", command=eliminar_seleccionado, background="tomato", activebackground="HotPink2")
boton_eliminar.place(x=600, y=200)

# menu desplegable para abrir el blackjack
barra_menus = tk.Menu(app)
archivo_menu = tk.Menu(barra_menus, tearoff=0)
archivo_menu.add_command(label="Blackjack", command=blackjack)
barra_menus.add_cascade(label="Blackjack", menu=archivo_menu)
app.config(menu=barra_menus)

# le decimos al programa donde encontrar el logo (si no está descargada la imagen o no está en esa dirección tira error)
ima = PhotoImage(file="C:/Users/Usuario/Downloads/Library progarm simulator project/DMP.png") 

label_photo = Label(app, image=ima) # creamos un label que muestre la imagen
label_photo.place(x=800, y=10)

# cada bucle el programa va a revisar la cantidad de libros disponibles para vender,prestar,y el dinero disponible.
revisar_cantV1()
revisar_cantV2() 
revisar_cantV3() 
revisar_cantV4() 
revisar_cant1() 
revisar_cant2() 
revisar_cant3() 
revisar_cant4()  
revisar_dinero1()  
revisar_dinero2()  
revisar_dinero3()  
revisar_dinero4()  

app.mainloop() 
