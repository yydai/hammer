def extract(s1, s2):
    s1_list = list(s1)
    s2_list = list(s2)
    s1_len = len(s1_list)
    s2_len = len(s2_list)
    idx_i = 0
    idx_j = 0
    common = []
    new_str = ''
    stop_str = ''
    while idx_i < len(s1_list):
        s = s1_list[idx_i]
        try:
            idx_j = s2.index(s)
            while idx_j < s2_len and idx_i < s1_len and s2_list[idx_j] == s1_list[idx_i]:
                new_str += s2_list[idx_j]
                idx_j += 1
                idx_i += 1

            if new_str:
                if len(new_str.strip()) > 1:
                    common.extend(new_str.strip().split())

                else:
                    stop_str += new_str
                new_str = ''

            if idx_i > 0:
                idx_i -= 1
        except:
            stop_str += s

        idx_i += 1
    common = [word for word in common if len(word) > 1]
    return list(set(common)), stop_str.split()
