import os
from PIL import Image

def get_img_number(filename):
    # Extracts the number from the filename
    return int(filename.split('img')[1].split('.')[0])

def concatenate_images(base_dir, target_dir):
    for subdir, dirs, files in os.walk(base_dir):
        # Sort files based on the number extracted from filenames
        files = [f for f in files if f.endswith('.jpg')]
        files = sorted(files, key=get_img_number)
        for i in range(len(files) - 1):
            img1_path = os.path.join(subdir, files[i])
            img2_path = os.path.join(subdir, files[i + 1])

            images = [Image.open(img1_path), Image.open(img2_path)]
            widths, heights = zip(*(i.size for i in images))

            total_width = sum(widths)
            max_height = max(heights)

            new_img = Image.new('RGB', (total_width, max_height))

            x_offset = 0
            for im in images:
                new_img.paste(im, (x_offset,0))
                x_offset += im.size[0]

            # Construct target path
            target_subdir = subdir.replace(base_dir, target_dir)
            os.makedirs(target_subdir, exist_ok=True)
            # Save with a name reflecting the concatenated images
            target_img_path = os.path.join(target_subdir, f'concat_{files[i].split(".")[0]}_{files[i+1].split(".")[0]}.jpg')
            new_img.save(target_img_path)

base_dir = 'test'  # Base directory containing the image directories
target_dir = 'test_concat'  # Target directory for concatenated images

concatenate_images(base_dir, target_dir)
