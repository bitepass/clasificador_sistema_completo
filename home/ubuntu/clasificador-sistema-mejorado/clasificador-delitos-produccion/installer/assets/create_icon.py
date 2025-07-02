#!/usr/bin/env python3
"""
Generador de ícono DDIC-SM
Crea un ícono profesional basado en el logo: Base de datos + Lupa
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_ddic_icon():
    """Crea el ícono de DDIC-SM"""
    # Crear imagen base
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colores DDIC-SM
    db_color = '#1e3a8a'      # Azul marino para base de datos
    accent_color = '#3b82f6'  # Azul para detalles
    glass_color = '#6b7280'   # Gris para lupa
    handle_color = '#374151'  # Gris oscuro para mango
    
    # Dibujar base de datos (cilindros apilados)
    center_x = size // 2
    center_y = size // 2
    
    # Base de datos - 3 cilindros
    db_width = 100
    db_height = 25
    db_spacing = 30
    
    for i in range(3):
        y_pos = center_y - 30 + (i * db_spacing)
        
        # Cilindro superior (elipse)
        draw.ellipse([
            center_x - db_width//2, y_pos - db_height//2,
            center_x + db_width//2, y_pos + db_height//2
        ], fill=db_color, outline=accent_color, width=2)
        
        # Lado del cilindro
        if i < 2:  # No dibujar el lado del último cilindro
            draw.rectangle([
                center_x - db_width//2, y_pos,
                center_x + db_width//2, y_pos + db_spacing - 5
            ], fill=db_color, outline=accent_color, width=1)
    
    # Líneas de datos dentro de la base de datos
    for i in range(3):
        y_pos = center_y - 30 + (i * db_spacing)
        for j in range(3):
            line_y = y_pos - 8 + (j * 6)
            draw.line([
                center_x - db_width//3, line_y,
                center_x + db_width//3, line_y
            ], fill='white', width=2)
    
    # Dibujar lupa
    glass_radius = 35
    glass_x = center_x + 40
    glass_y = center_y - 40
    
    # Círculo de la lupa
    draw.ellipse([
        glass_x - glass_radius, glass_y - glass_radius,
        glass_x + glass_radius, glass_y + glass_radius
    ], fill=None, outline=glass_color, width=8)
    
    # Interior de la lupa (transparente)
    draw.ellipse([
        glass_x - glass_radius + 8, glass_y - glass_radius + 8,
        glass_x + glass_radius - 8, glass_y + glass_radius - 8
    ], fill=(255, 255, 255, 100), outline=None)
    
    # Mango de la lupa
    handle_start_x = glass_x + glass_radius - 15
    handle_start_y = glass_y + glass_radius - 15
    handle_end_x = glass_x + glass_radius + 25
    handle_end_y = glass_y + glass_radius + 25
    
    draw.line([
        handle_start_x, handle_start_y,
        handle_end_x, handle_end_y
    ], fill=handle_color, width=12)
    
    # Reflejo en la lupa
    draw.ellipse([
        glass_x - 15, glass_y - 15,
        glass_x + 5, glass_y + 5
    ], fill=(255, 255, 255, 150), outline=None)
    
    return img

def create_icon_sizes():
    """Crea el ícono en múltiples tamaños"""
    base_icon = create_ddic_icon()
    
    # Tamaños estándar para Windows
    sizes = [16, 24, 32, 48, 64, 128, 256]
    
    # Crear directorio si no existe
    os.makedirs('icons', exist_ok=True)
    
    # Guardar cada tamaño
    for size in sizes:
        resized = base_icon.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(f'icons/ddic_icon_{size}.png')
        print(f"✅ Ícono {size}x{size} creado")
    
    # Crear archivo .ico con múltiples tamaños
    try:
        base_icon.save('logo.ico', format='ICO', sizes=[(s, s) for s in sizes])
        print("✅ Archivo logo.ico creado con múltiples tamaños")
    except Exception as e:
        print(f"⚠️ Error creando .ico: {e}")
        # Fallback: usar solo el tamaño 256
        base_icon.save('logo.ico', format='ICO')
        print("✅ Archivo logo.ico creado (tamaño único)")
    
    # Crear también PNG principal
    base_icon.save('ddic_logo.png')
    print("✅ Logo principal ddic_logo.png creado")

if __name__ == "__main__":
    print("🎨 Generando ícono DDIC-SM...")
    print("📊 Base de datos + 🔍 Lupa")
    
    try:
        create_icon_sizes()
        print("\n🎉 ¡Ícono DDIC-SM generado exitosamente!")
        print("📁 Archivos creados:")
        print("   - logo.ico (para instalador)")
        print("   - ddic_logo.png (logo principal)")
        print("   - icons/ (múltiples tamaños)")
    except ImportError:
        print("❌ Error: Se requiere Pillow")
        print("💡 Instalar con: pip install Pillow")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")