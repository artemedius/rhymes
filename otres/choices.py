def round_to_multiple(number, multiple):
    return multiple * round(number / multiple)

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
    print(f"Вы можете поднять {weight}кг на {reps} повторения")

    import formula
    onerm = formula.one_rm(weight=weight, rep=reps)
    print(f'Ваш максимум на одно повторение - {round(onerm,1)}')
    print(f'Ваш рабочий вес - {round(onerm*0.85, 1)}')

def programme():
    import pandas as pd
    import inquirer
    db = pd.read_excel('db.xlsx')

    # Задаём вопрос пользователю, даём опции
    question_cat = [
        inquirer.List('cat1', message='Какую категорию упражнений? ', choices=list(db['Категория'].unique())),
        inquirer.List('cat2', message='С чем совместить? ', choices=list(db['Категория'].unique()))
    ]
    print("Пожалуйста выберите две разных категории")
    category = inquirer.prompt(question_cat)
    print(f"Вы выбрали категории - {category['cat1']} и {category['cat2']}")

    # Заставляем выбрать две разных категории
    if category['cat1'] == category['cat2']:
        print("Программе нужны разные категории, извините")
        programme()
    else:
        pass

    c1_ex = list(db.loc[db['Категория'] == category['cat1']]['Упражнение'])
    c2_ex = list(db.loc[db['Категория'] == category['cat2']]['Упражнение'])
    exercises = c1_ex + c2_ex
    print(f'Количество упражнений: {len(exercises)}')

    proga = pd.DataFrame(columns=['Упражнение', '1пх', '2пх', '3пх'])
    for x in exercises:
        df = db[db['Упражнение'] == x]
        weight = int(df['Вес'].values)
        reps = int(df['Повторения'].values)

        import formula
        orm = formula.one_rm(weight, reps)

        weightlist = []
        if 'гантел' in x:
            weightlist.extend([x, round_to_multiple(orm*0.71, 2), round_to_multiple(orm*0.81, 2), round_to_multiple(orm*0.91, 2)])
        else:
            weightlist.extend([x, round(orm*0.71), round(orm*0.81), round(orm*0.91)])
        proga = pd.concat([pd.DataFrame([weightlist], columns=['Упражнение', '1пх', '2пх', '3пх']), proga], ignore_index=True)
    # proga.to_excel('proga.xlsx', index=False)
    print(proga)