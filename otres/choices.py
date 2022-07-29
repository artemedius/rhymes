def delete_random_elems(list, n):
    import random
    to_delete = set(random.sample(range(len(list)), n))
    return [x for i,x in enumerate(list) if not i in to_delete]

def round_to_multiple(number, multiple):
    return multiple * round(number / multiple)

def formula(weight, reps):
    from statistics import mean

    def brzycki(w,r):
        return(w*(36/(37-r)))
    def lombardi(w,r):
        return(w*(r**0.10))
    def oconner(w,r):
        return(w*(1+(r/40)))

    b = brzycki(weight, reps)
    l = lombardi(weight, reps)
    c = oconner(weight, reps)

    return(mean([b, l, c]))

def one_rep_max():
    import pandas as pd
    import inquirer
    db = pd.read_excel('db.xlsx')

    question_cat = [inquirer.List('category',message='Какую категорию упражнений? ',
                    choices=list(db['Категория'].unique()))]
    category = inquirer.prompt(question_cat)
    print(f"Вы выбрали категорию - {category['category']}")

    question_ex = [inquirer.List('exercise',message='Какое упражнение? ', 
                    choices=list(db.loc[db['Категория']==category['category']]['Упражнение']))]
    exercise = inquirer.prompt(question_ex)
    print(f"Вы выбрали упражнение - {exercise['exercise']}")

    filter = db.loc[db['Упражнение'] == exercise['exercise']]
    weight = int(filter['Вес'])
    reps = int(filter['Повторения'])
    print(f"Последний раз вы подняли {weight}кг на {reps} повторения")

    onerm = formula(weight=weight, reps=reps)
    print(f'Ваш максимум на одно повторение - {round(onerm,1)}')
    print(f'Ваш рабочий вес - {round(onerm*0.85, 1)}')

def programme():
    import pandas as pd
    import inquirer
    import re
    db = pd.read_excel('db.xlsx')

    # Задаём вопрос пользователю, даём опции
    print('Для построения программы пожалуйста ответьте на пару вопросов:')

    legs_or_nah = [inquirer.List('mg1', message='1. Какую группу мышц Вы хотите тренировать? ', choices=list(db['Категория'].unique()))]
    legs = inquirer.prompt(legs_or_nah)
    if legs['mg1'] == 'Ноги':
        print('Ну вы зверюга...')
        print('Ронни Коулмэна из себя возомнили?...')
        import legs
        legs.legs()
        quit()
    else:
        pass
    
    cats = list(db['Категория'].unique())
    cats.remove('Ноги')
    cats.remove(legs['mg1'])
    muscle_groups = [inquirer.List('mg2', message='2. С чем совместить? ', choices=cats)]
    print("Пожалуйста выберите две разных группы мышц")
    category = inquirer.prompt(muscle_groups)

    # Заставляем выбрать две разных категории
    if legs['mg1'] == category['mg2']:
        print("Программе нужны разные группы мышц, выберите пожалуйста разные группы")
        programme()
        quit() # Без quit скрипт идёт до print(programme) и задаёт 3,4 вопросы снова
    else:
        pass

    parameters = [
        inquirer.Text('number', message='3. Сколько упражнений?', validate= lambda _, x: re.match('[1-9]', x)),
        inquirer.Text('ratio', message='4. С каким соотношением?', validate=lambda _, x: re.match('0+\.[1-9]', x))
    ]
    params = inquirer.prompt(parameters)
    print(f"Вы выбрали группы мышц - {legs['mg1']} и {category['mg2']} с соотношением {params['ratio']} ")
    print(f"В тренировку войдёт {params['number']} упражнений:")

    list1 = list(db.loc[db['Категория'] == legs['mg1']]['Упражнение'])
    list2 = list(db.loc[db['Категория'] == category['mg2']]['Упражнение'])
    exercises=[list1, list2]
    number = int(float(params['number']))
    ratio = float(params['ratio'])

    list1_num = round(number * ratio)
    list2_num = number - list1_num
    print(f"{list1_num} упражнения на {legs['mg1']}")
    print(f"{list2_num} упражнения на {category['mg2']}")

    if len(exercises[0]) != list1_num:
        list1 = delete_random_elems(exercises[0], (len(exercises[0])-list1_num))
    if len(exercises[1]) != list2_num:
        list2 = delete_random_elems(exercises[1], (len(exercises[1])-list2_num))
    total = list1 + list2

    proga = pd.DataFrame(columns=['Упражнение', '1пх', '2пх', '3пх'])
    for x in total:
        df = db[db['Упражнение'] == x]
        weight = int(df['Вес'].values)
        reps = int(df['Повторения'].values)

        orm = formula(weight, reps)

        weightlist = []
        if 'гантел' in x:
            weightlist.extend([x, round_to_multiple(orm*0.71, 2), round_to_multiple(orm*0.81, 2), round_to_multiple(orm*0.91, 2)])
        else:
            weightlist.extend([x, round(orm*0.71), round(orm*0.81), round(orm*0.91)])
        proga = pd.concat([pd.DataFrame([weightlist], columns=['Упражнение', '1пх', '2пх', '3пх']), proga], ignore_index=True)
        proga = proga.sort_values(by=['1пх'], ascending=False)
    # proga.to_excel('proga.xlsx', index=False)
    print("Ваша программа на тренировку: ")
    print(proga)