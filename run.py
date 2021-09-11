# import the necessary packages
import numpy as np
import argparse
import cv2

def transparentOverlay(src, overlay, pos=(0, 0), scale=1):
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape  # Size of foreground
    rows, cols, a = src.shape  # Size of background Image
    y, x = pos[0], pos[1]  # Position of foreground/overlay image
    blackimg = np.zeros((rows, cols, a), np.uint8)
    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
            blackimg[x + i][y + j][:3] = alpha * overlay[i][j][:3] + (1 - alpha) * blackimg[x + i][y + j][:3]
            blackimg[x + i][y + j][3] = 255
    return blackimg


def changeWatermarkColor(waterImg, oriImg, pos=(10, 100)):
    tgtColor = oriImg[pos[1], pos[0]]
    h, w, a = waterImg.shape
    retImg = np.zeros((h, w, a), np.uint8)
    for i in range(h):
        for j in range(w):
            retImg[i][j][:3] = 1.5 * tgtColor[:3]
            retImg[i][j][3] = waterImg[i][j][3]
    return retImg

def addImageWatermark(waterImg, OriImg, opacity, pos=(10,100), scale=1):
    opacity = opacity / 100
    tempImg = OriImg.copy()
    clrWaterMark = changeWatermarkColor(waterImg, OriImg, pos)
    #cv2.imwrite("output.png", clrWaterMark)
    overlay = transparentOverlay(tempImg, clrWaterMark, pos, scale)
    #cv2.imwrite("overlay.jpg", overlay)
    # apply the overlay
    return cv2.addWeighted(overlay, opacity, OriImg, 1, 0, OriImg)

def takeRadius(elem):
    return elem[1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", help = "path to the image file")
    ap.add_argument("-t", "--threshold", type = int, default=200,
        help = "high light threshold(1-255)")
    ap.add_argument("-r", "--radius", type = int, default = 2,
        help = "Output light point radius threshold")
    ap.add_argument("-w", "--watermark", default = "spike.png",
        help = "Add water mark image")
    ap.add_argument("-n", "--spikenum", type = int, default = 5,
        help = "Number of spikes")
    args = vars(ap.parse_args())

    # load the image and convert it to grayscale
    image = cv2.imread(args["image"], -1)
    if image.shape[2] == 3:
        print("Add alpha channel")
        image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
        image[:, :, 3] = 255
    spike = cv2.imread(args["watermark"], -1)
    star_sz = image.shape[1] / 900
    if args["threshold"] > star_sz:
        threshold = args["threshold"]
    else:
        threshold = star_sz
    radius_limit = args["radius"]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]
    cnts, h = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    nums = 0
    scale = 0.1
    spikeList = []
    size_param = (image.shape[1] / 1920) * 80 / spike.shape[1]
    # loop over the contours
    for (i, c) in enumerate(cnts):
        ((cX, cY), radius) = cv2.minEnclosingCircle(c)
        # cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)
        if radius < radius_limit:
            continue
        spikeList.append(((cX, cY), radius))
    spikeList.sort(key=takeRadius, reverse=True)

    for ((cX, cY), radius) in spikeList:
        scale = size_param * radius
        img_size = scale * spike.shape[1]
        if img_size > image.shape[1] / 3:
            continue
        image = addImageWatermark(spike, image, 100, (int(cX - img_size / 2), int(cY - img_size / 2)), scale)

        if nums < args["spikenum"]:
            nums += 1
        else:
            break
    cv2.imwrite("output.jpg", image)

if __name__ == '__main__':
    main()
