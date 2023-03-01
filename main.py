import plotly.express as px

def s_pom(k, xs, ys, M):
    hk = xs[k + 1] - xs[k]
    def fun(x):
        return (1 / hk) * ((1 / 6) * M[k] * pow((xs[k+1] - x), 3)
                           + (1 / 6) * M[k+1] * pow((x - xs[k]), 3)
                           + (ys[k] - (1 / 6) * M[k] * hk**2) * (xs[k+1] - x)
                           + (ys[k+1] - (1 / 6) * M[k+1] * hk**2) * (x - xs[k]))
    return fun

def s(xs, ys, ps):
    ds = ilorazy(xs, ys)
    qs = q(xs, ds, ps)
    M = momenty(xs, ps, qs)
    n = len(xs)-1
    tab = []
    for i in range(n):
        tab.append(s_pom(i, xs, ys, M))
    return tab

def ilorazy(xs, ys):
    n = len(xs) - 1
    tab = []
    for i in range(1, n):
        wyn = (((ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i])) - ((ys[i] - ys[i - 1]) / (xs[i] - xs[i - 1]))) / (
                xs[i + 1] - xs[i - 1])
        tab.append(6*wyn)
    return tab

def p(xs):
    n = len(xs) - 1
    tab = [0]
    for i in range(1, n - 1):
        lam = (xs[i] - xs[i - 1]) / (xs[i + 1] - xs[i - 1])
        p = (lam - 1) / (lam * tab[i - 1] + 2)
        tab.append(p)
    return tab

def q(xs, ds, ps):
    n = len(xs) - 1
    tab = [0]
    for i in range(1, n):
        lam = (xs[i] - xs[i - 1]) / (xs[i + 1] - xs[i - 1])
        q = (ds[i - 1] - lam * tab[i - 1]) / (lam * ps[i - 1] + 2)
        tab.append(q)
    return tab

def momenty(xs, ps, qs):
    n = len(xs) - 1
    tab = [0]
    tab.append(qs[-1])
    for i in range(n - 2, 0, -1):
        tab.append(ps[i] * tab[n-i - 1] + qs[i])
    tab.append(0)
    tab.reverse()
    return tab

def data(n):
    f = open("dane/nifs" + str(n) + ".txt")
    x = []
    y = []
    u = []
    flag = 'x'
    for line in f:
        line = line.split()[0]
        if line == 'x' or line == 'y' or line == 'u':
            flag = line
            continue
        if flag == 'x': x.append(float(line))
        elif flag == 'y': y.append(float(line))
        else: u.append(float(line))
    f.close()
    return [x, y, u]

def podpis():
    fig = px.line(range_x = [0,50], range_y = [0,56])
    for i in range(1,11):
        x_tab, y_tab, u_tab = data(i)
        n = len(x_tab)-1
        xs = [i/n for i in range(n+1)]
        ps = p(xs)
        sx = s(xs, x_tab, ps)
        sy = s(xs, y_tab, ps)
        x = []
        y = []
        k = 1
        for u in u_tab:
            while k < n and u > xs[k]: k += 1
            x.append(sx[k - 1](u))
            y.append(sy[k - 1](u))
        if i == 1: fig.add_scatter(x=x,y=y, line_color='blue', line_width=6, opacity=0.9)
        else: fig.add_scatter(x=x,y=y, line_color='blue', line_width=4, opacity=0.9)

    fig.update_layout(height=900, width=900)
    fig.update_traces(mode='lines')
    fig.show()


podpis()
