import os
import cv2
import numpy as np
from collections import deque
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
Accepts a range of intensity values that will be considered when searching for a suitable path. 
Verifies that this range is valid, i.e., 0 <= lower intensity <= maximum intensity <= 255
Will only exit if a valid intensity range is parsed from the user.
'''
def intensity_validity():

    upper_intensity_bound_check = False

    while not upper_intensity_bound_check:
        try:
            upper_intensity = int(input("Please enter a numeric intensity between 0 < max intensity <= 255:"))

            if 0 < upper_intensity <= 255:
                upper_intensity_bound_check= True

            else:
                print("Incorrect input. Please, try again. Remember the max intensity must be between 0 < intensity max <= 255.")

        except ValueError:
            print("Incorrect input. Please, try again. Remember the intensity is a numeric value i.e. integer.")

    print(f"Valid max intensity: {upper_intensity} !")

    lower_intensity_bound_check = False

    while not lower_intensity_bound_check:
        try:
            lower_intensity = int(input("Please enter a numeric minimum intensity between 0 <= minimum intensity <= max intensity:"))
            print(f"The max intensity previously inputted is: {upper_intensity}")
            if 0 <= lower_intensity <= upper_intensity:
                lower_intensity_bound_check= True

            else:
                print("Incorrect input. Please, try again. Remember the intensity must be between 0 <= minimum intensity <= max intensity.")

        except ValueError:
            print("Incorrect input. Please, try again. Remember the intensity is a numeric value i.e. integer.")

    print(f"Valid max intensity: {lower_intensity} !")
    
    return upper_intensity, lower_intensity

'''
Initializes the set V that contains all intensity values that a pixel in the 4- or 8-path
can contain for the path to use that pixel.
Returns this set V. 
'''
def intensities_set_creation(upper_intensity, lower_intensity):
    V = set()
    for i in range(lower_intensity, upper_intensity):
        V.add(i)
    return V

'''
Asks and returns whether the user wants to search for a 4-neighbour or 8-neighbour adjacency path.
'''
def path_option_selection():
    path_selection_check = False
    while not path_selection_check:
        try:
            path = int(input("Please enter a numeric path either 4 for 4-path or 8 for 8-path:"))
            if path == 4 or path == 8:
                path_selection_check= True

            else:
                print("Incorrect input. Please, try again. Remember the path either is 4 for 4-path or 8 for 8-path:.")

        except ValueError:
            print("Incorrect input. Please, try again. Remember the intensity is a numeric value i.e. integer.")

    print(f"You have selected: {path} - path!")
    return path

'''
Accepts a valid x and y co-ordinate of the starting point of the path.
'''
def p_coordinate_input_verification(img_height, img_width):
    px = False
    while (not px):
        p_x_coordinate = input("Enter an x co-ordinate for p(starting pixel): ")
        try:
            p_x_coordinate = int(p_x_coordinate)
            if (p_x_coordinate < img_width) and (p_x_coordinate >= 0):
                px = True
            else:
                print("The entered co-ordinate was out of bounds or negative")
        except ValueError:
            print("Please input an integer")

    py = False
    while (not py):
        p_y_coordinate = input("Enter a y co-ordinate for p(starting pixel): ")
        try:
            p_y_coordinate = int(p_y_coordinate)
            if (p_y_coordinate < img_height) and (p_y_coordinate >= 0):
                py = True
            else:
                print("The entered co-ordinate was out of bounds or negative")
        except ValueError:
            print("Please input an integer")

    return p_x_coordinate, p_y_coordinate

'''
Accepts a valid x and y co-ordinate of the ending point of the path.
'''
def q_coordinate_input_verification(img_height, img_width):
    qx = False
    while (not qx):
        q_x_coordinate = input("Enter an x co-ordinate for q(ending pixel): ")
        try:
            q_x_coordinate = int(q_x_coordinate)
            if (q_x_coordinate < img_width) and (q_x_coordinate >= 0):
                qx = True
            else:
                print("The entered co-ordinate was out of bounds or negative")
        except ValueError:
            print("Please input an integer")

    qy = False
    while (not qy):
        q_y_coordinate = input("Enter a y co-ordinate for q(ending pixel): ")
        try:
            q_y_coordinate = int(q_y_coordinate)
            if (q_y_coordinate < img_height) and (q_y_coordinate >= 0):
                qy = True
            else:
                print("The entered co-ordinate was out of bounds or negative")
        except ValueError:
            print("Please input an integer")
    return q_x_coordinate, q_y_coordinate


'''
Pre-processes the image. Stores a list of co-ordinates where there exists a pixel 
with an intensity value contained in set V. Sets up a two-dimensional numpy binary array
that contains a zero at co-ordinates where there is a pixel with intensity value outside of 
set V, and a one at co-ordinates where the pixel intensity value is within V.   
'''
def img_preprocessing(image, V, img_height, img_width):
    x_position = 0
    y_position = 0

    #List that stores values of x and y that have intensities of set V
    xy_list = []

    #Matrix that will store the intensities of the image depending if its on set V
    matrix_intensities_set_v = np.zeros(shape=(img_height, img_width)) 

    while (img_height > y_position):
        while (img_width > x_position):

            current_pixel_intensity = int(image[y_position,x_position])

            #Check if current pixel is in set V and put a 1. Otherwise set it to 0
            if (current_pixel_intensity not in V):
                matrix_intensities_set_v[y_position][x_position] = 0
            else:
                xy_list.append([x_position,y_position])
                matrix_intensities_set_v[y_position][x_position] = 1

            x_position = x_position + 1

        x_position = 0
        y_position = y_position + 1
    np.savetxt("foo.csv", matrix_intensities_set_v, delimiter=",")
    return xy_list, matrix_intensities_set_v

'''
Checks if the start and end locations are the same pixel,
return True if they are and that pixel is contained in set V, and false otherwise.
Used later to capture this edge case during the path search.
'''
def pixel_valid(matrix, xstart, ystart, xend, yend):
    if matrix[ystart][xstart] == 1 and xstart == xend and ystart == yend:
        return True
    else:
        return False

'''
A breadth-first search algorithm. Returns the length of the shortest 4- or 8-neighbour path
between two given points. If the path cannot be found, then returns -1. 
'''   
def shortest_path_calculation_BFS(path, px, py, qx, qy, img_height, img_width, matrix_intensities_set_v):

    #Store 4-path adjacency co-ordinate transforms
    if path == 4:
        adj_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    #Store 8-path adjacency co-ordinate transforms
    if path == 8:
        adj_directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    
    p = px, py
    q = qx, qy

    queue = deque([(p,0)])
    visited_pts = set()
    path_distance = -1
    while queue:
        current_pt , distance = queue.popleft()
        x , y = current_pt

        if current_pt == q:
            path_distance = distance
            break

        for x_i, y_i in adj_directions:

            neighboor_coordinate_x, neighboor_coordinate_y = x + x_i, y + y_i

            if (0 <= neighboor_coordinate_y < img_height and 0 <= neighboor_coordinate_x < img_width):
                if (matrix_intensities_set_v[neighboor_coordinate_y][neighboor_coordinate_x] == 1 and (neighboor_coordinate_x, neighboor_coordinate_y) not in visited_pts):
                            
                    queue.append(((neighboor_coordinate_x, neighboor_coordinate_y), distance + 1))
                    visited_pts.add((neighboor_coordinate_x, neighboor_coordinate_y))

    return path_distance


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
        upper_intensity, lower_intensity = intensity_validity()
        intensities_set_v = intensities_set_creation(upper_intensity, lower_intensity)
        path_selection = path_option_selection()
        px, py = p_coordinate_input_verification(img_height, img_width)
        qx, qy = q_coordinate_input_verification(img_height, img_width)
        xy_list, matrix_intensities_set_v = img_preprocessing(grayscale_image, intensities_set_v, img_height, img_width)
        path_distance = -1
        
        # If the path exists, then use the breadth-first search function to find the length of the shortest path between the two points
        if pixel_valid(matrix_intensities_set_v, px, py, qx, qy):
            path_distance = shortest_path_calculation_BFS(path_selection, px, py, qx, qy, img_height, img_width, matrix_intensities_set_v)
        
        # Display the caluclated result appropriately
        if path_distance != -1:
            if path_selection == 4:
                print(f"The length of the shortest 4-neighbour adjacency path from p to q is {path_distance}")
            if path_selection == 8:
                print(f"The length of the shortest 8-neighbour adjacency path from p to q is {path_distance}")
        else:
            if path_selection == 4:
                print("No 4-neighbour adjacency path from p to q was found.")
            if path_selection == 8:
                print("No 8-neighbour adjacency path from p to q was found.")
            

if __name__ == "__main__":
    main()



