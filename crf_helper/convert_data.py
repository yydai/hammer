def convert(data):
    '''
    convert indexed data to BIO labeled data
    data: type map
    [{"text": "raw string", "labels": [[0, 1, 'O'], [2, 4, 'P']]}]
    '''

    if not isinstance(data, list):
        raise ValueError("need a list, but got a type of {}".format(type(data)))

    res = []
    for item in data:
        text = item.get('text', None)
        labels = item.get('labels', None)
        if not (text and labels):
            raise ValueError("text and labels must contained")

        word_label = {}
        for i in range(len(text)):
            word_label[i] = 'O'

        for label in labels:
            start, end, l = label
            for i in range(start, end):
                if i == start:
                    word_label[i] = 'B-{}'.format(l)
                else:
                    word_label[i] = 'I-{}'.format(l)

        for i in range(len(text)):
            res.append('{}\t{}\n'.format(text[i], word_label[i]))
        res.append('\n')

    return res

def crf2human(file, remove=False):
    pair = []
    string = ''
    status = 'OUT'
    pre_l = None
    pre_t = None
    result = []
    with open(file, 'r') as fin:
        for line in fin:
            if not line.strip("\n"):
                string += '/{} '.format(pre_l)
                result.append(string)
                string = ''
                continue

            items = line.split()
            w = items[0]
            l = items[-1]
            l = l.strip().split("-")

            if l[0] == 'O':
                if status != 'O':
                    if pre_l and string:
                        string += '/{} '.format(pre_l)
                    status = 'O'

                string += w
                pre_l = 'O'
                pre_t = 'O'
            else:
                cur_l = l[-1]
                if status != cur_l or (l[0] != pre_t and pre_t != 'B'):
                    status = cur_l
                    if string:
                        string += '/{} '.format(pre_l)

                string += w
                pre_l = cur_l
                pre_t = l[0]

    string += '/{}'.format(pre_l)
    return result
