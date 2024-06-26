import os
import cv2
import numpy as np

'''
Accepts a string input of the user's image path file 
and parses the '~' from the path to the user's root directory
'''
def user_img_input():

    path = input("Hello! Please enter the path to your image file:  ")
    img_path = os.path.expanduser(path)
    return img_path

'''
Verifies that a file exists at the path that has been parsed from the user input
'''
def path_validity(img_path):

    if os.path.isfile(img_path):
        print("\nFile path found at: " + str(img_path))
        return img_path
    else:
        print("File path not found. Path was: " + str(img_path))
        return None


'''
If the image exists, uses OpenCV's grayscale mode to display the image
and waits one second before closing it. Returns the image height and width.
If image does not exist, returns none.
RaisesException: Depending on error in opening image
'''
def img_grayscale_conversion(img_path):
    try:
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        if image is not None:
            cv2.imshow("Grayscale Image", image)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            img_height = image.shape[0]
            img_width = image.shape[1]
            return image, img_height, img_width

        else:
            print("\nSorry, the image could not be loaded\n")
            return None

    except Exception as e:
            print("\nError encountered while opening image using OpenCV:  "+ str(e)+'\n')
            return None


'''
Adds a 1pixel-deep black padding around the entire image using OpenCV.
'''
def add_img_padding(image):
    # Define the border size (1 pixel)
    border_size = 1

    # Define the border color (black in BGR format)
    border_color = (0, 0, 0)

    # Add a 1-pixel black border to the image
    padded_image = cv2.copyMakeBorder(image, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT, value=border_color)

    return padded_image


'''
Filters an image using a 3x3 averaging mask in the 8-neighbourhood of each pixel.
'''
def filter_img(padded_grayscale_image, grayscale_image):
    # Get the dimensions of the grayscale image
    height, width = grayscale_image.shape

    # Create an empty matrix to store the output image with the same dimensions
    output_image = np.zeros((height, width), dtype=np.uint8)

    # Define the 3x3 filter matrix with all ones
    filter_matrix = np.array([[1/9, 1/9, 1/9],
                             [1/9, 1/9, 1/9],
                             [1/9, 1/9, 1/9]])

    # Iterate through the padded image, leaving a 1-pixel border. This will remove the padding added previously to image
    for y in range(1, height + 1):
        for x in range(1, width + 1):
            # Extract the 3x3 neighborhood from the padded image
            neighborhood = padded_grayscale_image[y - 1:y + 2, x - 1:x + 2]

            # Perform convolution by element-wise multiplication and summation
            filtered_value = np.sum(neighborhood * filter_matrix)

            if filtered_value > 255:
                filtered_value = 255
            elif filtered_value < 0:
                filtered_value = 0

            # Assign the filtered value to the corresponding pixel in the output image
            output_image[y - 1, x - 1] = filtered_value

    return output_image

'''
Function that generates the mask image by substracting the original grayscale image - the blur image
'''
def mask_creation(original_img, blur_img):
    mask_img = np.zeros((original_img.shape[0],original_img.shape[1]),dtype=np.uint8)
    for y in range(original_img.shape[0]):
        for x in range(original_img.shape[1]):
            # Calculate the difference
            diff = original_img[y, x].astype(int) - blur_img[y, x].astype(int)
            # Clip the result to the range [0, 255]
            mask_img[y, x] = np.clip(diff, 0, 255).astype(np.uint8)    
    return mask_img


'''
Function that adds the original grayscale image to the mask image
'''
def sharpen_img(original_img, mask_img):
    sharpened_img = np.zeros((original_img.shape[0],original_img.shape[1]),dtype=np.uint8)
    for y in range(original_img.shape[0]):
        for x in range(original_img.shape[1]):
            # Calculate the sum
            summ = original_img[y, x].astype(int) + mask_img[y, x].astype(int)
            # Clip the result to the range [0, 255]
            sharpened_img[y, x] = np.clip(summ, 0, 255).astype(np.uint8)

    return sharpened_img


'''
Displays a side-by-side stack of two images passed to it using OpenCV.
'''
def display_images(image_1, image_2):
    cv2.namedWindow("Original vs Sharpened", cv2.WINDOW_NORMAL)
    stacked_image = np.hstack((image_1, image_2))

    cv2.imshow("Original vs Sharpened", stacked_image)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()


'''
Accepts a path from the user and opens the image at that path in
grayscale mode. Performs the filtering using a 3x3 averaging mask
and a padded version of the original image. Displays both the original
and the Sharpened image and saves the Sharpened image. 
'''
def main():
    # Accept path to image
    image_path_user = user_img_input()

    # Verify that the path entered by the user is a valid one
    valid_path = path_validity(image_path_user)

    # Tries to open the image at the path in the OpenCV grayscale mode
    image_integrity_results = img_grayscale_conversion(image_path_user)
    
    # If the image is valid and openable, then sets up params and computes shortest path distance
    if (valid_path is not None and image_integrity_results):
        grayscale_image, img_height, img_width = image_integrity_results
        padded_grayscale_image = add_img_padding(grayscale_image)
        blurry_img = filter_img(padded_grayscale_image, grayscale_image)
        mask_img = mask_creation(grayscale_image,blurry_img)
        resultant_img = sharpen_img(grayscale_image, mask_img)

        output_file_name = 'sharpened_result__img.jpg'
        cv2.imwrite(output_file_name, resultant_img)
        print(f"Sharpened image saved as file name: {output_file_name}")

        display_images(grayscale_image, resultant_img)


            
if __name__ == "__main__":
    main()
