let pyodide = null;

async function loadPythonFile(path, target) {
  const res = await fetch(path + "?" + Date.now());
  const text = await res.text();

  // --- pastikan semua folder target ada ---
  const dirs = target.split("/").slice(1, -1); // semua folder sebelum file
  let current = "/";
  for (const dir of dirs) {
    try {
      pyodide.FS.mkdir(current + dir);
    } catch (e) {
      if (e.errno !== 20) throw e; // 17 = folder exists
    }
    current += dir + "/";
  }

  pyodide.FS.writeFile(target, text);
}

async function loadPyodideAndPackages() {
  const outputEl = document.getElementById("output");
  outputEl.textContent = "Memuat program...";

  pyodide = await loadPyodide();
  await pyodide.loadPackage(["pandas", "regex", "PyMuPDF"]);
  await loadPythonFile(
    "../utils/normalize_text.py",
    "/utils/normalize_text.py"
  );
  await loadPythonFile(
    "../utils/parse_articles.py",
    "/utils/parse_articles.py"
  );
  await loadPythonFile("../utils/patterns.py", "/utils/patterns.py");
  await pyodide.runPython(`
    import sys
    sys.path.append("/")
  `);

  outputEl.textContent = "";

  const input = document.getElementById("input");
  input.style.display = "block";
}

function readFileAsUint8Array(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(new Uint8Array(reader.result));
    reader.onerror = reject;
    reader.readAsArrayBuffer(file);
  });
}

function downloadSpreadsheet(data) {
  if (!data || !data.length) {
    alert("Tidak ada data untuk diunduh");
    return;
  }

  // Convert array of objects → worksheet
  const worksheet = XLSX.utils.json_to_sheet(data);

  // Buat workbook
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Data");

  // Trigger download
  XLSX.writeFile(workbook, "output.xlsx");
}

document.getElementById("run").addEventListener("click", async () => {
  const outputEl = document.getElementById("output");
  outputEl.textContent = "Sedang memproses...";

  const downloadBtn = document.getElementById("download");
  downloadBtn.style.display = "none";
  downloadBtn.onclick = undefined;

  const fileInputEl = document.getElementById("pdffile");
  if (!fileInputEl.files.length) return alert("Pilih file PDF dulu!");

  const pdfBytes = await readFileAsUint8Array(fileInputEl.files[0]);

  // Write PDF to Pyodide filesystem
  pyodide.FS.writeFile("/input.pdf", pdfBytes);

  // Python code untuk jalankan parser
  const pythonCode = `
from pathlib import Path
from utils.normalize_text import normalize_text
from utils.parse_articles import parse_articles

def extract_text(pdf_path: Path) -> str:
    import fitz  # PyMuPDF

    texts = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text("text")
            if text:
                texts.append(text)
    return "\\n".join(texts)

raw_text = extract_text("/input.pdf")
normalized_lines = normalize_text(raw_text)
parsed = parse_articles(normalized_lines)

parsed
`;

  const pyResult = await pyodide.runPythonAsync(pythonCode);
  pyodide.FS.unlink("/input.pdf");

  const result = pyResult.toJs({ dicts: true });
  pyResult.destroy();

  const resultStr = JSON.stringify(
    result,
    (_, value) => (value === undefined ? null : value),
    2
  );
  outputEl.textContent = resultStr;

  downloadBtn.style.display = "inline-block";
  downloadBtn.onclick = () => downloadSpreadsheet(result);
});

// Load Pyodide saat awal
loadPyodideAndPackages();
