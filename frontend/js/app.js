/**
 * Mercado de Cartas Mitológicas - Controlador Frontend
 * Arquitectura desacoplada: Capa de Presentación / Sesión de Usuario
 */

// ============================================================================
// Estado Global del Frontend (Simulación del Dominio / Puente con API)
// ============================================================================
const NOMBRE_MONEDA_COMUN = "Aureos";
const NOMBRE_MONEDA_EVENTO = "Jacks";
const NOMBRE_SOBRE_EVENTO = "Noche Eterna";
const NOMBRE_EVENTO_VIGENTE = "Noche Eterna";

const MISIONES = [
  { id: "comprar-cartas", tipo: "compras", nombre: "Comprador frecuente", objetivo: 3, recompensa: 50, descripcion: "Compra 3 cartas individuales en el mercado." },
  { id: "abrir-sobres", tipo: "sobres", nombre: "Abrir sobres", objetivo: 2, recompensa: 50, descripcion: "Compra y abre 2 sobres." },
  { id: "realizar-intercambio", tipo: "intercambios", nombre: "Un buen trato", objetivo: 1, recompensa: 50, descripcion: "Completa 1 intercambio como jugador activo." },
  { id: "coleccionar-cartas", tipo: "coleccion", nombre: "Coleccionista", objetivo: 15, recompensa: 50, descripcion: "Ten 15 cartas en tu inventario." }
];

// Cartas exclusivas del evento Noche Eterna
// Chupacabritas (Comun), Espíritu oscuro (Comun) y Wendigo (Rara)
// No se pueden conseguir en ningún sobre que no sea el de evento
const CODIGOS_CARTAS_EVENTO_EXCLUSIVAS = ["CCHU", "CESO", "RWEN"];

// Distribución del 15% de cartas exclusivas según rareza (Comun 2x, Rara 1x):
// Chupacabritas: 6.0%, Espíritu oscuro: 6.0%, Wendigo: 3.0%
const PESOS_CARTAS_EVENTO = {
  "CCHU": 6.0,
  "CESO": 6.0,
  "RWEN": 3.0
};

// 25 cartas oficiales disponibles directamente en el mercado
const CODIGOS_CARTAS_MERCADO = [
  "CNIX", // Nixie (Comun)
  "COTR", // Oni travieso (Comun)
  "CSIR", // Sirena (Comun)
  "CDIA", // Diablillo (Comun)
  "CHBO", // Hada del bosque (Comun)
  "CHAG", // Hada del agua (Comun)
  "CLOQ", // Loquace (Pixie) (Comun)
  "CDUE", // Duendecillo (Comun)
  "CGPI", // Golem de piedra (Comun)
  "CTCA", // Troll de caverna (Comun)
  "CTIN", // Titán niño (Comun)
  "CPCI", // Pequeño cíclope (Comun)
  "CNFA", // Niño fauno (Comun)
  "CDHO", // Duendes de hollín (Comun)
  "CESE", // Espíritu errante (Comun)
  "RDFU", // Dragón de Fuego (Rara)
  "RTDR", // Trio dragónico (Rara)
  "RCOC", // Cocatrice (Rara)
  "RTRI", // Tritón (Rara)
  "RGOB", // Goblin (Rara)
  "RDJE", // Diablo de Jersey (Rara)
  "RGRA", // Golem de rayo (Rara)
  "STHE", // Troll hechicero (Super Rara)
  "SKJO", // Kraken Joven (Super Rara)
  "SMAN"  // Mantícora (Super Rara)
];

const PRECIOS_POR_RAREZA = {
  "comun": 10,
  "rara": 25,
  "super rara": 40
};

const GameState = {
  activePlayerId: null,
  currentDate: "2026-11-16",
  
  // Jugadores del sistema (inicialmente con 0 monedas)
  players: {
    "j1": {
      id: "j1",
      nombre: "Ash",
      avatar: "🧙‍♂️",
      billetera: {
        comun: 0,
        evento: 0
      },
      cartas: [], // Lista de objetos { id: "CDRA-1", plantilla: {...} }
      actividades_completadas: [],
      contadoresMisiones: { compras: 0, sobres: 0, intercambios: 0 }
    },
    "j2": {
      id: "j2",
      nombre: "Misty",
      avatar: "🧝‍♀️",
      billetera: {
        comun: 0,
        evento: 0
      },
      cartas: [],
      actividades_completadas: [],
      contadoresMisiones: { compras: 0, sobres: 0, intercambios: 0 }
    }
  },

  // Contadores para IDs únicos de cartas (ej. "CDRA-1", "CDRA-2")
  cardCounters: {},

  // Evento Activo
  eventoActivo: {
    nombre: NOMBRE_EVENTO_VIGENTE,
    fecha_inicio: "2026-11-01",
    fecha_fin: "2026-11-30",
    moneda: NOMBRE_MONEDA_EVENTO,
    tasa_cambio: 5 // 5 Aureos = 1 Jack
  },

  // Sobres disponibles en el mercado
  sobres: [
    {
      id: "sobre_clasico",
      nombre: "Sobre Comun",
      tipo: "estable",
      moneda: "comun",
      precio: 20,
      cantidad_cartas: 6,
      descripcion: "Contiene 6 criaturas míticas comunes o raras del reino antiguo.",
      probabilidadesRareza: {
        "Comun": 74,
        "Rara": 20,
        "Super Rara": 5,
        "Super Super Rara": 0.9,
        "Legendaria": 0.1
      },
      grafico: "classic",
      imagen: "comun.png"
    },
    {
      id: "sobre_exclusivo",
      nombre: NOMBRE_SOBRE_EVENTO,
      tipo: "variable",
      moneda: "evento",
      precio: 20,
      cantidad_cartas: 3,
      descripcion: `Disponible solo durante el evento ${NOMBRE_EVENTO_VIGENTE}. Contiene 3 cartas. ¡Sin SSR ni Legendarias!`,
      probabilidadesRareza: {
        "Comun": 40,
        "Rara": 30,
        "Super Rara": 15,
        "Cartas del evento": 15
      },
      grafico: "lunar",
      imagen: "noche_eterna.png",
      badge: "Evento Especial"
    },
    {
      id: "sobre_especial",
      nombre: "Sobre Especial",
      tipo: "estable",
      moneda: "comun",
      precio: 45,
      cantidad_cartas: 6,
      descripcion: "Contiene 6 cartas con probabilidades de rareza especiales.",
      probabilidadesRareza: {
        "Comun": 45,
        "Rara": 35,
        "Super Rara": 15,
        "Super Super Rara": 4,
        "Legendaria": 1
      },
      grafico: "special",
      imagen: "Especial.png"
    },
    {
      id: "sobre_legendario",
      nombre: "Sobre Legendario",
      tipo: "estable",
      moneda: "comun",
      precio: 80,
      cantidad_cartas: 6,
      descripcion: "Contiene 6 cartas con altas probabilidades de obtener una legendaria!",
      probabilidadesRareza: {
        "Comun": 20,
        "Rara": 35,
        "Super Rara": 30,
        "Super Super Rara": 10,
        "Legendaria": 5
      },
      grafico: "legendary",
      imagen: "Legendario.png"
    }
  ],

  // Intercambio en curso
  tradeState: {
    targetPlayerId: "j2",
    offeredByActive: [], // IDs de cartas (máx 3)
    offeredByTarget: [], // IDs de cartas (máx 3)
    acceptedActive: false,
    acceptedTarget: false
  }
};

// ============================================================================
// Inicialización al Cargar la Página
// ============================================================================
document.addEventListener("DOMContentLoaded", () => {
  initCreatureCounters();
  setupEventListeners();
  
  // Revisar si ya hay una sesión guardada en sessionStorage
  const savedPlayerId = sessionStorage.getItem("jugador_id");
  if (savedPlayerId && GameState.players[savedPlayerId]) {
    loginPlayer(savedPlayerId);
  } else {
    // Abrir modal de Login inicial
    openModal("modal-login");
  }
});

// Inicializar contadores de cartas a partir del catálogo
function initCreatureCounters() {
  if (window.CRIATURAS_DATA && Array.isArray(window.CRIATURAS_DATA)) {
    window.CRIATURAS_DATA.forEach(c => {
      GameState.cardCounters[c.codigo] = 0;
    });
  }
}

// Generar una carta física con ID único e incremental
function crearCarta(codigo) {
  const plantilla = window.CRIATURAS_DATA.find(c => c.codigo === codigo) || window.CRIATURAS_DATA[0];
  const contador = (GameState.cardCounters[plantilla.codigo] || 0) + 1;
  GameState.cardCounters[plantilla.codigo] = contador;
  const cartaId = `${plantilla.codigo}-${contador}`;
  return {
    id: cartaId,
    contador: contador,
    plantilla: { ...plantilla }
  };
}

// ============================================================================
// Gestión de Sesión y Login
// ============================================================================
function loginPlayer(playerId) {
  if (!GameState.players[playerId]) return;
  GameState.activePlayerId = playerId;
  sessionStorage.setItem("jugador_id", playerId);
  
  updateHUD();
  closeModal("modal-login");
  showToast(`Sesión iniciada como ${getActivePlayer().nombre}`);
}

function getActivePlayer() {
  return GameState.players[GameState.activePlayerId] || GameState.players["j1"];
}

function getTargetTradePlayer() {
  return GameState.players[GameState.tradeState.targetPlayerId] || GameState.players["j2"];
}

// ============================================================================
// Actualización del HUD (Esquinas y Contadores)
// ============================================================================
function updateHUD() {
  const player = getActivePlayer();
  if (!player) return;

  // Esquina Superior Izquierda: Contadores de monedas (comienzan en 0)
  const contadorComunes = document.getElementById("contador-comunes");
  const contadorEvento = document.getElementById("contador-evento");
  if (contadorComunes) contadorComunes.textContent = player.billetera.comun;
  if (contadorEvento) contadorEvento.textContent = player.billetera.evento;

  // Esquina Inferior Izquierda: Datos del perfil del jugador
  const profileName = document.getElementById("hud-profile-name");
  const profileAvatar = document.getElementById("hud-profile-avatar");
  if (profileName) profileName.textContent = player.nombre;
  if (profileAvatar) profileAvatar.textContent = player.avatar;

  // Actualizar datos del modal de cuenta si está abierto
  const accountUserName = document.getElementById("account-user-name");
  const accountUserId = document.getElementById("account-user-id");
  const accountBalanceComun = document.getElementById("account-balance-comun");
  const accountBalanceEvento = document.getElementById("account-balance-evento");
  const accountAvatar = document.getElementById("account-avatar");
  const accountTotalCartas = document.getElementById("account-total-cartas");

  if (accountUserName) accountUserName.textContent = player.nombre;
  if (accountUserId) accountUserId.textContent = `ID de Jugador: ${player.id}`;
  if (accountBalanceComun) accountBalanceComun.textContent = player.billetera.comun;
  if (accountBalanceEvento) accountBalanceEvento.textContent = player.billetera.evento;
  if (accountAvatar) accountAvatar.textContent = player.avatar;
  if (accountTotalCartas) accountTotalCartas.textContent = player.cartas.length;
}

// ============================================================================
// Configuración de Eventos de la Interfaz
// ============================================================================
function setupEventListeners() {
  // Esquina Superior Derecha: Botón Mercado
  const btnMercado = document.getElementById("btn-acceder-mercado");
  if (btnMercado) {
    btnMercado.addEventListener("click", () => {
      renderMarketView();
      openModal("modal-mercado");
    });
  }

  // Esquina Inferior Izquierda: Botón Perfil / Cuenta
  const btnPerfil = document.getElementById("btn-acceder-perfil");
  if (btnPerfil) {
    btnPerfil.addEventListener("click", () => {
      updateHUD();
      openModal("modal-cuenta");
    });
  }

  const btnOptionMisiones = document.getElementById("opt-misiones");
  if (btnOptionMisiones) {
    btnOptionMisiones.addEventListener("click", () => {
      closeModal("modal-cuenta");
      renderMissionsView();
      openModal("modal-misiones");
    });
  }

  // Botón "+ Monedas Demo" para poder probar compras sin romper el estado inicial de 0 monedas
  const btnDemoCoins = document.getElementById("btn-demo-coins");
  if (btnDemoCoins) {
    btnDemoCoins.addEventListener("click", () => {
      const player = getActivePlayer();
      player.billetera.comun += 100;
      updateHUD();
      showToast("+100 Monedas Comunes recibidas (Recompensa de misión)");
    });
  }

  // Opciones de Mi Cuenta:
  // 1. Deshabilitadas con feedback explicativo
  document.querySelectorAll(".account-option-card.disabled").forEach(card => {
    card.addEventListener("click", () => {
      const feature = card.dataset.feature || "Esta opción";
      if (feature === "batalla") {
        showToast("⚔️ El sistema de batalla está planificado para una versión futura.");
      } else if (feature === "chat") {
        showToast("💬 El chat entre jugadores estará disponible próximamente.");
      } else if (feature === "config") {
        showToast("⚙️ Configuración de cuenta en desarrollo.");
      } else {
        showToast("Opción deshabilitada actualmente.");
      }
    });
  });

  // 2. Habilitadas:
  // Intercambio
  const btnOptionIntercambio = document.getElementById("opt-intercambio");
  if (btnOptionIntercambio) {
    btnOptionIntercambio.addEventListener("click", () => {
      closeModal("modal-cuenta");
      setupTradeArena();
      openModal("modal-intercambio");
    });
  }

  // Catálogo
  const btnOptionCatalogo = document.getElementById("opt-catalogo");
  if (btnOptionCatalogo) {
    btnOptionCatalogo.addEventListener("click", () => {
      closeModal("modal-cuenta");
      renderCatalogView();
      openModal("modal-catalogo");
    });
  }

  // Mis Cartas
  const btnOptionMisCartas = document.getElementById("opt-mis-cartas");
  if (btnOptionMisCartas) {
    btnOptionMisCartas.addEventListener("click", () => {
      closeModal("modal-cuenta");
      renderInventoryView();
      openModal("modal-inventario");
    });
  }

  // Botón Cambiar Jugador / Logout
  const btnLogout = document.getElementById("btn-logout");
  if (btnLogout) {
    btnLogout.addEventListener("click", () => {
      closeModal("modal-cuenta");
      openModal("modal-login");
    });
  }

  // Formulario de Login: Selección de Jugadores
  document.querySelectorAll(".player-select-pill").forEach(pill => {
    pill.addEventListener("click", () => {
      document.querySelectorAll(".player-select-pill").forEach(p => p.classList.remove("selected"));
      pill.classList.add("selected");
    });
  });

  const btnConfirmLogin = document.getElementById("btn-confirm-login");
  if (btnConfirmLogin) {
    btnConfirmLogin.addEventListener("click", () => {
      const selectedPill = document.querySelector(".player-select-pill.selected");
      if (selectedPill) {
        const id = selectedPill.dataset.id;
        loginPlayer(id);
      }
    });
  }

  // Filtros del Catálogo
  const searchInput = document.getElementById("catalog-search");
  const rarityFilter = document.getElementById("catalog-rarity");
  const typeFilter = document.getElementById("catalog-type");

  if (searchInput) searchInput.addEventListener("input", filterCatalog);
  if (rarityFilter) rarityFilter.addEventListener("change", filterCatalog);
  if (typeFilter) typeFilter.addEventListener("change", filterCatalog);

  // Cerrar modales con botones de cierre y backdrop
  document.querySelectorAll(".modal-close-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const modal = e.target.closest(".modal-overlay");
      if (modal) closeModal(modal.id);
    });
  });

  document.querySelectorAll(".modal-overlay").forEach(overlay => {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) {
        closeModal(overlay.id);
      }
    });
  });
}

// ============================================================================
// Funciones de Modales
// ============================================================================
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add("active");
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove("active");
  }
}

// ============================================================================
// VISTA: Catálogo de Criaturas (227 Criaturas del Juego)
// ============================================================================
function renderCatalogView() {
  const container = document.getElementById("catalog-cards-container");
  if (!container || !window.CRIATURAS_DATA) return;

  // Llenar selector de tipos si no está lleno
  const typeSelect = document.getElementById("catalog-type");
  if (typeSelect && typeSelect.options.length <= 1) {
    const tipos = [...new Set(window.CRIATURAS_DATA.map(c => c.tipo))].sort();
    tipos.forEach(tipo => {
      const opt = document.createElement("option");
      opt.value = tipo;
      opt.textContent = tipo;
      typeSelect.appendChild(opt);
    });
  }

  filterCatalog();
}

function filterCatalog() {
  const container = document.getElementById("catalog-cards-container");
  const countBadge = document.getElementById("catalog-count-badge");
  if (!container || !window.CRIATURAS_DATA) return;

  const query = (document.getElementById("catalog-search")?.value || "").toLowerCase().trim();
  const rarity = (document.getElementById("catalog-rarity")?.value || "").toLowerCase().trim();
  const type = (document.getElementById("catalog-type")?.value || "").toLowerCase().trim();

  const filtered = window.CRIATURAS_DATA.filter(c => {
    const matchesQuery = !query || c.nombre.toLowerCase().includes(query) || c.codigo.toLowerCase().includes(query);
    const matchesRarity = !rarity || c.rareza.toLowerCase() === rarity;
    const matchesType = !type || c.tipo.toLowerCase() === type;
    return matchesQuery && matchesRarity && matchesType;
  });

  // Las cartas exclusivas del evento del momento se colocan al inicio del catálogo
  filtered.sort((a, b) => {
    const aEx = CODIGOS_CARTAS_EVENTO_EXCLUSIVAS.includes(a.codigo) ? 1 : 0;
    const bEx = CODIGOS_CARTAS_EVENTO_EXCLUSIVAS.includes(b.codigo) ? 1 : 0;
    if (bEx !== aEx) return bEx - aEx;
    return 0;
  });

  if (countBadge) {
    countBadge.textContent = `${filtered.length} de ${window.CRIATURAS_DATA.length} Criaturas`;
  }

  container.innerHTML = filtered.map(c => renderCreatureCardHTML(c, false)).join("");
}

// Renderizar HTML para una carta de criatura
function renderCreatureCardHTML(creatura, esCartaFisica = false, cartaId = null) {
  const isExclusive = CODIGOS_CARTAS_EVENTO_EXCLUSIVAS.includes(creatura.codigo);
  const rarezaClass = isExclusive ? "rareza-exclusiva" : getRarityClass(creatura.rareza);
  const typeIcon = getTypeIcon(creatura.tipo);
  const artworkPath = getCreatureArtworkPath(creatura.nombre);

  return `
    <div class="creature-card ${rarezaClass}">
      <div class="card-illustration">
        ${artworkPath ? `<img class="creature-artwork" src="${artworkPath}" alt="${creatura.nombre}" loading="lazy" decoding="async" onerror="this.remove()">` : ""}
        <span aria-hidden="true">${typeIcon}</span>
        <div class="card-top-info" style="display: flex; justify-content: space-between; align-items: center; gap: 0.35rem;">
          <div style="display: flex; align-items: center; gap: 0.35rem;">
            <span class="card-code">${esCartaFisica ? cartaId : creatura.codigo}</span>
            ${isExclusive ? `
              <span class="card-rarity-badge">
                ${creatura.rareza}
              </span>
            ` : ""}
          </div>
          <div style="display: flex; align-items: center; gap: 0.35rem;">
            ${isExclusive ? `
              <span class="hero-badge" style="margin: 0; font-size: 0.65rem; padding: 0.2rem 0.55rem; background: rgba(168, 85, 247, 0.25); border: 1px solid rgba(192, 132, 252, 0.6); color: #c084fc; letter-spacing: 0.5px;">
                Evento Especial
              </span>
            ` : `
              <span class="card-rarity-badge">
                ${creatura.rareza}
              </span>
            `}
          </div>
        </div>
        <div class="card-caption">
          <div class="card-creature-name" title="${creatura.nombre}">${creatura.nombre}</div>
          <div class="card-type-tag">${creatura.tipo}</div>
        </div>
      </div>

      <div class="card-stats-row">
        <div class="card-stat hp" title="Vida">❤️ ${creatura.vida}</div>
        <div class="card-stat atk" title="Ataque">⚔️ ${creatura.ataque}</div>
        <div class="card-stat def" title="Defensa">🛡️ ${creatura.defensa}</div>
      </div>

      <div class="card-ability-box">
        <span class="card-ability-name">⚡ ${creatura.habilidad} (${creatura.usos_habilidad || 1} uso)</span>
        <div style="color: #94a3b8; font-size: 0.7rem;">${creatura.descripcion_habilidad}</div>
      </div>
    </div>
  `;
}

const creatureArtworkFiles = [
  "cocatrice.png", "diablillo.png", "diablo_de_jersey.png", "dragon_de_fuego.png",
  "Duendecillo.png", "duendes_de_holin.png", "espiritu_errante.png",
  "fenix_legenedario.png", "Goblin.png", "golem_de_amatista.png",
  "golem_de_piedra.png", "golem_de_rayo.png", "hada_del_agua.png",
  "hada_del_bosque.png", "hija_de_lucifer.png", "kitsune_de_tres_colas.png",
  "kraken_joven.png", "leviatan.png", "loquace.png", "manticora.png",
  "Mooncalf.png", "niño_fauno.png", "Nixie.png", "oni_travieso.png",
  "Pegaso.png", "pequeño_ciclope.png", "pichon_de_fenix.png",
  "reina_de_las_pixies.png", "Sirena.png", "titan_del_viento.png",
  "titan_niño.png", "trio_dragonico.png", "triton.png",
  "troll_de_las_cavernas.png", "troll_hechicero.png", "Unicornio.png",
  "vita.png"
];

const creatureArtworkByName = new Map(
  creatureArtworkFiles.map(filename => [
    normalizeArtworkName(filename.replace(/\.png$/i, "")),
    filename
  ])
);

const creatureArtworkAliases = {
  duendesdehollin: "duendes_de_holin.png",
  fenixlegendario: "fenix_legenedario.png",
  golemamatista: "golem_de_amatista.png",
  loquacepixie: "loquace.png",
  trolldecaverna: "troll_de_las_cavernas.png",
  vitapixie: "vita.png"
};

function normalizeArtworkName(name) {
  return name.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]/g, "");
}

function getCreatureArtworkPath(name) {
  const normalizedName = normalizeArtworkName(name);
  const filename = creatureArtworkAliases[normalizedName] || creatureArtworkByName.get(normalizedName);
  return filename ? `/Documentos/Imagenes/Personajes/${encodeURIComponent(filename)}` : null;
}

function getPackArtworkPath(filename) {
  return `/Documentos/Imagenes/Sobres/${encodeURIComponent(filename)}`;
}

function getCurrencyArtworkPath(currency) {
  return `/Documentos/Imagenes/Monedas/${currency === "evento" ? "Jacks.png" : "aureos.png"}`;
}

function getRarityClass(rareza) {
  const r = (rareza || "").toLowerCase();
  if (r.includes("com")) return "rareza-comun";
  if (r.includes("super super") || r.includes("súper súper") || r.includes("ssr")) return "rareza-ssr";
  if (r.includes("super") || r.includes("súper") || r.includes("sr")) return "rareza-sr";
  if (r.includes("rara")) return "rareza-rara";
  if (r.includes("legen")) return "rareza-legendaria";
  if (r.includes("exclus")) return "rareza-exclusiva";
  return "rareza-comun";
}

function getTypeIcon(tipo) {
  const t = (tipo || "").toLowerCase();
  if (t.includes("drag")) return "🐉";
  if (t.includes("mar")) return "🧜‍♀️";
  if (t.includes("celes")) return "🪽";
  if (t.includes("infer")) return "👹";
  if (t.includes("feér") || t.includes("feer")) return "🧚";
  if (t.includes("gigan")) return "🗿";
  if (t.includes("híb") || t.includes("hib")) return "🦅";
  if (t.includes("espír") || t.includes("espir")) return "👻";
  if (t.includes("ave")) return "🦅";
  return "🔮";
}

// ============================================================================
// VISTA: Mis Cartas (Inventario del Jugador)
// ============================================================================
function renderInventoryView() {
  const container = document.getElementById("inventory-cards-container");
  const emptyState = document.getElementById("inventory-empty-state");
  const countBadge = document.getElementById("inventory-count-badge");
  const player = getActivePlayer();

  if (!container || !player) return;

  const total = player.cartas.length;
  if (countBadge) countBadge.textContent = `${total} Cartas`;

  if (total === 0) {
    container.innerHTML = "";
    if (emptyState) emptyState.style.display = "block";
  } else {
    if (emptyState) emptyState.style.display = "none";
    container.innerHTML = player.cartas.map(c => 
      renderCreatureCardHTML(c.plantilla, true, c.id)
    ).join("");
  }
}

function renderMissionsView() {
  const container = document.getElementById("missions-list");
  const player = getActivePlayer();
  if (!container || !player) return;

  container.innerHTML = MISIONES.map(mision => {
    const avance = mision.tipo === "coleccion"
      ? player.cartas.length
      : player.contadoresMisiones[mision.tipo];
    const progreso = Math.min(avance, mision.objetivo);
    const reclamada = player.actividades_completadas.includes(mision.id);
    const puedeReclamar = progreso >= mision.objetivo && !reclamada;

    return `
      <article class="mission-card">
        <div class="mission-info">
          <h4>${mision.nombre}</h4>
          <p>${mision.descripcion}</p>
        </div>
        <div class="mission-progress">
          <div class="mission-progress-label">
            <span>Progreso</span>
            <span>${progreso} / ${mision.objetivo}</span>
          </div>
          <div class="mission-progress-track" role="progressbar" aria-valuenow="${progreso}" aria-valuemin="0" aria-valuemax="${mision.objetivo}" aria-label="${mision.nombre}">
            <div class="mission-progress-fill" style="width: ${(progreso / mision.objetivo) * 100}%"></div>
          </div>
          <span class="mission-reward">Recompensa: ${mision.recompensa} ${NOMBRE_MONEDA_COMUN}</span>
        </div>
        <button class="mission-claim-btn" ${!puedeReclamar ? "disabled" : ""} onclick="claimMission('${mision.id}')">
          ${reclamada ? "Reclamada" : puedeReclamar ? "Reclamar" : "En progreso"}
        </button>
      </article>
    `;
  }).join("");
}

function claimMission(missionId) {
  const player = getActivePlayer();
  const mision = MISIONES.find(item => item.id === missionId);
  if (!mision) {
    showToast("❌ No se encontró la misión.");
    return;
  }
  if (player.actividades_completadas.includes(missionId)) {
    showToast("Esta misión ya fue reclamada.");
    return;
  }

  const avance = mision.tipo === "coleccion"
    ? player.cartas.length
    : player.contadoresMisiones[mision.tipo];
  if (avance < mision.objetivo) {
    showToast("Aún no completaste esta misión.");
    return;
  }

  player.actividades_completadas.push(missionId);
  player.billetera.comun += mision.recompensa;
  updateHUD();
  renderMissionsView();
  showToast(`✅ Misión completada: recibiste ${mision.recompensa} ${NOMBRE_MONEDA_COMUN}.`);
}

// ============================================================================
// VISTA: Mercado de Cartas y Sobres
// ============================================================================
function renderMarketView() {
  const player = getActivePlayer();
  const packsContainer = document.getElementById("market-packs-list");
  if (!packsContainer) return;

  const sobresOrdenados = [...GameState.sobres].sort((a, b) => {
    const aEsEvento = a.moneda === "evento";
    const bEsEvento = b.moneda === "evento";
    if (aEsEvento === bEsEvento) return 0;
    return aEsEvento ? 1 : -1;
  });

  packsContainer.innerHTML = sobresOrdenados.map(sobre => {
    const isEvent = sobre.moneda === "evento";
    const userSaldo = isEvent ? player.billetera.evento : player.billetera.comun;
    const canAfford = userSaldo >= sobre.precio;

    return `
      <div class="pack-card ${isEvent ? 'event-pack' : ''}">
        ${isEvent ? `
          <span class="hero-badge" style="position: absolute; top: 12px; right: 12px; margin: 0; font-size: 0.65rem;">
            ${sobre.badge}
          </span>
        ` : ""}
        <div class="pack-graphic ${sobre.grafico}">
          <img src="${getPackArtworkPath(sobre.imagen)}" alt="${sobre.nombre}" loading="lazy" decoding="async">
        </div>

        <div>
          <h4 style="font-family: var(--font-heading); font-size: 1.1rem; margin-bottom: 0.25rem;">${sobre.nombre}</h4>
          <p style="font-size: 0.8rem; color: #94a3b8;">${sobre.descripcion}</p>
        </div>

        <div class="pack-price-tag">
          <img class="pack-currency-artwork" src="${getCurrencyArtworkPath(sobre.moneda)}" alt="" aria-hidden="true">
          <span>${sobre.precio} ${isEvent ? NOMBRE_MONEDA_EVENTO : NOMBRE_MONEDA_COMUN}</span>
        </div>

        <button class="buy-pack-btn" ${!canAfford ? 'disabled' : ''} onclick="buyPack('${sobre.id}')">
          ${canAfford ? 'Comprar y Abrir Sobre' : 'Saldo Insuficiente'}
        </button>
      </div>
    `;
  }).join("");

  // Casa de cambio de moneda (comunes a evento)
  const exchangeRateSpan = document.getElementById("exchange-rate-factor");
  if (exchangeRateSpan) {
    exchangeRateSpan.innerHTML = `
      <img class="exchange-currency-artwork" src="${getCurrencyArtworkPath("comun")}" alt="" aria-hidden="true">
      ${GameState.eventoActivo.tasa_cambio} ${NOMBRE_MONEDA_COMUN} =
      <img class="exchange-currency-artwork" src="${getCurrencyArtworkPath("evento")}" alt="" aria-hidden="true">
      1 ${NOMBRE_MONEDA_EVENTO}
    `;
  }

  // Cartas individuales del mercado (25 cartas oficiales)
  const cardsContainer = document.getElementById("market-cards-list");
  if (cardsContainer && window.CRIATURAS_DATA) {
    const marketCards = CODIGOS_CARTAS_MERCADO
      .map(cod => window.CRIATURAS_DATA.find(c => c.codigo === cod))
      .filter(Boolean);

    cardsContainer.innerHTML = marketCards.map(creatura => {
      const precio = obtenerPrecioCartaMercado(creatura);
      if (precio === null) {
        throw new Error(`No se pudo determinar el precio de ${creatura.codigo} en el mercado.`);
      }
      const canAfford = player.billetera.comun >= precio;

      return `
        <div class="market-card-wrapper" style="display: flex; flex-direction: column; align-items: stretch; gap: 0.5rem;">
          ${renderCreatureCardHTML(creatura, false)}
          <button class="buy-pack-btn" style="width: 100%; padding: 0.5rem 0.75rem; font-size: 0.82rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;"
                  ${!canAfford ? 'disabled' : ''} onclick="buyMarketCard('${creatura.codigo}')">
            <img class="pack-currency-artwork" src="${getCurrencyArtworkPath('comun')}" alt="" aria-hidden="true" style="width: 16px; height: 16px;">
            <span>${canAfford ? `Comprar (${precio} ${NOMBRE_MONEDA_COMUN})` : `Sin saldo (${precio} ${NOMBRE_MONEDA_COMUN})`}</span>
          </button>
        </div>
      `;
    }).join("");
  }
}

function buyMarketCard(codigo) {
  const player = getActivePlayer();
  if (!CODIGOS_CARTAS_MERCADO.includes(codigo)) {
    showToast("❌ Esta carta no está disponible en el mercado.");
    return;
  }

  const creatura = window.CRIATURAS_DATA.find(c => c.codigo === codigo);
  if (!creatura) {
    showToast("❌ No se encontró la carta seleccionada.");
    return;
  }

  const precio = obtenerPrecioCartaMercado(creatura);
  if (precio === null) {
    showToast("❌ No se pudo determinar el precio de esta carta.");
    return;
  }

  if (player.billetera.comun < precio) {
    showToast(`❌ Saldo insuficiente (${player.billetera.comun}/${precio} ${NOMBRE_MONEDA_COMUN}).`);
    return;
  }

  // Cobrar
  player.billetera.comun -= precio;

  // Entregar carta con ID único
  player.cartas.push(crearCarta(creatura.codigo));
  player.contadoresMisiones.compras += 1;

  updateHUD();
  renderMarketView();
  showToast(`✅ ¡Has adquirido a ${creatura.nombre} por ${precio} ${NOMBRE_MONEDA_COMUN}!`);
}

function obtenerPrecioCartaMercado(creatura) {
  if (!CODIGOS_CARTAS_MERCADO.includes(creatura.codigo)) return null;
  return PRECIOS_POR_RAREZA[normalizarRareza(creatura.rareza)] ?? null;
}

function buyPack(sobreId) {
  const player = getActivePlayer();
  const sobre = GameState.sobres.find(s => s.id === sobreId);
  if (!sobre) return;

  const isEvent = sobre.moneda === "evento";
  const userSaldo = isEvent ? player.billetera.evento : player.billetera.comun;

  if (userSaldo < sobre.precio) {
    showToast("❌ Saldo insuficiente para adquirir el sobre.");
    return;
  }

  // 1. Cobrar
  if (isEvent) {
    player.billetera.evento -= sobre.precio;
  } else {
    player.billetera.comun -= sobre.precio;
  }

  // 2. Generar cartas aleatorias según la cantidad de cartas del sobre
  const cartasObtenidas = [];
  for (let i = 0; i < sobre.cantidad_cartas; i++) {
    const plantilla = sobre.probabilidadesRareza
      ? elegirCriaturaPorRareza(sobre.probabilidadesRareza)
      : elegirCriaturaAleatoria(
          window.CRIATURAS_DATA.filter(c => !CODIGOS_CARTAS_EVENTO_EXCLUSIVAS.includes(c.codigo))
        );
    const carta = crearCarta(plantilla.codigo);
    player.cartas.push(carta);
    cartasObtenidas.push(carta);
  }
  player.contadoresMisiones.sobres += 1;

  updateHUD();
  renderMarketView();
  showPackOpening(sobre, cartasObtenidas);
}

function elegirCriaturaAleatoria(criaturas) {
  const randomIndex = Math.floor(Math.random() * criaturas.length);
  return criaturas[randomIndex];
}

function elegirCriaturaPorRareza(probabilidadesRareza) {
  const rarezas = Object.entries(probabilidadesRareza);
  const pesoTotal = rarezas.reduce((total, [, peso]) => total + peso, 0);
  let tirada = Math.random() * pesoTotal;
  let rarezaElegida = rarezas[rarezas.length - 1][0];

  for (const [rareza, peso] of rarezas) {
    tirada -= peso;
    if (tirada < 0) {
      rarezaElegida = rareza;
      break;
    }
  }

  // Si la categoría elegida es "Cartas del evento":
  // Distribución exclusiva entre Chupacabritas (6%), Espíritu oscuro (6%) y Wendigo (3%)
  if (rarezaElegida.toLowerCase().includes("evento")) {
    const opcionesEvento = Object.entries(PESOS_CARTAS_EVENTO);
    const totalPesosEvento = opcionesEvento.reduce((tot, [, p]) => tot + p, 0);
    let tiradaEvento = Math.random() * totalPesosEvento;
    let codigoElegido = opcionesEvento[opcionesEvento.length - 1][0];
    for (const [codigo, peso] of opcionesEvento) {
      tiradaEvento -= peso;
      if (tiradaEvento < 0) {
        codigoElegido = codigo;
        break;
      }
    }
    const criaturaEvento = window.CRIATURAS_DATA.find(c => c.codigo === codigoElegido);
    if (criaturaEvento) return criaturaEvento;
  }

  // Para categorías regulares (Comun, Rara, Super Rara, etc.):
  // Las cartas exclusivas de evento NO se pueden conseguir en ningún sobre regular ni pool regular
  const rarezaNormalizada = normalizarRareza(rarezaElegida);
  const candidatas = window.CRIATURAS_DATA.filter(
    criatura =>
      !CODIGOS_CARTAS_EVENTO_EXCLUSIVAS.includes(criatura.codigo) &&
      normalizarRareza(criatura.rareza) === rarezaNormalizada
  );
  if (candidatas.length === 0) {
    throw new Error(`No hay criaturas disponibles de rareza "${rarezaElegida}".`);
  }
  return elegirCriaturaAleatoria(candidatas);
}

function normalizarRareza(rareza) {
  if (!rareza) return "comun";
  let r = rareza.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
  if (r === "c" || r === "comun") return "comun";
  if (r === "r" || r === "rara" || r === "raro") return "rara";
  if (r === "sr" || r === "super rara" || r === "super_rara") return "super rara";
  if (r === "ssr" || r === "super super rara" || r === "super_super_rara") return "super super rara";
  if (r === "l" || r === "legendaria" || r === "legendario") return "legendaria";
  return r;
}

function showPackOpening(sobre, cartasObtenidas) {
  const pack = document.getElementById("opening-pack");
  const cards = document.getElementById("opening-cards");
  const subtitle = document.getElementById("opening-subtitle");
  if (!pack || !cards || !subtitle) return;

  pack.style.setProperty("--pack-image", `url("${getPackArtworkPath(sobre.imagen)}")`);
  pack.classList.add("is-resetting");
  pack.classList.remove("is-tearing");
  void pack.offsetWidth;
  cards.classList.remove("is-revealed");
  cards.innerHTML = cartasObtenidas.map((carta, index) => `
    <div class="opening-reward-card" style="--card-index: ${index}">
      ${renderCreatureCardHTML(carta.plantilla, true, carta.id)}
    </div>
  `).join("");
  subtitle.textContent = `¡Abriendo ${sobre.nombre}!`;
  openModal("modal-apertura-sobre");

  window.setTimeout(() => {
    pack.classList.remove("is-resetting");
    void pack.offsetWidth;
    pack.classList.add("is-tearing");
    const revealDelay = window.matchMedia("(prefers-reduced-motion: reduce)").matches ? 50 : 2400;
    window.setTimeout(() => {
      cards.classList.add("is-revealed");
      subtitle.textContent = "¡Estas son las cartas que obtuviste!";
    }, revealDelay);
  }, 50);
}

function convertCurrency() {
  const player = getActivePlayer();
  const inputAmount = parseInt(document.getElementById("convert-amount-input")?.value || "0", 10);

  if (isNaN(inputAmount) || inputAmount <= 0) {
    showToast("Ingresa una cantidad válida a convertir.");
    return;
  }

  if (player.billetera.comun < inputAmount) {
    showToast("❌ No tienes suficientes monedas comunes.");
    return;
  }

  const exchangeRate = GameState.eventoActivo.tasa_cambio;
  if (inputAmount % exchangeRate !== 0) {
    showToast(`La cantidad debe ser múltiplo de ${exchangeRate} ${NOMBRE_MONEDA_COMUN}.`);
    return;
  }

  const converted = inputAmount / exchangeRate;
  player.billetera.comun -= inputAmount;
  player.billetera.evento += converted;

  updateHUD();
  renderMarketView();
  const convertedCurrencyName = converted === 1 ? "Jack" : NOMBRE_MONEDA_EVENTO;
  showToast(`✨ Convertiste ${inputAmount} ${NOMBRE_MONEDA_COMUN} a ${converted} ${convertedCurrencyName}.`);
}

// ============================================================================
// VISTA: Intercambio de Cartas (Máx 3 cartas, doble aceptación requerida)
// ============================================================================
function setupTradeArena() {
  const active = getActivePlayer();
  // El otro jugador
  const otherId = active.id === "j1" ? "j2" : "j1";
  GameState.tradeState.targetPlayerId = otherId;
  const target = getTargetTradePlayer();

  // Reset de la oferta
  GameState.tradeState.offeredByActive = [];
  GameState.tradeState.offeredByTarget = [];
  GameState.tradeState.acceptedActive = false;
  GameState.tradeState.acceptedTarget = false;

  const nameA = document.getElementById("trade-player-a-name");
  const nameB = document.getElementById("trade-player-b-name");
  if (nameA) nameA.textContent = active.nombre;
  if (nameB) nameB.textContent = target.nombre;

  // Llenar selector de cartas a ofrecer por el jugador activo
  renderTradeSlots();
  renderTradePools();
}

function renderTradeSlots() {
  const active = getActivePlayer();
  const target = getTargetTradePlayer();

  // Slots de Jugador Activo (Máximo 3)
  for (let i = 0; i < 3; i++) {
    const slotEl = document.getElementById(`trade-slot-a-${i}`);
    if (slotEl) {
      const cartaId = GameState.tradeState.offeredByActive[i];
      if (cartaId) {
        const carta = active.cartas.find(c => c.id === cartaId);
        const artworkPath = getCreatureArtworkPath(carta.plantilla.nombre);
        slotEl.className = "trade-card-slot filled";
        slotEl.innerHTML = `
          ${artworkPath
            ? `<img class="trade-card-artwork" src="${artworkPath}" alt="" loading="lazy" decoding="async">`
            : `<span style="font-size: 1.2rem;">${getTypeIcon(carta.plantilla.tipo)}</span>`}
          <div style="font-weight: 700; font-size: 0.7rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 90%;">
            ${carta.plantilla.nombre}
          </div>
          <span style="font-size: 0.65rem; color: #fbbf24;">${carta.id}</span>
          <span style="font-size: 0.65rem; color: #ef4444; margin-top: 4px;">(Quitar)</span>
        `;
        slotEl.onclick = () => toggleOfferCard('active', cartaId);
      } else {
        slotEl.className = "trade-card-slot";
        slotEl.innerHTML = `<span>+ Ranura ${i + 1}</span><small>Vacío</small>`;
        slotEl.onclick = null;
      }
    }
  }

  // Slots de Jugador Objetivo (Máximo 3)
  for (let i = 0; i < 3; i++) {
    const slotEl = document.getElementById(`trade-slot-b-${i}`);
    if (slotEl) {
      const cartaId = GameState.tradeState.offeredByTarget[i];
      if (cartaId) {
        const carta = target.cartas.find(c => c.id === cartaId);
        const artworkPath = getCreatureArtworkPath(carta.plantilla.nombre);
        slotEl.className = "trade-card-slot filled";
        slotEl.innerHTML = `
          ${artworkPath
            ? `<img class="trade-card-artwork" src="${artworkPath}" alt="" loading="lazy" decoding="async">`
            : `<span style="font-size: 1.2rem;">${getTypeIcon(carta.plantilla.tipo)}</span>`}
          <div style="font-weight: 700; font-size: 0.7rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 90%;">
            ${carta.plantilla.nombre}
          </div>
          <span style="font-size: 0.65rem; color: #c084fc;">${carta.id}</span>
          <span style="font-size: 0.65rem; color: #ef4444; margin-top: 4px;">(Quitar)</span>
        `;
        slotEl.onclick = () => toggleOfferCard('target', cartaId);
      } else {
        slotEl.className = "trade-card-slot";
        slotEl.innerHTML = `<span>+ Ranura ${i + 1}</span><small>Vacío</small>`;
        slotEl.onclick = null;
      }
    }
  }

  // Checkboxes de aceptación
  const checkA = document.getElementById("trade-accept-a");
  const checkB = document.getElementById("trade-accept-b");
  const executeBtn = document.getElementById("btn-execute-trade");

  if (checkA) checkA.checked = GameState.tradeState.acceptedActive;
  if (checkB) checkB.checked = GameState.tradeState.acceptedTarget;

  const hasCards = (GameState.tradeState.offeredByActive.length > 0 || GameState.tradeState.offeredByTarget.length > 0);
  const bothAccepted = GameState.tradeState.acceptedActive && GameState.tradeState.acceptedTarget;

  if (executeBtn) {
    executeBtn.disabled = !(hasCards && bothAccepted);
  }
}

function renderTradePools() {
  const active = getActivePlayer();
  const target = getTargetTradePlayer();

  const poolA = document.getElementById("trade-pool-a");
  const poolB = document.getElementById("trade-pool-b");

  if (poolA) {
    if (active.cartas.length === 0) {
      poolA.innerHTML = `<p style="font-size: 0.75rem; color: #94a3b8;">${active.nombre} no tiene cartas en su inventario para ofrecer.</p>`;
    } else {
      poolA.innerHTML = active.cartas.map(c => {
        const isSelected = GameState.tradeState.offeredByActive.includes(c.id);
        const artworkPath = getCreatureArtworkPath(c.plantilla.nombre);
        return `
          <button class="action-pill-btn" style="font-size: 0.75rem; padding: 0.35rem 0.6rem; ${isSelected ? 'border-color: #e6b450; background: rgba(230,180,80,0.2);' : ''}"
            onclick="toggleOfferCard('active', '${c.id}')">
            ${artworkPath ? `<img class="trade-pool-artwork" src="${artworkPath}" alt="" loading="lazy" decoding="async">` : ""}
            ${isSelected ? '✓ ' : '+ '} ${c.plantilla.nombre} (${c.id})
          </button>
        `;
      }).join("");
    }
  }

  if (poolB) {
    if (target.cartas.length === 0) {
      poolB.innerHTML = `<p style="font-size: 0.75rem; color: #94a3b8;">${target.nombre} no tiene cartas en su inventario para ofrecer.</p>`;
    } else {
      poolB.innerHTML = target.cartas.map(c => {
        const isSelected = GameState.tradeState.offeredByTarget.includes(c.id);
        const artworkPath = getCreatureArtworkPath(c.plantilla.nombre);
        return `
          <button class="action-pill-btn" style="font-size: 0.75rem; padding: 0.35rem 0.6rem; ${isSelected ? 'border-color: #a855f7; background: rgba(168,85,247,0.2);' : ''}"
            onclick="toggleOfferCard('target', '${c.id}')">
            ${artworkPath ? `<img class="trade-pool-artwork" src="${artworkPath}" alt="" loading="lazy" decoding="async">` : ""}
            ${isSelected ? '✓ ' : '+ '} ${c.plantilla.nombre} (${c.id})
          </button>
        `;
      }).join("");
    }
  }
}

function toggleOfferCard(playerSide, cartaId) {
  const list = playerSide === 'active' 
    ? GameState.tradeState.offeredByActive 
    : GameState.tradeState.offeredByTarget;

  const idx = list.indexOf(cartaId);
  if (idx >= 0) {
    list.splice(idx, 1);
  } else {
    if (list.length >= 3) {
      showToast("⚠️ Máximo 3 cartas por jugador según las reglas del juego.");
      return;
    }
    list.push(cartaId);
  }

  // Cualquier cambio en la oferta anula la aceptación previa
  GameState.tradeState.acceptedActive = false;
  GameState.tradeState.acceptedTarget = false;

  renderTradeSlots();
  renderTradePools();
}

function toggleTradeAcceptance(playerSide) {
  if (playerSide === 'active') {
    GameState.tradeState.acceptedActive = !GameState.tradeState.acceptedActive;
  } else {
    GameState.tradeState.acceptedTarget = !GameState.tradeState.acceptedTarget;
  }
  renderTradeSlots();
}

function executeTrade() {
  const active = getActivePlayer();
  const target = getTargetTradePlayer();

  const cardsA = [...GameState.tradeState.offeredByActive];
  const cardsB = [...GameState.tradeState.offeredByTarget];

  if (cardsA.length === 0 && cardsB.length === 0) {
    showToast("El intercambio debe incluir al menos una carta.");
    return;
  }

  if (!GameState.tradeState.acceptedActive || !GameState.tradeState.acceptedTarget) {
    showToast("Ambos jugadores deben aceptar el intercambio.");
    return;
  }

  // Quitar cartas de A y dárselas a B
  cardsA.forEach(id => {
    const cardObj = active.cartas.find(c => c.id === id);
    if (cardObj) {
      active.cartas = active.cartas.filter(c => c.id !== id);
      target.cartas.push(cardObj);
    }
  });

  // Quitar cartas de B y dárselas a A
  cardsB.forEach(id => {
    const cardObj = target.cartas.find(c => c.id === id);
    if (cardObj) {
      target.cartas = target.cartas.filter(c => c.id !== id);
      active.cartas.push(cardObj);
    }
  });

  // Reset del intercambio
  GameState.tradeState.offeredByActive = [];
  GameState.tradeState.offeredByTarget = [];
  GameState.tradeState.acceptedActive = false;
  GameState.tradeState.acceptedTarget = false;

  active.contadoresMisiones.intercambios += 1;
  updateHUD();
  setupTradeArena();
  showToast("🤝 ¡Intercambio completado con éxito!");
}

// ============================================================================
// Utilidad: Notificaciones Toast Flotantes
// ============================================================================
let toastTimer = null;
function showToast(message) {
  const toast = document.getElementById("toast-notification");
  const text = document.getElementById("toast-text");
  if (!toast || !text) return;

  text.textContent = message;
  toast.classList.add("active");

  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.classList.remove("active");
  }, 4000);
}
