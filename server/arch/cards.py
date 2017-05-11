#-*- coding: utf-8 -*-

import random


#含有大小王，54张牌，1到13表示黑桃，14-26表示红桃，27-39表示梅花，40-52表示方片
#53表示小王，54表示大王。系统把数字发给客户端，由客户端去完成转化
#Q_CARDS = [i for i in xrange(1, 55)]
#NO_Q_CARDS = [i for i in xrange(1, 52)]


def magic_shuffle(card_type, num):
    res = {}
    cards = [i for i in xrange(1, 53)]
    random.shuffle(cards)

    if card_type == "public":
        #NOTE(jake):公用一张，每人发两张
        res["cards"] = cards[0: num * 2]
        res["pubilc"] = cards[random.randint(num * 2 + 1, 51)]
    elif card_type == "private":
        #NOTE(jake):每人梦幻一张，系统给每人发两张
        res["cards"] = cards[0: num * 2]

    return res


def shuffle(card_type, num):
    """
    num:需要几组牌，即几个玩家。此函数直接发三张
    """
    res = {}
    if card_type == "Q_CARDS":
        q_cards = [i for i in xrange(1, 55)]
        random.shuffle(q_cards)
        res["cards"] = q_cards[0: num * 3]
    elif card_type == "NO_Q_CARDS":
        no_q_cards = [i for i in xrange(1, 53)]
        #如果不够随机，可以再调用次函数一次
        random.shuffle(no_q_cards)
        res["cards"] = no_q_cards[0: num * 3]

    return res


def make_up_9_cards(_card=55, num=2):
    """
    _card:传55表示，包含大小王；传53表示没有大小王
    """
    res = {}
    cards = [i for i in xrange(1, _card)]
    random.shuffle(cards)
    res["cards"] = cards[0: num * 9]
    return res


def test():
    print shuffle("Q_CARDS", 4)
    print shuffle("Q_CARDS", 3)
    print shuffle("NO_Q_CARDS", 5)
    print shuffle("NO_Q_CARDS", 3)

    print make_up_9_cards(num=3)
    print make_up_9_cards(num=2)

    print magic_shuffle("public", 5)
    print magic_shuffle("public", 4)
    print magic_shuffle("public", 3)

    print magic_shuffle("private", 6)
    print magic_shuffle("private", 5)
    print magic_shuffle("private", 4)
    print magic_shuffle("private", 3)


if __name__ == "__main__":
    test()
