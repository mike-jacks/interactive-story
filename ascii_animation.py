from ascii_magic import AsciiArt  # type: ignore
import time, os, sys
import json
import re
from utility import Utility, ThreadControl

def _create_ascii_art_animation_from_images(image_folder_path: str, columns: int = 150) -> list[str]:
    """
    Converts all images in a specified folder to ASCII art representations.

    Parameters:
        image_folder_path (str): The path to the folder containing image files.
        columns (int): The width of the ASCII art, in characters.

    Returns:
        list[str]: A list of ASCII art strings, each representing an image.
    """
    # Get the list of image files
    image_files = sorted([f for f in os.listdir(image_folder_path) if os.path.isfile(os.path.join(image_folder_path, f))])
    ascii_art_images = [AsciiArt.from_image(os.path.join(image_folder_path, image_file)).to_ascii(columns=columns) for image_file in image_files if image_file.endswith('.jpg')]
    return ascii_art_images

def _create_ascii_art_from_image(image_file_path: str, columns: int = 150) -> list[str]:
    """
    Converts a single image file to an ASCII art representation.

    Parameters:
        image_file_path (str): The path to the image file.
        columns (int): The width of the ASCII art, in characters.

    Returns:
        list[str]: ASCII art representation of the image.
    """
    ascii_art_image = AsciiArt.from_image(image_file_path).to_ascii(columns=columns)
    return ascii_art_image

def clean_up_ascii_art_animation(ascii_art_animation: list[str]) -> list[str]:
    """
    Cleans up ASCII art animation frames by replacing dark and bright black patterns with a space (no character).

    Parameters:
        ascii_art_animation (list[str]): A list of ASCII art animation frames.

    Returns:
        list[str]: The cleaned-up ASCII art animation frames.
    """
    dark_black_pattern = re.compile(r'(\033\[90m).')
    bright_black_pattern = re.compile(r'(\u001b\[90m).')
    hack_the_planet_animation_cleaned_up = []
    for string in ascii_art_animation:
        replaced_string = dark_black_pattern.sub(r'\033[30m ', string)
        replaced_string = bright_black_pattern.sub(r'\033[30m ', replaced_string)
        hack_the_planet_animation_cleaned_up.append(replaced_string)
    return hack_the_planet_animation_cleaned_up

def load_ascii_art_animation_from_json(json_file_path: str) -> list[str]:
    """
    Loads ASCII art animation frames from a JSON file.

    Parameters:
        json_file_path (str): The path to the JSON file containing ASCII art animation frames.

    Returns:
        list[str]: A list of ASCII art animation frames loaded from the file.
    """
    with open(json_file_path, 'r') as f:
        return json.load(f)

def play_ascii_animation(ascii_art_animation: list[str], frames_per_second: int, loop_num_times: int = 1, stop_event = None, continue_thread_after_stop_for: float = 0.0) -> ThreadControl:
    """
    Plays an ASCII art animation in the console.

    Parameters:
        ascii_art_animation (list[str]): A list of ASCII art animation frames.
        frames_per_second (int): The number of frames to display per second.
        loop_num_times (int): The number of times to loop the animation. A value of 0 will loop indefinitely.
        stop_event (threading.Event): An optional threading event to stop the animation.
        continue_thread_after_stop_for (float): Time in seconds to continue the thread after a stop event is set.

    Returns:
        ThreadControl | None: A control object for the animation thread if looping indefinitely, otherwise None.
    """

    if loop_num_times < 0:
        loop_num_times = -1 * loop_num_times
        last_frame = ascii_art_animation[0]
        for _ in range(loop_num_times):
            for i, frame in enumerate(ascii_art_animation):
                if i == 0:
                    continue
                sys.stdout.write(frame)
                sys.stdout.flush()
                time.sleep(1/frames_per_second)
                Utility.clear_multi_line(frame)
            for i, frame in enumerate(reversed(ascii_art_animation)):
                if i == 0:
                    continue
                sys.stdout.write(frame)
                sys.stdout.flush()
                time.sleep(1/frames_per_second)
                Utility.clear_multi_line(frame)
            print(last_frame)
    elif loop_num_times > 0:
        last_frame = ascii_art_animation[-1]
        for _ in range(loop_num_times):
            for frame in ascii_art_animation:
                sys.stdout.write(frame)
                sys.stdout.flush()
                time.sleep(1/frames_per_second)
                Utility.clear_multi_line(frame)
        print(last_frame)
    else:
        while True:
            def play_ascii_animation_thread(stop_event=None):
                while True:
                    if stop_event and stop_event.is_set():
                        break
                    for frame in ascii_art_animation:
                        sys.stdout.write(frame)
                        sys.stdout.flush()
                        time.sleep(1/frames_per_second)
                        Utility.clear_multi_line(frame)
                    sys.stdout.write(ascii_art_animation[-1])
                    sys.stdout.flush()
            ascii_animation_thread = ThreadControl(play_ascii_animation_thread, stop_event)
            ascii_animation_thread.start()
            time.sleep(continue_thread_after_stop_for)
            return ascii_animation_thread
    return ThreadControl(None, None)

if __name__ == "__main__":
    def main():
        """
        Main function that processes command-line arguments and initiates ASCII art conversion or animation.

        Usage:
            python script_name.py <path to image folder> <optional: true for folder of image sequence> <optional: number of columns>
        """

        if len(sys.argv) == 1:
            print("Usage: python make_ascii_json_from_image.py <path to image folder> <optional: true for folder of image sequence>")
            sys.exit(1)
        image_folder_path = sys.argv[1]
        if image_folder_path.endswith('/'):
            image_folder_path = image_folder_path[:-1]
        filename = os.path.basename(image_folder_path)
        if len(sys.argv) == 2:
            for image_file in os.listdir(image_folder_path):
                    if not image_file.endswith('.jpg') or not image_file.endswith('.png'):
                        continue
                    if image_file.endswith('.jpg') or image_file.endswith('.png'):
                        ascii_art_image = _create_ascii_art_from_image(os.path.join(image_folder_path, image_file))
                        while True:
                            try:
                                image_name, image_extension = os.path.splitext(image_file)
                                with open(f'image_json/{image_name}.json', 'w') as f:
                                    json.dump(obj=[ascii_art_image], fp=f, indent=4)
                                break
                            except FileNotFoundError:
                                os.mkdir('image_json')
                                continue
                    else:
                        print("Invalid image file type. Skipping file...")
                        continue
        elif len(sys.argv) == 3:
            if sys.argv[2] == "true" or sys.argv[2] == "True" or sys.argv[2] == "TRUE" or sys.argv[2] == "t" or sys.argv[2] == "T":
                ascii_art_animation = _create_ascii_art_animation_from_images(image_folder_path)
                while True:
                    try:
                        with open(f'animation_images_json/{filename}.json', 'w') as f:
                            json.dump(obj=ascii_art_animation, fp=f, indent=4)
                        break
                    except FileNotFoundError:
                        os.mkdir('animation_images_json')
                        continue
            elif sys.argv[2] == "false" or sys.argv[2] == "False" or sys.argv[2] == "FALSE" or sys.argv[2] == "f" or sys.argv[2] == "F" or sys.argv[2] == "" or sys.argv[2] == None:
                for image_file in os.listdir(image_folder_path):
                    if not image_file.endswith('.jpg') or not image_file.endswith('.png'):
                        continue
                    if image_file.endswith('.jpg') or image_file.endswith('.png'):
                        ascii_art_image = _create_ascii_art_from_image(os.path.join(image_folder_path, image_file))
                        while True:
                            try:
                                image_name, image_extension = os.path.splitext(image_file)
                                with open(f'image_json/{image_name}.json', 'w') as f:
                                    json.dump(obj=[ascii_art_image], fp=f, indent=4)
                                break
                            except FileNotFoundError:
                                os.mkdir('image_json')
                            continue
                    else:
                        print("Invalid image file type. Skipping file...")
                        continue
        elif len(sys.argv) == 4:
            if sys.argv[2] == "true" or sys.argv[2] == "True" or sys.argv[2] == "TRUE" or sys.argv[2] == "t" or sys.argv[2] == "T":
                try:
                    columns = int(sys.argv[3])
                except ValueError:
                    print("Invalid number of columns. Exiting...")
                    sys.exit(1)
                ascii_art_animation = _create_ascii_art_animation_from_images(image_folder_path, columns=columns)
                while True:
                    try:
                        with open(f'animation_images_json/{filename}.json', 'w') as f:
                            json.dump(obj=ascii_art_animation, fp=f, indent=4)
                        break
                    except FileNotFoundError:
                        os.mkdir('animation_images_json')
                        continue
            elif sys.argv[2] == "false" or sys.argv[2] == "False" or sys.argv[2] == "FALSE" or sys.argv[2] == "f" or sys.argv[2] == "F" or sys.argv[2] == "" or sys.argv[2] == None:
                try:
                    columns = int(sys.argv[3])
                except ValueError:
                    print("Invalid number of columns. Exiting...")
                    sys.exit(1)
                for image_file in os.listdir(image_folder_path):
                    if not image_file.endswith('.jpg') or not image_file.endswith('.png'):
                        continue
                    if image_file.endswith('.jpg') or image_file.endswith('.png'):
                        ascii_art_image = _create_ascii_art_from_image(os.path.join(image_folder_path, image_file), columns=columns)
                        while True:
                            try:
                                image_name, image_extension = os.path.splitext(image_file)
                                with open(f'image_json/{image_name}.json', 'w') as f:
                                    json.dump(obj=[ascii_art_image], fp=f, indent=4)
                                break
                            except FileNotFoundError:
                                os.mkdir('image_json')
                            continue
                    else:
                        print("Invalid image file type. Skipping file...")
                        continue
        else:
            print("Invalid number of arguments. Exiting...")
            print("Usage: python make_ascii_json_from_image.py <path to image folder> <optional: true for folder of image sequence>")
            sys.exit(1)


    main()
