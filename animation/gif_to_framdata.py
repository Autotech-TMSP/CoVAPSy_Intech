from PIL import Image
import sys

def convert_gif_to_bitmap(gif_path, output_path):
    # Open the GIF file
    gif = Image.open(gif_path)
    
    frame_data = []
    
    # Iterate through each frame in the GIF
    for frame in range(gif.n_frames):
        gif.seek(frame)
        # Convert the frame to monochrome (1-bit pixels, black and white)
        bitmap = gif.convert('1')
        # Get the pixel data
        pixels = list(bitmap.getdata())
        # Convert the pixel data to bytes
        byte_data = []
        for y in range(bitmap.height):
            for x in range(0, bitmap.width, 8):
                byte = 0
                for bit in range(8):
                    if x + bit < bitmap.width:
                        byte |= (pixels[y * bitmap.width + x + bit] == 0) << (7 - bit)
                byte_data.append(byte)
        frame_data.append(byte_data)
    
    # Write the frame data to the output file
    with open(output_path, 'w') as f:
        f.write('const uint8_t frames[][{}] = {{\n'.format(len(frame_data[0])))
        for frame in frame_data:
            f.write('  {')
            f.write(', '.join('0x{:02X}'.format(byte) for byte in frame))
            f.write('},\n')
        f.write('};\n')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python gif_to_framdata.py <input_gif> <output_file>')
        sys.exit(1)
    
    gif_path = sys.argv[1]
    output_path = sys.argv[2]
    
    convert_gif_to_bitmap(gif_path, output_path)