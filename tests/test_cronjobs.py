from tools import cronjobs
def test_daily():
    """
    >>> divmod(1,60)
(0, 1)
>>> divmod(5,60)
(0, 5)
>>> divmod(120,60)
(2, 0)
>>> divmod(-60,60)
(-1, 0)
>>> divmod(1,60)
(0, 1)
>>> divmod(1 + (60 * 21),60)
(21, 1)
>>> divmod(1 + (60 * 22),60)
(22, 1)
>>> divmod((4 * 60) + (60 * 22),60)
(26, 0)
>>> divmod((4 * 60) + (60 * 22),60)[1]
0
>>> divmod((4 * 60) + (60 * 22),60)[0]
# I think this is the rough logic for setting the hour
26
>>> divmod((4 * 60) + (60 * 22),60)[0] % 24
"""
    # assert below happens at 9pm
    print cronjobs.daily([('q', 'c', 't')])
    # assert below happens at 3am
    print cronjobs.daily([('q-{}'.format(i), 'c-{}'.format(i), 't-{}'.format(i)) for i in range (0, 60*6)])

