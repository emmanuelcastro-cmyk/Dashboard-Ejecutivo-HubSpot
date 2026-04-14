import reflex as rx
from app.states.report_state import ReportState
from app.components.layout import layout


def report_card(report_id: str, title: str, icon: str, desc: str) -> rx.Component:
    return rx.el.div(
        rx.icon(
            icon,
            class_name=rx.cond(
                ReportState.report_type == report_id,
                "h-8 w-8 text-[#DC2626] mb-4",
                "h-8 w-8 text-[#9CA3AF] mb-4",
            ),
        ),
        rx.el.h3(title, class_name="text-lg font-bold text-white mb-2"),
        rx.el.p(desc, class_name="text-sm text-[#9CA3AF]"),
        on_click=lambda: ReportState.set_report_type(report_id),
        class_name=rx.cond(
            ReportState.report_type == report_id,
            "cursor-pointer p-6 rounded-2xl border border-[#DC2626] bg-[rgba(220,38,38,0.08)] shadow-[0_0_20px_rgba(220,38,38,0.15)] transition-all",
            "cursor-pointer p-6 rounded-2xl border border-[rgba(255,255,255,0.06)] bg-[#141414] hover:border-[rgba(220,38,38,0.2)] transition-all",
        ),
    )


def comparison_metric_card(
    title: str,
    current: rx.Var,
    delta: rx.Var,
    growth: rx.Var,
    prev: rx.Var,
    icon: str,
    color: str,
) -> rx.Component:
    is_negative = delta.to(str).contains("-")
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                title, class_name="text-[10px] text-[#6B7280] uppercase tracking-wider"
            ),
            rx.icon(icon, class_name="h-4 w-4", style={"color": color}),
            class_name="flex justify-between items-center mb-2",
        ),
        rx.el.h3(current.to(str), class_name="text-lg font-bold text-white"),
        rx.el.div(
            rx.el.p("Prev: " + prev.to(str), class_name="text-sm text-[#6B7280]"),
            rx.el.div(
                rx.cond(
                    is_negative,
                    rx.icon("trending-down", class_name="h-3 w-3 text-[#EF4444]"),
                    rx.icon("trending-up", class_name="h-3 w-3 text-[#10B981]"),
                ),
                rx.el.span(
                    delta.to(str),
                    class_name=rx.cond(
                        is_negative,
                        "text-sm font-bold text-[#EF4444]",
                        "text-sm font-bold text-[#10B981]",
                    ),
                ),
                rx.el.div(
                    growth.to(str),
                    class_name=rx.cond(
                        is_negative,
                        "px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#EF4444]/20 text-[#EF4444]",
                        "px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#10B981]/20 text-[#10B981]",
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex justify-between items-center mt-2",
        ),
        class_name="bg-[#0E0E0E] border border-white/5 rounded-xl p-4 shadow-sm hover:border-[rgba(220,38,38,0.2)] transition-all",
    )


def date_filter_bar() -> rx.Component:
    presets = [
        ("Todo", "all"),
        ("Hoy", "today"),
        ("7D", "7d"),
        ("Semana", "this_week"),
        ("Sem. Ant.", "last_week"),
        ("Mes", "this_month"),
        ("Mes Ant.", "last_month"),
        ("Quarter", "this_quarter"),
        ("Q Ant.", "last_quarter"),
        ("6M", "6m"),
        ("YTD", "ytd"),
        ("12M", "12m"),
        ("Año", "this_year"),
        ("Año Ant.", "last_year"),
        ("Custom", "custom"),
    ]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("calendar", class_name="h-4 w-4"),
                    rx.el.span(
                        ReportState.active_date_label, class_name="text-sm font-bold"
                    ),
                    class_name="bg-[#DC2626]/20 text-[#DC2626] px-3 py-1.5 rounded-full flex items-center gap-2",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option(
                            "Fecha de creación",
                            value="createdate",
                            class_name="bg-[#0E0E0E]",
                        ),
                        rx.el.option(
                            "Fecha de cierre",
                            value="closedate",
                            class_name="bg-[#0E0E0E]",
                        ),
                        rx.el.option(
                            "Fecha 1er cierre",
                            value="fecha_de_1er_cierre",
                            class_name="bg-[#0E0E0E]",
                        ),
                        rx.el.option(
                            "Última actividad",
                            value="hs_lastmodifieddate",
                            class_name="bg-[#0E0E0E]",
                        ),
                        value=ReportState.date_field,
                        on_change=ReportState.set_date_field,
                        class_name="bg-[#0E0E0E] text-white border border-white/10 rounded-xl px-3 py-1.5 text-xs appearance-none",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="absolute right-2 top-1/2 -translate-y-1/2 h-3 w-3 text-[#9CA3AF] pointer-events-none",
                    ),
                    class_name="relative",
                ),
                class_name="flex items-center gap-4",
            ),
            rx.el.div(
                rx.el.span("Comparar", class_name="text-xs text-[#9CA3AF]"),
                rx.el.button(
                    rx.el.div(
                        class_name=rx.cond(
                            ReportState.compare_enabled,
                            "h-4 w-4 bg-[#DC2626] rounded-full translate-x-5 transition-transform duration-200",
                            "h-4 w-4 bg-[#374151] rounded-full translate-x-0 transition-transform duration-200",
                        )
                    ),
                    on_click=lambda: ReportState.toggle_compare(
                        ~ReportState.compare_enabled
                    ),
                    class_name="w-10 h-5 rounded-full bg-white/5 border border-white/10 flex items-center p-0.5",
                ),
                rx.cond(
                    ReportState.compare_enabled,
                    rx.el.div(
                        rx.el.button(
                            "vs Anterior",
                            on_click=lambda: ReportState.set_compare_mode("previous"),
                            class_name=rx.cond(
                                ReportState.compare_mode == "previous",
                                "bg-[#DC2626] text-white px-2 py-1 rounded-lg text-[10px] font-bold",
                                "text-[#9CA3AF] px-2 py-1 rounded-lg text-[10px] font-bold hover:bg-white/5",
                            ),
                        ),
                        rx.el.button(
                            "vs Año Pasado",
                            on_click=lambda: ReportState.set_compare_mode("yoy"),
                            class_name=rx.cond(
                                ReportState.compare_mode == "yoy",
                                "bg-[#DC2626] text-white px-2 py-1 rounded-lg text-[10px] font-bold",
                                "text-[#9CA3AF] px-2 py-1 rounded-lg text-[10px] font-bold hover:bg-white/5",
                            ),
                        ),
                        class_name="flex bg-[#0E0E0E] rounded-xl border border-white/10 p-1 gap-1 animate-in fade-in slide-in-from-right-2 duration-300",
                    ),
                    rx.fragment(),
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    presets,
                    lambda p: rx.el.button(
                        p[0],
                        on_click=lambda: ReportState.set_date_preset(p[1]),
                        class_name=rx.cond(
                            ReportState.date_preset == p[1],
                            "whitespace-nowrap bg-[#DC2626] text-white rounded-full px-4 py-1.5 text-xs font-bold shadow-[0_0_15px_rgba(220,38,38,0.3)] transition-all shrink-0",
                            "whitespace-nowrap bg-white/5 text-[#9CA3AF] hover:bg-white/10 hover:text-white rounded-full px-4 py-1.5 text-xs font-medium transition-all shrink-0",
                        ),
                    ),
                ),
                class_name="flex gap-2 overflow-x-auto pb-2 scrollbar-hide",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Desde", class_name="text-[10px] text-[#6B7280] uppercase mb-1"
                    ),
                    rx.el.input(
                        type="date",
                        on_change=ReportState.set_custom_start,
                        default_value=ReportState.custom_start,
                        class_name="bg-[#0E0E0E] border border-white/10 text-white rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-[#DC2626]",
                    ),
                    class_name="flex flex-col flex-1",
                ),
                rx.el.div(
                    rx.el.label(
                        "Hasta", class_name="text-[10px] text-[#6B7280] uppercase mb-1"
                    ),
                    rx.el.input(
                        type="date",
                        on_change=ReportState.set_custom_end,
                        default_value=ReportState.custom_end,
                        class_name="bg-[#0E0E0E] border border-white/10 text-white rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-[#DC2626]",
                    ),
                    class_name="flex flex-col flex-1",
                ),
                class_name="flex gap-4 w-full max-w-lg",
            ),
            class_name="mb-6 bg-[#0E0E0E]/50 p-4 rounded-2xl border border-white/5",
        ),
        rx.cond(
            ReportState.compare_enabled & ReportState.report_generated,
            rx.el.div(
                comparison_metric_card(
                    "Negocios",
                    ReportState.comparison_stats["current_deals"],
                    ReportState.comparison_stats["deals_delta"],
                    ReportState.comparison_stats["deals_growth_pct"],
                    ReportState.comparison_stats["previous_deals"],
                    "briefcase",
                    "#DC2626",
                ),
                comparison_metric_card(
                    "kWh Agregados",
                    ReportState.comparison_stats["current_kwh"],
                    ReportState.comparison_stats["kwh_delta"],
                    ReportState.comparison_stats["kwh_growth_pct"],
                    ReportState.comparison_stats["previous_kwh"],
                    "zap",
                    "#F59E0B",
                ),
                comparison_metric_card(
                    "Valor USD",
                    ReportState.comparison_stats["current_usd"],
                    ReportState.comparison_stats["usd_delta"],
                    ReportState.comparison_stats["usd_growth_pct"],
                    ReportState.comparison_stats["previous_usd"],
                    "dollar-sign",
                    "#10B981",
                ),
                comparison_metric_card(
                    "Convenios",
                    ReportState.comparison_stats["current_won"],
                    ReportState.comparison_stats["won_delta"],
                    ReportState.comparison_stats["won_growth_pct"],
                    ReportState.comparison_stats["previous_won"],
                    "message_circle_check",
                    "#10B981",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 animate-in slide-in-from-bottom-2 duration-500",
            ),
            rx.fragment(),
        ),
        class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6 mb-8",
    )


def action_bar() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.cond(
                ReportState.report_generating,
                rx.icon("loader", class_name="h-5 w-5 mr-2 animate-spin"),
                rx.icon("play", class_name="h-5 w-5 mr-2"),
            ),
            "Generar Reporte",
            on_click=ReportState.generate_report,
            disabled=ReportState.report_generating,
            class_name="flex items-center bg-[#DC2626] hover:bg-[#DC2626]/80 text-white rounded-xl font-bold px-6 py-3 transition-all",
        ),
        rx.el.button(
            rx.icon("file-text", class_name="h-5 w-5 mr-2"),
            "Exportar CSV",
            on_click=ReportState.export_csv,
            class_name="flex items-center bg-transparent border border-[rgba(220,38,38,0.3)] text-[#DC2626] hover:bg-[rgba(220,38,38,0.08)] rounded-xl font-bold px-6 py-3 transition-all",
        ),
        rx.el.button(
            rx.icon("table-2", class_name="h-5 w-5 mr-2"),
            "Exportar Excel",
            on_click=ReportState.export_excel,
            class_name="flex items-center bg-transparent border border-[rgba(220,38,38,0.3)] text-[#DC2626] hover:bg-[rgba(220,38,38,0.08)] rounded-xl font-bold px-6 py-3 transition-all",
        ),
        rx.el.button(
            rx.icon("mail", class_name="h-5 w-5 mr-2"),
            "Enviar por Correo",
            on_click=rx.toast("Próximamente", duration=3000),
            class_name="flex items-center bg-transparent border border-[rgba(220,38,38,0.3)] text-[#DC2626] hover:bg-[rgba(220,38,38,0.08)] rounded-xl font-bold px-6 py-3 transition-all",
        ),
        rx.el.button(
            rx.icon("link", class_name="h-5 w-5 mr-2"),
            "Compartir Link",
            on_click=rx.toast("Próximamente", duration=3000),
            class_name="flex items-center bg-transparent border border-[rgba(220,38,38,0.3)] text-[#DC2626] hover:bg-[rgba(220,38,38,0.08)] rounded-xl font-bold px-6 py-3 transition-all",
        ),
        class_name="flex flex-wrap gap-4 items-center",
    )


def report_kpi_card(
    title: str, value: rx.Var, icon: str, color: str = "#DC2626"
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-6 w-6", style={"color": color}),
                class_name="p-3 rounded-xl mb-4 w-fit",
                style={"backgroundColor": rx.cond(True, f"{color}1a", "")},
            ),
            rx.el.h3(
                value.to(str),
                class_name="text-2xl font-bold text-white mb-1 truncate",
                title=value.to(str),
            ),
            rx.el.p(
                title,
                class_name="text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
            ),
            class_name="flex flex-col flex-1 p-5",
        ),
        class_name="bg-[#0E0E0E] border border-white/5 rounded-xl shadow-sm hover:border-[rgba(220,38,38,0.2)] transition-all duration-300",
    )


def intelligence_card(insight: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                insight["icon"].to(str),
                class_name="h-6 w-6",
                style={"color": insight["color"].to(str)},
            ),
            rx.el.span(
                insight["severity"].to(str),
                class_name="px-2 py-0.5 rounded-full text-[10px] font-bold bg-white/10 uppercase",
                style={"color": insight["color"].to(str)},
            ),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.h4(
            insight["title"].to(str), class_name="text-base font-bold text-white mb-2"
        ),
        rx.el.p(insight["description"].to(str), class_name="text-sm text-[#9CA3AF]"),
        class_name="bg-[#141414] border-l-4 p-5 rounded-r-xl shadow-md",
        style={"borderLeftColor": insight["color"].to(str)},
    )


def executive_preview() -> rx.Component:
    data = ReportState.executive_report_data
    return rx.el.div(
        rx.el.div(
            report_kpi_card("Total Negocios", data["total_deals"].to(str), "briefcase"),
            report_kpi_card(
                "Activos", data["active_deals"].to(str), "activity", "#22D3EE"
            ),
            report_kpi_card(
                "Convenio Firmado",
                data["convenio_firmado"].to(str),
                "message_circle_check",
                "#10B981",
            ),
            report_kpi_card(
                "Cerrados Perdidos",
                data["cerrados_perdidos"].to(str),
                "message_circle_x",
                "#EF4444",
            ),
            report_kpi_card(
                "Valor USD", data["total_usd"].to(str), "dollar-sign", "#10B981"
            ),
            report_kpi_card("kWh Total", data["total_kwh"].to(str), "zap", "#F59E0B"),
            report_kpi_card(
                "kWh Cerrados",
                data["kwh_cerrados"].to(str),
                "battery-charging",
                "#10B981",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        data["overall_pct_q"].to(str) + "%",
                        class_name="text-2xl font-bold text-[#10B981]",
                    ),
                    rx.el.p(
                        "Cumplimiento Q",
                        class_name="text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                    ),
                    class_name="flex flex-col items-center justify-center h-full p-5 text-center",
                ),
                class_name="bg-[#0E0E0E] border border-white/5 rounded-xl shadow-sm hover:border-[rgba(220,38,38,0.2)] transition-all duration-300",
            ),
            class_name="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Top Asesores", class_name="text-lg font-bold text-white mb-4"
                ),
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "#",
                                class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                            ),
                            rx.el.th(
                                "Nombre",
                                class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                            ),
                            rx.el.th(
                                "Deals",
                                class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                            ),
                            rx.el.th(
                                "USD",
                                class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                            ),
                            rx.el.th(
                                "kWh",
                                class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                            ),
                        ),
                        class_name="bg-[#0E0E0E]",
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            data["top_advisors"].to(list[dict[str, str | int]]),
                            lambda adv: rx.el.tr(
                                rx.el.td(
                                    adv["rank"].to_string(),
                                    class_name="p-2 text-sm text-[#6B7280]",
                                ),
                                rx.el.td(
                                    adv["name"].to(str),
                                    class_name="p-2 text-sm text-white font-medium",
                                ),
                                rx.el.td(
                                    adv["total"].to_string(),
                                    class_name="p-2 text-sm text-[#9CA3AF]",
                                ),
                                rx.el.td(
                                    adv["usd_fmt"].to(str),
                                    class_name="p-2 text-sm text-[#10B981]",
                                ),
                                rx.el.td(
                                    adv["kwh_fmt"].to(str),
                                    class_name="p-2 text-sm text-[#22D3EE]",
                                ),
                                class_name="border-b border-white/5",
                            ),
                        )
                    ),
                    class_name="w-full",
                ),
                class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6 flex-[2]",
            ),
            rx.el.div(
                rx.el.h3(
                    "Forecast Summary", class_name="text-lg font-bold text-white mb-4"
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "Projected kWh", class_name="text-sm text-[#9CA3AF]"
                        ),
                        rx.el.span(
                            data["forecast_summary"].to(dict)["projected"].to(str),
                            class_name="text-2xl font-bold text-white",
                        ),
                        class_name="flex flex-col mb-4",
                    ),
                    rx.cond(
                        data["forecast_summary"].to(dict)["will_meet"].to(bool),
                        rx.el.div(
                            rx.icon(
                                "message_circle_check",
                                class_name="h-5 w-5 text-[#10B981] mr-2",
                            ),
                            rx.el.span(
                                "On Track for Target",
                                class_name="text-sm font-bold text-[#10B981]",
                            ),
                            class_name="flex items-center bg-[#10B981]/10 px-3 py-2 rounded-lg",
                        ),
                        rx.el.div(
                            rx.icon(
                                "circle_alert", class_name="h-5 w-5 text-[#EF4444] mr-2"
                            ),
                            rx.el.span(
                                "At Risk for Target",
                                class_name="text-sm font-bold text-[#EF4444]",
                            ),
                            class_name="flex items-center bg-[#EF4444]/10 px-3 py-2 rounded-lg",
                        ),
                    ),
                    class_name="bg-[#0E0E0E] p-4 rounded-xl border border-white/5 h-[calc(100%-3rem)]",
                ),
                class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6 flex-1",
            ),
            class_name="flex flex-col lg:flex-row gap-6 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Riesgos Detectados",
                    class_name="text-lg font-bold text-white mb-4 flex items-center",
                ),
                rx.el.ul(
                    rx.foreach(
                        data["risks"].to(list[dict[str, str]]),
                        lambda r: rx.el.li(
                            rx.icon(
                                "triangle_alert",
                                class_name="h-4 w-4 text-[#F59E0B] mr-2 shrink-0 mt-0.5",
                            ),
                            rx.el.span(
                                r["description"].to(str),
                                class_name="text-sm text-[#9CA3AF]",
                            ),
                            class_name="flex items-start mb-3",
                        ),
                    )
                ),
                class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6 flex-1",
            ),
            rx.el.div(
                rx.el.h3(
                    "Insights",
                    class_name="text-lg font-bold text-white mb-4 flex items-center",
                ),
                rx.el.ul(
                    rx.foreach(
                        data["insights"].to(list[dict[str, str]]),
                        lambda i: rx.el.li(
                            rx.icon(
                                "lightbulb",
                                class_name="h-4 w-4 text-[#22D3EE] mr-2 shrink-0 mt-0.5",
                            ),
                            rx.el.span(
                                i["description"].to(str),
                                class_name="text-sm text-[#9CA3AF]",
                            ),
                            class_name="flex items-start mb-3",
                        ),
                    )
                ),
                class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6 flex-1",
            ),
            class_name="flex flex-col lg:flex-row gap-6",
        ),
    )


def pipeline_preview() -> rx.Component:
    data = ReportState.pipeline_report_data
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Ventas Funnel", class_name="text-lg font-bold text-white mb-4"),
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Etapa",
                            class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                        ),
                        rx.el.th(
                            "Deals",
                            class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                        ),
                        rx.el.th(
                            "%",
                            class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2 w-1/3",
                        ),
                    ),
                    class_name="bg-[#0E0E0E]",
                ),
                rx.el.tbody(
                    rx.foreach(
                        data["ventas_stages"].to(list[dict[str, str | int]]),
                        lambda st: rx.el.tr(
                            rx.el.td(
                                st["stage_name"].to(str),
                                class_name="p-2 text-sm text-white",
                            ),
                            rx.el.td(
                                st["count"].to(str),
                                class_name="p-2 text-sm text-[#9CA3AF]",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.div(
                                        class_name="h-1.5 bg-[#22D3EE] rounded-full",
                                        style={"width": st["percentage"].to(str)},
                                    ),
                                    rx.el.span(
                                        st["percentage"].to(str),
                                        class_name="text-xs text-[#6B7280] ml-2",
                                    ),
                                    class_name="flex items-center",
                                ),
                                class_name="p-2",
                            ),
                            class_name="border-b border-white/5",
                        ),
                    )
                ),
                class_name="w-full",
            ),
            class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6 mb-6",
        ),
        rx.el.div(
            rx.el.h3(
                "Stale Deals (>30 días sin cambio)",
                class_name="text-lg font-bold text-[#EF4444] mb-4 flex items-center",
            ),
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Negocio",
                            class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                        ),
                        rx.el.th(
                            "Propietario",
                            class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                        ),
                        rx.el.th(
                            "Días",
                            class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                        ),
                        rx.el.th(
                            "Etapa",
                            class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                        ),
                    ),
                    class_name="bg-[#0E0E0E]",
                ),
                rx.el.tbody(
                    rx.foreach(
                        data["stale_deals"].to(list[dict[str, str | int]]),
                        lambda st: rx.el.tr(
                            rx.el.td(
                                st["dealname"].to(str),
                                class_name="p-2 text-sm text-white",
                            ),
                            rx.el.td(
                                st["owner"].to(str),
                                class_name="p-2 text-sm text-[#9CA3AF]",
                            ),
                            rx.el.td(
                                st["days_stale"].to(str),
                                class_name="p-2 text-sm font-bold text-[#F59E0B]",
                            ),
                            rx.el.td(
                                st["stage"].to(str),
                                class_name="p-2 text-xs text-[#6B7280]",
                            ),
                            class_name="border-b border-white/5",
                        ),
                    )
                ),
                class_name="w-full",
            ),
            class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6",
        ),
    )


def advisor_preview() -> rx.Component:
    data = ReportState.advisor_report_data
    return rx.el.div(
        rx.el.h3("Scorecard Resumen", class_name="text-lg font-bold text-white mb-4"),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Asesor",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "kWh Cerrados",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "Objetivo",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "% Cumplimiento",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "Gap",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "Ranking",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                ),
                class_name="bg-[#0E0E0E]",
            ),
            rx.el.tbody(
                rx.foreach(
                    data.to(list[dict[str, str | int]]),
                    lambda a: rx.el.tr(
                        rx.el.td(
                            a["name"].to(str), class_name="p-2 text-sm text-white"
                        ),
                        rx.el.td(
                            a["kwh_cerrados_fmt"].to(str),
                            class_name="p-2 text-sm text-[#9CA3AF]",
                        ),
                        rx.el.td(
                            a["target_q_fmt"].to(str),
                            class_name="p-2 text-sm text-[#6B7280]",
                        ),
                        rx.el.td(
                            rx.el.span(
                                a["pct_str"].to(str),
                                class_name="font-bold",
                                style={"color": a["color"].to(str)},
                            ),
                            class_name="p-2 text-sm",
                        ),
                        rx.el.td(
                            a["gap_fmt"].to(str),
                            class_name="p-2 text-sm text-[#EF4444]",
                        ),
                        rx.el.td(
                            a["rank"].to(str), class_name="p-2 text-sm text-[#6B7280]"
                        ),
                        class_name="border-b border-white/5",
                    ),
                )
            ),
            class_name="w-full",
        ),
        class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6",
    )


def deal_explorer_preview() -> rx.Component:
    data = ReportState.deal_explorer_data
    return rx.el.div(
        rx.el.h3(
            "Deal Explorer (Top 50)", class_name="text-lg font-bold text-white mb-4"
        ),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Negocio",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "Propietario",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "Pipeline",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "Etapa",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "USD",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "kWh",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "Socio",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "Risk",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                ),
                class_name="bg-[#0E0E0E]",
            ),
            rx.el.tbody(
                rx.foreach(
                    data,
                    lambda d: rx.el.tr(
                        rx.el.td(
                            d["dealname"].to(str),
                            class_name="p-2 text-sm text-white max-w-[150px] truncate",
                        ),
                        rx.el.td(
                            d["owner_name"].to(str),
                            class_name="p-2 text-xs text-[#9CA3AF]",
                        ),
                        rx.el.td(
                            d["pipeline_name"].to(str),
                            class_name="p-2 text-xs text-[#6B7280]",
                        ),
                        rx.el.td(
                            d["stage_name"].to(str),
                            class_name="p-2 text-xs text-[#6B7280]",
                        ),
                        rx.el.td(
                            d["amount_fmt"].to(str),
                            class_name="p-2 text-sm font-medium text-[#10B981]",
                        ),
                        rx.el.td(
                            d["kwh_fmt"].to(str),
                            class_name="p-2 text-sm font-medium text-[#22D3EE]",
                        ),
                        rx.el.td(
                            d["socio"].to(str), class_name="p-2 text-xs text-[#9CA3AF]"
                        ),
                        rx.el.td(
                            rx.match(
                                d["risk_score"].to(str),
                                (
                                    "Bajo",
                                    rx.el.span(
                                        "Bajo",
                                        class_name="px-2 py-0.5 bg-[#10B981]/20 text-[#10B981] rounded-full text-[10px] font-bold",
                                    ),
                                ),
                                (
                                    "Medio",
                                    rx.el.span(
                                        "Medio",
                                        class_name="px-2 py-0.5 bg-[#F59E0B]/20 text-[#F59E0B] rounded-full text-[10px] font-bold",
                                    ),
                                ),
                                (
                                    "Alto",
                                    rx.el.span(
                                        "Alto",
                                        class_name="px-2 py-0.5 bg-[#EF4444]/20 text-[#EF4444] rounded-full text-[10px] font-bold",
                                    ),
                                ),
                                rx.fragment(),
                            ),
                            class_name="p-2",
                        ),
                        class_name="border-b border-white/5",
                    ),
                )
            ),
            class_name="w-full",
        ),
        class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6 overflow-x-auto",
    )


def temporal_preview() -> rx.Component:
    data = ReportState.temporal_report_data
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Seleccionar Período", class_name="text-lg font-bold text-white mr-4"
            ),
            rx.el.select(
                rx.el.option("Mes", value="month", class_name="bg-[#0E0E0E]"),
                rx.el.option("Trimestre", value="quarter", class_name="bg-[#0E0E0E]"),
                rx.el.option("Año", value="year", class_name="bg-[#0E0E0E]"),
                value=ReportState.temporal_period,
                on_change=ReportState.set_temporal_period,
                class_name="bg-[#0E0E0E] text-white border border-white/10 rounded-xl px-4 py-2 appearance-none",
            ),
            class_name="flex items-center mb-6",
        ),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Periodo",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "Nuevos Negocios",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "kWh Agregados",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "USD",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                    rx.el.th(
                        "Convenios",
                        class_name="text-left text-xs font-semibold text-[#9CA3AF] p-2",
                    ),
                ),
                class_name="bg-[#0E0E0E]",
            ),
            rx.el.tbody(
                rx.foreach(
                    data["periods"].to(list[dict[str, str | int]]),
                    lambda p: rx.el.tr(
                        rx.el.td(
                            p["label"].to(str),
                            class_name="p-2 text-sm text-white font-bold",
                        ),
                        rx.el.td(
                            p["deals"].to(str), class_name="p-2 text-sm text-[#9CA3AF]"
                        ),
                        rx.el.td(
                            p["kwh_fmt"].to(str),
                            class_name="p-2 text-sm font-medium text-[#22D3EE]",
                        ),
                        rx.el.td(
                            p["usd_fmt"].to(str),
                            class_name="p-2 text-sm font-medium text-[#10B981]",
                        ),
                        rx.el.td(
                            p["won"].to(str), class_name="p-2 text-sm text-[#9CA3AF]"
                        ),
                        class_name="border-b border-white/5",
                    ),
                )
            ),
            class_name="w-full",
        ),
        class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6",
    )


def reportes() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Centro de Reportes",
                    class_name="text-4xl font-bold text-white mb-2",
                ),
                rx.el.p(
                    "Reportes ejecutivos y operativos con datos vivos de HubSpot",
                    class_name="text-lg text-[#9CA3AF]",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                report_card(
                    "executive",
                    "Reporte Ejecutivo",
                    "file-bar-chart",
                    "KPIs, forecast, top asesores, riesgos",
                ),
                report_card(
                    "pipeline",
                    "Reporte Pipeline",
                    "git-commit-horizontal",
                    "Etapas, aging, deals estancados, funnel",
                ),
                report_card(
                    "advisor",
                    "Reporte por Asesor",
                    "users",
                    "Scorecard, conversión, cumplimiento, ranking",
                ),
                report_card(
                    "deal_explorer",
                    "Deal Explorer",
                    "search",
                    "Lista de negocios, timeline, risk score",
                ),
                report_card(
                    "temporal",
                    "Reporte Temporal",
                    "calendar",
                    "MoM, QoQ, YoY, tendencias",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6 mb-8",
            ),
            date_filter_bar(),
            rx.el.div(
                rx.el.h3(
                    "Programar Envío Automático",
                    class_name="text-sm font-bold text-white mb-2",
                ),
                rx.el.select(
                    rx.el.option("Ninguno", value="none", class_name="bg-[#0E0E0E]"),
                    rx.el.option("Diario", value="daily", class_name="bg-[#0E0E0E]"),
                    rx.el.option("Semanal", value="weekly", class_name="bg-[#0E0E0E]"),
                    rx.el.option("Mensual", value="monthly", class_name="bg-[#0E0E0E]"),
                    rx.el.option(
                        "Cierre de Quarter",
                        value="quarterly",
                        class_name="bg-[#0E0E0E]",
                    ),
                    value=ReportState.report_schedule,
                    on_change=ReportState.set_report_schedule,
                    class_name="bg-[#141414] text-white border border-white/10 rounded-xl px-4 py-2 w-full max-w-[250px] appearance-none",
                ),
                class_name="bg-[#0E0E0E] border border-[rgba(255,255,255,0.05)] p-4 rounded-xl mb-8 flex items-center gap-4 w-fit",
            ),
            rx.el.div(
                action_bar(),
                class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] p-6 rounded-2xl mb-8",
            ),
            rx.cond(
                ReportState.report_generated,
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.h2(
                                    "Vista Previa del Reporte",
                                    class_name="text-xl font-bold text-white",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        ReportState.report_meta["report_type_label"],
                                        class_name="px-2 py-0.5 rounded bg-[#DC2626]/20 text-[#DC2626] text-[10px] font-bold uppercase tracking-wider",
                                    ),
                                    rx.el.div(
                                        rx.icon("calendar", class_name="h-3 w-3"),
                                        rx.el.span(
                                            ReportState.report_meta["date_range"],
                                            class_name="text-[10px] font-bold",
                                        ),
                                        class_name="flex items-center gap-1.5 px-2 py-0.5 rounded bg-white/5 text-[#9CA3AF]",
                                    ),
                                    rx.el.div(
                                        rx.icon("briefcase", class_name="h-3 w-3"),
                                        rx.el.span(
                                            ReportState.report_meta[
                                                "deal_count"
                                            ].to_string()
                                            + " negocios",
                                            class_name="text-[10px] font-bold",
                                        ),
                                        class_name="flex items-center gap-1.5 px-2 py-0.5 rounded bg-white/5 text-[#9CA3AF]",
                                    ),
                                    class_name="flex flex-wrap gap-2 mt-2",
                                ),
                                class_name="flex flex-col",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Generado: ",
                                    rx.el.span(
                                        ReportState.report_meta["generated_at"],
                                        class_name="font-mono text-white",
                                    ),
                                    class_name="text-[10px] text-[#6B7280] uppercase tracking-tighter",
                                ),
                                class_name="flex flex-col items-end",
                            ),
                            class_name="flex justify-between items-start mb-6",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Período: ",
                                rx.el.span(
                                    ReportState.active_date_label,
                                    class_name="font-mono text-[#DC2626]",
                                ),
                                class_name="text-sm text-[#9CA3AF]",
                            ),
                            rx.el.p(
                                "Campo: ",
                                rx.el.span(
                                    ReportState.date_field_label, class_name="font-mono"
                                ),
                                class_name="text-sm text-[#9CA3AF]",
                            ),
                            class_name="flex flex-col gap-1 mb-8 p-4 bg-[#0E0E0E] rounded-xl border border-white/5",
                        ),
                    ),
                    rx.match(
                        ReportState.report_type,
                        ("executive", executive_preview()),
                        ("pipeline", pipeline_preview()),
                        ("advisor", advisor_preview()),
                        ("deal_explorer", deal_explorer_preview()),
                        ("temporal", temporal_preview()),
                        rx.fragment(),
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "Inteligencia Automática",
                            class_name="text-xl font-bold text-white mb-6 mt-12",
                        ),
                        rx.el.div(
                            rx.foreach(ReportState.report_insights, intelligence_card),
                            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                        ),
                        class_name="mb-8",
                    ),
                ),
                rx.fragment(),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Historial de Reportes",
                        class_name="text-xl font-bold text-white",
                    ),
                    rx.el.button(
                        "Limpiar Historial",
                        on_click=ReportState.clear_history,
                        class_name="text-sm text-[#DC2626] hover:text-white transition-colors",
                    ),
                    class_name="flex justify-between items-center mb-4",
                ),
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Fecha/Hora",
                                class_name="text-left text-xs font-semibold text-[#9CA3AF] p-3",
                            ),
                            rx.el.th(
                                "Tipo",
                                class_name="text-left text-xs font-semibold text-[#9CA3AF] p-3",
                            ),
                            rx.el.th(
                                "Filtros",
                                class_name="text-left text-xs font-semibold text-[#9CA3AF] p-3",
                            ),
                        ),
                        class_name="bg-[#0E0E0E]",
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            ReportState.report_history,
                            lambda h: rx.el.tr(
                                rx.el.td(
                                    h["timestamp"].to(str),
                                    class_name="p-3 text-sm text-[#9CA3AF]",
                                ),
                                rx.el.td(
                                    h["type"].to(str),
                                    class_name="p-3 text-sm font-bold text-white uppercase",
                                ),
                                rx.el.td(
                                    h["filters"].to(str),
                                    class_name="p-3 text-xs text-[#6B7280]",
                                ),
                                class_name="border-b border-white/5",
                            ),
                        )
                    ),
                    class_name="w-full",
                ),
                class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6 mt-12",
            ),
            class_name="max-w-7xl mx-auto pb-20",
        )
    )