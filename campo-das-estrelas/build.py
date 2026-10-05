# Gera o jogo a partir do template.html:
#  - index.html: versão leve para o site (fotos/ e musicas/ ficam em arquivos separados e carregam aos poucos)
#  - index-arquivo-unico.html: tudo embutido num arquivo só (para abrir offline ou mandar por mensagem; fica fora do git)
import base64, json, pathlib
root = pathlib.Path(__file__).parent
fotos = sorted((root / "fotos").glob("foto*.jpg"))
MIME = {".m4a": "audio/mp4", ".mp3": "audio/mpeg"}
faixas = [root / "musica.m4a"] + sorted(p for p in (root / "musicas").glob("*") if p.suffix.lower() in MIME)  # musica.m4a primeiro, depois a pasta musicas/
faixas = [f for f in faixas if f.exists()]
template = (root / "template.html").read_text(encoding="utf-8")
def montar(fotos_src, musicas_src):
    return template.replace("/*__PHOTOS__*/[]", json.dumps(fotos_src)).replace("/*__MUSIC__*/[]", json.dumps(musicas_src))
rel = lambda f: f.relative_to(root).as_posix()
data = lambda f, mime: f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()

leve = montar([rel(f) for f in fotos], [rel(f) for f in faixas])
(root / "index.html").write_text(leve, encoding="utf-8")
print(f"index.html (site) gerado com {len(fotos)} fotos e {len(faixas)} músicas: {len(leve) // 1024} KB")
unico = montar([data(f, "image/jpeg") for f in fotos], [data(f, MIME[f.suffix.lower()]) for f in faixas])
(root / "index-arquivo-unico.html").write_text(unico, encoding="utf-8")
print(f"index-arquivo-unico.html gerado: {len(unico) // 1024} KB")
