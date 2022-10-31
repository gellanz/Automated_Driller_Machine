import cv2
class ProcessPinHolesCenters():
    def __init__(self, img, raw_coords):
        self.img = img
        self.one_channel, _, _ = cv2.split(self.img)
        self.image_bin_not = cv2.bitwise_not(self.one_channel)
        self.raw_coords = raw_coords
        self.coords_processed = []
        self.get_img_coords()

    def get_img_coords(self):
        for i in range(0, len(self.raw_coords), 4):
            x1, y1 = int(self.raw_coords[i]), int(self.raw_coords[i+1])
            x2, y2 = int(self.raw_coords[i+2]), int(self.raw_coords[i+3])
            half_x = (x2-x1) // 2
            half_y = (y1-y2) // 2
            # Big box to detect the center
            x1 = x1 - half_x // 2 if x1 - half_x // 2 > 0 else 0
            x2 = x2 + half_x // 2
            y1 = y1 + half_y // 2 if y1 - half_y // 2 > 0 else 0
            y2 = y2 - half_y // 2
            self.get_sub_image_center(x1,y1,x2,y2)

    def get_sub_image_center(self, x1, y1, x2, y2):
        sub_image = self.image_bin_not[y2:y1, x2:x1]
        detected_circles = cv2.HoughCircles(
                                sub_image,
                                cv2.HOUGH_GRADIENT, 1, 20,
                                param1 = 50,
                                param2 = 5,
                                minRadius = 2,
                                maxRadius = 20
                            )

        for pt in detected_circles[0, :]:
            # circle coords
            a, b, r = int(pt[0]), int(pt[1]), int(pt[2])
            # writing positions to a txt file
            new_x1, new_x2 = x1 + (a - r), x2 + (a + r)
            new_y1, new_y2 = y1 + (b + r), y2 + (b - r)
            self.coords_processed.append(new_x1)
            self.coords_processed.append(new_y1)
            self.coords_processed.append(new_x2)
            self.coords_processed.append(new_y2)

    def show_green_holes(self):
        for i in range(0, len(self.coords_processed), 4):
            x1, y1 = int(self.coords_processed[i]), int(self.coords_processed[i+1])
            x2, y2 = int(self.coords_processed[i+2]), int(self.coords_processed[i+3])
            half_x = (x2-x1) // 2
            half_y = (y1-y2) // 2

            cv2.circle(self.img, (x1 + half_x, y1 - half_y), abs(int((y1-y2)/2)), (0, 255, 0), 2)

        cv2.imshow("processed", self.img)
        cv2.waitKey(0)

img = cv2.imread("/Users/angel.elizarraras/MyStuff/Automated_Driller_Machine/dataset/useful_handpicked_rot/12100011_test_2.jpg")
cv2.imshow("originalz", img)
cv2.waitKey(0)
coords = [329,352,303,326,521,351,494,325,505,183,480,157]
x = ProcessPinHolesCenters(img, coords)
x.get_img_coords()
x.show_green_holes()