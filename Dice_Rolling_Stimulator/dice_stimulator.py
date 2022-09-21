import random
print("Esse é um simulador de dados!")
rolarnovamente = "Y"
vezesdadorolado = 0
soma = 0
while rolarnovamente == "Y":
    vezesdadorolado += 1
    number = random.randint(1,6)
    soma += number
    if number == 1:
        print('='*11)
        print("|         |")
        print("|    O    |")
        print("|         |")
        print('='*11)
        print('O dado resultou no número 1')

    if number == 2:
        print('='*11)
        print("|         |")
        print("| O     O |")
        print("|         |")
        print('='*11)
        print('O dado resultou no número 2')

    if number == 3:
        print('='*11)
        print("|    O    |")
        print("|    O    |")
        print("|    O    |")
        print('='*11)
        print('O dado resultou no número 3')
        
    if number == 4:
        print('='*11)
        print("| O     O |")
        print("|         |")
        print("| O     O |")
        print('='*11)
        print('O dado resultou no número 4')
        
    if number == 5:
        print('='*11)
        print("| O     O |")
        print("|    O    |")
        print("| O     O |")
        print('='*11)
        print('O dado resultou no número 5')
        
    if number == 6:
        print('='*11)
        print("| O     O |")
        print("| O     O |")
        print("| O     O |")
        print('='*11)
        print('O dado resultou no número 6')

    rolarnovamente =  input("Pressione Y para rolar o dado novamente: ").upper()
print()
print('='*10)
print('Você não pressionou Y, então o simulador de dados foi encerrado.')
if vezesdadorolado == 1:
    print(f'O dado foi rolado {vezesdadorolado} vez!')
else:
    print(f'O dado foi rolado {vezesdadorolado} vezes!')
print(f'A soma de todos os valores que o dado simulou foi: {soma}')