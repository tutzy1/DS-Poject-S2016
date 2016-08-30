from Tkinter import *
import pickle
#import DS-Poject-S2016.Ranker_Enviroment # need to see how to make it work
#from DS-Poject-S2016 import Index_envierment # need to see how to make it work


class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.title = Label(self, text = "Tech",fg="blue",font = ("Helvetica", 20))
        self.title1 = Label(self, text="o", fg="red", font=("Helvetica", 20))
        self.title2 = Label(self, text="o", fg="yellow", font=("Helvetica", 20))
        self.title3 = Label(self, text="g", fg="blue", font=("Helvetica", 20))
        self.title4 = Label(self, text="l", fg="green", font=("Helvetica", 20))
        self.title5 = Label(self, text="e", fg="red", font=("Helvetica", 20))
        self.title.grid(row = 0, column = 10, columnspan = 1, padx = 0, sticky = W)
        self.title1.grid(row=0, column=11, columnspan=1,padx = 0, sticky=W)
        self.title2.grid(row=0, column=12, columnspan=1,padx = 0, sticky=W)
        self.title3.grid(row=0, column=13, columnspan=1,padx = 0, sticky=W)
        self.title4.grid(row=0, column=14, columnspan=1,padx = 0, sticky=W)
        self.title5.grid(row=0, column=15, columnspan=1,padx = 0, sticky=W)
        self.create_primery_witches()

    def create_primery_witches(self):
        """
        :return: creates the main menu witches
        """
        # instruction for first option
        self.instructionopt1 = Label(self, text="do you want to provide a douments and query file and to get the ranking of documents (for each query) in separate file?")
        self.instructionopt1.grid(row=1, column=0, columnspan=120, sticky=W)
        # butten for first option
        self.button1 = Button(self, text = "Yes", command = self.create_first_action_witches)
        self.button1.grid(row = 2, column = 0 , columnspan = 120, sticky = W)
        # instruction for second option
        self.instructionopt2 = Label(self,text="do you want to provide a douments and path for a file and to get the document file indexed and save at the proveded file?")
        self.instructionopt2.grid(row=3, column=0, columnspan=120, sticky=W)
        # butten for second option
        self.button2 = Button(self, text="Yes", command = self.create_second_action_witches)
        self.button2.grid(row=4, column=0, columnspan=120, sticky=W)
        # instruction for third option
        self.instructionopt3 = Label(self,text="do you want to provide a path for a file that has an Index (pickled file) and a query file and get the documents ranking from the Index (for each query) in separate file?")
        self.instructionopt3.grid(row=5, column=0, columnspan=120, sticky=W)
        # butten for third option
        self.button3 = Button(self, text="Yes", command=self.create_third_action_witches)
        self.button3.grid(row=6, column=0, columnspan=120, sticky=W)
        # instruction for forth option
        self.instructionopt4 = Label(self, text="do you want to provide a path for a document file Index it and run querys on it?")
        self.instructionopt4.grid(row=7, column=0, columnspan=120, sticky=W)
        # butten for forth option
        self.button4 = Button(self, text="Yes", command=self.create_forth_action_witches)
        self.button4.grid(row=8, column=0, columnspan=120, sticky=W)

    def clear_primery_witches(self):
        """
        :return: deletes the main menu's witches
        """
        self.instructionopt1.destroy()
        self.button1.destroy()
        self.instructionopt2.destroy()
        self.button2.destroy()
        self.instructionopt3.destroy()
        self.button3.destroy()
        self.instructionopt4.destroy()
        self.button4.destroy()

    def return_to_menu(self):
        """
        :return: deletes the current withchs and creates the main menu's witches
        """
        option_list = ['instructiondocfile','docfile','instructionqueryfile','queryfile','instructionresultfile','resultfile','subbmitbutton','returnbutton','instructionquery','query','text','subbmitbutton1','instructionlength','length','results']
        for i in range (len(option_list)):
            if hasattr(self, option_list[i]):
                getattr(self,option_list[i]).destroy()
        self.create_primery_witches()

    def create_first_action_witches(self):
        """
        :return: creates the first action's witches
        """
        self.clear_primery_witches()
        # instruction for enter document file
        self.instructiondocfile = Label(self, text = "enter doccument file pathname:")
        self.instructiondocfile.grid(row = 1, column = 0 , columnspan = 2, sticky = W)
        # text entry for document file pathname
        self.docfile = Entry(self)
        self.docfile.grid(row = 1, column = 5 , columnspan = 2, sticky = W)
        # instruction for enter query file
        self.instructionqueryfile = Label(self, text="enter query file pathname:")
        self.instructionqueryfile.grid(row=2, column=0, columnspan=1, sticky=W)
        # text entry for query file pathname
        self.queryfile = Entry(self)
        self.queryfile.grid(row=2, column=5, columnspan=2, sticky=W)
        # instruction for enter result file
        self.instructionresultfile = Label(self, text="enter result file pathname:")
        self.instructionresultfile.grid(row=3, column=0, columnspan=2, sticky=W)
        # text entry for result file pathname
        self.resultfile = Entry(self)
        self.resultfile.grid(row=3, column=5, columnspan=2, sticky=W)
        # subbmit button
        self.subbmitbutton = Button(self, text = "Subbmit", command = self.first_action)
        self.subbmitbutton.grid(row=4, column=0, columnspan=2, sticky=W)
        # return button
        self.returnbutton = Button(self, text = "return to menu", command = self.return_to_menu)
        self.returnbutton.grid(row=4, column=1, columnspan=2, sticky=W)

    def first_action(self):
        """
        :return: returns the documents rank from document file according to the queries in
        queryfile and writes it to the resultflie in TREC 6 columns format
        """
        # text box
        self.text = Text(self, width=35, height=20, wrap=WORD)
        self.text.grid(row=4, column=0, columnspan=10, sticky=W)
        self.text.delete(0.0, END)
        message = 'wait for it...'
        self.text.insert(0.0, message)
        content1 = self.docfile.get()
        content2 = self.queryfile.get()
        try:
            Index = IndexEnvironment()
            Index.addIndex(content1)
            Ranker = RankerEnvironment(Index)
            Ranker.loadQueries(content2)
        except Exception as e:
            self.text.delete(0.0, END)
            message = str(e).replace(",", "").replace("'", "").replace("(", "").replace(")", "")
            self.text.insert(0.0, message)
        else:
            try:
                Ranker.runQueries(self.resultfile.get())
            except Exception as e:
                self.text.delete(0.0, END)
                message = str(e).replace(",", "").replace("'", "").replace("(", "").replace(")", "")
                self.text.insert(0.0, message)
            else:
                self.text.delete(0.0, END)
                message = 'successful result !!!!'
                self.text.insert(0.0, message)

    def create_second_action_witches(self):
        """
        :return: creates the second action's witches
        """
        self.clear_primery_witches()
        # instruction for enter document file
        self.instructiondocfile = Label(self, text="enter doccument file pathname:")
        self.instructiondocfile.grid(row=1, column=0, columnspan=2, sticky=W)
        # text entry for document file pathname
        self.docfile = Entry(self)
        self.docfile.grid(row=1, column=5, columnspan=2, sticky=W)
        # instruction for enter result file
        self.instructionresultfile = Label(self, text="enter result file pathname:")
        self.instructionresultfile.grid(row=2, column=0, columnspan=2, sticky=W)
        # text entry for result file pathname
        self.resultfile = Entry(self)
        self.resultfile.grid(row=2, column=5, columnspan=2, sticky=W)
        # subbmit button
        self.subbmitbutton = Button(self, text="Subbmit", command = self.second_action)
        self.subbmitbutton.grid(row=3, column=0, columnspan=2, sticky=W)
        # return button
        self.returnbutton = Button(self, text="return to menu", command=self.return_to_menu)
        self.returnbutton.grid(row=3, column=1, columnspan=2, sticky=W)

    def second_action(self):
        """
        :return: creates an Index from the docfile pathname and stores it into resultfile (with pickle)
        """
        # text box
        self.text = Text(self, width=35, height=20, wrap=WORD)
        self.text.grid(row=4, column=0, columnspan=10, sticky=W)
        self.text.delete(0.0, END)
        message = 'wait for it...'
        self.text.insert(0.0, message)
        content = self.docfile.get()
        try:
            Index = IndexEnvironment()
            Index.addIndex(content)
        except Exception as e:
            self.text.delete(0.0, END)
            message = str(e).replace(",", "").replace("'", "").replace("(", "").replace(")", "")
            self.text.insert(0.0, message)
        else:
            f = open(self.resultfile.get(), 'wb')
            pickle.dump(Index, f)
            f.close()
            self.text.delete(0.0, END)
            message = 'successful result !!!!'
            self.text.insert(0.0, message)

    def create_third_action_witches(self):
        """
        :return: creates the third action's witches
        """
        self.clear_primery_witches()
        # instruction for enter index file
        self.instructiondocfile = Label(self, text="enter index file pathname:")
        self.instructiondocfile.grid(row=1, column=0, columnspan=2, sticky=W)
        # text entry for index file pathname
        self.docfile = Entry(self)
        self.docfile.grid(row=1, column=5, columnspan=2, sticky=W)
        # instruction for enter query file
        self.instructionqueryfile = Label(self, text="enter query file pathname:")
        self.instructionqueryfile.grid(row=2, column=0, columnspan=2, sticky=W)
        # text entry for query file pathname
        self.queryfile = Entry(self)
        self.queryfile.grid(row=2, column=5, columnspan=2, sticky=W)
        # instruction for enter result file
        self.instructionresultfile = Label(self, text="enter result file pathname:")
        self.instructionresultfile.grid(row=3, column=0, columnspan=2, sticky=W)
        # text entry for result file pathname
        self.resultfile = Entry(self)
        self.resultfile.grid(row=3, column=5, columnspan=2, sticky=W)
        # subbmit button
        self.subbmitbutton = Button(self, text="Subbmit", command = self.third_action)
        self.subbmitbutton.grid(row=4, column=0, columnspan=2, sticky=W)
        # return button
        self.returnbutton = Button(self, text="return to menu", command=self.return_to_menu)
        self.returnbutton.grid(row=4, column=1, columnspan=2, sticky=W)

    def third_action(self):
        """
        :return: returns the documents rank from document file (in this case pickled file) according to the queries in
        queryfile and writes it to the resultflie in TREC 6 columns format
        """
        # text box
        self.text = Text(self, width=35, height=20, wrap=WORD)
        self.text.grid(row=4, column=0, columnspan=10, sticky=W)
        self.text.delete(0.0, END)
        message = 'wait for it...'
        self.text.insert(0.0, message)
        content1 = self.docfile.get()
        content2 = self.queryfile.get()
        try:
            with open(content1 +'.pickle', 'rb') as handle:
                Index = pickle.load(handle)
            Ranker = RankerEnvironment(Index)
            Ranker.loadQueries(content2)
        except Exception as e:
            self.text.delete(0.0, END)
            message = str(e).replace(",", "").replace("'", "").replace("(", "").replace(")", "")
            self.text.insert(0.0, message)
        else:
            try:
                Ranker.runQueries(self.resultfile.get())
            except Exception as e:
                self.text.delete(0.0, END)
                message = str(e).replace(",", "").replace("'", "").replace("(", "").replace(")", "")
                self.text.insert(0.0, message)
            else:
                self.text.delete(0.0, END)
                message = 'successful result !!!!'
                self.text.insert(0.0, message)

    def create_forth_action_witches(self):
        """
        :return: creates the forth action's witches
        """
        self.clear_primery_witches()
        # instruction for enter document file
        self.instructiondocfile = Label(self, text="enter document file pathname:")
        self.instructiondocfile.grid(row=1, column=0, columnspan=2, sticky=W)
        # text entry for document file pathname
        self.docfile = Entry(self)
        self.docfile.grid(row=1, column=5, columnspan=2, sticky=W)
        # subbmit button
        self.subbmitbutton = Button(self, text="Subbmit", command = self.forth_action)
        self.subbmitbutton.grid(row=2, column=0, columnspan=2, sticky=W)
        # return button
        self.returnbutton = Button(self, text="return to menu", command=self.return_to_menu)
        self.returnbutton.grid(row=2, column=1, columnspan=2, sticky=W)

    def forth_action(self):
        """
        :return: creates an Index from the docfile pathname and opens query box so the user can ask querys to the Index
        """
        # text box
        self.text = Text(self, width = 35, height = 20, wrap = WORD)
        self.text.grid(row = 6, column = 0, columnspan = 10, sticky = W)
        self.text.delete(0.0, END)
        message = 'wait for it...'
        self.text.insert(0.0, message)
        content = self.docfile.get()
        try:
            self.Index = IndexEnvironment()
            self.Index.addIndex(content)
        except Exception as e:
            self.text.delete(0.0, END)
            message = str(e).replace(",","").replace("'","").replace("(","").replace(")","")
            self.text.insert(0.0, message)
        else:
            # instruction for enter query
            self.instructionquery = Label(self, text="enter a query:", fg='red')
            self.instructionquery.grid(row=3, column=0, columnspan=2, sticky=W)
            # text entry for query
            self.query = Entry(self)
            self.query.grid(row=3, column=5, columnspan=2, sticky=W)
            # instruction for enter length
            self.instructionlength = Label(self, text="enter the length of result(an int):", fg='green')
            self.instructionlength.grid(row=4, column=0, columnspan=2, sticky=W)
            # text entry for length
            self.length = Entry(self)
            self.length.grid(row=4, column=5, columnspan=2, sticky=W)
            self.text.delete(0.0, END)
            message = 'input a query...'
            self.text.insert(0.0, message)
            # subbmit button
            self.subbmitbutton1 = Button(self, text="Ask Query", command=self.forth_action_query)
            self.subbmitbutton1.grid(row=5, column=0, columnspan=1, sticky=W)

    def forth_action_query(self):
        """
        :return: presents the result for the query asked on the Index
        """
        query = self.query.get()
        length = int(self.length.get())
        try:
            answer = self.Index.runQuery(query, length)
        except Exception as e:
            self.text.delete(0.0, END)
            message = str(e).replace(",", "").replace("'", "").replace("(", "").replace(")", "")
            self.text.insert(0.0, message)
        else:
            # result sign
            self.results = Label(self, text="the Doc ID's of the result:", fg='blue')
            self.results.grid(row=5, column=1, columnspan=5, sticky=W)
            self.text.delete(0.0, END)
            for i in range(len(answer)):
                message = "num - " + "'" + str(i+1) + "'" + " is - " + str(answer[i].Doc_ID) +" |"
                self.text.insert(0.0, message)

root = Tk()
root.title("techoogle")
root.geometry("900x500")
app = Application(root)


root.mainloop()