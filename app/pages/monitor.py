import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.layout import layout


def sync_log_row(log: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            log["timestamp"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-[#9CA3AF]",
        ),
        rx.el.td(
            rx.el.span(
                log["status"],
                class_name=rx.cond(
                    log["status"] == "success",
                    "px-2 py-1 rounded-lg text-xs font-bold bg-[#10B981]/10 text-[#10B981]",
                    "px-2 py-1 rounded-lg text-xs font-bold bg-[#EF4444]/10 text-[#EF4444]",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            log["deals"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-[#9CA3AF]",
        ),
        rx.el.td(
            log["owners"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-[#9CA3AF]",
        ),
        rx.el.td(
            log["duration"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-[#9CA3AF]",
        ),
        rx.el.td(
            log["http_status"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-[#9CA3AF]",
        ),
        rx.el.td(
            rx.el.span(
                log["error"],
                class_name="truncate block max-w-[200px]",
                title=log["error"],
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-[#EF4444]",
        ),
        class_name="border-b border-white/5 hover:bg-white/5 transition-colors duration-200",
    )


def status_metric(label: str, value: rx.Var, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-[#DC2626]"),
            rx.el.p(label, class_name="text-sm font-medium text-[#9CA3AF]"),
            class_name="flex items-center gap-2 mb-2",
        ),
        rx.el.h4(value.to_string(), class_name="text-xl font-bold text-white"),
        class_name="bg-[#0E0E0E] border border-white/5 rounded-xl p-4",
    )


def monitor() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1("Monitor HubSpot", class_name="text-4xl font-bold text-white"),
                rx.el.button(
                    rx.cond(
                        DashboardState.is_loading,
                        rx.icon("loader", class_name="h-5 w-5 animate-spin mr-2"),
                        rx.icon("refresh-cw", class_name="h-5 w-5 mr-2"),
                    ),
                    "Actualizar Ahora",
                    on_click=DashboardState.manual_refresh,
                    disabled=DashboardState.is_loading,
                    class_name="flex items-center bg-[#DC2626] hover:bg-[#DC2626]/80 text-white px-6 py-3 rounded-xl font-bold transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed",
                ),
                class_name="flex justify-between items-center mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.cond(
                        DashboardState.hubspot_connected,
                        rx.el.div(
                            rx.el.div(
                                class_name="w-4 h-4 rounded-full bg-[#10B981] animate-pulse"
                            ),
                            rx.el.h2(
                                "Conectado a HubSpot",
                                class_name="text-2xl font-bold text-white",
                            ),
                            class_name="flex items-center gap-3 mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(class_name="w-4 h-4 rounded-full bg-[#EF4444]"),
                            rx.el.h2(
                                "Error de conexión",
                                class_name="text-2xl font-bold text-white",
                            ),
                            class_name="flex items-center gap-3 mb-6",
                        ),
                    ),
                    rx.el.div(
                        status_metric(
                            "Última Sincronización",
                            DashboardState.last_sync_timestamp,
                            "clock",
                        ),
                        status_metric(
                            "Duración (seg)", DashboardState.last_sync_duration, "timer"
                        ),
                        status_metric(
                            "Negocios Cargados",
                            DashboardState.last_sync_deal_count,
                            "briefcase",
                        ),
                        status_metric(
                            "Propietarios Cargados",
                            DashboardState.last_sync_owner_count,
                            "users",
                        ),
                        status_metric(
                            "HTTP Status",
                            DashboardState.last_sync_http_status,
                            "server",
                        ),
                        status_metric(
                            "Endpoint", DashboardState.last_sync_endpoint, "link"
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
                    ),
                    rx.cond(
                        DashboardState.last_sync_error != "",
                        rx.el.div(
                            rx.icon(
                                "triangle_alert",
                                class_name="h-5 w-5 text-[#EF4444] mr-2",
                            ),
                            rx.el.span(
                                DashboardState.last_sync_error,
                                class_name="text-sm text-[#EF4444]",
                            ),
                            class_name="mt-6 p-4 bg-[#EF4444]/10 border border-[#EF4444]/20 rounded-xl flex items-start",
                        ),
                        rx.fragment(),
                    ),
                    class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl p-6 shadow-xl",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.h2(
                    "Historial de Sincronización",
                    class_name="text-xl font-bold text-white mb-6",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Fecha/Hora",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Status",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Negocios",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Propietarios",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Duración",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "HTTP",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Error",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider",
                                ),
                                class_name="bg-[#0E0E0E]",
                            )
                        ),
                        rx.el.tbody(rx.foreach(DashboardState.sync_log, sync_log_row)),
                        class_name="w-full table-auto",
                    ),
                    class_name="bg-[#141414] border border-[rgba(220,38,38,0.12)] rounded-2xl shadow-xl overflow-x-auto overflow-y-auto max-h-[500px]",
                ),
            ),
            class_name="max-w-7xl mx-auto",
        )
    )