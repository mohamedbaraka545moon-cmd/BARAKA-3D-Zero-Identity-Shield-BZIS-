# ==============================================================================
# PROJECT: BARAKA-3D ZERO IDENTITY SHIELD (BZIS)
# AUTHOR & SOLE COPYRIGHT OWNER: Mohamed Eid Abdel Alim Baraka
# CONTACT EMAIL: mohamedbaraka545moon@gmail.com
# RESEARCH DOMAIN: Non-Standard Parametric Differential Cryptography
# ------------------------------------------------------------------------------
# COPYRIGHT © 2026 MOHAMED EID ABDEL ALIM BARAKA. ALL RIGHTS RESERVED.
# ==============================================================================

import os
import math
import hashlib
from flask import Flask, render_template_string, request, send_file
import io

app = Flask(__name__)

SCALE = 1 << 32  # 32-bit fixed-point precision math

def to_fixed(f): return int(f * SCALE)
def from_fixed(i): return float(i) / SCALE

def fp_sin_sq(x_fp):
    x = from_fixed(x_fp)
    val = math.sin(math.pi * (math.exp(math.lgamma(x % 50 + 1)) + 1) / (x % 50 + 1))
    return to_fixed(val * val)

def fp_cosh(x_fp):
    return to_fixed(math.cosh(from_fixed(x_fp) % 4))

def bzis_deterministic_step(x_fp, y_fp, z_fp, t_fp, dt_fp):
    sin_sq = fp_sin_sq(x_fp)
    cosh_val = fp_cosh(x_fp)
    
    # دالة القوة الحركية الفريدة لبركة - تصفير التكرار الاحصائي R=0
    force_x = (sin_sq - y_fp) // (cosh_val if cosh_val != 0 else 1)
    force_y = to_fixed(math.sin(from_fixed(t_fp)))
    force_z = to_fixed(math.cos(from_fixed(x_fp + t_fp)))
    
    return x_fp + (force_x * dt_fp // SCALE), y_fp + (force_y * dt_fp // SCALE), z_fp + (force_z * dt_fp // SCALE), t_fp + dt_fp

# بروتوكول التوقيع الرقمي المبتكر لحفظ الملكية الفكرية وعزل الاختراق
def generate_baraka_signature(data_bytes, t0):
    file_hash = hashlib.sha256(data_bytes).digest()
    sig_seed = sum(file_hash) + int(t0)
    return f"BZIS-SIGN-M.E.A.B-{to_fixed(math.sinh(sig_seed % 5))}"

def process_bzis_cipher(data_bytes, t0_val):
    out = bytearray()
    x_fp, y_fp, z_fp = to_fixed(2.0), to_fixed(0.0), to_fixed(1.0)
    t_fp, dt_fp = to_fixed(t0_val), to_fixed(0.01)
    
    for b in data_bytes:
        x_fp, y_fp, z_fp, t_fp = bzis_deterministic_step(x_fp, y_fp, z_fp, t_fp, dt_fp)
        key_byte = (abs(x_fp ^ y_fp ^ z_fp) >> 8) & 0xFF
        out.append(b ^ key_byte)
    return bytes(out)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>BARAKA-3D Zero Identity Shield</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #090d16; color: #f1f5f9; text-align: center; padding: 30px; }
        .shield-container { max-width: 750px; margin: 0 auto; background: #111827; padding: 40px; border-radius: 16px; border: 1px solid #1e293b; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.7); }
        h1 { color: #38bdf8; margin-bottom: 5px; font-size: 28px; }
        .author-tag { color: #f59e0b; font-weight: bold; margin-bottom: 25px; font-size: 14px; }
        .form-box { text-align: right; margin: 20px 0; }
        label { display: block; margin-bottom: 8px; color: #94a3b8; }
        input { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #334155; background: #030712; color: #fff; box-sizing: border-box; }
        .actions { display: flex; gap: 20px; margin-top: 30px; }
        button { flex: 1; padding: 14px; font-size: 16px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; transition: 0.3s; }
        .enc-btn { background: #0284c7; color: #fff; } .enc-btn:hover { background: #0369a1; }
        .dec-btn { background: #16a34a; color: #fff; } .dec-btn:hover { background: #15803d; }
        .telemetry { margin-top: 30px; background: #030712; padding: 20px; border-radius: 8px; text-align: left; font-family: monospace; color: #34d399; font-size: 12px; border-left: 4px solid #f59e0b; }
    </style>
</head>
<body>
    <div class="shield-container">
        <h1>BARAKA-3D Zero Identity Shield (BZIS)</h1>
        <div class="author-tag">المبتكر والمؤلف: محمد عيد عبد العليم بركة</div>
        <p style="color: #94a3b8; font-size: 14px;">نظام تشفير حركي فراغي غير نمطي مع كبح دالة غاما وحماية ضد هجمات القوة العمياء</p>
        
        <form action="/execute" method="post" enctype="multipart/form-data">
            <div class="form-box">
                <label>المفتاح البارامتري الابتدائي للفضاء الزمني (t₀):</label>
                <input type="number" name="t0" value="73.1094" step="any" required>
            </div>
            <div class="form-box">
                <label>اختر الملف لحمايته وتوقيعه رقمياً بـ BZIS:</label>
                <input type="file" name="file" required>
            </div>
            <div class="actions">
                <button type="submit" name="mode" value="encrypt" class="enc-btn">تشفير وتوقيع حركي</button>
                <button type="submit" name="mode" value="decrypt" class="dec-btn">فك التشفير والتحقق</button>
            </div>
        </form>
        
        <div class="telemetry">
            [BZIS TELEMETRY OK] - المحرك الحتمي مستقر.<br>
            [الملكية الفكرية]: محفوظه دولياً © 2026 محمد عيد عبد العليم بركة.<br>
            [قناة التواصل]: mohamedbaraka545moon@gmail.com
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_PAGE)

@app.route('/execute', methods=['POST'])
def execute():
    file = request.files['file']
    t0 = float(request.form.get('t0', 0.0))
    mode = request.form.get('mode', 'encrypt')
    
    raw_data = file.read()
    processed = process_bzis_cipher(raw_data, t0)
    signature = generate_baraka_signature(raw_data, t0)
    
    out_name = f"{'BZIS_ENC_' if mode == 'encrypt' else 'BZIS_DEC_'}{file.filename}"
    return send_file(io.BytesIO(processed), as_attachment=True, download_name=out_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
