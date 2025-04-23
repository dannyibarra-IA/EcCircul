import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# --- Configuración de la app ---
st.title("Simulador de Flujo Circular de Materiales")
st.markdown("""
Este simulador permite explorar el comportamiento de un sistema de economía circular 
con materia prima, inventario de productos y material reciclable. Puedes ajustar la eficiencia,
capacidad de reciclaje y activar una crisis de materia prima.
""")

# --- Parámetros de entrada ---
eficiencia = st.slider("Eficiencia de reciclaje", 0.1, 1.0, 0.6, step=0.05)
capacidad_inicial = st.slider("Capacidad de reciclaje", 5, 30, 10)
crisis = st.checkbox("Activar crisis de materia prima virgen desde t=40")

# --- Parámetros fijos del sistema ---
Tasa_transformacion = 0.1
Tasa_perdida_MP = 0.05
Tasa_ventas = 0.1
Tasa_perdida_IP = 0.02
Ingreso_MP_virgen = 20
Tasa_disposicion = 0.1

y0 = [100, 50, 30]  # MP (Materia Prima), IP (Inventario de Productos), MR (Material Reciclable)
t = np.linspace(0, 100, 200)

# --- Modelo dinámico ---
def modelo(y, t):
    MP, IP, MR = y

    Transformacion = Tasa_transformacion * MP
    Perdida_MP = Tasa_perdida_MP * MP
    Ventas = Tasa_ventas * IP
    Perdida_IP = Tasa_perdida_IP * IP

    capacidad_actual = capacidad_inicial if t < 30 else capacidad_inicial * 2
    Transformacion_Reciclaje = min(MR, capacidad_actual) * eficiencia
    Disposicion = Tasa_disposicion * MR

    Ingreso_MP_virgen_local = Ingreso_MP_virgen if not crisis or t < 40 else Ingreso_MP_virgen * 0.2
    Ingreso_MP = Ingreso_MP_virgen_local + Transformacion_Reciclaje

    dMPdt = Ingreso_MP - Transformacion - Perdida_MP
    dIPdt = Transformacion - Ventas - Perdida_IP
    dMRdt = Ventas + Perdida_MP + Perdida_IP - Transformacion_Reciclaje - Disposicion

    return [dMPdt, dIPdt, dMRdt]

# --- Simulación ---
sol = odeint(modelo, y0, t)
MP, IP, MR = sol.T

# --- Visualización ---
fig, ax = plt.subplots()
ax.plot(t, MP, label='Materia Prima')
ax.plot(t, IP, label='Inventario de Productos')
ax.plot(t, MR, label='Material Reciclable')
ax.set_xlabel('Tiempo')
ax.set_ylabel('Cantidad')
ax.set_title('Dinámica del Sistema Circular')
ax.legend()
st.pyplot(fig)
