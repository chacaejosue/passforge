import fs from "node:fs";
import path from "node:path";
import sharp from "sharp";

async function generateFavicons() {
  const publicDir = path.resolve("public");
  const svgPath = path.join(publicDir, "favicon.svg");

  if (!fs.existsSync(svgPath)) {
    throw new Error(`No se encontró el archivo SVG en: ${svgPath}`);
  }

  console.log("Generando variantes rasterizadas de favicons para PassForge...");

  // 1. Variantes individuales PNG
  const pngConfigs = [
    { name: "favicon-48x48.png", size: 48 },
    { name: "favicon-96x96.png", size: 96 },
    { name: "favicon-192x192.png", size: 192 },
    { name: "apple-touch-icon.png", size: 180 },
  ];

  for (const cfg of pngConfigs) {
    const dest = path.join(publicDir, cfg.name);
    await sharp(svgPath)
      .resize(cfg.size, cfg.size)
      .png({ compressionLevel: 9 })
      .toFile(dest);
    console.log(`  ✓ Creado: ${cfg.name} (${cfg.size}x${cfg.size})`);
  }

  // 2. Generar favicon.ico multi-resolución (16, 32, 48 px)
  const icoSizes = [16, 32, 48];
  const pngBuffers = [];
  for (const s of icoSizes) {
    const buf = await sharp(svgPath).resize(s, s).png().toBuffer();
    pngBuffers.push({ width: s, height: s, buffer: buf });
  }

  const count = pngBuffers.length;
  const header = Buffer.alloc(6);
  header.writeUInt16LE(0, 0); // Reservado
  header.writeUInt16LE(1, 2); // Tipo de archivo: 1 = ICO
  header.writeUInt16LE(count, 4); // Cantidad de imágenes

  let offset = 6 + count * 16;
  const dirEntries = [];
  for (const img of pngBuffers) {
    const entry = Buffer.alloc(16);
    entry.writeUInt8(img.width >= 256 ? 0 : img.width, 0);
    entry.writeUInt8(img.height >= 256 ? 0 : img.height, 1);
    entry.writeUInt8(0, 2); // Paleta
    entry.writeUInt8(0, 3); // Reservado
    entry.writeUInt16LE(1, 4); // Planos de color
    entry.writeUInt16LE(32, 6); // Bits por pixel
    entry.writeUInt32LE(img.buffer.length, 8); // Tamaño del buffer
    entry.writeUInt32LE(offset, 12); // Desplazamiento
    dirEntries.push(entry);
    offset += img.buffer.length;
  }

  const icoBuffer = Buffer.concat([header, ...dirEntries, ...pngBuffers.map((img) => img.buffer)]);
  fs.writeFileSync(path.join(publicDir, "favicon.ico"), icoBuffer);
  console.log("  ✓ Creado: favicon.ico (multi-resolución 16, 32, 48 px)");

  console.log("Todos los favicons de PassForge fueron generados exitosamente.");
}

generateFavicons().catch((err) => {
  console.error("Error al generar favicons:", err);
  process.exit(1);
});
