def legs():
    import pandas as pd
    import inquirer
    import re
    import random
    db = pd.read_excel('db.xlsx')
    parameters = [inquirer.Text('number', message='2. Сколько упражнений?', validate= lambda _, x: re.match('[1-9]', x))]
    params = inquirer.prompt(parameters)
    total_list = list(db.loc[db['Категория'] == 'Ноги']['Упражнение'])
    sample_list = random.sample(total_list, int(params['number']))

    proga = pd.DataFrame(columns=['Упражнение', '1пх', '2пх', '3пх'])
    for x in sample_list:
        df = db[db['Упражнение'] == x]
        weight = int(df['Вес'].values)
        reps = int(df['Повторения'].values)

        import choices
        orm = choices.formula(weight, reps)

        weightlist = []
        if 'гантел' in x:
            weightlist.extend([x, choices.round_to_multiple(orm*0.71, 2), choices.round_to_multiple(orm*0.81, 2), choices.round_to_multiple(orm*0.91, 2)])
        else:
            weightlist.extend([x, round(orm*0.71), round(orm*0.81), round(orm*0.91)])
        proga = pd.concat([pd.DataFrame([weightlist], columns=['Упражнение', '1пх', '2пх', '3пх']), proga], ignore_index=True)
        proga = proga.sort_values(by=['1пх'], ascending=False)
    print(proga)