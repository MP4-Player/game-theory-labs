import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Лабораторная работа №2", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a0033 0%, #001a33 40%, #003322 100%);
        background-attachment: fixed;
    }
    .explanation {
        background: rgba(255,255,255,0.07);
        border-left: 4px solid #8877ee;
        border-radius: 0 8px 8px 0;
        padding: 10px 16px;
        margin: 6px 0 10px 0;
        font-size: 0.92rem;
        color: #ccccee;
    }
    .stButton > button {
        background: linear-gradient(90deg, #6a3fdb, #1a6fcc) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a2fcb, #0a5fbc) !important;
        box-shadow: 0 4px 14px rgba(100,80,200,0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Лабораторная работа №2: Принятие решений в условиях неопределенности")
st.markdown("---")

if 'calculated' not in st.session_state:
    st.session_state.calculated = False

# ------------------- Ввод матрицы Q -------------------
st.header("📥 Ввод матрицы последствий Q (размерность 4×4)")
st.markdown('<div class="explanation">Введите значения матрицы последствий Q, где строки — решения (A₁–A₄), столбцы — состояния среды (S₁–S₄).</div>', unsafe_allow_html=True)
st.markdown("")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.subheader("S₁")
    q11 = st.number_input("A₁,S₁", value=80, key="q11", step=5)
    q21 = st.number_input("A₂,S₁", value=65, key="q21", step=5)
    q31 = st.number_input("A₃,S₁", value=95, key="q31", step=5)
    q41 = st.number_input("A₄,S₁", value=60, key="q41", step=5)
with col2:
    st.subheader("S₂")
    q12 = st.number_input("A₁,S₂", value=70, key="q12", step=5)
    q22 = st.number_input("A₂,S₂", value=90, key="q22", step=5)
    q32 = st.number_input("A₃,S₂", value=85, key="q32", step=5)
    q42 = st.number_input("A₄,S₂", value=75, key="q42", step=5)
with col3:
    st.subheader("S₃")
    q13 = st.number_input("A₁,S₃", value=85, key="q13", step=5)
    q23 = st.number_input("A₂,S₃", value=60, key="q23", step=5)
    q33 = st.number_input("A₃,S₃", value=70, key="q33", step=5)
    q43 = st.number_input("A₄,S₃", value=80, key="q43", step=5)
with col4:
    st.subheader("S₄")
    q14 = st.number_input("A₁,S₄", value=75, key="q14", step=5)
    q24 = st.number_input("A₂,S₄", value=80, key="q24", step=5)
    q34 = st.number_input("A₃,S₄", value=90, key="q34", step=5)
    q44 = st.number_input("A₄,S₄", value=95, key="q44", step=5)

Q = np.array([
    [q11, q12, q13, q14],
    [q21, q22, q23, q24],
    [q31, q32, q33, q34],
    [q41, q42, q43, q44]
], dtype=float)

st.markdown("---")

# ------------------- Вероятности -------------------
st.header("🎲 Ввод вероятностей состояний среды pⱼ (опционально)")
st.markdown('<div class="explanation">Если вероятности состояний среды известны, задайте их ниже — это позволит рассчитать ожидаемый доход и ожидаемые сожаления (раздел 3).</div>', unsafe_allow_html=True)
st.markdown("")
use_probs = st.checkbox("Задать вероятности состояний среды", value=True)

probs = None
if use_probs:
    colp1, colp2, colp3, colp4 = st.columns(4)
    with colp1:
        p1 = st.number_input("p₁", value=0.2, step=0.05, format="%.2f")
    with colp2:
        p2 = st.number_input("p₂", value=0.3, step=0.05, format="%.2f")
    with colp3:
        p3 = st.number_input("p₃", value=0.4, step=0.05, format="%.2f")
    with colp4:
        p4 = st.number_input("p₄", value=0.1, step=0.05, format="%.2f")

    probs = np.array([p1, p2, p3, p4])
    if abs(probs.sum() - 1.0) > 0.01:
        st.warning(f"⚠️ Сумма вероятностей = {probs.sum():.3f} ≠ 1. Будет выполнена нормализация.")
        probs = probs / probs.sum()
        st.info(f"Нормализованные вероятности: [{probs[0]:.3f}, {probs[1]:.3f}, {probs[2]:.3f}, {probs[3]:.3f}]")
else:
    st.info("ℹ️ Вероятности не заданы. Будут рассчитаны только критерии Вальда, Сэвиджа и Гурвица.")

st.markdown("---")

col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    calculate = st.button("🧮 ВЫПОЛНИТЬ РАСЧЕТ", use_container_width=True, type="primary")

st.markdown("---")

# ------------------- Функции -------------------
def build_risk_matrix(Q):
    return Q.max(axis=0) - Q

def wald_criterion(Q):
    v = Q.min(axis=1)
    best = float(v.max())
    return v, best, np.where(v == best)[0]

def savage_criterion(R):
    v = R.max(axis=1)
    best = float(v.min())
    return v, best, np.where(v == best)[0]

def hurwicz_criterion(Q, lam):
    H = lam * Q.max(axis=1) + (1 - lam) * Q.min(axis=1)
    best = float(H.max())
    return H, best, np.where(H == best)[0]

def expected_value_criterion(Q, probs):
    MQ = Q @ probs
    best = float(MQ.max())
    return MQ, best, np.where(MQ == best)[0]

def expected_regret_criterion(R, probs):
    MR = R @ probs
    best = float(MR.min())
    return MR, best, np.where(MR == best)[0]

# ------------------- Расчёт -------------------
if calculate:
    st.session_state.calculated = True
    R = build_risk_matrix(Q)
    st.session_state.R = R
    st.session_state.Q = Q
    st.session_state.wald_min, st.session_state.wald_best_val, st.session_state.wald_best_idx = wald_criterion(Q)
    st.session_state.savage_max, st.session_state.savage_best_val, st.session_state.savage_best_idx = savage_criterion(R)
    st.session_state.hurwicz_results = {}
    for lam in [0.2, 0.5, 0.8]:
        H, bv, bi = hurwicz_criterion(Q, lam)
        st.session_state.hurwicz_results[lam] = {'H': H, 'best_val': bv, 'best_idx': bi}
    if use_probs and probs is not None:
        st.session_state.MQ, st.session_state.MQ_best_val, st.session_state.MQ_best_idx = expected_value_criterion(Q, probs)
        st.session_state.MR, st.session_state.MR_best_val, st.session_state.MR_best_idx = expected_regret_criterion(R, probs)
    st.session_state.use_probs = use_probs
    st.session_state.probs = probs
    st.rerun()

# ------------------- Результаты -------------------
if st.session_state.calculated:

    st.header("1. Матрица последствий Q и матрица рисков R")
    st.markdown('<div class="explanation">📌 <b>Матрица Q</b> — исходные данные. <b>Матрица рисков R</b> строится по формуле: rᵢⱼ = max(qₖⱼ) − qᵢⱼ — показывает упущенную выгоду при выборе Aᵢ вместо наилучшего решения при состоянии Sⱼ.</div>', unsafe_allow_html=True)
    st.markdown("")
    col_q, col_r = st.columns(2)
    with col_q:
        st.subheader("Матрица последствий Q")
        st.dataframe(pd.DataFrame(st.session_state.Q, index=[f"A{i+1}" for i in range(4)], columns=[f"S{j+1}" for j in range(4)]), use_container_width=True)
    with col_r:
        st.subheader("Матрица рисков R")
        st.dataframe(pd.DataFrame(st.session_state.R, index=[f"A{i+1}" for i in range(4)], columns=[f"S{j+1}" for j in range(4)]), use_container_width=True)

    st.markdown("---")
    st.header("2. Оптимальные решения в условиях полной неопределенности")
    st.markdown('<div class="explanation">Вероятности состояний среды неизвестны. Применяются критерии, основанные на пессимизме, осторожности или балансе оптимизма и пессимизма.</div>', unsafe_allow_html=True)
    st.markdown("")

    # Вальд
    st.subheader("🛡️ Критерий Вальда (максиминный)")
    st.markdown('<div class="explanation">Для каждого решения берётся <b>минимальный выигрыш</b>. Выбирается решение с <b>максимальным из минимумов</b>. Позиция крайнего пессимизма — «рассчитывай на худшее». Применяется, когда цена ошибки очень высока.</div>', unsafe_allow_html=True)
    st.markdown("")
    st.dataframe(pd.DataFrame({"Решение": [f"A{i+1}" for i in range(4)], "min по строке (худший исход)": st.session_state.wald_min.astype(float)}), use_container_width=True)
    st.success(f"✅ **Оптимальное решение по Вальду:** A{st.session_state.wald_best_idx[0]+1} — гарантированный минимальный выигрыш = **{st.session_state.wald_best_val:.0f}**")

    st.markdown("---")

    # Сэвидж
    st.subheader("⚖️ Критерий Сэвиджа (минимаксный риска)")
    st.markdown('<div class="explanation">Для каждого решения берётся <b>максимальное сожаление</b> из матрицы R. Выбирается решение с <b>минимальным из максимальных сожалений</b>. ЛПР стремится не упустить лучший вариант.</div>', unsafe_allow_html=True)
    st.markdown("")
    st.dataframe(pd.DataFrame({"Решение": [f"A{i+1}" for i in range(4)], "max сожаление по строке": st.session_state.savage_max.astype(float)}), use_container_width=True)
    st.success(f"✅ **Оптимальное решение по Сэвиджу:** A{st.session_state.savage_best_idx[0]+1} — максимальное сожаление = **{st.session_state.savage_best_val:.0f}**")

    st.markdown("---")

    # Гурвиц
    st.subheader("🎯 Критерий Гурвица (пессимизм-оптимизм)")
    st.markdown('<div class="explanation">Формула: H = λ·max + (1−λ)·min. Коэффициент λ — степень оптимизма: λ=0 совпадает с Вальдом, λ=1 — полный оптимизм, λ=0.5 — нейтральная позиция.</div>', unsafe_allow_html=True)
    st.markdown("")
    for lam in [0.2, 0.5, 0.8]:
        label = {0.2: "пессимист", 0.5: "нейтральный", 0.8: "оптимист"}[lam]
        st.write(f"**λ = {lam}** ({label})")
        st.dataframe(pd.DataFrame({"Решение": [f"A{i+1}" for i in range(4)], f"H (λ={lam})": st.session_state.hurwicz_results[lam]['H'].astype(float)}), use_container_width=True)
        st.success(f"✅ **Оптимум (λ={lam}):** A{st.session_state.hurwicz_results[lam]['best_idx'][0]+1} — H = **{st.session_state.hurwicz_results[lam]['best_val']:.1f}**")
        st.markdown("")

    st.markdown("---")

    # MQ и MR
    if st.session_state.use_probs and st.session_state.probs is not None:
        st.header("3. Оптимальные решения в условиях частичной неопределенности")
        p = st.session_state.probs
        st.markdown('<div class="explanation">Вероятности состояний известны. Рассчитываются математические ожидания: ожидаемый доход MQᵢ и ожидаемые сожаления MRᵢ.</div>', unsafe_allow_html=True)
        st.markdown("")
        st.write(f"**Вероятности:** p₁={p[0]:.3f}, p₂={p[1]:.3f}, p₃={p[2]:.3f}, p₄={p[3]:.3f}")

        col_mq, col_mr = st.columns(2)
        with col_mq:
            st.subheader("💰 Ожидаемый доход MQᵢ")
            st.markdown('<div class="explanation">MQᵢ = Σ Qᵢⱼ·pⱼ. Выбирается решение с <b>максимальным MQ</b>.</div>', unsafe_allow_html=True)
            st.markdown("")
            st.dataframe(pd.DataFrame({"Решение": [f"A{i+1}" for i in range(4)], "MQᵢ": st.session_state.MQ.astype(float)}), use_container_width=True)
            st.success(f"✅ **Оптимум по MQ:** A{st.session_state.MQ_best_idx[0]+1} — MQ = **{st.session_state.MQ_best_val:.2f}**")
        with col_mr:
            st.subheader("😟 Ожидаемые сожаления MRᵢ")
            st.markdown('<div class="explanation">MRᵢ = Σ Rᵢⱼ·pⱼ. Выбирается решение с <b>минимальным MR</b>.</div>', unsafe_allow_html=True)
            st.markdown("")
            st.dataframe(pd.DataFrame({"Решение": [f"A{i+1}" for i in range(4)], "MRᵢ": st.session_state.MR.astype(float)}), use_container_width=True)
            st.success(f"✅ **Оптимум по MR:** A{st.session_state.MR_best_idx[0]+1} — MR = **{st.session_state.MR_best_val:.2f}**")

        st.markdown("---")
        st.header("4. Подтверждение теоремы эквивалентности")
        st.markdown('<div class="explanation">Теорема: решение, максимизирующее MQ, одновременно минимизирует MR — оба критерия <b>эквивалентны</b> при известных вероятностях.</div>', unsafe_allow_html=True)
        st.markdown("")
        if np.array_equal(np.sort(st.session_state.MQ_best_idx), np.sort(st.session_state.MR_best_idx)):
            st.success("✅ **Теорема эквивалентности подтверждена!** Оптимальные решения по MQ и MR совпадают.")
        else:
            st.warning(f"⚠️ Решения не совпадают. MQ: {', '.join([f'A{i+1}' for i in st.session_state.MQ_best_idx])} / MR: {', '.join([f'A{i+1}' for i in st.session_state.MR_best_idx])}")
        st.markdown("---")
    else:
        st.info("ℹ️ Раздел 3 не отображается — вероятности не заданы.")

    st.header("5. Анализ выбора разных стратегий")
    st.markdown("""<div class="explanation">
<b>Почему в разных условиях выбираются разные стратегии?</b><br><br>
🛡️ <b>Вальд</b> — крайний пессимизм, защита от худшего. <i>Пример: страховщик гарантирует себе защиту от катастрофических убытков.</i><br><br>
⚖️ <b>Сэвидж</b> — минимизация «горечи сожаления» об упущенной выгоде. ЛПР боится не столько проиграть, сколько упустить лучшее.<br><br>
🎯 <b>Гурвиц</b> — гибкий баланс. При λ→0 совпадает с Вальдом, при λ→1 — выбирается максимально возможный выигрыш.<br><br>
💰 <b>MQ и MR</b> — при известных вероятностях, нейтральное отношение к риску. <i>Пример: клиент при страховании груза ориентируется на ожидаемый доход, а не на худший сценарий.</i>
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Лабораторная работа №2: Принятие решений в условиях неопределенности")

else:
    st.info("👆 Введите данные и нажмите кнопку «ВЫПОЛНИТЬ РАСЧЕТ» для отображения результатов")