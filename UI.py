from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.garden.scrolllabel import ScrollLabel
from kivy.garden.xpopup.file import XFileOpen, XFileSave
from kivy.garden.xpopup.form import XTextInput
from kivy.garden.xpopup.notification import XMessage
from os.path import expanduser
from Ranker import *
from Index import *
from Document import *
from Query import *
from os.path import join, isdir




class Menu(FloatLayout):
    Index = IndexEnvironment()
    Ranker_Environment = RankerEnvironment(Index)
    Doc_Count = StringProperty()
    Queries_Count = StringProperty()
    query1 = ""
    limit = 0
    history = ['MainScreen']

    def GetLastScreen(self):
        if len(self.history) == 1:
            return 'MainScreen'
        else:
            return self.history.pop()

    def Update_Index(self):
        XFileOpen(on_dismiss=self.loadIndex_filepopup_callback, path=expanduser(u'~'),multiselect=False)
        return

    def loadIndex_filepopup_callback(self, instance):
        if instance.is_canceled():
            return
        self.Index.addIndex(instance.selection[0])
        s = 'The index was updated'
        s += ('\nSelection: %s' % instance.selection[0])
        XMessage(title='Pressed button: ' + instance.button_pressed, text=s)

    def Load_Queries(self):
        XFileOpen(on_dismiss=self.loadQuesries_filepopup_callback, path=expanduser(u'~'), multiselect=False)
        return

    def loadQuesries_filepopup_callback(self, instance):
        if instance.is_canceled():
            return
        self.Ranker_Environment.loadQueries(instance.selection[0])
        s = 'The queries was uploaded'
        s += ('\nSelection: %s' % instance.selection[0])
        XMessage(title='Pressed button: ' + instance.button_pressed, text=s)

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
        XMessage(title='Pressed button: ' + instance.button_pressed, text=s)

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
        s += ('\nFilename: %s\nFull path: %s' % (instance.filename, instance.get_full_name()))
        XMessage(title='Pressed button: ' + instance.button_pressed, text=s)

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

