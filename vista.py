from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap

class Login(QWidget):
    #constructor
    def __init__(self, ppal=None):
        super(Login,self).__init__(ppal)
        loadUi('interfaz.ui',self)
        self.botones()
        self.imagen()

    def botones(self):
        self.Ingresar.clicked.connect(self.Ingresar_sig)

    def imagen(self):
        self.label.setStyleSheet(f"border-image: url('C:/Users/aleja/OneDrive/Escritorio/UdeA/Semestre4/Informática2/Entregable_3/login.jpg'); border-top-left-radius: 50px;")
    def asignarControlador(self,c):
        self.__controlador = c

    def Ingresar_sig(self):
        usuario = self.usuario.text()
        password = self.contrasena.text()
        resultado = self.__controlador.validar_usuario(usuario,password)
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Resultado")

        if resultado == True:
            self.abrirVentana2()

        else:
            msg.setText("Usuario no Valido")
            msg.show()
            self.usuario.clear()
            self.contrasena.clear()
        
    def abrirVentana2(self):
        self.usuario.clear()
        self.contrasena.clear()
        ventana_ingreso=VentanaPrincipal(self)
        ventana_ingreso.asignarControlador(self.__controlador)
        self.hide()
        ventana_ingreso.show()

class VentanaPrincipal(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi("VentanaPrincipal.ui",self)
        self.__ventanaPadre = ppal
        self.__resultado_lista = []
        self.botones2()
        self.imagen2()

    def botones2(self):
        self.CerrarSesion.clicked.connect(self.accionSalir)
        self.SeleccionarCarpeta.clicked.connect(self.cargarSenal)
        self.horizontalSlider.valueChanged.connect(self.Slider)

    def imagen2(self):
        self.label_7.setStyleSheet(f"border-image: url('C:/Users/aleja/OneDrive/Escritorio/UdeA/Semestre4/Informática2/Entregable_3/d67fdd224ad205b7c1ca86260cfbfe29.jpg');")

    def asignarControlador(self,c):
        self.__controlador = c

    def accionSalir(self):
        print("Boton presionado Salir")
        self.hide()
        self.__ventanaPadre.show()
 
    def cargarSenal(self):
        ruta_carpeta = QFileDialog.getExistingDirectory(self, 'Seleccionar Carpeta', '/')
        self.__resultado_lista = self.__controlador.cargar_senal_desde_carpeta(ruta_carpeta)
        self.configurar_rango_slider()
        if self.__resultado_lista:
            primer_archivo = self.__resultado_lista[0]
            metadata = self.__controlador.obtener_info_dicom(primer_archivo)
            self.nombre.setText(f"{metadata.get('Nombre', 'No disponible')}")
            self.sexo.setText(f"{metadata.get('Sexo', 'No disponible')}")
            self.edad.setText(f"{metadata.get('Edad', 'No disponible')}")
            self.fecha.setText(f"{metadata.get('FechaEstudio', 'No disponible')}")
            self.peso.setText(f"{metadata.get('Peso', 'No disponible')}")
        return ruta_carpeta
     
    def configurar_rango_slider(self):
        num_elementos = len(self.__resultado_lista)
        self.horizontalSlider.setRange(0, num_elementos - 1)
        self.horizontalSlider.setSingleStep(1)

    def Slider(self):
      self.cargar_imagen()

    def cargar_imagen(self):
        x = int(self.horizontalSlider.value())
        x = self.__resultado_lista[x]
        y= self.__controlador.cargar_dicom(x)
        self.mostrar_imagen(y)

    def mostrar_imagen(self, img_q):
        pixmap = QPixmap.fromImage(img_q)
        self.img.setScaledContents(True)
        self.img.setPixmap(pixmap)