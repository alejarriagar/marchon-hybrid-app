import datetime as dt
import math
import os
import sys
import time
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st

st.set_page_config(page_title="MARCHON Hybrid OS", layout="wide", initial_sidebar_state="collapsed")

from src.database import repository as repo
from src.seed_data import OCTOBER_BJJ_PROGRAM, PROGRAMS_CATALOG, SEPTEMBER_PROGRAM
from src.services.progression import (
    calculate_running_10k_paces,
    calculate_target_weight,
    get_week_periodization_wave,
)
from src.ui.components import check_pin_auth, render_exercise_item, render_kpi_table, render_phase_snapshot
from src.ui.styles import apply_custom_styles

TZ = ZoneInfo("Europe/Madrid")
BJJ_START = dt.date(2026, 10, 1)
DAY_NAMES = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
MONTHS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
WEEK_NAMES = {1: "Acumulación", 2: "Sobrecarga", 3: "Pico", 4: "Descarga"}
RPE_OPTIONS = [6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
LIFT_NAMES = {
    "bench_press": "Bench Press",
    "back_squat": "Back Squat",
    "deadlift": "Deadlift",
    "ohp": "Overhead Press",
}
BLOCK_COLORS = {"W": "green", "S": "orange", "H": "blue", "E": "violet", "R": "green", "B": "blue"}
NAV_ITEMS = [("home", "HOME"), ("workout", "WORKOUT"), ("programs", "PROGRAMS"), ("kpis", "KPIS"), ("account", "ACCOUNT")]

apply_custom_styles()

if not check_pin_auth():
    st.stop()

repo.ensure_schema()
ss = st.session_state


# ---------------------------------------------------------------- utilidades
def monday_of(day: dt.date) -> dt.date:
    return day - dt.timedelta(days=day.weekday())


def floor_to_plate(value: float, step: float = 2.5) -> float:
    return math.floor(value / step) * step


def short_date(day: dt.date) -> str:
    return f"{day.day} {MONTHS[day.month - 1]}"


def estimate_1rm(weight: float, reps: int, rpe: float) -> float:
    """Epley corregido por RPE: suma las repeticiones en recámara."""
    if weight <= 0 or reps <= 0:
        return 0.0
    effective = reps + max(0.0, 10.0 - rpe)
    return round(weight if effective <= 1 else weight * (1 + effective / 30.0), 1)


today = dt.datetime.now(TZ).date()
this_monday = monday_of(today)
block_start = monday_of(
    dt.date.fromisoformat(repo.get_setting("block_start", this_monday.isoformat(), persist=True))
)


def block_info(day: dt.date):
    weeks = (monday_of(day) - block_start).days // 7
    if weeks < 0:
        return 1, 0
    return weeks % 4 + 1, weeks // 4 + 1


def program_for(day: dt.date):
    return OCTOBER_BJJ_PROGRAM if day >= BJJ_START else SEPTEMBER_PROGRAM


def program_label(day: dt.date) -> str:
    return "PERFORM + BJJ" if day >= BJJ_START else "PERFORM"


def week_label(offset: int) -> str:
    monday = this_monday + dt.timedelta(weeks=offset)
    week, block = block_info(monday)
    phase = "Pre-bloque" if block == 0 else f"Bloque {block} · S{week} {WEEK_NAMES[week]}"
    current = " · actual" if offset == 0 else ""
    return f"Semana del {short_date(monday)} — {phase}{current}"


# ---------------------------------------------------------------- estado
ss.setdefault("week_offset", 0)
ss.setdefault("sel_weekday", today.weekday())
ss.setdefault("view", "workout")
ss.setdefault("rest_end", None)
ss.setdefault("rest_label", "")


def go_today():
    ss["week_offset"] = 0
    ss["sel_weekday"] = today.weekday()


def select_day(index: int):
    ss["sel_weekday"] = index


def set_view(view: str):
    ss["view"] = view


def start_rest(seconds: int, label: str):
    if seconds and seconds > 0:
        ss["rest_end"] = time.time() + seconds
        ss["rest_label"] = label


def skip_rest():
    ss["rest_end"] = None


def save_set_cb(session_date, day_id, block_week, ex_key, ex_name, set_number, pct, w_key, r_key, rpe_key, rest_seconds):
    weight = float(ss.get(w_key, 0.0))
    reps = int(ss.get(r_key, 0))
    rpe = float(ss.get(rpe_key, 8.0))
    repo.save_single_set(
        session_date=session_date, day_id=day_id, block_week=block_week, exercise_key=ex_key,
        exercise_name=ex_name, set_number=set_number, pct_1rm=pct, weight=weight, reps=reps,
        rpe=rpe, est_1rm=estimate_1rm(weight, reps, rpe),
    )
    start_rest(rest_seconds, f"{ex_name} · serie {set_number}")
    st.toast(f"Serie {set_number} guardada")


def finalize_cb(session_date, day_id, title, sauna_key, duration_key):
    repo.finalize_session(session_date, day_id, title, bool(ss.get(sauna_key, False)), int(ss.get(duration_key, 55)))
    st.toast("Entrenamiento guardado")


def apply_best_cb(updates):
    for key, value in updates.items():
        repo.update_user_1rm(key, value, LIFT_NAMES.get(key))
    st.toast("1RMs actualizados con tus mejores marcas")


def logout_cb():
    ss["authenticated"] = False


# ---------------------------------------------------------------- temporizador
@st.fragment(run_every=1)
def rest_timer():
    end = ss.get("rest_end")
    if not end:
        return
    remaining = int(round(end - time.time()))
    if remaining > 0:
        minutes, seconds = divmod(remaining, 60)
        st.markdown(
            f'<div class="rest-banner">DESCANSO {minutes}:{seconds:02d}<span>{ss.get("rest_label", "")}</span></div>',
            unsafe_allow_html=True,
        )
        st.button("Saltar descanso", key="skip_rest_btn", on_click=skip_rest, use_container_width=True)
    elif remaining > -6:
        st.markdown('<div class="rest-banner done">DESCANSO TERMINADO</div>', unsafe_allow_html=True)
    else:
        ss["rest_end"] = None


# ---------------------------------------------------------------- vistas
def render_workout():
    st.selectbox("Semana", list(range(-12, 13)), key="week_offset", format_func=week_label, label_visibility="collapsed")
    week_monday = this_monday + dt.timedelta(weeks=ss["week_offset"])
    completed = repo.get_completed_dates()

    with st.container(key="cal_strip"):
        cols = st.columns(7)
        for i in range(7):
            day_date = week_monday + dt.timedelta(days=i)
            plan_day = program_for(day_date)[i]
            if day_date.isoformat() in completed:
                icon = "✓"
            elif plan_day.is_rest_day:
                icon = "○"
            else:
                icon = "•"
            cols[i].button(
                f"{icon}\n{DAY_NAMES[i]}\n{day_date.day}",
                key=f"day_btn_{i}",
                type="primary" if i == ss["sel_weekday"] else "secondary",
                use_container_width=True,
                on_click=select_day,
                args=(i,),
            )

    sel_date = week_monday + dt.timedelta(days=ss["sel_weekday"])
    day = program_for(sel_date)[ss["sel_weekday"]]
    date_str = sel_date.isoformat()
    block_week, block_num = block_info(sel_date)
    wave = get_week_periodization_wave(block_week)
    readiness = repo.get_readiness(date_str)
    load_factor = 0.95 if (readiness is not None and readiness < 65) else 1.0
    is_today = sel_date == today

    block_txt = "PRE-BLOQUE" if block_num == 0 else f"BLOQUE {block_num} · SEMANA {block_week} · {WEEK_NAMES[block_week].upper()}"
    date_txt = f"{'HOY · ' if is_today else ''}{DAY_NAMES[sel_date.weekday()].upper()} {sel_date.day} {MONTHS[sel_date.month - 1].upper()} {sel_date.year}"
    st.markdown(
        f'<div class="day-date">{date_txt}</div>'
        f'<div class="day-program">{program_label(sel_date)}</div>'
        f'<div class="day-title">{day.title}</div>'
        f'<div class="day-block">{block_txt} · {wave["pct_wave"][0]:g}–{wave["pct_wave"][-1]:g}% 1RM</div>',
        unsafe_allow_html=True,
    )

    if not is_today:
        st.button("Volver a hoy", on_click=go_today, use_container_width=True)
    if load_factor < 1:
        st.warning(f"Readiness {readiness}%: cargas sugeridas reducidas un 5 %.")
    elif readiness is None and is_today:
        st.caption("Aún no has registrado el readiness de hoy (pestaña HOME).")

    if day.is_rest_day:
        st.markdown(
            '<div class="marchon-card" style="text-align:center;padding:2rem 1rem;">'
            '<div style="color:white;font-weight:900;">DESCANSO Y REGENERACIÓN</div>'
            '<div class="muted-small">Sueño, nutrición y sauna.</div></div>',
            unsafe_allow_html=True,
        )
        return

    saved = repo.get_day_logged_sets(date_str, day.day_id)
    one_rms = repo.get_all_user_1rms()
    paces = calculate_running_10k_paces(float(repo.get_setting("target_10k", "45")))
    first_pending_opened = False

    for b_idx, block in enumerate(day.blocks):
        color = BLOCK_COLORS.get(block.code, "gray")
        with st.expander(f":{color}[**{block.code}**]   ·   **{block.title}**", expanded=(block.code != "W")):
            caption = block.subtitle
            if block.rest_block_desc:
                caption += f" · Descanso: {block.rest_block_desc}"
            st.caption(caption)

            for e_idx, ex in enumerate(block.exercises):
                if block.code in ("S", "H"):
                    is_main = bool(ex.exercise_key)
                    if is_main:
                        num_sets = wave["sets"]
                        reps_default = wave["reps"]
                        one_rm = float(one_rms.get(ex.exercise_key, 0.0))
                    else:
                        num_sets = min(ex.target_sets, 2) if block_week == 4 else ex.target_sets
                        reps_default = ex.target_reps
                        one_rm = 0.0
                    done = sum(1 for s in range(1, num_sets + 1) if (ex.name, s) in saved)
                    ex_id = f"{date_str}_{b_idx}_{e_idx}"

                    with st.container(border=True, key=f"ex_{ex_id}"):
                        status = "✓ completado" if done == num_sets else f"{done}/{num_sets} series"
                        st.markdown(
                            f'<div class="ex-head"><span class="ex-title">{ex.name}</span>'
                            f'<span class="ex-status{" ok" if done == num_sets else ""}">{status}</span></div>'
                            f'<div class="ex-sub">{ex.target} · {ex.rest_description}</div>',
                            unsafe_allow_html=True,
                        )
                        if is_main:
                            extra = " · -5 % por readiness" if load_factor < 1 else ""
                            st.caption(f"1RM: {one_rm:g} kg{extra}")
                        if ex.notes:
                            st.caption(ex.notes)

                        auto_open = (not first_pending_opened) and done < num_sets
                        if auto_open:
                            first_pending_opened = True

                        if st.toggle("Registrar series", value=auto_open, key=f"show_{ex_id}"):
                            labels = [f"S{s}{' ✓' if (ex.name, s) in saved else ''}" for s in range(1, num_sets + 1)]
                            for s, tab in zip(range(1, num_sets + 1), st.tabs(labels)):
                                with tab:
                                    rec = saved.get((ex.name, s))
                                    if is_main:
                                        pct_list = wave["pct_wave"]
                                        pct = pct_list[s - 1] if s <= len(pct_list) else pct_list[-1]
                                        suggested = calculate_target_weight(one_rm * load_factor, pct / 100.0) if one_rm else 0.0
                                        st.markdown(f"**Objetivo:** {pct:g}% 1RM → **{suggested:g} kg** × {reps_default}")
                                    else:
                                        pct = 0.0
                                        suggested = float(ex.default_weight or 0.0)
                                        st.markdown(f"**Objetivo:** {ex.target}")

                                    w0 = float(rec["weight"]) if rec else float(suggested)
                                    r0 = int(rec["reps"]) if rec else int(reps_default)
                                    rpe0 = float(rec["rpe"]) if rec else 8.0
                                    base = f"{ex_id}_{s}_{w0:g}_{r0}"
                                    w_key, r_key, rpe_key = f"w_{base}", f"r_{base}", f"rpe_{base}"

                                    st.number_input("Peso (kg)", min_value=0.0, max_value=500.0, value=w0, step=2.5, key=w_key)
                                    c_reps, c_rpe = st.columns(2)
                                    c_reps.number_input("Reps", min_value=0, max_value=50, value=r0, step=1, key=r_key)
                                    c_rpe.selectbox(
                                        "RPE", RPE_OPTIONS,
                                        index=RPE_OPTIONS.index(rpe0) if rpe0 in RPE_OPTIONS else 4,
                                        key=rpe_key,
                                    )
                                    if rec:
                                        st.caption(
                                            f"Guardada: {rec['weight']:g} kg × {rec['reps']} @ RPE {rec['rpe']:g}"
                                            f" · 1RM est. {rec['est_1rm']:g} kg"
                                        )
                                    st.button(
                                        "Actualizar serie" if rec else f"Guardar serie {s}",
                                        key=f"save_{base}",
                                        type="secondary" if rec else "primary",
                                        use_container_width=True,
                                        on_click=save_set_cb,
                                        args=(date_str, day.day_id, block_week, ex.exercise_key, ex.name, s, pct,
                                              w_key, r_key, rpe_key, ex.rest_seconds or 0),
                                    )
                elif block.code == "R":
                    name = ex.name.lower()
                    if "x 1000" in name or "x 2000" in name:
                        pace, kind = paces["intervals_1000m"], "series"
                    elif "ritmo" in name or "fuertes" in name:
                        pace, kind = paces["race_pace"], "ritmo 10k"
                    else:
                        pace, kind = paces["z2_easy"], "Z2"
                    render_exercise_item(ex.name, ex.target, f"Ritmo {kind}: {pace} · {ex.rest_description}")
                else:
                    note = f"{ex.notes} · {ex.rest_description}" if ex.notes else ex.rest_description
                    render_exercise_item(ex.name, ex.target, note)

    st.divider()
    sauna_key, duration_key = f"sauna_{date_str}", f"dur_{date_str}"
    st.checkbox("Sauna realizada (20-30 min)", key=sauna_key)
    st.number_input("Duración (min)", min_value=10, max_value=240, value=55, step=5, key=duration_key)
    st.button(
        "Actualizar resumen de la sesión" if date_str in completed else "Finalizar entrenamiento",
        type="primary",
        use_container_width=True,
        on_click=finalize_cb,
        args=(date_str, day.day_id, day.title, sauna_key, duration_key),
    )


def render_home():
    today_str = today.isoformat()
    st.markdown("### PANEL")
    count, minutes = repo.get_session_stats()
    one_rms = repo.get_all_user_1rms()
    best = repo.get_best_est_1rm_by_key()
    pbs = sum(1 for key, value in best.items() if key in one_rms and value > one_rms[key])
    render_phase_snapshot(sessions=count, pbs=pbs, total_time=f"{minutes // 60}h {minutes % 60:02d}m")

    st.markdown("#### Readiness de hoy")
    current = repo.get_readiness(today_str)
    if current is not None:
        st.caption(f"Registrado hoy: {current}%" + (" · cargas -5 %" if current < 65 else ""))
    with st.form("readiness_form"):
        sleep = st.slider("Calidad de sueño", 1, 5, 4)
        energy = st.slider("Energía", 1, 5, 4)
        soreness = st.slider("Molestia en el brazo (1 = nada · 5 = mucha)", 1, 5, 2)
        if st.form_submit_button("Guardar readiness", use_container_width=True):
            score = repo.log_readiness(today_str, sleep, energy, soreness)
            st.success(f"Readiness {score}%" + (" — se reducirán las cargas un 5 %" if score < 65 else ""))

    st.markdown("#### Últimas sesiones")
    sessions = repo.get_recent_sessions(10)
    if not sessions:
        st.caption("Aún no has finalizado ninguna sesión.")
    for row in sessions:
        extra = " · sauna" if row["sauna"] else ""
        render_exercise_item(row["title"], f"{row['volume_kg']:.0f} kg", f"{row['date']} · {row['duration']} min{extra}")


def render_programs():
    st.markdown("### PROGRAMAS")
    active_id = "perform_oct_bjj" if today >= BJJ_START else "perform_sep"
    for prog in PROGRAMS_CATALOG:
        badge = '<span class="badge-green">ACTIVO</span>' if prog.id == active_id else ""
        tags = "".join(f'<span class="badge-tag">{t}</span>' for t in prog.tags)
        st.markdown(
            f'<div class="marchon-card"><div style="display:flex;justify-content:space-between;gap:8px;">'
            f'<span class="badge-tag">{prog.category}</span>{badge}</div>'
            f'<div style="color:white;font-weight:800;margin:0.4rem 0;">{prog.title}</div>'
            f'<div class="muted-small" style="margin-bottom:0.5rem;">{prog.description}</div>{tags}</div>',
            unsafe_allow_html=True,
        )
    st.caption("El programa cambia solo por fecha: la fase con BJJ se activa el 1 de octubre de 2026.")


def render_kpis():
    st.markdown("### KPIS")
    one_rms = repo.get_all_user_1rms()
    best = repo.get_best_est_1rm_by_key()
    rows, updates = [], {}
    for key, name in LIFT_NAMES.items():
        current = float(one_rms.get(key, 0.0))
        top = best.get(key)
        delta = f"{(top / current - 1) * 100:+.1f}%" if (top and current) else "—"
        rows.append({"name": name, "current": f"{current:g} kg", "best": f"{top:g} kg" if top else "—", "delta": delta})
        if top and floor_to_plate(top) > current:
            updates[key] = floor_to_plate(top)
    render_kpi_table(rows)
    st.caption("Mejor estimado = Epley corregido por RPE, a partir de tus series guardadas.")

    if updates:
        resumen = ", ".join(f"{LIFT_NAMES[k]} → {v:g} kg" for k, v in updates.items())
        st.info(f"Puedes subir tus 1RMs: {resumen}")
        st.button("Actualizar 1RMs con mis mejores marcas", type="primary", use_container_width=True,
                  on_click=apply_best_cb, args=(updates,))

    paces = calculate_running_10k_paces(float(repo.get_setting("target_10k", "45")))
    st.markdown("#### San Silvestre 10k")
    render_exercise_item("Ritmo de carrera", paces["race_pace"])
    render_exercise_item("Series 1000 m", paces["intervals_1000m"])
    render_exercise_item("Rodaje Z2", paces["z2_easy"])


def render_account():
    st.markdown("### CUENTA")
    one_rms = repo.get_all_user_1rms()
    with st.form("account_form"):
        st.markdown("#### 1RMs")
        values = {
            key: st.number_input(f"{name} (kg)", min_value=0.0, max_value=500.0,
                                 value=float(one_rms.get(key, 0.0)), step=2.5)
            for key, name in LIFT_NAMES.items()
        }
        target = st.number_input("Objetivo San Silvestre 10k (min)", min_value=30.0, max_value=90.0,
                                 value=float(repo.get_setting("target_10k", "45")), step=0.5)
        start = st.date_input("Inicio del bloque (lunes de la semana 1)", value=block_start, format="DD/MM/YYYY")
        if st.form_submit_button("Guardar", type="primary", use_container_width=True):
            for key, value in values.items():
                repo.update_user_1rm(key, value, LIFT_NAMES[key])
            repo.set_setting("target_10k", float(target))
            repo.set_setting("block_start", monday_of(start).isoformat())
            st.toast("Guardado")
            st.rerun()

    if repo.using_external_db():
        st.caption("Base de datos: externa (Postgres). Tus datos se conservan entre reinicios.")
    else:
        st.caption("Base de datos: SQLite local. En Streamlit Cloud estos datos pueden perderse; configura DATABASE_URL.")

    df = repo.export_all_logs_dataframe()
    if not df.empty:
        st.download_button("Exportar series a CSV", df.to_csv(index=False).encode("utf-8"),
                           file_name="marchon_series.csv", mime="text/csv", use_container_width=True)
    st.button("Cerrar sesión", on_click=logout_cb, use_container_width=True)


# ---------------------------------------------------------------- render
rest_timer()

VIEWS = {
    "home": render_home,
    "workout": render_workout,
    "programs": render_programs,
    "kpis": render_kpis,
    "account": render_account,
}
VIEWS.get(ss["view"], render_workout)()

with st.container(key="bottom_nav"):
    nav_cols = st.columns(len(NAV_ITEMS))
    for col, (view, label) in zip(nav_cols, NAV_ITEMS):
        col.button(label, key=f"nav_{view}", type="primary" if ss["view"] == view else "secondary",
                   use_container_width=True, on_click=set_view, args=(view,))
