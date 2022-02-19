import cv2
from cmdengine import *
import numpy as np
from math import floor
from random import randint
from PIL import Image, ImageEnhance

def shuffle_matrix(matrix, seed, axis = 0):
    '''A function that shuffles a 2D matrix by column or row.''' 
    np.random.seed(seed)
    
    # By column
    if axis == 0:
        m = matrix.shape[1]
        permutation = list(np.random.permutation(m))
        shuffled_matrix = matrix[:, permutation]
    # By row
    else:
        m = matrix.shape[0]
        permutation = list(np.random.permutation(m))
        shuffled_matrix = matrix[permutation, :]

    return shuffled_matrix

def generate_image(folder_name, file_name, height, width):
    '''A function that generates an image from the frames of a video.''' 
    frames_imgs = os.listdir(folder_name)

    # Creates a blank image 
    generated = np.zeros([height, width, 3], dtype = np.uint8)
    generated.fill(255)
    
    written = cv2.imwrite(f"generated-{file_name}.png", generated)
    
    if not written:
        log("An error occurred while generating a new image (first phase).", False)

        return 0

    progress_counter = 0

    pixels_per_frame = floor((height * width) / len(frames_imgs))
    log(f"Pixels that are going to be used per frame are {pixels_per_frame}.")

    generated_img = cv2.imread(f"generated-{file_name}.png", 1)
    
    height_iter = 0
    width_iter = 0

    for img_path in frames_imgs:
        cur_img = cv2.imread(folder_name + img_path, 1)

        # Resizes image for optimization reasons
        resized_img = cv2.resize(cur_img, (width, height),
               interpolation = cv2.INTER_NEAREST)
           
        for iterator in range(pixels_per_frame):
            rand_h = randint(0, height - 1)
            rand_w = randint(0, width - 1)

            generated_img[height_iter, width_iter] = resized_img[rand_h, rand_w]
            progress_counter += 1

            if(width_iter < width - 1):
                width_iter += 1
            else:
                width_iter = 0
                height_iter += 1
                
            log(f"Generation progress: {progress_counter}/(~{height * width})")
    
    log("Shuffling is about to start...")
    
    # Shuffle 2D Matrix
    for iterator in range(floor(width / 1.5)):
        log(f"Shuffle progress (width): {iterator + 1}/{floor(width / 1.5)}")
        generated_img = shuffle_matrix(generated_img, height * width, 0)
    
    for iterator in range(floor(height / 1.5)):
        log(f"Shuffle progress (height): {iterator + 1}/{floor(height / 1.5)}")
        generated_img = shuffle_matrix(generated_img, height * width, 1)

    log("Blurring is about to start...")
    
    # Blur effect
    # See link number 5 in the Resources list in main.py for more info.
    dilation_kernel_size = np.ones((4, 4), 'uint8')
    blur_kernel_size = 25

    try:
        generated_img = cv2.dilate(generated_img, dilation_kernel_size, iterations = 1)
    except:
        log("An error occurred while generating a new image (dilation).", False)

        return 0

    try:
        generated_img = cv2.medianBlur(generated_img, blur_kernel_size)
    except:
        log("An error occurred while generating a new image (median blur).", False)

        return 0

    try:
        generated_img = cv2.bilateralFilter(generated_img, 15, 150, 10)
    except:
        log("An error occurred while generating a new image (bilateral filter).", False)

        return 0
    
    log("Image shown on display (UNSATURATED)...")

    cv2.imshow("(UNSATURATED) Press ENTER to continue...", generated_img)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    final_image = cv2.imwrite(f"generated-{file_name}.png", generated_img)

    if not final_image:
        log("An error occurred while generating a new image (final phase).", False)

        return 0

    log("Saturation is about to start...")

    image = Image.open(f"generated-{file_name}.png")
    saturation_filter = ImageEnhance.Color(image)
    saturated_img = saturation_filter.enhance(4)

    saturated_img.save(f"generated-{file_name}.png")

    log("Image shown on display (SATURATED)...")

    saturated_img.show()

    log(f"Image saved as generated-{file_name}.png", False)