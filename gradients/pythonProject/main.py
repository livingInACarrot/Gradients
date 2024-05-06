import numpy as np
from PIL import Image, ImageDraw

image = Image.open("hands.jpg")
draw = ImageDraw.Draw(image)
width = image.size[0]
height = image.size[1]
pix = image.load()

min_x = 20
min_y = 30
prox = 20

image = np.array(image)

def left_up_neighbours (i, j):
    if i == 0:
        if j == 0:
            return []
        elif j == height - 1:
            return [[0, height - 2]]
        else:
            return [[i, j - 1]]
    elif i == width - 1:
        if j == 0:
            return [[width - 2, 0]]
        elif j == height - 1:
            return [[width - 1, height - 2], [width - 2, height - 1]]
        else:
            return [[i - 1, j], [i, j - 1]]
    elif j == 0:
        return [[i - 1, j]]
    elif j == height - 1:
        return [[i - 1, j], [i, j - 1]]
    else:
        return [[i - 1, j], [i, j - 1]]

grad = np.zeros((width, height))
for i in range(width):
    for j in range(height):
        nei = left_up_neighbours(i, j)
        passes = True
        for k in nei:
            for c in range(3):
                if abs(int(image[k[1]][k[0]][c]) - int(image[j][i][c])) > prox:
                    passes = False
        if not passes:
            grad[i][j] = 1


def solver(a, n, m, restrict=None):
    ans = 0

    d = [-1] * m
    d1 = [0] * m
    d2 = [0] * m

    A = None
    B = None

    st = list()

    for i in range(n):
        for j in range(m):
            if a[i][j] == 1:
                d[j] = i

        while len(st):
            st.pop()

        for j in range(m):
            while len(st) > 0 and d[st[len(st) - 1]] <= d[j]:
                st.pop()

            d1[j] = -1 if len(st) == 0 else st[len(st) - 1]
            st.append(j)

        while len(st):
            st.pop()

        for j in range(m - 1, -1, -1):
            while len(st) and d[st[len(st) - 1]] <= d[j]:
                st.pop()
            d2[j] = m if len(st) == 0 else st[len(st) - 1]
            st.append(j)

        for j in range(m):
            area = (i - d[j]) * (d2[j] - d1[j] - 1)
            if area > ans:
                A = (d[j] + 1, d1[j] + 1)
                B = (i, d2[j] - 1)
                ans = area

    return (ans, A, B)

max_rec = solver(grad, width, height)
first = True
rectangles = []
while max_rec[0] > 1000:
    if not first:
        max_rec = solver(grad, width, height)
    if max_rec[0] < 1000:
        break
    first = False
    for hi in range(max_rec[1][0], max_rec[2][0]):
        for wi in range(max_rec[1][1], max_rec[2][1]):
            grad[hi][wi] = 1
    rectangles.append(max_rec)
    im = Image.fromarray(image)
    im.save("your_file.jpeg")
    for i in range(width):
        for j in range(height):
            if grad[i][j] == 0:
                image[j][i] = [0, 0, 0]
            else:
                image[j][i] = [255, 255, 255]

print(rectangles)

