from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2
import os
import matplotlib.pyplot as plt

class ChickenDetect(object):
    def __init__(self):
        self.load_model()

    def load_model(self):
        # load the trained convolutional neural network
        print("[INFO] loading network...")
        self.model = load_model("model_chicken_monitor.cnn")

    def runAnalysis(self, image):
        self.image_name = image_name
        self.load_and_preprocess()
        self.check_image()

    def load_and_preprocess(self):
        print("Loading and Processing {}  ".format(self.image_name)).
        self.image = cv2.imread(os.path.join("unknown_images", self.image_name))
        self.orig = self.image.copy()

        # pre-process the image for classification
        self.image = cv2.resize(self.image, (28, 28))
        self.image = self.image.astype("float") / 255.0
        self.image = img_to_array(self.image)
        self.image = np.expand_dims(self.image, axis=0)

    def check_image(self):
        # classify the input image
        (self.notChicken, self.chicken) = self.model.predict(self.image)[0]

    def label_image(self):
        # build the label
        self.label = "Chicken" if self.chicken > self.notChicken else "Not a Chicken"
        self.proba = self.chicken if self.chicken > self.notChicken else self.notChicken
        self.label = "Label: {}: {:.2f}%".format(self.label, self.proba * 100)
        print(self.label)

        # draw the label on the image
        self.output = imutils.resize(self.orig, width=400)
        cv2.putText(self.output, self.label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        if self.chicken > self.notChicken:
            newDir = "Chicken"
        else:
            newDir = "Not_Chicken"

        cv2.imwrite(os.path.join(newDir, "{}_{}".format(newDir, image_name)), self.output)

    def display_image(image):
        plt.imshow(self.output, cmap=plt.cm.binary)
        plt.show()
        # show the output image
        #cv2.startWindowThread()
        #cv2.imshow("Output", output)
        #cv2.destroyAllWindows()
        #cv2.waitKey(0)
        #print("Exiting")

if __name__ == "__main__":
    label = 1
    display = 0
    move = 1

    # construct the argument parse and parse the arguments
    #ap = argparse.ArgumentParser()
    #ap.add_argument("-m", "--model", required=True, help="path to trained model model")
    #ap.add_argument("-i", "--image", required=True, help="path to input image")
    #args = vars(ap.parse_args())

    chickies = ChickenDetect()
    search_dir = os.listdir('unknown_images')

    x = 0
    while (x<10):
        for image_name in search_dir:
            chickies.runAnalysis(image_name)
            if label:
                chickies.label_image()
            if display:
                chickies.display_image()
        x += 1
