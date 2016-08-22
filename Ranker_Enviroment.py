import xml.etree.ElementTree as ET
import numpy as np
from nltk.stem.porter import PorterStemmer
import re
import Index_envierment # need to see how to make it work

class Query:
    def __init__(self, Query_ID, Text):
        self.Query_ID = Query_ID # unique query id
        self.Text = Text # the original query's text
        self.Terms = {}  # dictionery - keys: terms (strings) , values - arreys of positions(int)
        self.Stems = {}  # dictionery - keys: stems (strings) , values - arreys of positions(int)

    def addTerm(self, Term, position):
        """
        :param Term: type - string - a word from text
        :param position: type - int
        :return: the function adds the Term and position to the correct place inside Query
        """
        if Term in self.Terms:
            self.Terms[Term] = np.append(self.Terms[Term], (position))
        else:
            self.Terms[Term] = np.array(position)
        return

    def addStem(self, Stem, position):
        """
        :param Stem: type - string - a word from text in stem form
        :param position: type - int
        :return: the function adds the Stem and position to the correct place inside Query
        """
        if Stem in self.Stems:
            self.Stems[Stem] = np.append(self.Stems[Stem], (position))
        else:
            self.Stems[Stem] = np.array(position)
        return

    def RestoreText(self):
        """
        :return: returns the original Text that was on the input of the Query
        """
        return self.Text

    def Tf_For_Stem(self, stem):
        return self.Stems[stem].size

    def Break_Text_Into_Query(self, Text):
        """
        :param Doc: type - Query
        :param Text: type - string
        :return: the function breaks the words in the text and adds it to the Query
        """
        Text = str(Text)
        TextVec = re.split("\s|[!-&]|[(-/]|[:-@]|[[-`]|[{-~]|(?='s)|[']", Text)
        TextVec = filter(None, TextVec)
        for i in range(len(TextVec)):
            term = TextVec[i]
            st = PorterStemmer()
            stem = st.stem(term)
            self.addTerm(term, i)
            self.addStem(stem, i)
        return


class RankerEnvironment:
    def __init__(self, Index):
        """
        :param Index: type - IndexEnvironment
        """
        self.Index = Index
        self.QueryIndex = {}  # dictionery - keys: Query_IDs , values - Querys

    def Query_Exists_In_Index(self, Query_ID):
        """
        :param Query_ID: type - string/int - a Query's Query_ID
        :return: True if the Query exists in the index already and False if not
        """
        if Query_ID in self.QueryIndex :
            return True
        else:
            return False

    def loadQueries(self, pathname):
        """
        :param pathname: a path to a file
        :return: he function open the file and fills the RankerEnvironment type according to it
        :exceptions: throws exceptions if one of the querys in the file from pathname already exists in the Ranker
        and if the file cannot be opened
        """
        try:
            f = open(pathname, 'r')
        except (OSError, IOError) as e:
            raise Exception("file from -'", pathname, "'is not found")
        tree = ET.parse(f)
        root = tree.getroot()
        for Quer in root.findall('query'):
            Query_ID = (Quer.find('number').text).strip()
            Text = Quer.find('text').text
            if self.Query_Exists_In_Index(Query_ID):
                raise Exception("the Query titeled -'", Query_ID, "' is already inside the Ranker")
            temp = Query(Query_ID, Text)
            temp.Break_Text_Into_Query(Text)
            self.QueryIndex[Query_ID] = temp
        f.close()
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
        else :
            raise Exception('metadata -',metaData,' does not exists (from getQueriesMetadata)')