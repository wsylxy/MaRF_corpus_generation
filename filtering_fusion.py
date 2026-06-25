from collections import defaultdict
from custom_tokenize_new import LatexTokenizer
from custom_tokenize_new import *
from math_latex import *
from tqdm import tqdm
from os import makedirs
import bs4 as bs
import pickle
import os
import json
import re
import csv

# from tex_lex
data_path = './data_processing'
posts_file = json.load(open(f'{data_path}/cleaned_fusion_tagvote.json', encoding='utf-8'))
out_path = f'{data_path}'
makedirs(out_path, exist_ok=True)

splits = 1
voc_list = defaultdict(int)
found_space_token = False
defined_tokens = []
original_formulas = []
corrected_formulas = []
filtered_formulas = []
tok = LatexTokenizer()

def check_formula(eq, text_length):
    if len(eq)<15:
        return False
    for op in customize_operator:
        if op in eq:
            return False
    if (text_length/len(eq))>0.2:
        return False
    return True

def get_formulas(body):
    soup = bs.BeautifulSoup(body, "lxml")
    formulas = []
    for math in soup.find_all('span', {'class': "math-container"}):
        formulas.append(math.text)
    return formulas

# def write_block(block: list, post_type: str):
#     if len(block) > 0:
#         if post_type == 'question':
#             with open(f'{out_path}/processed/fusion_blocks_new2_tag_test2.txt', 'a', encoding='utf-8') as out_file:
#                 for row in block:  
#                     out_file.write('[Q]' + '\t' + row + '\n')
#         elif post_type == 'answer':
#             with open(f'{out_path}/processed/fusion_blocks_new2_tag_test2.txt', 'a', encoding='utf-8') as out_file:
#                 for row in block:  
#                     out_file.write('[R]' + '\t' + row + '\n')    
#                 out_file.write('\n')

def write_block(question_ps: list, answer_ps: list, question_id: int, tags: list, block_dict: dict):
    block_dict[question_id]["id"] = str(question_id)
    block_dict[question_id]["tags"] = tags
    block_dict[question_id]["question_posts"] = []
    for question in question_ps:
        block_dict[question_id]["question_posts"].append(question)
    block_dict[question_id]["answer_posts"] = []
    for answer in answer_ps:
        block_dict[question_id]["answer_posts"].append(answer)

def write_a_dict(post: str, formula: str, post_id: str, question_id: str):
    file_exists = os.path.isfile(f'{out_path}/a_dict_fusion.csv')
    with open(f'{out_path}/a_dict_fusion.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['post', 'formula', 'post_id', 'question_id'])
        writer.writerow([post, formula, post_id, question_id])


incorrect_count = 0
num_qf = 0
num_af = 0
longest_len = 512
num_clusters = 0
zero_formula_q = 0
num_answers = 0
block_dict = defaultdict(dict)
tag_dict = defaultdict(list)
for question in tqdm(posts_file, total=len(posts_file), desc='Processing formulas'):
    question_posts = []
    question_id = question['post_id']
    question_formulas = []  # list of formulas that pass filtering
    question_f = question['question_formulas'] #all formulas in a question
    question_tags = question["tags"]    # list
    question_tags = ' '.join(question_tags)
    question_post = question['question_posts']  #post is a string
    if len(question_f) == 0:    #if the question has no formulas
        continue
    for f in question_f:
        corrected_formula = correct_sin(f.strip().strip('.'))   #remove space and dot at the end of formula
        standard_formula = tok.standarization(corrected_formula)
        text_length = tok.count_textual_content(standard_formula) #some formulas may have some text, measure length of text part in a formula
        # print(standard_formula)
        if check_formula(standard_formula, text_length):
            question_formulas.append((standard_formula, f))    #each formula is a list
    if len(question_formulas) == 0:
        continue  
    # print(not_in_vocab)
    longest_formula, longest_f = max(question_formulas, key=lambda x: len(x[0]))
    if len(longest_formula) < 15:
        continue
    question_posts.append(f"{question_post}\t{longest_f}")
    # print(standard_post)      
    
    if 'answer_posts' in question:
        answer_count = 3 # editable: use up to answer_count answers with the most upvotes
        answer_posts = []
        assert len(question['answer_posts']) == len(question['answer_ids']), "length of answer_list doesn't match length of answer_ids"
        for i, (answer, answer_formula) in enumerate(zip(question['answer_posts'], question['answer_formulas'])):
            if len(answer_formula) == 0:
                continue
            single_answer_fs = []
            dict_fs = []
            answer_id = question['answer_ids'][i]
            if answer_count == 0:
                break
            answer_count -= 1  
            answer_post = answer
            answer_formulas = []    # list of formulas that pass filtering
            for f in answer_formula:
                a_corrected_formula = correct_sin(f.strip().strip('.'))
                a_standard_formula = tok.standarization(a_corrected_formula)
                a_text_length = tok.count_textual_content(a_standard_formula)
                if check_formula(a_standard_formula, a_text_length):
                    answer_formulas.append((a_standard_formula, f))  #each formula is a list
            if len(answer_formulas) == 0:
                continue
            a_longest_formula, a_longest_f = max(answer_formulas, key=lambda x: len(x[0]))
            if len(a_longest_formula) < 15:
                continue
            answer_posts.append(f"{answer_post}\t{a_longest_f}")
            num_answers += 1
            write_a_dict(post=answer_post, formula=a_longest_f, post_id=str(answer_id), question_id=question_id)
    else:
        continue
    # print(len(answer_ps))
    if len(question_posts) > 0 and len(answer_posts) > 0:
        num_clusters += 1
        write_block(question_ps=question_posts, answer_ps=answer_posts, question_id=question_id, tags=question_tags, block_dict=block_dict)
        tag_dict[question_tags].append(str(question_id))

with open(f'{out_path}/fusion_blocks.json', 'w', encoding='utf-8') as file:
    json.dump(block_dict, file)     

with open(f'{out_path}/tag_dict.json', 'w', encoding='utf-8') as file:
    json.dump(tag_dict, file)
print('num_clusters:', num_clusters)
print('num_answers', num_answers)


