import math


def obtener_mejor_par(n):
    for i in range(int(math.sqrt(n)), 0, -1):
        if n % i == 0:
            j = n // i

            if j <= 1.7 * i and i <= 15 and j / i > 1:
                return [j, i]

        return None
    return None


num = 500
resultados = {}

# Un solo ciclo para procesar y filtrar
for i in range(16, num + 1):
    par = obtener_mejor_par(i)
    if par:
        resultados[i] = (par[0], par[1])

# Escritura eficiente
with open("list2.txt", "w") as a:
    a.write("{\n")
    for n, par in resultados.items():
        a.write(f"\t\t\t\t{n}: {par},\n")
    a.write("}")

print("Escritura exitosa")
print(5 >= 0)
