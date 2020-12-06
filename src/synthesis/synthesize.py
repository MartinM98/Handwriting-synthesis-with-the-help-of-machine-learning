import os


def create_from_skeletons(model: str, input: str, output: str, text_to_render: str):
    """
    Creates new letters from skeletons

    Args:
        model (str): Path to pix2pix model
        input (str): Path to skeletons directory
        output (str): Output directory
        text_to_render (str): String of letters to be created
    """
    for letter in text_to_render:
        letter_to_int = ord(letter)
        if letter_to_int != 32:
            if letter_to_int == 46:
                letter_path = input + 'dot/'
                output_path = output + 'dot/'
            elif letter_to_int >= 97:
                letter_path = input + letter.upper() + '2/'
                output_path = output + letter.upper() + '2/'
            else:
                letter_path = input + letter + '/'
                output_path = output + letter + '/'
            if os.path.isdir(letter_path):
                input_path = letter_path + str(len([name for name in os.listdir(letter_path)]) - 1) + '.png'
                if not os.path.exists(output_path):
                    os.mkdir(output_path)
                output_path = output_path + str(len([name for name in os.listdir(letter_path)]) - 1) + '.png'
                command = 'python ../synthesis/process-local.py --model_dir ' + model + ' --input_file ' + input_path + ' --output_file ' + output_path
                os.system(command)


if __name__ == '__main__':
    create_from_skeletons('../graphical_interface/test_model', '../graphical_interface/synthesis/skeletons/', '../graphical_interface/synthesis/synthesized/', 'a')
