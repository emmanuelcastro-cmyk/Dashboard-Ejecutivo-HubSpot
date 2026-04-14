import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.layout import layout
from app.pages.resumen import filter_bar


def tooltip_style():
    return {
        "backgroundColor": "#141414",
        "borderColor": "rgba(220,38,38,0.15)",
        "borderRadius": "12px",
        "color": "#ffffff",
        "fontSize": "13px",
        "padding": "10px 14px",
    }


def status_card(
    title: str, key: str, icon: str, color: str = "#1F659D"
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                title,
                class_name="text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider truncate max-w-[150px]",
                title=title,
            ),
            rx.icon(icon, class_name="h-4 w-4", style={"color": color}),
            class_name="flex justify-between items-center mb-3",
        ),
        rx.el.h3(
            DashboardState.status_distribution[key].to_string(),
            class_name="text-xl font-bold text-white mb-1",
        ),
        rx.el.span(
            DashboardState.status_distribution[f"{key}_pct"].to_string(),
            class_name="text-[10px] text-[#6B7280] font-bold",
        ),
        class_name="bg-[#0E0E0E] border border-white/5 rounded-xl p-4 shadow-sm hover:border-white/10 transition-all",
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


def pipeline_ventas_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Pipeline de Ventas", class_name="text-lg font-semibold mb-6 text-white"
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", stroke="rgba(255,255,255,0.05)"
            ),
            rx.recharts.graphing_tooltip(
                content_style=tooltip_style(),
                label_style={"color": "#ffffff"},
                item_style={"color": "#e5e7eb"},
                cursor={"fill": "rgba(255,255,255,0.05)"},
            ),
            rx.recharts.x_axis(
                data_key="stage_name",
                stroke="#6b7280",
                angle=-35,
                text_anchor="end",
                height=120,
                interval=0,
            ),
            rx.recharts.y_axis(stroke="#6b7280"),
            rx.recharts.bar(
                data_key="count",
                fill="#1F659D",
                name="Negocios",
                radius=[4, 4, 0, 0],
                bar_size=30,
            ),
            data=DashboardState.pipeline_ventas_bar_data,
            width="100%",
            height=450,
            margin={"left": 20, "right": 20, "top": 20, "bottom": 20},
        ),
        class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] p-6 rounded-2xl shadow-xl w-full mb-8 overflow-hidden",
    )


def pipeline_socios_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Pipeline de Socios", class_name="text-lg font-semibold mb-6 text-white"
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", stroke="rgba(255,255,255,0.05)"
            ),
            rx.recharts.graphing_tooltip(
                content_style=tooltip_style(),
                label_style={"color": "#ffffff"},
                item_style={"color": "#e5e7eb"},
                cursor={"fill": "rgba(255,255,255,0.05)"},
            ),
            rx.recharts.x_axis(
                data_key="stage_name",
                stroke="#6b7280",
                angle=-35,
                text_anchor="end",
                height=120,
                interval=0,
            ),
            rx.recharts.y_axis(stroke="#6b7280"),
            rx.recharts.bar(
                data_key="count",
                fill="#10B981",
                name="Negocios",
                radius=[4, 4, 0, 0],
                bar_size=30,
            ),
            data=DashboardState.pipeline_socios_bar_data,
            width="100%",
            height=450,
            margin={"left": 20, "right": 20, "top": 20, "bottom": 20},
        ),
        class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] p-6 rounded-2xl shadow-xl w-full mb-8 overflow-hidden",
    )


def pipeline() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.h1(
                "Pipeline Detallado", class_name="text-4xl font-bold text-white mb-8"
            ),
            filter_bar(),
            rx.cond(
                DashboardState.selected_pipeline != "803674731",
                pipeline_ventas_chart(),
                rx.fragment(),
            ),
            rx.cond(
                DashboardState.selected_pipeline != "default",
                pipeline_socios_chart(),
                rx.fragment(),
            ),
            rx.el.div(
                rx.el.h2(
                    "Creación de Negocios en el Tiempo",
                    class_name="text-lg font-semibold mb-6 text-white",
                ),
                rx.recharts.area_chart(
                    rx.recharts.cartesian_grid(
                        horizontal=True,
                        vertical=False,
                        stroke_dasharray="3 3",
                        stroke="rgba(255,255,255,0.05)",
                    ),
                    rx.recharts.graphing_tooltip(
                        content_style=tooltip_style(),
                        label_style={"color": "#ffffff"},
                        item_style={"color": "#e5e7eb"},
                    ),
                    create_gradient("#1F659D", "ventasGrad"),
                    create_gradient("#10B981", "sociosGrad"),
                    rx.recharts.x_axis(data_key="month", stroke="#6b7280"),
                    rx.recharts.y_axis(stroke="#6b7280"),
                    rx.recharts.area(
                        data_key="Ventas",
                        stroke="#1F659D",
                        fill="url(#ventasGrad)",
                        type_="monotone",
                    ),
                    rx.recharts.area(
                        data_key="Socios",
                        stroke="#10B981",
                        fill="url(#sociosGrad)",
                        type_="monotone",
                    ),
                    rx.recharts.brush(
                        data_key="month", height=30, stroke="#DC2626", fill="#0E0E0E"
                    ),
                    data=DashboardState.pipeline_monthly_trend,
                    width="100%",
                    height=350,
                    margin={"left": 0, "right": 20, "top": 10, "bottom": 10},
                ),
                class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] p-6 rounded-2xl mb-8 shadow-xl w-full",
            ),
            rx.el.div(
                rx.el.h2(
                    "Distribución de kWh vs USD por Pipeline",
                    class_name="text-lg font-semibold mb-6 text-white",
                ),
                rx.recharts.scatter_chart(
                    rx.recharts.cartesian_grid(
                        stroke_dasharray="3 3", stroke="rgba(255,255,255,0.05)"
                    ),
                    rx.recharts.graphing_tooltip(
                        cursor={"strokeDasharray": "3 3"},
                        content_style=tooltip_style(),
                        label_style={"color": "#ffffff"},
                        item_style={"color": "#e5e7eb"},
                    ),
                    rx.recharts.x_axis(
                        data_key="kwh", type_="number", name="kWh", stroke="#6b7280"
                    ),
                    rx.recharts.y_axis(
                        data_key="amount", type_="number", name="USD", stroke="#6b7280"
                    ),
                    rx.recharts.scatter(
                        name="Ventas",
                        data=DashboardState.pipeline_scatter_ventas,
                        fill="#1F659D",
                    ),
                    rx.recharts.scatter(
                        name="Socios",
                        data=DashboardState.pipeline_scatter_socios,
                        fill="#10B981",
                    ),
                    width="100%",
                    height=350,
                    margin={"left": 20, "right": 20, "top": 10, "bottom": 10},
                ),
                class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] p-6 rounded-2xl mb-8 shadow-xl w-full",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Distribución por Status",
                        class_name="text-lg font-semibold mb-6 text-white",
                    ),
                    rx.el.div(
                        status_card(
                            "Negociación", "Negociación", "handshake", "#F59E0B"
                        ),
                        status_card(
                            "Convenio Enviado", "Convenio Enviado", "send", "#22D3EE"
                        ),
                        status_card(
                            "Convenio Firmado",
                            "Convenio Firmado",
                            "message_circle_check",
                            "#10B981",
                        ),
                        status_card(
                            "Socio Interesado",
                            "Socio Interesado",
                            "user-plus",
                            "#A78BFA",
                        ),
                        status_card(
                            "Propuesta Enviada",
                            "Propuesta Enviada",
                            "file-text",
                            "#3B82F6",
                        ),
                        status_card(
                            "Cerrado Perdido",
                            "Cerrado Perdido",
                            "message_circle_x",
                            "#EF4444",
                        ),
                        status_card("Sin Etapa", "Sin Etapa", "circle_help", "#6B7280"),
                        class_name="grid grid-cols-2 md:grid-cols-3 gap-4 flex-1",
                    ),
                ),
                rx.el.div(
                    rx.recharts.pie_chart(
                        rx.recharts.graphing_tooltip(
                            content_style=tooltip_style(),
                            label_style={"color": "#ffffff"},
                            item_style={"color": "#e5e7eb"},
                        ),
                        rx.recharts.pie(
                            data=DashboardState.status_pie_data,
                            data_key="value",
                            name_key="name",
                            cx="50%",
                            cy="50%",
                            inner_radius=60,
                            outer_radius=100,
                            padding_angle=2,
                            stroke="none",
                            stroke_width=0,
                        ),
                        width="100%",
                        height=300,
                    ),
                    class_name="flex items-center justify-center min-w-[300px]",
                ),
                class_name="flex flex-col xl:flex-row gap-8 bg-[#141414] border border-[rgba(220,38,38,0.12)] p-8 rounded-2xl shadow-xl",
            ),
            class_name="max-w-7xl mx-auto pb-20 flex flex-col",
        )
    )