import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow, Rectangle

# Crear la figura
fig, ax = plt.subplots(figsize=(10, 6))

# Servidor de Aplicaciones
ax.add_patch(Rectangle((2, 6), 4, 2, edgecolor='black', facecolor='#CDEAFF', label="Servidor de Aplicaciones"))
ax.text(4, 7, "Django App", ha='center', va='center', fontsize=10)

# Base de Datos
ax.add_patch(Rectangle((8, 6), 4, 2, edgecolor='black', facecolor='#FFCFCF', label="Base de Datos"))
ax.text(10, 7, "PostgreSQL", ha='center', va='center', fontsize=10)

# Cliente Web
ax.add_patch(Rectangle((2, 1), 4, 2, edgecolor='black', facecolor='#CFFFD2', label="Cliente Web"))
ax.text(4, 2, "Frontend\n(Browser)", ha='center', va='center', fontsize=10)

# Flechas de interacción
ax.add_patch(FancyArrow(4, 6, 0, -2, width=0.2, head_width=0.4, head_length=0.3, color='black'))
ax.add_patch(FancyArrow(6, 6, 2, 0, width=0.2, head_width=0.4, head_length=0.3, color='black'))
ax.add_patch(FancyArrow(8, 7, -2, 0, width=0.2, head_width=0.4, head_length=0.3, color='black'))

# Etiquetas
ax.text(5.2, 4.5, "Solicitudes HTTP\nREST API", ha='center', va='center', fontsize=10, color='blue')
ax.text(9, 6.5, "Consultas SQL", ha='center', va='center', fontsize=10, color='blue')

# Ajustes generales
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis('off')  # Ocultar los ejes

plt.title("Diagrama de Arquitectura Básica", fontsize=14)

# Guardar el diagrama como PNG
plt.savefig('diagrama_arquitectura.png', format='png', dpi=300)
print("El diagrama ha sido generado como 'diagrama_arquitectura.png'")

# Mostrar el diagrama
plt.show()
