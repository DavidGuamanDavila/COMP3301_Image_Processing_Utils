import cv2
import numpy as np
import matplotlib.pyplot as plt

def add_img_padding(image):
    # Define the border size (1 pixel)
    border_size = 1

    # Define the border color (black in BGR format)
    border_color = (0, 0, 0)

    # Add a 1-pixel black border to the image
    padded_image = cv2.copyMakeBorder(image, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT, value=border_color)

    return padded_image

def filter_img(padded_grayscale_image, grayscale_image):
    # Get the dimensions of the grayscale image
    height, width = grayscale_image.shape

    # Create an empty matrix to store the output image with the same dimensions
    output_image = np.zeros((height, width), dtype=np.uint8)

    # Define the 3x3 filter matrix with all ones
    filter_matrix = np.array([[1/9, 1/9, 1/9],
                             [1/9, 1/9, 1/9],
                             [1/9, 1/9, 1/9]])

    # Iterate through the padded image, leaving a 1-pixel border
    for y in range(1, height + 1):
        for x in range(1, width + 1):
            # Extract the 3x3 neighborhood from the padded image
            neighborhood = padded_grayscale_image[y - 1:y + 2, x - 1:x + 2]

            # Perform convolution by element-wise multiplication and summation
            filtered_value = np.sum(neighborhood * filter_matrix)

            # Assign the filtered value to the corresponding pixel in the output image
            output_image[y - 1, x - 1] = filtered_value

    return output_image

#Function that Creates the Souliton Image
def create_alternating_rows_image(height, width):
    # Create an empty image with the specified width and height passed from the parameters
    image = np.zeros((height, width), dtype=np.uint8)

    # Loop through rows and set odd rows to black (0 intensity) and even rows to white (255 intensity)
    for row in range(height):
        if row % 2 == 0:
            image[row, :] = 255  # Set even rows to white
        else:
            image[row, :] = 0    # Set odd rows to black

    return image

def main():
    #Load Checker Image
    image = cv2.imread("Checker.jpg", cv2.IMREAD_GRAYSCALE)
    #Load Rotated Image
    rotated_image = cv2.imread("Checker_Rotated.jpg", cv2.IMREAD_GRAYSCALE)
    #Load Soultion Image
    solution_new_image = create_alternating_rows_image(image.shape[0],image.shape[1])

    #Show Image
    cv2.imshow("Solution Image", solution_new_image)
    cv2.waitKey(4000)
    cv2.destroyAllWindows()
    
    #Save Solution Image as a file
    output_file_name = 'Solution_img.jpg'
    cv2.imwrite(output_file_name, solution_new_image)

    #Original Image Padding & Filtering
    padded_image = add_img_padding(image)
    filtered_image = filter_img(padded_image,image)

    #Save Solution Image as a file
    output_file_name_one = 'Checker_Filtered_img.jpg'
    cv2.imwrite(output_file_name_one, filtered_image)

    #Solution image Padding & Filtering
    padded_new_image = add_img_padding(solution_new_image)
    filtered_new_image = filter_img(padded_new_image, solution_new_image)

    #Save Solution Image as a file
    output_file_name_two = 'Solution_Filtered_img.jpg'
    cv2.imwrite(output_file_name_two, filtered_new_image)

    #Rotated Image Padding & Filtering
    padded_rotated_image = add_img_padding(rotated_image)
    filtered_rotate_image = filter_img(padded_rotated_image,rotated_image)
    
    #Checker Prior to Filter Histogram
    plt.hist(image.ravel(), 256, [0, 256])
    plt.title("Checker Histogram Prior to Filter")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.show()

    #Solution New Image Histogram Prior to Filter
    plt.hist(solution_new_image.ravel(), 256, [0, 256])
    plt.title("Solution New Image Histogram Prior to Filter")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.show()

    #Rotate Image Prior to Filter
    plt.hist(rotated_image.ravel(), 256, [0, 256])
    plt.title("Rotate Image Prior to Filter Histogram")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.show()

    #Checker Filtered Histogram
    plt.hist(filtered_image.ravel(), 256, [0, 256])
    plt.title("Checker Filtered Histogram")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.show()

    #New Solution Image Filter Histogram
    plt.hist(filtered_new_image.ravel(), 256, [0, 256])
    plt.title("Solution Filter Image Histogram")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.show()

    #Filter Rotated Histogram
    plt.hist(filtered_rotate_image.ravel(), 256, [0, 256])
    plt.title("Checker Rotated Filter Histogram")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.show()
          
if __name__ == "__main__":
    main()
