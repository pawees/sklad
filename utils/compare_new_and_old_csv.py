from utils import config
import csv
#TODO вставить старый вариант,проблема поиска в \n в конце строки,пусть скрипт допарсит,найти скрипт который почистит основной файл.Позже написать нормальную сравнивалку и зап-ть скрипт каждый день
class CompareLists():
    after_add=[]
    old_csv=[]
    new_csv=[]
    @classmethod
    def compare(cls,rows):
        for i in rows:
            for entr in CompareLists.old_csv:
                if i == entr:
                    return False
            with open(config.file_main_staff_csv , "a+", encoding='utf8') as f:
                f.write(i)
                f.write('\n')

            return True

    @classmethod
    def difference(cls):
        with open(config.file_main_staff_csv , "r+", encoding='utf8') as f:
            # gives you a list of the lines
            CompareLists.after_add = f.readlines()
        return (len(CompareLists.old_csv),len(CompareLists.after_add))

def main(rows):
    with open(config.file_main_staff_csv , "r+", encoding='utf8') as f:
        # gives you a list of the lines
        CompareLists.old_csv = f.readlines()
        q1=1

    res = CompareLists.compare(rows)

    return res

if __name__ == '__main__':
    rows = ['Волшебные перемены (Ольга Юрковская)', 'Ключ от стеклянного потолка (Ольга Юрковская)', '[Access Consciousness] Эта книга. Мой путь к исцелению (Грег Брайерс)', '[Access Consciousness] Что еще возможно (Дейн Хиир)', '[Access Consciousness] Вкус бизнеса и творчества (Дейн Хиир)', 'Онлайн-мастерская для психологов "Сессии под супервизией" (Мария Минакова)', 'Успешная работа с паническими атаками (Мария Минакова)', 'Убеждения. Я-Создатель. Тариф-Создатель + (Егор Астахов)']
    main(rows)