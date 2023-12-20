import os
import cv2
import numpy as np
from PIL import Image

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("Image file not found or unable to read the file.")
    return image

def add_gaussian_noise(image, strength):
    noise = np.random.normal(0, strength, image.shape).astype('uint8')
    noisy_image = cv2.add(image, noise)
    return noisy_image

def pixelate_image(image, block_size):
    width, height = image.size
    x_steps = width // block_size
    y_steps = height // block_size

    pixelated = image.resize((x_steps, y_steps), Image.NEAREST)
    pixelated = pixelated.resize(image.size, Image.NEAREST)
    return pixelated


def createDirectory() -> str :
    base_dir = 'noisy_pixelised_images'
    number = 1

    find_new_path = base_dir
    while os.path.exists(find_new_path):
        find_new_path = f'{base_dir}_{number}'
        number += 1
    
    os.mkdir(find_new_path)

    return find_new_path


def main():

    base_dir = createDirectory()
    path = './original_image.jpeg'

    block_size = 10
    noise_strength = 100

    for i in range(1,5):

        # pixelate image
        noisy_image_path = path
        input_image = Image.open(noisy_image_path)
        pixelated = pixelate_image(input_image, block_size)
        pixelated.save(f'./{base_dir}/pixelated_image_{i}_1.jpg')

        # add noise to image
        try:
            image_path = f'./{base_dir}/pixelated_image_{i}_1.jpg'
            image = load_image(image_path)

            noisy_image = add_gaussian_noise(image, noise_strength)

            noisy_image_output_path = f'./{base_dir}/noisy_{i}.jpeg'
            cv2.imwrite(noisy_image_output_path, noisy_image)
        except Exception as e:
            print("An error occurred:", e)

        # pixelate image
        noisy_image_path = f'./{base_dir}/noisy_{i}.jpeg'
        input_image = Image.open(noisy_image_path)
        pixelated = pixelate_image(input_image, block_size)
        pixelated.save(f'./{base_dir}/pixelated_image_{i}_2.jpg')

        path = f'./{base_dir}/pixelated_image_{i}_2.jpg'
    

if __name__ == "__main__":
    main()