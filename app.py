import pandas as pd
import tabulate as t

def negrita(texto: str) -> str:
    return f'\033[1m{texto}\033[0m'

def pedir_salida() -> bool:
    salida = pedir_campo("¿Quiere salir? (S)í o (N)o: ").capitalize()
    if salida == "S":
        return True
    else:
        return False

def pedir_campo(mensaje: str) -> str:
    while True:
        try:
            entrada = input(mensaje).strip()

            if not entrada:
                raise ValueError("El campo no puede estar vacío")

            return entrada

        except ValueError as e:
            print(f"Error: {e}")

            salir = pedir_salida()
            if salir:
                return

            continue

def pedir_numero(mensaje: str, min: int = None, max: int = None) -> int:
    while True:
        try:
            entrada = int(pedir_campo(mensaje))

            if min or max: #Si se especificaron cualquiera de las dos variables
                if entrada < min or entrada > max:
                    raise ValueError("Número fuera del rango especificado.")

            return entrada
        except ValueError as e:
            print(f"Error: {e}")

            salir = pedir_salida()
            if salir:
                return

            continue

def punto_equilibrio_menu() -> None:
    while True:
        print("-"*92)
        print(f"|{"Usted escogió: Punto de equilibrio":^90}|")
        print(f"|{'-'*90}|")
        print(f"|{"¿Normal o multilínea?":^90}|")
        print(f"|{"(1) - Normal":^90}|")
        print(f"|{"(2) - Multilínea":^90}|")
        print(f"|{"(3) - Regresar al menú principal":^90}|")
        print("-"*92)

        opcion = pedir_numero("Escriba el número de la opción que va a escoger: ", 1, 3)

        match opcion:
            case 1:
                pass
            case 2:
                pass
            case 3:
                return

def utilidad_impuestos_menu() -> None:
    while True:
        print("-"*92)
        print(f"|{negrita('Usted escogió: Utilidad antes/después de impuestos'):^90}|")
        print(f"|{'-'*90}|")
        print(f"|{'¿Normal o multilínea?':^90}|")
        print(f"|{'(1) - Normal':^90}|")
        print(f"|{'(2) - Multilínea':^90}|")
        print(f"|{'(3) - Regresar al menú principal':^90}|")
        print("-"*92)

        opcion = pedir_numero("Escriba el número de la opción que va a escoger: ", 1, 3)

        match opcion:
            case 1:
                pass
            case 2:
                pass
            case 3:
                return


def menu() -> None:
    while True:
        print("-"*92)
        print(f"|{negrita('Bienvenido al programa contable'):^98}|")
        print(f"|{'-'*90}|")

        print(f"|{negrita('Escoge la opción que quieres hacer: '):^98}|")
        print(f"|{'(1) - Punto de equilibrio en unidades/pesos normal o multilínea':^90}|")
        print(f"|{'(2) - Utilidad antes/después de impuestos normal o multilínea':^90}|")
        print(f"|{'(3) - Análisis Costo - Volumen - Utilidad ':^90}|")
        print(f"|{'(4) - Presupuesto de Ventas y Producción':^90}|")
        print(f"|{'(5) - Presupuesto de necesidades de Materias Primas y Compras':^90}|")
        print(f"|{'(6) - Salir del programa':^90}|")
        print("-"*92)

        opcion = pedir_numero("Escribe el número de la opción que vas a escoger: ", 1, 6)

        match opcion:
            case 1:
                punto_equilibrio_menu()
            case 2:
                utilidad_impuestos_menu()
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case 6:
                break



def main():
    menu()

if __name__ == "__main__":
    main()
