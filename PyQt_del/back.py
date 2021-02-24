# This back end of my project
# I create save in file , install from fail
# additional and delete some position of eat
# front end write with PYQT
import openpyxl

class Main_part():
    # in A dish name
    # in B ingredients
    # in C recipe
    # in D time
    # E variably
    def __init__(self):
        self.column_name = ['A', 'B', 'C', 'D']
        self.excel_list_name = 'mytable.xlsx'
        with open(self.excel_list_name,'a') as f:
            self.wb = openpyxl.load_workbook(self.excel_list_name)

        self.sheet = self.wb.active
        self.max_size = len(self.sheet['A'])

    def write_in_file(self,dishes_list:list):
        for i in range(len(dishes_list)):
            self.sheet[self.column_name[i] + str(self.max_size + 1)].value = dishes_list[i]
        self.wb.save(self.excel_list_name)

    def my_filter(self, products_from_recipe, input_products):
        # возвращаю разницу между количеством продуктов,
        # необходимых для рецепта и тем, что ввел пользователь
        count = 0
        recipe_string = ' ,'.join(products_from_recipe)
        for item in input_products:
            if item in recipe_string:
                count += 1
        return len(products_from_recipe) - count

    def find_dishes_on_product(self, text: list):
        dishes = []
        dictionary = {}
        # delete last character for correct find
        products = list(map(lambda string: string[0:len(string) - 1], text))
        # complete dictionary
        for i in range(2, self.max_size + 1):
            dictionary['A{}'.format(i)] = self.sheet['B{}'.format(i)].value.split(',')
        # compare ingredients which user input and from recipe
        for key, item in dictionary.items():
            if self.my_filter(item, products) <= 3:
                dishes.append(key)
        dictionary.clear()
        # return number column from excel
        return dishes

    def recommend(self, text):
        excel_column_list = []
        found_dishes = self.find_dishes_on_product(text)
        column_number = list(map(lambda string: string[1::], found_dishes))
        for number in column_number:
            temp_list = []
            for word in self.column_name:
                temp_list.append(self.sheet[str(word + number)].value)
            excel_column_list.append(temp_list)
        return excel_column_list

    def show_all_dishes(self):
        # if i will write front-end replace print and return!
        dish_list = []
        for row in range(2, self.max_size + 1):  # move all row in table
            temp_list = []  # temporary  list
            for j in range(1, 5):  # move on column
                temp_list.append(self.sheet[self.column_name[j - 1] + str(row)].value)
            dish_list.append(temp_list)
            temp_list = []
        return dish_list

    def find_dishes(self, dish_name):
        all_about_dish = []
        for i in range(self.max_size + 1):
            if self.sheet['A{}'.format(i + 1)].value == dish_name:
                temp = []
                for item in self.column_name:
                    temp.append(self.sheet[item + str(i + 1)].value)
                all_about_dish.append(temp)
                temp=[]
        return all_about_dish

    def str_filter(self, string: str):
        #  бесполезна, тк. как есть self.tableWidget.resizeRowsToContents()
        count =1
        for item in range(len(string)):
            if item>=50*count and string[item]==' ':
                string=string[:item]+'\n'+string[item:]
                count+=1
        return string