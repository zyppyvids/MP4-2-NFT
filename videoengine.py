from datetime import timedelta
from imagegenerator import *

# Defines how much frames it saves in a second. 20-30 is good because its not a small value but it is not as big as the FPS of most videos.
FRAMES_PER_SECOND = 25

def format_td(td):
    """Utility function to format timedelta objects in a cool way (i.e 00:00:20.05) omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return (result.lstrip() + ".00").replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)

    # ': 02' type of formatting leads to a space we don't want (i.e [2 : 02 -> ' 02'])
    ms_text = ("0" + str(ms)) if ms < 10 else ms

    return f"{result.lstrip()}.{ms_text}".replace(":", "-")


def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []

    # Get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    
    # Use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)

    return s

def ve_run(video_file):
    # Saving frames is true by default
    save_frames = True

    log(f"Reading file {video_file}...")

    folder_name, _ = os.path.splitext(video_file)
    folder_name += "-frames"

    log(f"Frames are going to be saved in \"{folder_name}\".")
    
    # Try to make a folder with the created name
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    else:
        input_value = get_input(f"A folder with the name \"{folder_name}\" already exists. Do you want to overwrite them [Y / N]: ", False);
        if input_value.lower() == "y":
            import shutil
            shutil.rmtree(folder_name)
            os.mkdir(folder_name)   
            
            save_frames = True
        elif input_value.lower() == "n":
            save_frames = False
        else:
            log("Invalid input.");

            return 0

    # Read the video file    
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_per_second = min(fps, FRAMES_PER_SECOND)
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)

    frame_count = 0
    
    while True:
        is_read, frame = cap.read()
        
        if not is_read:
            break

        frame_duration = frame_count / fps
        
        try:
            # Get the earliest duration to save
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # The list is empty, all duration frames were saved
            break
        if frame_duration >= closest_duration and save_frames:
            frame_duration_formatted = format_td(timedelta(seconds = frame_duration))

            log(f"Saving frame{frame_duration_formatted}.png...")

            cv2.imwrite(os.path.join(folder_name, f"frame{frame_duration_formatted}.png"), frame) 
            # Drop the duration spot from the list, since this duration spot is already saved
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # Increment the frame count
        frame_count += 1
    
    return folder_name