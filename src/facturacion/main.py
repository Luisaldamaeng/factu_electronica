from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=BASE_DIR / "web" / "templates")

app = FastAPI(title="Facturacion Electronica SIFEN")
app.mount("/static", StaticFiles(directory=BASE_DIR / "web" / "static"), name="static")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="inicio.html",
        context={"titulo": "Inicio"},
    )
