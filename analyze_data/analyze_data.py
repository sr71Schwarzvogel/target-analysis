import matplotlib as mlp
import matplotlib.pyplot as plt
import cv2
import time

point_list = []

# Print laser
f = open('data.txt', 'r')
img = cv2.imread('target1.jpeg', cv2.IMREAD_COLOR)
img2 = cv2.resize(img, (300, 300))
not_first = False

for line in f:
    point = line.split(",")
    point_list.append(point)

for idx, point in enumerate(point_list):
    if len(point) == 3:
        if not_first:
            print(point)
            print(int(float(point[1])), int(float(point[0])))
            cv2.line(img, (int(float(point_list[idx - 1][1])), int(float(point_list[idx - 1][0]))), (int(float(point[1])), int(float(point[0]))), (0, 0, 255), 2)
            cv2.circle(img, (int(float(point[1])), int(float(point[0]))), 5, (0, 255, 0), 5)


        not_first = True

    if len(point) == 2:

        if not_first:
            #print(idx)
            #print(point_list[idx][0])
            cv2.line(img, (int(float(point_list[idx - 1][1])), int(float(point_list[idx - 1][0]))),
                     (int(float(point[1])), int(float(point[0]))), (0, 0, 255), 2)
            # lvalue = laser
            # print("Here was the laser: ", lvalue)
            # plt.scatter(lvalue[0], lvalue[1])
        not_first = True

    cv2.imshow('Bild', img)

    #time.sleep(0.01)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cv2.destroyAllWindows()

# Wertebereich für x-Achse festlegen:
#x2 = [num**2 for num in hvalue]
#x3 = [num**3 for num in hvalue]

# Diagramm-Gitter einblenden:
#plt.grid(True)
#plt.savefig('graph.png')

# Diagramm ausgeben:
plt.show()


'''
import xlsxwriter

#Try 2
# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Hit_Analysis.xlsx')
worksheet = workbook.add_worksheet()

# Some data we want to write to the worksheet.
values = (
    ['Here was a hit', hit],
    ['Here was the laser', laser],
    )

# Start from the first cell. Rows and columns are zero indexed.
#row = 0
#col = 0


# Iterate over the data and write it out row by row.
for value in (values):
    worksheet.write(values)
    worksheet.write(values)

workbook.close()

'''


'''
#Write into Excel Test 1
import xlwt

def output(filename, sheet, list1, list2, x, y, z):
    book = xlwt.Workbook()
    sh = book.add_sheet(sheet)

    variables = [x, y, z]
    x_desc = 'Display'
    y_desc = 'Dominance'
    z_desc = 'Test'
    desc = [x_desc, y_desc, z_desc]

    col1_name = 'Stimulus Time'
    col2_name = 'Reaction Time'

    # You may need to group the variables together
    # for n, (v_desc, v) in enumerate(zip(desc, variables)):
    for n, v_desc, v in enumerate(zip(desc, variables)):
        sh.write(n, 0, v_desc)
        sh.write(n, 1, v)

    n += 1

    sh.write(n, 0, col1_name)
    sh.write(n, 1, col2_name)

    for m, e1 in enumerate(list1, n + 1):
        sh.write(m, 0, e1)

    for m, e2 in enumerate(list2, n + 1):
        sh.write(m, 1, e2)

    book.save("test.xls")
'''