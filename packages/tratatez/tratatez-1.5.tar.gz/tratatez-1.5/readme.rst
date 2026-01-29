# Librería Tratatez

Librería de Python para manipulación avanzada de archivos de texto (.txt).
con proposito educativo...
Enfocada, para construir y simular una consola (preferiblemente utilizando el comando match de python).

## Descripción

`tratatez` es una librería completa que proporciona 30 operaciones diferentes para trabajar con archivos de texto, incluyendo operaciones básicas, manipulación de líneas, modificación de caracteres, cifrado y conversión a CSV.

## Ultima Actualización

enero de 2026,
Versión: 1.5 (Mejoras en la documentación y ejemplos adicionales)

## Instalación

Puedes usar la librería copiando la carpeta `tratatez` a tu proyecto y luego importándola:

```python
from tratatez import tratatez
```

## Uso Básico

La función principal es `tratatez(dire, tipe, conte="", line=None, punt=None)`:

- **dire**: Ruta del archivo .txt
- **tipe**: Número de operación (0-29)
- **conte**: Contenido/texto según la operación
- **line**: Número de línea (base 0)
- **punt**: Parámetro adicional según la operación

### Ejemplos

#### Operaciones Básicas (Tipos 0-13)

```python
from tratatez import tratatez

# Tipo 1: Crear archivo vacío
tratatez("mi_archivo.txt", 1)

# Tipo 5: Escribir contenido
tratatez("mi_archivo.txt", 5, "Línea 1\nLínea 2\nLínea 3")

# Tipo 7: Leer contenido completo
contenido = tratatez("mi_archivo.txt", 7)
print(contenido)

# Tipo 8: Leer como lista de líneas
lineas = tratatez("mi_archivo.txt", 8)
for i, linea in enumerate(lineas):
    print(f"Línea {i}: {linea}")

# Tipo 9: Leer línea específica
linea_2 = tratatez("mi_archivo.txt", 9, line=2)
print(f"Línea 2: {linea_2}")

# Tipo 10: Reemplazar línea específica
tratatez("mi_archivo.txt", 10, "Nueva línea 1", line=1)

# Tipo 3: Copiar archivo
tratatez("mi_archivo.txt", 3, "copia.txt", punt="./respaldo")

# Tipo 2: Eliminar archivo
tratatez("copia_temporal.txt", 2)
```

#### Manipulación de Líneas

```python
# Tipo 6, punt=1: Añadir nueva línea al final
tratatez("mi_archivo.txt", 6, "Nueva línea al final", punt=1)

# Tipo 6, punt=2: Añadir al inicio
tratatez("mi_archivo.txt", 6, "Primera línea", punt=2)

# Tipo 6, punt=3: Insertar debajo de línea específica
tratatez("mi_archivo.txt", 6, "Insertada debajo de línea 1", line=1, punt=3)

# Tipo 13, punt=0: Enumerar líneas
tratatez("mi_archivo.txt", 13, "ITEM_", punt=0)

# Tipo 13, punt=1: Quitar enumeración
tratatez("mi_archivo.txt", 13, punt=1)
```

#### Operaciones de Caracteres (Tipos 14-23)

```python
# Tipo 14: Modificar un caracter específico (posición base 1)
tratatez("archivo.txt", 14, "X", line=0, punt=5)  # Cambia posición 5 en línea 0

# Tipo 15: Verificar si línea termina con texto
resultado = tratatez("archivo.txt", 15, ".", line=2)
print(f"¿Termina con punto?: {resultado}")

# Tipo 16: Verificar si línea contiene texto
resultado = tratatez("archivo.txt", 16, "palabra", line=1)
print(f"¿Contiene 'palabra'?: {resultado}")

# Tipo 17: Eliminar último(s) caracter(es)
tratatez("archivo.txt", 17, "1", line=0)  # Elimina 1 caracter
tratatez("archivo.txt", 17, "2", line=1)  # Elimina 2 caracteres

# Tipo 18: Buscar posiciones de subcadena
posiciones = tratatez("archivo.txt", 18, "la", line=0)
print(f"Posiciones de 'la': {posiciones}")

# Tipo 19: Contar tabs o espacios al inicio
tabs = tratatez("archivo.txt", 19, "", line=0, punt=0)  # Contar tabs
espacios = tratatez("archivo.txt", 19, "", line=0, punt=1)  # Contar espacios

# Tipo 20: Poner/quitar tabulador o espacios
tratatez("archivo.txt", 20, "0", line=0, punt=0)  # Poner tab
tratatez("archivo.txt", 20, "1", line=0, punt=0)  # Poner espacio
tratatez("archivo.txt", 20, "0", line=0, punt=1)  # Quitar tab
tratatez("archivo.txt", 20, "1", line=0, punt=1)  # Quitar espacios

# Tipo 21: Quitar espacios al final
tratatez("archivo.txt", 21, "", line=0, punt=0)  # Línea específica
tratatez("archivo.txt", 21, "", line=0, punt=1)  # Todas las líneas

# Tipo 22: Extraer entre delimitadores
# punt: 0:(), 1:[], 2:{}, 3:<>, 4://, 5:¿?, 6:¡!, 7:'', 8:**
texto = tratatez("archivo.txt", 22, "0", line=0, punt=0)  # Entre paréntesis
print(f"Texto entre paréntesis: {texto}")

# Tipo 23: Extraer substring por índices
texto = tratatez("archivo.txt", 23, "5", line=0, punt=10)  # Del índice 5 al 10
print(f"Substring [5:10]: {texto}")
```

#### Cifrado y Conversión (Tipos 24, 27-29)

```python
# Tipo 24: Cifrado XOR
# punt=1: Encriptar con XOR
tratatez("archivo.txt", 24, "mi_clave_secreta", punt=1)

# punt=0: Desencriptar con XOR
tratatez("archivo_encriptado.txt", 24, "mi_clave_secreta", punt=0)

# punt=2: Cifrado César
# conte=dirección (1=adelante, 0=atrás), line=desplazamiento
tratatez("archivo.txt", 24, "1", line=3, punt=2)  # César con desp=3, adelante

# Tipo 27: Separar por punto y coma
# punt=0: Todo el archivo
lista_completa = tratatez("archivo.txt", 27, "", punt=0)

# punt=1: Línea específica
lista_linea = tratatez("archivo.txt", 27, "", line=0, punt=1)

# Tipo 28: Unir lista con punto y coma
mi_lista = ["elemento1", "elemento2", "elemento3"]

# punt=0: Añadir al inicio
tratatez("archivo.txt", 28, mi_lista, punt=0)

# punt=1: Reemplazar línea
tratatez("archivo.txt", 28, mi_lista, line=2, punt=1)

# punt=2: Añadir al final
tratatez("archivo.txt", 28, mi_lista, punt=2)

# Tipo 29: Crear CSV desde TXT (delimitado por comas)
tratatez("datos.txt", 29, "")  # Crea datos.csv
```

## Referencia Rápida de Operaciones

### Módulo 1 (tratadocu-1.py): Tipos 0-13
- **0**: Mostrar documentación
- **1**: Crear archivo vacío
- **2**: Eliminar archivo
- **3**: Copiar archivo
- **4**: Mover archivo
- **5**: Reemplazar contenido completo
- **6**: Añadir contenido (punt: 0=final línea, 1=nueva línea, 2=inicio, 3=debajo línea)
- **7**: Leer contenido completo
- **8**: Leer como lista de líneas
- **9**: Leer línea específica
- **10**: Reemplazar línea
- **11**: Modificar palabra en línea
- **12**: Añadir texto al final de línea
- **13**: Enumerar/des-enumerar líneas

### Módulo 2 (tratadocu-2.py): Tipos 14-23
- **14**: Modificar caracter específico
- **15**: Verificar si línea termina con texto
- **16**: Verificar si línea contiene texto
- **17**: Eliminar último(s) caracter(es)
- **18**: Buscar posiciones de subcadena
- **19**: Contar tabs/espacios al inicio
- **20**: Poner/quitar tabs/espacios al inicio
- **21**: Quitar espacios al final
- **22**: Extraer entre delimitadores
- **23**: Extraer substring por índices

### Módulo 3 (tratadocu-3.py): Tipos 24, 27-29
- **24**: Cifrado XOR/César (punt: 0=desc XOR, 1=enc XOR, 2=César)
- **27**: Separar por ';' en lista
- **28**: Unir lista con ';'
- **29**: Crear CSV desde TXT

## Notas Importantes

1. Los números de línea son **base 0** (la primera línea es 0)
2. En tipo 14, las posiciones de caracteres son **base 1** (primer caracter es 1)
3. Los archivos se crean con codificación **UTF-8**
4. Algunos tipos requieren que el archivo exista, otros lo crean automáticamente
5. El tipo 24 con punt=1 (encriptar XOR) solo acepta contenido alfanumérico y espacios

## Manejo de Errores

La librería imprime mensajes de error descriptivos y retorna `None` en caso de error. Siempre verifica el resultado:

```python
contenido = tratatez("archivo.txt", 7)
if contenido is not None:
    print(f"Contenido leído: {contenido}")
else:
    print("Error al leer el archivo")
```

## Licencia

Este proyecto es de uso libre.

---

Para más detalles sobre cada operación, llama a la función con tipo 0:
```python
tratatez("", 0)
```
Esto permitirá ver la documentación completa directamente en la consola.

## A continueación se presenta el codigo fuente de una consola (basica) que utiliza la librería tratatez:

Copie y pegue el siguiente código en un archivo .py para probar la consola... y tratatez:

```python
""" Mi consola personal """


"==================================="

# llamado a la libreria tratatez... aqui, de proposito educativo.
from tratatez import tratatez

"==================================="

# mensaje de bienvenida
print()
print("Bienvenido a mi consola personal. Escribe 'ayuda' para ver los comandos disponibles.")

"..................................."

# clases de apoyo para la consola
class Estilo_de_enter:
    
    def __init__(self):
        
        self.cual= 0
        
        self.normal = ">> "
        self.modo_de_ayuda = ">>> "
        self.in_dir_from = "root_from: >> "
        self.in_dir_to = "root_to: >> "
        self.add_lista = "add_list: >> "
        self.en_split= "c_lista: >> "
        self.which_list= "which_list: >> "
        self.a_reset_list= "reset_list_num: >> "
        self.en_reset_list= "reset_list_que: >> "
        
    def obtener(self):
        
        if self.cual == 0:
            return input(self.normal)
        elif self.cual == 1:
            return input(self.in_dir_from)
        elif self.cual == 2:
            return input(self.in_dir_to)
        elif self.cual == 3:
            return input(self.add_lista)
        elif self.cual == 4:
            return input(self.en_split)
        elif self.cual == 5:
            return input(self.which_list)
        elif self.cual == 6:
            return input(self.a_reset_list)
        elif self.cual == 7:
            return input(self.en_reset_list)
        elif self.cual == 8:
            return input(self.modo_de_ayuda)
        
entrada= Estilo_de_enter()
        
class MiConsola:
    
    def __init__(self):
        
        self.pez= None # solo para hacer comparaciones
        
        self.root_from= None
        self.root_to= None
        self.siempre_despues_de_dir_1= False
        self.siempre_despues_de_dir_2= False
        
        self.add_de_list= False
        self.listado_de_sentencias_1= []
        self.listado_de_sentencias_2= []
        self.single_which_list= None
        self.reset_list= 0
        self.indice_a_resetear= None
        
        self.streamg_cortado= False
        
        self.numero= None
        self.linea_de_sentencia= None
        
        self.modo_de_ayuda_activado= False
        self.en_ayuda= 0
        
        # almaceno las variables aqui (las creadas por mi, en mi lenguaje personal)
        self.hallo_el_tipo_str= {} # para identificacion del Type   ({'nombre_en_txt': tipo_variable})
        self.hallo_el_tipo_int= {}
        self.hallo_el_tipo_boolear= {}
        #
        self.algunas_variables_aqui= {} # elementos                 ({'nombre_en_txt': 'id_de_objeto o valor_de_variable'})
        
    "..................................."
        
    def guardando_variable(self, nombre_variable, el_valor):
        
        def conociendo_el_tipo_de_variable(): # para identificar los Types (facilmente)
        
            tipo_variable= type(el_valor)
            
            if tipo_variable == str:
                self.hallo_el_tipo_str= {nombre_variable: tipo_variable}
            elif tipo_variable == int:
                self.hallo_el_tipo_int= {nombre_variable: tipo_variable}
            elif tipo_variable == bool:
                self.hallo_el_tipo_boolear= {nombre_variable: tipo_variable}
                        
        conociendo_el_tipo_de_variable()
        self.algunas_variables_aqui[nombre_variable]= el_valor
    
    def extraeigo_el_valor_de_variable(self, nombre_variable):
        try:
            valor_variable= self.algunas_variables_aqui[nombre_variable]
            return valor_variable
        except:
            print("error: la variable no existe.")
            return None
    
    "..................................."
    
    def la_linea_extraida_la_paso_a_lista_sentencia(self):
        
        pedasitos= self.linea_de_sentencia.split()
        self.listado_de_sentencias_2= pedasitos
        self.linea_de_sentencia= None
    
    def resetea_un_indice_de_lista_1(self, nuevo_elemento):
        elemento_a_guardar= nuevo_elemento
        try:
            self.listado_de_sentencias_1[self.indice_a_resetear]= elemento_a_guardar
            print(self.listado_de_sentencias_1)
            print(f"el elemento '{elemento_a_guardar}' ha sido guardado en lista 1.")
        except:
            print("error: indice fuera de rango.")
        
        entrada.cual= 0
    
    def resetea_un_indice_de_lista_2(self, nuevo_elemento):
        elemento_a_guardar= nuevo_elemento
        try:
            self.listado_de_sentencias_2[self.indice_a_resetear]= elemento_a_guardar
            print(self.listado_de_sentencias_2)
            print(f"el elemento '{elemento_a_guardar}' ha sido guardado en lista 2.")
        except:
            print("error: indice fuera de rango.")
        
        entrada.cual= 0
        
    def efectuando(self, esto):
        
        if True: # manejo de directorio fuente
            if self.siempre_despues_de_dir_1 == True:
                
                self.root_from= esto
                self.siempre_despues_de_dir_1= False
                print("La fuente ha sido establecida")
                
                if self.modo_de_ayuda_activado == True: # con esto, gestiono el modo de ayuda continua
                    
                    if self.en_ayuda == 1:
                        print(".")
                        print("¡Bien hecho! has establecido la ruta fuente.")
                        print("ya puedes proceder a crear la lista de sentencias: 'sentencia', 'numero', 'un_numero_entero'")
                        print("ahora, Utiliza el comando 'add_list' para agregar esos elementos a la lista.")
                        entrada.cual= 8 # restableciendo el estilo de modo de ayuda continua
                        self.en_ayuda= 2
                        
                    elif self.en_ayuda == 0: # por depuracion (no se ha establecido una ruta y hubo un error)
                        entrada.cual= 8 # restableciendo el estilo de modo de ayuda continua
                        
                else:
                    entrada.cual= 0 # restableciendo el estilo normal
                
                return
            
            if esto == "dir_from":
                
                self.siempre_despues_de_dir_1= True
                entrada.cual= 1
                print(f"Por favor... ingrese la ruta, del fichero, fuente ''de codigo'' (documento de extension .txt)")
                
                return
            
        if True: # manejo de directorio destino
            if self.siempre_despues_de_dir_2 == True:
                self.root_to= esto
                self.siempre_despues_de_dir_2= False
                print("El destino ha sido establecido")
                entrada.cual= 0 # estableciendo el estilo normal
                return
            
            if esto == "dir_to":
                self.siempre_despues_de_dir_2= True
                entrada.cual= 2
                print(f"Por favor ingrese la ruta, del fichero, de destino:")
                return
        
        "...................................."
        
        if True: # ingresando streamg a listado_de_sentencias
            if self.streamg_cortado == True:
                
                def cortando_streamg():
                    
                    # aqui iria el codigo para contar el streamg
                    lista_creada= esto.split()
                    self.listado_de_sentencias_1= lista_creada
                    print(lista_creada)
                
                self.streamg_cortado= False
                cortando_streamg()
                print("El streamg ha sido cortado.")
                
                if self.modo_de_ayuda_activado == True: # por depuracion.
                    entrada.cual= 8 # restableciendo el estilo de modo de ayuda continua
                else:
                    entrada.cual= 0 # estableciendo el estilo normal
                
                return
            
            if esto == "in_str":
                self.streamg_cortado= True
                entrada.cual= 4
                print("Por favor, ingresa el streamg a cortar:")
                return
        
        if True: # agrega elementos a la lista de manera continua.
                 # para testiar la consola mientras la construyo
            #""" quita el carapter numeral (#) para desactivar esta seccion
            
            def ingresa_a_lista():
                
                # agregando el elemento a la lista
                self.listado_de_sentencias_1.append(esto)
                
                # para limpiar la lista
                num_elementos= len(self.listado_de_sentencias_1)
                ultima_posicion= num_elementos - 1
                #
                if self.listado_de_sentencias_1[ultima_posicion] == "clear_list":
                    self.listado_de_sentencias_1.clear()
                
                # es muy comodo visualizar lo que hay (en la lista)... por consola
                print(self.listado_de_sentencias_1)

            if self.add_de_list == True:    # PROCESO "uno por uno".
                
                ingresa_a_lista()
                self.add_de_list= False
                
                if self.modo_de_ayuda_activado == True: # con esto, gestiono el modo de ayuda continua
                    if self.en_ayuda == 2:
                        
                        if esto == "numero":
                            print(".")
                            print("¡Bien hecho! has establecido el segdo elemento necesario en la lista de sentencia 1.")
                            print("ahora, ingresa un numero (este, es el numero de la linea de tu documento .txt)")
                            print("por ejemplo si tu .txt tiene 100 lineas, puedes ingresar un numero entre: el 0 y el 100.")
                            print("no olvides ingresar primero a 'add_list' para poder agregar ese numero.")
                        
                        try:
                            if self.listado_de_sentencias_1[2] != self.pez:
                                print(".")
                                print("¡Excelente! has creado los tres elementos necesarios.")
                                print("ahora, vuelve a ingresar el comando 'muestra' para que veas la diferencia.")
                                self.en_ayuda= 3
                        except:
                            pass
                            
                        entrada.cual= 8 # restableciendo el estilo de modo de ayuda continua
                
                else:
                    entrada.cual= 0 # restableciendo el estilo normal
                
                return
            
            if esto == "add_list":
                self.add_de_list= True
                entrada.cual= 3
                print(f"ingrese elemento")
                
                return
            
            "--fin de la seccion de add_list y comienzo del proceso (ciclo) in --"
        
            if esto == "in":    # PROCESO "ciclo" (para agregar varios elementos simultaneamente).
                while True:
                    
                    # definiendo el elemento a agregar
                    elemento= input("agrega_en_lista>> ")
                    elemento.strip(); elemento.lower()
                    
                    # terminando el ciclo de agregar
                    if elemento != "out":
                        self.listado_de_sentencias_1.append(elemento)
                    else:
                        esto= "saliste de agregacion continua"
                        break
                    
                    print(self.listado_de_sentencias_1)
                    #print("escriba 'out' para terminar")
            #"""
        
        "...................................."
        
        if True: # eliminando los elementos de las listas de sentencias.
            
            if esto == "clear_list_1":
                self.listado_de_sentencias_1.clear()
                print("la lista de sentencias ha sido limpiada.")
                return
        
            if esto == "clear_list_2":
                self.listado_de_sentencias_2.clear()
                print("la lista de sentencias ha sido limpiada.")
                return
        
        if True: # reseteando un elemento de la lista de sentencias.
            
            if self.reset_list == 3:
                
                if self.single_which_list == 1:
                    self.resetea_un_indice_de_lista_1(esto)
                elif self.single_which_list == 2:
                    self.resetea_un_indice_de_lista_2(esto)
                
                # el estilo de cursor, se esta restableciendo en las llamadas.
                self.reset_list= 0
                
                return
            
            elif self.reset_list == 2: # ingreso el nuevo elemento.
                
                self.indice_a_resetear= int(esto)
                self.reset_list= 3
                entrada.cual= 7
                print("ingrese el elemento nuevo:")
                
                return
            
            elif self.reset_list == 1: # indico el numero (indice) del elemento.
                
                if esto == "1":
                    self.single_which_list= 1
                elif esto == "2":
                    self.single_which_list= 2
                    
                self.reset_list= 2
                entrada.cual= 6
                print("ingrese el numero de elemento a modificar:")
                
                return
            
            elif esto == "reset_list": # entro a resetear un elemento de la lista
                
                self.reset_list= 1
                entrada.cual= 5
                print("¿de cual lista quiere modificar (un indice), opciones 1 o 2:")
                
                return
        
        if True: # traspaso la linea extraida a lista de sentencias (como lista)
            
            if esto == "traspasoline":
                if self.linea_de_sentencia is not None:
                    self.la_linea_extraida_la_paso_a_lista_sentencia()
                    print("la linea extraida ha sido pasada a la lista de sentencias_2.")
                
                return
        
        if True: # moviendo el numero de linea
            
            cadena= esto.split()
            distancia= len(cadena)
            dista= distancia - 1
            numero_indicador= cadena[dista]
            cadena.pop()
            comando_base= " ".join(cadena)
            
            if comando_base == "mueve puntero a":
                try:
                    nuevo_numero= int(numero_indicador)
                    self.numero= nuevo_numero
                    print(f"el numero de linea ha sido movido a: {self.numero}")
                except:
                    print("error: el indicador no es un numero valido.")
                
                return
        
        if True: # transponiendo las listas de sentencias
            if esto == "traspaso":
                
                momeamente= self.listado_de_sentencias_1
                self.listado_de_sentencias_1= self.listado_de_sentencias_2
                self.listado_de_sentencias_2= momeamente
                print("las listas de sentencias han sido transpuestas.")
                
                return
        
        "...................................."
        
        if True: # guardado de variables
            if esto == "guarda":
                
                # coloque en self.listado_de_sentencias_1: variable_nueva = x
                # x seria un numero entero (int).
                # ten en cuenta que, los elementos de la lista deben ser tres (el "=" es uno de esos elementos).
                # el signo '=' se ingnoran, en este sistema (consola).
                
                #"""
                
                pasa= False
                if len(self.listado_de_sentencias_1) == 3:
                    pasa= True
                
                if (self.listado_de_sentencias_1 != self.pez) and (pasa == True) and (self.listado_de_sentencias_1[1] == "="):
                    try:
                        nombre_var= self.listado_de_sentencias_1[0]
                    except:
                        print("error: no se ha especificado el nombre de la variable.")
                        return
                    try:
                        valor_var= int(self.listado_de_sentencias_1[2])
                    except:
                        print("error: el valor de la variable no es un numero entero valido.")
                        return
                    
                    self.guardando_variable(nombre_var, valor_var)
                    print(f"La variable '{nombre_var}' ha sido guardada con el valor '{valor_var}'")
                
                else: # por depuracion.
                    print("la primera palabra 'guarda' indica que se va a guardar una variable, pero el formato no es correcto.")
                    print("error: la sintaxis para guardar una variable es incorrecta.")
                
                return
                #"""
        
        if True: # extraccion de variables
            
            nombre_var= None
            valor_obtenido= None
            
            pasa= False
            listo= list(esto.split())
            if len(listo) == 2:
                pasa= True
            
            if pasa == True:
            
                match listo: # utilizo match case pora intentar extraer cualquier variable.
                    case "consigue", *resto:
                        
                        nombre_var= str(resto[0])
                        valor_obtenido= self.extraeigo_el_valor_de_variable(nombre_var)
                        
                        if valor_obtenido != None:
                            print(f"El valor de la variable '{nombre_var}' es: {valor_obtenido}")
                    
                return
        
        if True: # limpia la urna... de variables (todas las variables almacenadas)
            if esto == "limpia_urna":
                
                self.hallo_el_tipo_str.clear()
                self.hallo_el_tipo_int.clear()
                self.hallo_el_tipo_boolear.clear()
                self.algunas_variables_aqui.clear()
                
                print("todas las variables han sido limpiadas.")
                
                return
        
        "...................................."
        
        if esto == "muestra":
            print(".")
            print("Ruta fuente:", self.root_from)
            print("Ruta destino:", self.root_to)
            print("variables:", self.algunas_variables_aqui)
            print(".")
            print("Lista de sentencias 1:", self.listado_de_sentencias_1)
            print("Lista de sentencias 2:", self.listado_de_sentencias_2)
            print(".")
            print("Numero_de_linea:", self.numero)
            print("linea_extraida:", self.linea_de_sentencia)
            print(".")
            print("El proceso continua...")
            print(".")
            
            if self.modo_de_ayuda_activado == True: # con esto, gestiono el modo de ayuda continua
                
                if self.en_ayuda == 0:
                        
                    print("ahora, escriba 'dir_from' asi estableceras la Ruta fuente.")
                    print("(recuerde que fue el segundo punto que se le sugirio al activar el modo de ayuda continua)")
                    self.en_ayuda= 1
                        
                if self.en_ayuda == 3:
                    
                    print("exelente, has completado los pasos principales.")
                    print("ahora puedes proceder a ejecutar la lista (1) con el comando 'ejcut'.")
                    self.en_ayuda= 4
            
            return
        
        if esto == "activar modo de ayuda continua, guia inicial":
            
            def sospecha():
                
                veneno= False
                lista_vacia= []

                if self.root_from != self.pez:
                    veneno= True
                if self.root_to != self.pez:
                    veneno= True
                if self.listado_de_sentencias_1 != lista_vacia:
                    veneno= True
                if self.listado_de_sentencias_2 != lista_vacia:
                    veneno= True
                if self.numero != self.pez:
                    veneno= True
                if self.linea_de_sentencia != self.pez:
                    veneno= True
                    
                return veneno
            
            evaluo= sospecha()
            
            if self.en_ayuda == 0: # compruevo primero para prevenirme y alertar al usuario.
                if evaluo == True:
                    
                    self.en_ayuda= 100 # la coloco en 100 por prudencia.
                    print("usted usó 'desactivar modo de ayuda continua' pero la lista de sentencia (1) no tiene la cofiguracion inicial.")
                    print("si quiere seguir la guia de ayuda continua, por favor, restablezca la configuracion inicial.")
            
            if (self.en_ayuda == 0) and (evaluo == False):
                
                print(self.en_ayuda, evaluo) # para debuguear
                self.modo_de_ayuda_activado= True
                entrada.cual= 8
                print("Modo de ayuda continua activado.")
                print("Escriba 'desactivar modo de ayuda continua' para salir de este modo.")
                print(".")
                print("- introdusca 'muestra' y presione enter (para ver las configuraciones iniciales).")
                print("- empecemos primero introduciendo la ruta fuente, escribiendo 'dir_from'")
                print("- y... posteriormente vallamos a match case (ya sea con 'in', 'in_str', 'add_list', etc...)")
                print("    en 'listado_de_sentencias_1' deben crearse los elementos: 'sentencia', 'numero', 'un_numero_'")
            
            if self.en_ayuda == 100:
                
                if evaluo == True: # esta condicion... para la guia continua.
                    
                    print("recuerde que para usar el modo de ayuda continua")
                    print("debes restablecer la configuracion inicial de la consola.")
                    print(".")
            
            return
        
        if esto == "desactivar modo de ayuda continua":
            
            self.modo_de_ayuda_activado= False
            entrada.cual= 0
            print("Modo de ayuda continua desactivado.")
            
            return
        
        # Apartir de aqui podemos empezar a usar la libreria tratatez
        print(f"Ejecutando: {esto}")
        
        if self.listado_de_sentencias_1 == []:
            match esto:                        
                case "llamando lo que quiero, aqui.":
                    print("mi codigo esta siendo ejecutado.")
                case _:
                    print("comando no reconocido.")
                    print("""
                          nota # 1: puede editar el codigo de esta consola,
                          para agregar nuevos comandos en este espacio.
                          
                          como por ejemplo:
                          - en modo alternativo.
                          - en la seccion de 'match case'.
                          - o como dije antes, en esta seccion.
                          
                          tambien puede llamar a una inteligencia artificial,
                          que tenga en su pc o en la nube,
                          para que le ayude a hacer cualquier tipo de tarea.
                          
                          nota # 2: en este momento la lista 1 esta vacia,
                          es, por lo que ahora... se encuentra aqui.
                          
                          se sugiere que, 
                          cree sus nuevos comandos en este espacio.
                          
                          ... en caso de ser novato usando esta consola,
                          por favor, escriba 'ayuda' y active el modo de ayuda.
                          el modo de ayuda 
                          es el penultimo comando que aparece
                          ''en la lista de comandos'' al introducir 'ayuda'.
                          """)
                                            
        else:
            if esto == "ejcut":
                
                expongo_msg_final= True # para eludir un error (no se asigno ruta).
                
                match self.listado_de_sentencias_1:
                    
                    case "sentencia", *algo: # con esta 1 palabra de la lista ("sentencia", de este script)
                        tamaño= len(algo)
                        
                        if tamaño == 1:     # simplemente ejecuta algo
                            print("sentencia:", algo[0])
                            
                        elif tamaño == 2:   # extraigo una linea de fichero.from
                            
                            if algo[0] == "numero":
                                
                                self.numero= int(algo[1])
                                self.linea_de_sentencia= tratatez(self.root_from, 9, line=self.numero)  # otro ejemplo
                                print("en la 2 opcion de mi script (consola), por favor mire el codigo (me encuentro ejecutando un match case).")
                                
                                if self.linea_de_sentencia == self.pez: # por depuracion.
                                    print("error: la Ruta fuente no ha sido establecida.")
                                    expongo_msg_final= False
                                else:
                                    print("sentencia_de_mi_linea:", self.linea_de_sentencia)
                                    
                            if self.modo_de_ayuda_activado == True: # con esto, gestiono el modo de ayuda continua
                                if self.en_ayuda == 4:
                                    
                                    print(".")
                                    print("has ejecutado la lista de sentencias.")
                                    self.en_ayuda= 100 # con este numero alto (especifico) finalizo cualquier induccion, que quiera hacer para esta consola.
                                    print("felicidades, has finalizado el modo de ayuda continua, por tanto, se procede a desactivar de forma automatica...")
                                    print("""
                                          has logrado hacer varias cosas:
                                          
                                          - has ejecutado la libreria tratatez
                                          - has aprendido que la lista 1 te permite 
                                            interactuar con la consola de una manera especial
                                          - has llegado a un punto en el que puedes usar 
                                            el comando 'ayuda'. y darte cuenta 
                                            (mas facilmente por ti mismo) 
                                            de como puedes usar los otros comandos.
                                          
                                          por ultimo, te pido que ejecutes 'muestra'
                                          y posteriormente 'ayuda'.
                                          """)
                            
                        if self.modo_de_ayuda_activado == True: # terminando (el modo de ayuda continua)
                            if self.linea_de_sentencia != self.pez: # por depuracion.
                                
                                # DESACTIVA (siempre y cuando)
                                self.modo_de_ayuda_activado= False
                                self.en_ayuda= 0
                                entrada.cual= 0 # restableciendo el estilo normal
                                                        
                        else:
                            print("tratatez ha sido ejecutado.")
                        
                    case "condicion_unica", "(if)", valor_1, "==", valor_2: # otro ejemplo de match case
                        print("ejecutando... condicion unica (if)")
                        print(f"y estos son sus valores: {valor_1}, {valor_2}")
                    
                    case "if", *resto_frase: # otro ejemplo de match case
                        print(".")
                        print("mi lenguaje personal puede tener el comando 'if'.")
                        print("pero, debere terminar de procesar el resto del codigo.")
                        print("con... la libreria tratatez, ¡con ella puedo hacer muchas cosas!")
                        print("como por ejemplo, extraer una linea (que comience con 'if')")
                        print(".")
                        print("sacar la primera palabra 'if' (como primer elemento de una lista).")
                        print("has que el resto de la frase sea un string (para mas luego integrarla al 'if').")
                        print("pero antes de integrarla...")
                        print("hacerle un... resto_.replace(' ', '') a ese string.")
                        print("y luego separar los dos valores con un split('==').")
                        print("ahora si, integro estos elementos (valores) al 'if'.")
                        print(".")
                        print("paso esta nueva lista a la lista de sentencia 1 o 2.")
                        print("luego, ejecuto la lista, con el comando 'ejcut' u otro, para traerla a esta seccion de codigo.")
                        print(".")
                        print("posteriormente... comparo los valores aqui.")
                        print("*resto_frase  ... serian dos argumentos (2 valores de entradas).")
                        print(".")
                        print(f"estos son los valores: {resto_frase}")
                        print(".")
                        
                    case _: #...
                        print("comando no reconocido (en la lista)")
                    
                if expongo_msg_final == True:
                    print("ahora puede usar el comando 'muestra' de manera mas activa... fin de la ejecucion.")

            elif esto == "saliste de agregacion continua": # captando la salida del ciclo de agregar
                print("ahora, si quiere ejecutar la lista, use 'ejcut'.")
            else:
                print("¿esta tratando... de ejecutar match case? utilice 'ejcut' para eso.")
                print("La lista no esta vacia.")
                
consol= MiConsola()

"..................................."

# ciclo principal de la consola
while True:
    
    comando = entrada.obtener()
    comando.strip()
    
    if comando == "":
        continue

    if comando.lower() in ["salir", "exit", "quit"]:
        print("consola cerrada.")
        break
        
    if comando.lower() == "ayuda":
        print()
        print("Comandos disponibles:")
        print("  salir, exit, quit  - Salir de la consola")
        print("  dir_from           - Establecer el fichero fuente")
        print("  dir_to             - Establecer el fichero destino")
        print("  muestra            - Muestra las configuraciones actuales")
        print("  in                 - Agregar varios elementos a la lista (terminar con 'out')")
        print("  in_str             - Ingresar un string para cortarlo en lista e ingresarlo a lista de sentencias")
        print("  add_list           - Agregar un elemento a la lista")
        print("  reset_list         - Modificar un elemento (de una de las dos listas de sentencias)")
        print("  clear_list_x       - Limpiar la lista de elementos (x = 1 o 2)")
        print("  clear_list         - Limpia completamente la lista 1 (unicamente en add_list, como ultimo elemento)")
        print("  ejcut              - Ejecutar la lista, de 'sentencias'")
        print("  traspasoline       - Pasar la linea extraida a la lista de sentencias 2")
        print("  traspaso           - Transpone las listas de sentencias (1 y 2)")
        print("  mueve puntero a x  - Mueve el numero de linea, a un valor especifico (x)")
        print("  guarda             - Guardar una variable (listado...1 debe tener: nombre_var = valor_var)")
        print("  consigue var_nomb  - Obtener el valor de una variable guardada")
        print("  limpia_urna        - Limpia todas las variables guardadas")
        print("  activar modo de ayuda continua, guia inicial - Entra en un modo especial de ayuda")
        print(".")
        print("  cualquier otro comando si la lista 1 esta vacia (se ejecuta directamente)")
        continue
    
    if comando == "modo_alternativo":
        print("Has entrado en el modo alternativo.")
        while True:
            alt_comando = input("modo_alt: >> ")
            alt_comando.strip()
            
            if alt_comando.lower() in ["salir_de_alta", "exit_alt", "quit_alt"]:
                print("Saliendo del modo alternativo...")
                break
            
            print(f"Comando alternativo recibido: {alt_comando}")
            # en este punto, puedo hacer los que quiera con 'alt_comando'.
        continue
    
    consol.efectuando(comando)
```
