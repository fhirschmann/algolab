# -*- coding: utf-8 -*-
"""
Sample data. This data can be used to test algorithms.

.. moduleauthor:: Fabian Hirschmann <fabian@hirschm.net>

Data Set 0
----------

.. plot::

    from algolab.data import points
    from pylab import *

    title("Data Set 0")
    plot(zip(*points[0])[0], zip(*points[0])[1], 'o-')
    show()

Data Set 1
----------

.. plot::

    from algolab.data import points
    from pylab import *

    title("Data Set 1")
    plot(zip(*points[1])[0], zip(*points[1])[1], 'o-')
    show()

Data Set 2 - 7
--------------

.. plot::

    from algolab.data import points
    from pylab import *

    data = {k: v for k, v in points.items() if k in [2, 3, 4, 5, 6, 7]}
    title("Data Set 2 - 5")
    lines = [plot(zip(*p)[0], zip(*p)[1], 'o-')[0] for p in data.values()]
    legend(lines, data.keys())
    show()

Data Set 8 - 11
---------------

.. plot::

    from algolab.data import points
    from pylab import *

    data = {k: v for k, v in points.items() if k in [8, 9, 10, 11]}
    title("Data Set 8 - 10")
    lines = [plot(zip(*p)[0], zip(*p)[1], 'o-')[0] for p in data.values()]
    legend(lines, data.keys())
    show()
"""

points = {}
npoints = {}

points[0] = [[483, 83], [483, 78], [479, 75], [474, 73], [467, 72],
        [462, 72], [456, 73], [450, 74], [444, 76], [437, 78],
        [430, 79], [424, 80], [415, 84], [410, 85], [405, 87],
        [399, 90], [393, 92], [386, 95], [380, 97], [374, 100],
        [369, 102], [364, 103], [359, 107], [349, 112], [342, 118],
        [337, 122], [331, 125], [325, 131], [320, 134], [315, 138],
        [309, 143], [305, 147], [301, 150], [295, 155], [290, 158],
        [285, 161], [281, 166], [277, 170], [272, 174], [269, 178],
        [265, 183], [260, 187], [256, 190], [253, 195], [249, 200],
        [246, 204], [241, 209], [238, 213], [236, 218], [234, 223],
        [233, 228], [231, 233], [231, 239], [231, 246], [231, 251],
        [231, 256], [233, 263], [234, 270], [235, 275], [239, 284],
        [242, 291], [245, 295], [248, 300], [251, 304], [255, 309],
        [258, 313], [264, 318], [272, 322], [278, 325], [283, 327],
        [288, 329], [294, 331], [299, 333], [305, 335], [313, 337],
        [320, 337], [326, 337], [332, 337], [337, 338], [342, 339],
        [349, 340], [355, 340], [360, 339], [366, 339], [371, 340],
        [376, 340], [383, 341], [391, 343], [397, 343], [402, 345],
        [407, 347], [412, 348], [417, 349], [424, 349], [430, 350],
        [437, 353], [445, 355], [450, 357], [455, 361], [460, 363],
        [466, 367], [472, 370], [478, 374], [483, 377], [487, 380],
        [496, 385], [501, 389], [506, 393], [510, 398], [514, 402],
        [519, 409], [523, 415], [527, 420], [530, 425], [532, 431],
        [535, 435], [537, 440], [539, 445], [540, 451], [540, 456],
        [540, 461], [540, 467], [539, 476], [537, 484], [535, 489],
        [532, 493], [530, 498], [527, 503], [522, 509], [518, 513],
        [515, 517], [510, 522], [505, 527], [498, 528], [491, 531],
        [485, 534], [477, 536], [471, 539], [466, 541], [458, 542],
        [452, 543], [444, 543], [438, 543], [432, 543], [426, 543],
        [420, 543], [413, 543], [406, 543], [399, 543], [390, 543],
        [383, 543], [374, 543], [366, 544], [360, 544], [351, 545],
        [344, 545], [336, 545], [327, 545], [320, 545], [314, 545],
        [306, 545], [298, 546], [292, 546], [280, 547], [272, 548],
        [267, 548], [258, 549], [251, 550], [246, 550], [238, 552],
        [231, 553], [225, 554], [218, 555], [212, 556], [205, 559],
        [199, 560], [193, 564], [188, 567], [179, 572], [171, 574],
        [167, 578], [161, 583], [157, 588], [153, 592], [150, 598],
        [147, 602], [144, 606], [141, 610], [141, 615], [140, 620],
        [139, 625], [139, 631], [139, 636], [140, 641], [142, 646],
        [145, 650], [148, 654]]
npoints[0] = [[p[0], p[1], i] for i, p in enumerate(points[0])]

points[1] = [[44, 95], [26, 91], [22, 90], [21, 90],
        [19, 89], [17, 89], [15, 87], [15, 86], [16, 85],
        [20, 83], [26, 81], [28, 80], [30, 79], [32, 74],
        [32, 72], [33, 71], [34, 70], [38, 68], [43, 66],
        [49, 64], [52, 63], [52, 62], [53, 59], [54, 57],
        [56, 56], [57, 56], [58, 56], [59, 56], [60, 56],
        [61, 55], [61, 55], [63, 55], [64, 55], [65, 54],
        [67, 54], [68, 54], [76, 53], [82, 52], [84, 52],
        [87, 51], [91, 51], [93, 51], [95, 51], [98, 50],
        [105, 50], [113, 49], [120, 48], [127, 48], [131, 47],
        [134, 47], [137, 47], [139, 47], [140, 47], [142, 47],
        [145, 46], [148, 46], [152, 46], [154, 46], [155, 46],
        [159, 46], [160, 46], [165, 46], [168, 46], [169, 45],
        [171, 45], [173, 45], [176, 45], [182, 45], [190, 44],
        [204, 43], [204, 43], [207, 43], [215, 40], [215, 38],
        [215, 37], [200, 37], [195, 41]]
npoints[1] = [[p[0], p[1], i] for i, p in enumerate(points[1])]

# Note: points[2] and points[3] have one common point!
npoints[2] = [[1, 1, 0], [2, 1, 1], [3, 1, 2], [4, 1, 3]]
points[2] = [[p[0], p[1]] for p in npoints[2]]

npoints[3] = [[3, 0, 4], [3, 1, 2], [3, 5, 5]]
points[3] = [[p[0], p[1]] for p in npoints[3]]

npoints[4] = [[2, 2, 6], [3, 1, 2]]
points[4] = [[p[0], p[1]] for p in npoints[4]]

npoints[5] = [[9, 4, 7], [8, 5, 8], [3, 1, 2], [8, 0, 9], [9, 1, 10], [8, 2, 11]]
points[5] = [[p[0], p[1]] for p in npoints[5]]

npoints[6] = [[0, 0, 12], [3, 1, 2], [6, 2, 13], [6, 3, 14]]
points[6] = [[p[0], p[1]] for p in npoints[6]]

npoints[7] = [[4, 3, 15], [6, 2, 13], [8, 3, 16]]
points[7] = [[p[0], p[1]] for p in npoints[7]]


# Intersection <-> Intersection connection
npoints[8] = [[1, 1, 0], [2, 2, 1]]
points[8] = [[p[0], p[1]] for p in npoints[8]]
npoints[9] = [[2, 0, 2], [3, 1, 3]]
points[9] = [[p[0], p[1]] for p in npoints[9]]
npoints[10] = [[2, 2, 1], [3, 1, 3]]
points[10] = [[p[0], p[1]] for p in npoints[10]]
npoints[11] = [[2, 2, 1], [3, 3, 4], [4, 4, 5], [4, 2, 6], [3, 1, 3]]
points[11] = [[p[0], p[1]] for p in npoints[11]]


# Parallel tracks
npoints[12] = [[1, 1, 0], [2, 1, 1], [3, 1, 2], [4, 1, 3], [5, 1, 4], [6, 1, 5], [7, 1, 6]]
points[12] = [[p[0], p[1]] for p in npoints[12]]
npoints[13] = [[2, 1, 1], [3, 1.3, 7], [4, 1.3, 8], [5, 1.3, 9], [6, 1, 5]]
points[13] = [[p[0], p[1]] for p in npoints[13]]
npoints[14] = [[4, 1, 3], [5, 0.7, 10], [6, 0.7, 11], [7, 1, 6]]
points[14] = [[p[0], p[1]] for p in npoints[14]]
npoints[15] = [[4, 1.3, 8], [4, 4, 12]]
