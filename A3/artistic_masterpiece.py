import cv2
import numpy as np
from matplotlib import pyplot as plt


"""
Function that runs an intensity threshold on a given image and
creates a new one with only the pixels above the threshold
"""
def threshold(image):
  
  height, width = image.shape[0], image.shape[1]
  new_image = np.zeros((height, width), dtype= np.uint8)
  # Now that preprocessing is done, use a intensity threshold of 185 and only select those pixels to add to new image
  for y in range(height):
    for x in range (width):
      current_pixel_value = image[y][x]
      if current_pixel_value >= 185:
        new_image[y][x] = current_pixel_value
      else:
        new_image[y][x] = 0

  return new_image

"""
Adds a 5-pixel black padding to a given image
"""
def pad(image):

  top = bottom = left = right = 5 
  borderType = cv2.BORDER_CONSTANT
  value = (0,0,0)
  height, width = image.shape[0], image.shape[1]
  new_image = np.zeros((height, width), dtype=np.uint8)
  padImage = cv2.copyMakeBorder(image, top, bottom, left, right, borderType, value)
  
  return padImage

"""
Runs the in-built median blur function on a given image
"""
def smooth(image):

  blurred_image = cv2.medianBlur(image,45)  
  
  return blurred_image

"""
Removes a 5-pixel padding from the borders of an image, returns a new image
"""
def removepadding(image):

  height, width = image.shape
  top = 5
  bottom = height - 5
  left = 5
  right = width - 5
  cropped_image = image [top:bottom, left:right]

  return cropped_image

"""
Given two images, makes the first image the same size as the second
"""
def crop_function(image1, image2):

  height, width = image2.shape
  # Simply use indexing to crop the image
  cropped_image = image1 [0:height, 0:width]
  
  return cropped_image

"""
Runs a pixel-wise and operation between two given images
"""
def and_op(image1, image2):

  new_image = np.zeros((image1.shape[0], image1.shape[1]), dtype = np.uint8)
  for y in range(image1.shape[0]):
    for x in range(image1.shape[1]):
      if image1 [y][x] and image2 [y][x]:
        new_image [y][x] =  image1 [y][x]
      else:
        new_image [y][x] = 0  
  
  return new_image

"""
Returns the negative of an image by flipping dark and light
"""
def negative(image1):

  # Simply subtract the pixel intensity from 255 to flip
  negative = 255 - image1
  
  return negative

"""
Uses the in-built add operation to add two given images
"""
def add(image1, image2):

  return cv2.add(image1, image2)

"""
Uses the midpoint algorithm provided in class to draw a circle 
at a given center and a given radius
"""
def draw_circle(image, center, radius):

  with_circle = image
  x, y = 0, radius
  d = 5/4 - radius
  x0, y0 = center[:2]

  while y >= x:
      # Draw points in all octants around the center
      with_circle[x0 + x, y0 + y] = 80
      with_circle[x0 + x, y0 - y] = 80
      with_circle[x0 - x, y0 + y] = 80
      with_circle[x0 - x, y0 - y] = 80
      with_circle[x0 + y, y0 + x] = 80
      with_circle[x0 + y, y0 - x] = 80
      with_circle[x0 - y, y0 + x] = 80
      with_circle[x0 - y, y0 - x] = 80

      if d < 0:
          d += 2 * x + 3
          x += 1
      else:
          d += 2 * (x - y) + 5
          x += 1
          y -= 1

  return with_circle
    
"""
Function that performs flood fill detection
"""
def flood_fill(image, seed, fill_intensity):
    #Add seed to stack
    stack = [seed]
    #Extract image dimensions
    width, height = image.shape[1], image.shape[0]
    #Set the boundary color from the object that has been drawn already
    boundary_color = 80 
    #Run loop while there is an exist element in the stack
    while stack:
        #Extract the x and y coordinate of pixel
        u, v = stack.pop()

        # Condition that checks if the current pixel is inside the image
        if u < 0 or u >= width or v < 0 or v >= height:
            continue  
        #Condition that checks if the pixel has already been filled or is a boundary pixel of the drawn object
        if image[v, u] == fill_intensity or image[v, u] == boundary_color:
            continue

        # Fill the pixel with the required color
        image[v, u] = fill_intensity

        # Check four neighboring pixels
        neighbors = [(u - 1, v), (u + 1, v), (u, v - 1), (u, v + 1)]
        for neighbor in neighbors:
            #Current pixel coordinate for the specific iteration
            x, y = neighbor
            #Add neighbor to stack
            stack.append((x, y))

    return image


def main():

  # First, load two images into variables
  image = cv2.imread("photo1.jpg", cv2.IMREAD_GRAYSCALE)
  image2 = cv2.imread("photo2.jpg", cv2.IMREAD_GRAYSCALE)

  # Run a thresholding on the first image and (median) blur the result after padding. Remove padding after blurring.
  threshold_img = threshold(image)
  pad_image = pad(threshold_img)
  blurred_image = smooth(pad_image)
  blurred_image_no_pad = removepadding(blurred_image)

  # Crop the second image to the size of the first
  cropped_image2 = crop_function(image2, image)

  # Use the thresholded mask to obtain the inverse mask, the foreground of the image, and the pixelwise "and" between the two
  foreground = and_op(image, blurred_image_no_pad)
  negative_mask = negative(blurred_image_no_pad)
  inverse_masked = and_op(cropped_image2, negative_mask)

  # Obtain the overlaid image by adding the first image foreground to the space identified by the inverse mask
  final = add(inverse_masked, foreground)

  # Draw a circle in the resultant image of radius 50 
  final_with_circle = draw_circle(final, (80, 80), 50)

  # Use the pixel center as the seed pixel and use the flood fill algorithm to fill the circle with dark gray
  seed_pixel= (80,80)
  final_with_circle_two = flood_fill(final_with_circle, seed_pixel, 30)

  # Save the final final final image
  cv2.imwrite("final_image.jpg", final_with_circle_two)

if __name__ == "__main__":
  main()
