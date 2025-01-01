from graphviz import Digraph
from PIL import Image

# Crear el diagrama de clases UML
class_diagram = Digraph('Diagrama_Clases_Consultorio', format='png')
class_diagram.attr(rankdir='TB', size='1')  # Ajustar tamaño general del diagrama
class_diagram.attr(dpi='2400')  # Incrementar la resolución para que sea más claro

# Definir las clases
class_diagram.node('Paciente', shape='record', label="""{
    Paciente|
    - id_paciente: SERIAL\\l
    - nombre: VARCHAR(100)\\l
    - apellido: VARCHAR(100)\\l
    - email: VARCHAR(100)\\l
    - telefono: VARCHAR(15)\\l
    - contrasena: VARCHAR(100)\\l|
    + registrarse(): void\\l
    + iniciarSesion(email: string, contrasena: string): void\\l
}""")

class_diagram.node('Medico', shape='record', label="""{
    Medico|
    - id_medico: SERIAL\\l
    - nombre: VARCHAR(100)\\l
    - especialidad: VARCHAR(100)\\l
    - correo: VARCHAR(100)\\l|
    + gestionarCitas(idCita: INT): void\\l
    + actualizarHistorial(idHistorial: INT): void\\l
}""")

class_diagram.node('Cita', shape='record', label="""{
    Cita|
    - id_cita: SERIAL\\l
    - id_paciente: INT\\l
    - id_medico: INT\\l
    - fecha: DATE\\l
    - hora: TIME\\l
    - especialidad: VARCHAR(100)\\l
    - estado: VARCHAR(20)\\l|
    + crearCita(cita: Cita): void\\l
    + modificar(idCitaModificar: INT): void\\l
    + eliminarCita(idCitaEliminar: INT): void\\l
}""")

class_diagram.node('HistorialMedico', shape='record', label="""{
    HistorialMedico|
    - id_historial_medico: SERIAL\\l
    - id_paciente: INT\\l
    - notas: TEXT\\l
    - ultima_actualizacion: TIMESTAMP\\l|
    + consultar(cadenaBusqueda: string): list\\l
    + actualizar(): void\\l
    + registrarNota(nuevaNota: string): void\\l
    + listarNotas(): list\\l
}""")

class_diagram.node('Administrador', shape='record', label="""{
    Administrador|
    - id_admin: SERIAL\\l
    - nombre: VARCHAR(100)\\l
    - correo: VARCHAR(100)\\l|
    + gestionarUsuarios(rol: Roles): void\\l
}""")

class_diagram.node('Notificaciones', shape='record', label="""{
    Notificaciones|
    - id_notificacion: SERIAL\\l
    - id_cita: INT\\l
    - tipo: VARCHAR(50)\\l
    - mensaje: TEXT\\l
    - fecha_envio: TIMESTAMP\\l|
    + enviarNotificacion(idCita: INT): void\\l
}""")

class_diagram.node('Roles', shape='record', label="""{
    Roles|
    - id_rol: SERIAL\\l
    - nombre_rol: VARCHAR(50)\\l
}""")

class_diagram.node('UsuarioRol', shape='record', label="""{
    UsuarioRol|
    - id_usuario: INT\\l
    - id_rol: INT\\l
}""")

# Relacionar las clases
class_diagram.edge('Paciente', 'Cita', label='1:N', arrowhead='vee')
class_diagram.edge('Cita', 'Medico', label='N:1', arrowhead='vee')
class_diagram.edge('Cita', 'Notificaciones', label='1:1', arrowhead='vee')
class_diagram.edge('Paciente', 'HistorialMedico', label='1:N', arrowhead='vee')
class_diagram.edge('Medico', 'HistorialMedico', label='1:N', arrowhead='vee')
class_diagram.edge('Administrador', 'UsuarioRol', label='1:N', arrowhead='vee')
class_diagram.edge('Roles', 'UsuarioRol', label='1:N', arrowhead='vee')

# Guardar y renderizar el diagrama
output_path = class_diagram.render('diagrama_clases', format='png', cleanup=True)
print("El diagrama ha sido generado como 'diagrama_clases.png'")

# Mostrar el diagrama en pantalla
image = Image.open(output_path)
image.show()
