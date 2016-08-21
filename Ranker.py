import Index_envierment
import numpy as np
from nltk.stem.porter import PorterStemmer

class Query:
    def __init__(self, Query_ID, Text):
        self.Query_ID = Query_ID # unique Query_id
        self.Terms = {} # dictionery - keys: terms (strings) , values - arreys of positions(int)
        self.Stems = {} # dictionery - keys: stems (strings) , values - arreys of positions(int)
        self.Text = Text # original query's text

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


class RankerEnvironment:
    def __init__(self, Index):
        self.QueriesDict = {}
        self.Index = Index

    def Break_Text_Into_Query(self, Query, Text):
        """
        :param Query: type - Query
        :param Text: type - string
        :return: the function breaks the words in the text and adds it to the Query
        """
        Text = str(Text)
        TextVec = re.split("\s|[!-&]|[(-/]|[:-@]|[[-`]|[{-~]|(?='s)|[']", Text)
        TextVec = filter(None, TextVec)
        for i in range(len(TextVec)) :
            term = TextVec[i]
            st = PorterStemmer() # Is it necessary? Doesn't it create new object of the class in each iteration?
            stem = st.stem(term)
            Query.addTerm(term, i)
            Query.addStem(stem, i)
        return

    def runQuery(self, queryID, limit = 0):
        """
        :param queryID: type - string - the ID of the query
        :param limit: type - int
        :return: the function runs the query with the givven qeuryID, and output to
        the screen the rank of the documents
        """
        if queryID in self.QueriesDict:
            query = self.QueriesDict[qeuryID]
            N = self.