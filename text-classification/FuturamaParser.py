from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from collections import defaultdict
from itertools import product
from typing import Dict, List
import requests, re, spacy


class FuturamaParser:
    def __init__(self, url_base: str, url_stem: str) -> None:
        self.nlp = spacy.load('en')
        self.url_base = url_base
        self.url_stem = url_stem

    def get_script_soup(self, script_url: str):
        '''
        get_script_soup

        input: script_url (str) - URL from master link page
        output: BS4 object - The soup object for the script page.

        The actual script texts are from a secondary link off of the master link page.
        This is a helper function that takes a script url from the master link page,
        and goes down two levels to get the script text bs4 object.
        '''
        script_wrapper_soup = BeautifulSoup(requests.get(script_url).content, 'html.parser')
        script_url = script_wrapper_soup \
            .find_all("table", {"class": "script-details"})[0] \
            .find_all('a')[-1] \
            .attrs['href']
        return BeautifulSoup(requests.get(self.url_base + script_url).content, 'html.parser')


    def clean_line(self, line:str) -> List[str]:
        '''
        clean_line

        input: line (str) - a line from the script
        return: list of cleaned, lemetized tokens

        This does all the NLP preprocessing:
            * lower text
            * split on special characters, while removing annotations
            * remove stop words
            * perform lemmetization
        '''
        line = line.lower()
        line = [x for x in re.findall(r"[\w()']+", line) if x[0] != "(" and x[-1] != ")"]
        s_stop = set(stopwords.words())
        line = ' '.join([word for word in line if word not in s_stop])
        return [token.lemma_ for token in self.nlp(line)]


    def lines_by_character(self, script_url: str, b_first: bool) -> Dict[str, list]:
        '''
        lines_by_character

        input:
            * script_url (str) - The script URL
            * b_first (bool) - If it's the first episode.  Bender is introduced as "ROBOT",
                                and I hope to preserve as many of his lines as possible.
        return: dict - a dictionary where the key is the character that said it, and the value
                        is the lines in this episode.
        '''
        script_soup = self.get_script_soup(script_url)
        script_text = script_soup.find_all('td', {"class": "scrtext"})[0].find('body').text.split('\n')
        character = None
        b_actions = False
        d_lines: Dict[str, list] = defaultdict(list)
        cur_line = ''
        for line in [x.strip() for x in script_text if x.strip() != ''][6:]:
            if line == line.upper():
                d_lines[character].append(cur_line)
                cur_line = ""
                character = line
                if b_first == True and character == 'ROBOT':
                    character = 'BENDER'
                continue
            if character == None:
                continue
            if line[0] == "[" and line[-1] == "]":
                continue
            if line[0] == "[":
                b_actions = True
            if b_actions == True:
                if line[-1] == "]":
                    b_actions = False
                continue
            cur_line += " " + line
        return d_lines

    @staticmethod
    def merge_dols(dol1: Dict[str, list], dol2: Dict[str, list]) -> Dict[str, list]:
        ks = set(dol1).union(dol2)
        return dict((k, dol1.get(k, []) + dol2.get(k, [])) for k in ks)

    @staticmethod
    def flatten_sublist(l_in: list) -> List[str]:
        return [item for sublist in l_in for item in sublist]

    def parse_scripts(self, limit: int) -> None:
        d_all_lines: Dict[str, list] = {}
        req = requests.get(self.url_stem)
        soup = BeautifulSoup(req.content, 'html.parser')
        n_scripts = 0
        for td in soup.find_all('td'):
            if td.find('h1') is None or td.find('h1').text != "Futurama Transcripts":
                continue
            for a in td.find('a'):
                if a.title() == '#':
                    continue
                for aa in td.find_all('a'):
                    print(aa.attrs['title'])
                    d_script_lines = self.lines_by_character(self.url_stem + aa.attrs['href'].replace(" ", "%20"), aa.attrs['title'] == 'Space Pilot 3000 Script')
                    d_all_lines = self.merge_dols(d_all_lines, d_script_lines)
                    n_scripts += 1
                    if limit != -1 and n_scripts > limit:
                        break
        self.d_all_lines = d_all_lines

    def characters(self) -> List[str]:
        return list(self.d_all_lines.keys())

    def cleaned_character_lines(self, name: str, min_words: int) -> List[str]:
        return self.flatten_sublist([self.clean_line(x) for x in self.d_all_lines[name] if len(self.clean_line(x)) > min_words])

    def labeled_data(self, target_name: str, min_words: int) -> List:
        l_ret = []
        for k, v in self.d_all_lines.items():
            for line in v:
                cleaned = self.clean_line(line)
                if len(cleaned) > min_words:
                    l_ret.append((1 if k==target_name else 0, " ".join(cleaned)))
        return l_ret
