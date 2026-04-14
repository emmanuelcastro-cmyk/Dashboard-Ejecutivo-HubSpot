import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.layout import layout
from app.pages.resumen import filter_bar


def table_header(label: str, col_key: str) -> rx.Component:
    return rx.el.th(
        rx.el.div(
            rx.el.span(label),
            rx.cond(
                DashboardState.sort_column == col_key,
                rx.cond(
                    DashboardState.sort_direction == "desc",
                    rx.icon("chevron-down", class_name="h-4 w-4 ml-1 text-[#DC2626]"),
                    rx.icon("chevron-up", class_name="h-4 w-4 ml-1 text-[#DC2626]"),
                ),
                rx.icon("chevrons-up-down", class_name="h-4 w-4 ml-1 opacity-20"),
            ),
            class_name=rx.cond(
                DashboardState.sort_column == col_key,
                "flex items-center cursor-pointer text-white transition-colors",
                "flex items-center cursor-pointer hover:text-white transition-colors",
            ),
        ),
        on_click=lambda: DashboardState.set_sort(col_key),
        class_name="px-6 py-4 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider select-none",
    )


def table_row(advisor: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.span(
                advisor["name"].to(str),
                class_name="block truncate max-w-[200px]",
                title=advisor["name"].to(str),
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-white",
        ),
        rx.el.td(
            advisor["total"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-[#9CA3AF]",
        ),
        rx.el.td(
            advisor["active"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-[#22D3EE] font-medium",
        ),
        rx.el.td(
            advisor["convenio"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-[#10B981] font-medium",
        ),
        rx.el.td(
            advisor["perdidos"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-[#EF4444] font-medium",
        ),
        rx.el.td(
            advisor["kwh_fmt"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-[#9CA3AF]",
        ),
        rx.el.td(
            advisor["usd_fmt"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-[#9CA3AF]",
        ),
        on_click=lambda: DashboardState.select_advisor(advisor["owner_id"]),
        class_name="hover:bg-[#1A1A1A] cursor-pointer border-b border-white/5 transition-colors duration-200",
    )


def ranking_row(advisor: dict, index: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(f"#{index + 1}", class_name="font-bold w-8 text-[#6B7280]"),
            rx.el.span(
                advisor["name"].to(str),
                class_name="text-sm font-medium text-white truncate flex-1",
            ),
            rx.el.span(
                advisor["usd_fmt"].to(str),
                class_name="text-sm font-bold text-[#10B981] text-right",
            ),
            class_name="flex items-center gap-3 py-3 border-b border-white/5 last:border-0",
        )
    )


def ranking_row_kwh(advisor: dict, index: int, key: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(f"#{index + 1}", class_name="font-bold w-8 text-[#6B7280]"),
            rx.el.span(
                advisor["name"],
                class_name="text-sm font-medium text-white truncate flex-1",
            ),
            rx.el.span(
                advisor[key].to(str),
                class_name=f"text-sm font-bold text-[{color}] text-right",
            ),
            class_name="flex items-center gap-3 py-3 border-b border-white/5 last:border-0",
        )
    )


def modal_row(deal: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            deal["dealname"].to(str),
            class_name="px-4 py-3 text-sm text-white truncate max-w-[200px]",
        ),
        rx.el.td(deal["stage"].to(str), class_name="px-4 py-3 text-xs text-gray-300"),
        rx.el.td(deal["amount"].to(str), class_name="px-4 py-3 text-sm text-[#00ff88]"),
        rx.el.td(deal["kwh"].to(str), class_name="px-4 py-3 text-sm text-[#00d4ff]"),
        rx.el.td(deal["created"].to(str), class_name="px-4 py-3 text-xs text-gray-500"),
        on_click=lambda: DashboardState.open_deal_detail(deal["dealname"].to(str)),
        class_name="border-b border-white/5 hover:bg-white/10 cursor-pointer transition-colors duration-200",
    )


def advisor_modal() -> rx.Component:
    return rx.cond(
        DashboardState.show_advisor_modal,
        rx.el.div(
            rx.el.div(
                class_name="absolute inset-0 bg-[#0A0A0A]/70 backdrop-blur-sm",
                on_click=DashboardState.close_modal,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Detalle de Negocios", class_name="text-xl font-bold text-white"
                    ),
                    rx.icon(
                        "x",
                        class_name="h-5 w-5 text-[#9CA3AF] cursor-pointer hover:text-white transition-colors",
                        on_click=DashboardState.close_modal,
                    ),
                    class_name="flex justify-between items-center mb-8 px-2",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Negocio",
                                    class_name="px-4 py-3 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Etapa",
                                    class_name="px-4 py-3 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Monto",
                                    class_name="px-4 py-3 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "kWh",
                                    class_name="px-4 py-3 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Creado",
                                    class_name="px-4 py-3 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                class_name="bg-[#0E0E0E]",
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(DashboardState.selected_advisor_deals, modal_row)
                        ),
                        class_name="w-full table-auto",
                    ),
                    class_name="overflow-y-auto max-h-[60vh] rounded-xl overflow-hidden",
                ),
                class_name="relative bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl shadow-2xl p-8 w-full max-w-5xl z-10",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
        ),
        rx.fragment(),
    )


def equipo() -> rx.Component:
    return layout(
        rx.el.div(
            advisor_modal(),
            rx.el.h1(
                "Equipo Comercial", class_name="text-4xl font-bold text-white mb-8"
            ),
            filter_bar(),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    table_header("Asesor", "name"),
                                    table_header("Total", "total"),
                                    table_header("Activos", "active"),
                                    table_header("Firmado", "convenio"),
                                    table_header("Perdidos", "perdidos"),
                                    table_header("kWh Total", "kwh"),
                                    table_header("USD Total", "usd"),
                                    class_name="bg-[#0E0E0E]",
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(DashboardState.advisor_stats, table_row)
                            ),
                            class_name="w-full table-auto",
                        ),
                        class_name="overflow-x-auto",
                    ),
                    class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl flex-[3] shadow-xl overflow-hidden",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Top Asesores (USD)",
                            class_name="text-lg font-bold mb-4 text-white",
                        ),
                        rx.el.div(
                            rx.foreach(
                                DashboardState.advisor_ranking,
                                lambda adv, i: ranking_row(adv, i),
                            ),
                            class_name="flex flex-col",
                        ),
                        class_name="mb-6 bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6 shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Top Asesores (kWh Activos)",
                            class_name="text-lg font-bold mb-4 text-white",
                        ),
                        rx.el.div(
                            rx.foreach(
                                DashboardState.advisor_ranking,
                                lambda adv, i: ranking_row_kwh(
                                    adv, i, "kwh_activos", "#22D3EE"
                                ),
                            ),
                            class_name="flex flex-col",
                        ),
                        class_name="mb-6 bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6 shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Top Asesores (kWh Cerrados)",
                            class_name="text-lg font-bold mb-4 text-white",
                        ),
                        rx.el.div(
                            rx.foreach(
                                DashboardState.advisor_ranking,
                                lambda adv, i: ranking_row_kwh(
                                    adv, i, "kwh_cerrados", "#10B981"
                                ),
                            ),
                            class_name="flex flex-col",
                        ),
                        class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6 shadow-sm",
                    ),
                    class_name="flex-1 h-fit flex flex-col gap-1",
                ),
                class_name="flex flex-col xl:flex-row gap-6 mb-6",
            ),
            rx.el.div(
                rx.el.h2(
                    "Análisis Multidimensional (Top 5)",
                    class_name="text-lg font-bold text-white mb-8 text-center",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(class_name="w-3 h-3 rounded-full bg-[#1F659D]"),
                        rx.el.span(
                            DashboardState.radar_name_0,
                            class_name="text-xs font-medium text-[#9CA3AF]",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.div(
                        rx.el.div(class_name="w-3 h-3 rounded-full bg-[#10B981]"),
                        rx.el.span(
                            DashboardState.radar_name_1,
                            class_name="text-xs font-medium text-[#9CA3AF]",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.div(
                        rx.el.div(class_name="w-3 h-3 rounded-full bg-[#ffb703]"),
                        rx.el.span(
                            DashboardState.radar_name_2,
                            class_name="text-xs font-medium text-[#9CA3AF]",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.div(
                        rx.el.div(class_name="w-3 h-3 rounded-full bg-[#EF4444]"),
                        rx.el.span(
                            DashboardState.radar_name_3,
                            class_name="text-xs font-medium text-[#9CA3AF]",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.div(
                        rx.el.div(class_name="w-3 h-3 rounded-full bg-[#a78bfa]"),
                        rx.el.span(
                            DashboardState.radar_name_4,
                            class_name="text-xs font-medium text-[#9CA3AF]",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    class_name="flex flex-wrap justify-center gap-6 mb-8",
                ),
                rx.recharts.radar_chart(
                    rx.recharts.polar_grid(stroke="rgba(255,255,255,0.05)"),
                    rx.recharts.polar_angle_axis(
                        data_key="subject", stroke="#6b7280", font_size=10
                    ),
                    rx.recharts.polar_radius_axis(
                        angle=90, domain=[0, 100], stroke="#6b7280", font_size=10
                    ),
                    rx.cond(
                        DashboardState.radar_name_0 != "",
                        rx.recharts.radar(
                            data_key=DashboardState.radar_name_0,
                            stroke="#1F659D",
                            fill="#1F659D",
                            fill_opacity=0.15,
                            name=DashboardState.radar_name_0,
                        ),
                        rx.fragment(),
                    ),
                    rx.cond(
                        DashboardState.radar_name_1 != "",
                        rx.recharts.radar(
                            data_key=DashboardState.radar_name_1,
                            stroke="#10B981",
                            fill="#10B981",
                            fill_opacity=0.15,
                            name=DashboardState.radar_name_1,
                        ),
                        rx.fragment(),
                    ),
                    rx.cond(
                        DashboardState.radar_name_2 != "",
                        rx.recharts.radar(
                            data_key=DashboardState.radar_name_2,
                            stroke="#ffb703",
                            fill="#ffb703",
                            fill_opacity=0.15,
                            name=DashboardState.radar_name_2,
                        ),
                        rx.fragment(),
                    ),
                    rx.cond(
                        DashboardState.radar_name_3 != "",
                        rx.recharts.radar(
                            data_key=DashboardState.radar_name_3,
                            stroke="#EF4444",
                            fill="#EF4444",
                            fill_opacity=0.15,
                            name=DashboardState.radar_name_3,
                        ),
                        rx.fragment(),
                    ),
                    rx.cond(
                        DashboardState.radar_name_4 != "",
                        rx.recharts.radar(
                            data_key=DashboardState.radar_name_4,
                            stroke="#a78bfa",
                            fill="#a78bfa",
                            fill_opacity=0.15,
                            name=DashboardState.radar_name_4,
                        ),
                        rx.fragment(),
                    ),
                    rx.recharts.tooltip(cursor=False),
                    data=DashboardState.radar_chart_data,
                    width="100%",
                    height=400,
                ),
                class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl shadow-xl p-8 mb-12",
            ),
            class_name="max-w-7xl mx-auto",
        )
    )