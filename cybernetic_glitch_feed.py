import cv2
import numpy as np
import random

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Get frame dimensions
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Callback function for trackbars (does nothing, just required)
def nothing(x):
    pass

# Create windows for display and control
cv2.namedWindow("Cybernetic Glitch Feed")
cv2.namedWindow("Fine Tuning Board", cv2.WINDOW_NORMAL)

# Create trackbars for fine-tuning (10x more parameters for detailed control)
cv2.createTrackbar("Pixel Size", "Fine Tuning Board", 5, 50, nothing)  # Pixelation block size
cv2.createTrackbar("Glitch Shift X", "Fine Tuning Board", 5, 30, nothing)  # Horizontal glitch shift
cv2.createTrackbar("Glitch Shift Y", "Fine Tuning Board", 5, 30, nothing)  # Vertical glitch shift
cv2.createTrackbar("Noise Intensity", "Fine Tuning Board", 50, 255, nothing)  # Base noise strength
cv2.createTrackbar("Red Noise", "Fine Tuning Board", 30, 100, nothing)  # Red channel noise intensity
cv2.createTrackbar("Green Noise", "Fine Tuning Board", 40, 100, nothing)  # Green channel noise intensity
cv2.createTrackbar("Blue Noise", "Fine Tuning Board", 20, 100, nothing)  # Blue channel noise intensity
cv2.createTrackbar("Scan Line Freq", "Fine Tuning Board", 10, 50, nothing)  # Scan line frequency
cv2.createTrackbar("Particle Density", "Fine Tuning Board", 20, 100, nothing)  # Density of glowing particles
cv2.createTrackbar("Particle Speed", "Fine Tuning Board", 5, 20, nothing)  # Speed of particle movement
cv2.createTrackbar("Streak Intensity", "Fine Tuning Board", 30, 100, nothing)  # Red/green streaks intensity
cv2.createTrackbar("Binary Code Opacity", "Fine Tuning Board", 20, 100, nothing)  # Binary overlay opacity
cv2.createTrackbar("Color Shift Freq", "Fine Tuning Board", 10, 50, nothing)  # Frequency of color channel shifts
cv2.createTrackbar("Contrast Boost", "Fine Tuning Board", 100, 200, nothing)  # Contrast enhancement
cv2.createTrackbar("Blur Radius", "Fine Tuning Board", 0, 10, nothing)  # Subtle blur for depth

# Function to apply pixelation
def pixelate_frame(frame, pixel_size):
    if pixel_size <= 1:
        return frame
    small = cv2.resize(frame, (frame_width // pixel_size, frame_height // pixel_size), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(small, (frame_width, frame_height), interpolation=cv2.INTER_NEAREST)

# Function to apply glitch effect with independent X/Y shifts
def apply_glitch(frame, shift_x, shift_y):
    glitched = frame.copy()
    for _ in range(np.random.randint(1, 5)):  # Random glitch occurrences
        if np.random.rand() > 0.5:  # Horizontal glitch
            x_shift = np.random.randint(-shift_x, shift_x)
            glitched = np.roll(glitched, x_shift, axis=1)
        else:  # Vertical glitch
            y_shift = np.random.randint(-shift_y, shift_y)
            glitched = np.roll(glitched, y_shift, axis=0)
    return glitched

# Function to add colored noise with individual channel control
def add_colored_noise(frame, intensity, red_tint, green_tint, blue_tint):
    noise = np.random.randint(0, intensity, frame.shape, dtype=np.uint8)
    noise[:, :, 0] = noise[:, :, 0] * (blue_tint // 100)  # Blue channel
    noise[:, :, 1] = noise[:, :, 1] * (green_tint // 100)  # Green channel
    noise[:, :, 2] = noise[:, :, 2] * (red_tint // 100)  # Red channel
    return cv2.addWeighted(frame, 0.8, noise, 0.2, 0)

# Function to add scan lines
def add_scan_lines(frame, frequency):
    scan_lines = frame.copy()
    for y in range(0, frame_height, frequency):
        scan_lines[y:y+2, :, :] = scan_lines[y:y+2, :, :] * 0.7  # Darken scan lines
    return scan_lines

# Function to add glowing particle effects (dots and streaks)
def add_particles(frame, density, speed):
    particles = np.zeros_like(frame, dtype=np.uint8)
    num_particles = int(density * frame.size / 1000000)  # Scale density
    for _ in range(num_particles):
        x = random.randint(0, frame_width - 1)
        y = random.randint(0, frame_height - 1)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        radius = random.randint(1, 3)
        cv2.circle(particles, (x, y), radius, color, -1)
        # Add streaks (horizontal/vertical lines with fading)
        if random.random() > 0.7:
            streak_len = random.randint(5, 15)
            direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            for i in range(streak_len):
                px, py = x + direction[0] * i, y + direction[1] * i
                if 0 <= px < frame_width and 0 <= py < frame_height:
                    intensity = int(255 * (1 - i / streak_len))
                    cv2.circle(particles, (px, py), 1, color, -1, lineType=cv2.LINE_AA)
    # Move particles based on speed
    particles = np.roll(particles, (speed, speed), axis=(0, 1))
    return cv2.addWeighted(frame, 0.8, particles, 0.2, 0)

# Function to add binary code overlay
def add_binary_overlay(frame, opacity):
    binary_text = np.zeros_like(frame, dtype=np.uint8)
    for y in range(0, frame_height, 10):
        for x in range(0, frame_width, 10):
            text = random.choice(['0', '1'])
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            cv2.putText(binary_text, text, (x, y + 8), cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1, cv2.LINE_AA)
    return cv2.addWeighted(frame, (100 - opacity) / 100, binary_text, opacity / 100, 0)

# Function to apply color channel shifts
def apply_color_shift(frame, frequency):
    shifted = frame.copy()
    for _ in range(frequency // 10):  # Control frequency of shifts
        channel = random.randint(0, 2)
        shift = np.random.randint(-10, 10)
        shifted[:, :, channel] = np.roll(shifted[:, :, channel], shift, axis=random.choice([0, 1]))
    return shifted

# Function to boost contrast
def boost_contrast(frame, boost):
    alpha = boost / 100  # Contrast control
    beta = 0  # Brightness control
    return cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

# Function to apply subtle blur for depth
def apply_blur(frame, radius):
    if radius > 0:
        return cv2.GaussianBlur(frame, (radius * 2 + 1, radius * 2 + 1), 0)
    return frame

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Get trackbar values
    pixel_size = cv2.getTrackbarPos("Pixel Size", "Fine Tuning Board")
    glitch_shift_x = cv2.getTrackbarPos("Glitch Shift X", "Fine Tuning Board")
    glitch_shift_y = cv2.getTrackbarPos("Glitch Shift Y", "Fine Tuning Board")
    noise_intensity = cv2.getTrackbarPos("Noise Intensity", "Fine Tuning Board")
    red_noise = cv2.getTrackbarPos("Red Noise", "Fine Tuning Board")
    green_noise = cv2.getTrackbarPos("Green Noise", "Fine Tuning Board")
    blue_noise = cv2.getTrackbarPos("Blue Noise", "Fine Tuning Board")
    scan_freq = cv2.getTrackbarPos("Scan Line Freq", "Fine Tuning Board")
    particle_density = cv2.getTrackbarPos("Particle Density", "Fine Tuning Board")
    particle_speed = cv2.getTrackbarPos("Particle Speed", "Fine Tuning Board")
    streak_intensity = cv2.getTrackbarPos("Streak Intensity", "Fine Tuning Board")
    binary_opacity = cv2.getTrackbarPos("Binary Code Opacity", "Fine Tuning Board")
    color_shift_freq = cv2.getTrackbarPos("Color Shift Freq", "Fine Tuning Board")
    contrast_boost = cv2.getTrackbarPos("Contrast Boost", "Fine Tuning Board")
    blur_radius = cv2.getTrackbarPos("Blur Radius", "Fine Tuning Board")

    # Apply effects in sequence (10x more complexity)
    pixelated = pixelate_frame(frame, max(pixel_size, 1))
    glitched = apply_glitch(pixelated, glitch_shift_x, glitch_shift_y)
    noisy = add_colored_noise(glitched, noise_intensity, red_noise, green_noise, blue_noise)
    scanned = add_scan_lines(noisy, max(scan_freq, 1))
    particles = add_particles(scanned, particle_density, particle_speed)
    binary = add_binary_overlay(particles, binary_opacity)
    color_shifted = apply_color_shift(binary, color_shift_freq)
    contrasted = boost_contrast(color_shifted, contrast_boost)
    final_frame = apply_blur(contrasted, blur_radius)

    # Display the result
    cv2.imshow("Cybernetic Glitch Feed", final_frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()