import cv2
import math
import numpy
import numpy as np

######################## nacitanie obrazu a urcenie konstant ###################################
imageName = "railway.jpg"
houghThreshold = 375
#testimage - 150, railway- 375, railway2 - 125, fence - 175

inputImage = cv2.imread(imageName, cv2.IMREAD_GRAYSCALE)
originalImage = cv2.imread(imageName)



############################# aplikacia cannyho filtra #####################################
threshold1 = 90
threshold2 = 140
blurImage = cv2.GaussianBlur(inputImage, (5, 5), 1)
cannyImage = cv2.Canny(blurImage, threshold1, threshold2)

imageHeight, imageWidth = cannyImage.shape
imageCenterX = imageWidth/2
imageCenterY = imageHeight/2

#print("Rozmery obrazku: " + str(imageWidth) + "x" + str(imageHeight))
#print(cannyImage)


#############################  inicializacia akumulatora ########################################
thetas = numpy.linspace(0, 179, 180)
houghHeight = int(round(np.sqrt(imageHeight**2 + imageWidth**2)))
accumulatorHeight = int(np.ceil(houghHeight)*2)
accumulatorWidth = len(thetas)

accumulator = [[0 for x in range(accumulatorWidth)] for y in range(accumulatorHeight)]

#accumulatorCenterX = accumulatorWidth/2
#accumulatorCenterY = accumulatorHeight/2

print("Akumulator rozmery: " + str(len(accumulator)) + "x" + str(len(accumulator[0])))


##################################  inkrementacia buniek akumulatora ####################################
for y in range(0, imageHeight):
    for x in range(0, imageWidth):
        if cannyImage[y][x] > 250: #je to hrana
            for index, t in enumerate(thetas):
                r = ((x-imageCenterX)*math.cos(np.deg2rad(t))) + ((y-imageCenterY)*math.sin(np.deg2rad(t)))
                #print("X: " + str(x) + " Y: " + str(y) + " r: " + str(np.around(houghHeight+r)) + " t: " + str(t))
                accumulator[int(houghHeight+r)][index] += 1

print("Accumulator done")



#######################################  prehladavanie hodnot v akumulatore #################################
results = []
for r in range(0, accumulatorHeight):
    for t in range(0, accumulatorWidth):
        if accumulator[r][t] > houghThreshold: #bunka presiahla threshold - je to usecka
            maximum = accumulator[r][t]
            for ly in range(-4, 5): #prehladavanie okolia 9x9
                for lx in range(-4, 5):
                    if 0 <= (ly + r) < accumulatorHeight and 0 <= (lx + t) < accumulatorWidth:
                        if accumulator[r+ly][t+lx] > maximum:
                            maximum = accumulator[r+ly][t+lx]
                            ly = 5
                            lx = 5

            if maximum > accumulator[r][t]: #najdena hodnota nie je lokalne maximum
                continue

            if 45 <= thetas[t] <= 135: #priamka siaha od praveho okraja k lavemu
                x1 = 0
                y1 = int(((r-houghHeight) - ((x1 - imageWidth/2)*math.cos(np.deg2rad(t))))/math.sin(np.deg2rad(t))+imageHeight/2)
                x2 = imageWidth
                y2 = int(((r-houghHeight) - ((x2 - imageWidth/2)*math.cos(np.deg2rad(t))))/math.sin(np.deg2rad(t))+imageHeight/2)
                line = [x1, y1, x2, y2]
                results.append(line)
                #print("Suradnice: [" + str(x1) + "," + str(y1) + "] - [" + str(x2) + "," + str(y2) + "], prva rovnica - Uhol:" + str(thetas[t]))
            else: #priamka siaha zhora dole
                y1 = 0
                x1 = int(((r-houghHeight) - ((y1 - imageHeight/2)*math.sin(np.deg2rad(t))))/math.cos(np.deg2rad(t))+imageWidth/2)
                y2 = imageHeight
                x2 = int(((r-houghHeight) - ((y2 - imageHeight/2)*math.sin(np.deg2rad(t))))/math.cos(np.deg2rad(t))+imageWidth/2)
                line = [x1, y1, x2, y2]
                results.append(line)
#               print("Suradnice: [" + str(x1) + "," + str(y1) + "] -> [" + str(x2) + "," + str(y2) + "], druha rovnica - Uhol:" + str(thetas[t]))



####################################### vypisanie a vykreslenie vysledkov ##########################################
print(len(results))
print(results)
for i in range(0, len(results)):
    cv2.line(originalImage, (int(results[i][0]), int(results[i][1])), (int(results[i][2]), int(results[i][3])), (0, 0, 255), 2)

cv2.imshow("input", inputImage)
cv2.imshow("canny", cannyImage)
cv2.imshow("original", originalImage)
cv2.waitKey()
