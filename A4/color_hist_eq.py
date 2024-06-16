import os
import cv2
import math
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
Finds the hue values based on a given rgb image's path. Find the Hue in degrees.
'''
def hue_calculation(image):
    if image is not None:
        # Get the dimensions of the image
        height, width = image.shape[:2]

        # Create an empty hue matrix
        hue_image = np.zeros((height, width), dtype=np.float32)

        # Iterate through each pixel in the image
        for i in range(height):
            for j in range(width):
                # Calculate numerator and denominator for hue
                B, G, R = image[i, j]
                epsilon = 0.00001
                
                numerator = 0.5 * ((R - G) + (R - B))
                denominator = max(epsilon, math.sqrt(math.pow((R - G), 2) + ((R - B) * (G - B))) + epsilon)

                # Calculate hue using the given formula from the slides
                theta = math.degrees(math.acos(max(-1, min(1, numerator / denominator))))

                #Store hue image value in new image
                if B > G:
                    hue_image[i, j] = (360 - theta)

                else:
                    hue_image[i, j] = theta

    return hue_image

'''
Function that calculates the saturation of the colour image
'''
def saturation_calculation(image):
    try:
        if image is not None:
            # Get the dimensions of the image
            height, width = image.shape[:2]

            # Create an empty saturation matrix
            saturation_image = np.zeros((height, width), dtype=np.float32)

            # Iterate through each pixel in the image
            for i in range(height):
                for j in range(width):
                    # Extract the RGB values
                    B, G, R = image[i, j]
                    # Calculate saturation using the formula
                    numerator = 3 * min(R, G, B)
                    denominator = R + G + B + 0.0001  # Added small number to avoid division by 0
                    saturation = 1 - (numerator / denominator)

                    # Store the saturation value in the new image
                    saturation_image[i, j] = saturation

            return saturation_image

        else:
            print("\nSorry, the image could not be loaded\n")
            return None

    except Exception as e:
        print("\nError encountered while processing the image: " + str(e) + '\n')
        return None

'''
Calculates the intensity matrix 
'''
def intensity_calculation(image):
    try:
        if image is not None:

            # Get the dimensions of the image
            height, width = image.shape[:2]

            # Create an empty intensity matrix
            intensity_image = np.zeros((height, width), dtype=np.uint8)

            # Iterate through each pixel in the image
            for i in range(height):
                for j in range(width):           
                    B, G, R = image[i, j]

                    # Calculate intensity using the formula: Intensity = (Red + Green + Blue) / 3
                    intensity = np.sum(image[i, j]) / 3
                    intensity_image[i, j] = intensity

            return intensity_image

        else:
            print("\nSorry, the image could not be loaded\n")
            return None

    except Exception as e:
            print("\nError encountered while opening image using OpenCV:  "+ str(e)+'\n')
            return None


'''
Function that converts back from HSI -> RGB
'''
def hsi_conversion_rgb(hue_img, saturation_img, intensity_img):

    height, width = hue_img.shape[:2]

    # Create an empty saturation matrix
    rgb_img = np.zeros((height, width, 3), dtype=np.float32)

    for i in range(height):
        for j in range(width):
            H = hue_img[i, j]           #Extract Hue
            S = saturation_img[i, j]    #Extract Saturation
            I = intensity_img[i, j]     #Exctract Intensity

            #Address situation where hue is between 0 <= H and H < 120
            if 0 <= H and H < 120:
                B = I * (1 - S)
                R = I * (1 + ((S * math.cos(math.radians(H)))/(math.cos(math.radians(60 - H))))) 
                G = 3*I - (R + B)

            #Address situation where hue is between 120 <= H and H < 240
            elif 120 <= H and H < 240:
                R = I * (1 - S)
                G = I * (1 + ((S * math.cos(math.radians(H - 120)))/(math.cos(math.radians(180 - H))))) 
                B = 3*I - (R + G)

            #Address situation where hue is between 240 <= H and H < 360
            elif 240 <= H and H < 360:
                G = I * (1 - S)
                B = I * (1 + ((S * math.cos(math.radians(H - 240)))/(math.cos(math.radians(300 - H))))) 
                R = 3*I - (G + B)

            #Store calculated values into new image
            rgb_img[i, j, 0] = np.clip(B, 0, 1)
            rgb_img[i, j, 1] = np.clip(G, 0, 1)
            rgb_img[i, j, 2] = np.clip(R, 0, 1)

    return rgb_img
 
'''
Function that makes the color per pixel in an image from [0,255] to [0,1]
'''
def pixel_normalize_image(image):
    try:
        height, width = image.shape[:2]
        normalized_image = np.zeros((height, width), dtype= np.float32)
        if image is not None:
            for i in range(height):
                for j in range(width):

                    # Normalize the image to the range [0, 1]
                    normalized_image[i, j] = (image[i, j] / 255.0).astype('float32')

            return normalized_image

        else:
            print("\nSorry, the image could not be loaded\n")
            return None

    except Exception as e:
        print("\nError encountered while opening image using OpenCV: " + str(e) + '\n')
        return None

'''
Function that scales an image from [0,1] -> [0,255]
'''
def scale_image(image):
    try:
        if image is not None:

            # Scale the normalized image to the range [0, 255]
            scaled_image = (image * 255).astype('uint8')
            return scaled_image

        else:
            print("\nSorry, the image could not be loaded\n")
            return None

    except Exception as e:
        print("\nError encountered while opening image using OpenCV: " + str(e) + '\n')
        return None   

'''
Function that scales an image RGB three values from [0,1] -> [0,255]
'''
def normalize(image):
    try:
        if image is not None:

            # Normalize the image to the range [0, 1]
            normalized_image = (image /(255.0)).astype('float32')
            return normalized_image

        else:
            print("\nSorry, the image could not be loaded\n")
            return None

    except Exception as e:
        print("\nError encountered while opening image using OpenCV: " + str(e) + '\n')
        return None


def main():
    # Accept path to image
    image_path_user = user_img_input()

    # Verify that the path entered by the user is a valid one
    valid_path = path_validity(image_path_user)

    # If the image is valid and openable, then sets up params and computes shortest path distance
    if (valid_path is not None):

        #Read image from path
        image = cv2.imread(image_path_user)
        
        #Convert image to float
        image_float = np.float32(image)

        #Intensity Image in [0,255]
        intensity_image = intensity_calculation(image_float)

        #Normalize the histogram to get the PDF in [0,255]
        pdf = normalize_histogram(intensity_image)
        
        # Perform histogram equalization using the PDF in [0,255]
        intensity_histogram_equalized_image = histogram_equalization(intensity_image, pdf)

        #Normalize the intensity_histogram_equalized_image from [0,255] to [0,1] to be used for HSI -> RGB conversion
        normalized_intensity_histogram_equalized_image = pixel_normalize_image(intensity_histogram_equalized_image)
    
        #Normalize original RGB from [0,255] -> [0,1]
        normalized_rgb = normalize(image_float)
       
        # Calculate the hue of the image from RGB -> Hue
        hue_image = hue_calculation(normalized_rgb)

        #Calculate saturation of the color image from RGB -> Saturation
        saturation_image = saturation_calculation(normalized_rgb)
 
        #Calculate the RGB normalized in [0,1] using HSI -> RGB equations provided in class
        rgb_normalized_image = hsi_conversion_rgb(hue_image, saturation_image, normalized_intensity_histogram_equalized_image)

        #Calculate the RGB normalized in [0,255]
        rgb_scaled_image = scale_image(rgb_normalized_image)
        
        #Display Resulting Image
        cv2.imshow("RGB Histogram Equalized Resultant Image", rgb_scaled_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        #Define path of resultant image
        output_file_path = "RGB_Histogram_Equalized_Resultant_Image.jpg"

        # Save the image
        cv2.imwrite(output_file_path, rgb_scaled_image)

        #Display Original Image
        cv2.imshow("RGB Original Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
