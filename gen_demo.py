#!/usr/bin/env python3
"""Generate demo video for SentinelAI."""

from PIL import Image, ImageDraw, ImageFont
import subprocess
import os

WIDTH, HEIGHT = 1280, 720
FPS = 15
DURATION = 10  # seconds
TOTAL_FRAMES = FPS * DURATION

def create_frame(frame_num):
    """Create a single frame of the demo video."""
    img = Image.new('RGB', (WIDTH, HEIGHT), '#0a0a0f')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_med = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        font_xs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        font = ImageFont.load_default()
        font_med = font
        font_sm = font
        font_xs = font
    
    # Header
    draw.rectangle([(0, 0), (WIDTH, 80)], fill='#1a1a2e')
    draw.text((30, 20), "🛡️ SentinelAI", fill='#6366F1', font=font)
    draw.text((WIDTH-200, 30), "v2.0.0", fill='#6B7280', font=font_sm)
    
    # Progress bar
    progress = frame_num / TOTAL_FRAMES
    draw.rectangle([(0, 78), (int(WIDTH * progress), 82)], fill='#6366F1')
    
    # Stats cards
    y = 100
    cards = [
        ("TOTAL SCANS", f"{1247 + frame_num * 10:,}", "+47 today", "#6366F1"),
        ("VULNS FOUND", f"{8934 + frame_num * 5:,}", "234 critical", "#EF4444"),
        ("SECURITY SCORE", f"{72.4 + frame_num * 0.1:.1f}%", "+3.2% vs last month", "#22C55E"),
        ("LINES SCANNED", f"{2_847_391 + frame_num * 1000:,}", "45,678 files", "#3B82F6"),
    ]
    
    card_width = (WIDTH - 80) // 4
    for i, (label, value, sub, color) in enumerate(cards):
        x = 20 + i * (card_width + 20)
        draw.rectangle([(x, y), (x + card_width, y + 120)], fill='#1a1a2e', outline='#374151')
        draw.text((x + 15, y + 10), label, fill='#9CA3AF', font=font_xs)
        draw.text((x + 15, y + 35), value, fill=color, font=font_med)
        draw.text((x + 15, y + 75), sub, fill='#6B7280', font=font_xs)
    
    # Agents section
    y = 240
    draw.text((20, y), "Security Agents", fill='white', font=font_med)
    y += 45
    
    agents = [
        ("StaticAnalyzer", "Pattern-based vuln detection", "2,341", "active"),
        ("VulnDetector", "AI-powered (MiMo v2.5-pro)", "1,876", "active"),
        ("CodeQuality", "Complexity & duplication", "1,567", "active"),
        ("DependencyChecker", "CVE scanning", "1,234", "active"),
        ("SecretsScanner", "Hardcoded secrets", "916", "active"),
    ]
    
    for i, (name, desc, findings, status) in enumerate(agents):
        x = 20 + (i % 3) * 420
        y2 = y + (i // 3) * 80
        draw.rectangle([(x, y2), (x + 400, y2 + 70)], fill='#1a1a2e', outline='#374151')
        draw.text((x + 10, y2 + 5), name, fill='#6366F1', font=font_sm)
        draw.text((x + 10, y2 + 30), desc, fill='#9CA3AF', font=font_xs)
        draw.text((x + 300, y2 + 5), findings, fill='white', font=font_sm)
        draw.text((x + 300, y2 + 30), status, fill='#22C55E', font=font_xs)
    
    # Recent scans table
    y += 180
    draw.text((20, y), "Recent Scans", fill='white', font=font_med)
    y += 40
    
    headers = ["SCAN ID", "TARGET", "FINDINGS", "SCORE", "STATUS"]
    col_widths = [180, 200, 120, 120, 120]
    x = 20
    for header, w in zip(headers, col_widths):
        draw.text((x, y), header, fill='#9CA3AF', font=font_xs)
        x += w
    
    y += 25
    scans = [
        ("SCAN-001247", "web-app-frontend", "23", "78.5%", "completed"),
        ("SCAN-001246", "api-gateway", "15", "82.3%", "completed"),
        ("SCAN-001245", "auth-service", "8", "91.2%", "completed"),
        ("SCAN-001244", "data-pipeline", "31", "65.4%", "completed"),
        ("SCAN-001243", "mobile-backend", "12", "87.9%", "completed"),
    ]
    
    for scan_id, target, findings, score, status in scans:
        x = 20
        row_data = [scan_id, target, findings, score, status]
        for val, w in zip(row_data, col_widths):
            color = '#6366F1' if val == scan_id else '#E5E7EB'
            if val == "completed":
                color = '#22C55E'
            elif "%" in val:
                score_val = float(val.replace("%", ""))
                color = '#22C55E' if score_val >= 80 else '#EAB308' if score_val >= 60 else '#EF4444'
            draw.text((x, y), val, fill=color, font=font_xs)
            x += w
        y += 22
    
    # Severity distribution
    y += 20
    draw.rectangle([(20, y), (WIDTH-20, y + 100)], fill='#1a1a2e', outline='#6366F1')
    draw.text((40, y + 10), "Severity Distribution", fill='#6366F1', font=font_med)
    draw.text((40, y + 50), "Critical: 234", fill='#EF4444', font=font_sm)
    draw.text((250, y + 50), "High: 567", fill='#F97316', font=font_sm)
    draw.text((450, y + 50), "Medium: 1,234", fill='#EAB308', font=font_sm)
    draw.text((650, y + 50), "Low: 2,345", fill='#22C55E', font=font_sm)
    
    # Footer
    draw.rectangle([(0, HEIGHT-40), (WIDTH, HEIGHT)], fill='#1a1a2e')
    draw.text((20, HEIGHT-30), "SentinelAI v2.0.0 — Powered by MiMo", fill='#6B7280', font=font_xs)
    
    return img

def main():
    """Generate the demo video."""
    os.makedirs('/root/sentinai/screenshots', exist_ok=True)
    
    # Generate frames
    frames = []
    for i in range(TOTAL_FRAMES):
        frame = create_frame(i)
        frame_path = f'/tmp/frame_{i:04d}.png'
        frame.save(frame_path)
        frames.append(frame_path)
    
    # Create video with ffmpeg
    cmd = [
        'ffmpeg', '-y',
        '-framerate', str(FPS),
        '-i', '/tmp/frame_%04d.png',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-crf', '23',
        '/root/sentinai/screenshots/demo.mp4'
    ]
    subprocess.run(cmd, check=True)
    
    # Cleanup
    for f in frames:
        os.remove(f)
    
    print("✅ Demo video created: /root/sentinai/screenshots/demo.mp4")

if __name__ == "__main__":
    main()
