import inquirer
import choices

start = [inquirer.List('menu', message='Чем Вам помочь? ',
        choices=['Сколько поднять на раз', 'Составить тренировку на группу мышц',
        'Обновить рекорды'])]
menu = inquirer.prompt(start)

if menu['menu'] == 'Сколько поднять на раз':
    choices.one_rep_max()
elif menu['menu'] == 'Составить тренировку на группу мышц':
    choices.programme()
elif menu['menu'] == 'Обновить рекорды':
    choices.update()