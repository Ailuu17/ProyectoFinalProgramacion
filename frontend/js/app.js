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
const NOMBRE_EVENTO_VIGENTE = "Halloween";

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
      actividades_completadas: []
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
      actividades_completadas: []
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
      nombre: "Sobre Común",
      tipo: "estable",
      moneda: "comun",
      precio: 20,
      cantidad_cartas: 6,
      descripcion: "Contiene 6 criaturas míticas comunes o raras del reino antiguo.",
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
      descripcion: `Disponible solo durante ${NOMBRE_EVENTO_VIGENTE}. ¡Criaturas raras y legendarias!`,
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
        "Común": 45,
        "Rara": 35,
        "Súper Rara": 15,
        "Súper Súper Rara": 4,
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
        "Común": 20,
        "Rara": 35,
        "Súper Rara": 30,
        "Súper Súper Rara": 10,
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

  if (countBadge) {
    countBadge.textContent = `${filtered.length} de ${window.CRIATURAS_DATA.length} Criaturas`;
  }

  container.innerHTML = filtered.map(c => renderCreatureCardHTML(c, false)).join("");
}

// Renderizar HTML para una carta de criatura
function renderCreatureCardHTML(creatura, esCartaFisica = false, cartaId = null) {
  const rarezaClass = getRarityClass(creatura.rareza);
  const typeIcon = getTypeIcon(creatura.tipo);
  const artworkPath = getCreatureArtworkPath(creatura.nombre);

  return `
    <div class="creature-card ${rarezaClass}">
      <div class="card-top-info">
        <span class="card-code">${esCartaFisica ? cartaId : creatura.codigo}</span>
        <span class="card-rarity-badge" style="background: ${getRarityColor(creatura.rareza)}22; color: ${getRarityColor(creatura.rareza)};">
          ${creatura.rareza}
        </span>
      </div>

      <div class="card-illustration">
        ${artworkPath ? `<img class="creature-artwork" src="${artworkPath}" alt="${creatura.nombre}" loading="lazy" decoding="async" onerror="this.remove()">` : ""}
        <span aria-hidden="true">${typeIcon}</span>
      </div>

      <div>
        <div class="card-creature-name" title="${creatura.nombre}">${creatura.nombre}</div>
        <div class="card-type-tag">${creatura.tipo}</div>
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
  "Cocatriz.png", "Diabillo.png", "Diablo de Jersey.png", "Dragón de fuego.png",
  "Duendecillo.png", "Duendes de Hollín.png", "Espiritú errante.png",
  "Fenix Legendario.png", "Goblin.png", "Golem De Amatista.png",
  "Golem De Piedra.png", "Golem De Rayo.png", "Hada Del Agua.png",
  "Hada Del Bosque.png", "Hija De Lucifer.png", "Kitsune De Tres Colas.png",
  "Kranken Joven.png", "Leviatán.png", "Loquace (Pixie).png", "Mantícora.png",
  "Mooncalf.png", "Niño Fauno.png", "Nixie.png", "Oni Travieso.png",
  "Pegaso.png", "Pequeño Cíclope.png", "Pichón De Fénix.png",
  "Reina De Las Pixies.png", "Sirena.png", "Titán Del Viento.png",
  "Titán Niño.png", "Trío Dragónico.png", "Tritón.png",
  "Troll De Las Cavernas.png", "Troll Hechicero.png", "Unicornio.png",
  "Vita (Pixie).png"
];

const creatureArtworkByName = new Map(
  creatureArtworkFiles.map(filename => [
    normalizeArtworkName(filename.replace(/\.png$/i, "")),
    filename
  ])
);

const creatureArtworkAliases = {
  cocatricito: "Cocatriz.png",
  cocatrice: "Cocatriz.png",
  diablillo: "Diabillo.png",
  golemamatista: "Golem De Amatista.png",
  krakenjoven: "Kranken Joven.png",
  trolldecaverna: "Troll De Las Cavernas.png"
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

function getRarityColor(rareza) {
  const r = (rareza || "").toLowerCase();
  if (r.includes("com")) return "#94a3b8";
  if (r.includes("super super") || r.includes("súper súper") || r.includes("ssr")) return "#c084fc";
  if (r.includes("super") || r.includes("súper") || r.includes("sr")) return "#f59e0b";
  if (r.includes("rara")) return "#38bdf8";
  if (r.includes("legen")) return "#ef4444";
  if (r.includes("exclus")) return "#06b6d4";
  return "#94a3b8";
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

// ============================================================================
// VISTA: Mercado de Cartas y Sobres
// ============================================================================
function renderMarketView() {
  const player = getActivePlayer();
  const packsContainer = document.getElementById("market-packs-list");
  if (!packsContainer) return;

  packsContainer.innerHTML = GameState.sobres.map(sobre => {
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
          <span>${isEvent ? '🌙' : '🪙'}</span>
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
    exchangeRateSpan.textContent = `${GameState.eventoActivo.tasa_cambio} ${NOMBRE_MONEDA_COMUN} = 1 Jack`;
  }
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
      : elegirCriaturaAleatoria(window.CRIATURAS_DATA);
    const carta = crearCarta(plantilla.codigo);
    player.cartas.push(carta);
    cartasObtenidas.push(carta);
  }

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

  const rarezaNormalizada = normalizarRareza(rarezaElegida);
  const candidatas = window.CRIATURAS_DATA.filter(
    criatura => normalizarRareza(criatura.rareza) === rarezaNormalizada
  );
  if (candidatas.length === 0) {
    throw new Error(`No hay criaturas disponibles de rareza "${rarezaElegida}".`);
  }
  return elegirCriaturaAleatoria(candidatas);
}

function normalizarRareza(rareza) {
  return rareza.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
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
        slotEl.className = "trade-card-slot filled";
        slotEl.innerHTML = `
          <span style="font-size: 1.2rem;">${getTypeIcon(carta.plantilla.tipo)}</span>
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
        slotEl.className = "trade-card-slot filled";
        slotEl.innerHTML = `
          <span style="font-size: 1.2rem;">${getTypeIcon(carta.plantilla.tipo)}</span>
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
        return `
          <button class="action-pill-btn" style="font-size: 0.75rem; padding: 0.35rem 0.6rem; ${isSelected ? 'border-color: #e6b450; background: rgba(230,180,80,0.2);' : ''}"
            onclick="toggleOfferCard('active', '${c.id}')">
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
        return `
          <button class="action-pill-btn" style="font-size: 0.75rem; padding: 0.35rem 0.6rem; ${isSelected ? 'border-color: #a855f7; background: rgba(168,85,247,0.2);' : ''}"
            onclick="toggleOfferCard('target', '${c.id}')">
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
