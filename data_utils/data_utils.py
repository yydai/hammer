import numpy as np
import random

class DataUtils(object):
    def __init__(self):
        pass

    @classmethod
    def test(self):
        print("import success")

    @classmethod
    def read2list(self, filepath, is_strip=True, is_remove_dup=False):
        out = []
        with open(filepath, 'r') as fin:
            for line in fin:
                if is_strip:
                    line = line.strip()
                out.append(line)
        if is_remove_dup:
            return list(set(out))

        return out

    @classmethod
    def remove_file(self, filepath):
        import os
        if os.path.exists(filepath):
            os.remove(filepath)

    @classmethod
    def write2list(self, data, fileout, end_with='\n'):
        if not isinstance(data, list):
            raise ValueError("Wrong type of data: {}".format(type(data)))

        self.remove_file(fileout)
        f = open(fileout, 'a')
        for line in data:
            f.write(line + end_with)
            f.flush()
        print('Write success, the outpath is {}, and write length is {}'.format(fileout, len(data)))

    @classmethod
    def shuffle_list(self, data):
        data = random.shuffle(data)
        return data

    @classmethod
    def get_sample_n(self, data, n):
        return random.sample(data, n)

    @classmethod
    def split_data(self, data, r=0.2):
        length = len(data)
        index = np.arange(length)

        random.seed(24)
        random.shuffle(index)

        part1_index = index[:int(r * length)]
        part2_index = index[int(r * length):]

        part1_data = [data[i] for i in part1_index]
        part2_data = [data[i] for i in part2_index]

        return part1_data, part2_data

    @classmethod
    def merge_file(self, f1, f2, fout):
        f1_data = self.read2list(f1, is_strip=False)
        f2_data = self.read2list(f2, is_strip=False)
        f1_data.append('\n\n')
        f1_data.extend(f2_data)

        self.remove_file(fout)
        f = open(fout, 'a')
        for line in f1_data:
            f.write(line)
            f.flush()

        print("success")

    @classmethod
    def append2file(self, f1, f2):
        f1_data = self.read2list(f1, is_strip=False)
        f2_data = self.read2list(f2, is_strip=False)
        f1_data.append('\n\n')
        f1_data.extend(f2_data)
        self.remove_file(f1)

        f = open(f1, 'w')
        for line in f1_data:
            f.write(line)
            f.flush()

        print("success")

    @classmethod
    def merge_list(self, l1, l2, fout):
        l1.append('\n\n')
        l1.extend(l2)

        self.remove_file(fout)
        f = open(fout, 'a')
        for line in l1:
            f.write(line)
            f.flush()

        print("success")
