# Gera index.html (arquivo único) embutindo as fotos da pasta fotos/ no template.
import base64, json, pathlib
root = pathlib.Path(__file__).parent
fotos = sorted((root / "fotos").glob("foto*.jpg"))
uris = ["data:image/jpeg;base64," + base64.b64encode(f.read_bytes()).decode() for f in fotos]
html = (root / "template.html").read_text(encoding="utf-8")
html = html.replace("/*__PHOTOS__*/[]", json.dumps(uris))
# playlist: musica.m4a primeiro, depois as faixas da pasta musicas/ (em ordem alfabética)
MIME = {".m4a": "audio/mp4", ".mp3": "audio/mpeg"}
faixas = [root / "musica.m4a"] + sorted(p for p in (root / "musicas").glob("*") if p.suffix.lower() in MIME)
faixas = [f for f in faixas if f.exists()]
musicas = [f"data:{MIME[f.suffix.lower()]};base64," + base64.b64encode(f.read_bytes()).decode() for f in faixas]
html = html.replace("/*__MUSIC__*/[]", json.dumps(musicas))
(root / "index.html").write_text(html, encoding="utf-8")
print(f"index.html gerado com {len(uris)} fotos e {len(musicas)} músicas ({len(html)//1024} KB)")
