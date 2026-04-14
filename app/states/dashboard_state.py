import reflex as rx
from datetime import datetime
from app.services.hubspot_service import fetch_all_deals, fetch_all_owners
import logging

ADVISOR_TARGETS = {
    "83628698": {
        "name": "Edgar Peña",
        "Q1": 7200,
        "Q2": 14880,
        "Q3": 16800,
        "Q4": 21120,
    },
    "83628697": {
        "name": "Brenda Pérez González",
        "Q1": 3600,
        "Q2": 7440,
        "Q3": 8400,
        "Q4": 10560,
    },
    "83628696": {
        "name": "Marvin Salas Lopez",
        "Q1": 3600,
        "Q2": 7440,
        "Q3": 8400,
        "Q4": 10560,
    },
    "83628700": {
        "name": "Antía Nuñez Fernandez",
        "Q1": 4800,
        "Q2": 9920,
        "Q3": 11200,
        "Q4": 14080,
    },
    "85324618": {
        "name": "Pablo Alvarez",
        "Q1": 3600,
        "Q2": 7440,
        "Q3": 8400,
        "Q4": 10560,
    },
    "87210663": {
        "name": "Luis Rey Martínez",
        "Q1": 0,
        "Q2": 8740,
        "Q3": 9700,
        "Q4": 11860,
    },
    "88312805": {
        "name": "Freddy Fierro Hernandez",
        "Q1": 0,
        "Q2": 17180,
        "Q3": 19100,
        "Q4": 23420,
    },
    "88312807": {
        "name": "Giancarlo Nucci",
        "Q1": 0,
        "Q2": 8740,
        "Q3": 9700,
        "Q4": 11860,
    },
    "88312806": {
        "name": "Benjamin Rioja Sandoval",
        "Q1": 0,
        "Q2": 11220,
        "Q3": 12500,
        "Q4": 15380,
    },
    "88605662": {
        "name": "Edwin Yael Gonzalez Estrada",
        "Q1": 0,
        "Q2": 8740,
        "Q3": 9700,
        "Q4": 11860,
    },
    "89447958": {
        "name": "Gustavo Zamora Encarnación",
        "Q1": 0,
        "Q2": 12360,
        "Q3": 13800,
        "Q4": 17040,
    },
    "89068580": {
        "name": "Aurora Morales Catemaxca",
        "Q1": 0,
        "Q2": 6050,
        "Q3": 6530,
        "Q4": 7610,
    },
    "89453816": {
        "name": "Jorge De la Cerda Camargo",
        "Q1": 0,
        "Q2": 14880,
        "Q3": 16800,
        "Q4": 21120,
    },
    "89451791": {
        "name": "Hugo Steven Muñoz Santiesteban",
        "Q1": 0,
        "Q2": 7440,
        "Q3": 8400,
        "Q4": 10560,
    },
}
ANNUAL_KWH_TARGET = 530000


class DashboardState(rx.State):
    deals: list[dict[str, str | None]] = []
    owners: dict[str, str] = {}
    selected_pipeline: str = "all"
    date_range: str = "all"
    selected_owner: str = "all"
    date_preset: str = "all"
    custom_start: str = ""
    custom_end: str = ""
    date_field: str = "createdate"
    active_tab: str = "resumen"
    is_loading: bool = False
    _refresh_running: bool = False
    time_granularity: str = "month"
    hubspot_connected: bool = False
    last_sync_timestamp: str = ""
    last_sync_duration: float = 0.0
    last_sync_deal_count: int = 0
    last_sync_owner_count: int = 0
    last_sync_http_status: int = 0
    last_sync_error: str = ""
    last_sync_endpoint: str = ""
    sync_log: list[dict[str, str]] = []
    search_query: str = ""
    search_history: list[str] = []
    selected_deal_id: str = ""
    show_deal_detail: bool = False

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def open_deal_detail(self, deal_id: str):
        self.selected_deal_id = deal_id
        self.show_deal_detail = True

    @rx.event
    def close_deal_detail(self):
        self.show_deal_detail = False
        self.selected_deal_id = ""

    @rx.event
    def search_and_open(self, deal_id: str):
        if self.search_query and self.search_query not in self.search_history:
            self.search_history = [self.search_query] + self.search_history[:9]
        self.selected_deal_id = deal_id
        self.show_deal_detail = True
        self.search_query = ""

    @rx.event
    def clear_search(self):
        self.search_query = ""

    @rx.var
    def search_results(self) -> list[dict]:
        q = self.search_query.strip().lower()
        if len(q) < 2:
            return []
        results = []
        for d in self.deals:
            dealname = (d.get("dealname") or "").lower()
            owner_id = d.get("hubspot_owner_id") or ""
            owner_name = self.owners.get(owner_id, "").lower()
            socio = (d.get("referido_por_socio") or "").lower()
            pipeline = d.get("pipeline") or ""
            if q in dealname or q in owner_name or q in socio:
                from app.services.hubspot_service import STAGES_VENTAS, STAGES_SOCIOS

                st = d.get("dealstage") or ""
                st_name = (
                    STAGES_VENTAS.get(st, STAGES_SOCIOS.get(st, st))
                    if st
                    else "Sin etapa"
                )
                pipe_name = (
                    "Ventas"
                    if pipeline == "default"
                    else "Socios"
                    if pipeline == "803674731"
                    else pipeline
                )
                results.append(
                    {
                        "deal_id": d.get("dealname", ""),
                        "dealname": d.get("dealname", "Sin Nombre"),
                        "owner": self.owners.get(owner_id, "Sin asignar"),
                        "stage": str(st_name),
                        "pipeline": pipe_name,
                        "kwh": d.get("capacidad__kwh___clonada_") or "0",
                    }
                )
                if len(results) >= 8:
                    break
        return results

    @rx.var
    def deal_detail(self) -> dict[str, str | int | bool | list[dict[str, str | bool]]]:
        if not self.selected_deal_id:
            return {}
        deal = None
        for d in self.deals:
            if d.get("dealname") == self.selected_deal_id:
                deal = d
                break
        if not deal:
            return {}
        from app.services.hubspot_service import STAGES_VENTAS, STAGES_SOCIOS, PIPELINES
        from datetime import datetime, timezone

        owner_id = deal.get("hubspot_owner_id") or ""
        st = deal.get("dealstage") or ""
        pipeline = deal.get("pipeline") or ""
        st_name = (
            STAGES_VENTAS.get(st, STAGES_SOCIOS.get(st, st)) if st else "Sin etapa"
        )
        pipe_name = PIPELINES.get(pipeline, pipeline)
        kwh = deal.get("capacidad__kwh___clonada_")
        kwh_fmt = f"{float(kwh):,.0f}" if kwh else "0"
        amt = deal.get("amount")
        amt_fmt = f"${float(amt):,.2f}" if amt else "$0.00"
        now = datetime.now(timezone.utc)
        entered_current = deal.get("hs_v2_date_entered_current_stage")
        days_in_stage = 0
        if entered_current:
            try:
                dt = datetime.fromisoformat(entered_current.replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                days_in_stage = (now - dt).days
            except:
                logging.exception("Unexpected error")
        close_dt_str = deal.get("closedate")
        is_overdue = False
        if close_dt_str and st not in [
            "closedwon",
            "closedlost",
            "1182079922",
            "1182079923",
            "1233929775",
            "1232935533",
            "1232929105",
        ]:
            try:
                cd = datetime.fromisoformat(close_dt_str.replace("Z", "+00:00"))
                if cd.tzinfo is None:
                    cd = cd.replace(tzinfo=timezone.utc)
                is_overdue = cd < now
            except:
                logging.exception("Unexpected error")
        if pipeline == "default":
            timeline_def = [
                ("hs_v2_date_entered_1230967589", "2.0 Lead Calificado", "#00d4ff"),
                (
                    "hs_v2_date_entered_appointmentscheduled",
                    "2.1 Propuesta solicitada",
                    "#38bdf8",
                ),
                (
                    "hs_v2_date_entered_qualifiedtobuy",
                    "2.2 Propuesta presentada",
                    "#22d3ee",
                ),
                (
                    "hs_v2_date_entered_1329256222",
                    "2.3 Negociación propuesta",
                    "#a78bfa",
                ),
                ("hs_v2_date_entered_contractsent", "2.4 Contrato enviado", "#818cf8"),
                (
                    "hs_v2_date_entered_1212783978",
                    "2.5 Levantamiento Preliminar",
                    "#c084fc",
                ),
                (
                    "hs_v2_date_entered_1212794259",
                    "2.6 Negociación contrato",
                    "#e879f9",
                ),
                ("hs_v2_date_entered_closedwon", "2.7 Firmado cliente", "#00ff88"),
                ("hs_v2_date_entered_1233929775", "2.8 RTP Enviado", "#34d399"),
                ("hs_v2_date_entered_1232935533", "2.9 RTP Aprobado", "#6ee7b7"),
                ("hs_v2_date_entered_1232929105", "2.10 Firmado Quartux", "#10b981"),
                ("hs_v2_date_entered_closedlost", "X Negocio perdido", "#ff3366"),
            ]
        else:
            timeline_def = [
                ("hs_v2_date_entered_1182079917", "Socio interesado", "#fbbf24"),
                ("hs_v2_date_entered_1185807635", "Convenio enviado", "#f59e0b"),
                ("hs_v2_date_entered_1329255962", "Negociación", "#d97706"),
                ("hs_v2_date_entered_1338977193", "Área legal", "#b45309"),
                ("hs_v2_date_entered_1182079922", "Convenio firmado", "#22c55e"),
                ("hs_v2_date_entered_1182079923", "Negocio perdido", "#ff3366"),
            ]
        timeline = []
        prev_dt = None
        for prop, label, color in timeline_def:
            val = deal.get(prop)
            entered = ""
            days_str = ""
            is_current = False
            if val:
                try:
                    dt = datetime.fromisoformat(val.replace("Z", "+00:00"))
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    entered = dt.strftime("%d %b %Y")
                    if prev_dt:
                        days_str = f"{(dt - prev_dt).days}d"
                    prev_dt = dt
                except:
                    logging.exception("Unexpected error")
                    entered = val[:10] if val else ""
            stage_id_from_prop = prop.replace("hs_v2_date_entered_", "")
            is_current = stage_id_from_prop == st
            timeline.append(
                {
                    "label": label,
                    "entered": entered,
                    "days": days_str,
                    "color": color,
                    "active": bool(val),
                    "is_current": is_current,
                }
            )
        return {
            "dealname": deal.get("dealname", "Sin Nombre"),
            "owner": self.owners.get(owner_id, "Sin asignar"),
            "owner_id": owner_id,
            "pipeline": pipe_name,
            "stage": str(st_name),
            "amount": amt_fmt,
            "kwh": kwh_fmt,
            "created": (deal.get("createdate") or "")[:10],
            "close_date": (deal.get("closedate") or "")[:10],
            "first_close": (deal.get("fecha_de_1er_cierre") or "")[:10],
            "days_in_stage": days_in_stage,
            "is_overdue": is_overdue,
            "socio": deal.get("referido_por_socio") or "—",
            "heredado": "Sí" if deal.get("negocio_heredado") == "true" else "No",
            "rmkt": "Sí" if deal.get("remarketing") == "true" else "No",
            "potencia": deal.get("potencia__kw___clonada_") or "—",
            "timeline": timeline,
        }

    @rx.event
    def set_time_granularity(self, val: str):
        self.time_granularity = val

    @rx.event(background=True)
    async def load_data(self):
        async with self:
            self.is_loading = True
        from datetime import datetime, timezone
        from app.services.hubspot_service import (
            fetch_all_deals_with_meta,
            fetch_all_owners_with_meta,
        )

        deals_result = fetch_all_deals_with_meta()
        owners_result = fetch_all_owners_with_meta()
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        async with self:
            self.deals = deals_result["deals"]
            self.owners = owners_result.get("owners", {})
            self.is_loading = False
            self.hubspot_connected = deals_result["status"] == "success"
            self.last_sync_timestamp = now_str
            self.last_sync_duration = deals_result["duration_sec"]
            self.last_sync_deal_count = deals_result["count"]
            self.last_sync_owner_count = owners_result.get("count", 0)
            self.last_sync_http_status = deals_result["http_status"]
            self.last_sync_error = deals_result["error_msg"]
            self.last_sync_endpoint = deals_result["endpoint"]
            log_entry = {
                "timestamp": now_str,
                "status": deals_result["status"],
                "deals": str(deals_result["count"]),
                "owners": str(owners_result.get("count", 0)),
                "duration": f"{deals_result['duration_sec']}s",
                "http_status": str(deals_result["http_status"]),
                "error": deals_result["error_msg"][:100]
                if deals_result["error_msg"]
                else "",
            }
            self.sync_log = [log_entry] + self.sync_log[:49]
        yield DashboardState.auto_refresh

    @rx.event(background=True)
    async def auto_refresh(self):
        async with self:
            if self._refresh_running:
                return
            self._refresh_running = True
        import asyncio
        from datetime import datetime, timezone
        from app.services.hubspot_service import (
            fetch_all_deals_with_meta,
            fetch_all_owners_with_meta,
        )

        while True:
            await asyncio.sleep(900)
            deals_result = fetch_all_deals_with_meta()
            owners_result = fetch_all_owners_with_meta()
            now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            async with self:
                self.deals = deals_result["deals"]
                self.owners = owners_result.get("owners", {})
                self.hubspot_connected = deals_result["status"] == "success"
                self.last_sync_timestamp = now_str
                self.last_sync_duration = deals_result["duration_sec"]
                self.last_sync_deal_count = deals_result["count"]
                self.last_sync_owner_count = owners_result.get("count", 0)
                self.last_sync_http_status = deals_result["http_status"]
                self.last_sync_error = deals_result["error_msg"]
                self.last_sync_endpoint = deals_result["endpoint"]
                log_entry = {
                    "timestamp": now_str,
                    "status": deals_result["status"],
                    "deals": str(deals_result["count"]),
                    "owners": str(owners_result.get("count", 0)),
                    "duration": f"{deals_result['duration_sec']}s",
                    "http_status": str(deals_result["http_status"]),
                    "error": deals_result["error_msg"][:100]
                    if deals_result["error_msg"]
                    else "",
                }
                self.sync_log = [log_entry] + self.sync_log[:49]

    @rx.event
    def manual_refresh(self):
        yield DashboardState.load_data

    @rx.event
    def set_pipeline(self, pipeline: str):
        self.selected_pipeline = pipeline

    @rx.event
    def set_owner(self, owner: str):
        self.selected_owner = owner

    @rx.event
    def set_date_preset(self, preset: str):
        self.date_preset = preset

    @rx.event
    def set_custom_start(self, val: str):
        self.custom_start = val
        if val:
            self.date_preset = "custom"

    @rx.event
    def set_custom_end(self, val: str):
        self.custom_end = val
        if val:
            self.date_preset = "custom"

    @rx.event
    def set_date_field(self, field: str):
        self.date_field = field

    def _get_global_date_range(self) -> tuple[datetime | None, datetime | None]:
        from datetime import datetime, timezone, timedelta

        now = datetime.now(timezone.utc)
        if self.date_preset == "all":
            return (None, None)
        elif self.date_preset == "today":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            return (start, now)
        elif self.date_preset == "7d":
            return (now - timedelta(days=7), now)
        elif self.date_preset == "this_week":
            start = (now - timedelta(days=now.weekday())).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            return (start, now)
        elif self.date_preset == "last_week":
            end = (now - timedelta(days=now.weekday() + 1)).replace(
                hour=23, minute=59, second=59
            )
            start = (end - timedelta(days=6)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            return (start, end)
        elif self.date_preset == "this_month":
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            return (start, now)
        elif self.date_preset == "last_month":
            end = (now.replace(day=1) - timedelta(days=1)).replace(
                hour=23, minute=59, second=59
            )
            start = end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            return (start, end)
        elif self.date_preset == "this_quarter":
            q = (now.month - 1) // 3
            start = now.replace(
                month=q * 3 + 1, day=1, hour=0, minute=0, second=0, microsecond=0
            )
            return (start, now)
        elif self.date_preset == "last_quarter":
            q = (now.month - 1) // 3
            if q == 0:
                start = now.replace(
                    year=now.year - 1,
                    month=10,
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
                end = now.replace(
                    year=now.year - 1, month=12, day=31, hour=23, minute=59, second=59
                )
            else:
                start = now.replace(
                    month=(q - 1) * 3 + 1,
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
                end_month = q * 3
                import calendar

                end_day = calendar.monthrange(now.year, end_month)[1]
                end = now.replace(
                    month=end_month, day=end_day, hour=23, minute=59, second=59
                )
            return (start, end)
        elif self.date_preset == "6m":
            return (now - timedelta(days=180), now)
        elif self.date_preset in ["ytd", "this_year"]:
            start = now.replace(
                month=1, day=1, hour=0, minute=0, second=0, microsecond=0
            )
            return (start, now)
        elif self.date_preset == "12m":
            return (now - timedelta(days=365), now)
        elif self.date_preset == "last_year":
            start = now.replace(
                year=now.year - 1,
                month=1,
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
            end = now.replace(
                year=now.year - 1, month=12, day=31, hour=23, minute=59, second=59
            )
            return (start, end)
        elif self.date_preset == "custom" and self.custom_start and self.custom_end:
            try:
                start = datetime.fromisoformat(self.custom_start).replace(
                    tzinfo=timezone.utc
                )
                end = datetime.fromisoformat(self.custom_end).replace(
                    hour=23, minute=59, second=59, tzinfo=timezone.utc
                )
                return (start, end)
            except:
                logging.exception("Unexpected error")
        return (None, None)

    @rx.var
    def active_date_label(self) -> str:
        labels = {
            "all": "Todo",
            "today": "Hoy",
            "7d": "7 días",
            "this_week": "Semana",
            "last_week": "Sem. Ant.",
            "this_month": "Mes",
            "last_month": "Mes Ant.",
            "this_quarter": "Quarter",
            "last_quarter": "Q Ant.",
            "6m": "6 Meses",
            "ytd": "YTD",
            "12m": "12 Meses",
            "this_year": "Año",
            "last_year": "Año Ant.",
        }
        if self.date_preset == "custom":
            return f"{self.custom_start} → {self.custom_end}"
        return labels.get(self.date_preset, "Todo")

    @rx.var
    def date_field_label(self) -> str:
        labels = {
            "createdate": "Fecha de creación",
            "closedate": "Fecha de cierre",
            "fecha_de_1er_cierre": "Fecha 1er cierre",
            "hs_lastmodifieddate": "Última actividad",
        }
        return labels.get(self.date_field, "Fecha")

    @rx.var
    def filtered_deals(self) -> list[dict[str, str | None]]:
        filtered = self.deals
        if self.selected_pipeline != "all":
            filtered = [
                d for d in filtered if d.get("pipeline") == self.selected_pipeline
            ]
        if self.selected_owner != "all":
            filtered = [
                d for d in filtered if d.get("hubspot_owner_id") == self.selected_owner
            ]
        from datetime import datetime, timezone

        start, end = self._get_global_date_range()
        if start and end:
            date_filtered = []
            for d in filtered:
                dt_str = d.get(self.date_field)
                if dt_str:
                    try:
                        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                        if start <= dt <= end:
                            date_filtered.append(d)
                    except:
                        logging.exception("Unexpected error")
            filtered = date_filtered
        return filtered

    @rx.var
    def total_deals(self) -> int:
        return len(self.filtered_deals)

    @rx.var
    def active_deals(self) -> int:
        count = 0
        for d in self.filtered_deals:
            stage = d.get("dealstage")
            pipe = d.get("pipeline")
            if pipe == "default":
                if stage not in ["closedlost", "closedwon"]:
                    count += 1
            elif pipe == "803674731":
                if stage != "1182079923":
                    count += 1
        return count

    @rx.var
    def active_deals_percent(self) -> str:
        if not self.total_deals:
            return "0%"
        return f"{self.active_deals / self.total_deals * 100:.1f}%"

    @rx.var
    def convenio_firmado(self) -> int:
        count = 0
        for d in self.filtered_deals:
            stage = d.get("dealstage")
            if stage in ["closedwon", "1182079922"]:
                count += 1
        return count

    @rx.var
    def convenio_firmado_percent(self) -> str:
        if not self.total_deals:
            return "0%"
        return f"{self.convenio_firmado / self.total_deals * 100:.1f}%"

    @rx.var
    def cerrados_perdidos(self) -> int:
        count = 0
        for d in self.filtered_deals:
            stage = d.get("dealstage")
            if stage in ["closedlost", "1182079923"]:
                count += 1
        return count

    @rx.var
    def cerrados_perdidos_percent(self) -> str:
        if not self.total_deals:
            return "0%"
        return f"{self.cerrados_perdidos / self.total_deals * 100:.1f}%"

    @rx.var
    def total_kwh(self) -> str:
        total = 0.0
        for d in self.filtered_deals:
            val = d.get("capacidad__kwh___clonada_")
            if val:
                try:
                    total += float(val)
                except ValueError:
                    pass
        return f"{total:,.0f}"

    def _format_compact_currency(self, value: float) -> str:
        if value >= 1000000000:
            return f"${value / 1000000000:.1f}B"
        elif value >= 1000000:
            return f"${value / 1000000:.1f}M"
        elif value >= 1000:
            return f"${value / 1000:.1f}K"
        else:
            return f"${value:,.0f}"

    @rx.var
    def total_usd(self) -> str:
        total = 0.0
        for d in self.filtered_deals:
            val = d.get("amount")
            if val:
                try:
                    total += float(val)
                except ValueError:
                    pass
        return self._format_compact_currency(total)

    @rx.var
    def propuestas_enviadas(self) -> int:
        count = 0
        for d in self.filtered_deals:
            stage = d.get("dealstage")
            monto = d.get("monto_propuesta")
            if stage == "qualifiedtobuy" or (monto and monto != "0"):
                count += 1
        return count

    @rx.var
    def avg_sales_cycle_days(self) -> str:
        total_days = 0
        count = 0
        for d in self.filtered_deals:
            stage = d.get("dealstage")
            created = d.get("createdate")
            closed = d.get("closedate")
            if stage in ["closedwon", "1182079922"] and created and closed:
                try:
                    c_date = datetime.fromisoformat(created.replace("Z", "+00:00"))
                    cl_date = datetime.fromisoformat(closed.replace("Z", "+00:00"))
                    total_days += (cl_date - c_date).days
                    count += 1
                except Exception:
                    logging.exception("Unexpected error")
        if count == 0:
            return "0"
        return str(total_days // count)

    @rx.var
    def owner_options(self) -> list[tuple[str, str]]:
        opts = [("all", "Todos los Asesores")]
        for k, v in self.owners.items():
            opts.append((k, v))
        return opts

    sort_column: str = "total"
    sort_direction: str = "desc"
    selected_advisor: str = ""
    show_advisor_modal: bool = False

    @rx.event
    def set_sort(self, column: str):
        if self.sort_column == column:
            self.sort_direction = "asc" if self.sort_direction == "desc" else "desc"
        else:
            self.sort_column = column
            self.sort_direction = "desc"

    @rx.event
    def select_advisor(self, owner_id: str):
        self.selected_advisor = owner_id
        self.show_advisor_modal = True

    @rx.event
    def close_modal(self):
        self.show_advisor_modal = False
        self.selected_advisor = ""

    @rx.var
    def pipeline_ventas_funnel(self) -> list[dict[str, str | int]]:
        from app.services.hubspot_service import STAGES_VENTAS

        stages_order = [
            "1230967589",
            "appointmentscheduled",
            "qualifiedtobuy",
            "1329256222",
            "contractsent",
            "1212783978",
            "1212794259",
            "closedwon",
            "1233929775",
            "1232935533",
            "1232929105",
            "closedlost",
        ]
        counts = {s: 0 for s in stages_order}
        total = 0
        for d in self.filtered_deals:
            if d.get("pipeline") == "default":
                st = d.get("dealstage")
                if st in counts:
                    counts[st] += 1
                    total += 1
        result = []
        for st in stages_order:
            c = counts[st]
            pct = f"{c / total * 100:.1f}%" if total > 0 else "0%"
            result.append(
                {
                    "stage_name": STAGES_VENTAS.get(st, st),
                    "count": c,
                    "percentage": pct,
                    "raw_pct": c / total * 100 if total > 0 else 0,
                }
            )
        return result

    @rx.var
    def current_quarter(self) -> int:
        from datetime import datetime, timezone

        return (datetime.now(timezone.utc).month - 1) // 3 + 1

    @rx.var
    def current_quarter_label(self) -> str:
        return f"Q{self.current_quarter}"

    @rx.var
    def current_year(self) -> int:
        from datetime import datetime, timezone

        return datetime.now(timezone.utc).year

    @rx.var
    def advisor_quota_data(self) -> list[dict]:
        """For each advisor in ADVISOR_TARGETS, compute kWh closed in current Q using fecha_de_1er_cierre (fallback closedate)."""
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        current_q = (now.month - 1) // 3 + 1
        current_year = now.year
        q_key = f"Q{current_q}"
        q_start_month = (current_q - 1) * 3 + 1
        q_start = datetime(current_year, q_start_month, 1, tzinfo=timezone.utc)
        if current_q == 4:
            q_end = datetime(current_year + 1, 1, 1, tzinfo=timezone.utc)
        else:
            q_end = datetime(current_year, q_start_month + 3, 1, tzinfo=timezone.utc)
        results = []
        for owner_id, info in ADVISOR_TARGETS.items():
            target = info.get(q_key, 0)
            kwh_closed = 0.0
            for d in self.deals:
                if d.get("hubspot_owner_id") != owner_id:
                    continue
                stage = d.get("dealstage")
                if stage not in ["closedwon", "1182079922"]:
                    continue
                date_str = d.get("fecha_de_1er_cierre") or d.get("closedate")
                if not date_str:
                    continue
                try:
                    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                except Exception:
                    logging.exception("Unexpected error")
                    continue
                if q_start <= dt < q_end:
                    kwh_val = d.get("capacidad__kwh___clonada_")
                    if kwh_val:
                        try:
                            kwh_closed += float(kwh_val)
                        except Exception:
                            logging.exception("Unexpected error")
            pct = kwh_closed / target * 100 if target > 0 else 0
            gap = max(0, target - kwh_closed)
            if pct >= 100:
                color = "#00ff88"
            elif pct >= 70:
                color = "#ffb703"
            else:
                color = "#ff3366"
            results.append(
                {
                    "owner_id": owner_id,
                    "name": info["name"],
                    "kwh_cerrados": round(kwh_closed),
                    "kwh_cerrados_fmt": f"{kwh_closed:,.0f}",
                    "target_q": target,
                    "target_q_fmt": f"{target:,.0f}",
                    "pct": round(pct, 1),
                    "pct_str": f"{pct:.1f}%",
                    "gap": round(gap),
                    "gap_fmt": f"{gap:,.0f}",
                    "color": color,
                    "bar_pct": min(100.0, pct),
                }
            )
        results.sort(key=lambda x: x["pct"], reverse=True)
        for i, r in enumerate(results):
            r["rank"] = i + 1
        return results

    @rx.var
    def total_kwh_cerrados_q(self) -> float:
        return float(sum((a["kwh_cerrados"] for a in self.advisor_quota_data)))

    @rx.var
    def total_kwh_cerrados_q_fmt(self) -> str:
        v = self.total_kwh_cerrados_q
        return f"{v:,.0f}"

    @rx.var
    def total_target_q(self) -> float:
        return float(sum((a["target_q"] for a in self.advisor_quota_data)))

    @rx.var
    def total_target_q_fmt(self) -> str:
        v = self.total_target_q
        return f"{v:,.0f}"

    @rx.var
    def overall_pct_q(self) -> float:
        total_target = self.total_target_q
        if total_target == 0:
            return 0.0
        return round(self.total_kwh_cerrados_q / total_target * 100, 1)

    @rx.var
    def overall_pct_q_color(self) -> str:
        p = self.overall_pct_q
        if p >= 100:
            return "#00ff88"
        elif p >= 70:
            return "#ffb703"
        return "#ff3366"

    @rx.var
    def days_remaining_in_quarter(self) -> int:
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        q = (now.month - 1) // 3 + 1
        if q == 4:
            q_end = datetime(now.year + 1, 1, 1, tzinfo=timezone.utc)
        else:
            q_end = datetime(now.year, q * 3 + 1, 1, tzinfo=timezone.utc)
        return (q_end - now).days

    @rx.var
    def days_elapsed_in_quarter(self) -> int:
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        q = (now.month - 1) // 3 + 1
        q_start_month = (q - 1) * 3 + 1
        q_start = datetime(now.year, q_start_month, 1, tzinfo=timezone.utc)
        return (now - q_start).days

    @rx.var
    def usd_deals_with_amount_pct(self) -> str:
        """% of filtered deals that have an amount value."""
        total = len(self.filtered_deals)
        if total == 0:
            return "0%"
        with_amount = sum(
            (
                1
                for d in self.filtered_deals
                if d.get("amount") and d.get("amount") != "0"
            )
        )
        return f"{with_amount / total * 100:.0f}% con valor asignado"

    @rx.var
    def quarterly_advisor_heatmap(self) -> list[dict]:
        """For each advisor, compute kWh closed and % per quarter Q1-Q4 of current year."""
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        current_year = now.year
        results = []
        for owner_id, info in ADVISOR_TARGETS.items():
            row = {"name": info["name"], "owner_id": owner_id}
            for q in range(1, 5):
                q_key = f"Q{q}"
                q_start_month = (q - 1) * 3 + 1
                q_start = datetime(current_year, q_start_month, 1, tzinfo=timezone.utc)
                if q == 4:
                    q_end = datetime(current_year + 1, 1, 1, tzinfo=timezone.utc)
                else:
                    q_end = datetime(
                        current_year, q_start_month + 3, 1, tzinfo=timezone.utc
                    )
                target = info.get(q_key, 0)
                kwh_closed = 0.0
                for d in self.deals:
                    if d.get("hubspot_owner_id") != owner_id:
                        continue
                    stage = d.get("dealstage")
                    if stage not in ["closedwon", "1182079922"]:
                        continue
                    date_str = d.get("fecha_de_1er_cierre") or d.get("closedate")
                    if not date_str:
                        continue
                    try:
                        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                    except Exception:
                        logging.exception("Unexpected error")
                        continue
                    if q_start <= dt < q_end:
                        kwh_val = d.get("capacidad__kwh___clonada_")
                        if kwh_val:
                            try:
                                kwh_closed += float(kwh_val)
                            except Exception:
                                logging.exception("Unexpected error")
                pct = kwh_closed / target * 100 if target > 0 else 0.0
                row[f"{q_key}_kwh"] = round(kwh_closed)
                row[f"{q_key}_target"] = target
                row[f"{q_key}_pct"] = round(pct, 1)
                if target == 0:
                    row[f"{q_key}_color"] = "#374151"
                elif pct >= 100:
                    row[f"{q_key}_color"] = "#00ff88"
                elif pct >= 70:
                    row[f"{q_key}_color"] = "#ffb703"
                else:
                    row[f"{q_key}_color"] = "#ff3366"
            results.append(row)
        return results

    @rx.var
    def advisor_forecast_data(self) -> list[dict]:
        """Forecast projected kWh at end of quarter based on current run rate."""
        elapsed = self.days_elapsed_in_quarter
        remaining = self.days_remaining_in_quarter
        total_days = elapsed + remaining
        results = []
        for a in self.advisor_quota_data:
            if elapsed > 0:
                daily_rate = a["kwh_cerrados"] / elapsed
                projected = daily_rate * total_days
            else:
                projected = 0.0
            target = a["target_q"]
            forecast_pct = projected / target * 100 if target > 0 else 0
            will_meet = projected >= target
            results.append(
                {
                    "name": a["name"],
                    "kwh_cerrados": a["kwh_cerrados"],
                    "kwh_cerrados_fmt": a["kwh_cerrados_fmt"],
                    "target_q": a["target_q"],
                    "target_q_fmt": a["target_q_fmt"],
                    "projected": round(projected),
                    "projected_fmt": f"{projected:,.0f}",
                    "forecast_pct": round(forecast_pct, 1),
                    "forecast_pct_str": f"{forecast_pct:.1f}%",
                    "will_meet": will_meet,
                    "pct": a["pct"],
                    "pct_str": a["pct_str"],
                    "gap_fmt": a["gap_fmt"],
                    "color": a["color"],
                    "rank": a["rank"],
                }
            )
        return results

    @rx.var
    def kwh_gauge_pct(self) -> float:
        return min(100.0, max(0.0, self.overall_pct_q))

    @rx.var
    def kwh_activos(self) -> float:
        total = 0.0
        for d in self.filtered_deals:
            stage = d.get("dealstage")
            if stage not in ["closedlost", "closedwon", "1182079923", "1182079922"]:
                val = d.get("capacidad__kwh___clonada_")
                if val:
                    try:
                        total += float(val)
                    except:
                        logging.exception("Unexpected error")
        return total

    @rx.var
    def kwh_cerrados(self) -> float:
        total = 0.0
        for d in self.filtered_deals:
            stage = d.get("dealstage")
            if stage in ["closedwon", "1182079922"]:
                val = d.get("capacidad__kwh___clonada_")
                if val:
                    try:
                        total += float(val)
                    except:
                        logging.exception("Unexpected error")
        return total

    @rx.var
    def kwh_perdidos(self) -> float:
        total = 0.0
        for d in self.filtered_deals:
            stage = d.get("dealstage")
            if stage in ["closedlost", "1182079923"]:
                val = d.get("capacidad__kwh___clonada_")
                if val:
                    try:
                        total += float(val)
                    except:
                        logging.exception("Unexpected error")
        return total

    @rx.var
    def pipeline_ventas_bar_data(self) -> list[dict]:
        from app.services.hubspot_service import STAGES_VENTAS

        stages_order = [
            "1230967589",
            "appointmentscheduled",
            "qualifiedtobuy",
            "1329256222",
            "contractsent",
            "1212783978",
            "1212794259",
            "closedwon",
            "1233929775",
            "1232935533",
            "1232929105",
            "closedlost",
        ]
        counts = {s: {"count": 0, "kwh": 0.0, "usd": 0.0} for s in stages_order}
        total = 0
        for d in self.filtered_deals:
            if d.get("pipeline") == "default":
                st = d.get("dealstage")
                if st in counts:
                    counts[st]["count"] += 1
                    kwh_val = d.get("capacidad__kwh___clonada_")
                    if kwh_val:
                        try:
                            counts[st]["kwh"] += float(kwh_val)
                        except:
                            logging.exception("Unexpected error")
                    usd_val = d.get("amount")
                    if usd_val:
                        try:
                            counts[st]["usd"] += float(usd_val)
                        except:
                            logging.exception("Unexpected error")
                    total += 1
        result = []
        for st in reversed(stages_order):
            c = counts[st]
            pct = c["count"] / total * 100 if total > 0 else 0
            result.append(
                {
                    "stage_name": STAGES_VENTAS.get(st, st),
                    "count": c["count"],
                    "pct_str": f"{pct:.1f}%",
                    "kwh_fmt": f"{c['kwh']:,.0f}",
                    "usd_fmt": self._format_compact_currency(c["usd"]),
                    "fill": "#00d4ff",
                }
            )
        return result

    @rx.var
    def pipeline_socios_bar_data(self) -> list[dict]:
        from app.services.hubspot_service import STAGES_SOCIOS

        stages_order = [
            "1182079917",
            "1185807635",
            "1329255962",
            "1338977193",
            "1182079922",
            "1182079923",
        ]
        counts = {s: {"count": 0, "kwh": 0.0, "usd": 0.0} for s in stages_order}
        total = 0
        for d in self.filtered_deals:
            if d.get("pipeline") == "803674731":
                st = d.get("dealstage")
                if st in counts:
                    counts[st]["count"] += 1
                    kwh_val = d.get("capacidad__kwh___clonada_")
                    if kwh_val:
                        try:
                            counts[st]["kwh"] += float(kwh_val)
                        except:
                            logging.exception("Unexpected error")
                    usd_val = d.get("amount")
                    if usd_val:
                        try:
                            counts[st]["usd"] += float(usd_val)
                        except:
                            logging.exception("Unexpected error")
                    total += 1
        result = []
        for st in reversed(stages_order):
            c = counts[st]
            pct = c["count"] / total * 100 if total > 0 else 0
            result.append(
                {
                    "stage_name": STAGES_SOCIOS.get(st, st),
                    "count": c["count"],
                    "pct_str": f"{pct:.1f}%",
                    "kwh_fmt": f"{c['kwh']:,.0f}",
                    "usd_fmt": self._format_compact_currency(c["usd"]),
                    "fill": "#00ff88",
                }
            )
        return result

    @rx.var
    def pipeline_monthly_trend(self) -> list[dict]:
        from datetime import datetime, timezone, timedelta

        dates = []
        for d in self.filtered_deals:
            dt = self._parse_date(d.get("createdate"))
            if dt:
                dates.append(dt)
        if not dates:
            now = datetime.now(timezone.utc)
            months = []
            for i in range(11, -1, -1):
                dt = (now.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
                months.append(dt.strftime("%Y-%m"))
            months = sorted(list(set(months)))[-12:]
        else:
            min_date = min(dates)
            max_date = max(dates)
            months = []
            current = min_date.replace(day=1)
            while current <= max_date:
                months.append(current.strftime("%Y-%m"))
                if current.month == 12:
                    current = current.replace(year=current.year + 1, month=1)
                else:
                    current = current.replace(month=current.month + 1)
            months = months[-18:]
        data = {m: {"month": m, "Ventas": 0, "Socios": 0} for m in months}
        for d in self.filtered_deals:
            dt = self._parse_date(d.get("createdate"))
            if dt:
                m = dt.strftime("%Y-%m")
                if m in data:
                    pipe = d.get("pipeline")
                    if pipe == "default":
                        data[m]["Ventas"] += 1
                    elif pipe == "803674731":
                        data[m]["Socios"] += 1
        return [data[m] for m in months]

    @rx.var
    def pipeline_scatter_ventas(self) -> list[dict]:
        result = []
        for d in self.filtered_deals:
            if d.get("pipeline") == "default":
                kwh = d.get("capacidad__kwh___clonada_")
                amt = d.get("amount")
                if kwh and amt:
                    try:
                        if float(kwh) > 0 and float(amt) > 0:
                            result.append(
                                {
                                    "kwh": round(float(kwh)),
                                    "amount": round(float(amt)),
                                    "name": d.get("dealname", "")[:30],
                                }
                            )
                    except:
                        logging.exception("Unexpected error")
        return result[:100]

    @rx.var
    def pipeline_scatter_socios(self) -> list[dict]:
        result = []
        for d in self.filtered_deals:
            if d.get("pipeline") == "803674731":
                kwh = d.get("capacidad__kwh___clonada_")
                amt = d.get("amount")
                if kwh and amt:
                    try:
                        if float(kwh) > 0 and float(amt) > 0:
                            result.append(
                                {
                                    "kwh": round(float(kwh)),
                                    "amount": round(float(amt)),
                                    "name": d.get("dealname", "")[:30],
                                }
                            )
                    except:
                        logging.exception("Unexpected error")
        return result[:100]

    @rx.var
    def status_pie_data(self) -> list[dict]:
        dist = self.status_distribution
        mapping = {
            "Negociación": "#ffb703",
            "Convenio Enviado": "#00d4ff",
            "Convenio Firmado": "#00ff88",
            "Socio Interesado": "#a78bfa",
            "Propuesta Enviada": "#00d4ff",
            "Cerrado Perdido": "#ff3366",
            "Sin Etapa": "#6b7280",
        }
        res = []
        for k, color in mapping.items():
            val = dist.get(k, 0)
            if val > 0:
                res.append({"name": k, "value": val, "fill": color})
        return res

    @rx.var
    def pipeline_socios_funnel(self) -> list[dict[str, str | int]]:
        from app.services.hubspot_service import STAGES_SOCIOS

        stages_order = [
            "1182079917",
            "1185807635",
            "1329255962",
            "1338977193",
            "1182079922",
            "1182079923",
        ]
        counts = {s: 0 for s in stages_order}
        total = 0
        for d in self.filtered_deals:
            if d.get("pipeline") == "803674731":
                st = d.get("dealstage")
                if st in counts:
                    counts[st] += 1
                    total += 1
        result = []
        for st in stages_order:
            c = counts[st]
            pct = f"{c / total * 100:.1f}%" if total > 0 else "0%"
            result.append(
                {
                    "stage_name": STAGES_SOCIOS.get(st, st),
                    "count": c,
                    "percentage": pct,
                    "raw_pct": c / total * 100 if total > 0 else 0,
                }
            )
        return result

    @rx.var
    def active_deals_funnel(self) -> list[dict[str, str | int]]:
        from app.services.hubspot_service import STAGES_VENTAS, STAGES_SOCIOS

        counts = {}
        total = 0
        for d in self.filtered_deals:
            st = d.get("dealstage")
            if st not in ["closedlost", "closedwon", "1182079923", "1182079922", None]:
                counts[st] = counts.get(st, 0) + 1
                total += 1
        result = []
        for st, c in sorted(counts.items(), key=lambda item: item[1], reverse=True):
            name = STAGES_VENTAS.get(st, STAGES_SOCIOS.get(st, st))
            pct = f"{c / total * 100:.1f}%" if total > 0 else "0%"
            result.append(
                {
                    "stage_name": name,
                    "count": c,
                    "percentage": pct,
                    "raw_pct": c / total * 100 if total > 0 else 0,
                }
            )
        return result

    @rx.var
    def status_distribution(self) -> dict[str, str | int]:
        counts = {
            "Negociación": 0,
            "Convenio Enviado": 0,
            "Convenio Firmado": 0,
            "Socio Interesado": 0,
            "Propuesta Enviada": 0,
            "Cerrado Perdido": 0,
            "Sin Etapa": 0,
        }
        total = len(self.filtered_deals)
        for d in self.filtered_deals:
            st = d.get("dealstage")
            if st in ["1329256222", "1329255962", "1212794259"]:
                counts["Negociación"] += 1
            elif st == "1185807635":
                counts["Convenio Enviado"] += 1
            elif st in ["1182079922", "closedwon"]:
                counts["Convenio Firmado"] += 1
            elif st == "1182079917":
                counts["Socio Interesado"] += 1
            elif st == "qualifiedtobuy":
                counts["Propuesta Enviada"] += 1
            elif st in ["closedlost", "1182079923"]:
                counts["Cerrado Perdido"] += 1
            elif not st:
                counts["Sin Etapa"] += 1
        for k in list(counts.keys()):
            counts[f"{k}_pct"] = (
                f"{counts[k] / total * 100:.1f}%" if total > 0 else "0%"
            )
        return counts

    @rx.var
    def advisor_stats(self) -> list[dict[str, str | int | float]]:
        stats = {}
        for d in self.filtered_deals:
            owner_id = d.get("hubspot_owner_id")
            if not owner_id:
                continue
            if owner_id not in stats:
                stats[owner_id] = {
                    "owner_id": owner_id,
                    "name": self.owners.get(owner_id, "Desconocido"),
                    "total": 0,
                    "active": 0,
                    "convenio": 0,
                    "perdidos": 0,
                    "kwh": 0.0,
                    "usd": 0.0,
                    "proposals": 0,
                    "activities": 0,
                    "kwh_activos": 0.0,
                    "kwh_cerrados": 0.0,
                    "sum_days": 0.0,
                    "days_count": 0,
                }
            s = stats[owner_id]
            s["total"] += 1
            st = d.get("dealstage")
            kwh_val = d.get("capacidad__kwh___clonada_")
            kwh_float = 0.0
            if kwh_val:
                try:
                    kwh_float = float(kwh_val)
                    s["kwh"] += kwh_float
                except:
                    logging.exception("Unexpected error")
            if st in ["closedwon", "1182079922"]:
                s["convenio"] += 1
                s["kwh_cerrados"] += kwh_float
            elif st in ["closedlost", "1182079923"]:
                s["perdidos"] += 1
            else:
                s["active"] += 1
                s["kwh_activos"] += kwh_float
            usd_val = d.get("amount")
            if usd_val:
                try:
                    s["usd"] += float(usd_val)
                except:
                    logging.exception("Unexpected error")
            mp = d.get("monto_propuesta")
            if mp and mp != "0":
                s["proposals"] += 1
            nn = d.get("num_notes")
            if nn:
                try:
                    s["activities"] += int(float(nn))
                except:
                    logging.exception("Unexpected error")
            days = d.get("days_to_close")
            if days:
                try:
                    s["sum_days"] += float(days)
                    s["days_count"] += 1
                except:
                    logging.exception("Unexpected error")
        res = list(stats.values())
        formatted_res = []
        for r in res:
            avg_days = r["sum_days"] / r["days_count"] if r["days_count"] > 0 else 0
            formatted_res.append(
                {
                    **r,
                    "kwh_fmt": f"{r['kwh']:,.0f}",
                    "usd_fmt": self._format_compact_currency(r["usd"]),
                    "avg_days": round(avg_days),
                }
            )
        reverse = self.sort_direction == "desc"
        col = self.sort_column
        formatted_res.sort(
            key=lambda x: x.get(col, 0)
            if isinstance(x.get(col), (int, float))
            else str(x.get(col, "")),
            reverse=reverse,
        )
        return formatted_res

    @rx.var
    def treemap_data(self) -> list[dict]:
        result = []
        from app.services.hubspot_service import STAGES_VENTAS, STAGES_SOCIOS

        stage_counts = {}
        for d in self.filtered_deals:
            st = d.get("dealstage")
            pipe = d.get("pipeline")
            if st:
                name = STAGES_VENTAS.get(st, STAGES_SOCIOS.get(st, st))
                key = f"{name}"
                if key not in stage_counts:
                    stage_counts[key] = {
                        "name": name,
                        "size": 0,
                        "fill": "#00d4ff" if pipe == "default" else "#00ff88",
                    }
                stage_counts[key]["size"] += 1
        return list(stage_counts.values())

    @rx.var
    def radar_chart_data(self) -> list[dict]:
        stats = self.advisor_stats[:5]
        if not stats:
            return []
        dimensions = ["Negocios", "kWh", "USD", "Propuestas", "Actividades"]
        keys = ["total", "kwh", "usd", "proposals", "activities"]
        maxes = {}
        for k in keys:
            vals = [float(s.get(k, 0)) for s in stats]
            maxes[k] = max(vals) if vals and max(vals) > 0 else 1
        result = []
        for dim, k in zip(dimensions, keys):
            row = {"subject": dim}
            for s in stats:
                name = s["name"][:15]
                row[name] = round(float(s.get(k, 0)) / maxes[k] * 100)
            result.append(row)
        win_row = {"subject": "Win Rate"}
        for s in stats:
            name = s["name"][:15]
            total = s["total"]
            won = s["convenio"]
            rate = won / total * 100 if total > 0 else 0
            win_row[name] = round(rate)
        result.append(win_row)
        return result

    @rx.var
    def radar_advisor_names(self) -> list[str]:
        return [s["name"][:15] for s in self.advisor_stats[:5]]

    @rx.var
    def radar_name_0(self) -> str:
        names = self.radar_advisor_names
        return names[0] if len(names) > 0 else ""

    @rx.var
    def radar_name_1(self) -> str:
        names = self.radar_advisor_names
        return names[1] if len(names) > 1 else ""

    @rx.var
    def radar_name_2(self) -> str:
        names = self.radar_advisor_names
        return names[2] if len(names) > 2 else ""

    @rx.var
    def radar_name_3(self) -> str:
        names = self.radar_advisor_names
        return names[3] if len(names) > 3 else ""

    @rx.var
    def radar_name_4(self) -> str:
        names = self.radar_advisor_names
        return names[4] if len(names) > 4 else ""

    @rx.var
    def advisor_ranking(self) -> list[dict[str, str | int | float]]:
        stats = self.advisor_stats
        sorted_stats = sorted(stats, key=lambda x: x["total"], reverse=True)
        return sorted_stats[:10]

    @rx.var
    def selected_advisor_deals(self) -> list[dict[str, str]]:
        from app.services.hubspot_service import STAGES_VENTAS, STAGES_SOCIOS, PIPELINES

        if not self.selected_advisor:
            return []
        deals = []
        for d in self.filtered_deals:
            if d.get("hubspot_owner_id") == self.selected_advisor:
                st = d.get("dealstage")
                st_name = (
                    STAGES_VENTAS.get(st, STAGES_SOCIOS.get(st, st))
                    if st
                    else "Sin etapa"
                )
                kwh_val = d.get("capacidad__kwh___clonada_")
                kwh_fmt = f"{float(kwh_val):,.0f}" if kwh_val else "0"
                usd_val = d.get("amount")
                usd_fmt = f"${float(usd_val):,.2f}" if usd_val else "$0.00"
                deals.append(
                    {
                        "dealname": d.get("dealname", "Sin Nombre"),
                        "stage": str(st_name),
                        "pipeline": PIPELINES.get(d.get("pipeline"), "Desconocido"),
                        "amount": usd_fmt,
                        "kwh": kwh_fmt,
                        "created": d.get("createdate", "")[:10]
                        if d.get("createdate")
                        else "",
                    }
                )
        return deals

    def _parse_date(self, date_str: str | None) -> datetime | None:
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except:
            logging.exception("Unexpected error")
            return None

    def _get_iso_week(self, dt: datetime) -> str:
        year, week, _ = dt.isocalendar()
        return f"{year}-W{week:02d}"

    @rx.var
    def weekly_new_deals(self) -> list[dict[str, str | int | float]]:
        from datetime import datetime, timezone, timedelta

        now = datetime.now(timezone.utc)
        weeks = []
        for i in range(11, -1, -1):
            dt = now - timedelta(weeks=i)
            year, week, _ = dt.isocalendar()
            weeks.append(f"{year}-W{week:02d}")
        counts = {w: 0 for w in weeks}
        for d in self.filtered_deals:
            dt = self._parse_date(d.get("createdate"))
            if dt:
                w = self._get_iso_week(dt)
                if w in counts:
                    counts[w] += 1
        max_val = max(list(counts.values())) if counts else 0
        return [
            {
                "label": f"Sem {w.split('W')[1]}",
                "count": c,
                "bar_pct": c / max_val * 100 if max_val > 0 else 0,
            }
            for w, c in counts.items()
        ]

    @rx.var
    def weekly_proposals(self) -> list[dict[str, str | int | float]]:
        from datetime import datetime, timezone, timedelta

        now = datetime.now(timezone.utc)
        weeks = []
        for i in range(11, -1, -1):
            dt = now - timedelta(weeks=i)
            year, week, _ = dt.isocalendar()
            weeks.append(f"{year}-W{week:02d}")
        counts = {w: 0 for w in weeks}
        for d in self.filtered_deals:
            dt_str = d.get("carga_propuesta_a_monday_historica") or (
                d.get("hs_lastmodifieddate")
                if d.get("dealstage") == "qualifiedtobuy"
                else None
            )
            dt = self._parse_date(dt_str)
            if dt:
                w = self._get_iso_week(dt)
                if w in counts:
                    counts[w] += 1
        max_val = max(list(counts.values())) if counts else 0
        return [
            {
                "label": f"Sem {w.split('W')[1]}",
                "count": c,
                "bar_pct": c / max_val * 100 if max_val > 0 else 0,
            }
            for w, c in counts.items()
        ]

    @rx.var
    def weekly_stage_movements(self) -> list[dict[str, str | int]]:
        from datetime import datetime, timezone, timedelta

        now = datetime.now(timezone.utc)
        this_week = self._get_iso_week(now)
        last_week = self._get_iso_week(now - timedelta(weeks=1))
        categories = {
            "Lead Calificado": ["1230967589", "1182079917"],
            "Propuesta": ["appointmentscheduled", "qualifiedtobuy"],
            "Negociación": ["1329256222", "1329255962", "1212794259"],
            "Contrato": ["contractsent", "1185807635", "1338977193"],
            "Cerrado Ganado": ["closedwon", "1182079922"],
            "Cerrado Perdido": ["closedlost", "1182079923"],
        }
        stats = {k: {"this": 0, "last": 0} for k in categories}
        for d in self.filtered_deals:
            st = d.get("dealstage")
            dt = self._parse_date(d.get("hs_lastmodifieddate"))
            if st and dt:
                w = self._get_iso_week(dt)
                for cat, stages in categories.items():
                    if st in stages:
                        if w == this_week:
                            stats[cat]["this"] += 1
                        elif w == last_week:
                            stats[cat]["last"] += 1
        result = []
        for cat, vals in stats.items():
            delta = vals["this"] - vals["last"]
            result.append(
                {
                    "stage": cat,
                    "count": vals["this"],
                    "delta": f"+{delta}" if delta > 0 else str(delta),
                    "is_positive": delta >= 0,
                }
            )
        return result

    def _extract_weekly_stats(self, week_iso: str) -> list[float]:
        new_d = 0.0
        kwh = 0.0
        usd = 0.0
        prop = 0.0
        won = 0.0
        lost = 0.0
        for d in self.filtered_deals:
            c_dt = self._parse_date(d.get("createdate"))
            if c_dt and self._get_iso_week(c_dt) == week_iso:
                new_d += 1
                k_val = d.get("capacidad__kwh___clonada_")
                if k_val:
                    try:
                        kwh += float(k_val)
                    except:
                        logging.exception("Unexpected error")
                u_val = d.get("amount")
                if u_val:
                    try:
                        usd += float(u_val)
                    except:
                        logging.exception("Unexpected error")
            st = d.get("dealstage")
            m_dt = self._parse_date(d.get("hs_lastmodifieddate"))
            if m_dt and self._get_iso_week(m_dt) == week_iso:
                if st in ["closedwon", "1182079922"]:
                    won += 1
                elif st in ["closedlost", "1182079923"]:
                    lost += 1
            p_dt_str = d.get("carga_propuesta_a_monday_historica")
            p_dt = self._parse_date(p_dt_str)
            if p_dt and self._get_iso_week(p_dt) == week_iso:
                prop += 1
        return [new_d, kwh, usd, prop, won, lost]

    @rx.var
    def weekly_comparison(self) -> list[dict[str, str]]:
        from datetime import datetime, timezone, timedelta

        now = datetime.now(timezone.utc)
        w0 = self._get_iso_week(now)
        w1 = self._get_iso_week(now - timedelta(weeks=1))
        w2 = self._get_iso_week(now - timedelta(weeks=2))
        s0 = self._extract_weekly_stats(w0)
        s1 = self._extract_weekly_stats(w1)
        s2 = self._extract_weekly_stats(w2)
        labels = [
            "Nuevos Negocios",
            "kWh Agregados",
            "Valor USD",
            "Propuestas",
            "Convenios Firmados",
            "Negocios Perdidos",
        ]
        fmts = [
            lambda x: str(int(x)),
            lambda x: f"{x:,.0f}",
            lambda x: f"${x:,.0f}",
            lambda x: str(int(x)),
            lambda x: str(int(x)),
            lambda x: str(int(x)),
        ]
        rows = []
        for i in range(6):
            delta = s0[i] - s1[i]
            is_pos = delta >= 0
            if labels[i] == "Negocios Perdidos":
                is_pos = delta <= 0
            rows.append(
                {
                    "metric": labels[i],
                    "w0": fmts[i](s0[i]),
                    "w1": fmts[i](s1[i]),
                    "w2": fmts[i](s2[i]),
                    "delta": f"+{fmts[i](delta)}"
                    if delta > 0
                    else fmts[i](delta).replace("$-", "-$"),
                    "color": "#00ff88" if is_pos else "#ff3366",
                }
            )
        return rows

    def _group_by_period(self, value_fn) -> list[dict[str, str | int | float]]:
        from datetime import datetime, timezone, timedelta

        dates = []
        for d in self.filtered_deals:
            dt = self._parse_date(d.get("createdate"))
            if dt:
                dates.append(dt)
        now = datetime.now(timezone.utc)
        periods = []
        if not dates:
            if self.time_granularity == "day":
                for i in range(29, -1, -1):
                    periods.append((now - timedelta(days=i)).strftime("%Y-%m-%d"))
            elif self.time_granularity == "week":
                for i in range(11, -1, -1):
                    periods.append(self._get_iso_week(now - timedelta(weeks=i)))
            elif self.time_granularity == "month":
                for i in range(11, -1, -1):
                    dt = (now.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
                    periods.append(dt.strftime("%Y-%m"))
                periods = sorted(list(set(periods)))[-12:]
            else:
                years = [str(now.year - i) for i in range(4, -1, -1)]
                periods = years
        else:
            min_date = min(dates)
            max_date = max(dates)
            if self.time_granularity == "day":
                current = min_date
                while current <= max_date:
                    periods.append(current.strftime("%Y-%m-%d"))
                    current += timedelta(days=1)
                periods = periods[-60:]
            elif self.time_granularity == "week":
                current = min_date
                while current <= max_date:
                    periods.append(self._get_iso_week(current))
                    current += timedelta(weeks=1)
                periods = sorted(list(set(periods)))[-24:]
            elif self.time_granularity == "month":
                current = min_date.replace(day=1)
                while current <= max_date:
                    periods.append(current.strftime("%Y-%m"))
                    if current.month == 12:
                        current = current.replace(year=current.year + 1, month=1)
                    else:
                        current = current.replace(month=current.month + 1)
                periods = periods[-18:]
            else:
                for y in range(min_date.year, max_date.year + 1):
                    periods.append(y)
        counts = {p: 0.0 for p in periods}
        for d in self.filtered_deals:
            dt = self._parse_date(d.get("createdate"))
            if dt:
                if self.time_granularity == "day":
                    k = dt.strftime("%Y-%m-%d")
                elif self.time_granularity == "week":
                    k = self._get_iso_week(dt)
                elif self.time_granularity == "month":
                    k = dt.strftime("%Y-%m")
                else:
                    k = str(dt.year)
                if k in counts:
                    counts[k] += value_fn(d)
        max_val = max(list(counts.values())) if counts else 0.0
        res = []
        for p, c in counts.items():
            label = p
            if self.time_granularity == "week":
                label = f"Sem {p.split('W')[-1]}"
            res.append(
                {
                    "label": label,
                    "value": c,
                    "bar_pct": c / max_val * 100 if max_val > 0 else 0,
                }
            )
        return res

    @rx.var
    def time_deals_chart(self) -> list[dict[str, str | int | float]]:
        return self._group_by_period(lambda d: 1)

    @rx.var
    def time_kwh_chart(self) -> list[dict[str, str | int | float]]:
        @rx.event
        def get_kwh(d):
            try:
                return float(d.get("capacidad__kwh___clonada_") or 0)
            except:
                logging.exception("Unexpected error")
                return 0.0

        return self._group_by_period(get_kwh)

    @rx.var
    def time_revenue_chart(self) -> list[dict[str, str | int | float]]:
        @rx.event
        def get_rev(d):
            try:
                return float(d.get("amount") or 0)
            except:
                logging.exception("Unexpected error")
                return 0.0

        return self._group_by_period(get_rev)

    @rx.var
    def time_convenios_chart(self) -> list[dict[str, str | int | float]]:
        @rx.event
        def is_won(d):
            return 1 if d.get("dealstage") in ["closedwon", "1182079922"] else 0

        return self._group_by_period(is_won)

    @rx.var
    def heatmap_data(self) -> list[dict]:
        """Build heatmap data: owner vs time period (month).
        Each point: {x: month_index, y: owner_index, z: count, owner: str, month: str}
        """
        from datetime import datetime, timezone, timedelta

        now = datetime.now(timezone.utc)
        months = []
        for i in range(5, -1, -1):
            dt = (now.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
            months.append(dt.strftime("%Y-%m"))
        months = sorted(list(set(months)))[-6:]
        owner_counts = {}
        for d in self.filtered_deals:
            oid = d.get("hubspot_owner_id")
            if oid:
                owner_counts[oid] = owner_counts.get(oid, 0) + 1
        top_owners = sorted(owner_counts.items(), key=lambda x: -x[1])[:15]
        owner_ids = [o[0] for o in top_owners]
        grid = {}
        for d in self.filtered_deals:
            oid = d.get("hubspot_owner_id")
            dt = self._parse_date(d.get("createdate"))
            if oid in owner_ids and dt:
                m = dt.strftime("%Y-%m")
                if m in months:
                    key = (oid, m)
                    grid[key] = grid.get(key, 0) + 1
        result = []
        for oi, oid in enumerate(owner_ids):
            for mi, m in enumerate(months):
                count = grid.get((oid, m), 0)
                if count > 0:
                    result.append(
                        {
                            "x": mi,
                            "y": oi,
                            "z": count,
                            "owner": self.owners.get(oid, "?")[:20],
                            "month": m,
                        }
                    )
        return result

    @rx.var
    def stage_flow_data(self) -> list[dict]:
        """Build stage flow showing how many deals moved between stages."""
        flow_stages = [
            ("Lead/Interesado", ["1230967589", "1182079917"]),
            ("Propuesta", ["appointmentscheduled", "qualifiedtobuy", "1185807635"]),
            ("Negociación", ["1329256222", "1329255962", "1212794259", "1338977193"]),
            (
                "Contrato",
                [
                    "contractsent",
                    "1212783978",
                    "1233929775",
                    "1232935533",
                    "1232929105",
                ],
            ),
            ("Cerrado Ganado", ["closedwon", "1182079922"]),
            ("Cerrado Perdido", ["closedlost", "1182079923"]),
        ]
        counts = []
        total = len(self.filtered_deals)
        for name, stage_ids in flow_stages:
            c = sum((1 for d in self.filtered_deals if d.get("dealstage") in stage_ids))
            pct = c / total * 100 if total > 0 else 0
            counts.append(
                {"stage": name, "count": c, "pct": round(pct, 1), "bar_pct": pct}
            )
        max_c = max([c["count"] for c in counts]) if counts else 1
        for c in counts:
            c["bar_pct"] = c["count"] / max_c * 100 if max_c > 0 else 0
        return counts

    @rx.var
    def scatter_data(self) -> list[dict]:
        """Scatter plot: x=kWh, y=amount for each deal with data."""
        result = []
        for d in self.filtered_deals:
            kwh = d.get("capacidad__kwh___clonada_")
            amt = d.get("amount")
            if kwh and amt:
                try:
                    kwh_val = float(kwh)
                    amt_val = float(amt)
                    if kwh_val > 0 and amt_val > 0:
                        result.append(
                            {
                                "kwh": round(kwh_val),
                                "amount": round(amt_val),
                                "name": d.get("dealname", "")[:30],
                            }
                        )
                except:
                    logging.exception("Unexpected error")
        return result[:200]

    @rx.var
    def time_series_data(self) -> list[dict]:
        """Time series with: new_deals, kwh_added, revenue, convenios."""
        from datetime import datetime, timezone, timedelta

        dates = []
        for d in self.filtered_deals:
            dt = self._parse_date(d.get("createdate"))
            if dt:
                dates.append(dt)
        now = datetime.now(timezone.utc)
        periods = []
        if not dates:
            if self.time_granularity == "day":
                for i in range(29, -1, -1):
                    periods.append((now - timedelta(days=i)).strftime("%Y-%m-%d"))
            elif self.time_granularity == "week":
                for i in range(11, -1, -1):
                    periods.append(self._get_iso_week(now - timedelta(weeks=i)))
            elif self.time_granularity == "month":
                for i in range(11, -1, -1):
                    dt = (now.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
                    periods.append(dt.strftime("%Y-%m"))
                periods = sorted(list(set(periods)))[-12:]
            else:
                years = [str(now.year - i) for i in range(4, -1, -1)]
                periods = years
        else:
            min_date = min(dates)
            max_date = max(dates)
            if self.time_granularity == "day":
                current = min_date
                while current <= max_date:
                    periods.append(current.strftime("%Y-%m-%d"))
                    current += timedelta(days=1)
                periods = periods[-60:]
            elif self.time_granularity == "week":
                current = min_date
                while current <= max_date:
                    periods.append(self._get_iso_week(current))
                    current += timedelta(weeks=1)
                periods = sorted(list(set(periods)))[-24:]
            elif self.time_granularity == "month":
                current = min_date.replace(day=1)
                while current <= max_date:
                    periods.append(current.strftime("%Y-%m"))
                    if current.month == 12:
                        current = current.replace(year=current.year + 1, month=1)
                    else:
                        current = current.replace(month=current.month + 1)
                periods = periods[-18:]
            else:
                for y in range(min_date.year, max_date.year + 1):
                    periods.append(y)
        data = {
            p: {"month": p, "deals": 0, "kwh": 0, "revenue": 0, "convenios": 0}
            for p in periods
        }
        for d in self.filtered_deals:
            dt = self._parse_date(d.get("createdate"))
            if dt:
                if self.time_granularity == "day":
                    k = dt.strftime("%Y-%m-%d")
                elif self.time_granularity == "week":
                    k = self._get_iso_week(dt)
                elif self.time_granularity == "month":
                    k = dt.strftime("%Y-%m")
                else:
                    k = str(dt.year)
                if k in data:
                    data[k]["deals"] += 1
                    kwh = d.get("capacidad__kwh___clonada_")
                    if kwh:
                        try:
                            data[k]["kwh"] += float(kwh)
                        except:
                            logging.exception("Unexpected error")
                    amt = d.get("amount")
                    if amt:
                        try:
                            data[k]["revenue"] += float(amt)
                        except:
                            logging.exception("Unexpected error")
                    if d.get("dealstage") in ["closedwon", "1182079922"]:
                        data[k]["convenios"] += 1
        result = []
        for p in periods:
            item = data[p]
            if self.time_granularity == "week":
                item["month"] = f"Sem {p.split('W')[-1]}"
            result.append(item)
        return result

    @rx.var
    def pipeline_stacked_data(self) -> list[dict]:
        from app.services.hubspot_service import STAGES_VENTAS, STAGES_SOCIOS

        ventas_row = {"pipeline": "Pipeline de Ventas"}
        socios_row = {"pipeline": "Pipeline de Socios"}
        for d in self.filtered_deals:
            st = d.get("dealstage")
            pipe = d.get("pipeline")
            if not st:
                continue
            if pipe == "default":
                name = STAGES_VENTAS.get(st, st)
                ventas_row[name] = ventas_row.get(name, 0) + 1
            elif pipe == "803674731":
                name = STAGES_SOCIOS.get(st, st)
                socios_row[name] = socios_row.get(name, 0) + 1
        return [ventas_row, socios_row]

    @rx.var
    def heatmap_owners_labels(self) -> list[str]:
        owner_counts = {}
        for d in self.filtered_deals:
            oid = d.get("hubspot_owner_id")
            if oid:
                owner_counts[oid] = owner_counts.get(oid, 0) + 1
        top = sorted(owner_counts.items(), key=lambda x: -x[1])[:15]
        return [self.owners.get(o[0], "?")[:20] for o in top]

    @rx.var
    def heatmap_month_labels(self) -> list[str]:
        from datetime import datetime, timezone, timedelta

        now = datetime.now(timezone.utc)
        months = []
        for i in range(5, -1, -1):
            dt = (now.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
            months.append(dt.strftime("%Y-%m"))
        return sorted(list(set(months)))[-6:]