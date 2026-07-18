from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

class AxiomHiveImageProcessor:
    """
    Functional image processing utility for AxiomHive.
    Implements precise branding, editorial color grading, and typography overlays.
    """

    def __init__(self, source_path):
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source image not found: {source_path}")
        self.source_path = source_path
        self.img = Image.open(source_path).convert("RGB")
        self.W, self.H = self.img.size

    def apply_editorial_grade(self):
        """Applies a professional S-curve contrast and color balance."""
        arr = np.array(self.img, dtype=np.float32) / 255.0
        
        # Lift shadows (Gamma adjustment)
        arr = np.power(arr, 0.92)
        
        # Subtle warmth (Adjust R and B channels)
        arr[:, :, 0] = np.clip(arr[:, :, 0] * 1.04, 0, 1)
        arr[:, :, 2] = np.clip(arr[:, :, 2] * 0.96, 0, 1)
        
        # Contrast S-curve
        def s_curve(x, strength=0.08):
            return x + strength * np.sin(np.pi * x) * (1 - x) * x * 4
        
        arr = s_curve(arr)
        arr = np.clip(arr * 255, 0, 255).astype(np.uint8)
        self.img = Image.fromarray(arr)
        return self

    def add_branding(self, brand_text="AXIOMHIVE", logo_color=(28, 28, 28)):
        """Renders high-quality typography overlays."""
        draw = ImageDraw.Draw(self.img)
        
        # Font selection
        font_candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        ]
        font_path = next((fp for fp in font_candidates if os.path.exists(fp)), None)
        
        logo_font_size = int(self.W * 0.085)
        if font_path:
            logo_font = ImageFont.truetype(font_path, logo_font_size)
        else:
            logo_font = ImageFont.load_default()

        letter_spacing = int(logo_font_size * 0.22)
        
        # Measure total width with spacing
        total_width = 0
        char_widths = []
        for ch in brand_text:
            bbox = draw.textbbox((0, 0), ch, font=logo_font)
            w = bbox[2] - bbox[0]
            char_widths.append(w)
            total_width += w
        total_width += letter_spacing * (len(brand_text) - 1)

        # Position: Top Center
        x_cursor = (self.W - total_width) // 2
        y_pos = int(self.H * 0.05)

        for i, ch in enumerate(brand_text):
            draw.text((x_cursor, y_pos), ch, font=logo_font, fill=logo_color)
            x_cursor += char_widths[i] + letter_spacing
            
        return self

    def save(self, output_path, quality=95):
        self.img.save(output_path, "JPEG", quality=quality)
        print(f"Saved processed image to: {output_path}")

if __name__ == "__main__":
    # Example usage for verification
    # processor = AxiomHiveImageProcessor("input.jpg")
    # processor.apply_editorial_grade().add_branding().save("output.jpg")
    pass
