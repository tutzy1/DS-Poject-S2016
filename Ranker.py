import xml.etree.ElementTree as ET
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

    def RestoreText(self):
        """
        :return: returns the original Text that was on the input of the query
        """
        return self.Text



class RankerEnvironment:
    def __init__(self, Index):
        self.QueriesDict = {} # dictionary - keys: queryID (strings) , values - Query
        self.Index = Index # the index for this ranker environment

    def query_Exists_In_Dictionary(self, Query_ID):
        """
        :param Query_ID: type - string/int - a Query's Query_ID
        :return: True if the query already exists in the dictionary and False if not
        """
        if Query_ID in self.QueriesDict :
            return True
        else:
            return False

    def loadQueries(self, pathname):
        """
        :param pathname: a path to a queries XML file
        :return: the function opens the file and saves the queries to the in the dictionary QueriesDict
        :exceptions: throws exceptions if one of the Queries in the file from pathname already exists in the dictionary
        or if the file can't be opened
        """
        try:
            f = open(pathname, 'r')
        except (OSError, IOError) as e:
            raise Exception("file from -'",pathname,"'is not found")
        tree = ET.parse(f)
        root = tree.getroot()
        for Quer in root.findall('query'):
            Query_ID = (Quer.find('number').text).strip()
            text = Quer.find('text').text
            if self.Query_Exists_In_Dictionary(Query_ID):
                raise Exception("the query titeled -'", Query_ID, "' is already inside the dictionary")
            temp = Query(Query_ID, text)
            self.Break_Text_Into_Query(temp, text)
        f.close()
        return

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
            for key in self.QueriesDict:
                result.append(key)
            return result
        elif metaData.lower() == 'text':
            for key in self.QueriesDict:
                temp = self.QueriesDict[key].RestoreText()
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
        the screen the rank of the documents (up to |limit| documents) in "TREC 6 columns" format
        exceptions: throws an exception if the given queryID does not exist in the dictionary,
                    or a relevant exception if the query matching the given queryID is empty.
        """
        if not self.query_Exists_In_Dictionary(queryID):
            raise Exception("the query titeled -'", queryID, "' does not exist in dictionary")
        else:
            query = self.QueriesDict[queryID].RestoreText()
            result = self.get_Result_In_TREC6Columns(queryID, query, limit)
            print result
        return

    def get_Result_In_TREC6Columns(self, queryID, query, limit = 0):
        """
        :param queryID: type - int
        :param query: type - string - the query's text
        :param limit: type - int - maximum amount of documents in the result
        :return: return the result of the given query in a "TREC 6 columns" formatted string
        exceptions: throws an exception if the query is empty.
        """
        documents = self.Index.runQuery(query, limit)
        i = 1
        result = ""
        for tup in documents:
            result = result + "{0} {1} {2} {3} {4} {5}\n".format(queryID, "Q0", tup[0], i, tup[1], "col6")
            i = i + 1
        return result

    def runQueries(self, limit = 0):
        """
        :param limit: type - int - maximum amount of documents in the result of a single query
        :return: for each query in the dictionary - rank all the documents in the Index accordingly
                 and print the result for each query (up to |limit| documents per query) to screen
                 in
                 "TREC 6 columns" format.
        exceptions: throws an exception if one of the queries in the dictionary is empty.
        """
        for queryID in self.QueriesDict:
            self.runQuery(queryID, limit)
        return


