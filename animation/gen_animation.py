from PIL import Image, ImageDraw

# OLED display size
WIDTH, HEIGHT = 128, 64
FRAME_COUNT = 60  # 2 seconds at 30 FPS

# Car properties
CAR_WIDTH, CAR_HEIGHT = 30, 12  # Approximate size of the car
START_X = -CAR_WIDTH  # Start off-screen
END_X = WIDTH  # End off-screen

# Redraw the car with a more detailed shape based on the inspiration image

def draw_race_car(draw, x, y):
    """Draws a stylized race car at position (x, y)."""
    # Car body (sleek shape)
    draw.polygon([
        (x, y + 6), (x + 4, y + 2), (x + 12, y), (x + 22, y + 2),
        (x + 28, y + 6), (x + 30, y + 10), (x + 28, y + 12), (x + 2, y + 12),
        (x, y + 10)
    ], fill=1, outline=1)
    
    # Wheels
    draw.ellipse([x + 4, y + 10, x + 10, y + 16], fill=1, outline=1)  # Front wheel
    draw.ellipse([x + 20, y + 10, x + 26, y + 16], fill=1, outline=1)  # Rear wheel
    
    # Windows
    draw.line([x + 6, y + 3, x + 18, y + 3], fill=1)  # Windshield
    draw.line([x + 18, y + 3, x + 24, y + 6], fill=1)  # Side window

# Generate new animation frames with the improved car design
frames = []
for i in range(FRAME_COUNT):
    frame = Image.new("1", (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(frame)
    
    # Compute car position
    x = int(START_X + (END_X - START_X) * (i / (FRAME_COUNT - 1)))
    y = HEIGHT // 2 - 6  # Adjusted for new car height

    # Draw the improved race car
    draw_race_car(draw, x, y)

    # Speed lines
    if x > 0:
        for j in range(3):
            draw.line([x - (j * 4), y + 8, x - (j * 4) - 3, y + 8], fill=1)

    frames.append(frame.convert("P"))

# Save the improved animation
gif_path = "./improved_race_car_animation.gif"
frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=1000//30, loop=0)
gif_path
