from ascii_magic import AsciiArt  # type: ignore
import time, os, sys
import json
from utility import Utility, ThreadControl

def _create_ascii_art_animation_from_images(image_folder_path: str, columns: int = 150) -> list[str]:
    # Get the list of image files
    image_files = sorted([f for f in os.listdir(image_folder_path) if os.path.isfile(os.path.join(image_folder_path, f))])
    ascii_art_images = [AsciiArt.from_image(os.path.join(image_folder_path, image_file)).to_ascii(columns=columns) for image_file in image_files if image_file.endswith('.jpg')]
    return ascii_art_images

def _create_ascii_art_from_image(image_file_path: str, columns: int = 150) -> list[str]:
    ascii_art_image = AsciiArt.from_image(image_file_path).to_ascii(columns=columns)
    return ascii_art_image

def load_ascii_art_animation_from_json(json_file_path: str) -> list[str]:
    with open(json_file_path, 'r') as f:
        return json.load(f)

def play_ascii_animation(ascii_art_animation: list[str], frames_per_second: int, loop_num_times: int = 1, stop_event = None, continue_thread_after_stop_for: float = 0.0) -> ThreadControl | None:
    if loop_num_times < 0:
        loop_num_times = -1 * loop_num_times
        last_frame = ascii_art_animation[0]
        for _ in range(loop_num_times):
            for i, frame in enumerate(ascii_art_animation):
                if i == 0:
                    continue
                print(frame)
                time.sleep(1/frames_per_second)
                Utility.clear_multi_line(frame)
            for i, frame in enumerate(reversed(ascii_art_animation)):
                if i == 0:
                    continue
                print(frame)
                time.sleep(1/frames_per_second)
                Utility.clear_multi_line(frame)
            print(last_frame)
            return None
    elif loop_num_times > 0:
        last_frame = ascii_art_animation[-1]
        for _ in range(loop_num_times):
            for frame in ascii_art_animation:
                print(frame)
                time.sleep(1/frames_per_second)
                Utility.clear_multi_line(frame)
        print(last_frame)
        return None
    else:
        while True:
            def play_ascii_animation_thread(stop_event=None):
                while True:
                    if stop_event and stop_event.is_set():
                        break
                    last_frame = ascii_art_animation[-1]
                    for frame in ascii_art_animation:
                        print(frame)
                        time.sleep(1/frames_per_second)
                        Utility.clear_multi_line(frame)
                print(last_frame)
            ascii_animation_thread = ThreadControl(play_ascii_animation_thread, stop_event)
            ascii_animation_thread.start()
            time.sleep(continue_thread_after_stop_for)
            return ascii_animation_thread
    return None
        
if __name__ == "__main__":
    def main():
        if len(sys.argv) == 1:
            print("Usage: python make_ascii_json_from_image.py <path to image folder> <optional: true for folder of image sequence>")
            sys.exit(1)
        image_folder_path = sys.argv[1]
        if image_folder_path.endswith('/'):
            image_folder_path = image_folder_path[:-1]
        filename = os.path.basename(image_folder_path)
        if len(sys.argv) == 2:
            for image_file in os.listdir(image_folder_path):
                    if not image_file.endswith('.jpg'):
                        continue
                    if image_file.endswith('.jpg'):
                        ascii_art_image = _create_ascii_art_from_image(os.path.join(image_folder_path, image_file))
                        while True:
                            try:
                                image_name, image_extension = os.path.splitext(image_file)
                                with open(f'image_json/{image_file.strip(".jpg")}.json', 'w') as f:
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
                    if not image_file.endswith('.jpg'):
                        continue
                    if image_file.endswith('.jpg'):
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
                    if not image_file.endswith('.jpg'):
                        continue
                    if image_file.endswith('.jpg'):
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
