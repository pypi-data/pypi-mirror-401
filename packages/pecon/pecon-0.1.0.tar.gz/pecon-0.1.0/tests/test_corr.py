import pecon as pc

def test_corr():
    x = [2,4,6,8,10]
    y = [1,3,5,7,9]

    coef, pvalue = pc.corr(x, y)

    assert coef == 1
