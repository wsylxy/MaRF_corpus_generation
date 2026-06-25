from itertools import combinations, permutations
import random
import json
import sys

filepath = 'data_processing/fusion_blocks.json'
# filepath = 'test.json'
# test_set_file = './data_processing/processed/fusion_blocks_all_formulas_tag_testset.json'
tag_path = 'data_processing/tag_dict.json'
outfile = 'data_processing/train_set_fusion.txt'
clusters = [] #list of all clusters
cluster = [] #list of each cluster
random.seed(42)
target_len = 80 # number upperbound of each question's (q, a) pairs
longest_len = 256

clusters = json.load(open(file=filepath, encoding='utf-8'))
# test_set_clusters = json.load(open(file=test_set_file, encoding='utf-8'))
# clusters.update(test_set_clusters)
# print(test_set_clusters)
# for id in test_set_clusters.keys():
#     print(id)
# sys.exit()
tags_dict = json.load(open(file=tag_path, encoding='utf-8'))
num_neg = 3 #numbers of negative sample in each row

    
def generate_pairs(cluster:list, target_len:int, question_tags:str):
    question_posts = cluster["question_posts"]
    answer_posts = cluster["answer_posts"]
    output = []
    for q in question_posts:
        for a in answer_posts:
            output.append((q, a))
    if question_tags == 'testset':
        print(question_tags)
        return output
    if len(output) > target_len:
        output = output[:target_len-1]
    return output

def write_trainset(clusters, num_neg, outfile, target_len):
    total_output = []
    # ids_all = [id for id in clusters.keys() if not id.startswith("A.")]
    ids_all = [id for id in clusters.keys()]
    for i, (cluster_id, question_cluster) in enumerate(clusters.items()):
        # print(question_cluster)
        question_id = str(question_cluster["id"])
        question_tags = question_cluster["tags"]

        pos = generate_pairs(cluster=question_cluster, target_len=target_len, question_tags=question_tags)  # generate (query, positive) pairs
        if not question_tags == 'testset':
            ref = tags_dict[question_tags]
            # print("ref before remove", ref)
            ref.remove(question_id)
            # print("ref after remove", ref)
            count_same_tag_answer = 0
            same_tag_answers = []
            # print(ref)
            for id in ref:  # count the number of answer formulas under the same tag
                id = str(id)
                count_same_tag_answer += len(clusters[id]["answer_posts"])
                same_tag_answers.extend(clusters[id]["answer_posts"])
            # print("count_same_tag_answer", count_same_tag_answer)
            # print("same_tag_answer:", len(same_tag_answer))
            if count_same_tag_answer > num_neg*len(pos):    # find negatives from answers with the same tag
                neg_samples = random.sample(same_tag_answers, k=num_neg*len(pos))
            else:
                rest_need = num_neg*len(pos)-count_same_tag_answer
                # print("rest_need:", rest_need)
                while True:
                    rest_neg_cluster_ids = random.sample(ids_all, rest_need)
                    if question_id not in rest_neg_cluster_ids:
                        break
                neg_samples = same_tag_answers
                # print("neg_samples before", len(neg_samples))
                for neg_id in rest_neg_cluster_ids: # for answers under other tags, sample one
                    neg_sample = random.sample(clusters[neg_id]["answer_posts"], k=1)[0]
                    neg_samples.append(neg_sample)
                # print("neg_samples before", len(neg_samples))
        elif question_tags == 'testset':
            ref = ids_all
            ref.remove(question_cluster['avoid_q_ids'])
            ref = [x for x in ref if not x.startswith("A.")]
            while True:
                ids = random.sample(ref, k=num_neg*len(pos))
                if question_id not in ids:
                    break
            neg_samples = []
            for neg_id in ids:
                neg_sample = random.sample(clusters[neg_id]["answer_posts"], k=1)[0]
                neg_samples.append(neg_sample)
        random.shuffle(neg_samples)
        out = []
        id_neg = 0
        assert len(neg_samples) == num_neg*len(pos)
        for j, p in enumerate(pos):
            line = [p[0], p[1]]
            id_neg = j*num_neg
            line.extend(neg_samples[id_neg:id_neg+num_neg])
            # print('neg length', len(negs))
            out.append(line)
        print(i)
        # print('line length:', len(line))
        for line in out:
            total_output.append(line)
    random.shuffle(total_output)
    # total_output = random.sample(population=total_output, k=10000000)

    print("total:", len(total_output))
    write_file = open(file=outfile, mode='a', encoding='utf-8')
    for line in total_output:
        write_file.write('\t'.join(line))
        write_file.write('\n')
    write_file.close()

write_trainset(clusters, num_neg, outfile=outfile, target_len=target_len)