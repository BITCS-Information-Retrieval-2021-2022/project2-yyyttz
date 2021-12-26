import numpy as np


def char_to_idx(c):
    assert len(c) == 1
    c = c.lower()
    if ord('a') <= ord(c) <= ord('z'):
        return ord(c) - ord('a')
    else:
        return None


def char2_to_idx(c2):
    assert len(c2) == 2
    c2 = c2.lower()
    if ord(c2[0]) < ord('a') or ord(c2[0]) > ord('z'):
        return None
    if ord(c2[1]) < ord('a') or ord(c2[1]) > ord('z'):
        return None
    id1 = ord(c2[0]) - ord('a')
    id2 = ord(c2[1]) - ord('a')
    return 26 + id1 * 26 + id2


def name_to_vector(name, ngram=1):
    assert ngram in [1, 2]
    if ngram == 1:
        ids = [char_to_idx(c) for c in name]
        ids = [idx for idx in ids if idx is not None]
        vector = np.zeros(26)
        for idx in ids:
            vector[idx] += 1
    else:
        ids = [char_to_idx(c) for c in name]
        ids = [idx for idx in ids if idx is not None]
        for i in range(0, len(name) - 1):
            idx = char2_to_idx(name[i:i + 2])
            if idx is not None:
                ids.append(idx)
        vector = np.zeros(26 + 26 * 26)
        for idx in ids:
            vector[idx] += 1

    return vector


def vector_similarity(vector1, vector2):
    cos_sim = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    return cos_sim


def name_similarity(name1, name2, ngram=1):
    vec1, vec2 = name_to_vector(name1, ngram), name_to_vector(name2, ngram)
    return vector_similarity(vec1, vec2)


sim = name_similarity('michael s. myslobodsky', 'richard e straub', ngram=1)
print(sim)
sim = name_similarity('michael s. myslobodsky', 'abcdxyz', ngram=1)
print(sim)
sim = name_similarity('michael s. myslobodsky', 'richard e straub', ngram=2)
print(sim)
sim = name_similarity('michael s. myslobodsky', 'abcdxyz', ngram=2)
print(sim)
