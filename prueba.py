import keyboard

# Función para deshabilitar la entrada de teclado
def bloquear_entrada_teclado():
    print("Ejecutando una acción... Entrada de teclado bloqueada.")
    keyboard.hook(lambda e: keyboard.block_key(e.name))

    # Simulación de una acción que tarda un tiempo en completarse
    import time
    time.sleep(10)

    # Restaurar la entrada de teclado
    keyboard.unhook_all()
    print("Acción completada. Entrada de teclado restaurada.")

# Ejemplo de uso
message = input()
bloquear_entrada_teclado()
mesage = input()