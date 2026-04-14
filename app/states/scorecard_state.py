import reflex as rx
from datetime import datetime, timezone
import logging
import csv
import io
from app.states.dashboard_state import DashboardState, ADVISOR_TARGETS

MONTHS = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]
FIRMADO_STAGES = ["closedwon", "1233929775", "1232935533", "1232929105"]
INACTIVE_STAGES = ["closedlost", "closedwon", "1182079922", "1182079923"]


class ScorecardState(DashboardState):
    sc_month: int = 0
    sc_year: int = 0
    sc_owner_filter: str = "all"
    sc_sort_col: str = "kwh_firmados"
    sc_sort_dir: str = "desc"
    sc_selected_advisor: str = ""
    sc_show_detail: bool = False

    @rx.event
    def sc_set_month(self, m: str):
        self.sc_month = int(m)

    @rx.event
    def sc_set_year(self, y: str):
        self.sc_year = int(y)

    @rx.event
    def sc_set_owner(self, o: str):
        self.sc_owner_filter = o

    @rx.event
    def sc_set_sort(self, col: str):
        if self.sc_sort_col == col:
            self.sc_sort_dir = "asc" if self.sc_sort_dir == "desc" else "desc"
        else:
            self.sc_sort_col = col
            self.sc_sort_dir = "desc"

    @rx.event
    def sc_select_advisor(self, aid: str):
        self.sc_selected_advisor = aid
        self.sc_show_detail = True

    @rx.event
    def sc_close_detail(self):
        self.sc_show_detail = False
        self.sc_selected_advisor = ""

    @rx.var
    def sc_effective_month(self) -> int:
        return self.sc_month if self.sc_month > 0 else datetime.now(timezone.utc).month

    @rx.var
    def sc_effective_year(self) -> int:
        return self.sc_year if self.sc_year > 0 else datetime.now(timezone.utc).year

    @rx.var
    def sc_month_label(self) -> str:
        m = self.sc_effective_month
        y = self.sc_effective_year
        return f"{MONTHS[m - 1]} {y}"

    @rx.var
    def sc_month_options(self) -> list[tuple[str, str]]:
        opts = [("0", "Mes Actual")]
        for i, m in enumerate(MONTHS):
            opts.append((str(i + 1), m))
        return opts

    @rx.var
    def sc_year_options(self) -> list[tuple[str, str]]:
        opts = [("0", "Año Actual")]
        y = datetime.now(timezone.utc).year
        for i in range(y - 2, y + 2):
            opts.append((str(i), str(i)))
        return opts

    @rx.var
    def sc_owner_options(self) -> list[tuple[str, str]]:
        opts = [("all", "Todos los Asesores")]
        for k, v in ADVISOR_TARGETS.items():
            opts.append((k, v["name"]))
        return opts

    @rx.var
    def scorecard_data(self) -> list[dict]:
        month = self.sc_effective_month
        year = self.sc_effective_year
        q = (month - 1) // 3 + 1
        q_key = f"Q{q}"
        now = datetime.now(timezone.utc)
        now_str = now.strftime("%Y-%m-%d %H:%M")

        def _parse(dt_str):
            if not dt_str:
                return None
            try:
                return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
            except:
                logging.exception("Unexpected error")
                return None

        @rx.event
        def is_in_month(dt):
            return dt and dt.year == year and (dt.month == month)

        @rx.event
        def is_in_prev_month(dt):
            pm = month - 1
            py = year
            if pm == 0:
                pm = 12
                py -= 1
            return dt and dt.year == py and (dt.month == pm)

        results = []
        lost_stages = {"closedlost", "1182079923"}
        excluded_from_kwh = set(INACTIVE_STAGES) | set(FIRMADO_STAGES) | lost_stages
        for owner_id, info in ADVISOR_TARGETS.items():
            if self.sc_owner_filter != "all" and owner_id != self.sc_owner_filter:
                continue
            target_q = info.get(q_key, 0)
            target_m = target_q / 3 if target_q > 0 else 0
            kwh_activos = 0.0
            ofertas_count_all_time = 0
            firmados_count_all_time = 0
            ofertas_month = 0
            socios_a = 0
            alertas = 0
            sum_cycle_days = 0
            cycle_count = 0
            kwh_firmados = 0.0
            kwh_firmados_prev = 0.0
            for d in self.deals:
                if d.get("hubspot_owner_id") != owner_id:
                    continue
                st = d.get("dealstage")
                pipe = d.get("pipeline")
                monto_p = d.get("monto_propuesta")
                has_monto = monto_p is not None and monto_p != "0" and (monto_p != 0)
                dt_sol_all = _parse(d.get("solicitud_de_propuesta_historica"))
                dt_car_all = _parse(d.get("carga_propuesta_a_monday_historica"))
                is_oferta = (
                    dt_sol_all is not None or dt_car_all is not None or has_monto
                )
                ventas_stages_after_prop = [
                    "qualifiedtobuy",
                    "1329256222",
                    "contractsent",
                    "1212783978",
                    "1212794259",
                    "closedwon",
                    "1233929775",
                    "1232935533",
                    "1232929105",
                ]
                if (
                    not is_oferta
                    and pipe == "default"
                    and (st in ventas_stages_after_prop)
                ):
                    is_oferta = True
                if is_oferta:
                    ofertas_count_all_time += 1
                if st in FIRMADO_STAGES:
                    firmados_count_all_time += 1
                if st and st not in excluded_from_kwh:
                    k = d.get("capacidad__kwh___clonada_")
                    if k:
                        try:
                            kwh_activos += float(k)
                        except:
                            logging.exception("Unexpected error")
                if pipe == "default":
                    dt_entered_prop = _parse(d.get("hs_v2_date_entered_qualifiedtobuy"))
                    if is_in_month(dt_entered_prop):
                        ofertas_month += 1
                elif pipe == "803674731":
                    dt_entered_conv = _parse(d.get("hs_v2_date_entered_1185807635"))
                    if is_in_month(dt_entered_conv):
                        ofertas_month += 1
                if d.get("tipo_de_socio") == "A (Alto Valor)":
                    socios_a += 1
                cd = _parse(d.get("closedate"))
                if st and st not in excluded_from_kwh and (st != "1212783978"):
                    if d.get("remarketing") != "true":
                        if cd and cd < now:
                            alertas += 1
                cd_close = _parse(d.get("fecha_de_1er_cierre") or d.get("closedate"))
                if st in FIRMADO_STAGES:
                    k = d.get("capacidad__kwh___clonada_")
                    if k:
                        try:
                            kf = float(k)
                            if is_in_month(cd_close):
                                kwh_firmados += kf
                                dt_start = _parse(
                                    d.get("hs_v2_date_entered_1230967589")
                                )
                                dt_end = _parse(d.get("hs_v2_date_entered_closedwon"))
                                if dt_start and dt_end:
                                    days = (dt_end - dt_start).days
                                    sum_cycle_days += days
                                    cycle_count += 1
                            elif is_in_prev_month(cd_close):
                                kwh_firmados_prev += kf
                        except:
                            logging.exception("Unexpected error")
            ciclo = sum_cycle_days / cycle_count if cycle_count > 0 else 0
            conv = (
                firmados_count_all_time / ofertas_count_all_time * 100
                if ofertas_count_all_time > 0
                else 0.0
            )
            cumplimiento = kwh_firmados / target_m * 100 if target_m > 0 else 0
            gap = max(0, target_m - kwh_firmados)
            tendencia = kwh_firmados - kwh_firmados_prev
            color = (
                "#00ff88"
                if cumplimiento >= 100
                else "#ffb703"
                if cumplimiento >= 70
                else "#ff3366"
            )
            results.append(
                {
                    "owner_id": owner_id,
                    "name": info["name"],
                    "kwh_activos": kwh_activos,
                    "kwh_activos_fmt": f"{kwh_activos:,.0f}",
                    "ofertas": ofertas_month,
                    "socios_a": socios_a,
                    "alertas": alertas,
                    "ciclo": round(ciclo),
                    "conversion": round(conv, 1),
                    "kwh_firmados": kwh_firmados,
                    "kwh_firmados_fmt": f"{kwh_firmados:,.0f}",
                    "objetivo": target_m,
                    "objetivo_fmt": f"{target_m:,.0f}",
                    "cumplimiento": cumplimiento,
                    "cumplimiento_fmt": f"{cumplimiento:.1f}%",
                    "gap": gap,
                    "gap_fmt": f"{gap:,.0f}",
                    "tendencia": tendencia,
                    "tendencia_fmt": f"{('+' if tendencia > 0 else '')}{tendencia:,.0f}",
                    "tendencia_is_pos": tendencia >= 0,
                    "updated": now_str,
                    "color": color,
                }
            )
        rev = self.sc_sort_dir == "desc"
        col = self.sc_sort_col
        results.sort(
            key=lambda x: x.get(col, 0)
            if isinstance(x.get(col), (int, float))
            else str(x.get(col, "")),
            reverse=rev,
        )
        return results

    @rx.var
    def sc_detail_deals(self) -> list[dict]:
        if not self.sc_selected_advisor:
            return []
        month = self.sc_effective_month
        year = self.sc_effective_year

        def _parse(dt_str):
            if not dt_str:
                return None
            try:
                return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
            except:
                logging.exception("Unexpected error")
                return None

        res = []
        for d in self.deals:
            if d.get("hubspot_owner_id") == self.sc_selected_advisor:
                dt = _parse(d.get("createdate"))
                if dt and dt.year == year and (dt.month == month):
                    k = d.get("capacidad__kwh___clonada_")
                    m = d.get("amount")
                    res.append(
                        {
                            "dealname": d.get("dealname", "")[:30],
                            "stage": d.get("dealstage", ""),
                            "kwh": f"{float(k):,.0f}" if k else "0",
                            "monto": f"${float(m):,.0f}" if m else "$0",
                            "creado": d.get("createdate", "")[:10],
                            "heredado": "Sí"
                            if d.get("negocio_heredado") == "true"
                            else "No",
                            "rmkt": "Sí" if d.get("remarketing") == "true" else "No",
                        }
                    )
        return res

    @rx.var
    def sc_observations(self) -> list[dict]:
        res = []
        for r in self.scorecard_data:
            owner = r["owner_id"]
            heredados = sum(
                (
                    1
                    for d in self.deals
                    if d.get("hubspot_owner_id") == owner
                    and d.get("negocio_heredado") == "true"
                )
            )
            rmkts = sum(
                (
                    1
                    for d in self.deals
                    if d.get("hubspot_owner_id") == owner
                    and d.get("remarketing") == "true"
                )
            )
            sin_prop = sum(
                (
                    1
                    for d in self.deals
                    if d.get("hubspot_owner_id") == owner
                    and (not d.get("monto_propuesta"))
                )
            )
            if heredados > 0 or rmkts > 0 or sin_prop > 0:
                res.append(
                    {
                        "name": r["name"],
                        "heredados": heredados,
                        "rmkts": rmkts,
                        "sin_prop": sin_prop,
                    }
                )
        return res

    @rx.event
    def download_csv(self):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(
            [
                "Asesor",
                "kWh Activos",
                "Ofertas",
                "Socios A",
                "Alertas",
                "Ciclo",
                "Conversion",
                "kWh Firmados",
                "Objetivo",
                "% Cumplimiento",
                "Gap",
                "Tendencia",
                "Actualizacion",
            ]
        )
        for r in self.scorecard_data:
            writer.writerow(
                [
                    r["name"],
                    r["kwh_activos"],
                    r["ofertas"],
                    r["socios_a"],
                    r["alertas"],
                    r["ciclo"],
                    r["conversion"],
                    r["kwh_firmados"],
                    r["objetivo"],
                    r["cumplimiento_fmt"],
                    r["gap"],
                    r["tendencia"],
                    r["updated"],
                ]
            )
        data = output.getvalue()
        return rx.download(
            data=data,
            filename=f"scorecard_{ScorecardState.sc_effective_month}_{ScorecardState.sc_effective_year}.csv",
        )