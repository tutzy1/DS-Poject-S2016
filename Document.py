import numpy as np
from nltk.stem.porter import PorterStemmer
import re

class Document:
    def __init__(self, Doc_ID, Text):
        self.Doc_ID = Doc_ID # unique Doc_id
        self.Terms = {} # dictionery - keys: terms (strings) , values - arreys of positions(int)
        self.Stems = {} # dictionery - keys: stems (strings) , values - arreys of positions(int)
        self.Text = Text # original doc's text
        self.Tf_Idf_Ranks = {} # dictionary - keys: stems (strings) , values - Tf_Idf rank for the stem in the document

    def addTerm(self, Term, position):
        """
        :param Term: type - string - a word from text
        :param position: type - int
        :return: the function adds the Term and position to the correct place inside doc
        """
        if Term in self.Terms:
            self.Terms[Term] = np.append(self.Terms[Term],(position))
        else :
            self.Terms[Term] = np.array(position)
        return

    def addStem(self, Stem, position):
        """
        :param Stem: type - string - a word from text in stem form
        :param position: type - int
        :return: the function adds the Stem and position to the correct place inside doc
        """
        if Stem in self.Stems:
            self.Stems[Stem] = np.append(self.Stems[Stem],(position))
        else:
            self.Stems[Stem] = np.array(position)
        return

    def RestoreText(self):
        """
        :return: returns the original Text that was on the input of the doc
        """
        return self.Text

    def Tf_For_Stem(self, stem):
        """
        :param stem: type - string - a stem
        :return: the Tf value of the stem in the Doc (int)
        """
        doc_Text = str(self.Text)
        doc_Text_Vec = re.split("\s|[!-&]|[(-/]|[:-@]|[[-`]|[{-~]|(?='s)|[']", doc_Text)
        doc_Text_Vec = filter(None, doc_Text_Vec)
        return float(self.Stems[stem].size)/float(len(doc_Text_Vec))
