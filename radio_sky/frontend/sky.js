"use strict";

const API = "http://localhost:5001/api";
const CANVAS_SIZE = 600;
const CX = CANVAS_SIZE / 2;
const CY = CANVAS_SIZE / 2;
const R_MAX = CANVAS_SIZE / 2 - 30; // matches Python haslam.py r_max

let skyData           = null;
let galacticData      = null;
let targetsData       = null;
let starsData         = null;
let constellationData = null;
let moonData          = null;
let haslamImg         = null;

const layers = {
  haslam:         true,
  galactic_plane: true,
  targets:        true,
  stars:          true,
  constellations: true,
  moon:           true,
  grid:           true,
};

// ── Projection ────────────────────────────────────────────────────────────────
// Azimuthal equidistant, zenith-centred.  North=up, East=left (sky view).
// r = R_MAX * (90 - alt) / 90  →  zenith at centre, horizon at edge
// az=0→North(up), az=90→East(left)  — matches Python haslam.py exactly
function altazToXY(alt, az) {
  const r   = R_MAX * (90 - alt) / 90;
  const rad = az * Math.PI / 180;
  return [CX - r * Math.sin(rad), CY - r * Math.cos(rad)];
}

// ── Data fetching ─────────────────────────────────────────────────────────────
async function refresh() {
  try {
    const [sky, gal, tgt, sts, cons, moon] = await Promise.all([
      fetch(`${API}/sky`).then(r => r.json()),
      fetch(`${API}/galactic_plane`).then(r => r.json()),
      fetch(`${API}/targets`).then(r => r.json()),
      fetch(`${API}/stars`).then(r => r.json()),
      fetch(`${API}/constellations`).then(r => r.json()),
      fetch(`${API}/moon`).then(r => r.json()),
    ]);
    skyData           = sky;
    galacticData      = gal;
    targetsData       = tgt;
    starsData         = sts;
    constellationData = cons;
    moonData          = moon;
    updateClock();
    updateTargetList();
    render();
  } catch (e) {
    console.error("Refresh failed:", e);
  }
}

function loadHaslam() {
  const badge = document.getElementById("haslam-status");
  fetch(`${API}/haslam`)
    .then(r => r.json())
    .then(data => {
      if (data.status !== "ok") throw new Error(data.message);
      const img = new Image();
      img.onload = () => {
        haslamImg = img;
        badge.textContent = "408 MHz ready";
        badge.className = "status-badge ready";
        setTimeout(() => { badge.className = "status-badge hidden"; }, 3000);
        render();
      };
      img.src = "data:image/png;base64," + data.image;
    })
    .catch(e => {
      badge.textContent = "408 MHz unavailable";
      badge.className = "status-badge loading";
      console.warn("Haslam load failed:", e);
    });
}

// ── Clock ─────────────────────────────────────────────────────────────────────
function updateClock() {
  if (!skyData) return;
  document.getElementById("utc-time").textContent =
    new Date(skyData.utc).toUTCString().replace(" GMT", " UTC");
  document.getElementById("lst-display").textContent =
    `LST ${skyData.lst_hours.toFixed(2)} h`;
}

// ── Render ────────────────────────────────────────────────────────────────────
function render() {
  const canvas = document.getElementById("skyCanvas");
  const ctx    = canvas.getContext("2d");

  ctx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);

  // Sky background
  const grad = ctx.createRadialGradient(CX, CY, 0, CX, CY, R_MAX);
  grad.addColorStop(0,   "#0d0d2b");
  grad.addColorStop(0.7, "#080818");
  grad.addColorStop(1,   "#050510");
  ctx.save();
  ctx.beginPath();
  ctx.arc(CX, CY, R_MAX, 0, 2 * Math.PI);
  ctx.fillStyle = grad;
  ctx.fill();

  // Clip everything to the horizon circle
  ctx.beginPath();
  ctx.arc(CX, CY, R_MAX, 0, 2 * Math.PI);
  ctx.clip();

  // ── Haslam 408 MHz image ────────────────────────────────────────
  if (layers.haslam && haslamImg) {
    ctx.globalAlpha = 0.72;
    ctx.drawImage(haslamImg, 0, 0, CANVAS_SIZE, CANVAS_SIZE);
    ctx.globalAlpha = 1.0;
  }

  // ── Azimuth/altitude grid ───────────────────────────────────────
  if (layers.grid) {
    ctx.save();

    // Altitude rings: 15°, 30°, 45°, 60°, 75°
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 6]);
    for (const [alt, opacity] of [[15, 0.18], [30, 0.25], [45, 0.22], [60, 0.20], [75, 0.18]]) {
      const r = R_MAX * (90 - alt) / 90;
      ctx.strokeStyle = `rgba(140,170,220,${opacity})`;
      ctx.beginPath();
      ctx.arc(CX, CY, r, 0, 2 * Math.PI);
      ctx.stroke();
    }

    // Azimuth spokes every 45°
    ctx.setLineDash([2, 8]);
    for (let az = 0; az < 360; az += 45) {
      ctx.strokeStyle = `rgba(140,170,220,${az % 90 === 0 ? 0.22 : 0.13})`;
      const [hx, hy] = altazToXY(0, az);
      ctx.beginPath();
      ctx.moveTo(CX, CY);
      ctx.lineTo(hx, hy);
      ctx.stroke();
    }
    ctx.setLineDash([]);

    // Altitude ring labels at az=135° (SE, uncluttered)
    ctx.fillStyle    = "rgba(170,200,240,0.65)";
    ctx.font         = "10px monospace";
    ctx.textAlign    = "center";
    ctx.textBaseline = "middle";
    for (const alt of [15, 30, 45, 60, 75]) {
      const [lx, ly] = altazToXY(alt, 135);
      ctx.fillText(`${alt}°`, lx, ly);
    }

    ctx.restore();
  }

  // ── Galactic plane ──────────────────────────────────────────────
  if (layers.galactic_plane && galacticData) {
    ctx.save();
    ctx.strokeStyle  = "#ffaa00";
    ctx.lineWidth    = 2;
    ctx.shadowColor  = "#ffaa00";
    ctx.shadowBlur   = 10;

    let penDown = false;
    ctx.beginPath();
    for (const pt of galacticData.points) {
      if (pt.alt < 0) { penDown = false; continue; }
      const [x, y] = altazToXY(pt.alt, pt.az);
      if (!penDown) { ctx.moveTo(x, y); penDown = true; }
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.shadowBlur = 0;
    ctx.restore();
  }

  // ── Constellation stick figures ─────────────────────────────────
  if (layers.constellations && constellationData) {
    ctx.save();
    // Solid lines, bright enough to read over the Haslam glow
    ctx.strokeStyle = "rgba(180,210,255,0.55)";
    ctx.lineWidth   = 1.5;
    for (const c of constellationData.constellations) {
      for (const seg of c.lines) {
        const [x1, y1] = altazToXY(seg.alt1, seg.az1);
        const [x2, y2] = altazToXY(seg.alt2, seg.az2);
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();
      }
    }

    // Constellation name labels at centroid of visible segments
    ctx.fillStyle    = "rgba(160,185,230,0.55)";
    ctx.font         = "10px monospace";
    ctx.textAlign    = "center";
    ctx.textBaseline = "middle";
    for (const c of constellationData.constellations) {
      if (!c.lines.length) continue;
      const avgAlt = c.lines.reduce((s, l) => s + (l.alt1 + l.alt2) / 2, 0) / c.lines.length;
      const azVals = c.lines.map(l => (l.az1 + l.az2) / 2);
      // Circular mean for azimuth to handle wrap-around
      const sinA = azVals.reduce((s, a) => s + Math.sin(a * Math.PI/180), 0) / azVals.length;
      const cosA = azVals.reduce((s, a) => s + Math.cos(a * Math.PI/180), 0) / azVals.length;
      const avgAz = (Math.atan2(sinA, cosA) * 180 / Math.PI + 360) % 360;
      const [lx, ly] = altazToXY(avgAlt + 3, avgAz);
      ctx.fillText(c.name.toUpperCase(), lx, ly);
    }
    ctx.restore();
  }

  // ── Bright optical stars ────────────────────────────────────────
  if (layers.stars && starsData) {
    ctx.save();
    for (const s of starsData.stars) {
      const [x, y] = altazToXY(s.alt, s.az);
      const radius = Math.max(1.5, 4.5 - s.mag * 1.2);

      ctx.beginPath();
      ctx.arc(x, y, radius, 0, 2 * Math.PI);
      ctx.fillStyle = "#e8f0ff";
      ctx.fill();

      if (s.mag < 0.5) {
        ctx.fillStyle    = "rgba(200,215,255,0.6)";
        ctx.font         = "9px monospace";
        ctx.textAlign    = "left";
        ctx.textBaseline = "middle";
        ctx.fillText(s.name, x + radius + 3, y);
      }
    }
    ctx.restore();
  }

  // ── Moon ─────────────────────────────────────────────────────────
  if (layers.moon && moonData && moonData.visible) {
    const [mx, my] = altazToXY(moonData.alt, moonData.az);
    const mr = 10;

    ctx.save();
    // Glow
    ctx.shadowColor = "rgba(220,230,255,0.6)";
    ctx.shadowBlur  = 18;
    ctx.beginPath();
    ctx.arc(mx, my, mr, 0, 2 * Math.PI);
    ctx.fillStyle = `rgba(210,220,255,${0.3 + moonData.illumination / 200})`;
    ctx.fill();
    ctx.shadowBlur = 0;

    // Moon disc — shade based on illumination
    const illumFrac = moonData.illumination / 100;
    ctx.beginPath();
    ctx.arc(mx, my, mr, 0, 2 * Math.PI);
    ctx.fillStyle = `rgba(220,230,255,${0.2 + illumFrac * 0.65})`;
    ctx.fill();
    ctx.strokeStyle = "rgba(200,215,255,0.7)";
    ctx.lineWidth = 1;
    ctx.stroke();

    // Label
    ctx.fillStyle    = "rgba(210,225,255,0.75)";
    ctx.font         = "10px monospace";
    ctx.textAlign    = "center";
    ctx.textBaseline = "top";
    ctx.fillText(`☽ ${moonData.phase} (${moonData.illumination}%)`, mx, my + mr + 4);
    ctx.restore();
  }

  ctx.restore(); // end clip

  // ── Horizon ring ────────────────────────────────────────────────
  ctx.strokeStyle = "#2a4060";
  ctx.lineWidth   = 2;
  ctx.beginPath();
  ctx.arc(CX, CY, R_MAX, 0, 2 * Math.PI);
  ctx.stroke();

  // ── Cardinal direction labels (outside ring) ─────────────────────
  // N/S/E/W get bold treatment; NE/SE/SW/NW are smaller
  const CARDINALS = [
    ["N", 0, true], ["NE", 45, false], ["E", 90, true], ["SE", 135, false],
    ["S", 180, true], ["SW", 225, false], ["W", 270, true], ["NW", 315, false],
  ];
  for (const [label, az, bold] of CARDINALS) {
    const [hx, hy] = altazToXY(0, az);
    const nx = CX + (hx - CX) * 1.08;
    const ny = CY + (hy - CY) * 1.08;
    ctx.fillStyle    = bold ? "#aabbd4" : "#5a7090";
    ctx.font         = bold ? "bold 13px monospace" : "11px monospace";
    ctx.textAlign    = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(label, nx, ny);
  }

  // ── Zenith label ────────────────────────────────────────────────
  ctx.fillStyle    = "rgba(255,255,255,0.25)";
  ctx.font         = "10px monospace";
  ctx.textAlign    = "center";
  ctx.textBaseline = "bottom";
  ctx.fillText("zenith", CX, CY - 8);
  // crosshair
  ctx.save();
  ctx.strokeStyle = "rgba(255,255,255,0.18)";
  ctx.lineWidth   = 1;
  ctx.setLineDash([2, 5]);
  ctx.beginPath();
  ctx.moveTo(CX - 8, CY); ctx.lineTo(CX + 8, CY);
  ctx.moveTo(CX, CY - 8); ctx.lineTo(CX, CY + 8);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.restore();

  // ── Sky drift arrow ──────────────────────────────────────────────
  // Sky rotates east→west (left→right on this N-up, E-left map).
  // Draw a curved arrow near the bottom of the map.
  {
    ctx.save();
    const ay = CY + R_MAX * 0.78;   // near bottom, inside circle
    const ax1 = CX - 55, ax2 = CX + 55;
    const arrowColor = "rgba(180,200,230,0.55)";

    ctx.strokeStyle = arrowColor;
    ctx.fillStyle   = arrowColor;
    ctx.lineWidth   = 1.5;

    // Horizontal line with arrowhead pointing right (west = sky drift direction)
    ctx.beginPath();
    ctx.moveTo(ax1, ay);
    ctx.lineTo(ax2, ay);
    ctx.stroke();

    // Arrowhead pointing right (west)
    ctx.beginPath();
    ctx.moveTo(ax2, ay);
    ctx.lineTo(ax2 - 8, ay - 5);
    ctx.lineTo(ax2 - 8, ay + 5);
    ctx.closePath();
    ctx.fill();

    // Small "E" on left, "W" on right
    ctx.font         = "9px monospace";
    ctx.textBaseline = "middle";
    ctx.fillStyle    = arrowColor;
    ctx.textAlign    = "right";
    ctx.fillText("E", ax1 - 3, ay);
    ctx.textAlign = "left";
    ctx.fillText("W", ax2 + 5, ay);

    ctx.font      = "9px monospace";
    ctx.textAlign = "center";
    ctx.fillStyle = "rgba(160,185,220,0.5)";
    ctx.fillText("sky drifts this way", CX, ay + 12);
    ctx.restore();
  }

  // ── Radio sources ────────────────────────────────────────────────
  if (layers.targets && targetsData) {
    for (const t of targetsData.targets) {
      if (!t.visible || t.ra === null) continue;

      const [x, y] = altazToXY(t.alt, t.az);
      const radius  = Math.max(Math.log10(Math.max(t.flux_jy || 100, 10)) * 4, 5);

      ctx.beginPath();
      ctx.arc(x, y, radius + 3, 0, 2 * Math.PI);
      ctx.fillStyle = t.color + "22";
      ctx.fill();

      ctx.beginPath();
      ctx.arc(x, y, radius, 0, 2 * Math.PI);
      ctx.fillStyle   = t.color + "55";
      ctx.fill();
      ctx.strokeStyle = t.color;
      ctx.lineWidth   = 1.5;
      ctx.stroke();

      ctx.save();
      ctx.shadowColor = t.color;
      ctx.shadowBlur  = 14;
      ctx.beginPath();
      ctx.arc(x, y, radius * 0.4, 0, 2 * Math.PI);
      ctx.fillStyle = t.color;
      ctx.fill();
      ctx.restore();
    }
  }
}

// ── Target list (sidebar) ─────────────────────────────────────────────────────
function updateTargetList() {
  if (!targetsData) return;
  const visible = targetsData.targets
    .filter(t => t.visible && t.ra !== null)
    .sort((a, b) => b.alt - a.alt);

  const list = document.getElementById("target-list");
  list.innerHTML = "";

  if (visible.length === 0) {
    list.innerHTML = '<p class="muted">No notable sources above horizon.</p>';
    return;
  }

  for (const t of visible) {
    const div = document.createElement("div");
    div.className = "target-item";
    div.style.borderLeftColor = t.color;
    div.innerHTML = `
      <span class="target-name" style="color:${t.color}">${t.name}</span>
      <span class="target-meta">${t.type} &nbsp;·&nbsp; alt ${t.alt.toFixed(1)}°</span>
    `;
    div.addEventListener("click", () => showDetail(t));
    list.appendChild(div);
  }
}

// ── Detail panel ──────────────────────────────────────────────────────────────
function showDetail(t) {
  const card  = document.getElementById("detail-card");
  const panel = document.getElementById("detail-panel");
  const flux  = t.flux_jy
    ? `${t.flux_jy.toLocaleString()} Jy @ ${t.freq_mhz} MHz`
    : `variable (${t.freq_mhz} MHz)`;

  panel.innerHTML = `
    <div class="detail-name" style="color:${t.color}">${t.name}</div>
    <div class="detail-type">${t.type}</div>
    <div class="detail-pos">
      Alt&nbsp;${t.alt.toFixed(1)}° &nbsp;|&nbsp;
      Az&nbsp;${t.az.toFixed(1)}° &nbsp;|&nbsp;
      ${flux}
    </div>
    <div class="detail-section">
      <strong>Why it glows in radio</strong>
      ${t.why_radio}
    </div>
    ${t.from_bangalore ? `
    <div class="detail-section">
      <strong>From Bangalore</strong>
      ${t.from_bangalore}
    </div>` : ""}
  `;
  card.style.display = "block";
  card.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// ── Hover / click ─────────────────────────────────────────────────────────────
const canvas  = document.getElementById("skyCanvas");
const tooltip = document.getElementById("tooltip");

function nearestTarget(mx, my, radius = 22) {
  if (!targetsData) return null;
  let best = null, minD = radius;
  for (const t of targetsData.targets) {
    if (!t.visible || t.ra === null) continue;
    const [x, y] = altazToXY(t.alt, t.az);
    const d = Math.hypot(mx - x, my - y);
    if (d < minD) { minD = d; best = t; }
  }
  return best;
}

function nearestStar(mx, my, radius = 14) {
  if (!starsData) return null;
  let best = null, minD = radius;
  for (const s of starsData.stars) {
    const [x, y] = altazToXY(s.alt, s.az);
    const d = Math.hypot(mx - x, my - y);
    if (d < minD) { minD = d; best = s; }
  }
  return best;
}

canvas.addEventListener("mousemove", e => {
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;

  const t = nearestTarget(mx, my);
  const s = !t && layers.stars ? nearestStar(mx, my) : null;

  if (t) {
    tooltip.textContent = t.name;
    tooltip.style.display = "block";
    tooltip.style.left = (e.clientX + 14) + "px";
    tooltip.style.top  = (e.clientY - 6)  + "px";
    canvas.style.cursor = "pointer";
  } else if (s) {
    tooltip.textContent = `★ ${s.name}  (mag ${s.mag.toFixed(1)})`;
    tooltip.style.display = "block";
    tooltip.style.left = (e.clientX + 14) + "px";
    tooltip.style.top  = (e.clientY - 6)  + "px";
    canvas.style.cursor = "default";
  } else {
    tooltip.style.display = "none";
    canvas.style.cursor = "default";
  }
});

canvas.addEventListener("mouseleave", () => { tooltip.style.display = "none"; });

canvas.addEventListener("click", e => {
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;
  const t = nearestTarget(mx, my);
  if (t) showDetail(t);
});

// ── Layer toggles ─────────────────────────────────────────────────────────────
document.querySelectorAll(".layer-toggle").forEach(cb => {
  cb.addEventListener("change", e => {
    layers[e.target.dataset.layer] = e.target.checked;
    render();
  });
});

// ── Boot ──────────────────────────────────────────────────────────────────────
refresh();
loadHaslam();
setInterval(refresh, 60_000);
setInterval(loadHaslam, 300_000);
