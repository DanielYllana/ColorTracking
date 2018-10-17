import cv2
import _thread

# Set-up camera
cap = cv2.VideoCapture(0)

x = 0
y = 0


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
        distance = 1*abs(red1 - red2) + 1*abs(green1 - green2) + 1*abs(blue1 - blue2)

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


# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
mouseX = 0
mouseY = 0
click = False


def click_and_crop(event, x1, y1, flags, param):
    # grab references to the global variables
    global mouseX, mouseY, click

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        mouseX = x1
        mouseY = y1
        click = True


while click == False:
    # load the image, clone it, and setup the mouse callback function
    ret, img = cap.read()
    cv2.setMouseCallback("img", click_and_crop)
    # Show Image
    cv2.imshow("img", img)

    # Break Loop
    k = cv2.waitKey(1) & 0xff


# Get the BGR values of the x and y coordinates
pixel= img[mouseY, mouseX]

red1 = pixel[2]
green1 = pixel[1]
blue1 = pixel[0]


_thread.start_new_thread(tracking())

cap.release()
cv2.destroyAllWindows()
