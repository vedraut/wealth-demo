/**
 * Wealth AI — Memory Architecture Presentation
 * 4 slides: Title · Agent Memory Diagram · RAG Architecture · Microsoft Mapping
 */

const pptxgen = require('pptxgenjs');
const path = require('path');

const LOGO = '/home/ved/laracorp/wealth-demo/exaze.png';
const OUT  = path.join(__dirname, 'wealth-ai-memory-architecture.pptx');

// ── Design tokens — Light Finance Theme (no # prefix for PptxGenJS) ──────────
const C = {
  bg:          'F1F5F9',  // light slate body
  header:      '1E40AF',  // bright blue — header & footer bars
  card:        'FFFFFF',  // white cards
  shared_fill: 'DBEAFE',  // light blue — centralized memory box
  border:      'CBD5E1',  // light gray borders
  primary:     '2563EB',  // blue
  purple:      '7C3AED',  // purple
  cyan:        '0891B2',  // teal/cyan
  success:     '059669',  // green
  warning:     'D97706',  // amber
  danger:      'DC2626',  // red
  gold:        'B45309',  // dark gold
  text:        '0F172A',  // near-black body text
  text_sec:    '475569',  // slate secondary
  text_muted:  '94A3B8',  // light slate muted
  header_text: 'E2E8F0',  // light text on dark header bars
};

// Logo is 499×499 (square)
const LOGO_W = 0.52, LOGO_H = 0.52;

// ── Helpers ───────────────────────────────────────────────────────────────────

function bg(slide, pptx) {
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 5.625,
    fill: { color: C.bg }, line: { width: 0 },
  });
}

function header(slide, pptx, title) {
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.75,
    fill: { color: C.header }, line: { width: 0 },
  });
  // White left accent on blue header bar
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.07, h: 0.75,
    fill: { color: 'FFFFFF' }, line: { width: 0 },
  });
  slide.addText(title, {
    x: 0.25, y: 0, w: 8, h: 0.75,
    fontFace: 'Arial', fontSize: 17, bold: true,
    color: C.header_text, valign: 'middle',
  });
  // Logo top-right
  slide.addImage({ path: LOGO, x: 10 - LOGO_W - 0.18, y: 0.12, w: LOGO_W, h: LOGO_H });
}

function bottomBar(slide, pptx, text) {
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 5.25, w: 10, h: 0.375,
    fill: { color: C.header }, line: { width: 0 },
  });
  slide.addText(text, {
    x: 0.3, y: 5.255, w: 9.4, h: 0.36,
    fontFace: 'Arial', fontSize: 7.5, color: 'DBEAFE',
    align: 'center', valign: 'middle',
  });
}

function sectionLabel(slide, text, x, y, color) {
  slide.addText(text, {
    x, y, w: 9.5, h: 0.22,
    fontFace: 'Arial', fontSize: 7.5, bold: true,
    color: color || C.text_muted, charSpacing: 1.2,
  });
}

// Thin vertical connector
function connector(slide, pptx, cx, y1, y2, color) {
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: cx - 0.025, y: y1, w: 0.05, h: y2 - y1,
    fill: { color, transparency: 25 }, line: { width: 0 },
  });
}

// Thin horizontal arrow
function hArrow(slide, pptx, x, y, w, color) {
  slide.addShape(pptx.shapes.RECTANGLE, {
    x, y: y - 0.02, w, h: 0.04,
    fill: { color, transparency: 20 }, line: { width: 0 },
  });
  // Arrowhead (small triangle approximation via narrow tall rect)
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: x + w - 0.01, y: y - 0.06, w: 0.07, h: 0.12,
    fill: { color, transparency: 20 }, line: { width: 0 },
  });
}

function roundBox(slide, pptx, x, y, w, h, fillColor, borderColor, borderW) {
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.08,
    fill: { color: fillColor },
    line: { color: borderColor, width: borderW || 2 },
  });
}

// ── SLIDE 1: TITLE ────────────────────────────────────────────────────────────
function slide1(pptx) {
  const s = pptx.addSlide();
  bg(s, pptx);

  // Left accent stripe
  s.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.09, h: 5.625,
    fill: { color: C.primary }, line: { width: 0 },
  });

  // Subtle top-right corner accent
  s.addShape(pptx.shapes.RECTANGLE, {
    x: 7.5, y: 0, w: 2.5, h: 2.2,
    fill: { color: C.primary, transparency: 96 }, line: { width: 0 },
  });

  // Logo
  s.addImage({ path: LOGO, x: 9.2, y: 0.22, w: LOGO_W, h: LOGO_H });

  // Main title
  s.addText('Agentic Memory Management', {
    x: 0.5, y: 1.3, w: 9, h: 0.95,
    fontFace: 'Arial', fontSize: 38, bold: true,
    color: C.text, align: 'center',   // C.text = 0F172A on light bg ✓
  });

  // Subtitle
  s.addText('Centralized & Distributed Memory in Multi-Agent AI Systems', {
    x: 0.5, y: 2.35, w: 9, h: 0.52,
    fontFace: 'Arial', fontSize: 15.5,
    color: C.text_sec, align: 'center',
  });

  // Divider
  s.addShape(pptx.shapes.RECTANGLE, {
    x: 3.2, y: 3.02, w: 3.6, h: 0.04,
    fill: { color: C.primary }, line: { width: 0 },
  });

  // Tag pills
  const tags = [
    { t: 'LangGraph',            c: C.primary  },
    { t: 'AI Memory Management', c: C.purple   },
    { t: 'RAG',                  c: C.success  },
    { t: 'Wealth Management',    c: C.gold     },
  ];
  const tw = 1.9, th = 0.32, tgap = 0.12;
  const totalTW = tags.length * tw + (tags.length - 1) * tgap;
  let tx = (10 - totalTW) / 2;

  for (const tag of tags) {
    s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: tx, y: 3.18, w: tw, h: th, rectRadius: 0.1,
      fill: { color: tag.c, transparency: 82 },
      line: { color: tag.c, width: 1 },
    });
    s.addText(tag.t, {
      x: tx, y: 3.18, w: tw, h: th,
      fontFace: 'Arial', fontSize: 8.5, bold: true,
      color: tag.c, align: 'center', valign: 'middle',
    });
    tx += tw + tgap;
  }

  // Description line
  s.addText('A multi-agent AI pipeline using LangGraph — mapping to Microsoft Azure enterprise architecture', {
    x: 0.8, y: 3.7, w: 8.4, h: 0.35,
    fontFace: 'Arial', fontSize: 9.5,
    color: C.text_sec, align: 'center', italic: true,
  });

  bottomBar(s, pptx, 'Confidential  ·  Internal Demo  ·  Exaze AI');
}

// ── SLIDE 2: AGENT MEMORY ARCHITECTURE ───────────────────────────────────────
function slide2(pptx) {
  const s = pptx.addSlide();
  bg(s, pptx);
  header(s, pptx, 'Agent Memory Architecture');

  // ── CENTRALIZED SHARED MEMORY ──────────────────────────────────────────────
  sectionLabel(s, 'CENTRALIZED  SHARED  MEMORY', 0.45, 0.82, C.primary);

  // Main shared memory box
  roundBox(s, pptx, 0.45, 1.03, 9.1, 0.88, C.shared_fill, C.primary, 2);

  s.addText('LangGraph Shared State   ·   SQLite Client Database', {
    x: 0.55, y: 1.05, w: 8.9, h: 0.3,
    fontFace: 'Arial', fontSize: 10.5, bold: true,
    color: C.primary, align: 'center', valign: 'middle',
  });

  // Data chips inside shared memory
  const chips = ['Client Profile', 'Portfolio Holdings', 'Tax Regime', 'Transactions', 'Annual Income'];
  const cw = 1.56, ch = 0.26, cgap = 0.065;
  const totalCW = chips.length * cw + (chips.length - 1) * cgap;
  let cx = (10 - totalCW) / 2;
  for (const chip of chips) {
    s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: cx, y: 1.49, w: cw, h: ch, rectRadius: 0.07,
      fill: { color: 'FFFFFF' }, line: { color: C.primary, width: 1 },
    });
    s.addText(chip, {
      x: cx, y: 1.49, w: cw, h: ch,
      fontFace: 'Arial', fontSize: 7.5,
      color: C.primary, align: 'center', valign: 'middle',
    });
    cx += cw + cgap;
  }

  // ── THREE AGENTS ────────────────────────────────────────────────────────────
  const agentCXs = [1.85, 5.0, 8.15];
  const agentW = 2.62, agentH = 0.82, agentY = 2.33;
  const sharedBottom = 1.91;

  const agents = [
    { label: 'Data Retrieval Agent', sub: 'Fetches & structures\nclient portfolio data', color: C.primary  },
    { label: 'Tax Analysis Agent',   sub: 'Applies IT Act 2025\n& flags opportunities',  color: C.purple  },
    { label: 'Advisory Agent',       sub: 'Generates strategy\n& recommendations',       color: C.cyan    },
  ];

  for (let i = 0; i < agents.length; i++) {
    const ag = agents[i];
    const ax = agentCXs[i] - agentW / 2;

    // Connector: shared memory → agent
    connector(s, pptx, agentCXs[i], sharedBottom, agentY, ag.color);

    // Agent box
    roundBox(s, pptx, ax, agentY, agentW, agentH, C.card, ag.color, 2.5);

    s.addText(ag.label, {
      x: ax + 0.08, y: agentY + 0.06, w: agentW - 0.16, h: 0.34,
      fontFace: 'Arial', fontSize: 10.5, bold: true,
      color: ag.color, align: 'center', valign: 'middle',
    });
    s.addText(ag.sub, {
      x: ax + 0.08, y: agentY + 0.42, w: agentW - 0.16, h: 0.38,
      fontFace: 'Arial', fontSize: 8, color: C.text_sec,
      align: 'center', valign: 'top',
    });
  }

  // ── DISTRIBUTED MEMORY BOXES ─────────────────────────────────────────────
  sectionLabel(s, 'DISTRIBUTED  (AGENT-PRIVATE)  MEMORY', 0.45, 3.23, C.text_muted);

  const agentBottom = agentY + agentH;
  const memY = 3.44, memW = 2.72, memH = 1.58;

  const mems = [
    {
      cx: 1.85, color: C.primary,
      title: 'DB Schema Memory',
      items: ['Schema definitions', 'SQL query templates', 'Field type mappings', 'Data transformations'],
    },
    {
      cx: 5.0, color: C.purple,
      title: 'Tax Domain Memory',
      items: ['IT Act 2025 rules', 'Section 80C / 80CCD', 'LTCG & STCG limits', 'Capital gains tables'],
    },
    {
      cx: 8.15, color: C.cyan,
      title: 'Market Domain Memory',
      items: ['Asset benchmarks', 'RBI / SEBI guidelines', 'Fund performance data', 'Rebalancing models'],
    },
  ];

  for (const mem of mems) {
    const mx = mem.cx - memW / 2;

    // Connector: agent → memory
    connector(s, pptx, mem.cx, agentBottom, memY, mem.color);

    // Memory box (light card)
    roundBox(s, pptx, mx, memY, memW, memH, 'FFFFFF', mem.color, 1.5);

    // Title
    s.addText(mem.title, {
      x: mx, y: memY + 0.08, w: memW, h: 0.28,
      fontFace: 'Arial', fontSize: 9, bold: true,
      color: mem.color, align: 'center',
    });

    // Thin divider inside box
    s.addShape(pptx.shapes.RECTANGLE, {
      x: mx + 0.18, y: memY + 0.38, w: memW - 0.36, h: 0.025,
      fill: { color: C.border }, line: { width: 0 },
    });

    // Items
    const itemRows = mem.items.map((it, idx) => [
      { text: '-  ', options: { color: mem.color, bold: true } },
      { text: it + (idx < mem.items.length - 1 ? '\n' : ''), options: { color: C.text_sec } },
    ]).flat();

    s.addText(itemRows, {
      x: mx + 0.15, y: memY + 0.46, w: memW - 0.3, h: memH - 0.58,
      fontFace: 'Arial', fontSize: 8.2, valign: 'top', paraSpaceAfter: 1.5,
    });
  }

  bottomBar(s, pptx, 'Shared state ensures data consistency  ·  Distributed memory enables domain depth  ·  Sequential pipeline: Data → Tax → Advisory');
}

// ── SLIDE 3: RAG & INDEXING ARCHITECTURE ─────────────────────────────────────
function slide3(pptx) {
  const s = pptx.addSlide();
  bg(s, pptx);
  header(s, pptx, 'Distributed Memory: RAG & Indexing Architecture');

  s.addText('How each agent retrieves its private domain knowledge at query time — prototype path and Azure enterprise path', {
    x: 0.25, y: 0.8, w: 9.2, h: 0.26,
    fontFace: 'Arial', fontSize: 8.8, italic: true, color: C.text_sec,
  });

  // Pipeline step definitions (same for both agents)
  const steps = [
    { label: 'Chunk',    sub: 'Split docs\ninto segments',    fill: 'EFF6FF' },  // light blue
    { label: 'Embed',    sub: 'Generate vector\nembeddings',  fill: 'F5F3FF' },  // light purple
    { label: 'Index',    sub: 'Azure AI Search\nvector store', fill: 'ECFDF5' }, // light green
    { label: 'Retrieve', sub: 'Semantic query\nat runtime',   fill: 'E0F2FE' },  // light cyan
  ];

  const srcX = 0.18, srcW = 1.82;
  const stepW = 1.12, stepGap = 0.09;
  const arrowW = 0.22;
  const pipeStart = srcX + srcW + arrowW;
  const pipeEnd = pipeStart + steps.length * stepW + (steps.length - 1) * stepGap;
  const agentX = pipeEnd + arrowW;
  const agentW = 1.6;

  function drawRow(rowY, rowH, agentLabel, agentColor, accentColor, sources) {
    // Source docs box
    roundBox(s, pptx, srcX, rowY, srcW, rowH, C.card, accentColor, 1.5);
    s.addText('Source Documents', {
      x: srcX, y: rowY + 0.07, w: srcW, h: 0.24,
      fontFace: 'Arial', fontSize: 8, bold: true,
      color: accentColor, align: 'center',
    });
    s.addShape(pptx.shapes.RECTANGLE, {
      x: srcX + 0.12, y: rowY + 0.33, w: srcW - 0.24, h: 0.02,
      fill: { color: C.border }, line: { width: 0 },
    });
    const srcItems = sources.map((t, i) => ({
      text: t + (i < sources.length - 1 ? '\n' : ''),
      options: { color: C.text_sec },
    }));
    s.addText(srcItems, {
      x: srcX + 0.1, y: rowY + 0.38, w: srcW - 0.2, h: rowH - 0.44,
      fontFace: 'Arial', fontSize: 7.5, valign: 'top',
    });

    // Arrow: source → pipeline
    hArrow(s, pptx, srcX + srcW, rowY + rowH / 2, arrowW, accentColor);

    // Pipeline steps
    for (let i = 0; i < steps.length; i++) {
      const st = steps[i];
      const sx = pipeStart + i * (stepW + stepGap);

      roundBox(s, pptx, sx, rowY, stepW, rowH, st.fill, accentColor, 1);

      s.addText(st.label, {
        x: sx, y: rowY + 0.1, w: stepW, h: 0.3,
        fontFace: 'Arial', fontSize: 10, bold: true,
        color: C.text, align: 'center',
      });
      s.addText(st.sub, {
        x: sx + 0.04, y: rowY + 0.45, w: stepW - 0.08, h: rowH - 0.55,
        fontFace: 'Arial', fontSize: 7.2, color: C.text_sec,
        align: 'center', valign: 'top',
      });

      // Arrow between steps
      if (i < steps.length - 1) {
        s.addShape(pptx.shapes.RECTANGLE, {
          x: sx + stepW, y: rowY + rowH / 2 - 0.02, w: stepGap, h: 0.04,
          fill: { color: accentColor, transparency: 35 }, line: { width: 0 },
        });
      }
    }

    // Arrow: pipeline → agent
    hArrow(s, pptx, pipeEnd, rowY + rowH / 2, arrowW, agentColor);

    // Agent box
    roundBox(s, pptx, agentX, rowY, agentW, rowH, C.card, agentColor, 2.5);
    s.addText(agentLabel, {
      x: agentX + 0.05, y: rowY, w: agentW - 0.1, h: rowH,
      fontFace: 'Arial', fontSize: 9.5, bold: true,
      color: C.text, align: 'center', valign: 'middle',
    });
  }

  // Row 1: Tax Agent
  sectionLabel(s, 'TAX AGENT — DOMAIN KNOWLEDGE (IT ACT 2025)', 0.18, 1.12, C.purple);
  drawRow(1.35, 1.5, 'Tax\nAnalysis\nAgent', C.purple, C.purple,
    ['IT Act 2025 PDF', 'CBDT Circulars', 'Sec 80C / 80CCD', 'LTCG Rules', 'Tax Orders']);

  // Divider between rows
  s.addShape(pptx.shapes.RECTANGLE, {
    x: 0.18, y: 2.92, w: 9.64, h: 0.02,
    fill: { color: C.border }, line: { width: 0 },
  });

  // Row 2: Advisory Agent
  sectionLabel(s, 'ADVISORY AGENT — DOMAIN KNOWLEDGE (MARKET & REGULATORY)', 0.18, 3.01, C.cyan);
  drawRow(3.22, 1.5, 'Advisory\nAgent', C.cyan, C.cyan,
    ['RBI Bulletins', 'SEBI Filings', 'Fund Factsheets', 'Nifty Data', 'Sector Reports']);

  bottomBar(s, pptx, 'Azure AI Search  ·  Vector embeddings per agent  ·  Semantic retrieval at query time  ·  Per-agent isolated knowledge index');
}

// ── SLIDE 4: MICROSOFT ECOSYSTEM MAPPING ─────────────────────────────────────
function slide4(pptx) {
  const s = pptx.addSlide();
  bg(s, pptx);
  header(s, pptx, 'Microsoft Ecosystem Mapping');

  s.addText('From open-source prototype to enterprise-grade Azure deployment — a clear transition path for each architectural component', {
    x: 0.25, y: 0.8, w: 9.2, h: 0.26,
    fontFace: 'Arial', fontSize: 8.8, italic: true, color: C.text_sec,
  });

  // Column header bar
  const colDefs = [
    { label: 'COMPONENT',            x: 0.22, w: 2.02, fill: '1E293B',   tc: 'CBD5E1'     },
    { label: 'PROTOTYPE (DEMO)',      x: 2.46, w: 3.28, fill: '1E293B',   tc: 'CBD5E1'     },
    { label: 'MICROSOFT ENTERPRISE', x: 5.96, w: 3.78, fill: 'DBEAFE',   tc: C.primary    },
  ];
  const hdrY = 1.12, hdrH = 0.38;
  for (const col of colDefs) {
    s.addShape(pptx.shapes.RECTANGLE, {
      x: col.x, y: hdrY, w: col.w, h: hdrH,
      fill: { color: col.fill }, line: { color: C.border, width: 0.5 },
    });
    s.addText(col.label, {
      x: col.x + 0.1, y: hdrY, w: col.w - 0.12, h: hdrH,
      fontFace: 'Arial', fontSize: 7.5, bold: true,
      color: col.tc, valign: 'middle', charSpacing: 0.8,
    });
  }

  // Table rows
  const rows = [
    { comp: 'Orchestration',            demo: 'LangGraph Python\n(agent wiring & shared state)',           ent: 'Azure AI Foundry\n(pro-code agent orchestration & governance)',  ec: C.primary  },
    { comp: 'User Interface',           demo: 'Streamlit\n(developer dashboard)',                          ent: 'Microsoft Copilot Studio\n(low-code conversational front door)',     ec: C.purple  },
    { comp: 'LLM Serving',             demo: 'Ollama + Kimi K2.6\n(local & OpenClaw gateway)',             ent: 'Azure Model Catalog\n(GPT-4o, Phi-4, open-weight models via API)', ec: C.cyan    },
    { comp: 'Centralized\nMemory',     demo: 'SQLite + LangGraph\nshared state object',                    ent: 'Microsoft Fabric / Azure SQL\n+ Foundry pipeline state',            ec: C.success },
    { comp: 'Distributed\nMemory',     demo: 'Domain rules\nembedded in agent prompts',                   ent: 'Azure AI Search\n(per-agent isolated vector indexes)',               ec: C.gold    },
    { comp: 'Response Cache',          demo: 'JSON file cache\n(Fast Mode toggle)',                        ent: 'Azure Cache for Redis\n(sub-10ms cached retrieval)',                ec: C.text_sec},
    { comp: 'Security &\nCompliance',  demo: 'Local only\n(no auth layer)',                                ent: 'Microsoft Entra ID + Purview\n(RBAC, audit trail, data lineage)',   ec: C.danger  },
    { comp: 'Observability',           demo: 'Agent Timeline UI\n(Streamlit in-app view)',                 ent: 'Azure Monitor + App Insights\n(distributed tracing, dashboards)',   ec: C.warning },
  ];

  const rowH = 0.445;
  const startY = hdrY + hdrH;

  for (let i = 0; i < rows.length; i++) {
    const row = rows[i];
    const y = startY + i * rowH;
    const rowBg = i % 2 === 0 ? 'FFFFFF' : 'F8FAFC';

    // Component cell
    s.addShape(pptx.shapes.RECTANGLE, {
      x: 0.22, y, w: 2.02, h: rowH,
      fill: { color: rowBg }, line: { color: C.border, width: 0.5 },
    });
    s.addText(row.comp, {
      x: 0.32, y, w: 1.84, h: rowH,
      fontFace: 'Arial', fontSize: 8.2, bold: true,
      color: C.text_sec, valign: 'middle',
    });

    // Demo cell
    s.addShape(pptx.shapes.RECTANGLE, {
      x: 2.46, y, w: 3.28, h: rowH,
      fill: { color: rowBg }, line: { color: C.border, width: 0.5 },
    });
    s.addText(row.demo, {
      x: 2.56, y, w: 3.1, h: rowH,
      fontFace: 'Arial', fontSize: 7.8,
      color: C.text_sec, valign: 'middle',
    });

    // Enterprise cell
    s.addShape(pptx.shapes.RECTANGLE, {
      x: 5.96, y, w: 3.78, h: rowH,
      fill: { color: rowBg }, line: { color: C.border, width: 0.5 },
    });
    // Colored left accent
    s.addShape(pptx.shapes.RECTANGLE, {
      x: 5.96, y: y + 0.07, w: 0.05, h: rowH - 0.14,
      fill: { color: row.ec }, line: { width: 0 },
    });
    s.addText(row.ent, {
      x: 6.07, y, w: 3.62, h: rowH,
      fontFace: 'Arial', fontSize: 7.8,
      color: C.text, valign: 'middle',
    });
  }

  bottomBar(s, pptx, 'Each component maps 1:1 to an Azure equivalent  ·  Prototype validates the architecture  ·  Production path is clear');
}

// ── HELPER: Reusable per-agent detail slide ───────────────────────────────────
function agentDetailSlide(pptx, cfg) {
  const {
    title, agentName, agentColor, tagline, historicalNote,
    inputs, outputs,
    cenMemItems, distMemItems, distMemFill,
    footer,
  } = cfg;

  const s = pptx.addSlide();
  bg(s, pptx);
  header(s, pptx, title);

  s.addText(tagline, {
    x: 0.25, y: 0.8, w: 9.5, h: 0.22,
    fontFace: 'Arial', fontSize: 8.5, italic: true, color: C.text_sec,
  });

  let flowY = 1.1;

  if (historicalNote) {
    s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: 0.25, y: 1.06, w: 9.5, h: 0.3, rectRadius: 0.05,
      fill: { color: 'FEF3C7' }, line: { color: C.warning, width: 1 },
    });
    s.addText('Historical context:  ' + historicalNote, {
      x: 0.38, y: 1.06, w: 9.24, h: 0.3,
      fontFace: 'Arial', fontSize: 7.8, color: C.gold, valign: 'middle',
    });
    flowY = 1.48;
  }

  const flowH = 1.0, agH = 1.2;
  const inX = 0.2, inW = 2.0, arrowW = 0.28;
  const agX = inX + inW + arrowW, agW = 4.5;
  const outX = agX + agW + arrowW, outW = 9.78 - outX;
  const agY = flowY - 0.1;

  // INPUT
  roundBox(s, pptx, inX, flowY, inW, flowH, 'F8FAFC', C.border, 1.5);
  s.addText('INPUT', {
    x: inX, y: flowY + 0.05, w: inW, h: 0.22,
    fontFace: 'Arial', fontSize: 7, bold: true, color: C.text_muted,
    align: 'center', charSpacing: 0.8,
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: inX + 0.12, y: flowY + 0.29, w: inW - 0.24, h: 0.018,
    fill: { color: C.border }, line: { width: 0 },
  });
  s.addText(inputs.map((t, i) => ({
    text: '· ' + t + (i < inputs.length - 1 ? '\n' : ''),
    options: { color: C.text_sec },
  })), {
    x: inX + 0.1, y: flowY + 0.33, w: inW - 0.2, h: flowH - 0.37,
    fontFace: 'Arial', fontSize: 7.3, valign: 'top',
  });

  // Arrow input → agent
  hArrow(s, pptx, inX + inW, flowY + flowH / 2, arrowW, agentColor);

  // AGENT BOX
  roundBox(s, pptx, agX, agY, agW, agH, C.card, agentColor, 2.5);
  s.addText(agentName, {
    x: agX + 0.12, y: agY, w: agW - 0.24, h: agH,
    fontFace: 'Arial', fontSize: 12.5, bold: true,
    color: agentColor, align: 'center', valign: 'middle',
  });

  // Arrow agent → output
  hArrow(s, pptx, agX + agW, flowY + flowH / 2, arrowW, agentColor);

  // OUTPUT
  roundBox(s, pptx, outX, flowY, outW, flowH, 'F0FDF4', C.success, 1.5);
  s.addText('OUTPUT', {
    x: outX, y: flowY + 0.05, w: outW, h: 0.22,
    fontFace: 'Arial', fontSize: 7, bold: true, color: C.success,
    align: 'center', charSpacing: 0.8,
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: outX + 0.12, y: flowY + 0.29, w: outW - 0.24, h: 0.018,
    fill: { color: C.success, transparency: 70 }, line: { width: 0 },
  });
  s.addText(outputs.map((t, i) => ({
    text: '· ' + t + (i < outputs.length - 1 ? '\n' : ''),
    options: { color: C.text_sec },
  })), {
    x: outX + 0.1, y: flowY + 0.33, w: outW - 0.2, h: flowH - 0.37,
    fontFace: 'Arial', fontSize: 7.3, valign: 'top',
  });

  // ── Memory section ────────────────────────────────────────────────────────────
  const agBottom = agY + agH;
  const memY = agBottom + 0.28;
  const memH = 5.1 - memY;
  const memW = (9.6 - 0.1) / 2;  // 4.75 each
  const cenX = 0.2, distX = cenX + memW + 0.1;

  connector(s, pptx, agX + agW / 2, agBottom, memY, agentColor);
  sectionLabel(s, 'MEMORY ARCHITECTURE', 0.25, agBottom + 0.04, C.text_muted);

  // Centralized
  roundBox(s, pptx, cenX, memY, memW, memH, C.shared_fill, C.primary, 1.5);
  s.addText('CENTRALIZED  SHARED  MEMORY', {
    x: cenX + 0.1, y: memY + 0.07, w: memW - 0.2, h: 0.24,
    fontFace: 'Arial', fontSize: 8, bold: true, color: C.primary, align: 'center',
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: cenX + 0.18, y: memY + 0.34, w: memW - 0.36, h: 0.018,
    fill: { color: C.primary, transparency: 65 }, line: { width: 0 },
  });
  s.addText(cenMemItems.map((t, i) => [
    { text: '·  ', options: { color: C.primary, bold: true } },
    { text: t + (i < cenMemItems.length - 1 ? '\n' : ''), options: { color: C.text_sec } },
  ]).flat(), {
    x: cenX + 0.15, y: memY + 0.4, w: memW - 0.3, h: memH - 0.48,
    fontFace: 'Arial', fontSize: 8, valign: 'top', paraSpaceAfter: 2,
  });

  // Distributed (agent-private RAG)
  roundBox(s, pptx, distX, memY, memW, memH, distMemFill || 'F5F3FF', agentColor, 1.5);
  s.addText('DISTRIBUTED  MEMORY  ·  RAG', {
    x: distX + 0.1, y: memY + 0.07, w: memW - 0.2, h: 0.24,
    fontFace: 'Arial', fontSize: 8, bold: true, color: agentColor, align: 'center',
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: distX + 0.18, y: memY + 0.34, w: memW - 0.36, h: 0.018,
    fill: { color: agentColor, transparency: 65 }, line: { width: 0 },
  });
  s.addText(distMemItems.map((t, i) => [
    { text: '·  ', options: { color: agentColor, bold: true } },
    { text: t + (i < distMemItems.length - 1 ? '\n' : ''), options: { color: C.text_sec } },
  ]).flat(), {
    x: distX + 0.15, y: memY + 0.4, w: memW - 0.3, h: memH - 0.48,
    fontFace: 'Arial', fontSize: 8, valign: 'top', paraSpaceAfter: 2,
  });

  bottomBar(s, pptx, footer);
}

// ── USE CASE CARD helper (for slide 9) ────────────────────────────────────────
function drawUseCaseCard(s, pptx, x, y, w, h, uc) {
  roundBox(s, pptx, x, y, w, h, C.card, uc.color, 1.5);
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h: 0.3, rectRadius: 0.08,
    fill: { color: uc.color, transparency: 12 }, line: { width: 0 },
  });
  s.addText(uc.num, {
    x: x + 0.1, y: y + 0.04, w: 0.42, h: 0.22,
    fontFace: 'Arial', fontSize: 9, bold: true, color: 'FFFFFF', align: 'center',
  });
  s.addText(uc.title, {
    x: x + 0.1, y: y + 0.32, w: w - 0.2, h: 0.42,
    fontFace: 'Arial', fontSize: 9.5, bold: true, color: uc.color, valign: 'top',
  });
  s.addText(uc.desc, {
    x: x + 0.1, y: y + 0.74, w: w - 0.2, h: h - 0.8,
    fontFace: 'Arial', fontSize: 7.6, color: C.text_sec, valign: 'top',
  });
}

// ── SLIDE 5: CLIENT REPORTING AUTOMATION ─────────────────────────────────────
function slide5(pptx) {
  agentDetailSlide(pptx, {
    title:       'Client Reporting Automation Agent',
    agentName:   'Client Reporting\nAgent',
    agentColor:  C.gold,
    distMemFill: 'FEFCE8',
    tagline:     'Generates personalized client reports at scale — what took a 3-day manual effort now takes 20 minutes across thousands of portfolios',
    inputs:  ['Client portfolio data', 'Benchmark & NAV feeds', 'Reporting period trigger', 'RM customization flags'],
    outputs: ['Personalized PDF report', 'RM review queue entry', 'Auto-distribution to client', 'Audit log entry'],
    cenMemItems: [
      'Client profile & communication prefs',
      'Portfolio holdings & weightings',
      'Transaction & SIP history',
      'Performance benchmarks (YTD / 1Y / 3Y)',
      'Tax summary & realized gains / losses',
    ],
    distMemItems: [
      'Report narrative templates (HNI / retail)',
      'Regulatory disclosure language',
      'Market commentary library (sector-wise)',
      'Fund performance & star rating data',
      'Benchmark index definitions (Nifty / Sensex)',
    ],
    footer: 'RAG-powered narrative generation  ·  Template-aware personalization per client segment  ·  Zero manual report writing',
  });
}

// ── SLIDE 6: TRADE RECONCILIATION ────────────────────────────────────────────
function slide6(pptx) {
  agentDetailSlide(pptx, {
    title:          'Trade Reconciliation Agent',
    agentName:      'Trade Reconciliation\nAgent',
    agentColor:     C.cyan,
    distMemFill:    'ECFEFF',
    tagline:        'Matches executed trades against custodian records end-of-day — auto-resolves common breaks, surfaces only genuine exceptions to ops team',
    historicalNote: 'Among the earliest AI use cases in capital markets — rule-based matching engines date to the 1990s. Modern LLM agents now handle unstructured exceptions and narrative break descriptions that rigid rules never could.',
    inputs:  ['EOD trade blotter', 'Custodian settlement records', 'Exchange confirmations', 'ISIN master reference'],
    outputs: ['Matched trade register', 'Break report with severity', 'Auto-resolved items log', 'Exception queue for ops'],
    cenMemItems: [
      'Internal trade blotter (all executed orders)',
      'Custodian & depository records',
      'Client account positions',
      'Settlement status & funding state',
      'Historical break resolution log',
    ],
    distMemItems: [
      'Reconciliation rule playbooks',
      'SEBI settlement cycle guidelines (T+1)',
      'NSE / BSE / CDSL exchange norms',
      'Break resolution decision tree',
      'Common exception pattern library',
    ],
    footer: 'Cuts reconciliation from hours to minutes  ·  Only genuine exceptions reach ops team  ·  Full audit trail maintained',
  });
}

// ── SLIDE 7: AI VOICE SUPPORT ─────────────────────────────────────────────────
function slide7(pptx) {
  agentDetailSlide(pptx, {
    title:       'AI Voice Support Assistant',
    agentName:   'Voice Support\nAgent',
    agentColor:  C.purple,
    distMemFill: 'F5F3FF',
    tagline:     'Handles inbound client calls autonomously — portfolio queries, SIP changes, redemptions — escalates to human RM only on genuine exceptions',
    inputs:  ['Inbound voice call (telephony)', 'Speech-to-text transcript', 'Client ID & auth token', 'Intent classification'],
    outputs: ['Voice response (TTS)', 'Action executed (SIP / redemption)', 'Escalation to live RM', 'CRM ticket created'],
    cenMemItems: [
      'Client account & KYC data',
      'Portfolio holdings & live NAV',
      'Open service tickets & history',
      'SIP schedules & redemption status',
      'Transaction & statement history',
    ],
    distMemItems: [
      'Product FAQ & knowledge base',
      'Fund / bond / FD catalog',
      'Compliance call scripts & disclosures',
      'Escalation decision tree',
      'SEBI investor grievance guidelines',
    ],
    footer: 'Handles 80%+ of Tier-1 calls autonomously  ·  Sub-2s response latency  ·  Full compliance call transcript logging',
  });
}

// ── SLIDE 8: REGULATORY COMPLIANCE ───────────────────────────────────────────
function slide8(pptx) {
  agentDetailSlide(pptx, {
    title:       'Regulatory Compliance Agent',
    agentName:   'Regulatory\nCompliance Agent',
    agentColor:  C.danger,
    distMemFill: 'FFF1F2',
    tagline:     'Scans all portfolios daily for SEBI / AMFI violations, insider-watch breaches, and concentration limit failures — zero manual compliance monitoring',
    inputs:  ['Live portfolio positions', 'Market data & NAV feed', 'Regulatory update alerts', 'Insider watch-list changes'],
    outputs: ['Daily compliance dashboard', 'Violation alerts to officer', 'Regulatory filing drafts', 'Audit trail (Azure Purview)'],
    cenMemItems: [
      'All client portfolio positions',
      'AUM & NAV data (all funds)',
      'Client classification (HNI / retail / institutional)',
      'Historical trade data (3-year lookback)',
      'Risk category & mandate restriction flags',
    ],
    distMemItems: [
      'SEBI regulations & latest circulars',
      'AMFI guidelines & concentration limits',
      'Insider trading watch-list (NSE / SEBI)',
      'PMLA & KYC compliance rules',
      'Mandate-specific restriction tables',
    ],
    footer: 'Daily automated scans replace weekly manual reviews  ·  Violation alerts within minutes of breach  ·  Full regulatory audit trail',
  });
}

// ── SLIDE 9: MORE USE CASES ──────────────────────────────────────────────────
function slide9(pptx) {
  const s = pptx.addSlide();
  bg(s, pptx);
  header(s, pptx, 'More Agentic Finance Use Cases');

  s.addText('Each use case below follows the same memory pattern — centralized client data + distributed domain knowledge — no additional architecture needed', {
    x: 0.25, y: 0.8, w: 9.5, h: 0.22,
    fontFace: 'Arial', fontSize: 8.5, italic: true, color: C.text_sec,
  });

  const cases = [
    {
      num: '01', color: C.primary,
      title: 'Intelligent Client Onboarding',
      desc: 'Conversational KYC collection, PAN/CIBIL verification, and risk profiling. Auto-populates CRM. RM handoff only at final sign-off — reduces onboarding from days to minutes.',
    },
    {
      num: '02', color: C.purple,
      title: 'Real-Time Portfolio Q&A',
      desc: '"What is my LTCG exposure if I sell today?" — Agent fetches live holdings, applies IT Act rules from RAG memory, and answers in seconds. No advisor needed for routine queries.',
    },
    {
      num: '03', color: C.success,
      title: 'Tax-Loss Harvesting Agent',
      desc: 'Nightly scan of all portfolios for unrealized losses that can offset LTCG. Flags 80C/80CCD shortfalls before fiscal year-end. Generates harvesting plan with projected savings.',
    },
    {
      num: '04', color: C.cyan,
      title: 'Portfolio Rebalancing Agent',
      desc: 'Monitors allocation drift daily. When equity/debt/gold drifts beyond threshold, proposes a rebalancing trade set with full tax impact — sent for one-click RM approval.',
    },
    {
      num: '05', color: C.gold,
      title: 'Document Intelligence Agent',
      desc: 'Continuously ingests fund factsheets, SEBI circulars, DRHP filings, and annual reports. Chunks, embeds, and indexes into per-fund isolated RAG vector stores — powering all other agents.',
    },
  ];

  const cardW = 2.95, cardH = 1.62, cardGap = 0.18;

  // Row 1 — 3 cards
  const r1TotalW = 3 * cardW + 2 * cardGap;
  const r1StartX = (10 - r1TotalW) / 2;
  for (let i = 0; i < 3; i++) {
    drawUseCaseCard(s, pptx, r1StartX + i * (cardW + cardGap), 1.1, cardW, cardH, cases[i]);
  }

  // Row 2 — 2 cards centered
  const r2TotalW = 2 * cardW + cardGap;
  const r2StartX = (10 - r2TotalW) / 2;
  for (let i = 0; i < 2; i++) {
    drawUseCaseCard(s, pptx, r2StartX + i * (cardW + cardGap), 1.1 + cardH + 0.22, cardW, cardH, cases[3 + i]);
  }

  bottomBar(s, pptx, 'Agentic AI in finance — from front desk to back office — every workflow benefits from centralized + distributed memory');
}

// ── MAIN ──────────────────────────────────────────────────────────────────────
async function main() {
  const pptx = new pptxgen();
  pptx.layout  = 'LAYOUT_16x9';
  pptx.author  = 'Exaze AI';
  pptx.company = 'Exaze';
  pptx.title   = 'Agentic Wealth Management — Memory Architecture';

  slide1(pptx);
  slide2(pptx);
  slide3(pptx);
  slide4(pptx);
  slide5(pptx);
  slide6(pptx);
  slide7(pptx);
  slide8(pptx);
  slide9(pptx);

  await pptx.writeFile({ fileName: OUT });
  console.log('Done:', OUT);
}

main().catch(err => { console.error(err); process.exit(1); });
