import mysql.connector

#conexión con la base de datos
acceso_bd = {"host" : "localhost",
            "user" : "root",
            "password" : "wili",
            "database" : "bichos",
            "port" : "3306"
            }

#clase para trabajar con bases de datos
class BaseDatos:
    def __init__(self, **kwargs):
        self.conector= mysql.connector.connect(**kwargs)
        
    def consulta(self, sql):
        self.cursor = self.conector.cursor()
        self.cursor.execute(sql)
        return self.cursor
    
    def meterbicho(self, Nombre, Tamaño, Patas, Color, Desplazamiento, Descripcion):
        self.cursor = self.conector.cursor()
        self.cursor.execute("INSERT INTO bichos (Nombre, Tamaño, Patas, Color, Desplazamiento, Descripcion) VALUES ( '"+Nombre+"', '"+Tamaño+"', '"+Patas+"', '"+Color+"', '"+Desplazamiento+"', '"+Descripcion+"');")
        self.conector.commit()
    
    def buscarbicho(self, Tamaño, Patas, Color, Desplazamiento):
        self.cursor = self.conector.cursor()
        self.cursor.execute("SELECT Nombre, Descripcion FROM bichos WHERE "+
                            "tamaño LIKE '"+Tamaño+
                            "' AND Patas LIKE '"+Patas+
                            "' AND Color LIKE '"+Color+
                            "' AND Desplazamiento LIKE '"+Desplazamiento+"'")
        return self.cursor
    
    def buscarnombre(self, Nombre):
        a=False
        self.cursor = self.conector.cursor()
        self.cursor.execute("SELECT Nombre FROM bichos WHERE "+
                            "Nombre LIKE '"+Nombre+"'")
        if(self.cursor.fetchall().__len__()>0):
            a = True
        return a
    
    def getbichos(self):
        self.cursor = self.conector.cursor()
        self.cursor.execute("SELECT * FROM bichos")
        array = []
        arraya = []
        for Nombre, Tamaño, Patas, Color, Desplazamiento, Descripcion in self.cursor:
            arraya = [Nombre.__str__(), Tamaño.__str__(), Patas.__str__(), Color.__str__(), Desplazamiento.__str__(), Descripcion.__str__()]
            array.append(arraya)
        array = self.tratarArray2(array)
        return array
    
    def gettamaño(self):
        self.cursor = self.conector.cursor()
        self.cursor.execute("SELECT * FROM tamaño")
        array = []
        for tamaño in self.cursor:
            array.append(tamaño.__str__())
        array = self.tratarArray(array)
        return array
    
    def getpatas(self):
        self.cursor = self.conector.cursor()
        self.cursor.execute("SELECT * FROM Patas")
        array = []
        for patas in self.cursor:
            array.append(patas.__str__())
        array = self.tratarArray(array)
        return array

    def getColor(self):
        self.cursor = self.conector.cursor()
        self.cursor.execute("SELECT * FROM Color")
        array = []
        for color in self.cursor:
            array.append(color.__str__())
        array = self.tratarArray(array)
        return array
    
    def getdesplazamiento(self):
        self.cursor = self.conector.cursor()
        self.cursor.execute("SELECT * FROM Desplazamiento")
        array = []
        for desplazamiento in self.cursor:
            array.append(desplazamiento.__str__())
        array = self.tratarArray(array)
        return array
    
    
    def tratarArray(self, Array):
        cars = ["{", "}", "(", ")", "'", ","]
        ArrayTratado = []
        for item in Array:
            str = item
            for char in cars:
                #print("tratando " + str + " con "+char)
                str = str.replace(char,"")
            ArrayTratado.append(str)

        return ArrayTratado
    
    def tratarArray2(self, Array):
        cars = ["{", "}", "(", ")", "'", ","]
        ArrayTratado = []
        for array in Array:
            a = array
            ArrayTratado2 = []
            for item in a:
                str = item
                for char in cars:
                    #print("tratando " + str + " con "+char)
                    str = str.replace(char,"")
                ArrayTratado2.append(str)
            ArrayTratado.append(ArrayTratado2)
            

        return ArrayTratado
    
    def insertarTamaño(self, tamaño):
        self.cursor = self.conector.cursor()
        self.cursor.execute("INSERT INTO Tamaño (Tamaño) VALUES ( '"+tamaño+"');")
        self.conector.commit()

    def insertarCuerpo(self, patas):
        self.cursor = self.conector.cursor()
        self.cursor.execute("INSERT INTO Patas (Patas) VALUES ( '"+patas+"');")
        self.conector.commit()
    
    def insertarColor(self, color):
        self.cursor = self.conector.cursor()
        self.cursor.execute("INSERT INTO Color (Color) VALUES ( '"+color+"');")
        self.conector.commit()
    
    def insertarDesplazamiento(self, desplazamiento):
        self.cursor = self.conector.cursor()
        self.cursor.execute("INSERT INTO Desplazamiento (Desplazamiento) VALUES ( '"+desplazamiento+"');")
        self.conector.commit()