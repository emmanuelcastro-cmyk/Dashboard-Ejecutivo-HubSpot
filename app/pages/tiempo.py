import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.layout import layout
from app.pages.resumen import filter_bar


def gran_button(label: str, val: str) -> rx.Component:
    return rx.el.button(
        label,
        on_click=lambda: DashboardState.set_time_granularity(val),
        class_name=rx.cond(
            DashboardState.time_granularity == val,
            "bg-[#DC2626] text-white px-4 py-2 rounded-full text-sm font-bold shadow-[0_0_15px_rgba(220,38,38,0.4)] transition-all",
            "bg-white/5 text-[#9CA3AF] hover:text-white px-4 py-2 rounded-full text-sm font-medium hover:bg-white/10 transition-all",
        ),
    )


def create_gradient(color: str, id_name: str) -> rx.Component:
    return rx.el.svg.defs(
        rx.el.svg.linear_gradient(
            rx.el.svg.stop(stop_color=color, offset="5%", stop_opacity=0.3),
            rx.el.svg.stop(stop_color=color, offset="95%", stop_opacity=0),
            x1=0,
            x2=0,
            y1=0,
            y2=1,
            id=id_name,
        )
    )


def ts_area_chart(title: str, data_key: str, color: str, id_name: str) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-semibold text-white mb-6"),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                horizontal=True,
                vertical=False,
                stroke="rgba(255,255,255,0.05)",
                stroke_dasharray="3 3",
            ),
            rx.recharts.graphing_tooltip(
                content_style={
                    "backgroundColor": "#141414",
                    "borderColor": "rgba(220,38,38,0.15)",
                    "borderRadius": "12px",
                    "color": "#fff",
                }
            ),
            create_gradient(color, id_name),
            rx.recharts.x_axis(
                data_key="month", stroke="#6b7280", tick_line=False, axis_line=False
            ),
            rx.recharts.y_axis(stroke="#6b7280", tick_line=False, axis_line=False),
            rx.recharts.area(
                data_key=data_key,
                stroke=color,
                fill=f"url(#{id_name})",
                type_="monotone",
                name=title,
            ),
            data=DashboardState.time_series_data,
            width="100%",
            height=300,
            margin={"left": 0, "right": 20, "top": 10, "bottom": 0},
        ),
        class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] p-6 rounded-2xl shadow-xl w-full",
    )


def tiempo() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.h1(
                "Desglose por Tiempo", class_name="text-4xl font-bold text-white mb-8"
            ),
            filter_bar(),
            rx.el.div(
                rx.el.span(
                    "Agrupar por:", class_name="text-sm font-medium text-[#9CA3AF] mr-4"
                ),
                rx.el.div(
                    gran_button("Día", "day"),
                    gran_button("Semana", "week"),
                    gran_button("Mes", "month"),
                    gran_button("Año", "year"),
                    class_name="flex items-center gap-2",
                ),
                class_name="flex items-center mb-8 bg-[#141414] border border-[rgba(220,38,38,0.12)] p-4 rounded-xl w-fit",
            ),
            rx.el.div(
                ts_area_chart("Nuevos Negocios", "deals", "#DC2626", "dealGradient"),
                ts_area_chart("kWh Total", "kwh", "#10B981", "kwhGradient"),
                ts_area_chart("Revenue (USD)", "revenue", "#F59E0B", "revenueGradient"),
                rx.el.div(
                    rx.el.h3(
                        "Distribución de Negocios (kWh vs USD)",
                        class_name="text-lg font-semibold text-white mb-6",
                    ),
                    rx.recharts.scatter_chart(
                        rx.recharts.cartesian_grid(
                            stroke_dasharray="3 3", stroke="rgba(255,255,255,0.05)"
                        ),
                        rx.recharts.graphing_tooltip(
                            cursor={"strokeDasharray": "3 3"},
                            content_style={
                                "backgroundColor": "#141414",
                                "borderColor": "rgba(220,38,38,0.15)",
                                "borderRadius": "12px",
                            },
                        ),
                        rx.recharts.x_axis(
                            data_key="kwh", type_="number", name="kWh", stroke="#6b7280"
                        ),
                        rx.recharts.y_axis(
                            data_key="amount",
                            type_="number",
                            name="USD",
                            stroke="#6b7280",
                        ),
                        rx.recharts.scatter(
                            name="Negocios",
                            data=DashboardState.scatter_data,
                            fill="#DC2626",
                        ),
                        width="100%",
                        height=300,
                        margin={"left": 20, "right": 20, "top": 10, "bottom": 10},
                    ),
                    class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] p-6 rounded-2xl shadow-xl flex-1",
                ),
                class_name="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-12",
            ),
            class_name="max-w-7xl mx-auto",
        )
    )