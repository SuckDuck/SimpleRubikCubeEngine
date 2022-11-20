from engine import cube
rubik = cube()

rubik.scramble_cube()
"""while True:
    print(rubik.is_solved())
    move = input("Cual movimiento desea hacer? : ")
    if move != "":
        rubik.turn_face(move)
        if move == "exit":
            break

    respuesta = input("desea mostrar el cubo? : ")
    if respuesta == "si":
        rubik.show_cube(save=False)"""

print(rubik.cube.shape)

