from vista import Login
import sys
from PyQt5.QtWidgets import QApplication
from modelo import User

class Conector(object):
    def __init__(self, vista, sistema):
        self.__mi_vista = vista
        self.__mi_sistema = sistema


    def validar_usuario(self, u, p):
        return self.__mi_sistema.verificarUsuario(u,p)
    
    def cargar_senal_desde_carpeta(self,ruta_carpeta):
        return self.__mi_sistema.cargar_senal(ruta_carpeta)
    
    def cargar_dicom(self,x):
        return self.__mi_sistema.R_dicom(x)
    
    def obtener_info_dicom(self, ruta_archivo):
        return self.__mi_sistema.obtener_info_dicom(ruta_archivo)

class Ppal(object):
    def __init__(self):
        self.__app = QApplication(sys.argv)
        self.__mi_vista = Login()
        self.__mi_sistema = User()
        self.__mi_conector = Conector(self.__mi_vista, self.__mi_sistema)
        self.__mi_vista.asignarControlador(self.__mi_conector)
        
    def main(self):
        self.__mi_vista.show()
        sys.exit(self.__app.exec_())

clasePrincipal = Ppal()
clasePrincipal.main() 