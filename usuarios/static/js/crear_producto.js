/* ============================================================
   crear_producto.js
   Ubicación: static/js/crear_producto.js
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* ─────────────────────────────────────────────────────────
     1. FILTRO DINÁMICO DE FINCAS POR PRODUCTOR
  ───────────────────────────────────────────────────────── */
  const selectorProductor = document.getElementById('id_usuario');
  const fincaGrid         = document.getElementById('fincaGrid');

  if (selectorProductor && typeof FINCAS_JSON !== 'undefined') {

    selectorProductor.addEventListener('change', function () {
      const productorId = this.value;
      const fincas      = FINCAS_JSON[productorId] || [];
      renderizarFincas(fincas);
    });

    if (selectorProductor.value) {
      renderizarFincas(FINCAS_JSON[selectorProductor.value] || []);
    }
  }

  function renderizarFincas(fincas) {
    fincaGrid.innerHTML = '';

    if (fincas.length === 0) {
      fincaGrid.innerHTML = `
        <p style="color: var(--text-muted); font-size: 14px; grid-column: 1/-1;">
          Este productor no tiene fincas registradas.
        </p>`;
      return;
    }

    const emojis = ['🌞', '🌿', '⛰️', '🏞️', '🌾', '🍃', '🌱', '🏡'];

    fincas.forEach(function (finca, index) {
      const emoji = emojis[index % emojis.length];
      const card  = document.createElement('label');
      card.className = 'finca-card';
      card.innerHTML = `
        <input type="radio" name="id_finca" value="${finca.id}" />
        <div class="finca-label">
          <span class="finca-emoji">${emoji}</span>
          <span class="finca-name">${finca.nombre}</span>
          <span class="finca-loc">${finca.departamento || finca.ciudad || ''}</span>
        </div>
        <div class="finca-check">
          <svg viewBox="0 0 12 12"><polyline points="1.5,6 5,9.5 10.5,2.5"/></svg>
        </div>`;
      fincaGrid.appendChild(card);
    });
  }


  /* ─────────────────────────────────────────────────────────
     2. VISTA PREVIA DE IMAGEN (drag & drop)
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
     3. VALIDACIÓN ANTES DE ENVIAR A DJANGO
  ───────────────────────────────────────────────────────── */
  const form = document.getElementById('productoForm');

  if (form) {
    form.addEventListener('submit', function (e) {
      let valid = true;

      // Limpiar errores previos
      form.querySelectorAll('input, select, textarea').forEach(function (el) {
        el.style.borderColor = '';
      });
      fincaGrid.style.outline = '';

      // Validar campos requeridos
      form.querySelectorAll('[required]').forEach(function (el) {
        if (!el.value.trim()) {
          el.style.borderColor = 'var(--error)';
          valid = false;
        }
      });

      // Validar que se haya seleccionado una finca
      const fincaSeleccionada = form.querySelector('input[name="id_finca"]:checked');
      if (!fincaSeleccionada) {
        fincaGrid.style.outline      = '2px solid var(--error)';
        fincaGrid.style.borderRadius = '12px';
        valid = false;
      }

      if (!valid) {
        e.preventDefault(); // ← solo bloquea si hay errores
        showToast('Por favor completa todos los campos requeridos.', true);
      }
      // Si valid === true el form hace POST normal a Django
    });
  }


  /* ─────────────────────────────────────────────────────────
     4. RESET DEL FORMULARIO
  ───────────────────────────────────────────────────────── */
  window.resetForm = function () {
    if (form) form.reset();
    if (previewImg) {
      previewImg.src = '';
      previewImg.classList.remove('visible');
    }
    if (form) {
      form.querySelectorAll('input, select, textarea').forEach(function (el) {
        el.style.borderColor = '';
      });
    }
    if (fincaGrid) {
      fincaGrid.style.outline = '';
      fincaGrid.innerHTML = '<p style="color: var(--text-muted); font-size: 14px;">Selecciona un productor para ver sus fincas.</p>';
    }
  };


  /* ─────────────────────────────────────────────────────────
     5. TOAST DE NOTIFICACIÓN
  ───────────────────────────────────────────────────────── */
  window.showToast = function (msg, isError) {
    const toast    = document.getElementById('toast');
    const toastMsg = document.getElementById('toastMsg');
    if (!toast || !toastMsg) return;
    toastMsg.textContent   = msg;
    toast.style.background = isError ? '#c0392b' : 'var(--accent-dark)';
    toast.classList.add('show');
    setTimeout(function () { toast.classList.remove('show'); }, 3200);
  };

  // Mostrar toast si Django envió mensaje via messages framework
  const djangoMsg = document.getElementById('django-message');
  if (djangoMsg) {
    showToast(djangoMsg.dataset.msg, djangoMsg.dataset.error === 'true');
  }

});