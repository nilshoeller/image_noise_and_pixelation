import os
import numpy as np
from PIL import Image

def add_gaussian_noise(image, strength):
    img_array = np.array(image)
    mean = 0
    std_dev = strength
    gaussian = np.random.normal(mean, std_dev, img_array.shape)
    noisy_image = img_array + gaussian
    noisy_img = Image.fromarray(noisy_image.astype('uint8'))
    
    return noisy_img

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
    noise_strength = 40

    for i in range(1,8):

        noisy_image_path = path
        input_image = Image.open(noisy_image_path)
        pixelated = pixelate_image(input_image, block_size)
        pixelated.save(f'./{base_dir}/pixelated_image_{i}.jpg')

        image_path = f'./{base_dir}/pixelated_image_{i}.jpg'
        input_image = Image.open(image_path)
        noisy = add_gaussian_noise(input_image, noise_strength)
        noisy.save(f'./{base_dir}/noisy.jpeg')

        path = f'./{base_dir}/noisy.jpeg'
    
    # delete noisy.jpeg
    os.remove(path)

if __name__ == "__main__":
    main()