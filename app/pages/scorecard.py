import reflex as rx
from app.states.scorecard_state import ScorecardState
from app.components.layout import layout


def table_header(label: str, col_key: str) -> rx.Component:
    return rx.el.th(
        rx.el.div(
            rx.el.span(label),
            rx.cond(
                ScorecardState.sc_sort_col == col_key,
                rx.cond(
                    ScorecardState.sc_sort_dir == "desc",
                    rx.icon("chevron-down", class_name="h-4 w-4 ml-1"),
                    rx.icon("chevron-up", class_name="h-4 w-4 ml-1"),
                ),
                rx.icon("chevrons-up-down", class_name="h-4 w-4 ml-1 opacity-30"),
            ),
            class_name="flex items-center cursor-pointer hover:text-[#DC2626] transition-colors",
        ),
        on_click=lambda: ScorecardState.sc_set_sort(col_key),
        class_name="px-4 py-4 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider select-none whitespace-nowrap bg-[#0E0E0E]/95 backdrop-blur-md sticky top-0 z-10",
    )


def sc_row(row: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.span(
                row["name"].to(str),
                class_name="block truncate max-w-[150px] cursor-pointer hover:text-[#DC2626] transition-colors",
                on_click=lambda: ScorecardState.sc_select_advisor(row["owner_id"]),
            ),
            class_name="px-4 py-4 whitespace-nowrap text-sm font-medium text-white",
        ),
        rx.el.td(
            row["kwh_activos_fmt"],
            class_name="px-4 py-4 whitespace-nowrap text-sm text-[#9CA3AF]",
        ),
        rx.el.td(
            row["ofertas"].to(str),
            class_name="px-4 py-4 whitespace-nowrap text-sm text-[#22D3EE] font-medium",
        ),
        rx.el.td(
            row["socios_a"].to(str),
            class_name="px-4 py-4 whitespace-nowrap text-sm text-[#9CA3AF]",
        ),
        rx.el.td(
            rx.cond(
                row["alertas"].to(int) > 0,
                rx.el.span(
                    row["alertas"].to(str),
                    class_name="bg-[#EF4444]/20 text-[#EF4444] px-2 py-1 rounded-md font-bold",
                ),
                rx.el.span("0", class_name="text-[#6B7280]"),
            ),
            class_name="px-4 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            row["ciclo"].to(str),
            class_name="px-4 py-4 whitespace-nowrap text-sm text-[#9CA3AF]",
        ),
        rx.el.td(
            row["conversion"].to(str) + "%",
            class_name="px-4 py-4 whitespace-nowrap text-sm text-[#9CA3AF]",
        ),
        rx.el.td(
            row["kwh_firmados_fmt"],
            class_name="px-4 py-4 whitespace-nowrap text-sm font-bold text-white",
        ),
        rx.el.td(
            row["objetivo_fmt"],
            class_name="px-4 py-4 whitespace-nowrap text-sm text-[#6B7280]",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        class_name="h-full rounded-full transition-all",
                        style={
                            "width": rx.cond(
                                row["cumplimiento"].to(float) > 100.0,
                                "100%",
                                row["cumplimiento"].to(str) + "%",
                            ),
                            "backgroundColor": row["color"],
                        },
                    ),
                    class_name="w-16 h-2 bg-white/10 rounded-full mr-2 overflow-hidden",
                ),
                rx.el.span(
                    row["cumplimiento_fmt"],
                    class_name="font-bold",
                    style={"color": row["color"]},
                ),
                class_name="flex items-center",
            ),
            class_name="px-4 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            row["gap_fmt"],
            class_name="px-4 py-4 whitespace-nowrap text-sm text-[#6B7280]",
        ),
        rx.el.td(
            rx.el.div(
                rx.cond(
                    row["tendencia_is_pos"],
                    rx.icon("trending-up", class_name="h-4 w-4 text-[#10B981] mr-1"),
                    rx.icon("trending-down", class_name="h-4 w-4 text-[#EF4444] mr-1"),
                ),
                rx.el.span(
                    row["tendencia_fmt"],
                    class_name=rx.cond(
                        row["tendencia_is_pos"], "text-[#10B981]", "text-[#EF4444]"
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="px-4 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            row["updated"],
            class_name="px-4 py-4 whitespace-nowrap text-xs text-[#6B7280]",
        ),
        class_name="hover:bg-white/5 border-b border-white/5 transition-colors duration-200",
    )


def obs_card(obs: dict) -> rx.Component:
    return rx.el.div(
        rx.el.h4(obs["name"].to(str), class_name="font-bold text-white mb-2"),
        rx.el.ul(
            rx.cond(
                obs["heredados"].to(int) > 0,
                rx.el.li(
                    f"{obs['heredados'].to(str)} negocios heredados",
                    class_name="text-sm text-[#9CA3AF] list-disc ml-4",
                ),
                rx.fragment(),
            ),
            rx.cond(
                obs["rmkts"].to(int) > 0,
                rx.el.li(
                    f"{obs['rmkts'].to(str)} negocios en RMKT",
                    class_name="text-sm text-[#9CA3AF] list-disc ml-4",
                ),
                rx.fragment(),
            ),
            rx.cond(
                obs["sin_prop"].to(int) > 0,
                rx.el.li(
                    f"{obs['sin_prop'].to(str)} negocios sin propuesta",
                    class_name="text-sm text-[#F59E0B] list-disc ml-4",
                ),
                rx.fragment(),
            ),
        ),
        class_name="bg-white/5 backdrop-blur-md border-l-4 border-[#DC2626] p-4 rounded-r-xl shadow-lg",
    )


def scorecard() -> rx.Component:
    return layout(
        rx.el.div(
            rx.cond(
                ScorecardState.sc_show_detail,
                rx.el.div(
                    rx.el.div(
                        class_name="absolute inset-0 bg-[#0A0A0A]/80 backdrop-blur-sm",
                        on_click=ScorecardState.sc_close_detail,
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                "Detalle Asesor",
                                class_name="text-xl font-bold text-white",
                            ),
                            rx.icon(
                                "x",
                                class_name="h-6 w-6 text-[#9CA3AF] cursor-pointer hover:text-white transition-colors",
                                on_click=ScorecardState.sc_close_detail,
                            ),
                            class_name="flex justify-between items-center mb-6",
                        ),
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Negocio",
                                        class_name="text-left text-xs font-bold text-[#9CA3AF] p-2",
                                    ),
                                    rx.el.th(
                                        "Heredado",
                                        class_name="text-left text-xs font-bold text-[#9CA3AF] p-2",
                                    ),
                                    rx.el.th(
                                        "RMKT",
                                        class_name="text-left text-xs font-bold text-[#9CA3AF] p-2",
                                    ),
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    ScorecardState.sc_detail_deals,
                                    lambda d: rx.el.tr(
                                        rx.el.td(
                                            d["dealname"].to(str),
                                            class_name="p-2 text-sm text-white",
                                        ),
                                        rx.el.td(
                                            d["heredado"].to(str),
                                            class_name="p-2 text-sm text-[#9CA3AF]",
                                        ),
                                        rx.el.td(
                                            d["rmkt"].to(str),
                                            class_name="p-2 text-sm text-[#9CA3AF]",
                                        ),
                                        on_click=lambda: ScorecardState.open_deal_detail(
                                            d["dealname"]
                                        ),
                                        class_name="border-b border-white/5 hover:bg-white/10 cursor-pointer transition-colors",
                                    ),
                                )
                            ),
                        ),
                        class_name="relative bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl shadow-2xl p-6 w-full max-w-3xl z-10 max-h-[80vh] overflow-y-auto",
                    ),
                    class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
                ),
                rx.fragment(),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Scorecard Mensual por Asesor",
                        class_name="text-4xl font-bold text-white mr-4",
                    ),
                    rx.el.span(
                        ScorecardState.sc_month_label,
                        class_name="bg-white/10 px-3 py-1 rounded-full text-sm font-bold text-white",
                    ),
                    class_name="flex items-center mb-6",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.foreach(
                            ScorecardState.sc_month_options,
                            lambda opt: rx.el.option(
                                opt[1], value=opt[0], class_name="bg-[#0A0A0A]"
                            ),
                        ),
                        value=ScorecardState.sc_month.to(str),
                        on_change=ScorecardState.sc_set_month,
                        class_name="appearance-none bg-white/5 border border-white/10 text-white rounded-xl px-4 py-2 focus:outline-none focus:border-[#DC2626] transition-all",
                    ),
                    rx.el.select(
                        rx.foreach(
                            ScorecardState.sc_year_options,
                            lambda opt: rx.el.option(
                                opt[1], value=opt[0], class_name="bg-[#0A0A0A]"
                            ),
                        ),
                        value=ScorecardState.sc_year.to(str),
                        on_change=ScorecardState.sc_set_year,
                        class_name="appearance-none bg-white/5 border border-white/10 text-white rounded-xl px-4 py-2 focus:outline-none focus:border-[#DC2626] transition-all",
                    ),
                    rx.el.select(
                        rx.foreach(
                            ScorecardState.sc_owner_options,
                            lambda opt: rx.el.option(
                                opt[1], value=opt[0], class_name="bg-[#0A0A0A]"
                            ),
                        ),
                        value=ScorecardState.sc_owner_filter,
                        on_change=ScorecardState.sc_set_owner,
                        class_name="appearance-none bg-white/5 border border-white/10 text-white rounded-xl px-4 py-2 focus:outline-none focus:border-[#DC2626] transition-all",
                    ),
                    rx.el.button(
                        rx.icon("download", class_name="h-4 w-4 mr-2"),
                        "Exportar CSV",
                        on_click=ScorecardState.download_csv,
                        class_name="flex items-center bg-[#DC2626] hover:bg-[#DC2626]/80 text-white px-4 py-2 rounded-xl font-bold transition-all",
                    ),
                    class_name="flex gap-4 items-center bg-white/5 p-4 rounded-2xl border border-white/10 w-fit",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                table_header("Asesor", "name"),
                                table_header("kWh Activos", "kwh_activos"),
                                table_header("Ofertas", "ofertas"),
                                table_header("Socios A", "socios_a"),
                                table_header("Alertas", "alertas"),
                                table_header("Ciclo", "ciclo"),
                                table_header("Conversión", "conversion"),
                                table_header("kWh Firmados", "kwh_firmados"),
                                table_header("Objetivo", "objetivo"),
                                table_header("% Cump.", "cumplimiento"),
                                table_header("Gap", "gap"),
                                table_header("Tendencia", "tendencia"),
                                table_header("Actualización", "updated"),
                            )
                        ),
                        rx.el.tbody(rx.foreach(ScorecardState.scorecard_data, sc_row)),
                        class_name="w-full table-auto",
                    ),
                    class_name="overflow-x-auto max-h-[600px] overflow-y-auto",
                ),
                class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl shadow-2xl mb-8",
            ),
            rx.el.div(
                rx.el.h3(
                    "Observaciones", class_name="text-xl font-bold text-white mb-4"
                ),
                rx.el.div(
                    rx.foreach(ScorecardState.sc_observations, obs_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
                ),
            ),
            class_name="max-w-[1600px] mx-auto pb-12",
        )
    )