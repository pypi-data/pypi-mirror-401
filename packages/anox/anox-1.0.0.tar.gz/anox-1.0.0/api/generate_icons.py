#!/usr/bin/env python3
"""
Generate placeholder PWA icons for AXON.
This creates simple SVG-based PNG icons in various sizes.
For production, replace with proper designed icons.
"""

import os
from pathlib import Path

# Icon sizes needed for PWA
ICON_SIZES = [16, 32, 72, 96, 128, 144, 152, 180, 192, 384, 512]

# Icon directory
ICON_DIR = Path(__file__).parent / "static" / "icons"
ICON_DIR.mkdir(parents=True, exist_ok=True)

# SVG template for AXON logo
SVG_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="{size}" height="{size}" fill="#0a0e27" rx="{radius}"/>
  
  <!-- Lightning bolt icon -->
  <g transform="translate({size}/2, {size}/2)">
    <path d="M-{s1} -{s2} L{s3} -{s4} L-{s5} {s6} L{s7} {s8} L-{s9} {s10} L{s11} -{s12} Z" 
          fill="#00d4ff" 
          stroke="#00b8e6" 
          stroke-width="{stroke}"/>
  </g>
  
  <!-- Text (for larger icons) -->
  {text}
</svg>
"""

def generate_icon(size: int) -> str:
    """Generate SVG content for given size."""
    # Calculate proportional values
    radius = size * 0.15
    stroke = max(1, size * 0.01)
    
    # Lightning bolt coordinates (proportional to size)
    scale = size * 0.015
    s1, s2 = scale * 8, scale * 15
    s3, s4 = scale * 3, scale * 2
    s5, s6 = scale * 2, scale * 5
    s7, s8 = scale * 15, scale * 8
    s9, s10 = scale * 5, scale * 15
    s11, s12 = scale * 10, scale * 5
    
    # Add text for larger icons
    text = ""
    if size >= 192:
        font_size = size * 0.12
        text = f'<text x="{size/2}" y="{size * 0.85}" text-anchor="middle" fill="#00d4ff" font-family="Arial, sans-serif" font-weight="bold" font-size="{font_size}">AXON</text>'
    
    return SVG_TEMPLATE.format(
        size=size,
        radius=radius,
        stroke=stroke,
        s1=s1, s2=s2, s3=s3, s4=s4, s5=s5,
        s6=s6, s7=s7, s8=s8, s9=s9, s10=s10,
        s11=s11, s12=s12,
        text=text
    )

def create_icons():
    """Create all icon sizes."""
    print("🎨 Generating PWA icons for AXON...")
    
    # Check if PIL/Pillow is available for PNG conversion
    try:
        from PIL import Image
        import io
        has_pil = True
    except ImportError:
        has_pil = False
        print("⚠️  PIL/Pillow not available. Installing...")
        import subprocess
        try:
            subprocess.check_call([
                "pip", "install", "--quiet", "Pillow", "cairosvg"
            ])
            from PIL import Image
            import io
            has_pil = True
            print("✅ PIL/Pillow installed successfully")
        except Exception as e:
            print(f"❌ Could not install PIL/Pillow: {e}")
            print("📝 Creating SVG icons only. Install Pillow for PNG icons.")
    
    success_count = 0
    
    for size in ICON_SIZES:
        svg_content = generate_icon(size)
        
        # Save as SVG (always works)
        svg_path = ICON_DIR / f"icon-{size}x{size}.svg"
        with open(svg_path, 'w') as f:
            f.write(svg_content)
        print(f"✓ Created {svg_path.name}")
        
        # Try to convert to PNG
        if has_pil:
            try:
                # Try using cairosvg for better quality
                try:
                    import cairosvg
                    png_data = cairosvg.svg2png(
                        bytestring=svg_content.encode('utf-8'),
                        output_width=size,
                        output_height=size
                    )
                    png_path = ICON_DIR / f"icon-{size}x{size}.png"
                    with open(png_path, 'wb') as f:
                        f.write(png_data)
                    print(f"✓ Created {png_path.name}")
                    success_count += 1
                except ImportError:
                    # Fallback: create a simple colored square
                    from PIL import Image, ImageDraw, ImageFont
                    img = Image.new('RGBA', (size, size), (10, 14, 39, 255))
                    draw = ImageDraw.Draw(img)
                    
                    # Draw lightning bolt shape
                    points = [
                        (size*0.35, size*0.15),
                        (size*0.55, size*0.45),
                        (size*0.45, size*0.45),
                        (size*0.65, size*0.85),
                        (size*0.40, size*0.55),
                        (size*0.50, size*0.55),
                    ]
                    draw.polygon(points, fill=(0, 212, 255, 255), outline=(0, 184, 230, 255))
                    
                    # Save PNG
                    png_path = ICON_DIR / f"icon-{size}x{size}.png"
                    img.save(png_path, 'PNG')
                    print(f"✓ Created {png_path.name} (basic)")
                    success_count += 1
            except Exception as e:
                print(f"⚠️  Could not create PNG for {size}x{size}: {e}")
    
    # Create additional icon variants
    if has_pil:
        try:
            from PIL import Image, ImageDraw
            
            # Create chat icon
            img = Image.new('RGBA', (96, 96), (10, 14, 39, 255))
            draw = ImageDraw.Draw(img)
            draw.ellipse([10, 10, 86, 86], fill=(0, 212, 255, 255))
            draw.text((48, 48), "💬", anchor="mm")
            img.save(ICON_DIR / "icon-chat.png", 'PNG')
            
            # Create code icon
            img = Image.new('RGBA', (96, 96), (10, 14, 39, 255))
            draw = ImageDraw.Draw(img)
            draw.ellipse([10, 10, 86, 86], fill=(0, 212, 255, 255))
            draw.text((48, 48), "📝", anchor="mm")
            img.save(ICON_DIR / "icon-code.png", 'PNG')
            
            # Create files icon
            img = Image.new('RGBA', (96, 96), (10, 14, 39, 255))
            draw = ImageDraw.Draw(img)
            draw.ellipse([10, 10, 86, 86], fill=(0, 212, 255, 255))
            draw.text((48, 48), "📁", anchor="mm")
            img.save(ICON_DIR / "icon-files.png", 'PNG')
            
            print("✓ Created action icons")
        except Exception as e:
            print(f"⚠️  Could not create action icons: {e}")
    
    print(f"\n✅ Generated {len(ICON_SIZES)} icon sizes")
    if success_count > 0:
        print(f"✅ Created {success_count} PNG icons")
    print(f"📁 Icons saved to: {ICON_DIR}")
    print("\n💡 For production, replace these with professionally designed icons.")

if __name__ == "__main__":
    create_icons()
