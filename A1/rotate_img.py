import os
import cv2
import math
import numpy as np

def user_img_input():

    ''' Accepts the user's path to the image file being rotated.
        Returns image path after resolving ~ to user directory  '''
    
    # Accept user path
    path = input("Hello! Please enter the path to your image file:  ")
    img_path = os.path.expanduser(path)
    return img_path

def path_validity(img_path):
    ''' Takes the parsed image path and verifies that a file exists
        at that location                                            '''
    
    if os.path.isfile(img_path):
        print("File path found at: " + str(img_path))
        return img_path
    else:
        print("File path not found. Path was: " + str(img_path))
        return None

def img_grayscale_conversion(img_path):
    ''' Opens the image at the path in OpenCV's grayscale mode and displays it.
        RaisesException: if the image cannot be opened correctly               '''
    
    try:
        # Use OpenCV's grayscale mode to open the image
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        if image is not None:
            # If image found, display it
            cv2.imshow("Grayscale Image", image)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            return image

        else:
            print("Sorry, the image could not be loaded")
            return None

    except Exception as e:
            print("Error encountered while opening image using OpenCV:  "+ str(e))
            return None

def check_angle_input():
    ''' Asks for angle of rotation from the user until it is valid (an integer between 0 and 360)'''

    check_angle_input = False

    while not check_angle_input:
        try:
            rotation_angle = int(input("Please enter an angle in degrees ranging between 0 <= angle <= 360:"))
            
            # Check if valid angle
            if 0 <= rotation_angle <= 360:
                check_angle_input= True

            else:
                print("Incorrect input. Please, try again. Remember that the angle must be between 0 and 360 degrees.")

        except ValueError:
            print("Incorrect input. Please, try again. Remember that the angle is a numeric value i.e. integer.")

    print(f"Valid angle: {rotation_angle} degrees!")
    return rotation_angle

def check_direction_rotation():
    ''' Accepts the direction of rotation from user. 1 = counterclockwise, 2 = clockwise '''

    direction_rotation_check = False

    while not direction_rotation_check:
        try:
            direction_selection = int(input("Please enter a numeric value. Enter 1 for counterclockwise and 2 for clockwise:"))
            if direction_selection == 1 or direction_selection == 2:
                direction_rotation_check= True
            else:
                print("Incorrect input. Please, try again. Remember enter 1 for counterclockwise and 2 for clockwise.")
        except ValueError:
            print("Incorrect input. Please, try again. Remember enter 1 for counterclockwise and 2 for clockwise:.")
    if direction_selection == 1:
        print(f"You have selected: counterclockwise - direction!")
    else:
        print(f"You have selected: clockwise - direction!")
    return direction_selection

def new_image_dimensions(img_height, img_width, rotation_angle_degrees):
    ''' Accepts the original image dimensions and rotation angle. Finds and returns new image dimensions
        by calculating new minimum and maximum x and y coordinates.                                      '''


    angle_radians = math.radians(rotation_angle_degrees)
    #Four edges of the image
    img_edges = [(0,0), (img_width,0), (0,img_height), (img_width, img_height)]

    min_x_coordinate = math.inf
    max_x_coordinate = -math.inf
    min_y_coordinate = math.inf
    max_y_coordinate = -math.inf

    for x, y in img_edges:

        new_x_coordinate = x * math.cos(angle_radians) - y * math.sin(angle_radians)
        new_y_coordinate = x * math.sin(angle_radians) + y * math.cos(angle_radians)
        min_x_coordinate = min(min_x_coordinate, new_x_coordinate)
        max_x_coordinate = max(max_x_coordinate, new_x_coordinate)
        min_y_coordinate = min(min_y_coordinate, new_y_coordinate)
        max_y_coordinate = max(max_y_coordinate, new_y_coordinate)

    new_img_width = int(max_x_coordinate - min_x_coordinate)+1
    new_img_height = int(max_y_coordinate - min_y_coordinate)+1
    
    return new_img_width, new_img_height

def interpolate(intensity00, intensity01, intensity10, intensity11, col_weight00, col_weight01, col_weight10, col_weight11):
    ''' Accepts 4-neighbours' intensity values and their  column weights. Interpolates and returns top and bottom pixel intensities '''

    # Calculate PointA and PointB using col weights and intensities
    PointA = (col_weight00 * intensity00) + (col_weight01 * intensity01)
    PointB = (col_weight10 * intensity10) + (col_weight11 * intensity11)
    
    return PointA, PointB

def bilinear_interpolation(PointA, PointB, row_weight_top, row_weight_bottom):
    ''' Accepts interpolated top and bottom intensities and their row weights. Interpolates and returns final intensity value'''
    
    # Calculate the final intensity using row weights
    return PointA * row_weight_top + PointB * row_weight_bottom

def new_image_creation(image, rotation_angle_degrees, rotation_direction):
    ''' Accepts image object and rotation parameters.  Rotates image using inverse mapping and bilinear interpolation
        and also translates it to the center if necessary.                                                             '''

    # Find the original image height and width
    img_height = image.shape[0]
    img_width = image.shape[1]
    
    # Find old image center
    old_center_x = img_width / 2
    old_center_y = img_height / 2

    # Now calculate the new image width and height
    new_img_width, new_img_height = new_image_dimensions(img_height-1, img_width-1, rotation_angle_degrees)
    if rotation_direction == 2:
        rotation_angle_degrees = 0 - rotation_angle_degrees
    rotation_angle_radians = math.radians(rotation_angle_degrees)
    
    # Empty three-channel numpy array of the size of new image
    new_image_matrix = np.zeros((new_img_height, new_img_width, 3), dtype = np.uint8)

    # Calculate the coordinates of the center of the original image
    center_x = new_img_width / 2
    center_y = new_img_height / 2

    translation_x = old_center_x - center_x
    translation_y = old_center_y - center_y

    for y_out in range(new_img_height):
        for x_out in range(new_img_width):

            # Calculate the rotated coordinates in the original image
            x_in_float = (x_out - center_x) * math.cos(rotation_angle_radians) - (y_out - center_y) * math.sin(rotation_angle_radians) + center_x
            y_in_float = (x_out - center_x) * math.sin(rotation_angle_radians) + (y_out - center_y) * math.cos(rotation_angle_radians) + center_y
            
            if rotation_angle_degrees != 180 or rotation_angle_degrees != 360:
                x_in_float = x_in_float + translation_x
                y_in_float = y_in_float + translation_y

            # Find the coordinates of the top-left neighbor
            p = int(x_in_float)
            q = int(y_in_float)

            # Calculate the column and row weights
            col_weight_left = (p + 1) - x_in_float
            col_weight_right = x_in_float - ((p+1)-1) #Internal (p+1) to get the right index pixel since p is the floor

            row_weight_top = (q + 1) - y_in_float #Uses left equation
            row_weight_bottom = y_in_float - ((q+1)-1) #Internal (q+1) to get the right index pixel since q is the floor. Uses right equation

            # Ensure the indices are within bounds
            p = min(max(0, p), img_width - 2)
            q = min(max(0, q), img_height - 2)

            # Interpolate using bilinear interpolation
            intensity00 = image[q, p]
            intensity01 = image[q, p + 1]
            intensity10 = image[q + 1, p]
            intensity11 = image[q + 1, p + 1]

            PointA, PointB = interpolate(intensity00, intensity01, intensity10, intensity11, col_weight_left, col_weight_right, row_weight_top, row_weight_bottom)

            final_intensity = bilinear_interpolation(PointA, PointB, row_weight_top, row_weight_bottom)

            if 0 <= x_in_float < img_width - 1 and 0 <= y_in_float < img_height - 1:

                new_image_matrix[y_out, x_out] = final_intensity


    return new_image_matrix

def main():
    ''' Performs sequence of operations as outlined in requirements '''

    image_path_user = user_img_input()
    valid_path = path_validity(image_path_user)
    image = img_grayscale_conversion(image_path_user)
    if (valid_path is not None and image is not None):
        rotation_angle_degrees = check_angle_input()
        rotation_direction = check_direction_rotation()
        new_image = new_image_creation(image, rotation_angle_degrees, rotation_direction)
        rotated_image = cv2.imwrite("rotated_image.png", new_image)
        cv2.imshow("Rotated Image", new_image)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
