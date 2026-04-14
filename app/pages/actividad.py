import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.layout import layout
from app.pages.resumen import filter_bar


def vertical_bar(data: dict, gradient_classes: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name=f"w-full rounded-t-sm {gradient_classes} transition-all duration-500 hover:brightness-110",
                style={"height": f"{data['bar_pct']}%"},
                title=data["count"].to_string(),
            ),
            class_name="h-40 w-8 flex items-end justify-center bg-white/5 rounded-t-sm overflow-hidden group relative",
        ),
        rx.el.span(
            data["label"],
            class_name="text-[10px] text-gray-400 mt-2 rotate-45 md:rotate-0 origin-left",
        ),
        class_name="flex flex-col items-center gap-1",
    )


def stage_movement_card(data: dict) -> rx.Component:
    return rx.el.div(
        rx.el.h4(
            data["stage"],
            class_name="text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider mb-3",
        ),
        rx.el.div(
            rx.el.span(
                data["count"].to_string(), class_name="text-3xl font-bold text-white"
            ),
            rx.el.div(
                rx.cond(
                    data["is_positive"],
                    rx.icon("trending-up", class_name="h-4 w-4 text-[#10B981]"),
                    rx.icon("trending-down", class_name="h-4 w-4 text-[#EF4444]"),
                ),
                rx.el.span(
                    data["delta"],
                    class_name=rx.cond(
                        data["is_positive"],
                        "text-sm font-bold text-[#10B981]",
                        "text-sm font-bold text-[#EF4444]",
                    ),
                ),
                class_name="flex items-center gap-1 bg-white/5 px-2 py-1 rounded-lg",
            ),
            class_name="flex items-center justify-between",
        ),
        class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] p-5 rounded-2xl shadow-sm",
    )


def comparison_row(data: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            data["metric"],
            class_name="px-6 py-4 text-sm font-medium text-white whitespace-nowrap",
        ),
        rx.el.td(
            data["w0"], class_name="px-6 py-4 text-sm text-[#9CA3AF] whitespace-nowrap"
        ),
        rx.el.td(
            data["w1"], class_name="px-6 py-4 text-sm text-[#9CA3AF] whitespace-nowrap"
        ),
        rx.el.td(
            data["w2"], class_name="px-6 py-4 text-sm text-[#9CA3AF] whitespace-nowrap"
        ),
        rx.el.td(
            rx.el.span(
                data["delta"],
                class_name="px-2 py-1 rounded-lg text-xs font-bold",
                style={"color": data["color"], "backgroundColor": data["color"] + "1a"},
            ),
            class_name="px-6 py-4 text-sm whitespace-nowrap",
        ),
        class_name="border-b border-white/5 hover:bg-[#1A1A1A] transition-colors",
    )


def sankey_bar(data: dict, index: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                data["stage"],
                class_name="text-sm font-semibold text-[#9CA3AF] z-10 w-1/3",
            ),
            rx.el.div(
                rx.el.div(
                    class_name=rx.cond(
                        index == 5,
                        "h-full bg-gradient-to-r from-[#EF4444]/40 to-[#EF4444]/80 rounded-r-lg transition-all",
                        "h-full bg-gradient-to-r from-[#1F659D]/40 to-[#22D3EE]/80 rounded-r-lg transition-all",
                    ),
                    style={"width": f"{data['bar_pct']}%"},
                ),
                rx.el.span(
                    data["count"].to_string() + f" ({data['pct']}...%)",
                    class_name="absolute left-2 top-1/2 -translate-y-1/2 text-xs font-bold text-white z-10",
                ),
                class_name="flex-1 h-8 bg-[#0E0E0E] rounded-lg relative overflow-hidden",
            ),
            class_name="flex items-center gap-4 relative",
        ),
        class_name="mb-4",
    )


def actividad() -> rx.Component:
    tooltip_style_act = {
        "backgroundColor": "#141414",
        "borderColor": "rgba(220,38,38,0.15)",
        "borderRadius": "12px",
        "color": "#ffffff",
        "fontSize": "13px",
        "padding": "10px 14px",
    }
    return layout(
        rx.el.div(
            rx.el.h1(
                "Actividad Semanal", class_name="text-4xl font-bold text-white mb-8"
            ),
            filter_bar(),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Flujo de Negocios por Etapa",
                        class_name="text-lg font-semibold text-white mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(
                            DashboardState.stage_flow_data,
                            lambda d, i: sankey_bar(d, i),
                        )
                    ),
                    class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] p-6 rounded-2xl shadow-xl flex-1",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Actividad por Asesor (Heatmap)",
                        class_name="text-lg font-semibold text-white mb-6",
                    ),
                    rx.recharts.scatter_chart(
                        rx.recharts.cartesian_grid(
                            stroke_dasharray="3 3", stroke="rgba(255,255,255,0.05)"
                        ),
                        rx.recharts.graphing_tooltip(
                            cursor={"strokeDasharray": "3 3"},
                            content_style=tooltip_style_act,
                        ),
                        rx.recharts.x_axis(
                            data_key="month", type_="category", stroke="#6b7280"
                        ),
                        rx.recharts.y_axis(
                            data_key="owner",
                            type_="category",
                            stroke="#6b7280",
                            width=150,
                        ),
                        rx.recharts.z_axis(data_key="z", range=[20, 400]),
                        rx.recharts.scatter(
                            name="Negocios",
                            data=DashboardState.heatmap_data,
                            fill="#DC2626",
                        ),
                        width="100%",
                        height=350,
                        margin={"left": 20, "right": 20, "top": 10, "bottom": 10},
                    ),
                    class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] p-6 rounded-2xl shadow-xl flex-1",
                ),
                class_name="flex flex-col xl:flex-row gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Nuevos Negocios por Semana",
                        class_name="text-lg font-semibold mb-6 text-white",
                    ),
                    rx.el.div(
                        rx.foreach(
                            DashboardState.weekly_new_deals,
                            lambda d: vertical_bar(
                                d, "bg-gradient-to-t from-[#DC2626] to-[#EF4444]"
                            ),
                        ),
                        class_name="flex items-end justify-between gap-2 h-52 px-4",
                    ),
                    class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] p-6 rounded-2xl flex-1 shadow-xl overflow-x-auto",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Propuestas Enviadas por Semana",
                        class_name="text-lg font-semibold mb-6 text-white",
                    ),
                    rx.el.div(
                        rx.foreach(
                            DashboardState.weekly_proposals,
                            lambda d: vertical_bar(
                                d, "bg-gradient-to-t from-[#DC2626] to-[#10B981]"
                            ),
                        ),
                        class_name="flex items-end justify-between gap-2 h-52 px-4",
                    ),
                    class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] p-6 rounded-2xl flex-1 shadow-xl overflow-x-auto",
                ),
                class_name="flex flex-col xl:flex-row gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.h2(
                    "Movimientos de Etapa (Semana Actual)",
                    class_name="text-lg font-semibold mb-6 text-white",
                ),
                rx.el.div(
                    rx.foreach(
                        DashboardState.weekly_stage_movements, stage_movement_card
                    ),
                    class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.h2(
                    "Comparativa Semanal",
                    class_name="text-lg font-semibold mb-6 text-white",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Métrica",
                                    class_name="px-6 py-4 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Semana Actual",
                                    class_name="px-6 py-4 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Semana Anterior",
                                    class_name="px-6 py-4 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Hace 2 Semanas",
                                    class_name="px-6 py-4 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Tendencia",
                                    class_name="px-6 py-4 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                class_name="bg-[#0E0E0E]",
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(DashboardState.weekly_comparison, comparison_row)
                        ),
                        class_name="w-full table-auto",
                    ),
                    class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl shadow-xl overflow-x-auto overflow-hidden",
                ),
                class_name="mb-12",
            ),
            class_name="max-w-7xl mx-auto",
        )
    )