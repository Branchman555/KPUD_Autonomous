import helper
import cv2

IMG_PATH = './Images/'
img = cv2.imread(IMG_PATH + "sample" + '.jpg')

img = helper.crop(img, 0.1, 0.2)
cv2.imwrite('./Images/' + 'sample_crop' + '.jpg', img)

img, angles = helper.random_flip(img, 1, flipping_prob=1)
cv2.imwrite('./Images/' + 'sample_flip' + '.jpg', img)

img = helper.random_gamma(img)
cv2.imwrite('./Images/' + 'sample_gamma' + '.jpg', img)

img, angles = helper.random_shear(img, 0.5, shear_range=100)
cv2.imwrite('./Images/' + 'sample_sheer' + '.jpg', img)
print(angles)

