-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS ConsultorioMedico;
USE ConsultorioMedico;

-- Crear la tabla Paciente
CREATE TABLE Paciente (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    contrasena VARCHAR(100) NOT NULL
);

-- Crear la tabla Medico
CREATE TABLE Medico (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL
);

-- Crear la tabla Cita
CREATE TABLE Cita (
    id_cita INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    especialidad VARCHAR(100),
    estado ENUM('confirmada', 'cancelada', 'reprogramada') NOT NULL DEFAULT 'confirmada',
    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente) ON DELETE CASCADE,
    FOREIGN KEY (id_medico) REFERENCES Medico(id_medico) ON DELETE CASCADE
);

-- Crear la tabla HistorialMedico
CREATE TABLE HistorialMedico (
    id_historial_medico INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    notas TEXT,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente) ON DELETE CASCADE
);

-- Crear la tabla Administrador
CREATE TABLE Administrador (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL
);

-- Crear la tabla Notificaciones
CREATE TABLE Notificaciones (
    id_notificacion INT AUTO_INCREMENT PRIMARY KEY,
    id_cita INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    mensaje TEXT NOT NULL,
    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cita) REFERENCES Cita(id_cita) ON DELETE CASCADE
);

-- Crear la tabla Roles
CREATE TABLE Roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL
);

-- Crear la tabla UsuarioRol
CREATE TABLE UsuarioRol (
    id_usuario INT NOT NULL,
    id_rol INT NOT NULL,
    PRIMARY KEY (id_usuario, id_rol),
    FOREIGN KEY (id_usuario) REFERENCES Administrador(id_admin) ON DELETE CASCADE,
    FOREIGN KEY (id_rol) REFERENCES Roles(id_rol) ON DELETE CASCADE
);