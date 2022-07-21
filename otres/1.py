import pandas as pd
import inquirer
db = pd.read_excel('db.xlsx')

question_cat = [inquirer.List('category',message='Какую категорию упражнений? ',choices=list(db['Категория'].unique()))]

category = inquirer.prompt(question_cat)
print(f"Вы выбрали категорию - {category['category']}")

question_ex = [inquirer.List('exercise',message='Какое упражнение? ', choices=list(db.loc[db['Категория']==category['category']]['Упражнение']))]
exercise = inquirer.prompt(question_ex)
print(f"Вы выбрали упражнение - {exercise['exercise']}")