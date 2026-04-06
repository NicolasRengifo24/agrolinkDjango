/* ============================================================
   editar_producto.js
   Ubicación: static/js/editar_producto.js
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* ─────────────────────────────────────────────────────────
     1. CARGAR FINCAS Y PRESELECCIONAR LA FINCA ACTUAL
     FINCAS_JSON, PRODUCTOR_ID y FINCA_ACTUAL_ID
     vienen definidos en el <script> del template.
  ───────────────────────────────────────────────────────── */
  const fincaGrid = document.getElementById('fincaGrid');

  if (typeof FINCAS_JSON !== 'undefined' && PRODUCTOR_ID) {
    const fincas = FINCAS_JSON[PRODUCTOR_ID] || [];
    renderizarFincas(fincas, FINCA_ACTUAL_ID);
  }

  function renderizarFincas(fincas, fincaSeleccionadaId) {
    fincaGrid.innerHTML = '';

    if (fincas.length === 0) {
      fincaGrid.innerHTML = `
        <p style="color:var(--text-muted); font-size:14px; grid-column:1/-1;">
          Este productor no tiene fincas registradas.
        </p>`;
      return;
    }

    const emojis = ['🌞', '🌿', '⛰️', '🏞️', '🌾', '🍃', '🌱', '🏡'];

    fincas.forEach(function (finca, index) {
      const esActual = String(finca.id) === String(fincaSeleccionadaId);
      const emoji    = emojis[index % emojis.length];
      const card     = document.createElement('label');
      card.className = 'finca-card';
      card.innerHTML = `
        <input type="radio" name="id_finca" value="${finca.id}"
               ${esActual ? 'checked' : ''} />
        <div class="finca-label">
          <span class="finca-emoji">${emoji}</span>
          <span class="finca-name">
            ${finca.nombre}
            ${esActual ? '<span class="finca-actual-badge">Actual</span>' : ''}
          </span>
          <span class="finca-loc">${finca.departamento || finca.ciudad || ''}</span>
        </div>
        <div class="finca-check" ${esActual ? 'style="display:flex"' : ''}>
          <svg viewBox="0 0 12 12">
            <polyline points="1.5,6 5,9.5 10.5,2.5"/>
          </svg>
        </div>`;
      fincaGrid.appendChild(card);
    });
  }


  /* ─────────────────────────────────────────────────────────
     2. TOGGLE ZONA DE NUEVA IMAGEN
  ───────────────────────────────────────────────────────── */
  window.toggleNuevaImagen = function () {
    const zone   = document.getElementById('nuevaImagenZone');
    const toggle = document.getElementById('toggleBtn');
    const visible = zone.classList.toggle('visible');
    toggle.textContent = visible ? 'Cancelar cambio' : 'Cambiar imagen';
  };


  /* ─────────────────────────────────────────────────────────
     3. VISTA PREVIA DE NUEVA IMAGEN
  ───────────────────────────────────────────────────────── */
  const fileInput  = document.getElementById('imagen_producto');
  const uploadZone = document.getElementById('uploadZone');
  const previewImg = document.getElementById('previewImg');

  if (fileInput) {
    fileInput.addEventListener('change', function () {
      if (this.files[0]) showPreview(this.files[0]);
    });
  }

  if (uploadZone) {
    uploadZone.addEventListener('dragover', function (e) {
      e.preventDefault();
      uploadZone.classList.add('drag-over');
    });
    uploadZone.addEventListener('dragleave', function () {
      uploadZone.classList.remove('drag-over');
    });
    uploadZone.addEventListener('drop', function (e) {
      e.preventDefault();
      uploadZone.classList.remove('drag-over');
      const file = e.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) showPreview(file);
    });
  }

  function showPreview(file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      previewImg.src = e.target.result;
      previewImg.classList.add('visible');
    };
    reader.readAsDataURL(file);
  }


  /* ─────────────────────────────────────────────────────────
     4. VALIDACIÓN FRONTEND ANTES DE ENVIAR A DJANGO
  ───────────────────────────────────────────────────────── */
  const form = document.getElementById('productoForm');

  if (form) {
    form.addEventListener('submit', function (e) {
      let valid = true;

      // Limpiar errores previos
      form.querySelectorAll('input, select, textarea').forEach(function (el) {
        el.style.borderColor = '';
      });
      if (fincaGrid) fincaGrid.style.outline = '';

      // Validar campos requeridos
      form.querySelectorAll('[required]').forEach(function (el) {
        if (!el.value.trim()) {
          el.style.borderColor = 'var(--error)';
          valid = false;
        }
      });

      // Validar finca seleccionada
      const fincaSeleccionada = form.querySelector('input[name="id_finca"]:checked');
      if (!fincaSeleccionada) {
        if (fincaGrid) {
          fincaGrid.style.outline      = '2px solid var(--error)';
          fincaGrid.style.borderRadius = '12px';
        }
        valid = false;
      }

      if (!valid) {
        e.preventDefault();
        // Toast de error inmediato con Toastify
        Toastify({
          text: 'Por favor completa todos los campos requeridos.',
          duration: 3500,
          gravity: 'top',
          position: 'right',
          stopOnFocus: true,
          style: {
            background: '#c0392b',
            borderRadius: '10px',
            fontSize: '14px',
            fontFamily: 'DM Sans, sans-serif',
            padding: '12px 20px',
            boxShadow: '0 4px 16px rgba(0,0,0,0.18)',
            minWidth: '280px',
          }
        }).showToast();
      }
      // Si valid === true → POST normal a Django → redirect → Toastify en lista
    });
  }

});