######################## IMPORT Y OPCIONES GLOBALES ########################
import pandas as pd
from tabulate import tabulate
from time import sleep

#Cambiamos el formato de los tipos de dato float
pd.set_option('display.float_format', lambda x: '%.9f' % x)

######################## UTILIDADES ########################
class Salir(Exception):
    """Excepción usada para regresar al menú principal."""
    pass

def mostrar_aviso(descripcion: list[str], tipo: str = "Importante") -> None:
    """Muestra un aviso al usuario.

    Args:
        descripcion (list[str]): Lista de strings con el contenido.
        tipo (str, optional): Tipo de aviso. Puede ser "Importante", "Información" o "Resultado". Defaults to "Importante".
    """

    match tipo:
        case "Importante":
            print("\n")

            print("-"*90)
            print(f"|{'!!':^10}|", f"{negrita('AVISO'):^85}|", sep="")
            print(f"|{'!!':^10}|", f"{'-'*77:^77}|", sep="")
            print(f"|{'!!':^10}|", f"{' ':^77}|", sep="")

            for texto in descripcion:
                print(f"|{'!!':^10}|", f"{texto:^77}|", sep="")

            print(f"|{'':^10}|", f"{'':^77}|", sep="")
            print(f"|{'**':^10}|", f"{' ':^77}|", sep="")

            print("-"*90)

        case "Información":
            print("\n")

            print("-"*90)
            print(f"|{'**':^10}|", f"{negrita('INFORMACIÓN'):^85}|", sep="")
            print(f"|{'':^10}|", f"{'-'*77:^77}|", sep="")
            print(f"|{'II':^10}|", f"{' ':^77}|", sep="")

            for texto in descripcion:
                print(f"|{'II':^10}|", f"{texto:^77}|", sep="")

            print(f"|{'II':^10}|", f"{' ':^77}|", sep="")
            print("-"*90)

        case "Resultado":
            print("\n")

            print("-"*90)
            print(f"|{'':^10}|", f"{negrita('RESULTADO'):^85}|", sep="")
            print(f"|{'====':^10}|", f"{'-'*77:^77}|", sep="")
            print(f"|{'====':^10}|", f"{''*77:^77}|", sep="")

            for texto in descripcion:
                print(f"|{'':^10}|", f"{texto:^77}|", sep="")

            print(f"|{'====':^10}|", f"{'':^77}|", sep="")
            print(f"|{'====':^10}|", f"{'':^77}|", sep="")
            print(f"|{'':^10}|", f"{' ':^77}|", sep="")
            print("-"*90)

def exportar_excel(*dataframes: pd.DataFrame, nombre_archivo: str = "resultado") -> None:
    """Exporta uno o más dataframes a excel.

    Args:
        *dataframes (Dataframe): Dataframes a exportar. Puede ser uno o muchos.
        nombre_archivo (str, optional): Nombre del archivo que se guardará. Defaults to "resultado".
    """

    dataframes = [dataframe for dataframe in dataframes]

    try:
        if len(dataframes) == 1:
            dataframes[0].to_excel(f'{nombre_archivo}.xlsx', sheet_name="Hoja 1")
        else:
            with pd.ExcelWriter(f'{nombre_archivo}.xlsx') as writer:
                for hoja, dataframe in enumerate(dataframes):
                    dataframe.to_excel(writer, sheet_name=f'Hoja {hoja + 1}')
    except PermissionError:
        print("Error: El archivo ya está abierto. Ciérrelo y vuelva a intentarlo.")
    else:
        mostrar_aviso([f'Archivo exportado exitosamente a {nombre_archivo}.xlsx'], tipo = "Información")

def negrita(texto: str) -> str:
    """Retorna un F-string con un formato de negritas.

    Args:
        texto (str): Texto que será convertido a negritas.

    Returns:
        str: F-string con el estilo aplicado.
    """

    # \033[1m - Inicio de negritas
    # \033[0m - Fin de negritas

    return f'\033[1m{texto}\033[0m'

def pedir_salida() -> None | Exception:
    """Pregunta al usuario si quiere regresar al menú principal.

    Raises:
        Salir: Excepción que regresa al menú principal.

    Returns:
        None | Exception: Lanza la excepción sólo si el usuario acepta salir.
    """

    titulo = '¿Desea regresar al menú principal?'
    contenido = [
        '(S) - Sí',
        '(N) - No'
    ]

    mostrar_cuadro(contenido, titulo)

    print(f"{negrita('Respuesta: ')}", end="")

    salida = input().capitalize()

    if salida == "S":
        raise Salir

def pedir_campo(mensaje: str) -> str:
    """Pide al usuario que introduzca un campo no vacío.

    Args:
        mensaje (str): Mensaje que se mostrará al usuario.

    Raises:
        ValueError: Si el usuario dejó el campo vacío.

    Returns:
        str: Mensaje ya validado.
    """

    while True:
        try:
            entrada = input(mensaje).strip()

            if not entrada:
                raise ValueError("El campo no puede estar vacío")

            return entrada

        except ValueError as e:
            print(f"{negrita('Error')}: {e}")

            pedir_salida()

            continue

def pedir_numero(mensaje: str, min: int = None, max: int = None) -> int:
    """Pide que el usuario introduzca un número válido.

    Args:
        mensaje (str): Mensaje que se mostrará al usuario.
        min (int, optional): Valor mínimo. Defaults to None.
        max (int, optional): Valor máximo. Defaults to None.

    Raises:
        ValueError: El número es menor al mínimo especificado.
        ValueError: El número es mayor al máximo especificado.

    Returns:
        int: Número ya validado.
    """

    while True:
        try:
            entrada = int(pedir_campo(mensaje))

            #Checamos de manera individual si se especificó cada parámetro
            #y lo comparamos con la entrada en caso verdadero.
            if (min is not None):
                if entrada < min:
                    raise ValueError(f"El número debe ser mayor o igual a {min}")

            if (max is not None):
                if entrada > max:
                    raise ValueError(f"El número debe ser menor o igual a {max}")


            return entrada

        except ValueError as e:
            print(f"{negrita('Error')}: {e}")

            pedir_salida()
            continue

def mostrar_cuadro(contenido: list, titulo:str = None, subtitulo:str = None):
    """Muestra un cuadro que contiene el texto que se le pase como parámetro.

    Args:
        contenido (list): Lista de strings. Cada elemento representa una línea.
        titulo (str, optional): Título del cuadro. Defaults to None.
        subtitulo (str, optional): Subtítulo del cuadro. Defaults to None.
    """

    print("\n")
    print("-"*92)

    if titulo:
        print(f"|{negrita(titulo):^98}|")
        print(f"|{'-'*90}|")
    if subtitulo:
        print(f"|{negrita(subtitulo):^98}|")
        print(f"|{" ":^90}|")
    for linea in contenido:
        print(f"|{linea:^90}|")

    print("-"*92)

######################## PUNTO DE EQUILIBRIO ########################
def punto_equilibrio_menu() -> None:
    """Menú que muestra las opciones para el punto de equilibrio."""

    titulo = 'Usted escogió: Punto de equilibrio'
    subtitulo = 'Escoja el tipo de cálculo que le gustaría realizar'
    opciones = [
        '(1) - Normal',
        '(2) - Multilínea',
        '(3) - Regresar al menú principal'
    ]

    while True:

        mostrar_cuadro(opciones, titulo, subtitulo)

        opcion = pedir_numero(f"{negrita('Escribe el número de la opción que vas a escoger: ')}", 1, 3)

        match opcion:
            case 1:
                punto_equilibrio_normal()
            case 2:
                punto_equilibrio_multilinea()
            case 3:
                return

def punto_equilibrio_normal() -> None:
    """Función que muestra una interfaz para determinar el punto de equilibrio normal."""

    try:
        mostrar_cuadro(["1. Ingrese el precio de venta"])
        precio_venta = pedir_numero("Valor del precio de venta: ", 0)

        mostrar_cuadro(["2. Ingrese el costo variable"])
        costo_variable = pedir_numero("Valor del costo variable: ", 0)

        mostrar_cuadro(["3. Ingrese el costo fijo"])
        costo_fijo = pedir_numero("Valor del costo fijo: ", 0)

        margen_contribucion_unitario = precio_venta - costo_variable
        punto_equilibrio_unidades = costo_fijo / margen_contribucion_unitario
        punto_equilibrio_pesos = punto_equilibrio_unidades * precio_venta

        contenido = [
            f'El punto de equilibrio en unidades es: {punto_equilibrio_unidades}',
            f'El punto de equilibrio en pesos es: ${punto_equilibrio_pesos:,.2f}'
        ]

        mostrar_aviso(contenido, tipo='Resultado')

        sleep(5)

    except ZeroDivisionError:
        print(f"{negrita('Error')}: división por cero.")




def punto_equilibrio_multilinea() -> None:
    """Función que muestra una interfaz para determinar el punto de equilibrio multilínea."""

    contador_productos = 1

    datos = {} #Usamos primero un diccionario para recolectar los datos

    suma_porcentaje = 0 #Utilizado para verificar que no se pase del 100%

    #Recolección de datos
    while True:

        mostrar_cuadro([f'Producto {contador_productos}'])

        nombre_producto = pedir_campo('Escriba el nombre del producto: ')
        porcentaje_margen_contribucion = pedir_numero('Escriba el porcentaje del margen de contribución: ', 0, 100)
        suma_porcentaje += porcentaje_margen_contribucion

        if suma_porcentaje > 100:
            mostrar_aviso(['La suma del porcentaje superó el 100%'])

            contenido = [
                '¿Está seguro de querer continuar?',
                '(S) - Sí',
                '(N) - No'
            ]

            mostrar_cuadro(contenido)

            print("\n")
            confirmar = pedir_campo("Respuesta: ").capitalize()

            if confirmar == "N":
                break


        precio_venta = pedir_numero('Escriba el precio de venta: ', 0)
        costo_variable = pedir_numero('Escriba el costo variable: ', 0)
        margen_contribucion = pedir_numero('Escriba el margen de contribución: ', 0)

        datos[nombre_producto] = [porcentaje_margen_contribucion, precio_venta, costo_variable, margen_contribucion]

        contador_productos += 1

        contenido = [
            '¿Quiere añadir otro producto?',
            '(S) - Sí',
            '(N) - No'
        ]

        mostrar_cuadro(contenido)

        continuar = pedir_campo("Respuesta: ").capitalize()

        if continuar == "N":
            break

    #Conversión a Dataframe
    df_datos = pd.DataFrame(datos)
    df_datos.index = ['% de Margen de contribución', 'Precio de venta', 'Costo variable', 'Margen de contribución']

    #Pedimos el costo fijo para las operaciones posteriores
    costo_fijo = pedir_numero('Escriba el costo fijo: ', 0)

    #Parte donde se calcula el margen de contribución ponderado y unitario
    margen_ponderado = {}
    margen_contribucion_unitario = 0

    for nombre, informacion in datos.items():
        #Obtenemos los datos necesarios para el cálculo
        margen_contribucion = informacion[3]
        porcentaje_margen_contribucion = informacion[0]

        #Cálculos requeridos
        margen_contribucion_ponderado = margen_contribucion * (porcentaje_margen_contribucion / 100)
        margen_contribucion_unitario += margen_contribucion_ponderado

        #Lo añadimos al diccionario
        margen_ponderado[nombre] = [margen_contribucion, porcentaje_margen_contribucion, margen_contribucion_ponderado]

    #Lo convertimos a DataFrame para su posterior uso
    df_margen_ponderado = pd.DataFrame(margen_ponderado)
    df_margen_ponderado.index = ['Margen de contribución', 'Porcentaje del margen de contribución', 'Margen de contribución ponderado']

    #Parte donde calculamos el punto de equilibrio en unidades y su ponderación
    punto_equilibrio_unidades = costo_fijo / margen_contribucion_unitario

    dict_punto_equilibrio_unidades = {}
    for producto, informacion in datos.items():
        porcentaje_margen_contribucion = informacion[0]
        punto_equilibrio_por_unidad = punto_equilibrio_unidades * (porcentaje_margen_contribucion / 100)

        dict_punto_equilibrio_unidades[producto] = [porcentaje_margen_contribucion,
                                                    punto_equilibrio_unidades,
                                                    punto_equilibrio_por_unidad]

    df_punto_equilibrio_unidades = pd.DataFrame(dict_punto_equilibrio_unidades)
    df_punto_equilibrio_unidades.index = ['Porcentaje del margen de contribución', 'Punto de equilibrio en unidades', 'Punto de equilibrio por unidad']

    #Parte donde calculamos el punto de equilibrio en pesos
    dict_punto_equilibrio_pesos = {}
    total_punto_equilibrio_pesos = 0

    for producto, informacion in dict_punto_equilibrio_unidades.items():
        punto_equilibrio_por_unidad = informacion[2]
        precio_venta = datos[producto][1]

        punto_equilibrio_pesos = punto_equilibrio_por_unidad * precio_venta
        total_punto_equilibrio_pesos += punto_equilibrio_pesos

        dict_punto_equilibrio_pesos[producto] = [punto_equilibrio_por_unidad, precio_venta, punto_equilibrio_pesos]

    df_punto_equilibrio_pesos = pd.DataFrame(dict_punto_equilibrio_pesos)
    df_punto_equilibrio_pesos.index = ['Punto de equilibrio por unidad', 'Precio de venta', 'Punto de equilibrio en pesos']

    mostrar_aviso(['Su resultado se encuentra listo'], tipo = "Información")

    exportar_excel(df_datos, df_margen_ponderado, df_punto_equilibrio_unidades, df_punto_equilibrio_pesos, nombre_archivo="punto_equilibrio")

    #Usamos las matrices transpuestas porque intercambiar las filas por las columnas.
    descripcion = [
        f'El punto de equilibrio en unidades es: {punto_equilibrio_unidades}',
        f'El punto de equilibrio en pesos es: ${total_punto_equilibrio_pesos:,.2f}'
    ]
    mostrar_aviso(descripcion, tipo = "Resultado")

    mostrar_aviso(['A continuación se mostrarán las tablas'], tipo = "Información")

    mostrar_cuadro(['Datos'])
    print(tabulate(df_datos, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))

    mostrar_cuadro(['Ponderación de margen'])
    print(tabulate(df_margen_ponderado, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))

    mostrar_cuadro(['Ponderación de punto de equilibrio (unidades)'])
    print(tabulate(df_punto_equilibrio_unidades.T, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))

    mostrar_cuadro(['Ponderación de punto de equilibrio (pesos)'])
    print(tabulate(df_punto_equilibrio_pesos.T, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))

    sleep(5)

######################## UNIDADES ANTES Y DESPUÉS DE IMPUESTOS ########################
def unidades_impuestos_menu() -> None:
    """Función que muestra un menú para la opción de unidades de impuestos."""

    título = "Unidades antes/después de impuestos"
    subtítulo = "Escoja el tipo de cálculo que le gustaría realizar"
    opciones = [
        '(1) - Unidad antes de impuestos normal',
        '(2) - Unidad antes de impuestos multilínea',
        '(3) - Unidad después de impuestos normal',
        '(4) - Unidad después de impuestos multilínea',
        '(5) - Regresar'
    ]

    while True:
        mostrar_cuadro(opciones, título, subtítulo)

        opcion = pedir_numero(f"{negrita('Escribe el número de la opción que vas a escoger: ')}", 1, 5)

        match opcion:
            case 1:
                unidad_antes_de_impuestos_normal()
            case 2:
                unidad_antes_de_impuestos_multilinea()
            case 3:
                unidad_despues_de_impuestos_normal()
            case 4:
                unidad_despues_impuestos_multilinea()
            case 5:
                return

def unidad_antes_de_impuestos_normal(exportar: bool = False) -> None | float:
    """Calcula las unidades a vender antes de impuestos normal.

        Args:
            exportar (bool, optional): True si se quiere exportar el diccionario que contiene los datos del presupuesto. Defaults to False.
        Returns:
            None: Si no se especifica que se va a exportar.
            float: Unidades a vender antes de impuestos.
    """

    print("\n")

    mostrar_cuadro(["Escriba el costo fijo total"])
    costo_fijo_total = pedir_numero("Valor del costo fijo total: ", 0)

    mostrar_cuadro(["Escriba la utilidad deseada"])
    utilidad_deseada = pedir_numero("Valor de la utilidad deseada: ", 0)

    mostrar_cuadro(["Escriba el margen de contribución unitario"])
    margen_contribucion_unitario = pedir_numero("Valor del margen de contribución unitario: ", 0)

    unidades_antes_impuestos = (costo_fijo_total + utilidad_deseada) / margen_contribucion_unitario

    contenido = [f'Unidades a vender antes de impuestos: {unidades_antes_impuestos}']
    mostrar_aviso(contenido, tipo = 'Resultado')

    sleep(5)

    if exportar:
        return unidades_antes_impuestos

def unidad_despues_de_impuestos_normal(exportar: bool = False) -> None | float:
    """Calcula las unidades a vender después de impuestos normal.

        Args:
            exportar (bool, optional): True si se quiere exportar el diccionario que contiene los datos del presupuesto. Defaults to False.
        Returns:
            None: Si no se especifica que se va a exportar.
            float: Unidades a vender después de impuestos.
    """

    mostrar_cuadro(["Escriba el costo fijo total"])
    costo_fijo_total = pedir_numero("Valor del costo fijo total: ", 0)

    mostrar_cuadro(["Escriba la utilidad deseada"])
    utilidad_deseada = pedir_numero("Valor de la utilidad deseada: ", 0)

    mostrar_cuadro(["Escriba el margen de contribución unitario"])
    margen_contribucion_unitario = pedir_numero("Valor del margen de contribución unitario: ", 0)

    mostrar_cuadro(["Escriba la tasa impositiva"])
    tasa_impositiva = pedir_numero("Valor de la tasa impositiva (0 - 100): ", 0, 100) / 100

    unidades_despues_impuestos = (
        (costo_fijo_total + (utilidad_deseada / (1 - tasa_impositiva)))
        / margen_contribucion_unitario)

    contenido = [f'Unidades a vender después de impuestos: {unidades_despues_impuestos}']
    mostrar_aviso(contenido, tipo = 'Resultado')

    if exportar:
        return unidades_despues_impuestos

def unidad_antes_de_impuestos_multilinea() -> None:
    """Calcula las unidades antes de impuestos multilínea."""

    mostrar_aviso(['Primero deberá determinar la utilidad antes de impuestos normal'], tipo = "Información")

    unidad_antes_impuestos = unidad_antes_de_impuestos_normal(exportar= True)

    mostrar_aviso(['A continuación, deberá especificar los datos de los productos que tiene.'], tipo = "Información")

    contador_productos = 1
    suma_porcentaje_participacion = 0

    datos = {}

    while True:
        mostrar_cuadro([f'Producto {contador_productos}'])
        nombre_producto = pedir_campo('Escriba el nombre del producto: ')
        porcentaje_participacion = pedir_numero('Escriba el porcentaje de participación (0 - 100): ', 0, 100)

        suma_porcentaje_participacion += porcentaje_participacion
        if suma_porcentaje_participacion > 100:
            mostrar_aviso(['La suma del porcentaje superó el 100%'])

            contenido = [
                '¿Está seguro de querer continuar?',
                '(S) - Sí',
                '(N) - No'
            ]

            mostrar_cuadro(contenido)

            continuar = pedir_campo(f"{negrita('Escriba su respuesta: ')}").capitalize()

            if continuar == 'N':
                break

        unidad_antes_impuestos_ponderada = unidad_antes_impuestos * (porcentaje_participacion / 100)
        datos[nombre_producto] = [porcentaje_participacion, unidad_antes_impuestos, unidad_antes_impuestos_ponderada]

        contador_productos += 1

        contenido = ['¿Quiere añadir otro producto?',
                     '(S) - Sí',
                     '(N) - No']
        mostrar_cuadro(contenido)

        continuar = pedir_campo(f"{negrita('Escriba su respuesta: ')}").capitalize()

        if continuar == 'N':
            break

    df_datos = pd.DataFrame(datos)
    df_datos.index = ['% Participación', 'Total Uds', 'Uds. antes de impuestos']

    exportar_excel(df_datos.T, nombre_archivo="unidades_antes_de_impuestos")

    mostrar_cuadro(['Ponderación'])
    print(tabulate(df_datos.T, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))

    sleep(5)

def unidad_despues_impuestos_multilinea() -> None:
    """Calcula las unidades después de impuestos multilínea."""

    mostrar_aviso(['Primero deberá determinar la utilidad antes de impuestos normal'], tipo = "Información")

    unidad_despues_impuestos = unidad_despues_de_impuestos_normal(exportar= True)

    mostrar_aviso(['A continuación, deberá especificar los datos de los productos que tiene.'], tipo = "Información")

    contador_productos = 1
    suma_porcentaje_participacion = 0

    datos = {}

    while True:
        mostrar_cuadro([f'Producto {contador_productos}'])
        nombre_producto = pedir_campo('Escriba el nombre del producto: ')
        porcentaje_participacion = pedir_numero('Escriba el porcentaje de participación (0 - 100): ', 0, 100)

        suma_porcentaje_participacion += porcentaje_participacion
        if suma_porcentaje_participacion > 100:
            mostrar_aviso(['La suma del porcentaje superó el 100%'])

            contenido = [
                '¿Está seguro de querer continuar?',
                '(S) - Sí',
                '(N) - No'
            ]

            mostrar_cuadro(contenido)

            continuar = pedir_campo(f"{negrita('Escriba su respuesta: ')}").capitalize()

            if continuar == 'S':
                break

        unidad_despues_impuestos_ponderada = unidad_despues_impuestos * (porcentaje_participacion / 100)
        datos[nombre_producto] = [porcentaje_participacion, unidad_despues_impuestos, unidad_despues_impuestos_ponderada]

        contador_productos += 1

        contenido = ['¿Quiere añadir otro producto?',
                     '(S) - Sí',
                     '(N) - No']
        mostrar_cuadro(contenido)

        continuar = pedir_campo(f"{negrita('Escriba su respuesta: ')}").capitalize()

        if continuar == 'N':
            break

    df_datos = pd.DataFrame(datos)
    df_datos.index = ['% Participación', 'Total Uds', 'Uds. después de impuestos']

    exportar_excel(df_datos, nombre_archivo="unidades_despues_de_impuestos")

    mostrar_cuadro(['Ponderación'])
    print(tabulate(df_datos.T, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))

    sleep(5)

######################## ANÁLISIS COSTO - VOLUMEN - UTILIDAD ########################

def analisis_cvu_menu() -> None:
    """Muestra al usuario un menú para iniciar el análisis Costo - Volumen - Utilidad."""

    titulo = 'Análisis Costo - Volumen - Utilidad'
    subtitulo = '¿Qué quiere hacer?'
    contenido = ['(1) - Iniciar Análisis Costo - Volumen - Utilidad',
                 '(2) - Regresar al menú principal']

    while True:
        mostrar_cuadro(contenido, titulo, subtitulo)
        opcion = pedir_numero(f'{negrita("Escriba el número de la opción que vas a escoger: ")}', 1, 2)

        match opcion:
            case 1:
                analisis_cvu()
            case 2:
                return

def analisis_cvu() -> None:
    """Se le muestra una interfaz al usuario para realizar el análisis Costo - Volumen - Utilidad."""

    print("\n")
    mostrar_cuadro(['Bienvenido al análisis Costo - Volumen - Utilidad'])

    propuestas = {
        "actual":
        {
            "Precio de venta": 0,
            "Costos Variables": 0,
            "Costos Fijos": 0,
            "Ventas": 0
        }
    }

    for dato in propuestas["actual"].keys():
        titulo = f'{dato}'
        contenido = [f'Escriba el valor numérico de {dato}']
        mostrar_cuadro(contenido, titulo)

        valor = pedir_numero(f"Valor numérico de {dato}: ", 0)
        propuestas["actual"][dato] = valor


    propuestas_calculos = {
        "actual":
        {
            "Ingreso": propuestas["actual"]["Ventas"] * propuestas["actual"]["Precio de venta"],
            "Costo Variable": propuestas["actual"]["Costos Variables"],
        }
    }

    propuestas_calculos["actual"]["Margen de Contribución"] = propuestas_calculos["actual"]["Ingreso"] - propuestas['actual']['Costos Variables']
    propuestas_calculos["actual"]["Costo Fijo"] = propuestas["actual"]["Costos Fijos"]
    propuestas_calculos["actual"]["Utilidad de Operación"] = propuestas_calculos["actual"]["Margen de Contribución"] - propuestas["actual"]["Costos Fijos"]

    print("\n")

    mostrar_aviso(['A continuación, usted deberá introducir la cantidad de propuestas que tiene,',
                   'las cuales se compararán con los datos que proporcionó anteriormente.'],
                   tipo = "Información")

    num_propuestas = pedir_numero(f"{negrita('Escriba la cantidad de propuestas a realizar: ')}")

    for propuesta in range(1, num_propuestas + 1): #Le añadimos uno porque el range no toma en cuenta el último valor

        propuestas[propuesta] = {}

        mostrar_cuadro([f'Propuesta {propuesta}'])


        for dato in propuestas["actual"].keys():
            dato_original = propuestas["actual"][dato]

            titulo = f"¿Qué quieres hacer con {dato}?"
            contenido = [
                '(1) - Aumentar valor (% porcentaje)',
                '(2) - Aumentar valor (cantidad)',
                '(3) - Disminuir valor (% porcentaje)',
                '(4) - Disminuir valor (cantidad)',
                '(5) - Mantener el valor actual'
            ]

            mostrar_cuadro(contenido, titulo)

            opcion = pedir_numero(f"{negrita('Escriba el número de la opción que vas a escoger: ')}", 1, 5)

            match opcion:
                case 1:
                    mostrar_cuadro([f'Usted escogió aumentar el valor de {dato} en porcentaje'])
                    cantidad_aumento = pedir_numero('Escriba el porcentaje que desea aumentar: ', 0, 100)
                    propuestas[propuesta][dato] = dato_original * (1 + (cantidad_aumento / 100))
                case 2:
                    mostrar_cuadro([f'Usted escogió aumentar el valor de {dato} en cantidad ($)'])
                    cantidad_aumento = pedir_numero('Escriba la cantidad que desea aumentar: ', 0)
                    propuestas[propuesta][dato] = dato_original + cantidad_aumento
                case 3:
                    mostrar_cuadro([f'Usted escogió disminuir el valor de {dato} en porcentaje'])
                    cantidad_aumento = pedir_numero('Escriba el porcentaje que desea disminuir: ', 0, 100)
                    propuestas[propuesta][dato] = dato_original - (dato_original * (cantidad_aumento / 100))
                case 4:
                    mostrar_cuadro([f'Usted escogió disminuir el valor del {dato} en cantidad ($)'])
                    cantidad_aumento = pedir_numero('Escriba la cantidad que desea disminuir: ', 0)
                    propuestas[propuesta][dato] = dato_original - cantidad_aumento
                case 5:
                    propuestas[propuesta][dato] = dato_original

        propuestas_calculos[propuesta] = {
                "Ingreso": propuestas[propuesta]["Ventas"] * propuestas[propuesta]["Precio de venta"],
                "Costo Variable": propuestas[propuesta]["Costos Variables"],
        }

        propuestas_calculos[propuesta]["Margen de Contribución"] = propuestas_calculos[propuesta]["Ingreso"] - propuestas[propuesta]["Costos Variables"]
        propuestas_calculos[propuesta]["Costo Fijo"] = propuestas[propuesta]["Costos Fijos"]
        propuestas_calculos[propuesta]["Utilidad de Operación"] = propuestas_calculos[propuesta]["Margen de Contribución"] - propuestas[propuesta]["Costos Fijos"]

    df_propuestas_calculos = pd.DataFrame(propuestas_calculos)
    df_propuestas = pd.DataFrame(propuestas)


    exportar_excel(df_propuestas, df_propuestas_calculos, nombre_archivo="analisis_cvu")

    mostrar_cuadro(['Análisis'])
    print(tabulate(df_propuestas_calculos, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))
    print(tabulate(df_propuestas, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))

    sleep(5)

######################## PRESUPUESTO DE VENTAS Y PRODUCCIÓN ########################

def presupuesto_ventas_produccion_menu() -> None:
    """Muestra al usuario un menú para escoger el presupuesto que hará."""

    titulo = "Presupuesto de ventas y producción"
    subtitulo = "Escoja el tipo de cálculo que le gustaría realizar"
    contenido = ['(1) - Presupuesto de ventas',
        '(2) - Presupuesto de producción',
        '(3) - Regresar al menú principal']

    while True:
        mostrar_cuadro(contenido, titulo, subtitulo)
        opcion = pedir_numero('Escriba el número de la opción: ', 1, 3)

        match opcion:
            case 1:
                presupuesto_ventas()
            case 2:
                presupuesto_producción()
            case 3:
                return


def presupuesto_ventas(exportar: bool = False) -> None | dict:
    """Muestra una interfaz al usuario para realizar el presupuesto de ventas.

    Args:
        exportar (bool, optional): True si se quiere exportar el diccionario que contiene los datos del presupuesto. Defaults to False.

    Returns:
        None | dict: None si no se expecifica que se quiere exportar el diccionario.
    """

    mostrar_cuadro(['Escriba la cantidad de productos que tiene'])
    num_productos = pedir_numero('Cantidad de productos: ', 0)

    datos = {}

    for producto in range(0, num_productos):
        mostrar_cuadro([f'Producto {producto + 1}'])
        nombre = pedir_campo('Escriba el nombre del producto: ')
        pronostico_ventas = pedir_numero('Pronóstico de ventas: ', 0)
        precio_unitario = pedir_numero('Precio unitario (escriba el número 1 si no tiene este dato): ', 1)
        ventas_presupuestadas = pronostico_ventas * precio_unitario

        datos[nombre] = {
            "Pronóstico de ventas": pronostico_ventas,
            "Precio unitario": precio_unitario,
            "Ventas presupuestadas": ventas_presupuestadas
        }

    df_datos = pd.DataFrame(datos)
    df_datos.index = ['Pronóstico de ventas', 'Precio unitario', 'Ventas presupuestadas']

    exportar_excel(df_datos, nombre_archivo="presupuesto_ventas")

    mostrar_cuadro(['Resultado del presupuesto de ventas'])
    print(tabulate(df_datos, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))

    sleep(5)

    if exportar:
        return datos

def presupuesto_producción() -> None:
    """Muestra una interfaz al usuario para la realización del presupuesto de producción."""

    mostrar_aviso(['Primero usted deberá realizar el presupuesto de ventas,'
                   'debido a que se requieren ciertos datos de este.'], tipo = "Información")
    datos_ventas = presupuesto_ventas(exportar = True)

    mostrar_aviso(['A continuación, se iniciará el proceso del presupuesto de producción'], tipo = "Información")
    datos_produccion = {}

    for producto, informacion in datos_ventas.items():
        mostrar_cuadro([f'Producto {producto}'])
        ventas = informacion['Ventas presupuestadas']
        inventario_final = pedir_numero('Escriba el inventario final deseado de producto terminado: ', 0)
        inventario_inicial = pedir_numero('Escriba el inventario inicial de producto terminado: ', 0)
        produccion_requerida = (ventas + inventario_final) - inventario_inicial

        datos_produccion[producto] = {
            "Pronóstico de ventas": ventas,
            "Inventario final": inventario_final,
            "Inventario inicial": inventario_inicial,
            "Producción requerida": produccion_requerida
        }

    #En esta parte calculamos los datos de la columna de total para después añadirlos
    total_pronóstico_ventas = 0
    total_inventario_inicial = 0
    total_inventario_final = 0
    total_produccion_requerida = 0

    for producto, informacion in datos_produccion.items():
        total_pronóstico_ventas += informacion["Pronóstico de ventas"]
        total_inventario_final += informacion["Inventario final"]
        total_inventario_inicial += informacion["Inventario inicial"]
        total_produccion_requerida += informacion["Producción requerida"]


    datos_produccion["Total"] = {
        "Pronóstico de ventas": total_pronóstico_ventas,
        "Inventario final": total_inventario_final,
        "Inventario inicial": total_inventario_inicial,
        "Producción requerida": total_produccion_requerida
    }

    df_datos_producción = pd.DataFrame(datos_produccion)
    df_datos_producción.index = ['Pronóstico de ventas', 'Inventario final', 'Inventario inicial', 'Producción requerida']

    exportar_excel(df_datos_producción, nombre_archivo="presupuesto_producción")

    mostrar_cuadro(['Resultado del presupuesto de producción'])
    print(tabulate(df_datos_producción, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))

    sleep(5)

######################## PRESUPUESTO DE NECESIDADES DE MATERIAS PRIMAS Y COMPRAS ########################

def presupuesto_necesidades_menu() -> None:
    """Muestra un menú para iniciar el prespuesto de necesidades de materias primas y compras."""

    titulo = "Presupuesto de necesidades de materias primas y compras"
    subtitulo = "Escoja el tipo de cálculo que le gustaría realizar"
    contenido = ['(1) - Presupuesto de necesidades de materias primas y compras',
            '(2) - Regresar al menú principal']

    while True:
        mostrar_cuadro(contenido, titulo, subtitulo)
        opcion = pedir_numero('Escriba el número de la opción: ', 1, 3)

        match opcion:
            case 1:
                presupuesto_necesidades()
            case 2:
                return

def presupuesto_necesidades() -> None:
    """Se le muestra una interfaz al usuario para la realización del presupuesto de necesidades de materias primas y compras."""

    mostrar_aviso(['En este programa, este presupuesto se hará por producto',
                   'por lo que puede requerir hacerlo muchas veces',
                   'si tiene muchos productos.'])

    mostrar_cuadro(['Escriba la producción requerida para el producto'])
    produccion_requerida = pedir_numero('Producción requerida: ', 0)

    mostrar_cuadro(['Escriba la cantidad de componentes (o ingredientes) que utiliza para fabricar el producto'])
    num_componentes = pedir_numero('Cantidad de componentes: ', 0)

    datos = {}

    for componente in range(0, num_componentes):
        mostrar_cuadro([f'Componente {componente + 1}'])
        nombre = pedir_campo('Escriba el nombre del componente: ')
        materia_prima_unidad = pedir_numero('Escriba la materia prima por unidad: ', 0)
        materia_prima_produccion = produccion_requerida * materia_prima_unidad
        inventario_final = pedir_numero('Escriba el inventario final deseado de materia prima: ', 0)
        inventario_inicial = pedir_numero('Escriba el inventario inicial de materia prima: ', 0)
        materia_prima_requerida = (materia_prima_produccion + inventario_final) - inventario_inicial
        costo_materia_prima = pedir_numero('Escriba el costo de materia prima: ', 0)
        compras_presupuestadas = materia_prima_requerida * costo_materia_prima

        datos[nombre] = {
            "Materia prima por unidad": materia_prima_unidad,
            "Materia prima para la producción": materia_prima_produccion,
            "Inventario final deseado de materia prima": inventario_final,
            "Inventario inicial de materia prima": inventario_inicial,
            "Materia prima requerida": materia_prima_requerida,
            "Costo de materia prima": costo_materia_prima,
            "Compras presupuestadas": compras_presupuestadas
        }

    df_datos = pd.DataFrame(datos)
    df_datos.index = ['Materia prima por unidad', 'Materia prima para la producción', 'Inventario final deseado de materia prima', 'Inventario inicial de materia prima', 'Materia prima requerida', 'Costo de materia prima', 'Compras presupuestadas']

    exportar_excel(df_datos, nombre_archivo="presupuesto_necesidades")

    mostrar_cuadro(['Resultado'])
    print(tabulate(df_datos, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))

    sleep(5)

######################## MENÚ PRINCIPAL ########################
def menu() -> None:
    """Función que le muestra el menú principal al usuario."""

    titulo = "Bienvenido al programa contable"
    subtitulo = "Escoge la opción"
    opciones = [
        '(1) - Punto de equilibrio en unidades/pesos normal o multilínea',
        '(2) - Unidades a vender antes/después de impuestos normal o multilínea',
        '(3) - Análisis Costo-Volumen-Utilidad',
        '(4) - Presupuesto de Ventas y Producción',
        '(5) - Presupuesto de necesidades de Materias Primas y Compras',
        '(6) - Salir del programa'
    ]

    while True:
        try:
            mostrar_cuadro(opciones, titulo, subtitulo)
            opcion = pedir_numero(f"{negrita('Escribe el número de la opción que vas a escoger: ')}", 1, 6)

            match opcion:
                case 1:
                    punto_equilibrio_menu()
                case 2:
                    unidades_impuestos_menu()
                case 3:
                    analisis_cvu_menu()
                case 4:
                    presupuesto_ventas_produccion_menu()
                case 5:
                    presupuesto_necesidades_menu()
                case 6:
                    break
        except Salir:
            continue


######################## INICIALIZACIÓN DEL PROGRAMA ########################
if __name__ == "__main__":
    menu()
