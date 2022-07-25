import inquirer

start = [inquirer.List('menu', message='Чем Вам помочь? ',choices=['Сколько поднять на раз', 'Составить тренировку на группу мышц'])]
menu = inquirer.prompt(start)

if menu['menu'] == 'Сколько поднять на раз':
    import choices
    choices.one_rep_max()
elif menu['menu'] == 'Составить тренировку на группу мышц':
    import choices
    choices.programme()