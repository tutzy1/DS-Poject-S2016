from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from scrolllabel import ScrollLabel
from file import XFileOpen, XFileSave
from form import XTextInput
from notification import XMessage
from os.path import expanduser
from Ranker import *
from Index import *
from Document import *
from Query import *
from os.path import join, isdir
import pickle




class Menu(FloatLayout):
    Index = IndexEnvironment()
    Ranker_Environment = RankerEnvironment(Index)
    Doc_Count = StringProperty()
    Queries_Count = StringProperty()
    query1 = ""
    limit = 0
    history = ['MainScreen']

    def GetLastScreen(self):
        """
        :return: The screen that the user visit before the current screen
        """
        if len(self.history) == 1:
            return 'MainScreen'
        else:
            return self.history.pop()

    def Update_Index(self):
        """
        This function creates a popup massage contains a file chooser -
        to choose xml file with documents to load to the index.
        With press on the "Open" button the method loadIndex_filepopup_callback will be called.
        :return: nothing.
        """
        XFileOpen(on_dismiss=self.loadIndex_filepopup_callback, path=expanduser(u'~'),multiselect=False)
        return

    def loadIndex_filepopup_callback(self, instance):
        """
        This function calls the relevant function to add documents to the index,
        after the user selected a file.
        :param instance: contains data about the user's selection.
        :return: nothing.
        """
        if instance.is_canceled():
            return
        self.Index.addIndex(instance.selection[0])
        s = 'The index was updated'
        s += ('\nSelection: %s' % instance.selection[0])
        XMessage(title='Pressed button: ' + instance.button_pressed, text=s)

    def Load_Queries(self):
        """
        This function creates a popup massage contains a file chooser -
        to choose xml file with queries to load to the database.
        With press on the "Open" button the method loadQuesries_filepopup_callback will be called.
        :return: nothing.
        """
        XFileOpen(on_dismiss=self.loadQuesries_filepopup_callback, path=expanduser(u'~'), multiselect=False)
        return

    def loadQuesries_filepopup_callback(self, instance):
        """
        This function calls the relevant function to add queries to the database,
        after the user selected a file.
        :param instance: contains data about the user's selection.
        :return: nothing.
        """
        if instance.is_canceled():
            return
        self.Ranker_Environment.loadQueries(instance.selection[0])
        s = 'The queries was uploaded'
        s += ('\nSelection: %s' % instance.selection[0])
        XMessage(title='Pressed button: ' + instance.button_pressed, text=s)

    def Get_Limit(self):
        """
        This function creates a popup massage contains a text input field -
        to enter limit for the ranking.
        With press on the "Open" button the method limit_callback will be called.
        :return: nothing.
        """
        XTextInput(title='How many documents would you like \nto appear in the result list? \n(insert 0 to unlimit)', text='0', on_dismiss=self.limit_callback)
        return


    def limit_callback(self, instance):
        """
        This function limit value within this class with the value that
        the user inserted.
        :param instance: contains data about the user's input.
        :return: nothing.
        """
        if not instance.values['text']:
            self.limit = 0
        else:
            self.limit = int(instance.values['text'])
        return

    def Run_Queries_File(self):
        """
        This function creates a popup massage contains a file chooser -
        to choose a path to save the results of ranking all the
        queries in the database.
        With press on the "Save" button the method _filepopup_Queries_callback will be called.
        :return: nothing.
        """
        XFileSave(on_dismiss=self._filepopup_Queries_callback, path=expanduser(u'~'))
        return

    def _filepopup_Queries_callback(self, instance):
        """
        This function calls the relevant function to run queries from the database
        and save the results to file, after the user selected a path to save the file.
        :param instance: contains data about the user's selection.
        :return: nothing.
        """
        if instance.is_canceled():
            return
        self.Ranker_Environment.runQueries(pathnameToSave=instance.get_full_name() + ".txt", limit=self.limit)
        s = 'The file was saved!'
        s += ('\nFilename: %s\nFull path: %s' % (instance.filename, instance.get_full_name()))
        XMessage(title='Pressed button: ' + instance.button_pressed, text=s)

    def Run_Query_File(self, query):
        """
        This function creates a popup massage contains a file chooser -
        to choose a path to save the results of ranking the query inserted by the user.
        With press on the "Save" button the method _filepopup_Query_callback will be called.
        :param query: The query that the user inserted.
        :return: nothing.
        """
        self.query1 = query
        XFileSave(on_dismiss=self._filepopup_Query_callback, path=expanduser(u'~'))
        return

    def _filepopup_Query_callback(self, instance):
        """
        This function calls the relevant function to run query inserted by the user,
        and save the results to file, after the user selected a path to save the file.
        :param instance: contains data about the user's selection.
        :return: nothing.
        """
        if instance.is_canceled():
            return
        self.Ranker_Environment.runQuery(query=self.query1, pathnameToSave=instance.get_full_name() + ".txt",limit=self.limit)
        s = 'The file was saved!'
        s += ('\nFilename: %s\nFull path: %s' % (instance.filename, instance.get_full_name()))
        XMessage(title='Pressed button: ' + instance.button_pressed, text=s)

    def PrintDocsIDs(self):
        """
        :return: string contains all the document's IDs in the index, each in
                a different row.
        """
        ids = self.Index.getDocumentsMetadata(metaData='DOCNO')
        result = ""
        for id in ids:
            result = result + id + "\n"
        return result

    def PrintDocs(self):
        """
        :return: string contains all the documents in the index.
        """
        result = ""
        for key,val in self.Index.DocIndex.items():
            result = result + "Document ID: " + str(key) + "\n-------------------------------\n" + str(val.Text) + "\n===================End Of Document==================\n\n"
        return result

    def PrintQueriesIDs(self):
        """
        :return: string contains all the queries's IDs in the database, each in
                a different row.
        """
        ids = self.Ranker_Environment.getQueriesMetadata('number')
        result = ""
        for id in ids:
            result = result + id + "\n"
        return result

    def PrintQueries(self):
        """
        :return: string contains all the queries in the database.
        """
        result = ""
        for key,val in self.Ranker_Environment.QueriesDict.items():
            result = result + "Query ID: " + str(key) + "\n-------------------------------\n" + str(val.Text) + "\n===================End Of Query==================\n\n"
        return result

    def Load_Pickle(self):
        """
        This function creates a popup massage contains a file chooser -
        to choose pickle file with index to load.
        With press on the "Open" button the method loadPickle_filepopup_callback will be called.
        :return: nothing.
        """
        XFileOpen(on_dismiss=self.loadPickle_filepopup_callback, path=expanduser(u'~'), multiselect=False)
        return

    def loadPickle_filepopup_callback(self, instance):
        """
        This function calls the relevant function to load index from pickle file,
        after the user selected a file.
        :param instance: contains data about the user's selection.
        :return: nothing.
        """
        if instance.is_canceled():
            return
        f = open(instance.selection[0], 'rb')
        self.Index = pickle.load(f)
        f.close()
        self.Ranker_Environment = RankerEnvironment(self.Index)
        s = 'The Pickle was uploaded'
        s += ('\nSelection: %s' % instance.selection[0])
        XMessage(title='Pressed button: ' + instance.button_pressed, text=s)

    def Save_to_pickle(self):
        """
        This function creates a popup massage contains a file chooser -
        to choose a path to save the index to a pickle file within.
        With press on the "Save" button the method _filepopup_SavePickle_callback will be called.
        :return: nothing.
        """
        XFileSave(on_dismiss=self._filepopup_SavePickle_callback, path=expanduser(u'~'))
        return

    def _filepopup_SavePickle_callback(self, instance):
        """
        This function calls the relevant function to save index to a pickle file,
        after the user selected the path.
        :param instance: contains data about the user's selection.
        :return: nothing.
        """
        if instance.is_canceled():
            return
        self.Index.Put_Index_In_Pickle(pathname=instance.get_full_name())
        s = 'The index was saved to pickle!'
        s += ('\nFilename: %s\nFull path: %s' % (instance.filename, instance.get_full_name()))
        XMessage(title='Pressed button: ' + instance.button_pressed, text=s)

class MenuApp(App):
    def build(self):
        return Menu()

if __name__ == '__main__':
    MenuApp().run()

