import reflex as rx
from app.pages.resumen import resumen
from app.pages.pipeline import pipeline
from app.pages.equipo import equipo
from app.pages.actividad import actividad
from app.pages.tiempo import tiempo
from app.pages.monitor import monitor
from app.pages.scorecard import scorecard
from app.pages.metas import metas
from app.states.dashboard_state import DashboardState
from app.states.scorecard_state import ScorecardState
from app.pages.reportes import reportes
from app.states.dashboard_state import DashboardState

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="icon", href="/white_q_red.png", type="image/png"),
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(resumen, route="/", on_load=DashboardState.load_data)
app.add_page(pipeline, route="/pipeline", on_load=DashboardState.load_data)
app.add_page(equipo, route="/equipo", on_load=DashboardState.load_data)
app.add_page(actividad, route="/actividad", on_load=DashboardState.load_data)
app.add_page(tiempo, route="/tiempo", on_load=DashboardState.load_data)
app.add_page(scorecard, route="/scorecard", on_load=DashboardState.load_data)
app.add_page(metas, route="/metas", on_load=DashboardState.load_data)
app.add_page(monitor, route="/monitor", on_load=DashboardState.load_data)
app.add_page(reportes, route="/reportes", on_load=DashboardState.load_data)