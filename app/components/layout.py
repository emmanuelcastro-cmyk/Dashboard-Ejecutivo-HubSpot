import reflex as rx
from app.states.dashboard_state import DashboardState


def sidebar_item(icon: str, label: str, tab_id: str, href: str) -> rx.Component:
    is_active = rx.cond(rx.State.router.page.path == href, True, False)
    return rx.el.a(
        rx.icon(icon, class_name="h-5 w-5 mr-3"),
        rx.el.span(label, class_name="font-medium"),
        href=href,
        class_name=rx.cond(
            is_active,
            "flex items-center p-3 mx-4 mb-1 rounded-xl bg-[#DC2626] text-white transition-all duration-200",
            "flex items-center p-3 mx-4 mb-1 rounded-xl text-[#9CA3AF] hover:bg-[rgba(220,38,38,0.08)] hover:text-white transition-all duration-200",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src="/white_q_red.png",
                        class_name="h-9 w-9 rounded-lg object-contain",
                    ),
                    rx.el.span(
                        "QUARTUX",
                        class_name="text-xl font-bold text-white tracking-widest",
                    ),
                    class_name="flex items-center gap-3",
                ),
                rx.el.div(
                    class_name="absolute bottom-0 left-6 right-6 h-[1px] bg-[rgba(220,38,38,0.1)]"
                ),
                class_name="flex h-20 items-center px-8 relative",
            ),
            rx.el.nav(
                sidebar_item("layout-dashboard", "Resumen", "resumen", "/"),
                sidebar_item(
                    "git-commit-horizontal",
                    "Pipeline Detallado",
                    "pipeline",
                    "/pipeline",
                ),
                sidebar_item("users", "Equipo Comercial", "equipo", "/equipo"),
                sidebar_item("activity", "Actividad", "actividad", "/actividad"),
                sidebar_item("clock", "Desglose Tiempo", "tiempo", "/tiempo"),
                sidebar_item("table-2", "Scorecard Mensual", "scorecard", "/scorecard"),
                sidebar_item("target", "Cumplimiento Metas", "metas", "/metas"),
                sidebar_item(
                    "square_activity", "Monitor HubSpot", "monitor", "/monitor"
                ),
                sidebar_item(
                    "file-bar-chart-2", "Centro de Reportes", "reportes", "/reportes"
                ),
                class_name="flex flex-col gap-1 mt-6 flex-1",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="flex flex-col border-r border-[rgba(255,255,255,0.06)] bg-[#0E0E0E] w-[280px] h-screen shrink-0 sticky top-0",
    )


def search_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search",
                class_name="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4 text-[#6B7280]",
            ),
            rx.el.input(
                placeholder="Search everything...",
                on_change=DashboardState.set_search_query,
                class_name="w-full bg-[#141414] border border-[rgba(255,255,255,0.06)] text-white rounded-full pl-12 pr-10 py-2.5 focus:outline-none focus:border-[#DC2626] transition-all text-sm",
                default_value=DashboardState.search_query,
            ),
            rx.cond(
                DashboardState.search_query != "",
                rx.icon(
                    "circle-x",
                    class_name="absolute right-4 top-1/2 -translate-y-1/2 h-4 w-4 text-[#6B7280] cursor-pointer hover:text-white transition-colors",
                    on_click=DashboardState.clear_search,
                ),
                rx.fragment(),
            ),
            class_name="relative w-[320px]",
        ),
        rx.cond(
            (DashboardState.search_query.length() >= 2)
            & (DashboardState.search_results.length() > 0),
            rx.el.div(
                rx.foreach(
                    DashboardState.search_results,
                    lambda res: rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                res["dealname"],
                                class_name="text-sm font-bold text-white truncate",
                            ),
                            rx.el.span(
                                res["pipeline"],
                                class_name="text-[10px] bg-[#DC2626]/20 px-2 py-0.5 rounded text-[#DC2626] font-bold",
                            ),
                            class_name="flex justify-between items-center mb-1",
                        ),
                        rx.el.div(
                            rx.el.span(
                                res["owner"], class_name="text-xs text-[#9CA3AF]"
                            ),
                            rx.el.span(
                                res["stage"],
                                class_name="text-xs text-[#22D3EE] font-medium",
                            ),
                            class_name="flex justify-between items-center",
                        ),
                        on_click=lambda: DashboardState.search_and_open(res["deal_id"]),
                        class_name="p-4 hover:bg-[rgba(220,38,38,0.08)] cursor-pointer border-b border-[rgba(255,255,255,0.06)] transition-all",
                    ),
                ),
                class_name="absolute top-full left-0 right-0 mt-3 bg-[#141414] border border-[rgba(220,38,38,0.15)] rounded-2xl shadow-2xl z-[100] overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200",
            ),
            rx.fragment(),
        ),
        class_name="relative z-50",
    )


def deal_detail_panel() -> rx.Component:
    return rx.el.div(
        rx.cond(
            DashboardState.show_deal_detail,
            rx.el.div(
                rx.el.div(
                    class_name="fixed inset-0 bg-[#0A0A0A]/60 backdrop-blur-sm z-[90] animate-in fade-in duration-300",
                    on_click=DashboardState.close_deal_detail,
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                DashboardState.deal_detail["dealname"],
                                class_name="text-xl font-bold text-white truncate pr-8",
                            ),
                            rx.el.span(
                                "ID: " + DashboardState.selected_deal_id,
                                class_name="text-[10px] text-[#6B7280] font-mono tracking-wider",
                            ),
                            class_name="flex flex-col",
                        ),
                        rx.icon(
                            "x",
                            class_name="h-5 w-5 text-[#6B7280] cursor-pointer hover:text-white transition-colors",
                            on_click=DashboardState.close_deal_detail,
                        ),
                        class_name="p-8 border-b border-[rgba(255,255,255,0.06)] flex justify-between items-start bg-gradient-to-r from-[#0E0E0E] to-[#141414]",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "user", class_name="h-4 w-4 text-[#10B981]"
                                    ),
                                    rx.el.span(
                                        "Advisor",
                                        class_name="text-[10px] text-[#9CA3AF] font-bold uppercase",
                                    ),
                                    class_name="flex items-center gap-2 mb-2",
                                ),
                                rx.el.p(
                                    DashboardState.deal_detail["owner"],
                                    class_name="text-sm font-bold text-white",
                                ),
                                class_name="p-5 bg-[#141414] rounded-2xl border border-[rgba(220,38,38,0.12)] shadow-sm",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "git-branch",
                                        class_name="h-4 w-4 text-[#DC2626]",
                                    ),
                                    rx.el.span(
                                        "Pipeline",
                                        class_name="text-[10px] text-[#9CA3AF] font-bold uppercase",
                                    ),
                                    class_name="flex items-center gap-2 mb-2",
                                ),
                                rx.el.p(
                                    DashboardState.deal_detail["pipeline"],
                                    class_name="text-sm font-bold text-white",
                                ),
                                class_name="p-5 bg-[#141414] rounded-2xl border border-[rgba(220,38,38,0.12)] shadow-sm",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "dollar-sign",
                                        class_name="h-4 w-4 text-[#10B981]",
                                    ),
                                    rx.el.span(
                                        "Amount",
                                        class_name="text-[10px] text-[#9CA3AF] font-bold uppercase",
                                    ),
                                    class_name="flex items-center gap-2 mb-2",
                                ),
                                rx.el.p(
                                    DashboardState.deal_detail["amount"],
                                    class_name="text-sm font-bold text-white",
                                ),
                                class_name="p-5 bg-[#141414] rounded-2xl border border-[rgba(220,38,38,0.12)] shadow-sm",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.icon("zap", class_name="h-4 w-4 text-[#22D3EE]"),
                                    rx.el.span(
                                        "Capacity",
                                        class_name="text-[10px] text-[#9CA3AF] font-bold uppercase",
                                    ),
                                    class_name="flex items-center gap-2 mb-2",
                                ),
                                rx.el.p(
                                    DashboardState.deal_detail["kwh"].to_string()
                                    + " kWh",
                                    class_name="text-sm font-bold text-white",
                                ),
                                class_name="p-5 bg-[#141414] rounded-2xl border border-[rgba(220,38,38,0.12)] shadow-sm",
                            ),
                            class_name="grid grid-cols-2 gap-4 p-8 bg-[#0E0E0E]",
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "Deal Lifecycle",
                                class_name="text-xs font-bold text-[#9CA3AF] uppercase tracking-widest mb-10 flex items-center gap-2",
                            ),
                            rx.el.div(
                                rx.foreach(
                                    DashboardState.deal_detail["timeline"].to(
                                        list[dict[str, str | bool]]
                                    ),
                                    lambda step: rx.el.div(
                                        rx.el.div(
                                            rx.el.div(
                                                rx.cond(
                                                    step["active"],
                                                    rx.el.div(
                                                        rx.cond(
                                                            step["is_current"],
                                                            rx.el.div(
                                                                class_name="absolute inset-0 rounded-full animate-ping opacity-60",
                                                                style={
                                                                    "backgroundColor": "#22D3EE"
                                                                },
                                                            ),
                                                            rx.fragment(),
                                                        ),
                                                        class_name="w-3 h-3 rounded-full relative z-10",
                                                        style={
                                                            "backgroundColor": rx.cond(
                                                                step["is_current"],
                                                                "#22D3EE",
                                                                "#10B981",
                                                            )
                                                        },
                                                    ),
                                                    rx.el.div(
                                                        class_name="w-3 h-3 rounded-full border-2 border-[rgba(255,255,255,0.1)] bg-[#0E0E0E] relative z-10"
                                                    ),
                                                ),
                                                rx.el.div(
                                                    class_name="absolute top-3 left-[5px] bottom-[-2.5rem] w-[2px] bg-[rgba(255,255,255,0.05)] -z-10"
                                                ),
                                                class_name="relative mr-8 flex-shrink-0",
                                            ),
                                            rx.el.div(
                                                rx.el.p(
                                                    step["label"],
                                                    class_name=rx.cond(
                                                        step["active"],
                                                        "text-sm font-bold text-white",
                                                        "text-sm font-medium text-[#6B7280]",
                                                    ),
                                                ),
                                                rx.cond(
                                                    step["entered"] != "",
                                                    rx.el.p(
                                                        step["entered"],
                                                        class_name="text-[10px] text-[#9CA3AF] mt-1 font-medium",
                                                    ),
                                                    rx.fragment(),
                                                ),
                                                class_name="pb-12",
                                            ),
                                            rx.cond(
                                                step["days"] != "",
                                                rx.el.div(
                                                    step["days"],
                                                    class_name="ml-auto text-[10px] font-bold text-[#9CA3AF] bg-white/5 px-2 py-0.5 rounded-full border border-[rgba(255,255,255,0.06)] h-fit",
                                                ),
                                                rx.fragment(),
                                            ),
                                            class_name="flex items-start",
                                        )
                                    ),
                                ),
                                class_name="flex flex-col",
                            ),
                            class_name="px-8 py-8",
                        ),
                        class_name="overflow-y-auto h-[calc(100vh-120px)]",
                    ),
                    class_name="fixed top-0 right-0 h-screen w-[480px] bg-[#0E0E0E] border-l border-[rgba(255,255,255,0.06)] shadow-2xl z-[100] transform transition-all duration-500 ease-out animate-in slide-in-from-right duration-500",
                ),
                rx.fragment(),
            ),
            rx.fragment(),
        )
    )


def layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            rx.el.header(
                search_bar(),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "ES",
                            class_name="text-[10px] font-bold text-white bg-white/10 px-2 py-1 rounded",
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.div(
                        rx.icon(
                            "bell",
                            class_name="h-5 w-5 text-[#9CA3AF] cursor-pointer hover:text-white transition-colors",
                        ),
                        rx.el.div(
                            class_name="absolute top-0 right-0 h-2 w-2 bg-[#EF4444] rounded-full border-2 border-[#0A0A0A]"
                        ),
                        class_name="relative p-2",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Quartux Admin",
                                class_name="text-xs font-bold text-white",
                            ),
                            rx.el.p(
                                "Administrator", class_name="text-[10px] text-[#9CA3AF]"
                            ),
                            class_name="flex flex-col items-end mr-3 hidden md:flex",
                        ),
                        rx.el.div(
                            rx.el.span("QA", class_name="text-xs font-bold text-white"),
                            class_name="size-9 rounded-full bg-[#DC2626] flex items-center justify-center cursor-pointer shadow-lg hover:brightness-110 transition-all",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex items-center gap-6",
                ),
                class_name="h-20 flex items-center justify-between px-10 bg-[#0A0A0A]/80 backdrop-blur-xl sticky top-0 z-40",
            ),
            rx.el.main(
                content,
                class_name="flex-1 p-10 h-[calc(100vh-5rem)] overflow-y-auto relative",
            ),
            class_name="flex-1 flex flex-col h-screen overflow-hidden",
        ),
        deal_detail_panel(),
        class_name="flex min-h-screen w-screen bg-[#0A0A0A] text-white font-['Poppins'] selection:bg-[#DC2626]/30",
    )