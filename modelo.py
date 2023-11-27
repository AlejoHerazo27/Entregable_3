import os 
from PyQt5.QtWidgets import QMessageBox
import pydicom
from PyQt5.QtGui import QImage
import numpy as np

class User(object):
    def __init__(self):
        self.__usuarios = {}
        self.__usuarios['bio12345'] = 'medicoAnalitico'
        
    def verificarUsuario(self, u, c):
        try:
            if self.__usuarios[c] == u:
                return True
            else:
                return False
        except:
            return False
        
    def cargar_senal(self, ruta_carpeta):
        rutas_archivos_dcm = []
        archivos_en_carpeta = os.listdir(ruta_carpeta)
        
        for archivo in archivos_en_carpeta:
            ruta_archivo = os.path.join(ruta_carpeta, archivo)
            rutas_archivos_dcm.append(ruta_archivo)
        if os.path.isfile(ruta_archivo) and archivo.lower().endswith('.dcm'):
            self.__rutas = rutas_archivos_dcm
            return rutas_archivos_dcm
        else:
            print("Formato no válido.")

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Resultado")
            msg.setText("Archivo no valido")
            msg.show()        

    def obtener_info_dicom(self, ruta_archivo):
        archivo_dicom = pydicom.dcmread(ruta_archivo)

        nombre_paciente = getattr(archivo_dicom, 'PatientName', 'No disponible')
        sexo_paciente = getattr(archivo_dicom, 'PatientSex', 'No disponible')
        edad_paciente = getattr(archivo_dicom, 'PatientAge', 'No disponible')
        fecha_estudio = getattr(archivo_dicom, 'StudyDate', 'No disponible')
        peso_paciente = getattr(archivo_dicom, 'PatientWeight', 'No disponible')
        
        return {
            'Nombre': nombre_paciente,
            'Sexo': sexo_paciente,
            'Edad': edad_paciente,
            'FechaEstudio': fecha_estudio,
            'Peso': peso_paciente,
        }
       
    def R_dicom(self,x):
        z=pydicom.dcmread(x)
        matriz=z.pixel_array
        matriz = (matriz / np.max(matriz) * 255).astype(np.uint8)
        altura, ancho = matriz.shape
        img_q = QImage(matriz.data, ancho, altura, ancho, QImage.Format_Grayscale8)
        return img_q