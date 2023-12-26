from PIL import Image

def convert_jpg_to_png(jpg_path, png_path):
    img = Image.open(jpg_path)
    img.save(png_path)

if __name__ == "__main__":
    convert_jpg_to_png("tmp/output.png", "tmp/output.png")