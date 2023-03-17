from lub import *


class Controller:
    def __init__(self):
        super().__init__()

    def setView(self, view):
        self.view = view

    def get_data(self):
        dict2 = read_dict()
        dict = list(dict2.keys())
        return dict


    def search_data(self, filter):
        data = find_sent_in_dict(read_dict(), filter)[0]
        if data == None:
            return []
        return [data]

    def del_word(self, word):
        new_dict = delete_from_dict(read_dict(), str(word.id))
        save_dict(new_dict)
        self.view.show_data('nan')


    def selected(self, filename, label, button):
        if filename[0].find('docx', -4) == -1:
            label.text = 'Выберите docs файл!'
            button.disabled = True
        else:
            label.text = ''
            self.file = filename[0]
            button.disabled = False

    def load_word(self, label, button=None):
        read_from_doc(self.file, read_dict())
        print(self.file)
        button.disabled = True
        label.text = 'Загружено'
        self.view.show_data('nan')


    def get_forms(self, filter):
        data = search_rel(read_dict(), filter)
        if data == None:
            return []
        return data

    def edit_form(self, new_form, label):
        dict = read_dict()
        new_dict = change_analiz(dict, self.view.word, self.view.form, new_form.text)
        print(self.view.word)
        print(self.view.form)
        print(type(self.view.form))
        print(new_form.text)
        save_dict(new_dict)
        label.text = 'Изменено'
        self.view.show_data_form(self.view.word)
