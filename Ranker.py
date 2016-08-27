import Index_envierment
import numpy as np
from nltk.stem.porter import PorterStemmer
from math import pow
from math import sqrt
from numpy import linalg as LA



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
        self.QueriesDict = {} # dictionary - keys: queryID (strings) , values - Query
        self.Index = Index # the index for this ranker environment

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

    def getQueriesMetadata(self, metaData):
        """
        :param metaData: type - string - either 'number' or 'text' (not capital sensitive)
        :return: returns a list of the required metadata from all the Querys in the Ranker
        :exceptions: if the metadata isn't number or text trows an Exception
        """
        result = []
        if metaData.lower() == 'number':
            for key in self.QueryIndex:
                result.append(key)
            return result
        elif metaData.lower() == 'text':
            for key in self.QueryIndex:
                temp = self.QueryIndex[key].RestoreText()
                result.append(temp)
            return result
        else:
            raise Exception('metadata -', metaData, ' does not exists (from getQueriesMetadata)')

    def Calc_Similarity(self, doc, query):
        """
        :param doc: type - Document - the document to calculate similarity with
        :param query: type - Query - the query to calculate similarity with
        :return: the method calculates and return the similarity value between the given Document
                 and Query according to cosin similarity metric.
                 for simplicity in the documentation - A represent the vector of the TfIdf values for the document stems,
                 B for the qeury.
        """
        if self.Index.Tf_Idf_Flag == 0:
            self.Index.TfIdfUpdate()
        sum = 0 # sum A_i*B_i
        for stem in query.Stems:
            q_idf = query.Stems[stem].size()
            if stem in doc.Stems:
                sum = sum + q_idf*doc.Tf_Idf_Ranks[stem]

        return (sum)



    def runQuery(self, queryID, limit = 0):
        """
        :param queryID: type - string - the ID of the query
        :param limit: type - int
        :return: the function runs the query with the given qeuryID, and output to
        the screen the rank of the documents
        """

