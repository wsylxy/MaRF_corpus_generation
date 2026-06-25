# from ARQMathCode.post_reader_record import DataReaderRecord
from collections import defaultdict
from datetime import datetime
import ARQMathCode.post_reader_record as ARQ
import bs4 as bs
import json
import os
import gc


data_path = '../ARQmath_process/raw_data'
out_dir = './data_processing'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
reader = ARQ.DataReaderRecord(data_path, version='.V1.3')
questions = {}
answers = defaultdict(list)

def get_formulas(body):
    soup = bs.BeautifulSoup(body, "lxml")
    formulas = []
    for math in soup.find_all('span', {'class': "math-container"}):
        formulas.append(math.text)
    return formulas

def get_posts(body):
    soup = bs.BeautifulSoup(body, "lxml")
    result = ""
    for element in soup.recursiveChildGenerator():
        if element.name == 'span' and 'math-container' in element.get('class', []):
            math_text = element.get_text(strip=True).strip().strip('.').strip('$')
            # if math_text.startswith('$') and math_text.endswith('$'):
            #     math_text = math_text[1:-1]
            result += f"{math_text}"
        elif isinstance(element, str):
            parent = element.parent
            if parent.name == 'span' and 'math-container' in parent.get('class', []):
                continue
            result += element
        if hasattr(element, "tail") and element.tail:
            result += element.tail
    del soup
    return result.strip()
answer_count = 6
count = 0
cleaned = []
for year in [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]:
# for year in [2016]:
    print(f'Year - {year}')
    now = datetime.now()
    questions = reader.get_list_of_questions_posted_in_a_year(year)
    for q in questions:
        thread = {} #each question is a dictionary
        # print(q.body)
        question = get_posts(q.body)
        # print(thread['question_posts'])
        thread['post_id'] = q.post_id
        try:
            title = get_posts(q.title)
            thread['question_posts'] = f"{title}. {question}"
        except:
            print('could not parse', q.title)
        thread['question_formulas'] = get_formulas(q.title)
        thread['question_formulas'].extend(get_formulas(q.body))
        thread['tags'] = q.tags
        if q.answers:
            thread['answer_ids'] = []
            thread['answer_posts'] = []
            thread['answer_formulas'] = []
            thread['score'] = []
            for a in q.answers:   
                thread['answer_ids'].append(a.post_id)
                thread['answer_posts'].append(get_posts(a.body))
                thread['answer_formulas'].append(get_formulas(a.body))
                thread['score'].append(a.score)
        cleaned.append(thread)
        # print(thread['question_formulas'])
        count += 1
        # print(count)
    print(f'{year} took: {datetime.now() - now}')
    # json.dump(cleaned, open(f'{out_dir}/cleaned_posts_{year}.json', 'w', encoding='utf-8'))
    # cleaned = []
del reader
del questions
print("finished")
json.dump(cleaned, open(f'{out_dir}/cleaned_fusion_tagvote.json', 'w', encoding='utf-8'))

