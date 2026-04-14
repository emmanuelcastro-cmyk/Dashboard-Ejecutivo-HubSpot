import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.layout import layout


def radial_gauge(data: dict, size: int = 120, stroke_width: int = 10) -> rx.Component:
    radius = (size - stroke_width) // 2
    circumference = 2 * 3.14159 * radius
    s_size = f"{size}"
    s_center = f"{size // 2}"
    s_radius = f"{radius}"
    s_stroke = f"{stroke_width}"
    s_circum = f"{circumference}"
    return rx.el.div(
        rx.el.svg(
            rx.el.circle(
                cx=s_center,
                cy=s_center,
                r=s_radius,
                fill="none",
                stroke="rgba(255,255,255,0.05)",
                stroke_width=s_stroke,
            ),
            rx.el.circle(
                cx=s_center,
                cy=s_center,
                r=s_radius,
                fill="none",
                stroke=data["color"],
                stroke_width=s_stroke,
                stroke_dasharray=s_circum,
                stroke_dashoffset=(
                    circumference * (1 - data["bar_pct"].to(float) / 100)
                ).to_string(),
                stroke_linecap="round",
                transform=f"rotate(-90 {s_center} {s_center})",
                class_name="transition-all duration-1000",
            ),
            rx.el.text(
                data["pct_str"],
                x="50%",
                y="50%",
                text_anchor="middle",
                dominant_baseline="middle",
                class_name="text-lg font-bold fill-white",
            ),
            width=s_size,
            height=s_size,
            class_name="mx-auto",
        ),
        rx.el.p(
            data["name"],
            class_name="text-xs font-semibold text-[#9CA3AF] mt-3 text-center truncate w-full px-2",
        ),
        rx.el.p(
            f"{data['kwh_cerrados_fmt']} / {data['target_q_fmt']} kWh",
            class_name="text-[10px] text-[#6B7280] text-center",
        ),
        class_name="flex flex-col items-center",
    )


def leaderboard_row(row: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.span(f"#{row['rank']}", class_name="font-bold text-[#6B7280]"),
            class_name="px-4 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            rx.el.span(
                row["name"],
                class_name="font-medium text-white hover:text-[#DC2626] transition-colors cursor-pointer",
            ),
            class_name="px-4 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            row["kwh_cerrados_fmt"],
            class_name="px-4 py-4 whitespace-nowrap text-sm text-[#9CA3AF]",
        ),
        rx.el.td(
            row["target_q_fmt"],
            class_name="px-4 py-4 whitespace-nowrap text-sm text-[#6B7280]",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        class_name="h-full rounded-full transition-all duration-500",
                        style={
                            "width": f"{row['bar_pct']}%",
                            "backgroundColor": row["color"],
                        },
                    ),
                    class_name="w-24 h-1.5 bg-white/10 rounded-full mr-3 overflow-hidden",
                ),
                rx.el.span(
                    row["pct_str"],
                    class_name="font-bold",
                    style={"color": row["color"]},
                ),
                class_name="flex items-center",
            ),
            class_name="px-4 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            row["gap_fmt"],
            class_name="px-4 py-4 whitespace-nowrap text-sm text-[#EF4444] font-medium",
        ),
        rx.el.td(
            row["projected_fmt"],
            class_name="px-4 py-4 whitespace-nowrap text-sm text-[#22D3EE] font-medium",
        ),
        rx.el.td(
            rx.el.span(row["forecast_pct_str"], class_name="font-bold text-white"),
            class_name="px-4 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            rx.cond(
                row["will_meet"],
                rx.icon("circle_check", class_name="h-5 w-5 text-[#10B981]"),
                rx.icon("circle_alert", class_name="h-5 w-5 text-[#EF4444]"),
            ),
            class_name="px-4 py-4 whitespace-nowrap",
        ),
        class_name="hover:bg-white/5 border-b border-white/5 transition-colors",
    )


def horizontal_progress_bar(data: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                data["name"],
                class_name="text-sm font-medium text-gray-300 w-48 truncate",
            ),
            rx.el.div(
                rx.el.div(
                    class_name="h-full rounded-full transition-all duration-1000",
                    style={
                        "width": f"{data['bar_pct']}%",
                        "backgroundColor": data["color"],
                    },
                ),
                class_name="flex-1 h-3 bg-white/5 rounded-full relative overflow-hidden group",
                title=f"Cerrado: {data['kwh_cerrados_fmt']} | Meta: {data['target_q_fmt']} | Faltante: {data['gap_fmt']}",
            ),
            rx.el.span(
                data["pct_str"],
                class_name="text-sm font-bold ml-4 w-16 text-right",
                style={"color": data["color"]},
            ),
            class_name="flex items-center w-full",
        ),
        class_name="mb-4",
    )


def heatmap_cell(adv: dict, q: str, current_q: str) -> rx.Component:
    return rx.el.td(
        rx.match(
            adv[f"{q}_target"].to(int),
            (0, rx.el.span("—", class_name="text-[#6B7280]")),
            rx.el.div(
                rx.el.span(
                    adv[f"{q}_pct"].to_string() + "%", class_name="font-bold text-white"
                ),
                class_name="w-full h-full flex items-center justify-center rounded-lg",
                style={
                    "backgroundColor": adv[f"{q}_color"].to(str) + "33",
                    "border": rx.cond(
                        q == current_q, "1px solid rgba(255,255,255,0.4)", "none"
                    ),
                },
            ),
        ),
        class_name="p-1 text-center",
    )


def forecast_card(data: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h4(data["name"], class_name="text-sm font-bold text-white truncate"),
            rx.cond(
                data["will_meet"],
                rx.el.span(
                    "On Track",
                    class_name="text-[10px] px-2 py-0.5 bg-[#10B981]/20 text-[#10B981] rounded-full font-bold",
                ),
                rx.el.span(
                    "At Risk",
                    class_name="text-[10px] px-2 py-0.5 bg-[#EF4444]/20 text-[#EF4444] rounded-full font-bold",
                ),
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Current kWh", class_name="text-[10px] text-[#6B7280] uppercase"
                ),
                rx.el.p(
                    data["kwh_cerrados_fmt"], class_name="text-sm font-bold text-white"
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.p("Projected", class_name="text-[10px] text-[#6B7280] uppercase"),
                rx.el.p(
                    data["projected_fmt"], class_name="text-sm font-bold text-[#22D3EE]"
                ),
                class_name="flex-1",
            ),
            class_name="flex gap-4 mb-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    class_name="h-full transition-all duration-500",
                    style={
                        "width": f"{data['forecast_pct']}%",
                        "backgroundColor": rx.cond(
                            data["will_meet"], "#10B981", "#EF4444"
                        ),
                    },
                ),
                class_name="h-1 bg-white/10 rounded-full w-full overflow-hidden",
            ),
            rx.el.p(
                f"Forecast: {data['forecast_pct_str']}",
                class_name="text-[10px] mt-1 text-right text-[#6B7280]",
            ),
        ),
        class_name="bg-white/5 border border-white/10 p-4 rounded-xl backdrop-blur-md hover:bg-white/10 transition-all",
    )


def metas() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Cumplimiento de Metas",
                        class_name="text-4xl font-bold text-white mb-2",
                    ),
                    rx.el.div(
                        rx.el.span(
                            DashboardState.current_quarter_label
                            + " "
                            + DashboardState.current_year.to_string(),
                            class_name="bg-white/10 px-3 py-1 rounded-full text-xs font-bold text-white mr-3",
                        ),
                        rx.el.span(
                            DashboardState.days_remaining_in_quarter.to_string()
                            + " días restantes",
                            class_name="text-sm text-[#9CA3AF] font-medium",
                        ),
                        class_name="flex items-center mt-2",
                    ),
                    class_name="flex-1",
                ),
                rx.el.div(
                    rx.el.svg(
                        rx.el.circle(
                            cx="50",
                            cy="50",
                            r="42",
                            fill="none",
                            stroke="rgba(255,255,255,0.05)",
                            stroke_width="8",
                        ),
                        rx.el.circle(
                            cx="50",
                            cy="50",
                            r="42",
                            fill="none",
                            stroke=DashboardState.overall_pct_q_color,
                            stroke_width="8",
                            stroke_dasharray="263.89",
                            stroke_dashoffset=(
                                263.89 * (1 - DashboardState.kwh_gauge_pct / 100)
                            ).to_string(),
                            stroke_linecap="round",
                            transform="rotate(-90 50 50)",
                            class_name="transition-all duration-1000",
                        ),
                        rx.el.text(
                            DashboardState.overall_pct_q.to_string() + "%",
                            x="50",
                            y="50",
                            text_anchor="middle",
                            dominant_baseline="middle",
                            class_name="text-xl font-black fill-white",
                        ),
                        width="100",
                        height="100",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Team Total",
                            class_name="text-[10px] uppercase text-[#6B7280] text-center",
                        ),
                        rx.el.p(
                            DashboardState.total_kwh_cerrados_q_fmt + " kWh",
                            class_name="text-xs font-bold text-white text-center",
                        ),
                    ),
                    class_name="flex flex-col items-center",
                ),
                class_name="flex justify-between items-center mb-12",
            ),
            rx.el.div(
                rx.el.h2(
                    "Top 5 Asesores (Rendimiento)",
                    class_name="text-xl font-bold text-white mb-6",
                ),
                rx.el.div(
                    rx.foreach(
                        DashboardState.advisor_quota_data,
                        lambda d: rx.cond(
                            d["rank"].to(int) <= 5, radial_gauge(d), rx.fragment()
                        ),
                    ),
                    class_name="grid grid-cols-2 md:grid-cols-5 gap-6 p-8 bg-white/5 border border-white/10 rounded-2xl backdrop-blur-xl shadow-2xl mb-12",
                ),
            ),
            rx.el.div(
                rx.el.h2(
                    "Leaderboard Trimestral",
                    class_name="text-xl font-bold text-white mb-6",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "#",
                                    class_name="px-4 py-3 text-left text-xs font-bold text-gray-400 uppercase",
                                ),
                                rx.el.th(
                                    "Asesor",
                                    class_name="px-4 py-3 text-left text-xs font-bold text-gray-400 uppercase",
                                ),
                                rx.el.th(
                                    "kWh Cerrados",
                                    class_name="px-4 py-3 text-left text-xs font-bold text-gray-400 uppercase",
                                ),
                                rx.el.th(
                                    "Meta Q",
                                    class_name="px-4 py-3 text-left text-xs font-bold text-gray-400 uppercase",
                                ),
                                rx.el.th(
                                    "% Avance",
                                    class_name="px-4 py-3 text-left text-xs font-bold text-gray-400 uppercase",
                                ),
                                rx.el.th(
                                    "Gap",
                                    class_name="px-4 py-3 text-left text-xs font-bold text-gray-400 uppercase",
                                ),
                                rx.el.th(
                                    "Forecast kWh",
                                    class_name="px-4 py-3 text-left text-xs font-bold text-gray-400 uppercase",
                                ),
                                rx.el.th(
                                    "Forecast %",
                                    class_name="px-4 py-3 text-left text-xs font-bold text-gray-400 uppercase",
                                ),
                                rx.el.th(
                                    "Status",
                                    class_name="px-4 py-3 text-left text-xs font-bold text-gray-400 uppercase",
                                ),
                                class_name="bg-white/5",
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                DashboardState.advisor_forecast_data, leaderboard_row
                            )
                        ),
                        class_name="w-full table-auto",
                    ),
                    class_name="bg-white/5 border border-white/10 rounded-2xl shadow-xl overflow-x-auto mb-12",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Distribución de Logros",
                        class_name="text-xl font-bold text-white mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(
                            DashboardState.advisor_quota_data, horizontal_progress_bar
                        ),
                        class_name="p-6 bg-white/5 border border-white/10 rounded-2xl h-full",
                    ),
                    class_name="flex-1",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Quarterly Heatmap",
                        class_name="text-xl font-bold text-white mb-6",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Asesor",
                                        class_name="p-2 text-left text-[10px] text-gray-500 uppercase",
                                    ),
                                    rx.el.th(
                                        "Q1",
                                        class_name="p-2 text-center text-[10px] text-gray-500 uppercase",
                                    ),
                                    rx.el.th(
                                        "Q2",
                                        class_name="p-2 text-center text-[10px] text-gray-500 uppercase",
                                    ),
                                    rx.el.th(
                                        "Q3",
                                        class_name="p-2 text-center text-[10px] text-gray-500 uppercase",
                                    ),
                                    rx.el.th(
                                        "Q4",
                                        class_name="p-2 text-center text-[10px] text-gray-500 uppercase",
                                    ),
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    DashboardState.quarterly_advisor_heatmap,
                                    lambda adv: rx.el.tr(
                                        rx.el.td(
                                            adv["name"],
                                            class_name="p-2 text-xs font-medium text-gray-300 truncate max-w-[120px]",
                                        ),
                                        heatmap_cell(
                                            adv,
                                            "Q1",
                                            DashboardState.current_quarter_label,
                                        ),
                                        heatmap_cell(
                                            adv,
                                            "Q2",
                                            DashboardState.current_quarter_label,
                                        ),
                                        heatmap_cell(
                                            adv,
                                            "Q3",
                                            DashboardState.current_quarter_label,
                                        ),
                                        heatmap_cell(
                                            adv,
                                            "Q4",
                                            DashboardState.current_quarter_label,
                                        ),
                                        class_name="border-b border-white/5",
                                    ),
                                )
                            ),
                            class_name="w-full table-fixed",
                        ),
                        class_name="p-4 bg-white/5 border border-white/10 rounded-2xl",
                    ),
                    class_name="flex-1",
                ),
                class_name="flex flex-col xl:flex-row gap-8 mb-12",
            ),
            rx.el.div(
                rx.el.h2(
                    "Forecast Panel", class_name="text-xl font-bold text-white mb-6"
                ),
                rx.el.div(
                    rx.foreach(DashboardState.advisor_forecast_data, forecast_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4",
                ),
            ),
            class_name="max-w-7xl mx-auto pb-20",
        )
    )