import numpy as np
from nltk.stem.porter import PorterStemmer
import re
from string import lower as lowC


class Query:
    def __init__(self, Query_ID, Text):
        self.Query_ID = Query_ID # unique Query_id
        self.Terms = {} # dictionery - keys: terms (strings) , values - arreys of positions(int)
        self.Stems = {} # dictionery - keys: stems (strings) , values - arreys of positions(int)
        self.Text = Text # original query's text
        self.Break_Text_Into_Query()

    def addTerm(self, Term, position):
        """
        :param Term: type - string - a word from text
        :param position: type - int
        :return: the function adds the Term and position to the correct place inside query
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
        :return: the function adds the Stem and position to the correct place inside Query
        """
        if Stem in self.Stems:
            self.Stems[Stem] = np.append(self.Stems[Stem],(position))
        else:
            self.Stems[Stem] = np.array(position)
        return

    def RestoreText(self):
        """
        :return: returns the original Text that was on the input of the query
        """
        return self.Text

    def Break_Text_Into_Query(self):
        """
        :return: the function breaks the words in the text and adds it to the Query
        """
        Text = str(self.Text)
        TextVec = re.split("\s|[!-&]|[(-/]|[:-@]|[[-`]|[{-~]|(?='s)|[']", Text)
        TextVec = filter(None, TextVec)
        st = PorterStemmer()
        for i in range(len(TextVec)) :
            term = TextVec[i].lower()
            stem = str(st.stem(term))
            self.addTerm(term, i)
            self.addStem(stem, i)
        return