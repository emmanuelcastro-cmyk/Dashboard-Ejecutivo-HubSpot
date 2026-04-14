import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.layout import layout


def breakdown_card(title: str, value: rx.Var, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-5 w-5", style={"color": color}),
                class_name="p-3 rounded-xl mb-4",
                style={"backgroundColor": f"{color}1a"},
            ),
            rx.el.p(
                title,
                class_name="text-xs font-bold text-[#9CA3AF] uppercase tracking-widest mb-2",
            ),
            rx.el.div(
                rx.el.span(value, class_name="text-2xl font-bold text-white"),
                class_name="flex justify-between items-end",
            ),
            class_name="p-6",
        ),
        class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl shadow-sm hover:bg-[#1A1A1A] transition-all",
    )


def kpi_card(
    title: str, value: str, icon: str, percentage: str = "", color: str = "#DC2626"
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-6 w-6", style={"color": color}),
                class_name="p-3 rounded-xl mb-6 w-fit",
                style={"backgroundColor": f"{color}1a"},
            ),
            rx.el.p(
                title,
                class_name="text-xs font-bold text-[#9CA3AF] uppercase tracking-widest mb-1",
            ),
            rx.el.div(
                rx.el.h3(
                    value,
                    class_name="text-3xl font-bold text-white truncate",
                    title=value,
                ),
                rx.icon(
                    "gallery_horizontal",
                    class_name="h-4 w-4 text-[#6B7280] cursor-pointer hover:text-white transition-colors",
                ),
                class_name="flex justify-between items-end",
            ),
            rx.cond(
                percentage != "",
                rx.el.div(
                    rx.el.span(
                        percentage,
                        class_name="text-xs font-bold text-[#10B981] bg-[rgba(255,255,255,0.06)] px-2 py-1 rounded-md mt-4 inline-block",
                    ),
                    class_name="mt-2",
                ),
                rx.fragment(),
            ),
            class_name="flex flex-col flex-1 p-6",
        ),
        class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl shadow-sm hover:bg-[#1A1A1A] transition-all duration-300",
    )


def filter_bar() -> rx.Component:
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
    ]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.select(
                    rx.el.option(
                        "All Pipelines",
                        value="all",
                        class_name="bg-[#0E0E0E] text-white",
                    ),
                    rx.el.option(
                        "Sales Pipeline",
                        value="default",
                        class_name="bg-[#0E0E0E] text-white",
                    ),
                    rx.el.option(
                        "Partners Pipeline",
                        value="803674731",
                        class_name="bg-[#0E0E0E] text-white",
                    ),
                    value=DashboardState.selected_pipeline,
                    on_change=DashboardState.set_pipeline,
                    class_name="appearance-none bg-[#0E0E0E] border border-[rgba(255,255,255,0.06)] text-white rounded-xl px-5 py-2.5 pr-10 focus:outline-none focus:border-[#DC2626] focus:ring-1 focus:ring-[#DC2626]/30 transition-all text-sm font-medium cursor-pointer",
                ),
                rx.icon(
                    "chevron-down",
                    class_name="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#9CA3AF] pointer-events-none",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.select(
                    rx.foreach(
                        DashboardState.owner_options,
                        lambda opt: rx.el.option(
                            opt[1], value=opt[0], class_name="bg-[#0E0E0E] text-white"
                        ),
                    ),
                    value=DashboardState.selected_owner,
                    on_change=DashboardState.set_owner,
                    class_name="appearance-none bg-[#0E0E0E] border border-[rgba(255,255,255,0.06)] text-white rounded-xl px-5 py-2.5 pr-10 focus:outline-none focus:border-[#DC2626] focus:ring-1 focus:ring-[#DC2626]/30 transition-all text-sm font-medium cursor-pointer",
                ),
                rx.icon(
                    "chevron-down",
                    class_name="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#9CA3AF] pointer-events-none",
                ),
                class_name="relative",
            ),
            rx.cond(
                DashboardState.is_loading,
                rx.el.div(
                    rx.icon("loader", class_name="h-4 w-4 text-[#DC2626] animate-spin"),
                    rx.el.span(
                        "Syncing...",
                        class_name="text-[10px] font-bold text-[#DC2626] tracking-widest uppercase",
                    ),
                    class_name="flex items-center gap-2 ml-2",
                ),
                rx.el.div(
                    rx.el.div(class_name="w-2 h-2 rounded-full bg-[#10B981]"),
                    rx.el.span(
                        "HubSpot Live",
                        class_name="text-[10px] font-bold text-[#10B981] tracking-widest uppercase",
                    ),
                    class_name="flex items-center gap-2 ml-auto px-4 py-2 bg-[#10B981]/10 rounded-full border-[#10B981]/20",
                ),
            ),
            class_name="flex gap-4 items-center mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.select(
                    rx.el.option(
                        "Fecha de creación",
                        value="createdate",
                        class_name="bg-[#0d1321]",
                    ),
                    rx.el.option(
                        "Fecha de cierre", value="closedate", class_name="bg-[#0d1321]"
                    ),
                    rx.el.option(
                        "Fecha 1er cierre",
                        value="fecha_de_1er_cierre",
                        class_name="bg-[#0d1321]",
                    ),
                    rx.el.option(
                        "Última actividad",
                        value="hs_lastmodifieddate",
                        class_name="bg-[#0d1321]",
                    ),
                    value=DashboardState.date_field,
                    on_change=DashboardState.set_date_field,
                    class_name="bg-[#0d1321] border border-white/10 text-white rounded-xl px-3 py-1.5 text-xs appearance-none",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.icon("calendar", class_name="h-3 w-3"),
                rx.el.span(
                    DashboardState.active_date_label, class_name="text-xs font-bold"
                ),
                class_name="bg-[#DC2626]/20 text-[#DC2626] px-3 py-1 rounded-full flex items-center gap-1.5",
            ),
            class_name="flex items-center gap-4 mb-4",
        ),
        rx.el.div(
            rx.foreach(
                presets,
                lambda p: rx.el.button(
                    p[0],
                    on_click=lambda: DashboardState.set_date_preset(p[1]),
                    class_name=rx.cond(
                        DashboardState.date_preset == p[1],
                        "whitespace-nowrap bg-[#DC2626] text-white rounded-full px-3 py-1.5 text-xs font-bold shadow",
                        "whitespace-nowrap bg-white/5 text-[#9CA3AF] hover:bg-white/10 rounded-full px-3 py-1.5 text-xs",
                    ),
                ),
            ),
            class_name="flex gap-2 overflow-x-auto pb-4 scrollbar-hide",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Desde", class_name="text-[10px] text-[#6B7280] uppercase mb-1"
                ),
                rx.el.input(
                    type="date",
                    on_change=DashboardState.set_custom_start,
                    class_name="bg-[#0d1321] border border-white/10 text-white rounded-xl px-3 py-2 text-sm",
                    default_value=DashboardState.custom_start,
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.label(
                    "Hasta", class_name="text-[10px] text-[#6B7280] uppercase mb-1"
                ),
                rx.el.input(
                    type="date",
                    on_change=DashboardState.set_custom_end,
                    class_name="bg-[#0d1321] border border-white/10 text-white rounded-xl px-3 py-2 text-sm",
                    default_value=DashboardState.custom_end,
                ),
                class_name="flex flex-col",
            ),
            class_name="flex gap-4",
        ),
        class_name="flex flex-col mb-10 bg-[#141414] p-5 rounded-2xl border border-[rgba(220,38,38,0.12)] shadow-xl",
    )


def resumen() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.h1(
                "Executive Summary", class_name="text-4xl font-bold text-white mb-8"
            ),
            filter_bar(),
            rx.el.div(
                kpi_card(
                    "Total Negocios",
                    DashboardState.total_deals,
                    "briefcase",
                    color="#DC2626",
                ),
                kpi_card(
                    "Activos",
                    DashboardState.active_deals,
                    "activity",
                    DashboardState.active_deals_percent,
                    color="#22D3EE",
                ),
                kpi_card(
                    "Convenio Firmado",
                    DashboardState.convenio_firmado,
                    "message_circle_check",
                    DashboardState.convenio_firmado_percent,
                    color="#10B981",
                ),
                kpi_card(
                    "Cerrados Perdidos",
                    DashboardState.cerrados_perdidos,
                    "message_circle_x",
                    DashboardState.cerrados_perdidos_percent,
                    color="#EF4444",
                ),
                kpi_card("kWh Total", DashboardState.total_kwh, "zap", "", "#F59E0B"),
                kpi_card(
                    "Valor USD", DashboardState.total_usd, "dollar-sign", "", "#10B981"
                ),
                kpi_card(
                    "Propuestas Enviadas",
                    DashboardState.propuestas_enviadas,
                    "send",
                    "",
                    "#3B82F6",
                ),
                kpi_card(
                    "Ciclo Promedio Venta",
                    DashboardState.avg_sales_cycle_days + " días",
                    "clock",
                    "",
                    "#A78BFA",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Valor USD Total",
                        class_name="text-lg font-semibold text-[#9CA3AF] mb-6 text-center",
                    ),
                    rx.el.div(
                        rx.el.span(
                            DashboardState.total_usd,
                            class_name="text-5xl font-bold text-white",
                        ),
                        class_name="flex justify-center mb-3",
                    ),
                    rx.el.div(
                        rx.el.span(
                            DashboardState.usd_deals_with_amount_pct,
                            class_name="text-sm text-[#6B7280]",
                        ),
                        class_name="text-center",
                    ),
                    class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-8 shadow-xl flex flex-col justify-center",
                ),
                rx.el.div(
                    rx.el.h3(
                        "kWh Cerrados vs Meta ",
                        DashboardState.current_quarter_label,
                        class_name="text-lg font-semibold text-[#9CA3AF] mb-6 text-center",
                    ),
                    rx.el.div(
                        rx.el.svg(
                            rx.el.circle(
                                cx="70",
                                cy="70",
                                r="60",
                                fill="none",
                                stroke="rgba(255,255,255,0.06)",
                                stroke_width="12",
                            ),
                            rx.el.circle(
                                cx="70",
                                cy="70",
                                r="60",
                                fill="none",
                                stroke=DashboardState.overall_pct_q_color,
                                stroke_width="12",
                                stroke_dasharray=f"{2 * 3.14159 * 60}",
                                stroke_dashoffset=str(
                                    2
                                    * 3.14159
                                    * 60
                                    * (1 - DashboardState.kwh_gauge_pct / 100)
                                ),
                                stroke_linecap="round",
                                transform="rotate(-90 70 70)",
                                class_name="transition-all duration-1000",
                            ),
                            rx.el.text(
                                str(DashboardState.overall_pct_q) + "%",
                                x="70",
                                y="60",
                                text_anchor="middle",
                                dominant_baseline="middle",
                                class_name="text-2xl font-bold fill-white",
                            ),
                            rx.el.text(
                                "kWh",
                                x="70",
                                y="82",
                                text_anchor="middle",
                                dominant_baseline="middle",
                                class_name="text-[10px] fill-[#6B7280]",
                            ),
                            width="140",
                            height="140",
                            class_name="mx-auto",
                        ),
                        class_name="flex justify-center mb-4",
                    ),
                    rx.el.div(
                        rx.el.span(
                            DashboardState.total_kwh_cerrados_q_fmt,
                            class_name="text-sm font-bold text-white",
                        ),
                        rx.el.span(" / ", class_name="text-sm text-[#6B7280]"),
                        rx.el.span(
                            DashboardState.total_target_q_fmt,
                            class_name="text-sm text-[#9CA3AF]",
                        ),
                        rx.el.span(" kWh", class_name="text-sm text-[#6B7280]"),
                        class_name="text-center",
                    ),
                    class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6 shadow-xl",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6",
            ),
            rx.el.div(
                breakdown_card(
                    "kWh Cerrados",
                    DashboardState.kwh_cerrados,
                    "message_circle_check",
                    "#10B981",
                ),
                breakdown_card(
                    "kWh Activos", DashboardState.kwh_activos, "activity", "#22D3EE"
                ),
                breakdown_card(
                    "kWh Perdidos",
                    DashboardState.kwh_perdidos,
                    "message_circle_x",
                    "#EF4444",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6 mb-12",
            ),
            class_name="max-w-7xl mx-auto",
        )
    )


def kpi_card(
    title: str, value: str, icon: str, percentage: str = "", color: str = "#00d4ff"
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    title,
                    class_name="text-sm font-medium text-gray-400 truncate max-w-full",
                ),
                rx.el.h3(
                    value,
                    class_name="text-2xl font-bold text-white mt-2 truncate max-w-full",
                    title=value,
                ),
                class_name="flex flex-col min-w-0 flex-1 pr-2",
            ),
            rx.el.div(
                rx.icon(icon, class_name=f"h-8 w-8 text-[{color}]"),
                class_name=f"p-3 bg-[{color}]/10 rounded-xl",
            ),
            class_name="flex justify-between items-start",
        ),
        rx.cond(
            percentage != "",
            rx.el.div(
                rx.el.span(
                    percentage,
                    class_name="text-sm font-medium bg-white/10 px-2 py-1 rounded text-[#00ff88] truncate max-w-full",
                    title=percentage,
                ),
                class_name="mt-4",
            ),
            rx.fragment(),
        ),
        class_name="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-xl hover:bg-white/10 transition-all duration-300",
    )


def filter_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.select(
                rx.el.option(
                    "Todos los Pipelines",
                    value="all",
                    class_name="bg-[#0d1321] text-white",
                ),
                rx.el.option(
                    "Pipeline de Ventas",
                    value="default",
                    class_name="bg-[#0d1321] text-white",
                ),
                rx.el.option(
                    "Pipeline de Socios",
                    value="803674731",
                    class_name="bg-[#0d1321] text-white",
                ),
                value=DashboardState.selected_pipeline,
                on_change=DashboardState.set_pipeline,
                class_name="appearance-none bg-[#0d1321] border border-white/10 text-white rounded-xl px-5 py-2.5 pr-10 focus:outline-none focus:border-[#a3e635] focus:ring-1 focus:ring-[#a3e635]/30 transition-all text-sm font-medium",
            ),
            rx.icon(
                "chevron-down",
                class_name="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#94a3b8] pointer-events-none",
            ),
            class_name="relative",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    DashboardState.owner_options,
                    lambda opt: rx.el.option(
                        opt[1], value=opt[0], class_name="bg-[#0d1321] text-white"
                    ),
                ),
                value=DashboardState.selected_owner,
                on_change=DashboardState.set_owner,
                class_name="appearance-none bg-[#0d1321] border border-white/10 text-white rounded-xl px-5 py-2.5 pr-10 focus:outline-none focus:border-[#a3e635] focus:ring-1 focus:ring-[#a3e635]/30 transition-all text-sm font-medium",
            ),
            rx.icon(
                "chevron-down",
                class_name="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#94a3b8] pointer-events-none",
            ),
            class_name="relative",
        ),
        rx.cond(
            DashboardState.is_loading,
            rx.el.div(
                rx.icon("loader", class_name="h-5 w-5 text-[#a3e635] animate-spin"),
                rx.el.span(
                    "Syncing...",
                    class_name="text-xs font-bold text-[#a3e635] tracking-widest",
                ),
                class_name="flex items-center gap-2 ml-2",
            ),
            rx.el.div(
                rx.icon("message_circle_check", class_name="h-4 w-4 text-[#a3e635]"),
                rx.el.span(
                    "HubSpot Live",
                    class_name="text-[10px] font-black text-[#a3e635] tracking-widest uppercase",
                ),
                class_name="flex items-center gap-2 ml-auto px-4 py-2 bg-[#a3e635]/10 rounded-full border border-[#a3e635]/20",
            ),
        ),
        class_name="flex gap-4 items-center mb-10 bg-[#0d1321]/50 backdrop-blur-xl p-5 rounded-2xl border border-white/5 shadow-xl",
    )


def resumen() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.h1(
                "Executive Summary",
                class_name="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#00d4ff] to-[#00ff88] mb-8",
            ),
            filter_bar(),
            rx.el.div(
                kpi_card(
                    "Total Negocios",
                    DashboardState.total_deals.to_string(),
                    "briefcase",
                ),
                kpi_card(
                    "Activos",
                    DashboardState.active_deals.to_string(),
                    "activity",
                    DashboardState.active_deals_percent,
                    "#00ff88",
                ),
                kpi_card(
                    "Convenio Firmado",
                    DashboardState.convenio_firmado.to_string(),
                    "message_circle_check",
                    DashboardState.convenio_firmado_percent,
                    "#00ff88",
                ),
                kpi_card(
                    "Cerrados Perdidos",
                    DashboardState.cerrados_perdidos.to_string(),
                    "message_circle_x",
                    DashboardState.cerrados_perdidos_percent,
                    "#ff3366",
                ),
                kpi_card("kWh Total", DashboardState.total_kwh, "zap", "", "#ffb703"),
                kpi_card(
                    "Valor USD", DashboardState.total_usd, "dollar-sign", "", "#00ff88"
                ),
                kpi_card(
                    "Propuestas Enviadas",
                    DashboardState.propuestas_enviadas.to_string(),
                    "send",
                    "",
                    "#00d4ff",
                ),
                kpi_card(
                    "Ciclo Promedio Venta",
                    DashboardState.avg_sales_cycle_days + " días",
                    "clock",
                    "",
                    "#a78bfa",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Valor USD Total",
                        class_name="text-lg font-semibold text-gray-200 mb-6 text-center",
                    ),
                    rx.el.div(
                        rx.el.span(
                            DashboardState.total_usd,
                            class_name="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#00ff88] to-[#00d4ff]",
                        ),
                        class_name="flex justify-center mb-3",
                    ),
                    rx.el.div(
                        rx.el.span(
                            DashboardState.usd_deals_with_amount_pct,
                            class_name="text-sm text-gray-400",
                        ),
                        class_name="text-center",
                    ),
                    class_name="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8 shadow-xl flex flex-col justify-center",
                ),
                rx.el.div(
                    rx.el.h3(
                        "kWh Cerrados vs Meta ",
                        DashboardState.current_quarter_label,
                        class_name="text-lg font-semibold text-gray-200 mb-6 text-center",
                    ),
                    rx.el.div(
                        rx.el.svg(
                            rx.el.circle(
                                cx="70",
                                cy="70",
                                r="60",
                                fill="none",
                                stroke="rgba(255,255,255,0.1)",
                                stroke_width="12",
                            ),
                            rx.el.circle(
                                cx="70",
                                cy="70",
                                r="60",
                                fill="none",
                                stroke=DashboardState.overall_pct_q_color,
                                stroke_width="12",
                                stroke_dasharray=f"{2 * 3.14159 * 60}",
                                stroke_dashoffset=(
                                    2
                                    * 3.14159
                                    * 60
                                    * (1 - DashboardState.kwh_gauge_pct / 100)
                                ).to_string(),
                                stroke_linecap="round",
                                transform="rotate(-90 70 70)",
                                class_name="transition-all duration-1000",
                            ),
                            rx.el.text(
                                DashboardState.overall_pct_q.to_string() + "%",
                                x="70",
                                y="60",
                                text_anchor="middle",
                                dominant_baseline="middle",
                                class_name="text-2xl font-bold fill-white",
                            ),
                            rx.el.text(
                                "kWh",
                                x="70",
                                y="82",
                                text_anchor="middle",
                                dominant_baseline="middle",
                                class_name="text-[10px] fill-gray-400",
                            ),
                            width="140",
                            height="140",
                            class_name="mx-auto",
                        ),
                        class_name="flex justify-center mb-4",
                    ),
                    rx.el.div(
                        rx.el.span(
                            DashboardState.total_kwh_cerrados_q_fmt,
                            class_name="text-sm font-bold text-white",
                        ),
                        rx.el.span(" / ", class_name="text-sm text-gray-500"),
                        rx.el.span(
                            DashboardState.total_target_q_fmt,
                            class_name="text-sm text-gray-400",
                        ),
                        rx.el.span(" kWh", class_name="text-sm text-gray-500"),
                        class_name="text-center",
                    ),
                    class_name="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-xl",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6",
            ),
            rx.el.div(
                breakdown_card(
                    "kWh Cerrados",
                    DashboardState.kwh_cerrados,
                    "message_circle_check",
                    "#00ff88",
                ),
                breakdown_card(
                    "kWh Activos", DashboardState.kwh_activos, "activity", "#00d4ff"
                ),
                breakdown_card(
                    "kWh Perdidos",
                    DashboardState.kwh_perdidos,
                    "message_circle_x",
                    "#ff3366",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6 mb-12",
            ),
            class_name="max-w-7xl mx-auto",
        )
    )