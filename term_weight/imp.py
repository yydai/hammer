import numpy as np
import jieba
import time
from collections import defaultdict
from collections import Counter

class TermWeighting(object):
    def __init__(self, corpus):
        self.corpus = corpus
        self.queries = []
        self.docs = []
        self.term_weight = {}
        self.query_term_weight = []
        self.global_one_term = {}
        self.query_term_dtf = []

    # 加载所有的查询词
    def load_corpus(self, fin=None):
        if not fin:
            fin = self.corpus

        with open(fin, 'r') as fin:
            for line in fin:
                items = line.strip().split('\t')
                if len(items) < 2:
                    continue
                self.queries.append(items[1])

        return self.queries

    def load_corpus_v2(self, fin=None):
        if not fin:
            fin = self.corpus

        with open(fin, 'r') as fin:
            for line in fin:
                line = line.strip()
                terms = line.split("\t")
                if len(terms) < 2:
                    continue
                self.docs.append(terms[0])
                self.queries.append(terms[1])

    def filter_single_global_term(self, query_term):
        for terms in query_term:
            for term in terms:
                if term not in self.global_one_term:
                    self.global_one_term[term] = 1
                else:
                    del self.global_one_term[term]

    def query_to_term(self, need_cut=False):
        query_term = []
        print("query count is {}".format(len(self.queries)))
        if not need_cut:
            for query in self.queries:
                items = query.split(",")
                t = []
                for term in items:
                    if not term.strip():
                        continue
                    else:
                        t.append(term.strip())
                query_term.append(t)
            return query_term

        for query in self.queries:
            if (len(query) < 4):
                query_term.append([query])
            else:
                t = []
                for term in list(jieba.cut(query)):
                    if not term.strip():
                        continue
                    else:
                        t.append(term.strip())
                query_term.append(t)

        return query_term

    def term_in_doc(self, term, idx):
        doc = self.docs[idx]
        doc_items = doc.strip().split(',')
        for doc_item in doc_items:
            if term in doc_item:
                return True
        return False

    # term 所在的query的index
    def construct_term_dict(self, query_term):
        term_doc_index = defaultdict(list)
        print("Start cutting query...")
        for index, terms in enumerate(query_term):
            for term in set(terms):
                term_doc_index[term].append(index)

        print("Cutting query finished")
        return term_doc_index

    def global_query_tw_sum(self, terms):
        q_terms_sum = 0
        for term in terms:
            q_terms_sum += self.term_weight.get(term, 1.0)
        return q_terms_sum

    def sum_iqt(self, doc_list, term):
        w_s = 0.0
        for index in doc_list:
            local_term_weight = self.query_term_weight[index]
            w = local_term_weight.get(term)
            w_s += 1.0 / w
        return w_s

    def save_dict(self, outfile):
        with open(outfile, 'w') as fout:
            for k, v in self.term_weight.items():
                line = '{}\t{}\n'.format(k, v)
                fout.write(line)
                fout.flush()

    def doc_tf(self, term, idx):
        doc = self.docs[idx]
        doc_items = doc.strip().split(',')
        counter = Counter(doc_items)
        c = counter.get(term, 0)
        return np.log(np.e + c * 1.0)

    def init_doc_tf(self, query_term):
        for index, query_terms in enumerate(query_term):
            t = {}
            for term in query_terms:
                t[term] = self.doc_tf(term, index)
            self.query_term_dtf.append(t)

    def one_epoch(self, query_term, term_doc_index, epoch):
        # update every query weight
        time_start = time.time()
        self.query_term_weight = []
        for index, terms in enumerate(query_term):
            tmp_query_tw = {}
            global_term_weight_sum = self.global_query_tw_sum(terms)

            for term in terms:
                if not term.strip():
                    continue
                if term not in self.term_weight:
                    # init with 1
                    self.term_weight[term] = 1.0

                global_term_weight = self.term_weight.get(term)  # init with 1
                # test doc_tf
                # t = self.query_term_dtf[index]
                # dtf = t.get(term, 1.0)
                # 注意，如果不需要dtf， 去掉即可
                query_term_weight = global_term_weight / global_term_weight_sum
                tmp_query_tw[term] = query_term_weight
            self.query_term_weight.append(tmp_query_tw)
            del tmp_query_tw

        # update global weight
        for term, _ in self.term_weight.items():
            doc_list = term_doc_index.get(term)
            N = len(doc_list)
            sum_iqt = self.sum_iqt(doc_list, term)
            self.term_weight[term] = N / sum_iqt

        time_end = time.time()

        print("Epoch {}: calc global weight finished, {} seconds used".format(epoch, time_end - time_start))
        print("\tExample: term=如家 and score={}".format(self.term_weight.get("如家")))

    def validate(self):
        res = 0.0
        for k, v in self.term_weight.items():
            res += v

        print("\tSum of weights: {}".format(res))

    def imp(self, fileout, epoch=50):
        self.load_corpus()
        query_term = self.query_to_term()
        term_doc_index = self.construct_term_dict(query_term)

        # if len(self.query_term_dtf) <= 0:
        # self.init_doc_tf(query_term)
        print('-'*10)
        for i in range(epoch):
            self.one_epoch(query_term, term_doc_index, i)
            self.validate()

        self.save_dict(fileout)

    def init_term_weight(self, query_term):
        for idx, terms in enumerate(query_term):
            tmp_query_tw = {}
            for term in terms:
                if self.term_in_doc(term, idx):
                    tmp_query_tw[term] = 1.0
                else:
                    tmp_query_tw[term] = 0.1

                if term not in self.term_weight:
                    self.term_weight[term] = 0.0

            self.query_term_weight.append(tmp_query_tw)

    def imp_v2(self, fileout, epoch):
        self.load_corpus_v2()
        query_term = self.query_to_term()
        term_doc_index = self.construct_term_dict(query_term)


        # use different init value for query term weight
        self.init_term_weight(query_term)

        if len(self.query_term_dtf) <= 0:
            self.init_doc_tf(query_term)

        for term, _ in self.term_weight.items():
            doc_list = term_doc_index.get(term)
            N = len(doc_list)
            sum_iqt = self.sum_iqt(doc_list, term)
            self.term_weight[term] = N / sum_iqt

        print('-'*10)
        for i in range(epoch):
            self.one_epoch(query_term, term_doc_index, i)
            self.validate()

        self.save_dict(fileout)

    def tf(self, term, query_terms):
        counter = Counter(query_terms)
        return counter.get(term, 0) * 1.0 / len(query_terms)

    def idf(self, term, doc_n, N):
        return np.log(N * 1.0 / doc_n)

    def tf_idf(self, fileout):
        self.load_corpus()
        query_term = self.query_to_term()
        term_doc_index = self.construct_term_dict(query_term)
        N = len(query_term)

        count = 0
        for query_terms in query_term:
            if count % 10000 == 0:
                print("handled count: {}".format(count))
            for term in query_terms:
                doc_len = len(term_doc_index.get(term))
                tfidf = self.tf(term, query_terms) * self.idf(term, doc_len, N)
                if term not in self.term_weight:
                    self.term_weight[term] = 0.0
                self.term_weight[term] += tfidf * 1.0 / doc_len
            count += 1

        self.save_dict(fileout)


if __name__ == '__main__':
    corpus = './data/termweight-03-12.txt'  # file one line format : doc \t query
    tw = TermWeighting(corpus)
    tw.imp()
