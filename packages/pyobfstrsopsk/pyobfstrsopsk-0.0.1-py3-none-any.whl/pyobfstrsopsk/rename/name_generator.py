import itertools
import keyword
import random
import string

from pyobfstrsopsk.rename.util import builtins

CHINESE_CHARS = [
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这',
    '中', '大', '为', '来', '以', '到', '他', '时', '用', '们', '生', '作', '地', '于', '出', '分', '对', '成', '可', '主', '发', '年', '动', '同',
    '工', '能', '下', '过', '子', '产', '种', '面', '而', '方', '后', '多', '定', '行', '学', '所', '民', '得', '经', '十', '三', '之', '进', '等', '部', '度', '家',
    '水', '化', '高', '自', '二', '理', '起', '小', '物', '现', '实', '加', '量', '两', '体', '制', '机', '当', '使', '点', '从', '业', '本', '把', '性', '应', '开'
]

JAPANESE_CHARS = [
    'の', 'に', 'は', 'を', 'た', 'が', 'で', 'て', 'と', 'し', 'れ', 'さ', 'ある', 'いる', 'も', 'する', 'から', 'な', 'こと', 'として', 'い', 'や', 'れる', 'など', 'なっ', 'ため', 'でき', 'その',
    'あっ', 'まで', 'より', 'による', 'その後', 'しかし', 'それでも', 'つまり', 'このように', 'ところ', 'それ', 'これ', 'あれ', 'どれ', 'ここ', 'そこ', 'あそこ', 'どこ', 'こちら', 'そちら',
    'あちら', 'どちら', 'いずれ', 'それぞれ', 'どちらか', 'どちらも', 'これら', 'あれら', 'それら',
    '見る', '聞く', '話す', '読む', '書く', '食べる', '飲む', '行く', '来る', 'なる', '思う', '知る', '分かる', '考える', '言う', '教える', '習う', '覚える'
]

ALL_CJ_CHARS = CHINESE_CHARS + JAPANESE_CHARS


def random_generator(length=40):
    valid_first = string.ascii_uppercase + string.ascii_lowercase
    valid_rest = string.digits + valid_first + '_'

    while True:
        first = [random.choice(valid_first)]
        rest = [random.choice(valid_rest) for i in range(length - 1)]
        yield ''.join(first + rest)


def name_generator():
    while True:
        length = random.randint(5, 9)
        name = '_stein_' + ''.join(random.choices(ALL_CJ_CHARS, k=length))
        if not keyword.iskeyword(name):
            yield name


def name_filter():
    """
    Yield all valid python identifiers

    Name are returned sorted by length, then string sort order.

    Names that already have meaning in python (keywords and builtins)
    will not be included in the output.

    :rtype: Iterable[str]

    """

    reserved = keyword.kwlist + dir(builtins)

    for name in name_generator():
        if name not in reserved:
            yield name
