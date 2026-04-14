import os
import logging
from hubspot import HubSpot

PIPELINES = {"default": "Pipeline de Ventas", "803674731": "Pipeline de Socios"}
STAGES_VENTAS = {
    "1230967589": "Lead Calificado",
    "appointmentscheduled": "Propuesta solicitada",
    "qualifiedtobuy": "Propuesta presentada",
    "1329256222": "Negociación de propuesta",
    "contractsent": "Contrato enviado",
    "1212783978": "Levantamiento Preliminar",
    "1212794259": "Negociación de contrato",
    "closedwon": "Contrato firmado por cliente",
    "1233929775": "RTP Enviado a revisión",
    "1232935533": "RTP Aprobado por Ops",
    "1232929105": "Contrato firmado por Atlantica/Quartux",
    "closedlost": "Negocio perdido",
}
STAGES_SOCIOS = {
    "1182079917": "Socio interesado",
    "1185807635": "Convenio enviado",
    "1329255962": "Negociación",
    "1338977193": "Área legal",
    "1182079922": "Convenio firmado",
    "1182079923": "Negocio perdido",
}


def get_client():
    token = os.getenv("HUBSPOT_ACCESS_TOKEN")
    if not token:
        return None
    return HubSpot(access_token=token)


def fetch_all_deals() -> list[dict]:
    client = get_client()
    if not client:
        return []
    try:
        all_deals = []
        after = None
        properties = [
            "dealname",
            "pipeline",
            "dealstage",
            "amount",
            "hubspot_owner_id",
            "createdate",
            "closedate",
            "hs_lastmodifieddate",
            "capacidad__kwh___clonada_",
            "potencia__kw___clonada_",
            "monto_propuesta",
            "monto_de_recibo_2_0",
            "days_to_close",
            "carga_propuesta_a_monday_historica",
            "solicitud_de_propuesta_historica",
            "num_notes",
            "contrato_firmado",
            "propuesta",
            "referido_por_socio",
            "fecha_de_1er_cierre",
            "tipo_de_socio",
            "remarketing",
            "negocio_heredado",
            "hs_v2_date_entered_1230967589",
            "hs_v2_date_entered_closedwon",
            "fecha_de_primera_reunion",
            "hs_v2_date_entered_1182079917",
            "hs_v2_date_entered_1182079922",
            "hs_v2_date_entered_1182079923",
            "hs_v2_date_entered_1185807635",
            "hs_v2_date_entered_1212783978",
            "hs_v2_date_entered_1212794259",
            "hs_v2_date_entered_1232929105",
            "hs_v2_date_entered_1232935533",
            "hs_v2_date_entered_1233929775",
            "hs_v2_date_entered_1329255962",
            "hs_v2_date_entered_1329256222",
            "hs_v2_date_entered_1338977193",
            "hs_v2_date_entered_appointmentscheduled",
            "hs_v2_date_entered_closedlost",
            "hs_v2_date_entered_contractsent",
            "hs_v2_date_entered_qualifiedtobuy",
            "hs_v2_date_entered_current_stage",
        ]
        while True:
            kwargs = {"limit": 100, "properties": properties}
            if after:
                kwargs["after"] = after
            resp = client.crm.deals.basic_api.get_page(**kwargs)
            for d in resp.results:
                all_deals.append(d.properties)
            if resp.paging and resp.paging.next:
                after = resp.paging.next.after
            else:
                break
        return all_deals
    except Exception as e:
        logging.exception(f"Error fetching deals: {e}")
        return []


def fetch_all_owners() -> dict[str, str]:
    client = get_client()
    if not client:
        return {}
    try:
        owners_dict = {}
        after = None
        while True:
            kwargs = {"limit": 100}
            if after:
                kwargs["after"] = after
            resp = client.crm.owners.owners_api.get_page(**kwargs)
            for o in resp.results:
                owners_dict[o.id] = f"{o.first_name or ''} {o.last_name or ''}".strip()
            if resp.paging and resp.paging.next:
                after = resp.paging.next.after
            else:
                break
        return owners_dict
    except Exception as e:
        logging.exception(f"Error fetching owners: {e}")
        return {}


def fetch_all_deals_with_meta() -> dict:
    import time

    start = time.time()
    client = get_client()
    if not client:
        return {
            "deals": [],
            "status": "error",
            "http_status": 0,
            "duration_sec": 0,
            "count": 0,
            "error_msg": "No HUBSPOT_ACCESS_TOKEN configured",
            "endpoint": "N/A",
        }
    try:
        all_deals = []
        after = None
        properties = [
            "dealname",
            "pipeline",
            "dealstage",
            "amount",
            "hubspot_owner_id",
            "createdate",
            "closedate",
            "hs_lastmodifieddate",
            "capacidad__kwh___clonada_",
            "potencia__kw___clonada_",
            "monto_propuesta",
            "monto_de_recibo_2_0",
            "days_to_close",
            "carga_propuesta_a_monday_historica",
            "solicitud_de_propuesta_historica",
            "num_notes",
            "contrato_firmado",
            "propuesta",
            "referido_por_socio",
            "fecha_de_1er_cierre",
            "tipo_de_socio",
            "remarketing",
            "negocio_heredado",
            "hs_v2_date_entered_1230967589",
            "hs_v2_date_entered_closedwon",
            "fecha_de_primera_reunion",
            "hs_v2_date_entered_1182079917",
            "hs_v2_date_entered_1182079922",
            "hs_v2_date_entered_1182079923",
            "hs_v2_date_entered_1185807635",
            "hs_v2_date_entered_1212783978",
            "hs_v2_date_entered_1212794259",
            "hs_v2_date_entered_1232929105",
            "hs_v2_date_entered_1232935533",
            "hs_v2_date_entered_1233929775",
            "hs_v2_date_entered_1329255962",
            "hs_v2_date_entered_1329256222",
            "hs_v2_date_entered_1338977193",
            "hs_v2_date_entered_appointmentscheduled",
            "hs_v2_date_entered_closedlost",
            "hs_v2_date_entered_contractsent",
            "hs_v2_date_entered_qualifiedtobuy",
            "hs_v2_date_entered_current_stage",
        ]
        http_status = 200
        while True:
            kwargs = {"limit": 100, "properties": properties}
            if after:
                kwargs["after"] = after
            resp = client.crm.deals.basic_api.get_page(**kwargs)
            for d in resp.results:
                all_deals.append(d.properties)
            if resp.paging and resp.paging.next:
                after = resp.paging.next.after
            else:
                break
        duration = time.time() - start
        return {
            "deals": all_deals,
            "status": "success",
            "http_status": http_status,
            "duration_sec": round(duration, 2),
            "count": len(all_deals),
            "error_msg": "",
            "endpoint": "crm/v3/objects/deals",
        }
    except Exception as e:
        logging.exception("Unexpected error")
        duration = time.time() - start
        return {
            "deals": [],
            "status": "error",
            "http_status": getattr(e, "status", 500),
            "duration_sec": round(duration, 2),
            "count": 0,
            "error_msg": str(e)[:200],
            "endpoint": "crm/v3/objects/deals",
        }


def fetch_all_owners_with_meta() -> dict:
    import time

    start = time.time()
    client = get_client()
    if not client:
        return {
            "owners": {},
            "status": "error",
            "http_status": 0,
            "duration_sec": 0,
            "count": 0,
            "error_msg": "No HUBSPOT_ACCESS_TOKEN configured",
            "endpoint": "N/A",
        }
    try:
        owners_dict = {}
        after = None
        http_status = 200
        while True:
            kwargs = {"limit": 100}
            if after:
                kwargs["after"] = after
            resp = client.crm.owners.owners_api.get_page(**kwargs)
            for o in resp.results:
                owners_dict[o.id] = f"{o.first_name or ''} {o.last_name or ''}".strip()
            if resp.paging and resp.paging.next:
                after = resp.paging.next.after
            else:
                break
        duration = time.time() - start
        return {
            "owners": owners_dict,
            "status": "success",
            "http_status": http_status,
            "duration_sec": round(duration, 2),
            "count": len(owners_dict),
            "error_msg": "",
            "endpoint": "crm/v3/owners/",
        }
    except Exception as e:
        logging.exception("Unexpected error")
        duration = time.time() - start
        return {
            "owners": {},
            "status": "error",
            "http_status": getattr(e, "status", 500),
            "duration_sec": round(duration, 2),
            "count": 0,
            "error_msg": str(e)[:200],
            "endpoint": "crm/v3/owners/",
        }