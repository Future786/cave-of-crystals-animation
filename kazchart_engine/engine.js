/* KazChart engine — deterministic SVG frame renderer.
 * window.KZ.render(spec, t) draws the frame at time t (seconds) into #stage.
 * World space is always 1920x1080; output size comes from spec.width/height.
 */
(function () {
  let W = 1920, H = 1080;
  const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, k) => a + (b - a) * k;
  const easeOut = k => 1 - Math.pow(1 - clamp(k), 3);
  const easeInOut = k => { k = clamp(k); return k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };
  const back = k => { k = clamp(k); const c = 1.9; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
  const prog = (t, t0, d) => clamp((t - t0) / (d || 0.0001));
  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const hex = (h) => { h = h.replace('#', ''); return [0, 2, 4].map(i => parseInt(h.substr(i, 2), 16)); };
  const mix = (a, b, k) => { const A = hex(a), B = hex(b); return '#' + A.map((v, i) => Math.round(lerp(v, B[i], k)).toString(16).padStart(2, '0')).join(''); };
  function rng(seed) { let s = seed >>> 0 || 1; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }

  /* ---------------- presets ---------------- */
  const PRESETS = {
    abyss: {
      top: '#081e2d', bottom: '#02060a', stroke: 'none', sw: 0,
      font: 'Poppins', capsCaptions: true, hl: '#00f2fe', good: '#3ecf6a',
      text: '#f0f8ff', pill: '#081a26', marker: '#f2e35b',
      mode: 'abyss'
    },
    magma: {
      top: '#24160f', bottom: '#0d0704', stroke: '#ff9f1c', sw: 3,
      font: 'Poppins', capsCaptions: true, hl: '#ff9f1c', good: '#3ecf6a',
      text: '#fff3e0', pill: '#1c120c', marker: '#ffd600',
      mode: 'magma'
    },
    sonar: {
      top: '#03170e', bottom: '#010804', stroke: '#00ff66', sw: 2,
      font: 'Poppins', capsCaptions: true, hl: '#00ff66', good: '#00e5ff',
      text: '#e8f5e9', pill: '#051f14', marker: '#00e5ff',
      mode: 'sonar'
    },
    glacial: {
      top: '#0a2336', bottom: '#030d15', stroke: '#80deea', sw: 2,
      font: 'Poppins', capsCaptions: true, hl: '#00e5ff', good: '#b2ebf2',
      text: '#e0f7fa', pill: '#082133', marker: '#80deea',
      mode: 'glacial'
    },
    inferno: {
      top: '#2d0902', bottom: '#0c0200', stroke: '#ff3d00', sw: 3,
      font: 'Poppins', capsCaptions: true, hl: '#ff9100', good: '#ffd700',
      text: '#fff8e1', pill: '#260b05', marker: '#ff3d00',
      mode: 'inferno'
    },
    microscope: {
      top: '#0a1e14', bottom: '#020905', stroke: '#76ff03', sw: 2,
      font: 'Poppins', capsCaptions: true, hl: '#76ff03', good: '#00e5ff',
      text: '#f1f8e9', pill: '#091f14', marker: '#76ff03',
      mode: 'microscope'
    },
    cosmos: {
      top: '#05020c', bottom: '#010004', stroke: '#ffd700', sw: 2,
      font: 'Poppins', capsCaptions: true, hl: '#ffd700', good: '#80d8ff',
      text: '#f3e5f5', pill: '#14092b', marker: '#ffd700',
      mode: 'cosmos'
    },
    radiation: {
      top: '#171908', bottom: '#060702', stroke: '#ffd600', sw: 3,
      font: 'Poppins', capsCaptions: true, hl: '#ffd600', good: '#76ff03',
      text: '#fffde7', pill: '#171807', marker: '#ff1744',
      mode: 'radiation'
    },
    canyon: {
      top: '#181410', bottom: '#060503', stroke: '#26c6da', sw: 2,
      font: 'Poppins', capsCaptions: true, hl: '#00e5ff', good: '#80deea',
      text: '#eceff1', pill: '#141916', marker: '#ffd54f',
      mode: 'canyon'
    },
    strata: {
      top: '#241911', bottom: '#0c0704', stroke: '#ffab40', sw: 3,
      font: 'Poppins', capsCaptions: true, hl: '#ffab40', good: '#ffd54f',
      text: '#fff8e1', pill: '#1c1510', marker: '#ffab40',
      mode: 'strata'
    },
    ink: {
      top: '#2a6a85', bottom: '#08151e', stroke: '#14171a', sw: 4,
      font: 'Poppins', capsCaptions: false, hl: '#f5a623', good: '#3ecf6a',
      text: '#eef2f3', pill: '#122028', marker: '#f2e35b',
      mode: 'default'
    },
  };
  const MODES = {
    silhouette: () => ['#05090d', '#05090d', '#05090d'],
    thermal: () => ['#c8682f', '#f0a05a', '#7a3316'],
    sonar: () => ['#0b2a12', '#39ff6a', '#39ff6a'],
    ghost: () => ['#9aa3a8', '#c3c9cc', '#7d868b'],
  };

  /* ---------------- creatures (local coords, facing right, ~400 wide) ---------------- */
  function sty(P, fill, extra = '') {
    return `fill="${fill}" stroke="${P.stroke}" stroke-width="${P.sw}" stroke-linejoin="round" ${extra}`;
  }
  const C = {};
  C.whale = (P, col, t, o) => {
    const [b, , d] = col, sway = Math.sin(t * 2.2 + (o.phase || 0)) * 9;
    return `<g transform="rotate(${sway} -200 0)"><path ${sty(P, b)} d="M-196,-6 L-238,-34 C-252,-40 -266,-30 -256,-20 L-240,0 L-256,20 C-266,30 -252,40 -238,34 L-196,6 Z"/></g>
    <path ${sty(P, b)} d="M182,-8 C186,-46 150,-56 60,-54 L-110,-36 C-160,-26 -190,-10 -202,0 C-190,10 -160,22 -110,30 L60,50 C150,54 186,42 182,8 Z"/>
    <path fill="${d}" opacity=".35" d="M60,50 C150,54 186,42 182,8 L182,30 C160,52 120,58 60,58 Z"/>
    <path fill="none" stroke="${d}" stroke-width="3" d="M70,44 L172,30"/>
    <path ${sty(P, d)} d="M30,42 L0,76 L-14,44 Z"/>
    <path ${sty(P, b)} d="M-60,-40 L-80,-56 L-96,-36 Z"/>
    <circle cx="128" cy="8" r="4" fill="#0b0b0b"/>`;
  };
  C.shark = (P, col, t, o) => {
    const [b, belly, d] = col, sway = Math.sin(t * 3 + (o.phase || 0)) * 10;
    let teeth = ''; for (let i = 0; i < 6; i++) teeth += `${i ? 'l' : 'M108,17 l'}5,7 l5,-7`;
    const eye = o.threat ? `<circle cx="150" cy="-8" r="9" fill="#ff2a2a" opacity=".5"/><circle cx="150" cy="-8" r="4.5" fill="#ff4a3a"/>` : `<circle cx="150" cy="-8" r="4" fill="#0b0b0b"/>`;
    return `<g transform="rotate(${sway} -186 0)"><path ${sty(P, b)} d="M-184,-2 L-246,-78 L-228,0 L-250,56 Z"/></g>
    <path ${sty(P, d)} d="M30,-38 L0,-112 L-42,-36 Z"/>
    <path ${sty(P, b)} d="M204,0 C172,-32 100,-46 0,-42 C-80,-40 -150,-20 -190,-5 L-190,5 C-150,20 -80,40 0,42 C100,46 172,32 204,0 Z"/>
    <path fill="${belly}" d="M200,6 C166,30 100,42 0,40 C-80,38 -150,20 -186,5 L-140,8 L-120,0 L-100,12 L-80,2 L-60,14 L-40,4 L-20,16 L0,6 L20,18 L40,8 L60,18 L80,8 L100,16 L120,6 L140,12 L170,4 Z"/>
    <path fill="none" stroke="#fff" stroke-width="2.5" d="${teeth}"/>
    <path ${sty(P, d)} d="M70,28 L24,96 L4,36 Z"/>
    ${eye}`;
  };
  C.orca = (P, col, t, o) => {
    const [b, w] = col, sway = Math.sin(t * 2.6 + (o.phase || 0)) * 9;
    return `<g transform="rotate(${sway} -186 0)"><path ${sty(P, b)} d="M-184,0 L-236,-40 L-222,0 L-236,40 Z"/></g>
    <path ${sty(P, b)} d="M10,-40 L-8,-120 L-50,-36 Z"/>
    <path ${sty(P, b)} d="M200,4 C186,-30 110,-46 10,-44 C-80,-40 -150,-18 -190,0 C-150,18 -80,40 10,42 C110,44 190,34 200,4 Z"/>
    <path fill="${w}" d="M196,12 C170,30 110,40 30,36 C60,30 120,24 196,12 Z"/>
    <ellipse cx="120" cy="-14" rx="22" ry="9" fill="${w}"/><ellipse cx="-40" cy="-22" rx="26" ry="7" fill="#9aa0a6" opacity=".7"/>
    <path ${sty(P, b)} d="M60,30 L30,84 L14,34 Z"/>`;
  };
  C.squid = (P, col, t, o) => {
    const [b, l] = col; let arms = '';
    for (let i = 0; i < 8; i++) {
      const y = -14 + i * 4, w = Math.sin(t * 4 + i * .7 + (o.phase || 0)) * 10;
      arms += `<path fill="none" stroke="${b}" stroke-width="${i % 4 ? 4 : 6}" stroke-linecap="round" d="M60,${y} Q120,${y + w} ${170 + (i % 4 === 0 ? 50 : 0)},${y * 1.6 + w}"/>`;
    }
    return `${arms}<path ${sty(P, b)} d="M70,-22 C10,-30 -80,-24 -140,-8 L-170,-30 L-160,0 L-170,30 L-140,8 C-80,24 10,30 70,22 Z"/>
    <path fill="${l}" opacity=".5" d="M60,10 C0,18 -80,14 -130,4 C-80,8 0,8 60,4 Z"/><circle cx="48" cy="-4" r="6" fill="#111"/>`;
  };
  C.fish = (P, col, t, o) => {
    const [b, l] = col, sway = Math.sin(t * 7 + (o.phase || 0)) * 14;
    return `<g transform="rotate(${sway} -60 0)"><path ${sty(P, b)} d="M-58,0 L-100,-30 L-92,0 L-100,30 Z"/></g>
    <path ${sty(P, b)} d="M90,0 C70,-34 -20,-38 -62,0 C-20,38 70,34 90,0 Z"/><path fill="${l}" d="M86,6 C60,26 -10,28 -56,4 C0,14 50,14 86,6 Z"/><circle cx="58" cy="-6" r="5" fill="#111"/>`;
  };
  C.diver = (P, col, t, o) => {
    const [suit, tank, fin] = col, kick = Math.sin(t * 4 + (o.phase || 0)) * 12;
    return `<g transform="rotate(${kick} -120 0)"><path ${sty(P, fin)} d="M-120,-6 L-220,-30 L-214,-2 Z"/></g>
    <g transform="rotate(${-kick} -120 8)"><path ${sty(P, fin)} d="M-120,4 L-216,12 L-206,34 Z"/></g>
    <rect x="-130" y="-16" width="250" height="34" rx="16" ${sty(P, suit)}/>
    <rect x="-70" y="-46" width="150" height="26" rx="13" ${sty(P, tank)}/>
    <rect x="-40" y="-4" width="110" height="5" fill="#2fb6d6"/>
    <circle cx="150" cy="-4" r="26" ${sty(P, suit)}/><rect x="152" y="-16" width="26" height="16" rx="4" fill="#6fd3e6" stroke="#222" stroke-width="2"/>
    <path fill="none" stroke="${suit}" stroke-width="14" stroke-linecap="round" d="M110,8 L200,28"/><rect x="196" y="20" width="22" height="12" rx="6" fill="#ddd"/>`;
  };
  C.person = (P, col, t) => {
    const wave = Math.sin(t * 3) * 10;
    return `<circle cx="0" cy="-130" r="22" fill="#d8b48c" stroke="#222" stroke-width="3"/>
    <circle cx="-8" cy="-130" r="6" fill="none" stroke="#222" stroke-width="2.5"/><circle cx="9" cy="-130" r="6" fill="none" stroke="#222" stroke-width="2.5"/>
    <path fill="#5a3b25" d="M-22,-136 C-20,-160 20,-160 22,-136 Z"/>
    <rect x="-26" y="-104" width="52" height="96" rx="4" fill="#e6e6e6"/>
    <rect x="-20" y="-8" width="14" height="80" fill="#3a3f45"/><rect x="6" y="-8" width="14" height="80" fill="#3a3f45"/>
    <path fill="none" stroke="#e6e6e6" stroke-width="12" stroke-linecap="round" d="M26,-96 L${52 + wave * .3},${-150 + wave}"/>`;
  };
  // head-on views (approach shots, lineups)
  C.sharkFront = (P, col, t, o) => {
    const [b, belly, d] = col; let teeth = '';
    for (let i = 0; i < 13; i++) teeth += `${i ? 'l' : 'M-78,22 l'}6,12 l6,-12`;
    const eyes = o.threat ? `<circle cx="-82" cy="-14" r="16" fill="#ff2a2a" opacity=".35"/><circle cx="82" cy="-14" r="16" fill="#ff2a2a" opacity=".35"/><circle cx="-82" cy="-14" r="7" fill="#ff5040"/><circle cx="82" cy="-14" r="7" fill="#ff5040"/>` : `<circle cx="-82" cy="-14" r="6" fill="#0b0b0b"/><circle cx="82" cy="-14" r="6" fill="#0b0b0b"/>`;
    return `<path ${sty(P, d)} d="M-70,30 L-250,150 L-60,60 Z"/><path ${sty(P, d)} d="M70,30 L250,150 L60,60 Z"/>
    <path ${sty(P, d)} d="M-8,-60 L0,-170 L8,-60 Z"/>
    <path ${sty(P, b)} d="M-110,0 C-110,-60 110,-60 110,0 C110,60 -110,70 -110,0 Z"/>
    <path fill="${belly}" d="M-84,22 C-50,60 50,60 84,22 C40,40 -40,40 -84,22 Z"/>
    <path fill="#140d0b" d="M-84,20 C-40,34 40,34 84,20 C50,56 -50,56 -84,20 Z"/>
    <path fill="none" stroke="#fff" stroke-width="3" d="${teeth}"/>${eyes}`;
  };
  C.blob = (P, col) => `<ellipse rx="160" ry="50" ${sty(P, col[0])}/>`;

  function colorsFor(P, kind, mode) {
    if (mode && MODES[mode]) return MODES[mode]();
    const base = kind === 'sharkFront' ? 'shark' : kind;
    return P.creature[base] || P.creature.whale;
  }

  /* ---------------- background ---------------- */
  function background(P, bg, t, cam) {
    const depth = bg.depth == null ? 0.4 : bg.depth;
    let top = bg.top || mix(P.top, P.bottom, depth * .8), bot = bg.bottom || P.bottom;
    const mode = bg.mode || P.mode || 'default';

    if (mode === 'inferno') { top = '#2d0902'; bot = '#0c0200'; }
    else if (mode === 'cosmos') { top = '#05020c'; bot = '#010004'; }
    else if (mode === 'sonar') { top = '#03170e'; bot = '#010804'; }
    else if (mode === 'glacial') { top = '#0a2336'; bot = '#030d15'; }
    else if (mode === 'magma') { top = '#24160f'; bot = '#0d0704'; }
    else if (mode === 'radiation') { top = '#171908'; bot = '#060702'; }
    else if (mode === 'microscope') { top = '#0a1e14'; bot = '#020905'; }
    else if (mode === 'canyon') { top = '#181410'; bot = '#060503'; }
    else if (mode === 'strata') { top = '#241911'; bot = '#0c0704'; }
    else if (mode === 'abyss') { top = '#081e2d'; bot = '#02060a'; }

    let s = `<defs>
      <linearGradient id="bgg" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="${top}"/>
        <stop offset="1" stop-color="${bot}"/>
      </linearGradient>
      <radialGradient id="spot" cx=".5" cy="0" r="1">
        <stop offset="0" stop-color="#cfe8ff" stop-opacity=".35"/>
        <stop offset="1" stop-color="#cfe8ff" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="fireglow" cx=".5" cy="1" r=".8">
        <stop offset="0" stop-color="#ff3d00" stop-opacity=".45"/>
        <stop offset=".4" stop-color="#ff9100" stop-opacity=".2"/>
        <stop offset="1" stop-color="#ff3d00" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="nebulaglow" cx=".5" cy=".3" r=".6">
        <stop offset="0" stop-color="#7c4dff" stop-opacity=".3"/>
        <stop offset=".5" stop-color="#00e5ff" stop-opacity=".12"/>
        <stop offset="1" stop-color="#000" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="radglow" cx=".5" cy=".8" r=".7">
        <stop offset="0" stop-color="#76ff03" stop-opacity=".25"/>
        <stop offset=".6" stop-color="#d500f9" stop-opacity=".12"/>
        <stop offset="1" stop-color="#000" stop-opacity="0"/>
      </radialGradient>
      <filter id="blur6"><feGaussianBlur stdDeviation="6"/></filter>
      <filter id="blur2"><feGaussianBlur stdDeviation="2"/></filter>
      <filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    </defs>
    <rect x="-400" y="-400" width="${W + 800}" height="${H + 800}" fill="url(#bgg)"/>`;

    // 1. INFERNO (Darvaza)
    if (mode === 'inferno') {
      s += `<rect x="-400" y="400" width="${W + 800}" height="${H}" fill="url(#fireglow)"/>`;
      const r = rng(21), n = 55;
      for (let i = 0; i < n; i++) {
        const px = r() * W, py0 = r() * H, sp = 15 + r() * 25, rad = 2 + r() * 4;
        const py = ((py0 - t * sp) % H + H) % H; // rising
        const px2 = px + Math.sin(t * 1.5 + i) * 18;
        const col = i % 3 === 0 ? '#ffea00' : (i % 3 === 1 ? '#ff9100' : '#ff3d00');
        s += `<circle cx="${px2}" cy="${py}" r="${rad}" fill="${col}" opacity="${0.4 + r() * 0.5}" filter="url(#blur2)"/>`;
      }
    }
    // 2. COSMOS (The Wow! Signal)
    else if (mode === 'cosmos') {
      s += `<rect x="-400" y="-400" width="${W + 800}" height="${H + 800}" fill="url(#nebulaglow)"/>`;
      const r = rng(42), n = 80;
      for (let i = 0; i < n; i++) {
        const px = r() * W, py = r() * H, rad = 0.8 + r() * 2.2;
        const tw = 0.2 + 0.8 * Math.abs(Math.sin(t * 2.5 + i * 1.3));
        const col = i % 4 === 0 ? '#ffd700' : (i % 4 === 1 ? '#80d8ff' : '#ffffff');
        s += `<circle cx="${px}" cy="${py}" r="${rad}" fill="${col}" opacity="${tw.toFixed(2)}"/>`;
      }
    }
    // 3. SONAR (The Bloop)
    else if (mode === 'sonar') {
      const rot = (t * 45) % 360;
      s += `<g opacity="0.25">
        <circle cx="${W/2}" cy="${H/2}" r="180" fill="none" stroke="#00ff66" stroke-width="1.5" stroke-dasharray="6,6"/>
        <circle cx="${W/2}" cy="${H/2}" r="360" fill="none" stroke="#00ff66" stroke-width="1.5"/>
        <circle cx="${W/2}" cy="${H/2}" r="540" fill="none" stroke="#00ff66" stroke-width="1.5" stroke-dasharray="10,8"/>
        <line x1="${W/2}" y1="0" x2="${W/2}" y2="${H}" stroke="#00ff66" stroke-width="1" stroke-opacity="0.3"/>
        <line x1="0" y1="${H/2}" x2="${W}" y2="${H/2}" stroke="#00ff66" stroke-width="1" stroke-opacity="0.3"/>
        <g transform="rotate(${rot} ${W/2} ${H/2})">
          <polygon points="${W/2},${H/2} ${W/2 + 500},${H/2 - 120} ${W/2 + 500},${H/2}" fill="#00ff66" opacity="0.12" filter="url(#blur6)"/>
        </g>
      </g>`;
    }
    // 4. RADIATION (Chernobyl)
    else if (mode === 'radiation') {
      s += `<rect x="-400" y="200" width="${W + 800}" height="${H}" fill="url(#radglow)"/>`;
      const r = rng(Math.floor(t * 18)), n = 35;
      for (let i = 0; i < n; i++) {
        const px = r() * W, py = r() * H, rad = 1 + r() * 2.5;
        s += `<rect x="${px}" y="${py}" width="${rad * 2}" height="${rad * 2}" fill="#76ff03" opacity="${0.3 + r() * 0.6}"/>`;
      }
    }
    // 5. GLACIAL (Lake Vostok)
    else if (mode === 'glacial') {
      const r = rng(77), n = 40;
      for (let i = 0; i < n; i++) {
        const px = r() * W, py0 = r() * H, sp = 5 + r() * 10, rad = 1.5 + r() * 3;
        const py = ((py0 + t * sp) % H + H) % H;
        s += `<polygon points="${px},${py - rad} ${px + rad},${py} ${px},${py + rad} ${px - rad},${py}" fill="#e0f7fa" opacity="${0.2 + r() * 0.4}"/>`;
      }
    }
    // 6. MAGMA / SUBTERRANEAN (Kola Borehole)
    else if (mode === 'magma') {
      s += `<line x1="${W/2}" y1="0" x2="${W/2}" y2="${H}" stroke="#ff9f1c" stroke-width="3" stroke-dasharray="16,12" opacity="0.25"/>`;
      const r = rng(99), n = 30;
      for (let i = 0; i < n; i++) {
        const px = r() * W, py0 = r() * H, sp = 8 + r() * 15, rad = 2 + r() * 3;
        const py = ((py0 - t * sp) % H + H) % H;
        s += `<circle cx="${px}" cy="${py}" r="${rad}" fill="#ff9f1c" opacity="${0.25 + r() * 0.4}"/>`;
      }
    }
    // 7. MICROSCOPE (Tardigrades)
    else if (mode === 'microscope') {
      s += `<g opacity="0.18">
        <line x1="120" y1="${H/2}" x2="${W-120}" y2="${H/2}" stroke="#76ff03" stroke-width="1.5"/>
        <line x1="${W/2}" y1="200" x2="${W/2}" y2="${H-200}" stroke="#76ff03" stroke-width="1.5"/>
        <circle cx="${W/2}" cy="${H/2}" r="320" fill="none" stroke="#76ff03" stroke-width="2"/>
        <circle cx="${W/2}" cy="${H/2}" r="40" fill="none" stroke="#76ff03" stroke-width="1.5"/>
      </g>`;
      const r = rng(101), n = 25;
      for (let i = 0; i < n; i++) {
        const px = r() * W, py0 = r() * H, sp = 3 + r() * 8, rad = 2 + r() * 4;
        const py = ((py0 + t * sp) % H + H) % H, px2 = px + Math.sin(t * .8 + i) * 12;
        s += `<circle cx="${px2}" cy="${py}" r="${rad}" fill="#76ff03" opacity="${0.2 + r() * 0.35}"/>`;
      }
    }
    // 8. CANYON / WATERFALL (Devil's Kettle)
    else if (mode === 'canyon') {
      s += `<path d="M0,0 L180,0 L120,${H} L0,${H} Z" fill="#140f0c" opacity="0.6"/>
            <path d="M${W},0 L${W - 180},0 L${W - 120},${H} L${W},${H} Z" fill="#140f0c" opacity="0.6"/>`;
      const r = rng(55), n = 45;
      for (let i = 0; i < n; i++) {
        const px = 180 + r() * (W - 360), py0 = r() * H, sp = 25 + r() * 35, rad = 1.5 + r() * 3.5;
        const py = (py0 + t * sp) % H;
        s += `<circle cx="${px}" cy="${py}" r="${rad}" fill="#80deea" opacity="${0.2 + r() * 0.5}"/>`;
      }
    }
    // 9. STRATA / DEEP TIME (Silurian Hypothesis)
    else if (mode === 'strata') {
      const layers = [300, 600, 900, 1200, 1500];
      layers.forEach((ly, idx) => {
        const c = idx % 2 === 0 ? '#ffb74d' : '#8d6e63';
        s += `<line x1="60" y1="${ly}" x2="${W - 60}" y2="${ly}" stroke="${c}" stroke-width="2" stroke-dasharray="12,12" opacity="0.3"/>`;
      });
    }
    // 10. ABYSS / DEFAULT (Mariana Trench)
    else {
      if (bg.spotlight) {
        const sx = bg.spotlight.x || (W / 2), sw = bg.spotlight.w || 320;
        s += `<polygon filter="url(#blur6)" fill="url(#spot)" points="${sx - 40},-20 ${sx + 40},-20 ${sx + sw},${H} ${sx - sw},${H}"/>`;
      }
      if (bg.rays) {
        const r = rng(7);
        for (let i = 0; i < 6; i++) {
          const x = r() * W * 1.2 - 100, w = 70 + r() * 120, sk = 140 + r() * 180 + Math.sin(t * .4 + i) * 30;
          s += `<polygon filter="url(#blur6)" fill="#80d8ff" opacity="${0.06 + r() * .06}" points="${x},-50 ${x + w},-50 ${x + w + sk},${H + 50} ${x + sk - w * .6},${H + 50}"/>`;
        }
      }
      const r = rng(13), n = bg.particleCount || 40;
      for (let i = 0; i < n; i++) {
        const px = r() * W, py0 = r() * H, sp = 6 + r() * 14, rad = 1 + r() * 3.5;
        const py = ((py0 - t * sp) % H + H) % H, px2 = px + Math.sin(t * .5 + i) * 10;
        s += `<circle cx="${px2}" cy="${py}" r="${rad}" fill="#b0bec5" opacity="${0.12 + r() * .2}"/>`;
      }
    }

    if (bg.seabed) {
      const c = bg.seabed === 'sand' ? '#cdb98a' : '#0d1a20', y = bg.seabedY || (H - 180);
      s += `<path fill="${c}" stroke="${P.stroke}" stroke-width="${P.sw}" d="M-400,${y} C200,${y - 40} 500,${y + 30} 960,${y - 10} C1400,${y - 50} 1700,${y + 20} 2400,${y - 10} L2400,${H + 400} L-400,${H + 400} Z"/>`;
    }
    return s;
  }

  /* ---------------- overlay helpers ---------------- */
  function textEl(P, x, y, str, size, o = {}) {
    return `<text x="${x}" y="${y}" font-family="${P.font}" font-size="${size}" font-weight="${o.weight || 700}" fill="${o.fill || P.text}" text-anchor="${o.anchor || 'middle'}" letter-spacing="${o.ls || 0}" ${o.italic ? 'font-style="italic"' : ''} opacity="${o.op == null ? 1 : o.op}">${o.raw ? str : esc(str)}</text>`;
  }
  // "*word*" = highlight, "!word!" = alert colour
  function richSpans(P, text, caps, size) {
    return text.split(/(\*[^*]+\*|![^!]+!)/).filter(Boolean).map(seg => {
      let col = P.text, w = caps ? 800 : 400, s = seg;
      if (/^\*.*\*$/.test(seg)) { col = P.hl; w = 800; s = seg.slice(1, -1).toUpperCase(); }
      else if (/^!.*!$/.test(seg)) { col = '#e5383b'; w = 800; s = seg.slice(1, -1).toUpperCase(); }
      if (caps) s = s.toUpperCase();
      return `<tspan fill="${col}" font-weight="${w}" font-size="${/^\*|^!/.test(seg) && !caps ? size * 1.25 : size}">${esc(s)}</tspan>`;
    }).join('');
  }
  function wobbleEllipse(cx, cy, rx, ry, seed) {
    const r = rng(seed || 3), pts = []; const turns = 1.12;
    for (let i = 0; i <= 60; i++) {
      const a = -Math.PI * .6 + i / 60 * Math.PI * 2 * turns, k = 1 + (r() - .5) * .07 + i / 60 * .06;
      pts.push(`${(cx + Math.cos(a) * rx * k).toFixed(1)},${(cy + Math.sin(a) * ry * k).toFixed(1)}`);
    }
    return 'M' + pts.join(' L');
  }
  function fadeIn(t, t0, d = .35) { return easeOut(prog(t, t0, d)); }
  function life(t, e) { // returns opacity including optional out time
    let a = fadeIn(t, e.t0 || 0, e.fade || .35);
    if (e.t1 != null) a *= 1 - easeOut(prog(t, e.t1, .3));
    return a;
  }

  /* ---------------- elements ---------------- */
  const E = {};
  E.creature = (P, e, t) => {
    const a = life(t, e); if (a <= 0) return '';
    const lt = t - (e.t0 || 0);
    let x = e.x, y = e.y, s = e.scale || 1, rot = e.rotate || 0;
    if (e.swim) { x += (e.swim.vx || 0) * lt; y += (e.swim.vy || 0) * lt; }
    y += Math.sin(t * 1.6 + (e.phase || 0)) * (e.bob == null ? 4 : e.bob);
    if (e.approach) { const k = easeInOut(prog(t, e.approach.t0 ?? e.t0 ?? 0, e.approach.dur || 3)); s = lerp(e.approach.from, e.approach.to, k); }
    if (e.moveTo) { const k = easeInOut(prog(t, e.moveTo.t0 ?? e.t0 ?? 0, e.moveTo.dur || 2)); x = lerp(x, e.moveTo.x, k); y = lerp(y, e.moveTo.y, k); }
    const col = colorsFor(P, e.kind, e.mode), flip = e.flip ? -1 : 1;
    const glow = e.mode === 'sonar' ? 'filter="url(#glow)"' : '';
    const op = (e.opacity == null ? 1 : e.opacity) * a * (e.dim ? .45 : 1);
    const body = (C[e.kind] || C.blob)(e.mode === 'sonar' ? { ...P, stroke: '#39ff6a', sw: 3 } : P, col, t, e);
    let xray = '';
    if (e.mode === 'xray') xray = '';
    return `<g opacity="${op}" ${glow} transform="translate(${x} ${y}) rotate(${rot}) scale(${s * flip} ${s})">${body}${e.inner || ''}</g>`;
  };
  E.school = (P, e, t) => {
    const r = rng(e.seed || 5); let s = '';
    for (let i = 0; i < (e.count || 8); i++) {
      s += E.creature(P, { ...e, kind: e.kind || 'fish', x: e.x + (r() - .5) * (e.w || 400), y: e.y + (r() - .5) * (e.h || 160), scale: (e.scale || .3) * (.7 + r() * .5), phase: r() * 6 }, t);
    }
    return s;
  };
  E.caption = (P, e, t) => {
    const a = life(t, e); if (a <= 0) return '';
    const size = e.size || (P.isVertical ? 36 : (P.capsCaptions ? 38 : 42));
    const cx = e.x ?? (W / 2);
    const defaultY = e.pos === 'top' ? (P.isVertical ? 180 : 90) : e.pos === 'center' ? (H / 2) : (P.isVertical ? 1680 : 980);
    const y = e.y ?? defaultY;
    const caps = e.caps == null ? P.capsCaptions : e.caps;
    const dy = (1 - a) * 12;

    // Split text into lines: explicit lines array, \n, AND auto-wrapping per segment
    let rawLines = [];
    const maxC = e.maxChars || (P.isVertical ? 24 : 42);
    const rawSegments = typeof e.text === 'string' ? e.text.split('\n') : (Array.isArray(e.lines) ? e.lines : [String(e.text || '')]);
    for (const seg of rawSegments) {
      const words = seg.trim().split(/\s+/).filter(Boolean);
      let cur = '', inStar = false, inBang = false;
      for (const w of words) {
        const cleanLen = (cur + (cur ? ' ' : '') + w).replace(/[*!]/g, '').trim().length;
        if (cur && cleanLen > maxC) {
          let line = cur.trim();
          if (inStar && !line.endsWith('*')) line += '*';
          if (inBang && !line.endsWith('!')) line += '!';
          rawLines.push(line);
          cur = (inStar ? '*' : '') + (inBang ? '!' : '') + w;
        } else {
          cur = cur ? cur + ' ' + w : w;
        }
        const stars = (w.match(/\*/g) || []).length;
        if (stars % 2 === 1) inStar = !inStar;
        const bangs = (w.match(/!/g) || []).length;
        if (bangs % 2 === 1) inBang = !inBang;
      }
      if (cur) {
        let line = cur.trim();
        if (inStar && !line.endsWith('*')) line += '*';
        if (inBang && !line.endsWith('!')) line += '!';
        rawLines.push(line);
      }
    }
    if (rawLines.length === 0) return '';

    const lineH = e.lineHeight || (size * 1.34);
    const totalH = rawLines.length * lineH;
    const startY = y - (rawLines.length > 1 ? ((rawLines.length - 1) * lineH / 2) : 0);

    let pillMarkup = '';
    if (e.box !== false && e.backdrop !== false) {
      const maxChars = Math.max(...rawLines.map(l => l.replace(/[*!]/g, '').length));
      const boxW = Math.min(W - 120, Math.max(340, maxChars * size * 0.62 + 70));
      const boxH = totalH + size * 0.85;
      const boxY = startY - size * 0.95;
      const pillFill = e.boxColor || 'rgba(5, 12, 18, 0.88)';
      const pillStroke = e.borderColor || 'rgba(255, 255, 255, 0.16)';
      pillMarkup = `<rect x="${cx - boxW / 2}" y="${boxY}" width="${boxW}" height="${boxH}" rx="18" fill="${pillFill}" stroke="${pillStroke}" stroke-width="2.5" opacity="${a}"/>`;
    }

    let textMarkup = '';
    rawLines.forEach((line, i) => {
      const ly = startY + i * lineH + dy;
      textMarkup += `<text x="${cx}" y="${ly}" font-family="${P.font}" font-size="${size}" text-anchor="middle" letter-spacing="${caps ? 1 : 0}" opacity="${a}" style="paint-order:stroke fill" stroke="#03080c" stroke-opacity=".95" stroke-width="8" stroke-linejoin="round">${richSpans(P, line, caps, size)}</text>`;
    });

    if (e.underline) {
      const w = rawLines[rawLines.length - 1].length * size * .33;
      textMarkup += `<rect x="${cx - w}" y="${y + 16}" width="${w * 2 * easeOut(prog(t, (e.t0 || 0) + .1, .4))}" height="3" fill="${e.underlineColor || P.hl}" opacity="${a}"/>`;
    }

    return pillMarkup + textMarkup;
  };
  E.pill = (P, e, t) => {
    const a = life(t, e); if (a <= 0) return '';
    const size = e.size || 26, w = e.w || (e.text.length * size * .66 + (e.check ? 90 : 50)), h = size * 2;
    const dx = (1 - a) * -30, red = e.tone === 'red';
    let s = `<g opacity="${a}" transform="translate(${e.x + dx} ${e.y})"><rect width="${w}" height="${h}" rx="8" fill="${red ? '#5a1416' : P.pill}" opacity=".9"/>`;
    s += textEl(P, 24, h * .66, e.text.toUpperCase(), size, { anchor: 'start', fill: red ? '#ff6b6b' : P.text, weight: 800, ls: 1.5 });
    if (e.check) { const k = back(prog(t, e.t0 + .25, .3)); s += `<g transform="translate(${w - 38} ${h / 2}) scale(${k})"><circle r="15" fill="${P.good}"/><path d="M-7,0 L-2,6 L8,-6" fill="none" stroke="#0d2" stroke-width="0"/><path d="M-7,0 L-2,6 L8,-6" fill="none" stroke="#08311a" stroke-width="4" stroke-linecap="round"/></g>`; }
    return s + '</g>';
  };
  E.factstack = (P, e, t) => (e.items || []).map((it, i) => E.pill(P, { ...it, x: e.x, y: e.y + i * (e.gap || 70), w: e.w, size: e.size || 22, t1: e.t1 }, t)).join('');
  E.stamp = (P, e, t) => {
    const k = prog(t, e.t0, .25); if (k <= 0) return '';
    const sc = lerp(1.6, 1, back(k)), op = clamp(k * 3) * (e.t1 != null ? 1 - prog(t, e.t1, .3) : 1);
    const size = e.size || 54, w = e.text.length * size * .68 + 50, col = e.color || '#e5383b';
    const shake = k < 1 ? 0 : Math.max(0, .25 - (t - e.t0 - .25)) * Math.sin(t * 90) * 10;
    return `<g opacity="${op * .92}" transform="translate(${e.x + shake} ${e.y}) rotate(${e.rotate ?? -6}) scale(${sc})">
      <rect x="${-w / 2}" y="${-size * .8}" width="${w}" height="${size * 1.4}" fill="none" stroke="${col}" stroke-width="5" rx="4"/>
      ${textEl(P, 0, size * .32, e.text.toUpperCase(), size, { fill: col, weight: 800, ls: 2 })}</g>`;
  };
  E.circle = (P, e, t) => {
    const k = easeOut(prog(t, e.t0, e.dur || .45)); if (k <= 0) return '';
    const op = e.t1 != null ? 1 - prog(t, e.t1, .3) : 1;
    return `<path d="${wobbleEllipse(e.x, e.y, e.rx || 90, e.ry || e.rx || 90, e.seed)}" fill="none" stroke="${e.color || P.marker}" stroke-width="${e.width || 5}" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="${1 - k}" opacity="${op}"/>`;
  };
  E.redx = (P, e, t) => {
    const s = e.size || 90, k1 = easeOut(prog(t, e.t0, .2)), k2 = easeOut(prog(t, e.t0 + .18, .2)); if (k1 <= 0) return '';
    const c = e.color || '#e5383b';
    return `<g stroke="${c}" stroke-width="${e.width || 6}" stroke-linecap="round" fill="none" opacity="${e.t1 != null ? 1 - prog(t, e.t1, .3) : 1}">
      <path pathLength="1" stroke-dasharray="1" stroke-dashoffset="${1 - k1}" d="M${e.x - s},${e.y - s} L${e.x + s},${e.y + s}"/>
      <path pathLength="1" stroke-dasharray="1" stroke-dashoffset="${1 - k2}" d="M${e.x + s},${e.y - s} L${e.x - s},${e.y + s}"/></g>`;
  };
  E.tag = (P, e, t) => {
    const a = life(t, e); if (a <= 0) return '';
    const size = e.size || 26, x = e.x || 70, y = e.y || 80, txt = P.capsCaptions ? e.text.toUpperCase() : e.text;
    const w = txt.length * size * .58;
    return `<g opacity="${a}">${e.box ? `<rect x="${x - 14}" y="${y - size - 6}" width="${w + 28}" height="${size + 22}" rx="6" fill="${P.pill}" opacity=".85"/>` : ''}
      ${textEl(P, x, y, txt, size, { anchor: 'start', weight: 700, ls: P.capsCaptions ? 1.5 : 0 })}
      ${e.box ? '' : `<rect x="${x}" y="${y + 8}" width="${w * .55 * easeOut(prog(t, (e.t0 || 0) + .1, .4))}" height="2.5" fill="${P.hl}"/>`}</g>`;
  };
  E.reticle = (P, e, t) => {
    const k = easeOut(prog(t, e.t0, .5)); if (k <= 0) return '';
    const r = lerp(e.r * 1.8, e.r, k);
    return `<g fill="none" stroke="#dfe8ee" opacity="${.8 * k * (e.t1 != null ? 1 - prog(t, e.t1, .3) : 1)}"><circle cx="${e.x}" cy="${e.y}" r="${r}" stroke-width="3"/><circle cx="${e.x}" cy="${e.y}" r="${r * 2.6}" stroke-width="1.2" opacity=".5"/></g>`;
  };
  E.meter = (P, e, t) => {
    const a = life(t, e); if (a <= 0) return '';
    const x = e.x ?? 560, y = e.y ?? 520, w = e.w ?? 800, h = 26, k = easeInOut(prog(t, e.t0 + .3, e.dur || 1.6)) * (e.value ?? 1);
    let s = `<defs><linearGradient id="mg" x1="0" x2="1"><stop offset="0" stop-color="#3ecf6a"/><stop offset=".55" stop-color="#f2c94c"/><stop offset="1" stop-color="#e5383b"/></linearGradient>
      <clipPath id="mc"><rect x="${x}" y="${y}" width="${Math.max(h, w * k)}" height="${h}" rx="${h / 2}"/></clipPath></defs>
      <g opacity="${a}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${h / 2}" fill="#ffffff" opacity=".07"/>
      <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${h / 2}" fill="url(#mg)" clip-path="url(#mc)"/>`;
    if (e.number != null) { const n = Math.round(e.number * k / (e.value ?? 1)); s += textEl(P, x + w / 2, y + 120, `${n}${e.unit ? ' ' + e.unit : ''}`, 78, { weight: 800 }); }
    if (e.sub) s += textEl(P, x + w / 2, y + 160, e.sub, 22, { weight: 400, op: .6 });
    if (e.title) s += textEl(P, x + w / 2, y - 190, P.capsCaptions ? e.title.toUpperCase() : e.title, 40, { fill: P.hl, weight: 800, ls: 2 });
    const done = prog(t, e.t0 + .3 + (e.dur || 1.6), .8);
    if (done > 0 && done < 1) s += `<circle cx="${x + w * k}" cy="${y + h / 2}" r="${20 + done * 240}" fill="none" stroke="#fff" stroke-width="2" opacity="${(1 - done) * .6}"/>`;
    return s + '</g>';
  };
  E.isotype = (P, e, t) => {
    const a = life(t, e); if (a <= 0) return '';
    const cols = e.cols || 12, total = e.count || 60, cw = e.cell || 46, ch = e.rowH || 30, x0 = e.x ?? 300, y0 = e.y ?? 300;
    const shown = Math.floor(total * easeInOut(prog(t, e.t0 + .2, e.dur || 2.5)));
    const lostFrom = e.lostFrom ?? Infinity, lostK = e.lostT != null ? prog(t, e.lostT, 1.2) : 0;
    let s = `<g opacity="${a}">`;
    for (let i = 0; i < shown; i++) {
      const cx = x0 + (i % cols) * cw, cy = y0 + Math.floor(i / cols) * ch;
      const lost = i >= lostFrom && lostK > 0, fill = lost ? mix('#e8eef2', '#5a1a1e', lostK) : '#e8eef2';
      s += `<path transform="translate(${cx} ${cy}) scale(.1)" fill="${fill}" opacity="${lost ? 1 - lostK * .6 : .95}" d="M182,-8 C186,-46 150,-56 60,-54 L-110,-36 C-160,-26 -190,-10 -202,0 L-250,-30 L-240,0 L-250,30 L-202,0 C-190,10 -160,22 -110,30 L60,50 C150,54 186,42 182,8 Z"/>`;
    }
    if (e.label) s += textEl(P, x0 + cols * cw / 2, y0 - 70, P.capsCaptions ? e.label.toUpperCase() : e.label, 28, { ls: 1.5 });
    if (e.legend) s += textEl(P, x0 - 20, 1000, e.legend.toUpperCase(), 16, { anchor: 'start', op: .5 });
    if (e.counter) {
      const c = e.counter, k = prog(t, e.t0 + .2, e.dur || 2.5), v = Math.round(lerp(c.from || 0, c.to, easeInOut(k)) / (c.round || 1)) * (c.round || 1);
      const bx = x0 + cols * cw + 60;
      s += `<rect x="${bx}" y="${y0 + 40}" width="300" height="130" rx="10" fill="${P.pill}" opacity=".9"/>` +
        textEl(P, bx + 150, y0 + 115, `${c.prefix || ''}${v.toLocaleString('en-US')}`, 48, { weight: 800, fill: c.color || P.text }) +
        (c.sub ? textEl(P, bx + 150, y0 + 150, c.sub.toUpperCase(), 15, { op: .6 }) : '');
    }
    return s + '</g>';
  };
  E.sonar = (P, e, t) => {
    const a = life(t, e); if (a <= 0) return '';
    const cx = e.x ?? 220, cy = e.y ?? 540, R = e.r ?? 1700, ang = e.spread ?? 50;
    let s = `<g opacity="${a}" stroke="#39ff6a" fill="none">`;
    for (let i = 1; i <= 6; i++) s += `<path stroke-width="1" opacity=".25" d="M${cx + Math.cos(-ang * Math.PI / 180) * R * i / 6},${cy + Math.sin(-ang * Math.PI / 180) * R * i / 6} A${R * i / 6},${R * i / 6} 0 0 1 ${cx + Math.cos(ang * Math.PI / 180) * R * i / 6},${cy + Math.sin(ang * Math.PI / 180) * R * i / 6}"/>`;
    for (let d = -ang; d <= ang; d += ang / 3) s += `<line stroke-width="1" opacity=".2" x1="${cx}" y1="${cy}" x2="${cx + Math.cos(d * Math.PI / 180) * R}" y2="${cy + Math.sin(d * Math.PI / 180) * R}"/>`;
    const sw = Math.sin((t - e.t0) * (e.speed || 1.2)) * ang;
    s += `<line stroke-width="3" filter="url(#glow)" x1="${cx}" y1="${cy}" x2="${cx + Math.cos(sw * Math.PI / 180) * R}" y2="${cy + Math.sin(sw * Math.PI / 180) * R}"/></g>`;
    (e.blips || []).forEach(b => { const k = fadeIn(t, b.t, .3); if (k > 0) s += textEl(P, b.x, b.y, b.label.toUpperCase(), 24, { fill: '#39ff6a', weight: 800, op: k * a }); });
    return s;
  };
  E.gridlines = (P, e, t) => {
    const a = life(t, e); if (a <= 0) return '';
    return `<g opacity="${a}">` + (e.lines || []).map(l => `<line x1="0" x2="${W}" y1="${l.y}" y2="${l.y}" stroke="#fff" stroke-opacity=".12" stroke-width="2"/>${textEl(P, 30, l.y - 10, l.label, 24, { anchor: 'start', op: .55, weight: 500 })}`).join('') + '</g>';
  };
  E.namecard = (P, e, t) => {
    const a = life(t, e); if (a <= 0) return '';
    const w = e.w || 300;
    return `<g opacity="${a}" transform="translate(${e.x} ${e.y + (1 - a) * 20})"><rect x="${-w / 2}" y="-44" width="${w}" height="${e.sub ? 92 : 70}" rx="6" fill="#0d1419" opacity=".85" stroke="#e9eef2" stroke-width="2.5"/>
      ${textEl(P, 0, 4, e.title, 36, { weight: 800 })}${e.sub ? textEl(P, 0, 36, e.sub, 18, { weight: 400, op: .65 }) : ''}</g>`;
  };
  E.doccard = (P, e, t) => {
    const a = life(t, e); if (a <= 0) return '';
    const w = e.w || 560, h = e.h || 640, x = e.x ?? 960, y = e.y ?? 540;
    let s = `<g opacity="${a}" transform="translate(${x} ${y + (1 - a) * 30}) rotate(${e.rotate || -1})"><rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" fill="#e7e3d8" rx="3"/>`;
    if (e.header) s += textEl(P, 0, -h / 2 + 70, e.header.toUpperCase(), 20, { fill: '#555', ls: 1 });
    if (e.title) e.title.split('\n').forEach((l, i) => s += textEl(P, 0, -h / 2 + 150 + i * 46, l.toUpperCase(), 38, { fill: '#2a2a2a', weight: 800 }));
    for (let i = 0; i < 6; i++) s += `<rect x="${-w / 2 + 60}" y="${-h / 2 + 280 + i * 40}" width="${(w - 120) * (i % 3 === 2 ? .6 : 1)}" height="10" rx="5" fill="#9a968d" opacity=".5"/>`;
    if (e.footer) s += textEl(P, 0, h / 2 - 50, e.footer.toUpperCase(), 20, { fill: '#555' });
    return s + '</g>';
  };
  E.checklist = (P, e, t) => {
    const a = life(t, e); if (a <= 0) return '';
    const x = e.x ?? 700, y = e.y ?? 380;
    let s = `<g opacity="${a}"><rect x="${x - 30}" y="${y - 70}" width="${e.w || 560}" height="${(e.items.length) * 70 + 100}" rx="12" fill="${P.pill}" opacity=".85"/>`;
    if (e.title) s += textEl(P, x, y - 20, e.title.toUpperCase(), 22, { anchor: 'start', fill: P.hl, weight: 800, ls: 1 });
    e.items.forEach((it, i) => {
      const iy = y + 40 + i * 70, k = fadeIn(t, (e.t0 || 0) + .15 * i, .3), ck = it.check != null ? back(prog(t, it.check, .25)) : 0;
      s += `<g opacity="${k}"><rect x="${x}" y="${iy - 24}" width="32" height="32" rx="4" fill="none" stroke="#e9eef2" stroke-width="3"/>
        ${ck > 0 ? `<path transform="translate(${x + 16} ${iy - 8}) scale(${ck})" d="M-9,0 L-3,8 L11,-10" fill="none" stroke="${P.good}" stroke-width="5" stroke-linecap="round"/>` : ''}
        ${textEl(P, x + 56, iy + 2, it.text, 32, { anchor: 'start', weight: 500 })}</g>`;
    });
    return s + '</g>';
  };
  E.bignumber = (P, e, t) => {
    const a = life(t, e); if (a <= 0) return '';
    const k = easeOut(prog(t, e.t0, e.dur || 1)), v = Math.round(lerp(e.from || 0, e.to, k));
    return textEl(P, e.x ?? 960, e.y ?? 600, `${e.prefix || ''}${v.toLocaleString('en-US')}${e.suffix || ''}`, e.size || 160, { weight: 800, fill: e.color || P.hl, op: a });
  };
  E.bracket = (P, e, t) => { // measurement bracket
    const k = easeOut(prog(t, e.t0, .5)); if (k <= 0) return '';
    const x2 = lerp(e.x1, e.x2, k), y2 = lerp(e.y1, e.y2, k), c = e.color || P.marker;
    return `<g stroke="${c}" stroke-width="4" fill="none"><line x1="${e.x1}" y1="${e.y1}" x2="${x2}" y2="${y2}"/></g>${e.label ? textEl(P, (e.x1 + e.x2) / 2, Math.max(e.y1, e.y2) + 50, e.label, 34, { fill: c, op: k }) : ''}`;
  };
  E.marker = (P, e, t) => { // numbered evidence cone
    const k = back(prog(t, e.t0, .3)); if (k <= 0) return '';
    return `<g transform="translate(${e.x} ${e.y}) scale(${k})"><path d="M-30,0 L-20,-60 L20,-60 L30,0 Z" fill="#f2c51c" stroke="#5a4a00" stroke-width="2"/>${textEl(P, 0, -18, e.n, 32, { fill: '#1a1a1a', weight: 800 })}</g>`;
  };
  E.tooth = (P, e, t) => { // fossil tooth (ink style hero object)
    const a = life(t, e); if (a <= 0) return '';
    const s = e.scale || 1, cusps = e.cusps !== false;
    return `<g opacity="${a}" transform="translate(${e.x} ${e.y}) scale(${s})">
      <path fill="#c8a06a" stroke="${P.stroke}" stroke-width="${P.sw}" d="M-150,40 C-160,90 -100,110 -50,90 L0,70 L50,90 C100,110 160,90 150,40 Z"/>
      <path fill="#5a6570" stroke="${P.stroke}" stroke-width="${P.sw}" d="M-120,50 C-60,10 -30,-120 0,-200 C30,-120 60,10 120,50 C60,30 -60,30 -120,50 Z"/>
      <path fill="#8794a0" opacity=".5" d="M0,-190 C-10,-120 -30,-20 -60,30 C-20,22 -10,22 -4,22 Z"/>
      ${cusps ? `<path fill="#5a6570" stroke="${P.stroke}" stroke-width="${P.sw}" d="M-150,50 L-128,-10 L-108,48 Z"/><path fill="#5a6570" stroke="${P.stroke}" stroke-width="${P.sw}" d="M150,50 L128,-10 L108,48 Z"/>` : ''}</g>`;
  };
  E.rect = (P, e, t) => { const a = life(t, e); return a > 0 ? `<rect x="${e.x}" y="${e.y}" width="${e.w}" height="${e.h}" rx="${e.rx || 0}" fill="${e.fill || '#000'}" opacity="${a * (e.opacity ?? 1)}"/>` : ''; };
  E.svg = (P, e, t) => { const a = life(t, e); return a > 0 ? `<g opacity="${a}">${e.markup}</g>` : ''; };

  /* ---------------- frame ---------------- */
  function findShot(spec, t) {
    for (const s of spec.shots) if (t >= s.start && t < s.end) return s;
    return spec.shots[spec.shots.length - 1];
  }
  function render(spec, t) {
    W = spec.width || 1920;
    H = spec.height || 1080;
    const P = { ...PRESETS[spec.preset || 'abyss'], ...(spec.tokens || {}) };
    P.isVertical = W < H;
    P.W = W;
    P.H = H;
    const shot = findShot(spec, t), lt = t - shot.start, dur = shot.end - shot.start;
    const cam = shot.camera || {}, ck = easeInOut(lt / dur);
    const z = lerp(cam.zoomFrom ?? 1, cam.zoomTo ?? cam.zoomFrom ?? 1, ck);
    const fx = cam.x ?? (W / 2), fy = cam.y ?? (H / 2), px = lerp(0, cam.panX || 0, ck), py = lerp(0, cam.panY || 0, ck);
    const world = [], over = [];
    (shot.elements || []).forEach(e => {
      const fn = E[e.type]; if (!fn) return;
      const out = fn(P, e, lt); (e.layer === 'overlay' || (e.layer == null && !['creature', 'school', 'tooth', 'marker', 'svg', 'rect'].includes(e.type)) ? over : world).push(out);
    });
    // fade from/to black around shot edges if requested
    const fin = shot.fadeIn ? 1 - prog(lt, 0, shot.fadeIn) : 0, fout = shot.fadeOut ? prog(lt, dur - shot.fadeOut, shot.fadeOut) : 0;
    const grain = spec.grain ?? .05;
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="100%" height="100%" style="display:block;width:100%;height:100%;background:#000">
      <g transform="translate(${fx + px} ${fy + py}) scale(${z}) translate(${-fx} ${-fy})">${background(P, shot.bg || {}, t, cam)}${world.join('')}</g>
      ${over.join('')}
      <defs><radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="${shot.vignette ?? .75}"/></radialGradient>
      <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="${Math.floor(t * 30) % 97}"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1.4 -0.4"/></filter></defs>
      <rect width="${W}" height="${H}" fill="url(#vig)"/>
      ${grain > 0 ? `<rect width="${W}" height="${H}" filter="url(#grain)" opacity="${grain}"/>` : ''}
      ${fin + fout > 0 ? `<rect width="${W}" height="${H}" fill="#000" opacity="${clamp(fin + fout)}"/>` : ''}</svg>`;
    document.getElementById('stage').innerHTML = svg;
  }
  window.KZ = { render, PRESETS, elements: Object.keys(E), creatures: Object.keys(C) };
})();
