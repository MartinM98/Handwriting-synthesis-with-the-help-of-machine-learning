from typing import Tuple
import src.file_handler.file_handler as fh
import src.recognition.printed_text_recognition as pth
import multiprocessing
import cv2
from glob import glob


def crop_image(image):
    """
    Divide image into two parts.

    Args:
        image (image): Base image.

    Returns:
        (image, image): (Printed image, Handwritten image)
    """
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)

    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)
                      [2], reverse=True)[1:4]
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])

    bounding_rect1 = cv2.boundingRect(contours[0])
    bounding_rect2 = cv2.boundingRect(contours[1])
    bounding_rect3 = cv2.boundingRect(contours[2])

    crop_image1 = image[bounding_rect1[1] + 13:bounding_rect2[1] - 1, :]
    crop_image2 = image[bounding_rect2[1] + 13: bounding_rect3[1] - 1, :]

    return crop_image1, crop_image2


def preproduce(args: Tuple[str, str, str, bool]):
    """
    Divide and crop the dataset image to two images.
    One with the handwritten part and second with
    the printed text from the image. The function can delete
    the base image.

    Args:
        args (str, str, str, bool):
            file_path (str): Path to the image.
            PT_dir (str): Path to the directory where printed part is saving.
            HT_dir (str): Path to the directory where handwritten part is saving.
            delete_file_flag (bool): Flag decide if the image is deleted after the preproduce.
    """
    file_path, PT_dir, HT_dir, delete_file_flag = args
    image = cv2.imread(file_path)
    crop_image1, crop_image2 = crop_image(image)

    name = fh.get_file_name(file_path) + '.png'
    if crop_image1.size == 0 or crop_image2.size == 0:
        print(name)

    cv2.imwrite(fh.combine_paths(PT_dir, 'PT_' + name), crop_image1)
    cv2.imwrite(fh.combine_paths(HT_dir, 'HT_' + name), crop_image2)

    if delete_file_flag:
        fh.delete_file(file_path)


def preproduce_set(path: str, output_dir: str = None,
                   delete_file_flag: bool = False):
    """
    The function preproduce whole set provided in the 'path' variable.
    The 'output_dir' variable is optional and decide where resulta are saving
    (If the variable is None then, results are saving in the 'path' localization).
    The preproduced files can be deleted after the process.

    The funtion uses multiprocessing to improve the time of computing.

    Args:
        path (str): Path to the directory with the images.
        output_dir (str, optional): Path to the directory where the results are saving.
                                    Defaults to None.
        delete_file_flag (bool, optional): Flag decide if the image is deleted after the preproduce.
                                    Defaults to False.
    """
    PT_dir = 'PrintedText/'
    HT_dir = 'HandwrittenText/'
    TXT_dir = 'Text/'
    if output_dir is not None:
        PT_dir = fh.combine_paths(output_dir, PT_dir)
        HT_dir = fh.combine_paths(output_dir, HT_dir)
        TXT_dir = fh.combine_paths(output_dir, TXT_dir)
    else:
        PT_dir = fh.combine_paths(path, PT_dir)
        HT_dir = fh.combine_paths(path, HT_dir)
        TXT_dir = fh.combine_paths(path, TXT_dir)

    fh.ensure_create_dir(PT_dir)
    fh.ensure_create_dir(HT_dir)
    fh.ensure_create_dir(TXT_dir)

    dir_path = fh.combine_paths(path, '*.png')
    iterable = [(file, PT_dir, HT_dir, delete_file_flag)
                for file in glob(dir_path)]

    p = multiprocessing.Pool()
    p.map_async(preproduce, iterable)

    p.close()
    p.join()  # Wait for all child processes to close.

    dir_path = fh.combine_paths(PT_dir, '*.png')
    pth.take_texts(glob(dir_path), TXT_dir)


if __name__ == '__main__':
    path_to_dataset = fh.get_absolute_path('./data')
    preproduce_set(path_to_dataset)
