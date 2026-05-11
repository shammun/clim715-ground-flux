"""Build Lecture_Master_Guide.html with Chapter 0 prereqs + inline widgets prepended."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import markdown

# Read base content
with open("Lecture_Master_Guide.md", "r", encoding="utf-8") as f:
    base_md = f.read()
with open("chapter0_prereqs.md", "r", encoding="utf-8") as f:
    chapter0 = f.read()

# Find the position in base_md AFTER the TOC and "---" separator before Chapter 1.
# Look for "## 1. Big-Picture Orientation" and insert Chapter 0 before it.
ch1_idx = base_md.find("## 1. Big-Picture")
if ch1_idx == -1:
    # Fall back: insert near top
    ch1_idx = base_md.find("---", 100) + 4
md_text = base_md[:ch1_idx] + chapter0 + "\n\n" + base_md[ch1_idx:]

# Strip § characters
md_text = re.sub(r"§(\d+)(\.\d+)?", r"Section \1\2", md_text)
md_text = re.sub(r"§(\w)", r"Section \1", md_text)

# ============================================================
# Widget definitions (inline HTML+CSS+JS)
# ============================================================

WIDGETS = {}

# ---------- 1. Derivative / tangent-line widget ----------
WIDGETS["derivative_tangent"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · Derivative as the slope of a tangent line</div>
  <div class="cw-body">
    <svg id="cw_deriv_svg" viewBox="0 0 540 320" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>x₀</label>
      <input type="range" id="cw_deriv_x" min="-200" max="200" value="50" oninput="cwDerivDraw()">
      <span id="cw_deriv_val" style="min-width:140px;display:inline-block">x₀ = 0.5, slope = 1.000</span>
    </div>
    <div class="cw-note">The blue curve is f(x) = sin(x) + 0.4·x. The orange tangent line touches it at x₀; its slope IS the derivative f'(x₀) at that point. Slide x₀ along the curve and watch the tangent rotate.</div>
  </div>
</div>
<script>
function cwDerivDraw(){
  var svg = document.getElementById("cw_deriv_svg");
  if(!svg) return;
  var x0 = document.getElementById("cw_deriv_x").value/100;
  var w = 540, h = 320, mx = 30;
  // map x in [-2, 2] -> [mx, w-mx]
  function X(x){ return mx + (x+2)/4 * (w-2*mx); }
  function Y(y){ return h/2 - y*60; }
  var f = function(x){ return Math.sin(x) + 0.4*x; };
  var fp = function(x){ return Math.cos(x) + 0.4; };
  var pts = "";
  for(var i=0;i<=200;i++){
    var x = -2 + i*4/200;
    pts += (i===0?"M":"L") + X(x) + "," + Y(f(x)) + " ";
  }
  var s = fp(x0);
  var tx1 = x0 - 1.3, tx2 = x0 + 1.3;
  var ty1 = f(x0) + s*(tx1-x0), ty2 = f(x0) + s*(tx2-x0);
  svg.innerHTML =
    '<rect width="540" height="320" fill="#fafbff" rx="6"/>' +
    '<line x1="'+mx+'" y1="'+(h/2)+'" x2="'+(w-mx)+'" y2="'+(h/2)+'" stroke="#94a3b8" stroke-width="1"/>' +
    '<line x1="'+(w/2)+'" y1="20" x2="'+(w/2)+'" y2="'+(h-20)+'" stroke="#94a3b8" stroke-width="1"/>' +
    '<path d="'+pts+'" stroke="#6b5cb5" stroke-width="2.4" fill="none"/>' +
    '<line x1="'+X(tx1)+'" y1="'+Y(ty1)+'" x2="'+X(tx2)+'" y2="'+Y(ty2)+'" stroke="#ee845b" stroke-width="2.4"/>' +
    '<circle cx="'+X(x0)+'" cy="'+Y(f(x0))+'" r="6" fill="#ee845b" stroke="#fff" stroke-width="2"/>' +
    '<text x="20" y="20" font-size="11" fill="#475569">y = sin(x) + 0.4x</text>';
  document.getElementById("cw_deriv_val").textContent = "x₀ = " + x0.toFixed(2) + ", slope f'(x₀) = " + s.toFixed(3);
}
window.addEventListener("DOMContentLoaded", cwDerivDraw);
</script>
"""

# ---------- 2. Euler's formula unit circle ----------
WIDGETS["euler_unit_circle"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · Euler's formula e^(iθ) = cos θ + i sin θ on the unit circle</div>
  <div class="cw-body">
    <svg id="cw_euler_svg" viewBox="0 0 540 320" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>θ (radians)</label>
      <input type="range" id="cw_euler_th" min="0" max="628" value="120" oninput="cwEulerDraw()">
      <span id="cw_euler_val" style="min-width:240px;display:inline-block"></span>
    </div>
    <div class="cw-note">The point traces the unit circle at angle θ. Its horizontal coordinate is cos θ (orange, plotted below right); its vertical coordinate is sin θ (purple, plotted on the right axis). Together they ARE the real and imaginary parts of e^(iθ).</div>
  </div>
</div>
<script>
function cwEulerDraw(){
  var svg = document.getElementById("cw_euler_svg");
  if(!svg) return;
  var th = document.getElementById("cw_euler_th").value/100;
  var cx = 110, cy = 160, r = 90;
  var px = cx + r*Math.cos(th), py = cy - r*Math.sin(th);
  // sin trace on right side
  var sinPath = "";
  for(var i=0;i<=Math.floor(th*40);i++){
    var t = i/40;
    var xx = 240 + t*30;
    var yy = cy - r*Math.sin(t);
    sinPath += (i===0?"M":"L") + xx + "," + yy + " ";
  }
  var cosPath = "";
  for(var i=0;i<=Math.floor(th*40);i++){
    var t = i/40;
    var xx = 240 + t*30;
    var yy = 290 - r*Math.cos(t)*0.5;
    cosPath += (i===0?"M":"L") + xx + "," + yy + " ";
  }
  svg.innerHTML =
    '<rect width="540" height="320" fill="#fafbff" rx="6"/>' +
    '<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="#cbd5e1" stroke-width="1.5"/>' +
    '<line x1="'+(cx-r-10)+'" y1="'+cy+'" x2="'+(cx+r+10)+'" y2="'+cy+'" stroke="#94a3b8"/>' +
    '<line x1="'+cx+'" y1="'+(cy-r-10)+'" x2="'+cx+'" y2="'+(cy+r+10)+'" stroke="#94a3b8"/>' +
    '<line x1="'+cx+'" y1="'+cy+'" x2="'+px+'" y2="'+py+'" stroke="#2c3142" stroke-width="2"/>' +
    '<line x1="'+px+'" y1="'+py+'" x2="'+px+'" y2="'+cy+'" stroke="#ee845b" stroke-width="2" stroke-dasharray="4 3"/>' +
    '<line x1="'+px+'" y1="'+py+'" x2="'+cx+'" y2="'+py+'" stroke="#6b5cb5" stroke-width="2" stroke-dasharray="4 3"/>' +
    '<circle cx="'+px+'" cy="'+py+'" r="6" fill="#2c8a83" stroke="#fff" stroke-width="2"/>' +
    '<text x="'+(cx-110)+'" y="20" font-size="11" fill="#475569">complex plane (unit circle)</text>' +
    '<text x="240" y="20" font-size="11" fill="#6b5cb5">sin θ as θ increases →</text>' +
    '<text x="240" y="200" font-size="11" fill="#ee845b">cos θ as θ increases →</text>' +
    '<line x1="240" y1="50" x2="540" y2="50" stroke="#cbd5e1" stroke-dasharray="2 2"/>' +
    '<line x1="240" y1="160" x2="540" y2="160" stroke="#94a3b8"/>' +
    '<path d="'+sinPath+'" stroke="#6b5cb5" stroke-width="2.5" fill="none"/>' +
    '<line x1="240" y1="245" x2="540" y2="245" stroke="#94a3b8"/>' +
    '<path d="'+cosPath+'" stroke="#ee845b" stroke-width="2.5" fill="none"/>';
  document.getElementById("cw_euler_val").textContent =
    "θ = " + th.toFixed(2) + " rad,  cos θ = " + Math.cos(th).toFixed(3) + ",  sin θ = " + Math.sin(th).toFixed(3);
}
window.addEventListener("DOMContentLoaded", cwEulerDraw);
</script>
"""

# ---------- 3. Sine wave explorer ----------
WIDGETS["sine_explorer"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · Sine wave explorer: A sin(k x − ω t)</div>
  <div class="cw-body">
    <svg id="cw_sine_svg" viewBox="0 0 540 240" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>A</label><input type="range" id="cw_sine_A" min="20" max="100" value="60" oninput="cwSineDraw()"><span id="cw_sine_Av">0.6</span>
    </div>
    <div class="cw-ctrl">
      <label>k</label><input type="range" id="cw_sine_k" min="100" max="2000" value="500" oninput="cwSineDraw()"><span id="cw_sine_kv">5.0 rad/m</span>
    </div>
    <div class="cw-ctrl">
      <label>ω</label><input type="range" id="cw_sine_w" min="50" max="500" value="150" oninput="cwSineDraw()"><span id="cw_sine_wv">1.5 rad/s</span>
    </div>
    <div class="cw-ctrl">
      <label>t</label><input type="range" id="cw_sine_t" min="0" max="600" value="0" oninput="cwSineDraw()"><span id="cw_sine_tv">0.0 s</span>
      <button onclick="cwSineAnim()" id="cw_sine_btn" style="margin-left:10px;padding:4px 12px;background:#ee845b;color:#fff;border:none;border-radius:4px;cursor:pointer">Play</button>
    </div>
    <div class="cw-note">A is amplitude. k is wavenumber (radians per metre). ω is angular frequency (radians per second). Slide t to move the wave; click Play to animate. Notice wavelength λ = 2π/k and period T = 2π/ω; the wave moves at speed c = ω/k.</div>
  </div>
</div>
<script>
var cwSineTimer = null;
function cwSineDraw(){
  var svg = document.getElementById("cw_sine_svg"); if(!svg) return;
  var A = document.getElementById("cw_sine_A").value/100;
  var k = document.getElementById("cw_sine_k").value/100;
  var w = document.getElementById("cw_sine_w").value/100;
  var t = document.getElementById("cw_sine_t").value/100;
  document.getElementById("cw_sine_Av").textContent = A.toFixed(2);
  document.getElementById("cw_sine_kv").textContent = k.toFixed(1) + " rad/m (λ=" + (2*Math.PI/k).toFixed(2) + " m)";
  document.getElementById("cw_sine_wv").textContent = w.toFixed(1) + " rad/s (T=" + (2*Math.PI/w).toFixed(2) + " s)";
  document.getElementById("cw_sine_tv").textContent = t.toFixed(2) + " s";
  var W = 540, H = 240, mx = 30;
  var pts = "";
  for(var i=0;i<=540;i++){
    var x = i*4/540;
    var y = A*Math.sin(k*x - w*t);
    pts += (i===0?"M":"L") + (mx + i*(W-2*mx)/540) + "," + (H/2 - y*80) + " ";
  }
  svg.innerHTML =
    '<rect width="540" height="240" fill="#fafbff" rx="6"/>' +
    '<line x1="'+mx+'" y1="'+(H/2)+'" x2="'+(W-mx)+'" y2="'+(H/2)+'" stroke="#94a3b8"/>' +
    '<path d="'+pts+'" stroke="#6b5cb5" stroke-width="2.5" fill="none"/>' +
    '<text x="20" y="20" font-size="11" fill="#475569">x (metres) →</text>' +
    '<text x="450" y="20" font-size="11" fill="#475569">wave speed c = ω/k = ' + (w/k).toFixed(2) + ' m/s</text>';
}
function cwSineAnim(){
  var btn = document.getElementById("cw_sine_btn");
  if(cwSineTimer){ clearInterval(cwSineTimer); cwSineTimer = null; btn.textContent="Play"; return; }
  btn.textContent="Pause";
  cwSineTimer = setInterval(function(){
    var sl = document.getElementById("cw_sine_t");
    var v = (parseInt(sl.value) + 8) % 601;
    sl.value = v; cwSineDraw();
  }, 50);
}
window.addEventListener("DOMContentLoaded", cwSineDraw);
</script>
"""

# ---------- 4. k·Δz on a grid ----------
WIDGETS["kdz_grid"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · k Δz on a uniform grid — wavelengths the grid can hold</div>
  <div class="cw-body">
    <svg id="cw_kdz_svg" viewBox="0 0 540 260" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>k Δz</label>
      <input type="range" id="cw_kdz_v" min="0" max="314" value="100" oninput="cwKdzDraw()">
      <span id="cw_kdz_val" style="min-width:240px;display:inline-block"></span>
    </div>
    <div class="cw-note">The grid has 20 cells of size Δz; cell centres are the purple dots. The blue curve is sin(k z); coloured dots mark the value the grid samples at each cell centre. At k Δz = π (the rightmost slider position) the wave alternates sign at every grid point — the worst-case "2 Δz wave" that drives von-Neumann stability analysis.</div>
  </div>
</div>
<script>
function cwKdzDraw(){
  var svg = document.getElementById("cw_kdz_svg"); if(!svg) return;
  var kdz = document.getElementById("cw_kdz_v").value/100;
  var W = 540, H = 260, mx = 30, my = 40;
  var N = 20, dz = (W - 2*mx) / N;
  var pts = "";
  for(var i=0;i<=540;i++){
    var z = i;
    var y = Math.sin(kdz * z / dz);
    pts += (i===0?"M":"L") + (mx + i*(W-2*mx)/540) + "," + (H/2 - y*70) + " ";
  }
  var dots = "";
  for(var j=0;j<=N;j++){
    var cx = mx + j*dz;
    var v = Math.sin(kdz * j);
    var col = v >= 0 ? "#ee845b" : "#6b5cb5";
    dots += '<circle cx="'+cx+'" cy="'+(H/2 - v*70)+'" r="5" fill="'+col+'" stroke="#fff" stroke-width="1.5"/>';
    dots += '<line x1="'+cx+'" y1="'+(H-20)+'" x2="'+cx+'" y2="'+(H-30)+'" stroke="#94a3b8"/>';
  }
  svg.innerHTML =
    '<rect width="540" height="260" fill="#fafbff" rx="6"/>' +
    '<line x1="'+mx+'" y1="'+(H/2)+'" x2="'+(W-mx)+'" y2="'+(H/2)+'" stroke="#94a3b8"/>' +
    '<line x1="'+mx+'" y1="'+(H-25)+'" x2="'+(W-mx)+'" y2="'+(H-25)+'" stroke="#94a3b8"/>' +
    '<path d="'+pts+'" stroke="#cbd5e1" stroke-width="2" fill="none"/>' +
    dots +
    '<text x="20" y="20" font-size="11" fill="#475569">sin(k z) sampled at 20 grid cells (Δz spacing)</text>';
  var lam = 2*Math.PI / Math.max(kdz, 1e-4);
  var label;
  if(kdz < 0.05) label = "k Δz ≈ 0 — wavelength much longer than the grid";
  else if(Math.abs(kdz - Math.PI/2) < 0.1) label = "k Δz = π/2 — four cells per wavelength";
  else if(Math.abs(kdz - Math.PI) < 0.1) label = "k Δz ≈ π — the 2Δz wave (worst case)";
  else label = "λ/Δz = " + lam.toFixed(2) + " (cells per wavelength)";
  document.getElementById("cw_kdz_val").textContent = "k Δz = " + kdz.toFixed(2) + " — " + label;
}
window.addEventListener("DOMContentLoaded", cwKdzDraw);
</script>
"""

# ---------- 5. Time step visualizer ----------
WIDGETS["time_step"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · Time discretisation: continuous time vs. discrete time steps</div>
  <div class="cw-body">
    <svg id="cw_ts_svg" viewBox="0 0 540 220" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>Δt</label>
      <input type="range" id="cw_ts_dt" min="20" max="200" value="50" oninput="cwTsDraw()">
      <span id="cw_ts_val" style="min-width:240px;display:inline-block"></span>
    </div>
    <div class="cw-note">A smooth signal (blue) is sampled at discrete times t_n = n Δt (orange dots). As Δt grows, the discrete samples capture less and less of the smooth signal. The discrete time-derivative (φⁿ⁺¹ − φⁿ)/Δt approximates the true continuous derivative, with truncation error of order Δt.</div>
  </div>
</div>
<script>
function cwTsDraw(){
  var svg = document.getElementById("cw_ts_svg"); if(!svg) return;
  var dt = document.getElementById("cw_ts_dt").value/100;
  var W = 540, H = 220, mx = 30;
  var T = 4;
  var pts = "";
  for(var i=0;i<=540;i++){
    var t = i*T/540;
    var y = Math.sin(2*t) + 0.5*Math.sin(5*t);
    pts += (i===0?"M":"L") + (mx + i*(W-2*mx)/540) + "," + (H/2 - y*50) + " ";
  }
  var dots = "";
  var n = 0;
  for(var tt = 0; tt <= T; tt += dt){
    var cx = mx + tt/T * (W-2*mx);
    var y = Math.sin(2*tt) + 0.5*Math.sin(5*tt);
    dots += '<line x1="'+cx+'" y1="'+(H-25)+'" x2="'+cx+'" y2="'+(H/2 - y*50)+'" stroke="#cbd5e1" stroke-dasharray="2 2"/>';
    dots += '<circle cx="'+cx+'" cy="'+(H/2 - y*50)+'" r="5" fill="#ee845b" stroke="#fff" stroke-width="1.5"/>';
    dots += '<text x="'+cx+'" y="'+(H-8)+'" text-anchor="middle" font-size="10" fill="#475569">n='+n+'</text>';
    n++;
  }
  svg.innerHTML =
    '<rect width="540" height="220" fill="#fafbff" rx="6"/>' +
    '<line x1="'+mx+'" y1="'+(H/2)+'" x2="'+(W-mx)+'" y2="'+(H/2)+'" stroke="#94a3b8"/>' +
    '<line x1="'+mx+'" y1="'+(H-25)+'" x2="'+(W-mx)+'" y2="'+(H-25)+'" stroke="#94a3b8"/>' +
    '<path d="'+pts+'" stroke="#6b5cb5" stroke-width="2" fill="none"/>' +
    dots +
    '<text x="20" y="20" font-size="11" fill="#475569">smooth signal φ(t)</text>' +
    '<text x="380" y="20" font-size="11" fill="#ee845b">discrete samples φⁿ at t = n Δt</text>';
  document.getElementById("cw_ts_val").textContent =
    "Δt = " + dt.toFixed(2) + " s,  number of samples = " + (Math.floor(T/dt)+1);
}
window.addEventListener("DOMContentLoaded", cwTsDraw);
</script>
"""

# ---------- 6. Fourier square wave builder ----------
WIDGETS["fourier_square"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · Fourier series: a square wave as a sum of sines</div>
  <div class="cw-body">
    <svg id="cw_four_svg" viewBox="0 0 540 240" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>Number of harmonics</label>
      <input type="range" id="cw_four_n" min="1" max="30" value="1" oninput="cwFourDraw()">
      <span id="cw_four_val" style="min-width:120px;display:inline-block">N = 1</span>
    </div>
    <div class="cw-note">The Fourier series for a square wave is (4/π) [sin(x) + (1/3) sin(3x) + (1/5) sin(5x) + …]. Slide the number of harmonics up to see the approximation sharpen. The little overshoot that never goes away near the jumps is the Gibbs phenomenon — a famous quirk of Fourier series at discontinuities.</div>
  </div>
</div>
<script>
function cwFourDraw(){
  var svg = document.getElementById("cw_four_svg"); if(!svg) return;
  var N = parseInt(document.getElementById("cw_four_n").value);
  document.getElementById("cw_four_val").textContent = "N = " + N;
  var W = 540, H = 240, mx = 30;
  // ideal square wave
  var sq = "";
  for(var i=0;i<=540;i++){
    var x = i*Math.PI*2/540;
    var y = (x < Math.PI) ? 1 : -1;
    sq += (i===0?"M":"L") + (mx + i*(W-2*mx)/540) + "," + (H/2 - y*70) + " ";
  }
  // partial sum
  var ps = "";
  for(var i=0;i<=540;i++){
    var x = i*Math.PI*2/540;
    var s = 0;
    for(var k=1;k<=2*N-1;k+=2){ s += Math.sin(k*x)/k; }
    s *= 4/Math.PI;
    ps += (i===0?"M":"L") + (mx + i*(W-2*mx)/540) + "," + (H/2 - s*70) + " ";
  }
  svg.innerHTML =
    '<rect width="540" height="240" fill="#fafbff" rx="6"/>' +
    '<line x1="'+mx+'" y1="'+(H/2)+'" x2="'+(W-mx)+'" y2="'+(H/2)+'" stroke="#94a3b8"/>' +
    '<path d="'+sq+'" stroke="#cbd5e1" stroke-width="2" fill="none"/>' +
    '<path d="'+ps+'" stroke="#6b5cb5" stroke-width="2.5" fill="none"/>' +
    '<text x="20" y="20" font-size="11" fill="#94a3b8">ideal square wave</text>' +
    '<text x="430" y="20" font-size="11" fill="#6b5cb5">Fourier partial sum</text>';
}
window.addEventListener("DOMContentLoaded", cwFourDraw);
</script>
"""

# ---------- 7. Divergence visualiser ----------
WIDGETS["divergence_field"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · Divergence ∇·V — sources and sinks</div>
  <div class="cw-body">
    <svg id="cw_div_svg" viewBox="0 0 540 280" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>∇·V</label>
      <input type="range" id="cw_div_v" min="-100" max="100" value="0" oninput="cwDivDraw()">
      <span id="cw_div_val" style="min-width:180px;display:inline-block">∇·V = 0 (no divergence)</span>
    </div>
    <div class="cw-note">Arrows show a vector field on a 9 × 5 grid. Negative ∇·V (slider left) means flow is converging into the centre (a "sink"). Positive ∇·V (right) means flow is diverging outward from the centre (a "source"). Zero means each cell has equal in and out — the field is non-divergent.</div>
  </div>
</div>
<script>
function cwDivDraw(){
  var svg = document.getElementById("cw_div_svg"); if(!svg) return;
  var d = document.getElementById("cw_div_v").value/100;
  var W = 540, H = 280, mx = 40, my = 20;
  var nx = 9, ny = 5;
  var dx = (W-2*mx)/(nx-1), dy = (H-2*my-30)/(ny-1);
  var cx = W/2, cy = (H-30)/2;
  var arrows = "";
  for(var i=0;i<nx;i++){
    for(var j=0;j<ny;j++){
      var x = mx + i*dx, y = my + j*dy;
      var rx = x - cx, ry = y - cy;
      var rr = Math.sqrt(rx*rx + ry*ry) + 1e-3;
      var ux = d * rx/rr * 18;
      var uy = d * ry/rr * 18;
      var x2 = x + ux, y2 = y + uy;
      var col = d >= 0 ? "#ee845b" : "#2c8a83";
      arrows += '<line x1="'+x+'" y1="'+y+'" x2="'+x2+'" y2="'+y2+'" stroke="'+col+'" stroke-width="2"/>';
      // arrowhead
      var ang = Math.atan2(uy, ux);
      var ah = 6;
      arrows += '<polygon points="'+x2+','+y2+' '+(x2-ah*Math.cos(ang-0.3))+','+(y2-ah*Math.sin(ang-0.3))+' '+(x2-ah*Math.cos(ang+0.3))+','+(y2-ah*Math.sin(ang+0.3))+'" fill="'+col+'"/>';
    }
  }
  svg.innerHTML =
    '<rect width="540" height="280" fill="#fafbff" rx="6"/>' +
    arrows +
    '<circle cx="'+cx+'" cy="'+cy+'" r="6" fill="#6b5cb5" stroke="#fff" stroke-width="2"/>';
  var label;
  if(d < -0.05) label = "∇·V < 0 — convergence (sink)";
  else if(d > 0.05) label = "∇·V > 0 — divergence (source)";
  else label = "∇·V ≈ 0 — non-divergent";
  document.getElementById("cw_div_val").textContent = "∇·V = " + d.toFixed(2) + " — " + label;
}
window.addEventListener("DOMContentLoaded", cwDivDraw);
</script>
"""

# ---------- 8. Curl visualiser ----------
WIDGETS["curl_field"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · Curl ∇×V — rotation in a vector field</div>
  <div class="cw-body">
    <svg id="cw_curl_svg" viewBox="0 0 540 280" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>curl</label>
      <input type="range" id="cw_curl_v" min="-100" max="100" value="60" oninput="cwCurlDraw()">
      <span id="cw_curl_val" style="min-width:180px;display:inline-block"></span>
    </div>
    <div class="cw-note">The vector field arrows form a rotational pattern. Positive curl is counter-clockwise (cyclonic in the Northern Hemisphere); negative curl is clockwise (anticyclonic). The little paddle-wheel in the centre rotates at a speed proportional to the curl magnitude — that is the physical meaning of curl.</div>
  </div>
</div>
<script>
function cwCurlDraw(){
  var svg = document.getElementById("cw_curl_svg"); if(!svg) return;
  var c = document.getElementById("cw_curl_v").value/100;
  var W = 540, H = 280, mx = 40, my = 20;
  var nx = 9, ny = 5;
  var dx = (W-2*mx)/(nx-1), dy = (H-2*my-30)/(ny-1);
  var cx = W/2, cy = (H-30)/2;
  var arrows = "";
  for(var i=0;i<nx;i++){
    for(var j=0;j<ny;j++){
      var x = mx + i*dx, y = my + j*dy;
      var rx = x - cx, ry = y - cy;
      var ux = -c * ry / 6;
      var uy = c * rx / 6;
      var x2 = x + ux, y2 = y + uy;
      var col = c >= 0 ? "#ee845b" : "#2c8a83";
      arrows += '<line x1="'+x+'" y1="'+y+'" x2="'+x2+'" y2="'+y2+'" stroke="'+col+'" stroke-width="2"/>';
      var ang = Math.atan2(uy, ux);
      var ah = 6;
      arrows += '<polygon points="'+x2+','+y2+' '+(x2-ah*Math.cos(ang-0.3))+','+(y2-ah*Math.sin(ang-0.3))+' '+(x2-ah*Math.cos(ang+0.3))+','+(y2-ah*Math.sin(ang+0.3))+'" fill="'+col+'"/>';
    }
  }
  // paddle wheel
  var pw = "";
  for(var k=0;k<4;k++){
    var a = k*Math.PI/2;
    pw += '<line x1="'+(cx-22*Math.cos(a))+'" y1="'+(cy-22*Math.sin(a))+'" x2="'+(cx+22*Math.cos(a))+'" y2="'+(cy+22*Math.sin(a))+'" stroke="#6b5cb5" stroke-width="2.5"/>';
  }
  svg.innerHTML =
    '<rect width="540" height="280" fill="#fafbff" rx="6"/>' +
    arrows +
    pw +
    '<circle cx="'+cx+'" cy="'+cy+'" r="6" fill="#6b5cb5" stroke="#fff" stroke-width="2"/>';
  var label;
  if(c < -0.05) label = "negative curl — clockwise (anticyclonic)";
  else if(c > 0.05) label = "positive curl — counter-clockwise (cyclonic)";
  else label = "curl ≈ 0 — irrotational";
  document.getElementById("cw_curl_val").textContent = "curl = " + c.toFixed(2) + " — " + label;
}
window.addEventListener("DOMContentLoaded", cwCurlDraw);
</script>
"""

# ---------- 9. Partial-derivative slicer (T(x,t) field) ----------
WIDGETS["partial_deriv_slicer"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · Partial derivatives ∂T/∂t vs ∂T/∂x on a 2-D temperature field T(x, t)</div>
  <div class="cw-body">
    <svg id="cw_pd_svg" viewBox="0 0 540 320" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>x cursor</label>
      <input type="range" id="cw_pd_x" min="0" max="100" value="50" oninput="cwPdDraw()">
      <span id="cw_pd_xval" style="min-width:200px;display:inline-block"></span>
    </div>
    <div class="cw-ctrl">
      <label>t cursor</label>
      <input type="range" id="cw_pd_t" min="0" max="100" value="50" oninput="cwPdDraw()">
      <span id="cw_pd_tval" style="min-width:200px;display:inline-block"></span>
    </div>
    <div class="cw-note">A coloured map shows a 2-D field T(x, t). Drag the cursors to take slices. The horizontal slice (orange line) at fixed t shows how T varies with x — its slope at the cursor is ∂T/∂x. The vertical slice (purple line) at fixed x shows how T varies with t — its slope is ∂T/∂t. The two slopes are completely different quantities at the same (x, t) point; this is the whole point of partial derivatives.</div>
  </div>
</div>
<script>
function cwPdDraw(){
  var svg = document.getElementById("cw_pd_svg"); if(!svg) return;
  var xi = parseInt(document.getElementById("cw_pd_x").value);
  var ti = parseInt(document.getElementById("cw_pd_t").value);
  var W = 540, H = 320, mx = 50, my = 40, fw = 320, fh = 200;
  // T(x,t) = sin(2*pi*x/100) * exp(-t/120) + 0.4*sin(2*pi*x/40)*cos(2*pi*t/80)
  function T(x, t){
    return Math.sin(2*Math.PI*x/100)*Math.exp(-t/120) + 0.4*Math.sin(2*Math.PI*x/40)*Math.cos(2*Math.PI*t/80);
  }
  // colour map
  var cells = "";
  var step = 8;
  for(var i=0;i<fw;i+=step){
    for(var j=0;j<fh;j+=step){
      var x = i/fw*100, t = j/fh*100;
      var v = T(x, t);
      var r, g, b;
      if(v >= 0){ r = 238; g = 132 - Math.min(v,1)*60; b = 91 - Math.min(v,1)*40; }
      else { r = 107 + Math.min(-v,1)*30; g = 92 + Math.min(-v,1)*60; b = 181; }
      cells += '<rect x="'+(mx+i)+'" y="'+(my+j)+'" width="'+step+'" height="'+step+'" fill="rgb('+Math.round(r)+','+Math.round(g)+','+Math.round(b)+')"/>';
    }
  }
  // x-slice plot at right
  var sx1 = mx+fw+20, sw = 110;
  var slicePts = "";
  for(var i=0;i<=100;i+=2){
    var v = T(i, ti);
    var px = sx1 + (v+1)/2 * sw;
    var py = my + i/100 * fh;
    slicePts += (i===0?"M":"L") + px + "," + py + " ";
  }
  // t-slice plot at bottom
  var sy1 = my+fh+18, sh = 50;
  var tslicePts = "";
  for(var j=0;j<=100;j+=2){
    var v = T(xi, j);
    var px = mx + j/100 * fw;
    var py = sy1 + (1-(v+1)/2) * sh;
    tslicePts += (j===0?"M":"L") + px + "," + py + " ";
  }
  var cursorX = mx + xi/100 * fw;
  var cursorY = my + ti/100 * fh;
  svg.innerHTML =
    '<rect width="540" height="320" fill="#fafbff" rx="6"/>' +
    cells +
    '<rect x="'+mx+'" y="'+my+'" width="'+fw+'" height="'+fh+'" fill="none" stroke="#94a3b8"/>' +
    '<line x1="'+mx+'" y1="'+cursorY+'" x2="'+(mx+fw)+'" y2="'+cursorY+'" stroke="#ee845b" stroke-width="2" stroke-dasharray="4 3"/>' +
    '<line x1="'+cursorX+'" y1="'+my+'" x2="'+cursorX+'" y2="'+(my+fh)+'" stroke="#6b5cb5" stroke-width="2" stroke-dasharray="4 3"/>' +
    '<circle cx="'+cursorX+'" cy="'+cursorY+'" r="5" fill="#fff" stroke="#2c3142" stroke-width="2"/>' +
    '<line x1="'+sx1+'" y1="'+my+'" x2="'+sx1+'" y2="'+(my+fh)+'" stroke="#94a3b8"/>' +
    '<text x="'+sx1+'" y="'+(my-6)+'" font-size="10" fill="#6b5cb5">slice at fixed x</text>' +
    '<path d="'+slicePts+'" stroke="#6b5cb5" stroke-width="2" fill="none"/>' +
    '<line x1="'+mx+'" y1="'+(sy1+sh)+'" x2="'+(mx+fw)+'" y2="'+(sy1+sh)+'" stroke="#94a3b8"/>' +
    '<text x="'+mx+'" y="'+(sy1-4)+'" font-size="10" fill="#ee845b">slice at fixed t</text>' +
    '<path d="'+tslicePts+'" stroke="#ee845b" stroke-width="2" fill="none"/>' +
    '<text x="'+mx+'" y="20" font-size="11" fill="#475569">T(x, t) heat-map (orange = hot, purple = cold)</text>' +
    '<text x="'+(mx-30)+'" y="'+(my+fh/2)+'" font-size="10" fill="#94a3b8" transform="rotate(-90 '+(mx-30)+','+(my+fh/2)+')">t →</text>' +
    '<text x="'+(mx+fw/2)+'" y="'+(my+fh+12)+'" font-size="10" fill="#94a3b8">x →</text>';
  // slope estimates
  var dTdt = (T(xi, Math.min(ti+1,100)) - T(xi, Math.max(ti-1,0))) / 2;
  var dTdx = (T(Math.min(xi+1,100), ti) - T(Math.max(xi-1,0), ti)) / 2;
  document.getElementById("cw_pd_xval").textContent = "x = " + xi + ",  ∂T/∂x ≈ " + dTdx.toFixed(3);
  document.getElementById("cw_pd_tval").textContent = "t = " + ti + ",  ∂T/∂t ≈ " + dTdt.toFixed(3);
}
window.addEventListener("DOMContentLoaded", cwPdDraw);
</script>
"""

# ---------- 10. Gradient of a scalar field ----------
WIDGETS["gradient_field"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · Gradient ∇f — arrows pointing uphill on a scalar field</div>
  <div class="cw-body">
    <svg id="cw_grad_svg" viewBox="0 0 540 300" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>peak x</label><input type="range" id="cw_grad_px" min="20" max="80" value="50" oninput="cwGradDraw()"><span id="cw_grad_pxv">50</span>
    </div>
    <div class="cw-ctrl">
      <label>peak y</label><input type="range" id="cw_grad_py" min="20" max="80" value="50" oninput="cwGradDraw()"><span id="cw_grad_pyv">50</span>
    </div>
    <div class="cw-note">A scalar field f(x, y) — think pressure, terrain height, or temperature — is shown as a heat-map. Orange arrows are the gradient ∇f at each grid point. Every arrow points <em>uphill</em> (toward higher values); arrow length is the steepness. Drag the peak. The gradient field always points away from low values and into high values.</div>
  </div>
</div>
<script>
function cwGradDraw(){
  var svg = document.getElementById("cw_grad_svg"); if(!svg) return;
  var px = parseInt(document.getElementById("cw_grad_px").value);
  var py = parseInt(document.getElementById("cw_grad_py").value);
  document.getElementById("cw_grad_pxv").textContent = px;
  document.getElementById("cw_grad_pyv").textContent = py;
  var W = 540, H = 300, mx = 40, my = 30, fw = 460, fh = 220;
  function f(x, y){
    var dx = x - px, dy = y - py;
    return Math.exp(-(dx*dx+dy*dy)/600);
  }
  // colour map
  var cells = "";
  var step = 10;
  for(var i=0;i<fw;i+=step){
    for(var j=0;j<fh;j+=step){
      var x = i/fw*100, y = j/fh*100;
      var v = f(x, y);
      var r = 234 - v*180, g = 240 - v*150, b = 248 - v*30;
      cells += '<rect x="'+(mx+i)+'" y="'+(my+j)+'" width="'+step+'" height="'+step+'" fill="rgb('+Math.round(r)+','+Math.round(g)+','+Math.round(b)+')"/>';
    }
  }
  // gradient arrows on coarser grid
  var arrows = "";
  var ax = 9, ay = 5;
  var dx0 = fw/(ax-1), dy0 = fh/(ay-1);
  for(var i=0;i<ax;i++){
    for(var j=0;j<ay;j++){
      var xx = mx + i*dx0, yy = my + j*dy0;
      var xv = i*100/(ax-1), yv = j*100/(ay-1);
      var h = 1.5;
      var gx = (f(xv+h, yv) - f(xv-h, yv)) / (2*h);
      var gy = (f(xv, yv+h) - f(xv, yv-h)) / (2*h);
      var mag = Math.sqrt(gx*gx + gy*gy);
      if(mag < 1e-4) continue;
      var sc = 600;
      var ex = xx + gx*sc, ey = yy + gy*sc;
      arrows += '<line x1="'+xx+'" y1="'+yy+'" x2="'+ex+'" y2="'+ey+'" stroke="#ee845b" stroke-width="2"/>';
      var ang = Math.atan2(ey-yy, ex-xx);
      var ah = 5;
      arrows += '<polygon points="'+ex+','+ey+' '+(ex-ah*Math.cos(ang-0.3))+','+(ey-ah*Math.sin(ang-0.3))+' '+(ex-ah*Math.cos(ang+0.3))+','+(ey-ah*Math.sin(ang+0.3))+'" fill="#ee845b"/>';
    }
  }
  svg.innerHTML =
    '<rect width="540" height="300" fill="#fafbff" rx="6"/>' +
    cells +
    arrows +
    '<rect x="'+mx+'" y="'+my+'" width="'+fw+'" height="'+fh+'" fill="none" stroke="#94a3b8"/>' +
    '<text x="'+mx+'" y="20" font-size="11" fill="#475569">scalar field f(x,y) (white=low, blue=high)  ·  orange arrows = ∇f (uphill)</text>';
}
window.addEventListener("DOMContentLoaded", cwGradDraw);
</script>
"""

# ---------- 11. CFL advection animator ----------
WIDGETS["cfl_advection"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · The CFL number μ = c Δt / Δx — stable vs. exploding advection</div>
  <div class="cw-body">
    <svg id="cw_cfl_svg" viewBox="0 0 540 280" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>μ</label>
      <input type="range" id="cw_cfl_mu" min="20" max="200" value="80" oninput="cwCflReset(); cwCflDraw()">
      <span id="cw_cfl_muv" style="min-width:280px;display:inline-block"></span>
    </div>
    <div class="cw-ctrl">
      <button onclick="cwCflStep()" style="padding:4px 12px;background:#6b5cb5;color:#fff;border:none;border-radius:4px;cursor:pointer">Step +1 Δt</button>
      <button onclick="cwCflReset(); cwCflDraw()" style="padding:4px 12px;background:#94a3b8;color:#fff;border:none;border-radius:4px;cursor:pointer">Reset</button>
      <button onclick="cwCflAnim()" id="cw_cfl_btn" style="padding:4px 12px;background:#ee845b;color:#fff;border:none;border-radius:4px;cursor:pointer">Play</button>
    </div>
    <div class="cw-note">A Gaussian pulse is advected by the simple upstream scheme uⱼⁿ⁺¹ = uⱼⁿ − μ(uⱼⁿ − uⱼ₋₁ⁿ) with μ = c Δt/Δx. At μ ≤ 1 the pulse moves and slowly diffuses (stable). At μ > 1 the discrete scheme cannot keep up with the physical wave — errors amplify geometrically and the solution explodes. This is the CFL stability bound for upstream advection.</div>
  </div>
</div>
<script>
var cwCflU = null, cwCflN = 0, cwCflTimer = null;
function cwCflReset(){
  cwCflU = []; cwCflN = 0;
  for(var i=0;i<60;i++){
    var x = i - 15;
    cwCflU.push(Math.exp(-x*x/16));
  }
}
function cwCflStep(){
  if(!cwCflU) cwCflReset();
  var mu = document.getElementById("cw_cfl_mu").value/100;
  var u2 = cwCflU.slice();
  for(var i=1;i<u2.length;i++){
    u2[i] = cwCflU[i] - mu*(cwCflU[i] - cwCflU[i-1]);
  }
  cwCflU = u2; cwCflN++;
  cwCflDraw();
}
function cwCflDraw(){
  var svg = document.getElementById("cw_cfl_svg"); if(!svg) return;
  if(!cwCflU) cwCflReset();
  var mu = document.getElementById("cw_cfl_mu").value/100;
  var W = 540, H = 280, mx = 30;
  var pts = "";
  var maxV = 0;
  for(var i=0;i<cwCflU.length;i++){ if(Math.abs(cwCflU[i]) > maxV) maxV = Math.abs(cwCflU[i]); }
  for(var i=0;i<cwCflU.length;i++){
    var xv = mx + i*(W-2*mx)/(cwCflU.length-1);
    var yv = H/2 - cwCflU[i]*90;
    pts += (i===0?"M":"L") + xv + "," + yv + " ";
  }
  var stable = mu <= 1;
  var col = stable ? "#2c8a83" : "#d97757";
  var msg;
  if(mu < 0.95) msg = "μ = " + mu.toFixed(2) + " — stable (pulse advects)";
  else if(mu <= 1.05) msg = "μ ≈ 1 — perfect (no diffusion in upstream when μ=1)";
  else msg = "μ = " + mu.toFixed(2) + " — UNSTABLE — solution blows up";
  svg.innerHTML =
    '<rect width="540" height="280" fill="#fafbff" rx="6"/>' +
    '<line x1="'+mx+'" y1="'+(H/2)+'" x2="'+(W-mx)+'" y2="'+(H/2)+'" stroke="#94a3b8"/>' +
    '<path d="'+pts+'" stroke="'+col+'" stroke-width="2.5" fill="none"/>' +
    '<text x="20" y="20" font-size="11" fill="#475569">step n = ' + cwCflN + '  |  max |u| = ' + maxV.toFixed(2) + '</text>';
  document.getElementById("cw_cfl_muv").textContent = msg;
}
function cwCflAnim(){
  var btn = document.getElementById("cw_cfl_btn");
  if(cwCflTimer){ clearInterval(cwCflTimer); cwCflTimer = null; btn.textContent="Play"; return; }
  btn.textContent="Pause";
  cwCflTimer = setInterval(cwCflStep, 60);
}
window.addEventListener("DOMContentLoaded", function(){ cwCflReset(); cwCflDraw(); });
</script>
"""

# ---------- 12. Heat diffusion vs wave propagation ----------
WIDGETS["diffusion_vs_wave"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · Diffusion vs. wave propagation — two different physics on the same initial pulse</div>
  <div class="cw-body">
    <svg id="cw_dvw_svg" viewBox="0 0 540 280" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>time t</label>
      <input type="range" id="cw_dvw_t" min="0" max="200" value="0" oninput="cwDvwDraw()">
      <span id="cw_dvw_tv" style="min-width:80px;display:inline-block">t = 0.0</span>
      <button onclick="cwDvwAnim()" id="cw_dvw_btn" style="padding:4px 12px;background:#ee845b;color:#fff;border:none;border-radius:4px;cursor:pointer">Play</button>
    </div>
    <div class="cw-note">Start with a Gaussian pulse at the centre. The purple curve is the <strong>heat (diffusion) equation</strong> solution — the pulse spreads outward, gets shorter and wider, energy area is conserved but information is lost. The orange curve is the <strong>wave equation</strong> solution — the pulse splits into two copies that translate left and right at the wave speed without changing shape. Two completely different physics from the same PDE family.</div>
  </div>
</div>
<script>
var cwDvwTimer = null;
function cwDvwDraw(){
  var svg = document.getElementById("cw_dvw_svg"); if(!svg) return;
  var t = document.getElementById("cw_dvw_t").value/100;
  document.getElementById("cw_dvw_tv").textContent = "t = " + t.toFixed(2);
  var W = 540, H = 280, mx = 30;
  // diffusion: G(x,t) = 1/sqrt(1 + 4*kappa*t) * exp(-x^2/(sigma0^2 + 4*kappa*t)) with sigma0^2=0.25
  var kappa = 0.3;
  var s2 = 0.25 + 4*kappa*t;
  var ampD = Math.sqrt(0.25/s2);
  var diffPath = "", wavePath = "";
  for(var i=0;i<=540;i++){
    var x = i*4/540 - 2;
    var yD = ampD * Math.exp(-x*x/s2);
    var c = 0.8;
    var xL = x + c*t, xR = x - c*t;
    var yW = 0.5*Math.exp(-xL*xL/0.25) + 0.5*Math.exp(-xR*xR/0.25);
    var px = mx + i*(W-2*mx)/540;
    diffPath += (i===0?"M":"L") + px + "," + (H/2 - yD*120) + " ";
    wavePath += (i===0?"M":"L") + px + "," + (H/2 - yW*120) + " ";
  }
  svg.innerHTML =
    '<rect width="540" height="280" fill="#fafbff" rx="6"/>' +
    '<line x1="'+mx+'" y1="'+(H/2)+'" x2="'+(W-mx)+'" y2="'+(H/2)+'" stroke="#94a3b8"/>' +
    '<path d="'+diffPath+'" stroke="#6b5cb5" stroke-width="2.5" fill="none"/>' +
    '<path d="'+wavePath+'" stroke="#ee845b" stroke-width="2.5" fill="none" stroke-dasharray="6 4"/>' +
    '<text x="20" y="20" font-size="11" fill="#6b5cb5">diffusion ∂T/∂t = κ ∂²T/∂x²</text>' +
    '<text x="350" y="20" font-size="11" fill="#ee845b">wave ∂²u/∂t² = c² ∂²u/∂x²</text>';
}
function cwDvwAnim(){
  var btn = document.getElementById("cw_dvw_btn");
  if(cwDvwTimer){ clearInterval(cwDvwTimer); cwDvwTimer = null; btn.textContent="Play"; return; }
  btn.textContent="Pause";
  cwDvwTimer = setInterval(function(){
    var sl = document.getElementById("cw_dvw_t");
    var v = (parseInt(sl.value) + 3) % 201;
    sl.value = v; cwDvwDraw();
  }, 50);
}
window.addEventListener("DOMContentLoaded", cwDvwDraw);
</script>
"""

# ---------- 13. Amplification factor FTCS / BTCS / CN ----------
WIDGETS["amplification_factor"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · Amplification factor |A| for the diffusion equation: FTCS vs BTCS vs Crank–Nicolson</div>
  <div class="cw-body">
    <svg id="cw_amp_svg" viewBox="0 0 540 280" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>ν = κΔt/Δz²</label>
      <input type="range" id="cw_amp_nu" min="1" max="500" value="100" oninput="cwAmpDraw()">
      <span id="cw_amp_nuv" style="min-width:300px;display:inline-block"></span>
    </div>
    <div class="cw-note">For a Fourier mode of wavenumber k on a grid Δz, |A| is the per-step growth factor. <strong>FTCS</strong> (forward time, centred space): A = 1 − 4ν sin²(kΔz/2). Stable only when ν ≤ 1/2. <strong>BTCS</strong> (backward time): A = 1/(1 + 4ν sin²(kΔz/2)). Always |A| ≤ 1. <strong>Crank–Nicolson</strong>: A = (1 − 2ν sin²(kΔz/2))/(1 + 2ν sin²(kΔz/2)). Always |A| ≤ 1. The horizontal axis is the dimensionless wavenumber kΔz from 0 to π. The dashed line at |A| = 1 is the stability boundary — anything above is unstable.</div>
  </div>
</div>
<script>
function cwAmpDraw(){
  var svg = document.getElementById("cw_amp_svg"); if(!svg) return;
  var nu = document.getElementById("cw_amp_nu").value/100;
  var W = 540, H = 280, mx = 40, my = 30, fw = W-2*mx, fh = H-2*my-20;
  function s2(kdz){ var s = Math.sin(kdz/2); return s*s; }
  function ftcs(kdz){ return 1 - 4*nu*s2(kdz); }
  function btcs(kdz){ return 1/(1 + 4*nu*s2(kdz)); }
  function cn(kdz){ return (1 - 2*nu*s2(kdz))/(1 + 2*nu*s2(kdz)); }
  // Plot |A| vs kΔz in [0, π]; vertical from -3 to 3 then clip
  function Y(v){ return my + fh - (v + 3)/6 * fh; }
  function X(kdz){ return mx + kdz/Math.PI * fw; }
  var pathF = "", pathB = "", pathC = "";
  for(var i=0;i<=200;i++){
    var kdz = i/200 * Math.PI;
    pathF += (i===0?"M":"L") + X(kdz) + "," + Y(Math.max(-3, Math.min(3, ftcs(kdz)))) + " ";
    pathB += (i===0?"M":"L") + X(kdz) + "," + Y(btcs(kdz)) + " ";
    pathC += (i===0?"M":"L") + X(kdz) + "," + Y(cn(kdz)) + " ";
  }
  svg.innerHTML =
    '<rect width="540" height="280" fill="#fafbff" rx="6"/>' +
    '<line x1="'+mx+'" y1="'+Y(0)+'" x2="'+(mx+fw)+'" y2="'+Y(0)+'" stroke="#94a3b8"/>' +
    '<line x1="'+mx+'" y1="'+Y(1)+'" x2="'+(mx+fw)+'" y2="'+Y(1)+'" stroke="#cbd5e1" stroke-dasharray="3 3"/>' +
    '<line x1="'+mx+'" y1="'+Y(-1)+'" x2="'+(mx+fw)+'" y2="'+Y(-1)+'" stroke="#cbd5e1" stroke-dasharray="3 3"/>' +
    '<text x="'+(mx+fw+4)+'" y="'+(Y(1)+3)+'" font-size="10" fill="#94a3b8">+1</text>' +
    '<text x="'+(mx+fw+4)+'" y="'+(Y(-1)+3)+'" font-size="10" fill="#94a3b8">-1</text>' +
    '<text x="'+(mx+fw+4)+'" y="'+(Y(0)+3)+'" font-size="10" fill="#94a3b8">0</text>' +
    '<line x1="'+mx+'" y1="'+my+'" x2="'+mx+'" y2="'+(my+fh)+'" stroke="#94a3b8"/>' +
    '<path d="'+pathF+'" stroke="#d97757" stroke-width="2.5" fill="none"/>' +
    '<path d="'+pathB+'" stroke="#6b5cb5" stroke-width="2.5" fill="none"/>' +
    '<path d="'+pathC+'" stroke="#2c8a83" stroke-width="2.5" fill="none" stroke-dasharray="4 3"/>' +
    '<text x="'+(mx+fw-90)+'" y="'+(my+fh+16)+'" font-size="11" fill="#94a3b8">k Δz = π (2Δz wave)</text>' +
    '<text x="'+mx+'" y="'+(my+fh+16)+'" font-size="11" fill="#94a3b8">k Δz = 0</text>' +
    '<text x="20" y="20" font-size="11" fill="#d97757">FTCS</text>' +
    '<text x="100" y="20" font-size="11" fill="#6b5cb5">BTCS</text>' +
    '<text x="180" y="20" font-size="11" fill="#2c8a83">Crank–Nicolson</text>';
  // Worst-case |A| reported
  var aF = Math.abs(ftcs(Math.PI));
  var aB = Math.abs(btcs(Math.PI));
  var aC = Math.abs(cn(Math.PI));
  document.getElementById("cw_amp_nuv").textContent =
    "ν = " + nu.toFixed(2) + "  |  |A| at 2Δz wave:  FTCS=" + aF.toFixed(2) + ",  BTCS=" + aB.toFixed(2) + ",  CN=" + aC.toFixed(2);
}
window.addEventListener("DOMContentLoaded", cwAmpDraw);
</script>
"""

# ---------- 14. Damping-depth visualiser ----------
WIDGETS["damping_depth"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · Damping depth — diurnal surface wave penetrating into the ground</div>
  <div class="cw-body">
    <svg id="cw_dd_svg" viewBox="0 0 540 320" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>κ (m²/s × 1e-7)</label>
      <input type="range" id="cw_dd_k" min="5" max="100" value="15" oninput="cwDdDraw()">
      <span id="cw_dd_kv" style="min-width:200px;display:inline-block"></span>
    </div>
    <div class="cw-ctrl">
      <label>hour of day</label>
      <input type="range" id="cw_dd_h" min="0" max="240" value="120" oninput="cwDdDraw()">
      <span id="cw_dd_hv" style="min-width:120px;display:inline-block">12.0 h</span>
      <button onclick="cwDdAnim()" id="cw_dd_btn" style="padding:4px 12px;background:#ee845b;color:#fff;border:none;border-radius:4px;cursor:pointer">Play</button>
    </div>
    <div class="cw-note">A diurnal surface forcing T(0,t) = 10 sin(ωt) drives a thermal wave into the ground. The analytical solution is T(z,t) = 10 e^(−z/d) sin(ωt − z/d), where d = √(2κ/ω) is the damping depth. Below depth ≈ d, amplitude has dropped to 1/e ≈ 37% of the surface value; below 3d, the wave is essentially gone. The phase also lags — peak temperature at depth d arrives 1 radian later than at the surface (≈ 4 h for a daily wave).</div>
  </div>
</div>
<script>
var cwDdTimer = null;
function cwDdDraw(){
  var svg = document.getElementById("cw_dd_svg"); if(!svg) return;
  var kappa = document.getElementById("cw_dd_k").value*1e-7;
  var hr = document.getElementById("cw_dd_h").value/10;
  var omega = 2*Math.PI / 86400;
  var d = Math.sqrt(2*kappa/omega);
  document.getElementById("cw_dd_kv").textContent = "κ = " + (kappa*1e7).toFixed(0) + "e-7 m²/s,  d = " + (d*100).toFixed(1) + " cm";
  document.getElementById("cw_dd_hv").textContent = hr.toFixed(1) + " h";
  var W = 540, H = 320, mx = 60, my = 30, pw = 200, ph = H - 2*my;
  // Left: amplitude envelope vs depth (in cm)
  var maxZ = 1.0; // 1 m
  // envelope
  var envPath = "M"+mx+","+my;
  for(var i=0;i<=200;i++){
    var z = i/200 * maxZ;
    var amp = 10 * Math.exp(-z/d);
    var px = mx + amp/12 * pw;
    var py = my + i/200 * ph;
    envPath += " L" + px + "," + py;
  }
  envPath += " L"+mx+","+(my+ph)+" Z";
  // mirror envelope
  var envPath2 = "M"+mx+","+my;
  for(var i=0;i<=200;i++){
    var z = i/200 * maxZ;
    var amp = 10 * Math.exp(-z/d);
    var px = mx - amp/12 * pw;
    var py = my + i/200 * ph;
    envPath2 += " L" + px + "," + py;
  }
  // current profile at hour=hr
  var t = hr*3600;
  var profilePath = "";
  for(var i=0;i<=200;i++){
    var z = i/200 * maxZ;
    var Tval = 10 * Math.exp(-z/d) * Math.sin(omega*t - z/d);
    var px = mx + Tval/12 * pw;
    var py = my + i/200 * ph;
    profilePath += (i===0?"M":"L") + px + "," + py + " ";
  }
  // depth markers
  var dMarks = "";
  for(var k=1;k<=3;k++){
    var z = k*d;
    if(z > maxZ) break;
    var py = my + z/maxZ * ph;
    dMarks += '<line x1="'+(mx-pw)+'" y1="'+py+'" x2="'+(mx+pw)+'" y2="'+py+'" stroke="#cbd5e1" stroke-dasharray="3 3"/>';
    dMarks += '<text x="'+(mx+pw+6)+'" y="'+(py+4)+'" font-size="10" fill="#94a3b8">'+k+'d</text>';
  }
  // Right side: surface T(t) over 24h with current time marker
  var rx0 = mx + pw + 60, rw = 140, rh = 220, ry0 = 50;
  var sfPath = "";
  for(var i=0;i<=240;i++){
    var hh = i/10;
    var tt = hh*3600;
    var Tval = 10 * Math.sin(omega*tt);
    sfPath += (i===0?"M":"L") + (rx0 + i/240*rw) + "," + (ry0 + rh/2 - Tval*9) + " ";
  }
  var curX = rx0 + hr/24*rw;
  svg.innerHTML =
    '<rect width="540" height="320" fill="#fafbff" rx="6"/>' +
    '<path d="'+envPath+'" fill="rgba(238,132,91,0.18)" stroke="none"/>' +
    '<path d="'+envPath2+'" fill="rgba(238,132,91,0.18)" stroke="none"/>' +
    dMarks +
    '<line x1="'+mx+'" y1="'+my+'" x2="'+mx+'" y2="'+(my+ph)+'" stroke="#94a3b8"/>' +
    '<path d="'+profilePath+'" stroke="#6b5cb5" stroke-width="2.5" fill="none"/>' +
    '<text x="'+(mx-pw)+'" y="20" font-size="11" fill="#475569">T(z, t) profile and amplitude envelope</text>' +
    '<text x="'+(mx-pw-30)+'" y="'+(my+ph/2)+'" font-size="10" fill="#94a3b8" transform="rotate(-90 '+(mx-pw-30)+','+(my+ph/2)+')">depth z →</text>' +
    '<text x="'+rx0+'" y="40" font-size="11" fill="#475569">Surface T(0, t) over 24 h</text>' +
    '<line x1="'+rx0+'" y1="'+(ry0+rh/2)+'" x2="'+(rx0+rw)+'" y2="'+(ry0+rh/2)+'" stroke="#94a3b8"/>' +
    '<path d="'+sfPath+'" stroke="#ee845b" stroke-width="2" fill="none"/>' +
    '<line x1="'+curX+'" y1="'+ry0+'" x2="'+curX+'" y2="'+(ry0+rh)+'" stroke="#2c8a83" stroke-width="2"/>' +
    '<text x="'+curX+'" y="'+(ry0+rh+12)+'" text-anchor="middle" font-size="10" fill="#2c8a83">now</text>';
}
function cwDdAnim(){
  var btn = document.getElementById("cw_dd_btn");
  if(cwDdTimer){ clearInterval(cwDdTimer); cwDdTimer = null; btn.textContent="Play"; return; }
  btn.textContent="Pause";
  cwDdTimer = setInterval(function(){
    var sl = document.getElementById("cw_dd_h");
    var v = (parseInt(sl.value) + 3) % 241;
    sl.value = v; cwDdDraw();
  }, 60);
}
window.addEventListener("DOMContentLoaded", cwDdDraw);
</script>
"""

# ---------- 15. Cross product (right-hand rule) ----------
WIDGETS["cross_product"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · The cross product A × B and the right-hand rule</div>
  <div class="cw-body">
    <svg id="cw_cp_svg" viewBox="0 0 540 280" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>angle θ</label>
      <input type="range" id="cw_cp_th" min="0" max="180" value="60" oninput="cwCpDraw()">
      <span id="cw_cp_thv" style="min-width:300px;display:inline-block"></span>
    </div>
    <div class="cw-note">Two vectors A (orange) and B (purple) lie in the page. Their cross product A×B is a third vector perpendicular to both — its magnitude is |A||B| sin θ (= area of the parallelogram they span). At θ = 0 (parallel) the cross product is zero. At θ = 90° it is largest. In atmospheric physics the Coriolis force is −2Ω×V — perpendicular to the wind, which is what makes wind curve into cyclones and anticyclones.</div>
  </div>
</div>
<script>
function cwCpDraw(){
  var svg = document.getElementById("cw_cp_svg"); if(!svg) return;
  var th = document.getElementById("cw_cp_th").value*Math.PI/180;
  var W = 540, H = 280, cx = 200, cy = 150;
  var aLen = 100, bLen = 85;
  var ax = cx + aLen, ay = cy;
  var bx = cx + bLen*Math.cos(-th), by = cy + bLen*Math.sin(-th);
  // parallelogram
  var pgon = cx+","+cy + " " + ax+","+ay + " " + (ax+bx-cx)+","+(ay+by-cy) + " " + bx+","+by;
  // out-of-page indicator (circle with dot = out toward viewer if A×B points out)
  // sign of A×B z-component: A_x*B_y - A_y*B_x with A = (aLen, 0), B = (bLen cos(-th), bLen sin(-th))
  // = aLen * bLen * sin(-th) - 0 = -aLen*bLen*sin(th)
  // Negative z-component → into page (cross). Positive z → out of page (dot).
  var zComp = aLen * bLen * Math.sin(-th);
  // For pedagogy: convention is that with right-hand rule from A to B (going counter-clockwise from A to B), result is out of page.
  // Here B is drawn at angle -th below A — so swept clockwise — result is into page when th > 0.
  var outIndicator;
  if(th < 0.05){ outIndicator = '<text x="380" y="150" font-size="14" fill="#475569">A × B = 0 (parallel)</text>'; }
  else {
    var indX = 400, indY = 150;
    outIndicator = '<circle cx="'+indX+'" cy="'+indY+'" r="22" fill="none" stroke="#2c8a83" stroke-width="2"/>' +
      '<line x1="'+(indX-14)+'" y1="'+(indY-14)+'" x2="'+(indX+14)+'" y2="'+(indY+14)+'" stroke="#2c8a83" stroke-width="2"/>' +
      '<line x1="'+(indX+14)+'" y1="'+(indY-14)+'" x2="'+(indX-14)+'" y2="'+(indY+14)+'" stroke="#2c8a83" stroke-width="2"/>' +
      '<text x="'+indX+'" y="'+(indY+45)+'" text-anchor="middle" font-size="11" fill="#2c8a83">A × B into page</text>';
  }
  var magAB = aLen * bLen * Math.sin(th) / 100;
  svg.innerHTML =
    '<rect width="540" height="280" fill="#fafbff" rx="6"/>' +
    '<polygon points="'+pgon+'" fill="rgba(56,178,172,0.12)" stroke="none"/>' +
    '<line x1="'+cx+'" y1="'+cy+'" x2="'+ax+'" y2="'+ay+'" stroke="#ee845b" stroke-width="3"/>' +
    '<polygon points="'+ax+','+ay+' '+(ax-8)+','+(ay-4)+' '+(ax-8)+','+(ay+4)+'" fill="#ee845b"/>' +
    '<text x="'+(ax+8)+'" y="'+(ay+4)+'" font-size="13" fill="#ee845b" font-weight="bold">A</text>' +
    '<line x1="'+cx+'" y1="'+cy+'" x2="'+bx+'" y2="'+by+'" stroke="#6b5cb5" stroke-width="3"/>' +
    '<polygon points="'+bx+','+by+' '+(bx-8*Math.cos(-th)+4*Math.sin(-th))+','+(by-8*Math.sin(-th)-4*Math.cos(-th))+' '+(bx-8*Math.cos(-th)-4*Math.sin(-th))+','+(by-8*Math.sin(-th)+4*Math.cos(-th))+'" fill="#6b5cb5"/>' +
    '<text x="'+(bx+6)+'" y="'+(by+4)+'" font-size="13" fill="#6b5cb5" font-weight="bold">B</text>' +
    '<path d="M '+(cx+30)+' '+cy+' A 30 30 0 0 1 '+(cx+30*Math.cos(-th))+' '+(cy+30*Math.sin(-th))+'" fill="none" stroke="#94a3b8" stroke-width="1.5"/>' +
    '<text x="'+(cx+38)+'" y="'+(cy-6)+'" font-size="11" fill="#94a3b8">θ</text>' +
    outIndicator +
    '<text x="20" y="20" font-size="11" fill="#475569">A and B in the page</text>';
  document.getElementById("cw_cp_thv").textContent =
    "θ = " + (th*180/Math.PI).toFixed(0) + "°,  |A × B| = |A||B| sin θ = " + magAB.toFixed(2);
}
window.addEventListener("DOMContentLoaded", cwCpDraw);
</script>
"""

# ---------- 16. Coriolis deflection ----------
WIDGETS["coriolis"] = r"""
<div class="cw-card">
  <div class="cw-head">Widget · Coriolis deflection — a "straight" path on a rotating Earth</div>
  <div class="cw-body">
    <svg id="cw_cor_svg" viewBox="0 0 540 280" style="width:100%;height:auto;max-width:560px;display:block;margin:0 auto"></svg>
    <div class="cw-ctrl">
      <label>latitude (°N)</label>
      <input type="range" id="cw_cor_lat" min="-90" max="90" value="45" oninput="cwCorReset(); cwCorDraw()">
      <span id="cw_cor_latv" style="min-width:280px;display:inline-block"></span>
    </div>
    <div class="cw-ctrl">
      <button onclick="cwCorStep()" style="padding:4px 12px;background:#6b5cb5;color:#fff;border:none;border-radius:4px;cursor:pointer">Step forward</button>
      <button onclick="cwCorReset(); cwCorDraw()" style="padding:4px 12px;background:#94a3b8;color:#fff;border:none;border-radius:4px;cursor:pointer">Reset</button>
      <button onclick="cwCorAnim()" id="cw_cor_btn" style="padding:4px 12px;background:#ee845b;color:#fff;border:none;border-radius:4px;cursor:pointer">Play</button>
    </div>
    <div class="cw-note">A puck is launched eastward from the centre of the panel. In a non-rotating frame it would travel in a straight line (dashed). On a rotating Earth, the Coriolis acceleration f V (perpendicular to motion) curves the trajectory — to the right in the Northern Hemisphere (positive latitude), to the left in the Southern. Set latitude near zero and the deflection vanishes (Coriolis parameter f = 2Ω sin φ → 0 at the equator).</div>
  </div>
</div>
<script>
var cwCorTraj = null, cwCorTimer = null;
function cwCorReset(){
  cwCorTraj = [{x: 270, y: 140, vx: 1.6, vy: 0}];
}
function cwCorStep(){
  if(!cwCorTraj) cwCorReset();
  var lat = parseInt(document.getElementById("cw_cor_lat").value) * Math.PI/180;
  var f = 0.012 * Math.sin(lat);
  var p = cwCorTraj[cwCorTraj.length-1];
  var ax = f * p.vy, ay = -f * p.vx;
  var dt = 1.0;
  var np = {x: p.x + p.vx*dt, y: p.y + p.vy*dt, vx: p.vx + ax*dt, vy: p.vy + ay*dt};
  // bound
  if(np.x < 20 || np.x > 520 || np.y < 20 || np.y > 250){ return; }
  cwCorTraj.push(np);
  cwCorDraw();
}
function cwCorDraw(){
  var svg = document.getElementById("cw_cor_svg"); if(!svg) return;
  if(!cwCorTraj) cwCorReset();
  var lat = parseInt(document.getElementById("cw_cor_lat").value);
  var hem = lat > 0 ? "Northern (deflects right)" : (lat < 0 ? "Southern (deflects left)" : "equator (no deflection)");
  document.getElementById("cw_cor_latv").textContent = "lat = " + lat + "°  |  f = 2Ω sinφ → " + hem;
  var path = "M " + cwCorTraj[0].x + " " + cwCorTraj[0].y;
  for(var i=1;i<cwCorTraj.length;i++){ path += " L " + cwCorTraj[i].x + " " + cwCorTraj[i].y; }
  var straightPath = "M 270 140 L 520 140";
  var p = cwCorTraj[cwCorTraj.length-1];
  svg.innerHTML =
    '<rect width="540" height="280" fill="#fafbff" rx="6"/>' +
    '<circle cx="270" cy="140" r="6" fill="#94a3b8"/>' +
    '<text x="240" y="135" font-size="11" fill="#94a3b8">launch</text>' +
    '<path d="'+straightPath+'" stroke="#cbd5e1" stroke-width="1.5" fill="none" stroke-dasharray="4 3"/>' +
    '<text x="430" y="135" font-size="10" fill="#94a3b8">non-rotating path</text>' +
    '<path d="'+path+'" stroke="#6b5cb5" stroke-width="2.5" fill="none"/>' +
    '<circle cx="'+p.x+'" cy="'+p.y+'" r="6" fill="#ee845b" stroke="#fff" stroke-width="2"/>';
}
function cwCorAnim(){
  var btn = document.getElementById("cw_cor_btn");
  if(cwCorTimer){ clearInterval(cwCorTimer); cwCorTimer = null; btn.textContent="Play"; return; }
  btn.textContent="Pause";
  cwCorTimer = setInterval(cwCorStep, 80);
}
window.addEventListener("DOMContentLoaded", function(){ cwCorReset(); cwCorDraw(); });
</script>
"""

# ============================================================
# CSS for widget cards (added to existing CSS)
# ============================================================
WIDGET_CSS = """
.cw-card { margin: 22px -10px; background: #ffffff; border-radius: 8px; box-shadow: 0 4px 14px rgba(107,92,181,.10); border: 1px solid rgba(107,92,181,.18); overflow: hidden; }
.cw-head { background: linear-gradient(90deg, #ee845b, #d97757); color: #fff; padding: 10px 18px; font-size: 13.5px; font-weight: 700; letter-spacing: 0.3px; }
.cw-body { padding: 16px 18px; }
.cw-ctrl { display: flex; align-items: center; gap: 10px; margin: 8px 0; font-size: 13px; color: #475569; flex-wrap: wrap; }
.cw-ctrl label { font-weight: 700; color: #6b5cb5; min-width: 36px; }
.cw-ctrl input[type="range"] { flex: 1 1 220px; max-width: 320px; accent-color: #ee845b; }
.cw-note { margin-top: 10px; padding: 10px 14px; background: rgba(56,178,172,.06); border-left: 3px solid #38b2ac; border-radius: 0 4px 4px 0; font-size: 13px; color: #2c8a83; line-height: 1.55; }
"""

# Insert widgets into markdown text
for marker, html in WIDGETS.items():
    md_text = md_text.replace(f"<!--WIDGET:{marker}-->", html)

# ============================================================
# Math protect + markdown → HTML
# ============================================================
math_blocks = []
def stash_display(m):
    math_blocks.append(("display", m.group(1)))
    return f"@@@MATH{len(math_blocks)-1}@@@"
def stash_inline(m):
    math_blocks.append(("inline", m.group(1)))
    return f"@@@MATH{len(math_blocks)-1}@@@"
md_text = re.sub(r"\$\$(.+?)\$\$", stash_display, md_text, flags=re.DOTALL)
md_text = re.sub(r"\$([^$\n]+?)\$", stash_inline, md_text)

html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'extra', 'toc'])

def restore_math(html):
    def repl(m):
        idx = int(m.group(1))
        kind, body = math_blocks[idx]
        return (f"$${body}$$" if kind == "display" else f"${body}$")
    return re.sub(r"@@@MATH(\d+)@@@", repl, html)
html_body = restore_math(html_body)

# Find TOC items (h2 + h3) for sidebar
toc_items = []
for m in re.finditer(r'<h(\d)(?: id="([^"]*)")?>([^<]+)</h\1>', html_body):
    level = int(m.group(1))
    id_attr = m.group(2)
    title = m.group(3).strip()
    if 2 <= level <= 3 and id_attr:
        toc_items.append((level, id_attr, title))

# Strip leading <h1>
first_h1 = re.search(r"<h1>(.*?)</h1>", html_body, re.DOTALL)
if first_h1:
    html_body = html_body[:first_h1.start()] + html_body[first_h1.end():]

CSS = """
* { box-sizing: border-box; }
body, html { margin: 0; padding: 0; font-family: 'Segoe UI', Calibri, Geneva, sans-serif; background: #eaf0f8; color: #2c3142; line-height: 1.65; }
.layout { display: grid; grid-template-columns: 300px 1fr; max-width: 1600px; margin: 0 auto; }
.toc { position: sticky; top: 0; height: 100vh; overflow-y: auto; background: #ffffff; border-right: 1px solid rgba(107, 92, 181, 0.15); padding: 28px 16px 28px 24px; box-shadow: 2px 0 8px rgba(107, 92, 181, 0.05); }
.toc h2 { font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: #6b5cb5; margin: 0 0 14px 0; font-weight: 700; }
.toc ul { list-style: none; padding: 0; margin: 0; }
.toc li { margin-bottom: 3px; }
.toc a { color: #4a5066; text-decoration: none; font-size: 12.5px; display: block; padding: 4px 8px; border-radius: 4px; border-left: 2px solid transparent; transition: all 0.15s; line-height: 1.4; }
.toc a:hover { background: rgba(107, 92, 181, 0.06); color: #6b5cb5; border-left-color: #6b5cb5; }
.toc a.level-3 { padding-left: 22px; font-size: 11.5px; color: #6b7186; }
main { padding: 40px 60px 80px 60px; max-width: 1100px; }
h1 { color: #2c3142; font-size: 32px; margin-top: 0; margin-bottom: 12px; line-height: 1.25; }
h2 { color: #6b5cb5; font-size: 24px; margin-top: 44px; margin-bottom: 12px; padding-top: 16px; border-top: 1px solid rgba(107, 92, 181, 0.15); }
h3 { color: #4a5066; font-size: 19px; margin-top: 30px; margin-bottom: 8px; }
h4 { color: #ee845b; font-size: 15px; font-weight: 700; margin-top: 22px; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }
p { margin: 10px 0 14px 0; font-size: 15px; }
strong { color: #2c3142; }
em { color: #4a5066; }
code { background: #f3f0fa; color: #6b5cb5; padding: 1px 6px; border-radius: 3px; font-family: 'Cascadia Code', 'Consolas', monospace; font-size: 0.9em; }
pre { background: #1a1a2e; color: #cfd8dc; padding: 14px 18px; border-radius: 6px; overflow-x: auto; font-size: 13px; }
pre code { background: transparent; color: inherit; padding: 0; }
blockquote { margin: 14px 0; padding: 12px 18px; background: rgba(56, 178, 172, 0.08); border-left: 4px solid #38b2ac; border-radius: 0 6px 6px 0; color: #2c8a83; font-style: italic; }
blockquote strong { color: #2c8a83; }
table { border-collapse: collapse; width: 100%; margin: 16px 0; background: #ffffff; box-shadow: 0 2px 6px rgba(107, 92, 181, 0.08); border-radius: 6px; overflow: hidden; font-size: 14px; }
th { background: #6b5cb5; color: #ffffff; font-weight: 700; text-align: left; padding: 10px 14px; font-size: 13px; }
td { padding: 8px 14px; border-top: 1px solid rgba(107, 92, 181, 0.1); }
tr:nth-child(even) td { background: rgba(107, 92, 181, 0.03); }
hr { border: none; border-top: 1px solid rgba(107, 92, 181, 0.2); margin: 32px 0; }
ul, ol { margin: 10px 0 14px 24px; padding: 0; }
li { margin-bottom: 4px; font-size: 15px; }
mjx-container[display="true"] { margin: 14px 0 !important; overflow-x: auto; }
.banner { background: linear-gradient(135deg, #6b5cb5 0%, #2c8a83 100%); color: #ffffff; padding: 40px 60px; margin: 0 -60px 28px -60px; }
.banner h1 { color: #ffffff; margin: 0; font-size: 30px; }
.banner .subtitle { font-size: 16px; opacity: 0.95; margin-top: 8px; font-style: italic; }
.banner .meta { font-size: 13px; opacity: 0.85; margin-top: 16px; font-family: 'Cascadia Code', 'Consolas', monospace; }
iframe { width: 100%; }
""" + WIDGET_CSS + """
@media (max-width: 1000px) {
  .layout { grid-template-columns: 1fr; }
  .toc { position: relative; height: auto; border-right: none; border-bottom: 1px solid rgba(107, 92, 181, 0.15); }
  main { padding: 24px 18px 60px 18px; }
  .banner { padding: 24px 18px; margin: 0 -18px 20px -18px; }
}
"""

toc_html = "\n".join(
    f'<li><a href="#{id_attr}" class="level-{level}">{title}</a></li>'
    for level, id_attr, title in toc_items
)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CLIM-715 Study Guide</title>
<style>
{CSS}
</style>
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true, tags: 'none'
  }},
  options: {{ skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'] }}
}};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
<div class="layout">
<aside class="toc">
  <h2>Contents</h2>
  <ul>
{toc_html}
  </ul>
</aside>
<main>
  <div class="banner">
    <h1>CLIM-715 — Study Guide</h1>
    <div class="subtitle">Numerical Methods for Weather &amp; Climate Modeling — Plain-English, Easy to Follow Walkthrough</div>
    <div class="meta">A beginner-friendly help guide for anyone learning numerical modeling of weather and climate</div>
  </div>

{html_body}

  <hr>
  <p style="font-size: 13px; color: #6b7186; text-align: center;">
    <em>Source: Lecture_Master_Guide.md + chapter0_prereqs.md.</em>
  </p>
</main>
</div>
</body>
</html>
"""

with open("Lecture_Master_Guide.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"Wrote Lecture_Master_Guide.html ({len(HTML):,} bytes)")
print(f"  Math blocks: {len(math_blocks)}, TOC entries: {len(toc_items)}")
print(f"  Widgets embedded: {len(WIDGETS)}")
