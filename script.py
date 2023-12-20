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

def get_first_image_height():
    path = './original_image.jpeg'
    input_image = Image.open(path)
    return input_image.size[1]  # Getting the height of the image


def main():

    base_dir = createDirectory()
    path = './original_image.jpeg'

    image_count = 9
    block_size = 10
    noise_strength = 35

    pixelated_images = []

    first_image_height = get_first_image_height()
    # RGB or RGBA
    transparent_space = Image.new('RGB', (30, first_image_height), (0, 0, 0, 0))  # Creating a transparent image
    
    for i in range(1,image_count):

        noisy_image_path = path
        input_image = Image.open(noisy_image_path)
        pixelated = pixelate_image(input_image, block_size)
        pixelated_images.append(pixelated)
        pixelated.save(f'./{base_dir}/pixelated_image_{i}.jpeg')

        image_path = f'./{base_dir}/pixelated_image_{i}.jpeg'
        input_image = Image.open(image_path)
        noisy = add_gaussian_noise(input_image, noise_strength)
        noisy.save(f'./{base_dir}/noisy.jpeg')

        path = f'./{base_dir}/noisy.jpeg'

        if i != image_count - 1:
            pixelated_images.append(transparent_space)
    
    # delete noisy.jpeg
    os.remove(path)
    
    # Concatenate images horizontally
    concatenated_pixelated = np.concatenate([np.array(img) for img in pixelated_images], axis=1)
    # Convert numpy arrays back to PIL images
    final_pixelated = Image.fromarray(concatenated_pixelated)
    # Save the concatenated images
    final_pixelated.save(f'./{base_dir}/all_pixelated_images.jpeg')

if __name__ == "__main__":
    main()