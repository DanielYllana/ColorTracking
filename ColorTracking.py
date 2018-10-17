import cv2
import _thread

# Set-up camera
cap = cv2.VideoCapture(0)

x = 0
y = 0

# Set RGB variables
red1 = 0
green1 = 0
blue1 = 255


# Scan width in image
def scanDani(y, worldRecord, img):
    similarX = -1

    for x in range(1, 480, 6):

        # Get Pixel by X and Y
        pixel = img[x, y]
        # Tracking Colors
        blue2 = pixel[0]
        green2 = pixel[1]
        red2 = pixel[2]

        # Find distance
        distance = abs(red1 - red2) + abs(green1 - green2) + abs(blue1 - blue2)

        # Find the most similar color
        if distance < worldRecord:
            worldRecord = distance
            similarX = x

    return similarX, worldRecord


def tracking():
    while True:

        # Get the image from the camera
        ret, img = cap.read()


        # Setting up world record
        worldRecord = 500

        # Scan height in image
        finalX = 0
        for i in range(0, 640, 6):
            x, worldRecord = scanDani(i, worldRecord, img)
            if x >= 0:
                finalX = x
                finalY = i

        # Draw circle in position
        cv2.circle(img, (finalY, finalX), 25, (0, 255, 0), 3)

        # Show Image
        cv2.imshow("img", img)

        # Break Loop
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break


_thread.start_new_thread(tracking())


cap.release()
cv2.destroyAllWindows()
