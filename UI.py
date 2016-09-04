from kivy.app import App
from kivy.lang import Builder
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
from kivy.garden.xpopup.file import XFileOpen, XFileSave, XFolder
from kivy.garden.xpopup.form import XSlider, XTextInput, XNotes, XAuthorization
from kivy.garden.xpopup.notification import XNotification, XConfirmation, XError, XMessage, XProgress
from os.path import expanduser
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
    pathToSave = ""
    query1 = ""
    limit = 0
    save_flag = 0
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
    def Update_Index(self):
        XFileOpen(on_dismiss=self.loadIndex_filepopup_callback, path=expanduser(u'~'),multiselect=False)
        return

    def loadIndex_filepopup_callback(self, instance):
        if instance.is_canceled():
            return
        self.Index.addIndex(instance.selection[0])
        s = 'The index was updated'
        s += ('\nSelection: %s' % instance.selection[0])
        XNotification(title='Pressed button: ' + instance.button_pressed + '  (will disappear after 5 seconds...)',
                      text=s, show_time=5)

    def Load_Queries(self):
        XFileOpen(on_dismiss=self.loadQuesries_filepopup_callback, path=expanduser(u'~'), multiselect=False)
        return

    def loadQuesries_filepopup_callback(self, instance):
        if instance.is_canceled():
            return
        self.Ranker_Environment.loadQueries(instance.selection[0])
        s = 'The queries was uploaded'
        s += ('\nSelection: %s' % instance.selection[0])
        XNotification(title='Pressed button: ' + instance.button_pressed + '  (will disappear after 5 seconds...)',
                      text=s, show_time=5)

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

    def Get_Limit(self):
        XTextInput(title='How many documents would you like \nto appear in the result list? \n(insert 0 to unlimit)', text='0', on_dismiss=self.limit_callback)
        return


    def limit_callback(self, instance):
        if not instance.values['text']:
            self.limit = 0
        else:
            self.limit = int(instance.values['text'])
        return



    def Run_Queries_File(self, limit):
        self.limit = int(limit)
        XFileSave(on_dismiss=self._filepopup_Queries_callback, path=expanduser(u'~'))
        return

    def _filepopup_Queries_callback(self, instance):
        if instance.is_canceled():
            return
        self.Ranker_Environment.runQueries(pathnameToSave=instance.get_full_name() + ".txt", limit=self.limit)
        s = 'The file was saved!'
        s += ('\nFilename: %s\nFull path: %s' % (instance.filename, instance.get_full_name()))
        XNotification(title='Pressed button: ' + instance.button_pressed + '(will disappear after 5 seconds...)',
                      text=s, show_time=5)

    def Run_Query_File(self, query, limit):
        self.query1 = query
        self.limit = int(limit)
        XFileSave(on_dismiss=self._filepopup_Query_callback, path=expanduser(u'~'))
        return

    def _filepopup_Query_callback(self, instance):
        if instance.is_canceled():
            return
        self.Ranker_Environment.runQuery(query=self.query1, pathnameToSave=instance.get_full_name() + ".txt",limit=self.limit)
        s = 'The file was saved!'
        if instance.__class__.__name__ == 'XFileSave':
            s += ('\nFilename: %s\nFull path: %s' %
                  (instance.filename, instance.get_full_name()))
        else:
            s += ('\nSelection: %s' % instance.selection)
        XNotification(title='Pressed button: ' + instance.button_pressed + '(will disappear after 5 seconds...)',
                      text=s, show_time=5)

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

