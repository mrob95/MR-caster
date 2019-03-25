# coding=utf-8
import re
from dragonfly import Clipboard

file_path = ""

def compile_regex_list(list):
    return [re.compile(raw_regex) for raw_regex in list]

def regex_match(regex_list, string):
    contained = False
    for regex in regex_list:
        if regex.search(string):
            contained = True
    return contained

ignore_starts = [
    r"%.*",
    r"\\end{document}",
    r"\\begin{table}",
    r"\\begin{figure}",
    r"\\begin{equation}"
    ]
ignore_ends = [
    r"%.*",
    r"\\begin{document}",
    r"\\end{table}",
    r"\\end{figure}",
    r"\\end{equation}"
    ]
ignore_words = [
    r"^$", r"^\-$", r"^\\$",
    r"\\parencite.*", r"\\textcite.*", r"\\printbibliography",
    r"\\maketitle", r"\\newpage", r"\\ldots",
    r"\\item",
    r"\\begin{enumerate}", r"\\end{enumerate}",
    r"\\begin{itemize}", r"\\end{itemize}",
    r"\\begin{abstract}", r"\\end{abstract}"
    ]

ignore_starts_compiled = compile_regex_list(ignore_starts)
ignore_ends_compiled = compile_regex_list(ignore_ends)
ignore_words_compiled = compile_regex_list(ignore_words)

def replace_inline_equations(line):
    return re.sub(r"\$.*\$", "inline", line)

# First pass iterates through lines, removing unwanted chunks
# (starting to ignore when it hits something in ignore_starts, ending...)
def extract_sentences(line_list):
    sentence_list=[]
    flag=False
    for line in line_list:
        line = line.replace("\n", "")
        line = line.strip()
        if regex_match(ignore_starts_compiled, line):
            flag = False
        if flag:
            line = replace_inline_equations(line)
            sentence_list.append(line)
        if regex_match(ignore_ends_compiled, line):
            flag = True
    return sentence_list

# Second pass iterates through words, removing unwanted words (ignore_words)
def extract_words(sentence_list):
    words_list = []
    for sentence in sentence_list:
        words = sentence.split(" ")
        for word in words:
            if not regex_match(ignore_words_compiled, word):
                words_list.append(word)
    return words_list

# This just gets a list of lines from a text file
def list_of_lines(path):
    with open(path,'r') as f:
        return [line for line in f]

def file_to_words_list(path):
    raw_line_list = list_of_lines(path)
    sentence_list = extract_sentences(raw_line_list)
    words_list = extract_words(sentence_list)
    return words_list

def word_count_from_string(raw):
    raw_line_list = raw.readlines()
    sentence_list = extract_sentences(raw_line_list)
    words_list = extract_words(sentence_list)
    print(words_list)
    return len(wordlist)

def word_count(file_path):
    return len(file_to_words_list(file_path))
