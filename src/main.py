from videoengine import *

'''
    Resources used:
    1. https://www.thepythoncode.com/article/extract-frames-from-videos-in-python - Extracting frames from videos in python
    2. https://pyimagesearch.com/2021/01/20/opencv-getting-and-setting-pixels/ - Working with image pixels in python
    3. https://www.life2coding.com/create-a-white-background-image-using-opencv-in-python/ - Creating a blank image with OpenCV
    4. https://gist.github.com/AidySun/bb2b90a993d74400ababb8c8bdbf1d40 - Shuffle 2D Matrix
    5. https://www.geeksforgeeks.org/python-opencv-cv2-blur-method/ - Blur filtering in OpenCV
    6. https://stackoverflow.com/questions/16070078/change-saturation-with-imagekit-pil-or-pillow - PIL, enhancing saturation
'''

if __name__ == "__main__":
    import sys

    start_log()

    try:
        video_file = sys.argv[1]

        height = 500 if len(sys.argv) < 3 else int(sys.argv[2])
        width = 800 if len(sys.argv) < 4 else int(sys.argv[3])

        folder_name = ve_run(video_file) + "/"

        log("Generation is about to start...")
        generate_image(folder_name, video_file.split(".")[0], height, width)
    except:
        log(f"A critical error occurred: {sys.exc_info()[0]}. Program is about to stop...", False)
    
    log_file.close()
        
    

