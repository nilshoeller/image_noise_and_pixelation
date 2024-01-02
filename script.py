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

    noisy_img.save(f'./{BASE_DIR}/noisy.png')
    
    return (f'./{BASE_DIR}/noisy.png')

def pixelate_image(image, block_size, generated_images_list, index):
    width, height = image.size
    x_steps = width // block_size
    y_steps = height // block_size

    pixelated = image.resize((x_steps, y_steps), Image.NEAREST)
    pixelated = pixelated.resize(image.size, Image.NEAREST)

    generated_images_list.append(pixelated)
    pixelated.save(f'./{BASE_DIR}/pixelated_image_{index}.png')

    return (f'./{BASE_DIR}/pixelated_image_{index}.png')


def createDirectory() -> str :
    BASE_DIR = 'noisy_pixelised_images'
    number = 1

    find_new_path = BASE_DIR
    while os.path.exists(find_new_path):
        find_new_path = f'{BASE_DIR}_{number}'
        number += 1
    
    os.mkdir(find_new_path)

    return find_new_path


BASE_DIR = createDirectory()

def main():

    path = './original_image.png'
    input_image = Image.open(path)


    image_count = 8
    block_size = 4
    noise_strength = 30


    first_image_height = input_image.size[1]
    # RGB with .jpeg
    # RGBA with .png for transparency
    transparent_space = Image.new('RGBA', (30, first_image_height), (0, 0, 0, 0))  # Creating a transparent image

    pixelated_images = []
    pixelated_images.append(input_image)
    pixelated_images.append(transparent_space)
    
    path_pixelate = path
    for i in range(1, image_count):

        input_image = Image.open(path_pixelate)
        path_add_noise = pixelate_image(input_image, block_size, pixelated_images, i)

        input_image = Image.open(path_add_noise)
        path_pixelate = add_gaussian_noise(input_image, noise_strength)

        if i != image_count - 1:
            pixelated_images.append(transparent_space)
    
    # delete noisy.png
    os.remove(path_pixelate)
    
    # convert images to RGBA
    pixelated_images = [img.convert("RGBA") for img in pixelated_images]
    # Concatenate images horizontally
    concatenated_pixelated = np.concatenate([np.array(img) for img in pixelated_images], axis=1)
    # Convert numpy arrays back to PIL images
    final_pixelated = Image.fromarray(concatenated_pixelated)
    # Save the concatenated images
    final_pixelated.save(f'./{BASE_DIR}/all_pixelated_images.png')

if __name__ == "__main__":
    main()