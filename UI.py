from kivy.app import App
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.base import runTouchApp
from kivy.garden.scrolllabel import ScrollLabel
from Ranker import *
from Index_envierment import *
from Document import *
from Query import *

from os.path import join, isdir




class Menu(FloatLayout):
    Index = IndexEnvironment()
    Ranker_Environment = RankerEnvironment(Index)
    Doc_Count = StringProperty()
    Queries_Count = StringProperty()
    #history = ['MainScreen']
    #IndexDict = {} #Dictionary of the indexes
    #cur_index_selection = ''
    """
    def choose_index(self):
        self.dropdown = DropDown()
        for index in self.IndexDict:
            btn = Button(text=index, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
            self.ids.index_menu.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.ids.index_menu, 'text', x))
        return

    def save_index_selection(self, select):
        print select
        self.cur_index_selection = select
        return
"""
    def New_Index(self, path):
        self.Index.addIndex(path)
        print self.Index.count()
        self.popup_msg("The index has \nbeen updated \nsuccessfully!")
        return

    def Load_Queries(self,path):
        self.Ranker_Environment.loadQueries(path)
        self.popup_msg("The queries have \nbeen loaded \nsuccessfully!")
        return

    def popup_msg(self, msg, fsize = 40):
        button_layout = AnchorLayout(anchor_x='center', anchor_y='bottom')
        button = Button(text='Dismiss',
                        size_hint=(1, .3),
                        font_size=25)
        button_layout.add_widget(button)
        label_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        label = Label(text=msg,
                      font_size=fsize,
                      text_size=self.size,
                      halign='center',
                      valign='middle')
        label_layout.add_widget(label)
        box = BoxLayout(orientation='vertical')
        box.add_widget(label_layout)
        box.add_widget(button_layout)
        popup = Popup(title='',
                      content=box,
                      auto_dismiss=False,
                      size_hint=(None, None),
                      size=(400, 400))
        button.bind(on_press=popup.dismiss)
        popup.open()

    def Run_Queries_File(self, path, name, limit):
        self.Ranker_Environment.runQueries(pathnameToSave= path + "\\" + name + ".txt", limit=int(limit))
        self.popup_msg("The results have \nbeen saved \nsuccessfully!")
        return

    def Run_Query_File(self, query, path, name, limit):
        self.Ranker_Environment.runQuery(query=str(query), pathnameToSave=path + "\\" + name + ".txt", limit=int(limit))
        self.popup_msg("The results have \nbeen saved \nsuccessfully!")
        return

    def PrintDocsIDs(self):
        ids = self.Index.getDocumentsMetadata(metaData='DOCNO')
        result = ""
        for id in ids:
            result = result + id + "\n"
        return result

    def PrintDocs(self):
        docs = self.Index.getDocumentsMetadata(metaData='TEXT')
        result = ""
        for doc in docs:
            result = result + doc + "\n\n"
        return result

    def PrintQueriesIDs(self):
        ids = self.Ranker_Environment.getQueriesMetadata('number')
        result = ""
        for id in ids:
            result = result + id + "\n"
        return result

    def PrintQueries(self):
        queries = self.Ranker_Environment.getQueriesMetadata('text')
        result = ""
        for query in queries:
            result = result + query + "\n\n"
        return result


    def is_dir(self, directory, filename):
        return isdir(join(directory, filename))



class MenuApp(App):
    def build(self):
        return Menu()

if __name__ == '__main__':
    MenuApp().run()

