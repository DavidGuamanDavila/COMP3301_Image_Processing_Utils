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
Calculates the histogram of an image that is passed to it by polling and recording all
occurrences of each intensity value into a numpy zeroes array.
'''
def calculate_histogram(image):
    histogram = np.zeros(256, dtype=int)
    for row in image:
        for pixel in row:
            histogram[pixel] += 1
    return histogram


'''
Normalizes the histogram by dividing the number of occurrences of an intensity value 
by the total number of pixels in the image.
'''
def normalize_histogram(image):
    histogram = calculate_histogram(image)
    pdf = histogram / float(image.size)
    return pdf


'''
Find the CDF from the PDF and normalize it. Returns the equalized 8-bit integer format of
the normalized CDF value.
'''
def histogram_equalization(image, pdf):
    # Calculate the cumulative distribution function (CDF) using the PDF
    cdf = np.cumsum(pdf)

    # Multiply the cdf by L-1 = 255
    cdf = cdf * 255
    
    # Use the CDF values to map the pixel values in the image
    equalized_image = cdf[image]

    # Convert to 8-bit unsigned integer
    equalized_image = equalized_image.astype(np.uint8)

    return equalized_image


'''
Displays a side-by-side stack of two images passed to it using numpy and OpenCV.
'''
def display_images(image_1, image_2):
    cv2.namedWindow("Original vs Equalized", cv2.WINDOW_NORMAL)
    stacked_image = np.hstack((image_1, image_2))

    cv2.imshow("Original vs Equalized", stacked_image)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()


'''
Accepts an image path from the user and opens the image at that path
in grayscale. Normalizes, equalizes, and displays the original and modified images.
Saves the equalized image to your machine. 
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

        # Normalize the histogram to get the PDF
        pdf = normalize_histogram(grayscale_image)
        
        # Perform histogram equalization using the PDF
        equalized_image = histogram_equalization(grayscale_image, pdf)

        # Save the equalized image
        output_file_name = "result_equalized_image.png"  # You can change the output filename as needed
        cv2.imwrite(output_file_name, equalized_image)
        print(f"Equalized image saved as file name: {output_file_name}")

        # Display the original and equalized images side by side
        display_images(grayscale_image, equalized_image)
        

          
if __name__ == "__main__":
    main()
