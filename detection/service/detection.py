import cv2

class Detector:
    def __init__(self, config, images):
        self.__config = config
        
        self.__model = cv2.createBackgroundSubtractorMOG2(history = self.__config["HISTORY"])
        self.__model.setBackgroundRatio(self.__config["BACKGROUND_RATIO"])
        self.__model.setNMixtures(self.__config["NMIXTURES"])
        self.__model.setVarThreshold(self.__config["THRESHOLD"])
        
        for image in images:
            self.__model.apply(image, 0)

        
    def detect(self, image):
        mask = self.__gauss(image)
        mask = self.__correction(mask)
        fragments = self.__fragmentsSelection(mask)
        return fragments

    def __gauss(self, image):
        return self.__model.apply(image)

    def __correction(self, mask):
        element = cv2.getStructuringElement(cv2.MORPH_RECT, self.__config["CLOSING_RECT"])
        mask = cv2.erode(mask, element, iterations = 1)
        mask = cv2.dilate(mask, element, iterations = 1)
        element = cv2.getStructuringElement(cv2.MORPH_RECT, self.__config["OPENING_RECT"])
        mask = cv2.dilate(mask, element, iterations = 1)
        mask = cv2.erode(mask, element)
        return mask

    def __fragmentsSelection(self, mask):
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        fragments = []
        if len(contours) != 0:
            for i in range(len(contours)):
                hull = cv2.convexHull(contours[i], False)
                x, y, w, h = cv2.boundingRect(hull)
                fragment = Fragment(x, y, w, h)
                fragment.reshape(self.__config["INDENT"], mask.shape[1], mask.shape[0])
                #fragment.makeSquare()
                fragments.append(fragment)           
        return fragments

class Fragment:
    def __init__(self, left, top, width, height):
        self.__left = left
        self.__top = top
        self.__right = left + width
        self.__bottom = top + height
##    def makeSquare(self):
##        if self.__right - self.__left > self.__bottom - self.__top:
##            self.__bottom = self.__top + self.__right - self.__left
##        else:
##            self.__right = self.__left + self.__bottom - self.__top
    def reshape(self, indent, maxright, maxbottom, minleft = 0, mintop = 0):
        if self.__left - indent < minleft:
            self.__left =  minleft
        else:
            self.__left = self.__left - indent
            
        if self.__right + indent > maxright:
            self.__right = maxright
        else:
            self.__right =  self.__right + indent
            
        if self.__top - indent < mintop:
            self.__top = mintop
        else:
            self.__top =  self.__top - indent
            
        if self.__bottom + indent > maxbottom:
            self.__bottom = maxbottom
        else:
            self.__bottom =  self.__bottom + indent          
    def getLeft(self):
        return self.__left
    def getTop(self):
        return self.__top
    def getRight(self):
        return self.__right
    def getBottom(self):
        return self.__bottom
    def setFragmentCoords(self, left, top, right, bottom):
        self.__left = left
        self.__top = top
        self.__right = right
        self.__bottom = bottom
        
