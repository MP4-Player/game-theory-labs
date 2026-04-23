import streamlit as st
import pandas as pd
import numpy as np

# ------------------- Настройка страницы -------------------
st.set_page_config(page_title="Лабораторная работа №2", layout="wide")

# ------------------- Стили -------------------
st.markdown("""
<style>
    /* Светлый градиентный фон */
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #faf0ff 50%, #f0fff4 100%);
    }

    /* Заголовок страницы */
    h1 { color: #2c3e7a !important; font-size: 1.7rem !important; }
    h2 { color: #3a4a8a !important; }
    h3 { color: #5a4a9a !important; }

    /* Блок пояснения */
    .explanation {
        background: linear-gradient(90deg, #eef2ff 0%, #f5f0ff 100%);
        border-left: 4px solid #7c6fcd;
        border-radius: 0 8px 8px 0;
        padding: 10px 16px;
        margin-top: 6px;
        margin-bottom: 4px;
        font-size: 0.92rem;
        color: #3a3560;
    }

    /* Кнопка */
    .stButton > button {
        background: linear-gradient(90deg, #6a7fdb, #a06fcc) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fcb, #9060bc) !important;
        box-shadow: 0 4px 12px rgba(100,80,200,0.25) !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Лабораторная работа №2: Принятие решений в условиях неопределенности")
st.markdown("---")

# ------------------- Инициализация состояния сессии -------------------
if 'calculated' not in st.session_state:
    st.session_state.calculated = False

# ------------------- Ввод матрицы последствий Q -------------------
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

# ------------------- Ввод вероятностей -------------------
st.header("🎲 Ввод вероятностей состояний среды pⱼ (опционально)")
st.markdown('<div class="explanation">Если вероятности состояний среды известны, задайте их ниже. Это позволит рассчитать ожидаемый доход и ожидаемые сожаления (раздел 3).</div>', unsafe_allow_html=True)
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

# ------------------- Кнопка расчета -------------------
col_button1, col_button2, col_button3 = st.columns([1, 2, 1])
with col_button2:
    calculate = st.button("🧮 ВЫПОЛНИТЬ РАСЧЕТ", use_container_width=True, type="primary")

st.markdown("---")

# ------------------- Функции расчета -------------------
def build_risk_matrix(Q):
    max_by_col = Q.max(axis=0)
    R = max_by_col - Q
    return R

def wald_criterion(Q):
    min_per_row = Q.min(axis=1)
    best_value = float(min_per_row.max())
    best_indices = np.where(min_per_row == best_value)[0]
    return min_per_row, best_value, best_indices

def savage_criterion(R):
    max_per_row = R.max(axis=1)
    best_value = float(max_per_row.min())
    best_indices = np.where(max_per_row == best_value)[0]
    return max_per_row, best_value, best_indices

def hurwicz_criterion(Q, lambda_val):
    max_per_row = Q.max(axis=1)
    min_per_row = Q.min(axis=1)
    H = lambda_val * max_per_row + (1 - lambda_val) * min_per_row
    best_value = float(H.max())
    best_indices = np.where(H == best_value)[0]
    return H, best_value, best_indices

def expected_value_criterion(Q, probs):
    MQ = Q @ probs
    best_value = float(MQ.max())
    best_indices = np.where(MQ == best_value)[0]
    return MQ, best_value, best_indices

def expected_regret_criterion(R, probs):
    MR = R @ probs
    best_value = float(MR.min())
    best_indices = np.where(MR == best_value)[0]
    return MR, best_value, best_indices

# ------------------- Выполнение расчетов -------------------
if calculate:
    st.session_state.calculated = True

    R = build_risk_matrix(Q)
    wald_min, wald_best_val, wald_best_idx = wald_criterion(Q)
    savage_max, savage_best_val, savage_best_idx = savage_criterion(R)

    hurwicz_results = {}
    for lam in [0.2, 0.5, 0.8]:
        H, best_val, best_idx = hurwicz_criterion(Q, lam)
        hurwicz_results[lam] = {'H': H, 'best_val': best_val, 'best_idx': best_idx}

    if use_probs and probs is not None:
        MQ, MQ_best_val, MQ_best_idx = expected_value_criterion(Q, probs)
        MR, MR_best_val, MR_best_idx = expected_regret_criterion(R, probs)

    st.session_state.R = R
    st.session_state.wald_min = wald_min
    st.session_state.wald_best_val = wald_best_val
    st.session_state.wald_best_idx = wald_best_idx
    st.session_state.savage_max = savage_max
    st.session_state.savage_best_val = savage_best_val
    st.session_state.savage_best_idx = savage_best_idx
    st.session_state.hurwicz_results = hurwicz_results

    if use_probs and probs is not None:
        st.session_state.MQ = MQ
        st.session_state.MQ_best_val = MQ_best_val
        st.session_state.MQ_best_idx = MQ_best_idx
        st.session_state.MR = MR
        st.session_state.MR_best_val = MR_best_val
        st.session_state.MR_best_idx = MR_best_idx

    st.session_state.use_probs = use_probs
    st.session_state.probs = probs
    st.session_state.Q = Q

    st.rerun()

# ------------------- Отображение результатов -------------------
if st.session_state.calculated:

    # 1. Матрицы
    st.header("1. Матрица последствий Q и матрица рисков R")
    st.markdown('<div class="explanation">📌 <b>Матрица последствий Q</b> — исходные данные задачи. <b>Матрица рисков R</b> строится по формуле: <i>rᵢⱼ = max(qₖⱼ) − qᵢⱼ</i> — показывает упущенную выгоду при выборе решения Aᵢ вместо наилучшего при состоянии Sⱼ.</div>', unsafe_allow_html=True)
    st.markdown("")

    col_q, col_r = st.columns(2)
    with col_q:
        st.subheader("Матрица последствий Q")
        df_Q = pd.DataFrame(st.session_state.Q,
                            index=[f"A{i+1}" for i in range(4)],
                            columns=[f"S{j+1}" for j in range(4)])
        st.dataframe(df_Q, use_container_width=True)
    with col_r:
        st.subheader("Матрица рисков R")
        df_R = pd.DataFrame(st.session_state.R,
                            index=[f"A{i+1}" for i in range(4)],
                            columns=[f"S{j+1}" for j in range(4)])
        st.dataframe(df_R, use_container_width=True)

    st.markdown("---")

    # 2. Критерии
    st.header("2. Оптимальные решения в условиях полной неопределенности")
    st.markdown('<div class="explanation">В условиях <b>полной неопределенности</b> вероятности состояний среды неизвестны. Применяются критерии, основанные на пессимизме, осторожности или балансе оптимизма и пессимизма.</div>', unsafe_allow_html=True)
    st.markdown("")

    # Вальд
    st.subheader("🛡️ Критерий Вальда (максиминный критерий)")
    st.markdown('<div class="explanation">Для каждого решения берётся <b>минимальный выигрыш</b> по всем состояниям среды. Выбирается решение с <b>максимальным из минимумов</b>. Позиция крайнего пессимизма — «рассчитывай на худшее». Применяется, когда цена ошибки очень высока (например, при страховании).</div>', unsafe_allow_html=True)
    st.markdown("")
    wald_df = pd.DataFrame({
        "Решение": [f"A{i+1}" for i in range(4)],
        "min по строке (худший исход)": st.session_state.wald_min.astype(float)
    })
    st.dataframe(wald_df, use_container_width=True)
    st.success(f"✅ **Оптимальное решение по Вальду:** A{st.session_state.wald_best_idx[0]+1} — гарантированный минимальный выигрыш = **{st.session_state.wald_best_val:.0f}**")
    if len(st.session_state.wald_best_idx) > 1:
        st.info(f"Альтернативные оптимальные решения: {', '.join([f'A{i+1}' for i in st.session_state.wald_best_idx])}")

    st.markdown("---")

    # Сэвидж
    st.subheader("⚖️ Критерий Сэвиджа (минимаксный критерий риска)")
    st.markdown('<div class="explanation">Для каждого решения берётся <b>максимальное сожаление</b> (максимальная упущенная выгода из матрицы R). Выбирается решение с <b>минимальным из максимальных сожалений</b>. ЛПР стремится не столько выиграть, сколько <b>не упустить лучший вариант</b>.</div>', unsafe_allow_html=True)
    st.markdown("")
    savage_df = pd.DataFrame({
        "Решение": [f"A{i+1}" for i in range(4)],
        "max сожаление по строке": st.session_state.savage_max.astype(float)
    })
    st.dataframe(savage_df, use_container_width=True)
    st.success(f"✅ **Оптимальное решение по Сэвиджу:** A{st.session_state.savage_best_idx[0]+1} — максимальное сожаление = **{st.session_state.savage_best_val:.0f}**")
    if len(st.session_state.savage_best_idx) > 1:
        st.info(f"Альтернативные оптимальные решения: {', '.join([f'A{i+1}' for i in st.session_state.savage_best_idx])}")

    st.markdown("---")

    # Гурвиц
    st.subheader("🎯 Критерий Гурвица (критерий пессимизма-оптимизма)")
    st.markdown('<div class="explanation">Взвешивает <b>лучший и худший исходы</b> каждого решения по формуле: <i>H = λ·max + (1−λ)·min</i>. Коэффициент λ отражает степень оптимизма ЛПР: λ=0 — полный пессимизм (= критерий Вальда), λ=1 — полный оптимизм, λ=0.5 — нейтральная позиция.</div>', unsafe_allow_html=True)
    st.markdown("")

    for lam in [0.2, 0.5, 0.8]:
        label = {0.2: "пессимист", 0.5: "нейтральный", 0.8: "оптимист"}[lam]
        st.write(f"**λ = {lam}** ({label}: оптимизм = {lam}, пессимизм = {1-lam})")
        hurw_df = pd.DataFrame({
            "Решение": [f"A{i+1}" for i in range(4)],
            f"H (λ={lam})": st.session_state.hurwicz_results[lam]['H'].astype(float)
        })
        st.dataframe(hurw_df, use_container_width=True)
        st.success(f"✅ **Оптимальное решение (λ={lam}):** A{st.session_state.hurwicz_results[lam]['best_idx'][0]+1} — значение H = **{st.session_state.hurwicz_results[lam]['best_val']:.1f}**")
        if len(st.session_state.hurwicz_results[lam]['best_idx']) > 1:
            st.info(f"Альтернативные: {', '.join([f'A{i+1}' for i in st.session_state.hurwicz_results[lam]['best_idx']])}")
        st.markdown("")

    st.markdown("---")

    # 3. Ожидаемый доход и сожаления
    if st.session_state.use_probs and st.session_state.probs is not None:
        st.header("3. Оптимальные решения в условиях частичной неопределенности")
        p = st.session_state.probs
        st.markdown('<div class="explanation">В условиях <b>частичной неопределенности</b> вероятности состояний среды известны. Рассчитываются взвешенные средние: ожидаемый доход MQᵢ и ожидаемые сожаления MRᵢ.</div>', unsafe_allow_html=True)
        st.markdown("")
        st.write(f"**Вероятности состояний:** p₁ = {p[0]:.3f}, p₂ = {p[1]:.3f}, p₃ = {p[2]:.3f}, p₄ = {p[3]:.3f}")

        col_mq, col_mr = st.columns(2)

        with col_mq:
            st.subheader("💰 Ожидаемый доход MQᵢ")
            st.markdown('<div class="explanation">MQᵢ = Σ Qᵢⱼ·pⱼ — математическое ожидание дохода. Выбирается решение с <b>максимальным MQ</b>.</div>', unsafe_allow_html=True)
            st.markdown("")
            mq_df = pd.DataFrame({
                "Решение": [f"A{i+1}" for i in range(4)],
                "MQᵢ = Σ Qᵢⱼ·pⱼ": st.session_state.MQ.astype(float)
            })
            st.dataframe(mq_df, use_container_width=True)
            st.success(f"✅ **Оптимум по MQ:** A{st.session_state.MQ_best_idx[0]+1} — MQ = **{st.session_state.MQ_best_val:.2f}**")
            if len(st.session_state.MQ_best_idx) > 1:
                st.info(f"Альтернативные: {', '.join([f'A{i+1}' for i in st.session_state.MQ_best_idx])}")

        with col_mr:
            st.subheader("😟 Ожидаемые сожаления MRᵢ")
            st.markdown('<div class="explanation">MRᵢ = Σ Rᵢⱼ·pⱼ — математическое ожидание сожалений. Выбирается решение с <b>минимальным MR</b>.</div>', unsafe_allow_html=True)
            st.markdown("")
            mr_df = pd.DataFrame({
                "Решение": [f"A{i+1}" for i in range(4)],
                "MRᵢ = Σ Rᵢⱼ·pⱼ": st.session_state.MR.astype(float)
            })
            st.dataframe(mr_df, use_container_width=True)
            st.success(f"✅ **Оптимум по MR:** A{st.session_state.MR_best_idx[0]+1} — MR = **{st.session_state.MR_best_val:.2f}**")
            if len(st.session_state.MR_best_idx) > 1:
                st.info(f"Альтернативные: {', '.join([f'A{i+1}' for i in st.session_state.MR_best_idx])}")

        st.markdown("---")

        # 4. Теорема эквивалентности
        st.header("4. Подтверждение теоремы эквивалентности")
        st.markdown('<div class="explanation">Теорема утверждает: решение, максимизирующее ожидаемый доход MQ, одновременно минимизирует ожидаемые сожаления MR. То есть оба критерия <b>дают одинаковый результат</b> при известных вероятностях.</div>', unsafe_allow_html=True)
        st.markdown("")
        if np.array_equal(np.sort(st.session_state.MQ_best_idx), np.sort(st.session_state.MR_best_idx)):
            st.success("✅ **Теорема эквивалентности подтверждена!** Оптимальные решения по MQ и MR совпадают.")
        else:
            st.warning("⚠️ Оптимальные решения не совпадают. Возможна множественность оптимумов.")
            st.write(f"Оптимум по MQ: {', '.join([f'A{i+1}' for i in st.session_state.MQ_best_idx])}")
            st.write(f"Оптимум по MR: {', '.join([f'A{i+1}' for i in st.session_state.MR_best_idx])}")

        st.markdown("---")
    else:
        st.info("ℹ️ Раздел 3 не отображается — вероятности состояний среды не заданы.")

    # 5. Анализ стратегий
    st.header("5. Анализ выбора разных стратегий в условиях неопределенности")
    st.markdown("""
<div class="explanation">
<b>Почему в разных условиях неопределенности выбираются разные стратегии?</b><br><br>
🛡️ <b>Критерий Вальда</b> (максимин) — позиция крайнего пессимизма. Подходит для критически важных решений, где недопустимы потери. <i>Пример: страховщик при расчёте страхового возмещения гарантирует себе защиту от катастрофических убытков.</i><br><br>
⚖️ <b>Критерий Сэвиджа</b> — ЛПР боится не столько проиграть, сколько упустить лучший вариант. Ориентирован на минимизацию «горечи сожаления» об упущенной выгоде.<br><br>
🎯 <b>Критерий Гурвица</b> — гибкий инструмент. При λ→0 совпадает с Вальдом, при λ→1 выбирается решение с максимально возможным выигрышем. Позволяет настроить модель под конкретного ЛПР.<br><br>
💰 <b>Критерии MQ и MR</b> применяются при известных вероятностях и соответствуют нейтральному отношению к риску. <i>Пример: клиент при страховании груза ориентируется на ожидаемый доход, а не на худший сценарий.</i>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Лабораторная работа №2: Принятие решений в условиях неопределенности")

else:
    st.info("👆 Введите данные и нажмите кнопку «ВЫПОЛНИТЬ РАСЧЕТ» для отображения результатов")