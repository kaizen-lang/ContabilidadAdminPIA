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

    print("\n")
    print("-"*92)
    print(f"|{'¿Desea regresar al menú principal?':^90}|")
    print(f"|{'-'*90}|")
    print(f"|{'(S) - Sí':^90}|")
    print(f"|{'(N) - No':^90}|")
    print("-"*92)
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

######################## PUNTO DE EQUILIBRIO ########################
def punto_equilibrio_menu() -> None:
    """Menú que muestra las opciones para el punto de equilibrio."""

    while True:

        print("-"*92)
        print(f"|{negrita('Usted escogió: Punto de equilibrio'):^98}|")
        print(f"|{'-'*90}|")
        print(f"|{"¿Normal o multilínea?":^90}|")
        print(f"|{"(1) - Normal":^90}|")
        print(f"|{"(2) - Multilínea":^90}|")
        print(f"|{"(3) - Regresar al menú principal":^90}|")
        print("-"*92)

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

        print("\n")
        print("-"*92)
        print(f"|{f'El punto de equilibrio en unidades es: {punto_equilibrio_unidades}':^90}|")
        print(f"|{f'El punto de equilibrio en pesos es: {punto_equilibrio_pesos}':^90}|")
        print("-"*92)
        print("\n")

    except ZeroDivisionError:
        print(f"{negrita('Error')}: división por cero.")




def punto_equilibrio_multilinea() -> None:
    """Función que muestra una interfaz para determinar el punto de equilibrio multilínea."""

    contador_productos = 1

    df_datos = pd.DataFrame() #DataFrame que contendrá los datos del problema

    suma_porcentaje = 0 #Utilizado para verificar que no se pase del 100%

    while True:
        print("-"*92)
        print(f"|{negrita(f'Producto {contador_productos}'):^98}|")
        print("-"*92)

        nombre_producto = pedir_campo('Escriba el nombre del producto: ')
        porcentaje_margen_contribucion = pedir_numero('Escriba el porcentaje del margen de contribución: ', 0, 100)
        suma_porcentaje += porcentaje_margen_contribucion

        if suma_porcentaje > 100:
            print("-"*92)
            print(f"|{negrita('ADVERTENCIA'):^98}|")
            print(f"|{'La suma de porcentajes proporcionada hasta ahora supera el 100%':^90}|")
            print(f"|{'¿Está seguro de querer continuar?':^90}|")
            print(f"|{'(S) - Sí':^90}|")
            print(f"|{'(N) - No':^90}|")
            print("-"*92)

            confirmar = pedir_campo("Respuesta: ").capitalize()

            if confirmar == "N":
                break


        precio_venta = pedir_numero('Escriba el precio de venta: ', 0)
        costo_variable = pedir_numero('Escriba el costo variable: ', 0)
        margen_contribucion = pedir_numero('Escriba el margen de contribución: ', 0)

        df_datos[nombre_producto] = [porcentaje_margen_contribucion, precio_venta, costo_variable, margen_contribucion]

        contador_productos += 1

        print("-"*92)
        print(f"|{'¿Quiere añadir otro producto?':^90}|")
        print(f"|{'(S) - Sí':^90}|")
        print(f"|{'(N) - No':^90}|")
        print("-"*92)

        continuar = pedir_campo("Respuesta: ").capitalize()

        if continuar == "N":
            break

    df_datos.index = ['% de Margen de contribución', 'Precio de venta', 'Costo variable', 'Margen de contribución']

    costo_fijo = pedir_numero('Escriba el costo fijo: ', 0)

    print("\n")
    print(tabulate(df_datos, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))


    df_margen_ponderado = pd.DataFrame()
    margen_contribucion_unitario = 0

    for columna in df_datos:
        margen_contribucion = df_datos.loc['Margen de contribución', columna]
        porcentaje_margen_contribucion = df_datos.loc['% de Margen de contribución', columna]
        margen_contribucion_ponderado = margen_contribucion * (porcentaje_margen_contribucion / 100)

        margen_contribucion_unitario += margen_contribucion_ponderado

        df_margen_ponderado[columna] = [margen_contribucion, porcentaje_margen_contribucion, margen_contribucion_ponderado]

    df_margen_ponderado.index = ['Margen de contribución', 'Porcentaje del margen de contribución', 'Margen de contribución ponderado']

    print("\n")
    print(tabulate(df_margen_ponderado, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))

    punto_equilibrio_unidades = costo_fijo / margen_contribucion_unitario

    print("\n")
    print('-'*92)
    print(f"|{f'El punto de equilibrio en unidades es: {punto_equilibrio_unidades:,.2f}':^90}|")
    print(f"|{'A continuación se mostrará la ponderación':^90}|")
    print('-'*92)

    df_punto_equilibrio_unidades = pd.DataFrame()

    for columna in df_datos:
        porcentaje_margen_contribucion = df_datos.loc['% de Margen de contribución', columna]
        punto_equilibrio_por_unidad = punto_equilibrio_unidades * (porcentaje_margen_contribucion / 100)

        df_punto_equilibrio_unidades[columna] = [porcentaje_margen_contribucion, punto_equilibrio_unidades, punto_equilibrio_por_unidad]

    df_punto_equilibrio_unidades.index = ['Porcentaje del margen de contribución', 'Punto de equilibrio en unidades', 'Punto de equilibrio por unidad']

    print("\n")
    #Usamos la matriz transpuesta para cambiar las columnas por las filas.
    print(tabulate(df_punto_equilibrio_unidades.T, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))

    df_punto_equilibrio_pesos = pd.DataFrame()
    total_punto_equilibrio_pesos = 0

    for columna in df_punto_equilibrio_unidades:
        punto_equilibrio_por_unidad = df_punto_equilibrio_unidades.loc['Punto de equilibrio por unidad', columna]
        precio_venta = df_datos.loc['Precio de venta', columna]
        punto_equilibrio_pesos = punto_equilibrio_por_unidad * precio_venta
        total_punto_equilibrio_pesos += punto_equilibrio_pesos

        df_punto_equilibrio_pesos[columna] = [punto_equilibrio_por_unidad, precio_venta, punto_equilibrio_pesos]

    df_punto_equilibrio_pesos.index = ['Punto de equilibrio por unidad', 'Precio de venta', 'Punto de equilibrio en pesos']

    print("\n")
    print(tabulate(df_punto_equilibrio_pesos.T, headers='keys', tablefmt='psql', floatfmt=",.2f", numalign="center", intfmt=","))
    print("\n")

    print("-"*92)
    print(f"|{f'El punto de equilibrio en unidades es: {punto_equilibrio_unidades:,.2f}':^90}|")
    print(f"|{f'El punto de equilibrio en pesos es: ${total_punto_equilibrio_pesos:,.2f}':^90}|")
    print("-"*92)

    print("\n")
    print("-"*92)
    print(f"|{'¿Desea exportar los resultados a EXCEL?':^90}|")
    print(f"|{'(S) - Sí':^90}|")
    print(f"|{'(N) - No':^90}|")
    print("-"*92)

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

    while True:
        print("-"*92)
        print(f"|{negrita('Usted escogió: Unidades antes/después de impuestos'):^98}|")
        print(f"|{'-'*90}|")
        print(f"|{'(1) - Unidad antes de impuestos normal':^90}|")
        print(f"|{'(2) - Unidad antes de impuestos multilínea':^90}|")
        print(f"|{'(3) - Unidad después de impuestos normal':^90}|")
        print(f"|{'(4) - Unidad después de impuestos multilínea':^90}|")
        print(f"|{'(5) - Regresar':^90}|")
        print("-"*92)

        opcion = pedir_numero(f"{negrita('Escribe el número de la opción que vas a escoger: ')}", 1, 5)

        match opcion:
            case 1:
                unidad_antes_de_impuestos_normal()
            case 2:
                pass
            case 3:
                unidad_despues_de_impuestos_normal()
            case 4:
                pass
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

    print("\n")
    print("-"*92)
    print(f"|{f'Unidades a vender antes de impuestos: {unidades_antes_impuestos}':^90}|")
    print("-"*92)

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

    print("\n")
    print("-"*92)
    print(f"|{f'Unidades a vender después de impuestos: {unidades_despues_impuestos}':^90}|")
    print("-"*92)

def unidad_antes_de_impuestos_multilinea():
    pass

######################## MENÚ PRINCIPAL ########################
def menu() -> None:
    """Función que le muestra el menú principal al usuario."""

    while True:
        try:
            print("-"*92)
            print(f"|{negrita('Bienvenido al programa contable'):^98}|")
            print(f"|{'-'*90}|")

            print(f"|{negrita('Escoge la opción: '):^98}|")
            print(f"|{'(1) - Punto de equilibrio en unidades/pesos normal o multilínea':^90}|")
            print(f"|{'(2) - Unidades a vender antes/después de impuestos normal o multilínea':^90}|")
            print(f"|{'(3) - Análisis Costo - Volumen - Utilidad ':^90}|")
            print(f"|{'(4) - Presupuesto de Ventas y Producción':^90}|")
            print(f"|{'(5) - Presupuesto de necesidades de Materias Primas y Compras':^90}|")
            print(f"|{'(6) - Salir del programa':^90}|")
            print("-"*92)

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
