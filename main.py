# Image Pixelizer

from PIL import Image
import sys

def createNewImage(data_str, width, height, pixel_size):

    new_image_data = [[0 for x in range(width)] for y in range(height)]
    old_image_data = [[0 for x in range(width)] for y in range(height)]

    # Converting our bit string string to a 2D array
    # easier for manipulating when pixelating the image
    i = 0
    while (i < len(data_str)):
        for j in range(height):
            for k in range(width):
                old_image_data[j][k] = data_str[i]
                i = i + 1

    # Creating each pixel blok for final image
    for i in range(int(height/pixel_size)):
        for j in range(int(width/pixel_size)):
            h_start = i * pixel_size
            w_start = j * pixel_size

            value = [0,0,0]
            numVals = 0

            for a in range(h_start, h_start + pixel_size):
                for b in range(w_start, w_start + pixel_size):
                    try:
                        rgb_values = old_image_data[a][b]

                        value[0] += rgb_values[0]
                        value[1] += rgb_values[1]
                        value[2] += rgb_values[2]
                        numVals += 1

                    except Exception:
                        continue

            # Helps us avoid a divide by 0 error (this would occur when
            # we are at the end of an image)
            if (numVals == 0):
                numVals = 1

            new_values = (value[0]//numVals, value[1]//numVals, value[2]//numVals)

            # Assign averaged data to each pixel of the new block
            # based on the our pixel block size
            for a in range(h_start, h_start + pixel_size):
                for b in range(w_start, w_start + pixel_size):
                    try:
                        new_image_data[a][b] = new_values
                    except Exception:
                        pass

    # Our new data for the new image
    return new_image_data

def processData(data):
    new_data = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            new_data.append(data[i][j])
    return new_data


def main():
    if (len(sys.argv) != 4):
        print("incorrect number of arguments")
        return

    # Read in image file name (with extension)
    image_fp = sys.argv[1]
    # Read in the pixel size (in number of pixels)
    block_size = int(sys.argv[2])
    # Read in output file name (with extension) for new image
    file_output_name = sys.argv[3]

    image = None
    try:
        image = Image.open(image_fp)
    except Exception:
        print("Unable to open image file {image_filepath}.".format(image_filepath=image_fp))
        print("Image may nto exist")

    if image:
        image_data = list(image.getdata())
        size = image.size

        # new_data is a 2D array of pixelated data
        new_data = createNewImage(image_data, size[0], size[1], block_size)
        # converts 2D array to 1D array
        new_data = processData(new_data)

        new_image = Image.new(image.mode, image.size)
        new_image.putdata(new_data)
        new_image.save(file_output_name)

    return

if __name__ == '__main__':

    main()