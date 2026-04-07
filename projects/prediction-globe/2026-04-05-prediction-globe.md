# Prediction Globe Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a 3D interactive globe that visualizes Polymarket prediction market events as glowing markers positioned by geographic relevance.

**Architecture:** Single HTML file (`prediction-globe.html`) with inline CSS and JS. Three.js (CDN) renders a textured Earth sphere with atmosphere shader, star background, and instanced marker points. Polymarket Gamma API provides event data; a keyword-to-coordinates lookup table handles geo-positioning. DOM overlays handle tooltips, sidebar, and controls.

**Tech Stack:** HTML5, CSS3, JavaScript (ES modules), Three.js r160+ (CDN), Polymarket Gamma API

---

## File Structure

- **Create:** `prediction-globe.html` — single self-contained page with all HTML, CSS, and JS inline

---

### Task 1: HTML Scaffold + Three.js Scene

**Files:**
- Create: `prediction-globe.html`

Set up the HTML page with Three.js scene, camera, renderer, OrbitControls, and animation loop. Dark background, nothing rendered yet except a black canvas.

- [ ] **Step 1: Create the HTML file with base structure**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Prediction Globe</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      overflow: hidden;
      background: #000;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      color: #fff;
    }
    #canvas-container {
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
    }
  </style>
</head>
<body>
  <div id="canvas-container"></div>

  <script type="importmap">
  {
    "imports": {
      "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
      "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
    }
  }
  </script>
  <script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

    // --- Scene Setup ---
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 0, 3);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000);
    document.getElementById('canvas-container').appendChild(renderer.domElement);

    // --- Controls ---
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 1.5;
    controls.maxDistance = 6;
    controls.enablePan = false;

    // --- Resize ---
    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // --- Animation Loop ---
    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }
    animate();
  </script>
</body>
</html>
```

- [ ] **Step 2: Verify in browser**

Open `prediction-globe.html` in a browser. Expected: black screen, no errors in console. Mouse drag/scroll should work (OrbitControls active but nothing to see yet).

- [ ] **Step 3: Commit**

```bash
git add prediction-globe.html
git commit -m "feat(prediction-globe): scaffold HTML with Three.js scene and OrbitControls"
```

---

### Task 2: Earth Sphere + Atmosphere + Stars

**Files:**
- Modify: `prediction-globe.html`

Add the earth sphere with a procedural texture (dark landmass style), atmosphere glow shader, and star particle background. Use a procedural approach to avoid external texture dependencies for initial development — can swap in NASA texture later.

- [ ] **Step 1: Add star background after the Controls section**

Insert after `controls.enablePan = false;`:

```javascript
    // --- Stars ---
    const starGeometry = new THREE.BufferGeometry();
    const starCount = 3000;
    const starPositions = new Float32Array(starCount * 3);
    for (let i = 0; i < starCount * 3; i++) {
      starPositions[i] = (Math.random() - 0.5) * 200;
    }
    starGeometry.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
    const starMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 0.15, sizeAttenuation: true });
    scene.add(new THREE.Points(starGeometry, starMaterial));
```

- [ ] **Step 2: Add Earth sphere with texture loader**

Insert after the stars block:

```javascript
    // --- Earth ---
    const EARTH_RADIUS = 1;
    const earthGeometry = new THREE.SphereGeometry(EARTH_RADIUS, 64, 64);

    // Use a dark-style earth texture from a public CDN
    const textureLoader = new THREE.TextureLoader();
    const earthTexture = textureLoader.load(
      'https://unpkg.com/three-globe@2.31.1/example/img/earth-night.jpg'
    );
    const earthMaterial = new THREE.MeshPhongMaterial({
      map: earthTexture,
      bumpScale: 0.02,
    });
    const earth = new THREE.Mesh(earthGeometry, earthMaterial);
    scene.add(earth);

    // Ambient + directional light
    scene.add(new THREE.AmbientLight(0x333366, 1.5));
    const sunLight = new THREE.DirectionalLight(0xffffff, 1.0);
    sunLight.position.set(5, 3, 5);
    scene.add(sunLight);
```

- [ ] **Step 3: Add atmosphere glow**

Insert after the earth block:

```javascript
    // --- Atmosphere ---
    const atmosphereVertexShader = `
      varying vec3 vNormal;
      void main() {
        vNormal = normalize(normalMatrix * normal);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;
    const atmosphereFragmentShader = `
      varying vec3 vNormal;
      void main() {
        float intensity = pow(0.65 - dot(vNormal, vec3(0.0, 0.0, 1.0)), 2.0);
        gl_FragColor = vec4(0.3, 0.6, 1.0, 1.0) * intensity;
      }
    `;
    const atmosphereMesh = new THREE.Mesh(
      new THREE.SphereGeometry(EARTH_RADIUS * 1.15, 64, 64),
      new THREE.ShaderMaterial({
        vertexShader: atmosphereVertexShader,
        fragmentShader: atmosphereFragmentShader,
        blending: THREE.AdditiveBlending,
        side: THREE.BackSide,
        transparent: true,
      })
    );
    scene.add(atmosphereMesh);
```

- [ ] **Step 4: Add slow auto-rotation in the animate loop**

Modify the animate function:

```javascript
    function animate() {
      requestAnimationFrame(animate);
      earth.rotation.y += 0.0005;
      controls.update();
      renderer.render(scene, camera);
    }
```

- [ ] **Step 5: Verify in browser**

Expected: Dark earth globe with night lights texture, blue atmospheric glow, starfield background, slow rotation, mouse orbit works.

- [ ] **Step 6: Commit**

```bash
git add prediction-globe.html
git commit -m "feat(prediction-globe): add Earth sphere with night texture, atmosphere glow, and stars"
```

---

### Task 3: Polymarket API + Geo Matching

**Files:**
- Modify: `prediction-globe.html`

Add data fetching from Polymarket Gamma API and the geo-location keyword matching system. No rendering yet — just data processing.

- [ ] **Step 1: Add geo-location mapping table**

Insert before the `// --- Scene Setup ---` line:

```javascript
    // --- Geo Location Database ---
    const GEO_KEYWORDS = {
      // North America
      'trump': [38.9, -77.0], 'biden': [38.9, -77.0], 'us ': [38.9, -77.0],
      'united states': [38.9, -77.0], 'america': [38.9, -77.0], 'congress': [38.9, -77.0],
      'senate': [38.9, -77.0], 'democrat': [38.9, -77.0], 'republican': [38.9, -77.0],
      'fed ': [38.9, -77.0], 'federal reserve': [38.9, -77.0],
      'canada': [56.1, -106.3], 'mexico': [23.6, -102.5],
      // Europe
      'ukraine': [50.4, 30.5], 'zelensky': [50.4, 30.5], 'russia': [55.7, 37.6],
      'putin': [55.7, 37.6], 'uk ': [51.5, -0.1], 'britain': [51.5, -0.1],
      'england': [51.5, -0.1], 'france': [48.8, 2.3], 'macron': [48.8, 2.3],
      'germany': [52.5, 13.4], 'italy': [41.9, 12.5], 'spain': [40.4, -3.7],
      'eu ': [50.8, 4.4], 'european': [50.8, 4.4], 'nato': [50.8, 4.4],
      'poland': [52.2, 21.0], 'turkey': [39.9, 32.9], 'erdogan': [39.9, 32.9],
      // Asia
      'china': [39.9, 116.4], 'xi jinping': [39.9, 116.4], 'beijing': [39.9, 116.4],
      'japan': [35.7, 139.7], 'india': [28.6, 77.2], 'modi': [28.6, 77.2],
      'korea': [37.5, 127.0], 'taiwan': [25.0, 121.5], 'iran': [35.7, 51.4],
      'israel': [31.8, 35.2], 'gaza': [31.5, 34.5], 'palestine': [31.9, 35.2],
      'saudi': [24.7, 46.7], 'syria': [33.5, 36.3], 'iraq': [33.3, 44.4],
      // South America
      'brazil': [-14.2, -51.9], 'argentina': [-38.4, -63.6],
      // Africa
      'nigeria': [9.1, 7.5], 'south africa': [-30.6, 22.9], 'egypt': [26.8, 30.8],
      // Oceania
      'australia': [-25.3, 133.8],
      // Global/Crypto — no fixed location
      'bitcoin': null, 'btc': null, 'ethereum': null, 'eth': null, 'crypto': null,
      'solana': null, 'sol ': null, 'ai ': null, 'openai': [37.8, -122.4],
      'spacex': [25.9, -97.2], 'tesla': [30.2, -97.7], 'elon': [30.2, -97.7],
    };

    function matchGeoLocation(title, description) {
      const text = (title + ' ' + description).toLowerCase();
      for (const [keyword, coords] of Object.entries(GEO_KEYWORDS)) {
        if (coords && text.includes(keyword)) {
          return { lat: coords[0], lng: coords[1], keyword };
        }
      }
      return null;
    }

    function latLngToVector3(lat, lng, radius) {
      const phi = (90 - lat) * (Math.PI / 180);
      const theta = (lng + 180) * (Math.PI / 180);
      return new THREE.Vector3(
        -(radius * Math.sin(phi) * Math.cos(theta)),
        radius * Math.cos(phi),
        radius * Math.sin(phi) * Math.sin(theta)
      );
    }

    function distributeGlobal(index, total) {
      // Golden angle distribution for even spacing
      const phi = Math.acos(1 - 2 * (index + 0.5) / total);
      const theta = Math.PI * (1 + Math.sqrt(5)) * index;
      const lat = 90 - (phi * 180 / Math.PI);
      const lng = (theta * 180 / Math.PI) % 360 - 180;
      return { lat, lng };
    }
```

- [ ] **Step 2: Add Polymarket data fetching**

Insert after the geo functions:

```javascript
    // --- Polymarket Data ---
    const POLYMARKET_API = 'https://gamma-api.polymarket.com';

    async function fetchEvents() {
      try {
        const res = await fetch(`${POLYMARKET_API}/events?limit=50&order=volume24hr&ascending=false&active=true`);
        if (!res.ok) throw new Error(`API error: ${res.status}`);
        const events = await res.json();
        localStorage.setItem('prediction-globe-cache', JSON.stringify({ events, timestamp: Date.now() }));
        return events;
      } catch (err) {
        console.warn('API fetch failed, trying cache:', err);
        const cached = localStorage.getItem('prediction-globe-cache');
        if (cached) {
          const { events } = JSON.parse(cached);
          return events;
        }
        return [];
      }
    }

    function processEvents(events) {
      let globalIndex = 0;
      let globalTotal = events.filter(e => !matchGeoLocation(e.title, e.description || '')).length;

      return events.map(event => {
        const geo = matchGeoLocation(event.title, event.description || '');
        let lat, lng;

        if (geo) {
          // Add small random offset to prevent stacking
          lat = geo.lat + (Math.random() - 0.5) * 5;
          lng = geo.lng + (Math.random() - 0.5) * 5;
        } else {
          const pos = distributeGlobal(globalIndex++, Math.max(globalTotal, 1));
          lat = pos.lat;
          lng = pos.lng;
        }

        // Get top market probability
        const topMarket = event.markets?.[0];
        const probability = topMarket ? parseFloat(topMarket.outcomePrices?.[0] || '0.5') : 0.5;

        return {
          id: event.id,
          title: event.title,
          description: event.description || '',
          slug: event.slug,
          probability,
          volume: event.volume24hr || 0,
          totalVolume: event.volume || 0,
          liquidity: event.liquidity || 0,
          image: event.image,
          markets: event.markets || [],
          lat,
          lng,
          geoMatched: !!geo,
        };
      });
    }
```

- [ ] **Step 3: Verify API call works**

Add a temporary test at the end of the script (before closing `</script>`):

```javascript
    // Temporary test — remove after verification
    fetchEvents().then(events => {
      const processed = processEvents(events);
      console.log(`Loaded ${processed.length} events`, processed.slice(0, 3));
    });
```

Open browser, check console. Expected: array of ~50 events with lat/lng coordinates, probability, volume fields. Then remove the temporary test.

- [ ] **Step 4: Commit**

```bash
git add prediction-globe.html
git commit -m "feat(prediction-globe): add Polymarket API fetch and geo-location matching"
```

---

### Task 4: Marker Points + Light Beams

**Files:**
- Modify: `prediction-globe.html`

Render glowing marker points and vertical light beams on the earth surface based on fetched event data.

- [ ] **Step 1: Add marker rendering module**

Insert after the `processEvents` function:

```javascript
    // --- Markers ---
    const markers = [];
    const markerGroup = new THREE.Group();
    scene.add(markerGroup);

    function probabilityToColor(p) {
      // Green (high yes) → Yellow (uncertain) → Red (high no)
      if (p > 0.5) {
        const t = (p - 0.5) * 2; // 0..1
        return new THREE.Color().setHSL(0.3 * t, 1.0, 0.5); // yellow to green
      } else {
        const t = p * 2; // 0..1
        return new THREE.Color().setHSL(0.0 + 0.15 * t, 1.0, 0.5); // red to yellow
      }
    }

    function volumeToScale(volume, maxVolume) {
      const normalized = Math.log1p(volume) / Math.log1p(maxVolume);
      return 0.01 + normalized * 0.03; // marker radius range
    }

    function volumeToBeamHeight(volume, maxVolume) {
      const normalized = Math.log1p(volume) / Math.log1p(maxVolume);
      return 0.05 + normalized * 0.3;
    }

    function createMarkers(processedEvents) {
      // Clear old markers
      markerGroup.clear();
      markers.length = 0;

      const maxVolume = Math.max(...processedEvents.map(e => e.volume), 1);

      processedEvents.forEach(event => {
        const color = probabilityToColor(event.probability);
        const scale = volumeToScale(event.volume, maxVolume);
        const beamHeight = volumeToBeamHeight(event.volume, maxVolume);
        const surfacePos = latLngToVector3(event.lat, event.lng, EARTH_RADIUS * 1.005);

        // Glowing dot
        const dotGeo = new THREE.SphereGeometry(scale, 12, 12);
        const dotMat = new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.9 });
        const dot = new THREE.Mesh(dotGeo, dotMat);
        dot.position.copy(surfacePos);
        markerGroup.add(dot);

        // Pulse ring
        const ringGeo = new THREE.RingGeometry(scale * 1.2, scale * 2.5, 24);
        const ringMat = new THREE.MeshBasicMaterial({
          color, transparent: true, opacity: 0.4, side: THREE.DoubleSide
        });
        const ring = new THREE.Mesh(ringGeo, ringMat);
        ring.position.copy(surfacePos);
        ring.lookAt(new THREE.Vector3(0, 0, 0)); // face outward
        ring.lookAt(ring.position.clone().multiplyScalar(2)); // face away from center
        markerGroup.add(ring);

        // Light beam
        const beamGeo = new THREE.CylinderGeometry(scale * 0.3, scale * 0.1, beamHeight, 8);
        const beamMat = new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.3 });
        const beam = new THREE.Mesh(beamGeo, beamMat);
        // Position beam above surface
        const normal = surfacePos.clone().normalize();
        beam.position.copy(surfacePos.clone().add(normal.clone().multiplyScalar(beamHeight / 2)));
        beam.lookAt(new THREE.Vector3(0, 0, 0));
        beam.rotateX(Math.PI / 2);
        markerGroup.add(beam);

        markers.push({
          event,
          dot,
          ring,
          beam,
          baseScale: scale,
          surfacePos,
        });
      });
    }
```

- [ ] **Step 2: Add pulse animation to the animate loop**

Modify the animate function:

```javascript
    let time = 0;
    function animate() {
      requestAnimationFrame(animate);
      time += 0.016;
      earth.rotation.y += 0.0005;

      // Pulse markers
      markers.forEach(m => {
        const pulse = 1 + 0.3 * Math.sin(time * 2 + m.event.volume * 0.001);
        m.ring.scale.set(pulse, pulse, pulse);
        m.ring.material.opacity = 0.4 * (1 - (pulse - 1) / 0.3);
      });

      controls.update();
      renderer.render(scene, camera);
    }
```

- [ ] **Step 3: Load data and create markers on page load**

Replace the temporary test (or add at the end of script) with:

```javascript
    // --- Initialize ---
    let processedEvents = [];

    async function init() {
      const events = await fetchEvents();
      processedEvents = processEvents(events);
      createMarkers(processedEvents);
    }
    init();
```

- [ ] **Step 4: Make markers rotate with earth**

Add `markerGroup` to earth rotation. Modify animate:

```javascript
      earth.rotation.y += 0.0005;
      markerGroup.rotation.y = earth.rotation.y;
```

- [ ] **Step 5: Verify in browser**

Expected: Earth with glowing colored dots at various positions, light beams extending upward, pulsing ring animations. Larger dots for high-volume markets, color varies by probability.

- [ ] **Step 6: Commit**

```bash
git add prediction-globe.html
git commit -m "feat(prediction-globe): add colored marker points with light beams and pulse animation"
```

---

### Task 5: Hover Tooltip

**Files:**
- Modify: `prediction-globe.html`

Add raycaster-based hover detection and a floating tooltip card with glassmorphism effect.

- [ ] **Step 1: Add tooltip HTML and CSS**

Add inside `<body>`, before `<div id="canvas-container">`:

```html
  <!-- Tooltip -->
  <div id="tooltip" style="display:none; position:fixed; pointer-events:none; z-index:100;
    background: rgba(10,15,30,0.85); backdrop-filter: blur(12px); border: 1px solid rgba(100,150,255,0.3);
    border-radius: 12px; padding: 16px; max-width: 300px; box-shadow: 0 0 20px rgba(50,100,255,0.2);">
    <div id="tooltip-title" style="font-size:14px; font-weight:600; margin-bottom:8px; line-height:1.3;"></div>
    <div style="display:flex; align-items:baseline; gap:8px; margin-bottom:6px;">
      <span id="tooltip-prob" style="font-size:28px; font-weight:700;"></span>
      <span id="tooltip-prob-label" style="font-size:12px; opacity:0.6;">chance</span>
    </div>
    <div id="tooltip-volume" style="font-size:12px; opacity:0.6;"></div>
  </div>
```

- [ ] **Step 2: Add raycaster hover logic**

Insert after the `init()` call:

```javascript
    // --- Raycaster / Hover ---
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let hoveredMarker = null;
    let lastRaycastTime = 0;

    const tooltip = document.getElementById('tooltip');
    const tooltipTitle = document.getElementById('tooltip-title');
    const tooltipProb = document.getElementById('tooltip-prob');
    const tooltipVolume = document.getElementById('tooltip-volume');

    function formatVolume(v) {
      if (v >= 1e6) return `$${(v / 1e6).toFixed(1)}M`;
      if (v >= 1e3) return `$${(v / 1e3).toFixed(0)}K`;
      return `$${v.toFixed(0)}`;
    }

    renderer.domElement.addEventListener('mousemove', (e) => {
      mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

      // Throttle raycasting to ~30fps
      const now = performance.now();
      if (now - lastRaycastTime < 33) return;
      lastRaycastTime = now;

      raycaster.setFromCamera(mouse, camera);
      const dots = markers.map(m => m.dot);
      const intersects = raycaster.intersectObjects(dots);

      if (intersects.length > 0) {
        const hit = intersects[0].object;
        const marker = markers.find(m => m.dot === hit);
        if (marker) {
          hoveredMarker = marker;
          renderer.domElement.style.cursor = 'pointer';
          tooltipTitle.textContent = marker.event.title;
          tooltipProb.textContent = `${(marker.event.probability * 100).toFixed(0)}%`;
          tooltipProb.style.color = `#${probabilityToColor(marker.event.probability).getHexString()}`;
          tooltipVolume.textContent = `24h Volume: ${formatVolume(marker.event.volume)}`;
          tooltip.style.display = 'block';
          tooltip.style.left = `${e.clientX + 16}px`;
          tooltip.style.top = `${e.clientY - 16}px`;
        }
      } else {
        hoveredMarker = null;
        renderer.domElement.style.cursor = 'default';
        tooltip.style.display = 'none';
      }
    });
```

- [ ] **Step 3: Verify in browser**

Expected: Hovering over a marker dot shows a glassmorphism tooltip with title, probability percentage (colored), and 24h volume. Tooltip follows mouse. Moving away hides it.

- [ ] **Step 4: Commit**

```bash
git add prediction-globe.html
git commit -m "feat(prediction-globe): add hover tooltip with raycaster detection"
```

---

### Task 6: Click → Sidebar Detail Panel

**Files:**
- Modify: `prediction-globe.html`

Add a side panel that slides in when a marker is clicked, with event details, probability bar, and link to Polymarket.

- [ ] **Step 1: Add sidebar HTML and CSS**

Add inside `<style>`:

```css
    #sidebar {
      position: fixed; top: 0; right: -400px; width: 400px; height: 100%;
      background: rgba(10, 15, 30, 0.92); backdrop-filter: blur(20px);
      border-left: 1px solid rgba(100, 150, 255, 0.2);
      z-index: 200; padding: 24px; overflow-y: auto;
      transition: right 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    #sidebar.open { right: 0; }
    #sidebar-close {
      position: absolute; top: 16px; right: 16px; background: none; border: none;
      color: #fff; font-size: 24px; cursor: pointer; opacity: 0.6; line-height: 1;
    }
    #sidebar-close:hover { opacity: 1; }
    #sidebar-title { font-size: 20px; font-weight: 700; margin-bottom: 16px; padding-right: 32px; line-height: 1.4; }
    #sidebar-desc { font-size: 14px; opacity: 0.7; margin-bottom: 20px; line-height: 1.5; }
    .prob-bar-container { margin-bottom: 20px; }
    .prob-bar-label { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; }
    .prob-bar { height: 28px; border-radius: 14px; overflow: hidden; display: flex; background: rgba(255,255,255,0.1); }
    .prob-bar-yes { background: #22c55e; transition: width 0.5s; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 600; }
    .prob-bar-no { background: #ef4444; transition: width 0.5s; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 600; }
    .sidebar-stat { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.08); font-size: 14px; }
    .sidebar-stat-label { opacity: 0.5; }
    #sidebar-link {
      display: block; text-align: center; margin-top: 24px; padding: 12px;
      background: rgba(100, 150, 255, 0.2); border: 1px solid rgba(100, 150, 255, 0.4);
      border-radius: 8px; color: #7db4ff; text-decoration: none; font-weight: 600; font-size: 14px;
      transition: background 0.2s;
    }
    #sidebar-link:hover { background: rgba(100, 150, 255, 0.35); }
    @media (max-width: 768px) {
      #sidebar { width: 100%; right: auto; bottom: -100%; left: 0; top: auto; height: 70%; border-left: none; border-top: 1px solid rgba(100,150,255,0.2); transition: bottom 0.4s cubic-bezier(0.4,0,0.2,1); border-radius: 16px 16px 0 0; }
      #sidebar.open { bottom: 0; }
    }
```

Add inside `<body>`, after the tooltip div:

```html
  <!-- Sidebar -->
  <div id="sidebar">
    <button id="sidebar-close">&times;</button>
    <div id="sidebar-title"></div>
    <div id="sidebar-desc"></div>
    <div class="prob-bar-container">
      <div class="prob-bar-label"><span>Yes</span><span>No</span></div>
      <div class="prob-bar">
        <div class="prob-bar-yes" id="sidebar-yes"></div>
        <div class="prob-bar-no" id="sidebar-no"></div>
      </div>
    </div>
    <div id="sidebar-stats"></div>
    <a id="sidebar-link" href="#" target="_blank" rel="noopener">View on Polymarket →</a>
  </div>
```

- [ ] **Step 2: Add click handler and sidebar logic**

Insert after the mousemove event listener:

```javascript
    // --- Click / Sidebar ---
    const sidebar = document.getElementById('sidebar');
    const sidebarTitle = document.getElementById('sidebar-title');
    const sidebarDesc = document.getElementById('sidebar-desc');
    const sidebarYes = document.getElementById('sidebar-yes');
    const sidebarNo = document.getElementById('sidebar-no');
    const sidebarStats = document.getElementById('sidebar-stats');
    const sidebarLink = document.getElementById('sidebar-link');

    function openSidebar(marker) {
      const e = marker.event;
      sidebarTitle.textContent = e.title;
      sidebarDesc.textContent = e.description.slice(0, 300) + (e.description.length > 300 ? '...' : '');

      const yesP = (e.probability * 100).toFixed(0);
      const noP = (100 - e.probability * 100).toFixed(0);
      sidebarYes.style.width = `${yesP}%`;
      sidebarYes.textContent = `${yesP}%`;
      sidebarNo.style.width = `${noP}%`;
      sidebarNo.textContent = `${noP}%`;

      sidebarStats.innerHTML = `
        <div class="sidebar-stat"><span class="sidebar-stat-label">24h Volume</span><span>${formatVolume(e.volume)}</span></div>
        <div class="sidebar-stat"><span class="sidebar-stat-label">Total Volume</span><span>${formatVolume(e.totalVolume)}</span></div>
        <div class="sidebar-stat"><span class="sidebar-stat-label">Liquidity</span><span>${formatVolume(e.liquidity)}</span></div>
        <div class="sidebar-stat"><span class="sidebar-stat-label">Markets</span><span>${e.markets.length}</span></div>
      `;

      sidebarLink.href = `https://polymarket.com/event/${e.slug}`;
      sidebar.classList.add('open');

      // Rotate globe to face the marker
      animateToMarker(marker);
    }

    function closeSidebar() {
      sidebar.classList.remove('open');
    }

    function animateToMarker(marker) {
      // Stop auto-rotation temporarily and rotate to face marker
      const target = marker.surfacePos.clone().normalize().multiplyScalar(3);
      const start = camera.position.clone();
      const duration = 1000;
      const startTime = performance.now();

      function animateCamera(now) {
        const elapsed = now - startTime;
        const t = Math.min(elapsed / duration, 1);
        const ease = t * (2 - t); // ease-out quad
        camera.position.lerpVectors(start, target, ease);
        camera.lookAt(0, 0, 0);
        if (t < 1) requestAnimationFrame(animateCamera);
      }
      requestAnimationFrame(animateCamera);
    }

    renderer.domElement.addEventListener('click', () => {
      if (hoveredMarker) {
        openSidebar(hoveredMarker);
      }
    });

    document.getElementById('sidebar-close').addEventListener('click', closeSidebar);

    // Close sidebar on clicking canvas (not marker)
    renderer.domElement.addEventListener('click', (e) => {
      // Only close if no marker is hovered
      if (!hoveredMarker && sidebar.classList.contains('open')) {
        closeSidebar();
      }
    });
```

- [ ] **Step 3: Verify in browser**

Expected: Click a marker → sidebar slides in from right with title, description, Yes/No probability bar, stats, and Polymarket link. Globe rotates to face the clicked marker. X button closes sidebar. On mobile viewport, panel slides up from bottom.

- [ ] **Step 4: Commit**

```bash
git add prediction-globe.html
git commit -m "feat(prediction-globe): add click sidebar with event details and camera animation"
```

---

### Task 7: Top Controls (Filter + Search)

**Files:**
- Modify: `prediction-globe.html`

Add top bar with title, category filter buttons, and search input.

- [ ] **Step 1: Add top bar HTML and CSS**

Add inside `<style>`:

```css
    #top-bar {
      position: fixed; top: 0; left: 0; right: 0; z-index: 150;
      display: flex; justify-content: space-between; align-items: center;
      padding: 16px 24px;
      background: linear-gradient(to bottom, rgba(0,0,0,0.6), transparent);
      pointer-events: none;
    }
    #top-bar > * { pointer-events: auto; }
    #logo { font-size: 20px; font-weight: 700; letter-spacing: -0.5px; }
    #logo span { color: #7db4ff; }
    #controls { display: flex; gap: 8px; align-items: center; }
    .filter-btn {
      background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
      color: #fff; padding: 6px 14px; border-radius: 20px; font-size: 13px;
      cursor: pointer; transition: all 0.2s;
    }
    .filter-btn:hover, .filter-btn.active {
      background: rgba(100,150,255,0.25); border-color: rgba(100,150,255,0.5);
    }
    #search-input {
      background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
      color: #fff; padding: 6px 14px; border-radius: 20px; font-size: 13px;
      outline: none; width: 180px; transition: border-color 0.2s;
    }
    #search-input::placeholder { color: rgba(255,255,255,0.3); }
    #search-input:focus { border-color: rgba(100,150,255,0.5); }
```

Add inside `<body>`, before the tooltip div:

```html
  <!-- Top Bar -->
  <div id="top-bar">
    <div id="logo">Prediction <span>Globe</span></div>
    <div id="controls">
      <button class="filter-btn active" data-category="all">All</button>
      <button class="filter-btn" data-category="politics">Politics</button>
      <button class="filter-btn" data-category="crypto">Crypto</button>
      <button class="filter-btn" data-category="sports">Sports</button>
      <button class="filter-btn" data-category="tech">Tech</button>
      <input id="search-input" type="text" placeholder="Search events...">
    </div>
  </div>
```

- [ ] **Step 2: Add category detection and filter logic**

Insert after the `closeSidebar` function:

```javascript
    // --- Filtering ---
    const CATEGORY_KEYWORDS = {
      politics: ['trump', 'biden', 'election', 'president', 'congress', 'senate', 'democrat', 'republican', 'vote', 'party', 'governor', 'mayor', 'putin', 'zelensky', 'macron', 'modi', 'erdogan', 'xi jinping', 'war', 'nato'],
      crypto: ['bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'solana', 'sol', 'token', 'blockchain', 'defi', 'nft'],
      sports: ['nba', 'nfl', 'mlb', 'soccer', 'football', 'basketball', 'baseball', 'tennis', 'golf', 'world cup', 'champion', 'league', 'playoff', 'super bowl', 'fifa'],
      tech: ['ai ', 'openai', 'google', 'apple', 'spacex', 'tesla', 'microsoft', 'meta ', 'amazon', 'nvidia', 'gpt', 'robot'],
    };

    function detectCategory(title) {
      const text = title.toLowerCase();
      for (const [category, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
        if (keywords.some(kw => text.includes(kw))) return category;
      }
      return 'other';
    }

    let activeCategory = 'all';
    let searchQuery = '';

    function applyFilters() {
      markers.forEach(m => {
        const category = detectCategory(m.event.title);
        const matchesCategory = activeCategory === 'all' || category === activeCategory;
        const matchesSearch = !searchQuery || m.event.title.toLowerCase().includes(searchQuery);
        const visible = matchesCategory && matchesSearch;

        m.dot.material.opacity = visible ? 0.9 : 0.08;
        m.beam.material.opacity = visible ? 0.3 : 0.02;
        m.ring.visible = visible;
      });
    }

    document.querySelectorAll('.filter-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeCategory = btn.dataset.category;
        applyFilters();
      });
    });

    document.getElementById('search-input').addEventListener('input', (e) => {
      searchQuery = e.target.value.toLowerCase();
      applyFilters();
    });
```

- [ ] **Step 3: Verify in browser**

Expected: Top bar with "Prediction Globe" title on left, filter buttons and search on right. Clicking "Crypto" dims non-crypto markers. Typing in search filters by title. "All" shows everything.

- [ ] **Step 4: Commit**

```bash
git add prediction-globe.html
git commit -m "feat(prediction-globe): add top bar with category filters and search"
```

---

### Task 8: Bottom Info Bar + Auto-Refresh

**Files:**
- Modify: `prediction-globe.html`

Add bottom status bar and periodic data refresh.

- [ ] **Step 1: Add bottom bar HTML and CSS**

Add inside `<style>`:

```css
    #bottom-bar {
      position: fixed; bottom: 0; left: 0; right: 0; z-index: 150;
      display: flex; justify-content: space-between; align-items: center;
      padding: 12px 24px; font-size: 12px; opacity: 0.5;
      background: linear-gradient(to top, rgba(0,0,0,0.5), transparent);
      pointer-events: none;
    }
```

Add inside `<body>`, after the sidebar div:

```html
  <!-- Bottom Bar -->
  <div id="bottom-bar">
    <span id="event-count"></span>
    <span id="last-updated"></span>
    <span>Powered by <a href="https://polymarket.com" target="_blank" rel="noopener" style="color:#7db4ff; pointer-events:auto; text-decoration:none;">Polymarket</a></span>
  </div>
```

- [ ] **Step 2: Add status update and auto-refresh logic**

Insert after the `applyFilters` event listeners:

```javascript
    // --- Status & Auto-Refresh ---
    const eventCountEl = document.getElementById('event-count');
    const lastUpdatedEl = document.getElementById('last-updated');

    function updateStatus() {
      eventCountEl.textContent = `${processedEvents.length} events`;
      lastUpdatedEl.textContent = `Updated: ${new Date().toLocaleTimeString()}`;
    }

    async function refresh() {
      const events = await fetchEvents();
      processedEvents = processEvents(events);
      createMarkers(processedEvents);
      applyFilters();
      updateStatus();
    }

    // Modify the init function to include status update
    async function initApp() {
      const events = await fetchEvents();
      processedEvents = processEvents(events);
      createMarkers(processedEvents);
      updateStatus();

      // Auto-refresh every 5 minutes
      setInterval(refresh, 5 * 60 * 1000);
    }
```

- [ ] **Step 3: Replace the old `init()` call with `initApp()`**

Find and replace the existing init block:

```javascript
    // --- Initialize ---
    let processedEvents = [];

    async function init() {
      const events = await fetchEvents();
      processedEvents = processEvents(events);
      createMarkers(processedEvents);
    }
    init();
```

Replace with:

```javascript
    // --- Initialize ---
    let processedEvents = [];
    initApp();
```

Move the `initApp` function definition (from Step 2) to just before this block.

- [ ] **Step 4: Verify in browser**

Expected: Bottom bar shows event count, last updated time, and "Powered by Polymarket" link.

- [ ] **Step 5: Commit**

```bash
git add prediction-globe.html
git commit -m "feat(prediction-globe): add bottom info bar and 5-minute auto-refresh"
```

---

### Task 9: Loading State + Polish

**Files:**
- Modify: `prediction-globe.html`

Add a loading indicator, smooth the overall UX, and ensure mobile responsiveness.

- [ ] **Step 1: Add loading overlay HTML and CSS**

Add inside `<style>`:

```css
    #loading {
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      z-index: 999; background: #000; transition: opacity 0.8s;
    }
    #loading.hidden { opacity: 0; pointer-events: none; }
    .loading-spinner {
      width: 40px; height: 40px; border: 3px solid rgba(100,150,255,0.2);
      border-top-color: #7db4ff; border-radius: 50%; animation: spin 1s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    #loading-text { margin-top: 16px; font-size: 14px; opacity: 0.6; }
```

Add inside `<body>`, as the first child:

```html
  <!-- Loading -->
  <div id="loading">
    <div class="loading-spinner"></div>
    <div id="loading-text">Loading prediction markets...</div>
  </div>
```

- [ ] **Step 2: Hide loading after data loads**

Modify `initApp` to hide loading:

```javascript
    async function initApp() {
      const events = await fetchEvents();
      processedEvents = processEvents(events);
      createMarkers(processedEvents);
      updateStatus();
      // Hide loading screen
      document.getElementById('loading').classList.add('hidden');
      // Auto-refresh every 5 minutes
      setInterval(refresh, 5 * 60 * 1000);
    }
```

- [ ] **Step 3: Add mobile responsive tweaks to top bar**

Add inside `<style>`:

```css
    @media (max-width: 768px) {
      #top-bar { flex-direction: column; gap: 10px; padding: 12px 16px; }
      #controls { flex-wrap: wrap; gap: 6px; }
      .filter-btn { padding: 5px 10px; font-size: 12px; }
      #search-input { width: 100%; }
      #bottom-bar { flex-direction: column; gap: 4px; text-align: center; padding: 8px 16px; }
    }
```

- [ ] **Step 4: Verify in browser**

Expected: Loading spinner on page load, fades out when data is ready. All existing features still work. Test at mobile viewport width — top bar stacks vertically, sidebar slides up from bottom.

- [ ] **Step 5: Commit**

```bash
git add prediction-globe.html
git commit -m "feat(prediction-globe): add loading state and mobile responsive polish"
```

---

### Task 10: Final Integration Verification

**Files:**
- Verify: `prediction-globe.html`

End-to-end check of all features working together.

- [ ] **Step 1: Full feature checklist**

Open `prediction-globe.html` in browser and verify each feature:

1. Loading spinner appears → fades after data loads
2. Earth globe renders with night texture and atmosphere glow
3. Stars in background
4. Globe auto-rotates slowly
5. Mouse drag rotates globe, scroll zooms
6. Colored marker dots with light beams on globe surface
7. Markers pulse with ring animation
8. Hover over marker → tooltip shows title, probability, volume
9. Click marker → sidebar opens with details, globe rotates to face it
10. Sidebar has Yes/No probability bar, stats, Polymarket link
11. X button or clicking empty space closes sidebar
12. Filter buttons work (All/Politics/Crypto/Sports/Tech)
13. Search input filters markers by title
14. Bottom bar shows event count, update time, Polymarket attribution
15. No console errors

- [ ] **Step 2: Commit final version**

```bash
git add prediction-globe.html
git commit -m "feat(prediction-globe): complete 3D prediction market globe visualization"
```
