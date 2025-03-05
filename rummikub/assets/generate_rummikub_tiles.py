from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os
import sys
from typing import Tuple, Optional
import math

# Configuration for authentic Rummikub tiles
TILE_WIDTH = 60
TILE_HEIGHT = 100
BORDER_RADIUS = 5
BORDER_WIDTH = 2
OUTPUT_DIR = "rummikub_tiles"  # Output directory for the tiles

# Define colors to match authentic Rummikub sets
COLORS = {
    "red": (215, 38, 38),     # Bright red
    "blue": (30, 80, 190),    # Royal blue
    "black": (20, 20, 20),    # Rich black
    "yellow": (235, 180, 0)   # Rummikub uses yellow (not orange)
}

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def find_joker_face():
    """Search for the joker face image in multiple possible locations."""
    # Try multiple possible locations for the joker face
    possible_paths = [
        "joker_face.png",
        "assets/joker_face.png",
        "rummikub/assets/joker_face.png",
        "rummikub/assets/tiles/joker_face.png",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "joker_face.png"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "joker_face.png")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found joker face at: {path}")
            return path
    
    print("Warning: Could not find joker_face.png in any expected location.")
    return None

def rounded_rectangle(draw, xy, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = xy
    draw.rectangle((x1+radius, y1, x2-radius, y2), fill=fill, outline=None)
    draw.rectangle((x1, y1+radius, x2, y2-radius), fill=fill, outline=None)
    draw.pieslice((x1, y1, x1+radius*2, y1+radius*2), 180, 270, fill=fill)
    draw.pieslice((x2-radius*2, y1, x2, y1+radius*2), 270, 0, fill=fill)
    draw.pieslice((x1, y2-radius*2, x1+radius*2, y2), 90, 180, fill=fill)
    draw.pieslice((x2-radius*2, y2-radius*2, x2, y2), 0, 90, fill=fill)
    
    if outline:
        draw.arc((x1, y1, x1+radius*2, y1+radius*2), 180, 270, fill=outline, width=width)
        draw.arc((x2-radius*2, y1, x2, y1+radius*2), 270, 0, fill=outline, width=width)
        draw.arc((x1, y2-radius*2, x1+radius*2, y2), 90, 180, fill=outline, width=width)
        draw.arc((x2-radius*2, y2-radius*2, x2, y2), 0, 90, fill=outline, width=width)
        
        draw.line((x1+radius, y1, x2-radius, y1), fill=outline, width=width)
        draw.line((x1+radius, y2, x2-radius, y2), fill=outline, width=width)
        draw.line((x1, y1+radius, x1, y2-radius), fill=outline, width=width)
        draw.line((x2, y1+radius, x2, y2-radius), fill=outline, width=width)

def create_tile_base(scale=3):
    """Create a base tile with authentic Rummikub styling."""
    # Create a high-res base image
    width, height = TILE_WIDTH * scale, TILE_HEIGHT * scale
    base = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    
    # Off-white ivory color for authentic Rummikub tiles
    ivory = (250, 248, 240)
    
    # Create the main tile shape with rounded corners
    rounded_rectangle(draw, (0, 0, width, height), BORDER_RADIUS * scale, fill=ivory)
    
    # Add subtle texture like real tiles (fine grain)
    for i in range(0, width, 2):
        for j in range(0, height, 2):
            if (i + j) % 8 == 0:  # Sparse noise pattern
                shade = (245, 243, 235)
                draw.point((i, j), fill=shade)
    
    # Add subtle 3D effect with gradient shading
    for y in range(height):
        for x in range(width):
            # Distance from top-left (for gradient)
            dist = math.sqrt((x/width) ** 2 + (y/height) ** 2) * 15
            if 0 < x < width-1 and 0 < y < height-1:
                current_color = base.getpixel((x, y))
                if current_color[3] > 0:  # Only modify non-transparent pixels
                    shade = int(max(0, min(10, dist)))
                    new_color = tuple(max(c-shade, 220) for c in current_color[:3]) + (current_color[3],)
                    base.putpixel((x, y), new_color)

    # Add subtle highlight along top and left edges
    highlight = (255, 255, 255, 100)
    edge_width = scale
    for i in range(BORDER_RADIUS * scale, width - BORDER_RADIUS * scale):
        for j in range(edge_width):
            if base.getpixel((i, j))[3] > 0:
                base.putpixel((i, j), highlight)
                
    for j in range(BORDER_RADIUS * scale, height - BORDER_RADIUS * scale):
        for i in range(edge_width):
            if base.getpixel((i, j))[3] > 0:
                base.putpixel((i, j), highlight)
    
    return base

def create_number_tile(number, color_name, color_rgb, scale=3):
    """Create a number tile with authentic Rummikub styling."""
    # Get the base tile
    img = create_tile_base(scale)
    draw = ImageDraw.Draw(img)
    
    # Determine font size based on number of digits
    base_size = 55 * scale
    if number >= 10:
        base_size = 48 * scale
    
    # Try to load a bold sans-serif font similar to Rummikub
    try:
        # Try Arial Bold first (common on Windows)
        font = ImageFont.truetype("Arial Bold.ttf", base_size)
    except:
        try:
            font = ImageFont.truetype("arialbd.ttf", base_size)  # Another name for Arial Bold
        except:
            try:
                font = ImageFont.truetype("DejaVuSans-Bold.ttf", base_size)  # Common on Linux
            except:
                try:
                    # Try regular Arial if bold isn't available
                    font = ImageFont.truetype("Arial.ttf", base_size)  
                except:
                    # Fallback to default font
                    font = ImageFont.load_default()
                    base_size = base_size // 3  # Adjust size for default font
    
    # Draw the number with proper positioning
    number_text = str(number)
    
    # Get text dimensions
    try:
        # For newer Pillow versions
        bbox = draw.textbbox((0, 0), number_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except:
        # For older Pillow versions
        text_width, text_height = draw.textsize(number_text, font=font)
    
    # Position text in the center
    x = (TILE_WIDTH * scale - text_width) // 2
    y = (TILE_HEIGHT * scale - text_height) // 2 - scale * 2  # Slightly above center
    
    # Create embossed/3D effect for the number
    # 1. Drop shadow
    shadow_offset = scale
    shadow_color = tuple(max(0, c-60) for c in color_rgb)
    draw.text((x + shadow_offset, y + shadow_offset), number_text, fill=shadow_color, font=font)
    
    # 2. Main number
    draw.text((x, y), number_text, fill=color_rgb, font=font)
    
    # Add a small identifier at the bottom
    try:
        small_font_size = 11 * scale
        try:
            small_font = ImageFont.truetype("Arial.ttf", small_font_size)
        except:
            try:
                small_font = ImageFont.truetype("DejaVuSans.ttf", small_font_size)
            except:
                small_font = ImageFont.load_default()
                small_font_size = small_font_size // 3
    
        # Get small text width
        try:
            small_bbox = draw.textbbox((0, 0), color_name.upper(), font=small_font)
            small_width = small_bbox[2] - small_bbox[0]
        except:
            small_width, _ = draw.textsize(color_name.upper(), font=small_font)
        
        # Position at bottom
        bottom_margin = 10 * scale
        small_x = (TILE_WIDTH * scale - small_width) // 2
        small_y = TILE_HEIGHT * scale - bottom_margin - small_font_size
        
        draw.text((small_x, small_y), color_name.upper(), fill=color_rgb, font=small_font)
    except Exception as e:
        print(f"Warning: Could not add color name: {e}")
    
    # Resize to final dimensions with antialiasing
    img = img.resize((TILE_WIDTH, TILE_HEIGHT), Image.LANCZOS)
    
    return img

def create_joker_tile(joker_face_path=None, scale=3):
    """Create a joker tile with authentic Rummikub styling using the provided joker face."""
    # Get the base tile
    img = create_tile_base(scale)
    draw = ImageDraw.Draw(img)
    
    # Add a thin black border around the edge
    border_color = (0, 0, 0)
    border_rect = (
        BORDER_WIDTH * scale // 2, 
        BORDER_WIDTH * scale // 2, 
        TILE_WIDTH * scale - BORDER_WIDTH * scale // 2, 
        TILE_HEIGHT * scale - BORDER_WIDTH * scale // 2
    )
    rounded_rectangle(draw, border_rect, BORDER_RADIUS * scale - 1, 
                     outline=border_color, width=BORDER_WIDTH * scale)
    
    # Try to load the joker face image
    if joker_face_path and os.path.exists(joker_face_path):
        try:
            # Load the joker face
            joker_face = Image.open(joker_face_path).convert("RGBA")
            
            # Remove any background (assuming it's on a transparent or white background)
            # This makes the image work better when pasted onto our tile
            
            # Resize to fit nicely on the tile (approximately 2/3 of the tile height)
            face_size = int(TILE_HEIGHT * scale * 0.6)
            joker_face = joker_face.resize((face_size, face_size), Image.LANCZOS)
            
            # Center it in the upper portion of the tile
            face_position = (
                (TILE_WIDTH * scale - face_size) // 2,
                int(TILE_HEIGHT * scale * 0.20)
            )
            
            # Paste the joker face onto the tile
            img.paste(joker_face, face_position, joker_face)
            
        except Exception as e:
            print(f"Error processing joker face: {e}")
            print("Using fallback joker text")
            draw_fallback_joker(draw, scale)
    else:
        print("Joker face image not found, using text fallback")
        draw_fallback_joker(draw, scale)
    
    # Add "JOKER" text at the bottom
    try:
        joker_font_size = 18 * scale
        try:
            joker_font = ImageFont.truetype("Arial Bold.ttf", joker_font_size)
        except:
            try:
                joker_font = ImageFont.truetype("arialbd.ttf", joker_font_size)
            except:
                try:
                    joker_font = ImageFont.truetype("DejaVuSans-Bold.ttf", joker_font_size)
                except:
                    joker_font = ImageFont.load_default()
                    joker_font_size = joker_font_size // 3
        
        joker_text = "JOKER"
        
        # Get text width
        try:
            joker_bbox = draw.textbbox((0, 0), joker_text, font=joker_font)
            joker_width = joker_bbox[2] - joker_bbox[0]
        except:
            joker_width, _ = draw.textsize(joker_text, font=joker_font)
        
        # Position at bottom
        bottom_margin = 15 * scale
        joker_x = (TILE_WIDTH * scale - joker_width) // 2
        joker_y = TILE_HEIGHT * scale - bottom_margin - joker_font_size
        
        # Draw with slight shadow for 3D effect
        draw.text((joker_x + scale, joker_y + scale), joker_text, fill=(50, 50, 50), font=joker_font)
        draw.text((joker_x, joker_y), joker_text, fill=(0, 0, 0), font=joker_font)
    except Exception as e:
        print(f"Warning: Could not add JOKER text: {e}")
    
    # Resize to final dimensions with antialiasing
    img = img.resize((TILE_WIDTH, TILE_HEIGHT), Image.LANCZOS)
    
    return img

def draw_fallback_joker(draw, scale):
    """Draw a fallback joker text if image isn't available."""
    try:
        # Load a large font for the word "JOKER"
        large_font_size = 32 * scale
        try:
            large_font = ImageFont.truetype("Arial Bold.ttf", large_font_size)
        except:
            try:
                large_font = ImageFont.truetype("DejaVuSans-Bold.ttf", large_font_size)
            except:
                large_font = ImageFont.load_default()
                large_font_size = large_font_size // 3
        
        # Draw multicolor "JOKER" text
        joker_text = "JOKER"
        
        # Calculate text size
        try:
            bbox = draw.textbbox((0, 0), joker_text, font=large_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except:
            text_width, text_height = draw.textsize(joker_text, font=large_font)
        
        # Center text in upper portion of tile
        x = (TILE_WIDTH * scale - text_width) // 2
        y = (TILE_HEIGHT * scale // 3) - (text_height // 2)
        
        # Draw with multiple colors (like a rainbow effect)
        colors = list(COLORS.values())
        letter_width = text_width / len(joker_text)
        
        for i, letter in enumerate(joker_text):
            color = colors[i % len(colors)]
            draw.text((x + i * letter_width, y), letter, fill=color, font=large_font)
    except Exception as e:
        print(f"Warning: Fallback joker text failed: {e}")

def create_preview_image(tile_paths):
    """Create a preview image with all generated tiles."""
    # Calculate grid dimensions based on number of tiles
    total_tiles = len(tile_paths)
    cols = min(13, total_tiles)
    rows = (total_tiles + cols - 1) // cols  # Ceiling division
    
    # Create preview canvas with gray background
    preview = Image.new('RGBA', 
                      (cols * TILE_WIDTH + (cols-1) * 5, rows * TILE_HEIGHT + (rows-1) * 10),
                      (220, 220, 220, 255))
    
    # Place each tile on the preview
    for i, path in enumerate(tile_paths):
        if os.path.exists(path):
            tile = Image.open(path)
            row = i // cols
            col = i % cols
            x = col * (TILE_WIDTH + 5)
            y = row * (TILE_HEIGHT + 10)
            preview.paste(tile, (x, y), tile)
    
    return preview

def main():
    print("Generating authentic Rummikub tiles...")
    
    # Find the joker face image
    joker_face_path = find_joker_face()
    
    # List to track all generated tile paths for preview
    all_tile_paths = []
    
    # Generate number tiles
    for color_name, color_rgb in COLORS.items():
        for number in range(1, 14):  # Numbers 1-13
            img = create_number_tile(number, color_name, color_rgb)
            filename = f"tile_{number}_{color_name}.png"
            filepath = os.path.join(OUTPUT_DIR, filename)
            img.save(filepath)
            all_tile_paths.append(filepath)
            print(f"Created {filename}")
    
    # Create joker tiles
    joker_img = create_joker_tile(joker_face_path)
    joker1_path = os.path.join(OUTPUT_DIR, "tile_joker_1.png")
    joker2_path = os.path.join(OUTPUT_DIR, "tile_joker_2.png")
    joker_img.save(joker1_path)
    joker_img.save(joker2_path)
    all_tile_paths.append(joker1_path)
    all_tile_paths.append(joker2_path)
    print("Created joker tiles")
    
    # Create and save preview image
    preview_img = create_preview_image(all_tile_paths)
    preview_path = os.path.join(OUTPUT_DIR, "tiles_preview.png")
    preview_img.save(preview_path)
    print(f"Preview image saved to {preview_path}")
    
    print("All tiles generated successfully!")
    print(f"Tiles saved to {os.path.abspath(OUTPUT_DIR)}")

if __name__ == "__main__":
    main()