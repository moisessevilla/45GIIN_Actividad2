import uuid

from django.db import models


# Modelo para los pacientes
class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)  # Identificador único del paciente
    dni = models.CharField(unique=True, max_length=9)  # DNI del paciente
    nombre = models.CharField(max_length=100)  # Nombre del paciente
    apellido = models.CharField(max_length=100)  # Apellido del paciente
    email = models.CharField(unique=True, max_length=100)  # Correo único del paciente
    telefono = models.CharField(max_length=15, blank=True, null=True)  # Teléfono del paciente (opcional)
    contrasena = models.CharField(max_length=100)  # Contraseña del paciente

    class Meta:
        managed = False
        db_table = 'paciente'


# Modelo para los médicos
class Medico(models.Model):
    id_medico = models.AutoField(primary_key=True)  # Identificador único del médico
    ncolegiado = models.CharField(unique=True, max_length=8) # Número de colegiado del médico
    nombre = models.CharField(max_length=100)  # Nombre del médico
    especialidad = models.CharField(max_length=100)  # Especialidad del médico
    email = models.CharField(unique=True, max_length=100)  # Correo único del médico

    class Meta:
        managed = False
        db_table = 'medico'


# Modelo para las citas
class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True)  # Identificador único para cada cita
    id_paciente = models.ForeignKey('Paciente', models.DO_NOTHING, db_column='id_paciente')  # Relación con un paciente
    id_medico = models.ForeignKey('Medico', models.DO_NOTHING, db_column='id_medico')  # Relación con un médico
    fecha = models.DateField()  # Fecha de la cita
    hora = models.TimeField()  # Hora de la cita
    especialidad = models.CharField(max_length=100, null=True)  # Especialidad asociada
    estado = models.CharField(max_length=20, default='confirmada')
    refcita = models.CharField(max_length=12, unique=True, editable=False)

    def save(self, *args, **kwargs):
        # Generar refcita si no existe
        if not self.refcita:
            self.refcita = str(uuid.uuid4())[:12].replace('-', '').upper()
        super(Cita, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'cita'


# Modelo para los administradores del sistema
class Administrador(models.Model):
    id_admin = models.AutoField(primary_key=True)  # Identificador único para cada administrador
    nombre = models.CharField(max_length=100)  # Nombre del administrador
    correo = models.CharField(unique=True, max_length=100)  # Correo único del administrador

    class Meta:
        managed = False  # Indica que Django no gestionará esta tabla
        db_table = 'administrador'  # Nombre de la tabla en la base de datos


# Grupo de permisos (por defecto en Django)
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)  # Nombre único del grupo

    class Meta:
        managed = False
        db_table = 'auth_group'


# Relación entre grupos y permisos
class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)  # Relación con un grupo
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)  # Relación con un permiso

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)  # Clave única compuesta


# Modelo de permisos (por defecto en Django)
class AuthPermission(models.Model):
    name = models.CharField(max_length=255)  # Nombre del permiso
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)  # Código único para el permiso

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)  # Clave única compuesta


# Usuarios del sistema (por defecto en Django)
class AuthUser(models.Model):
    password = models.CharField(max_length=128)  # Contraseña cifrada
    last_login = models.DateTimeField(blank=True, null=True)  # Último inicio de sesión
    is_superuser = models.BooleanField()  # Indica si es un superusuario
    username = models.CharField(unique=True, max_length=150)  # Nombre de usuario único
    first_name = models.CharField(max_length=150)  # Nombre
    last_name = models.CharField(max_length=150)  # Apellido
    email = models.CharField(max_length=254)  # Correo electrónico
    is_staff = models.BooleanField()  # Indica si es parte del personal
    is_active = models.BooleanField()  # Indica si está activo
    date_joined = models.DateTimeField()  # Fecha de creación del usuario

    class Meta:
        managed = False
        db_table = 'auth_user'


# Relación entre usuarios y grupos
class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)  # Relación con un usuario
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)  # Relación con un grupo

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)  # Clave única compuesta


# Relación entre usuarios y permisos
class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)  # Relación con un usuario
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)  # Relación con un permiso

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)  # Clave única compuesta


# Modelo para registrar acciones administrativas
class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()  # Hora de la acción
    object_id = models.TextField(blank=True, null=True)  # Identificador del objeto afectado
    object_repr = models.CharField(max_length=200)  # Representación del objeto
    action_flag = models.SmallIntegerField()  # Tipo de acción
    change_message = models.TextField()  # Descripción de los cambios
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)  # Usuario que realizó la acción

    class Meta:
        managed = False
        db_table = 'django_admin_log'


# Modelo para los tipos de contenido en Django
class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)  # Nombre de la aplicación
    model = models.CharField(max_length=100)  # Nombre del modelo

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)  # Clave única compuesta


# Migraciones de Django
class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)  # Nombre de la aplicación
    name = models.CharField(max_length=255)  # Nombre de la migración
    applied = models.DateTimeField()  # Fecha de aplicación

    class Meta:
        managed = False
        db_table = 'django_migrations'


# Sesiones de usuarios en Django
class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)  # Clave única para la sesión
    session_data = models.TextField()  # Datos de la sesión
    expire_date = models.DateTimeField()  # Fecha de expiración

    class Meta:
        managed = False
        db_table = 'django_session'


# Modelo para el historial médico de pacientes
class Historialmedico(models.Model):
    id_historial_medico = models.AutoField(primary_key=True)  # Identificador único del historial
    id_paciente = models.ForeignKey('Paciente', models.DO_NOTHING, db_column='id_paciente')  # Relación con un paciente
    notas = models.TextField(blank=True, null=True)  # Notas del historial (opcional)
    ultima_actualizacion = models.DateTimeField(blank=True, null=True)  # Última actualización del historial

    class Meta:
        managed = False
        db_table = 'historialmedico'


# Modelo para las notificaciones
class Notificaciones(models.Model):
    id_notificacion = models.AutoField(primary_key=True)  # Identificador único de la notificación
    id_cita = models.ForeignKey(Cita, models.DO_NOTHING, db_column='id_cita')  # Relación con una cita
    tipo = models.CharField(max_length=50)  # Tipo de notificación (ejemplo: recordatorio)
    mensaje = models.TextField()  # Mensaje de la notificación
    fecha_envio = models.DateTimeField(blank=True, null=True)  # Fecha de envío (opcional)

    class Meta:
        managed = False
        db_table = 'notificaciones'


# Modelo para los roles en el sistema
class Roles(models.Model):
    id_rol = models.AutoField(primary_key=True)  # Identificador único del rol
    nombre_rol = models.CharField(max_length=50)  # Nombre del rol

    class Meta:
        managed = False
        db_table = 'roles'


# Relación entre usuarios y roles
class Usuariorol(models.Model):
    id_usuario = models.OneToOneField(Administrador, models.DO_NOTHING, db_column='id_usuario', primary_key=True)  # Relación con un administrador
    id_rol = models.ForeignKey(Roles, models.DO_NOTHING, db_column='id_rol')  # Relación con un rol

    class Meta:
        managed = False
        db_table = 'usuariorol'
        unique_together = (('id_usuario', 'id_rol'),)  # Clave única compuesta
