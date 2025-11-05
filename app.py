######################## IMPORT Y OPCIONES GLOBALES ########################
import pandas as pd
from tabulate import tabulate

#Cambiamos el formato de los tipos de dato float
pd.set_option('display.float_format', lambda x: '%.9f' % x)


######################## UTILIDADES ########################
class Salir(Exception):
    """Excepción usada para regresar al menú principal."""
    pass


def negrita(texto: str) -> str:
    """Retorna un F-string con un formato de negritas.

    Args:
        texto (str): Texto que será convertido a negritas.

    Returns:
        str: F-string con el estilo aplicado.
    """

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

    print(f"|{" ":^90}|")
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
        print("-"*92)
        precio_venta = pedir_numero("1. Ingrese el precio de venta: ", 0)
        print("-"*92)
        costo_variable = pedir_numero("2. Ingrese el costo variable: ", 0)
        print("-"*92)
        costo_fijo = pedir_numero("3. Ingrese el costo fijo: ", 0)
        print("-"*92)

        margen_contribucion_unitario = precio_venta - costo_variable
        punto_equilibrio_unidades = costo_fijo / margen_contribucion_unitario
        punto_equilibrio_pesos = punto_equilibrio_unidades * precio_venta

        contenido = [
            f'El punto de equilibrio en unidades es: {punto_equilibrio_unidades}',
            f'El punto de equilibrio en pesos es: ${punto_equilibrio_pesos:,.2f}'
        ]

        mostrar_cuadro(contenido)

    except ZeroDivisionError:
        print(f"{negrita('Error')}: división por cero.")




def punto_equilibrio_multilinea() -> None:
    """Función que muestra una interfaz para determinar el punto de equilibrio multilínea."""

    contador_productos = 1

    datos = {} #Usamos primero un diccionario para recolectar los datos

    suma_porcentaje = 0 #Utilizado para verificar que no se pase del 100%

    #Recolección de datos
    while True:
        print("-"*92)
        print(f"|{negrita(f'Producto {contador_productos}'):^98}|")
        print("-"*92)

        nombre_producto = pedir_campo('Escriba el nombre del producto: ')
        porcentaje_margen_contribucion = pedir_numero('Escriba el porcentaje del margen de contribución: ', 0, 100)
        suma_porcentaje += porcentaje_margen_contribucion

        if suma_porcentaje > 100:
            titulo = 'ADVERTENCIA'
            subtitulo = 'La suma de porcentajes proporcionada hasta ahora supera el 100%'
            contenido = [
                '¿Está seguro de querer continuar?',
                '(S) - Sí',
                '(N) - No'
            ]

            mostrar_cuadro(contenido, titulo, subtitulo)

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

        continuar = pedir_campo("Respuesta: ").capitalize()

        if continuar == "N":
            break

    #Conversión a Dataframe
    df_datos = pd.DataFrame(datos)
    df_datos.index = ['% de Margen de contribución', 'Precio de venta', 'Costo variable', 'Margen de contribución']

    #Pedimos el costo fijo para las operaciones posteriores
    costo_fijo = pedir_numero('Escriba el costo fijo: ', 0)

    print("\n")
    print(tabulate(df_datos, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))


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

    print("\n")
    print(tabulate(df_margen_ponderado, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))


    #Parte donde calculamos el punto de equilibrio en unidades y su ponderación
    punto_equilibrio_unidades = costo_fijo / margen_contribucion_unitario

    contenido = [
        f'El punto de equilibrio en unidades es: {punto_equilibrio_unidades:,.2f}',
        'A continuación se mostrará la ponderación'
    ]

    mostrar_cuadro(contenido)

    dict_punto_equilibrio_unidades = {}
    for producto, informacion in datos.items():
        porcentaje_margen_contribucion = informacion[0]
        punto_equilibrio_por_unidad = punto_equilibrio_unidades * (porcentaje_margen_contribucion / 100)

        dict_punto_equilibrio_unidades[producto] = [porcentaje_margen_contribucion,
                                                    punto_equilibrio_unidades,
                                                    punto_equilibrio_por_unidad]

    df_punto_equilibrio_unidades = pd.DataFrame(dict_punto_equilibrio_unidades)
    df_punto_equilibrio_unidades.index = ['Porcentaje del margen de contribución', 'Punto de equilibrio en unidades', 'Punto de equilibrio por unidad']

    print("\n")
    #Usamos la matriz transpuesta para cambiar las columnas por las filas.
    print(tabulate(df_punto_equilibrio_unidades.T, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))


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

    print("\n")
    print(tabulate(df_punto_equilibrio_pesos.T, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))
    print("\n")


    #Impresión de resultados
    contenido = [
            f'El punto de equilibrio en unidades es: {punto_equilibrio_unidades}',
            f'El punto de equilibrio en pesos es: ${total_punto_equilibrio_pesos:,.2f}'
        ]

    mostrar_cuadro(contenido)


    #Parte opcional de exportación
    titulo = '¿Desea exportar los resultados a EXCEL?'
    contenido = [
        '(S) - Sí',
        '(N) - No'
    ]

    mostrar_cuadro(contenido, titulo)
    exportar = pedir_campo("Respuesta: ").capitalize()

    if exportar == "S":
        with pd.ExcelWriter('punto_equilibrio.xlsx') as writer:
            df_datos.to_excel(writer, sheet_name='Datos')
            df_margen_ponderado.T.to_excel(writer, sheet_name='Margen ponderado')
            df_punto_equilibrio_unidades.T.to_excel(writer, sheet_name='Punto de equilibrio en unidades')

    #En esta ocasión lo usamos para que el usuario pueda ver los resultados y escoja si regresar o no al menú.
    pedir_salida()

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

def unidad_antes_de_impuestos_normal():
    """Calcula las unidades a vender antes de impuestos normal."""

    print("\n")
    costo_fijo_total = pedir_numero("Escriba el costo fijo total: ", 0)
    print("-"*92)
    utilidad_deseada = pedir_numero("Escriba la utilidad deseada: ", 0)
    print("-"*92)
    margen_contribucion_unitario = pedir_numero("Escriba el margen de contribución unitario: ", 0)
    print("-"*92)
    unidades_antes_impuestos = (costo_fijo_total + utilidad_deseada) / margen_contribucion_unitario

    contenido = [f'Unidades a vender antes de impuestos: {unidades_antes_impuestos}']

    mostrar_cuadro(contenido)

    return unidades_antes_impuestos

def unidad_despues_de_impuestos_normal():
    """Calcula las unidades a vender después de impuestos normal."""

    print("\n")
    costo_fijo_total = pedir_numero("Escriba el costo fijo total: ", 0)
    print("-"*92)
    utilidad_deseada = pedir_numero("Escriba la utilidad deseada: ", 0)
    print("-"*92)
    margen_contribucion_unitario = pedir_numero("Escriba el margen de contribución unitario: ", 0)
    print("-"*92)
    tasa_impositiva = pedir_numero("Escriba la tasa impositiva (0 - 100)", 0, 100) / 100

    unidades_despues_impuestos = (
        (costo_fijo_total + (utilidad_deseada / (1 - tasa_impositiva)))
        / margen_contribucion_unitario)

    contenido = [f'Unidades a vender después de impuestos: {unidades_despues_impuestos}']

    mostrar_cuadro(contenido)

    return unidades_despues_impuestos

def unidad_antes_de_impuestos_multilinea():

    contenido = ['PASO 1: Determinación de unidades antes de impuestos normal']
    mostrar_cuadro(contenido)

    unidad_antes_impuestos = unidad_antes_de_impuestos_normal()

    contenido = ['PASO 2: Ponderación']
    mostrar_cuadro(contenido)

    contador_productos = 1
    suma_porcentaje_participacion = 0

    datos = {}

    while True:
        mostrar_cuadro([f'Producto {contador_productos}'])
        nombre_producto = pedir_campo('Escriba el nombre del producto: ')
        porcentaje_participacion = pedir_numero('Escriba el porcentaje de participación (0 - 100): ', 0, 100)

        suma_porcentaje_participacion += porcentaje_participacion
        if suma_porcentaje_participacion > 100:
            título = 'ADVERTENCIA'
            subtítulo = 'La suma de porcentaje de participación excede del 100%'
            contenido = ['¿Quiere continuar?',
                         '(S) - Sí',
                         '(N) - No']
            mostrar_cuadro(contenido, título, subtítulo)

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

    print(tabulate(df_datos.T, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))

    #Parte opcional de exportación
    titulo = '¿Desea exportar los resultados a EXCEL?'
    contenido = [
        '(S) - Sí',
        '(N) - No'
    ]

    mostrar_cuadro(contenido, titulo)
    exportar = pedir_campo("Respuesta: ").capitalize()

    if exportar == "S":
        df_datos.to_excel('unidades_antes_de_impuestos.xlsx')

def unidad_despues_impuestos_multilinea():
    contenido = ['PASO 1: Determinación de unidades después de impuestos normal']
    mostrar_cuadro(contenido)

    unidad_despues_impuestos = unidad_despues_de_impuestos_normal()

    contenido = ['PASO 2: Ponderación']
    mostrar_cuadro(contenido)

    contador_productos = 1
    suma_porcentaje_participacion = 0

    datos = {}

    while True:
        mostrar_cuadro([f'Producto {contador_productos}'])
        nombre_producto = pedir_campo('Escriba el nombre del producto: ')
        porcentaje_participacion = pedir_numero('Escriba el porcentaje de participación (0 - 100): ', 0, 100)

        suma_porcentaje_participacion += porcentaje_participacion
        if suma_porcentaje_participacion > 100:
            título = 'ADVERTENCIA'
            subtítulo = 'La suma de porcentaje de participación excede del 100%'
            contenido = ['¿Quiere continuar?',
                         '(S) - Sí',
                         '(N) - No']
            mostrar_cuadro(contenido, título, subtítulo)

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

    print(tabulate(df_datos.T, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))

    #Parte opcional de exportación
    titulo = '¿Desea exportar los resultados a EXCEL?'
    contenido = [
        '(S) - Sí',
        '(N) - No'
    ]

    mostrar_cuadro(contenido, titulo)
    exportar = pedir_campo("Respuesta: ").capitalize()

    if exportar == "S":
        df_datos.to_excel('unidades_despues_de_impuestos.xlsx')
        print('Exportación hecha de manera exitosa.')

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
                    pass
                case 4:
                    pass
                case 5:
                    pass
                case 6:
                    break
        except Salir:
            continue


######################## INICIALIZACIÓN DEL PROGRAMA ########################
if __name__ == "__main__":
    menu()
