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
    .step-box {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(136,119,238,0.3);
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        font-size: 0.88rem;
        color: #ddeeff;
        font-family: monospace;
    }
    .step-header {
        background: rgba(100,80,200,0.2);
        border-left: 4px solid #6699ff;
        border-radius: 0 6px 6px 0;
        padding: 6px 14px;
        margin: 10px 0 6px 0;
        font-size: 0.85rem;
        color: #aaccff;
        font-weight: bold;
    }
    .formula-box {
        background: rgba(0,0,0,0.3);
        border: 1px solid rgba(100,200,100,0.3);
        border-radius: 6px;
        padding: 8px 14px;
        margin: 6px 0;
        font-size: 0.87rem;
        color: #aaffcc;
        font-family: monospace;
        white-space: pre-wrap;
    }
    .highlight-best {
        background: rgba(0,200,100,0.15);
        border-left: 3px solid #00cc66;
        padding: 4px 10px;
        border-radius: 0 4px 4px 0;
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
    .checkbox-hint {
        background: rgba(255,200,50,0.08);
        border-left: 3px solid #ffcc33;
        border-radius: 0 6px 6px 0;
        padding: 7px 14px;
        margin: 4px 0 8px 0;
        font-size: 0.85rem;
        color: #ffe88a;
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
])

st.markdown("---")

# ------------------- Опция детальных шагов -------------------
st.header("⚙️ Настройки отображения")

st.markdown("""
<div class="checkbox-hint">
☑️ <b>Галочка «Показывать детальные вычисления»</b>:<br>
• <b>Включена</b> — под каждым результатом появятся все промежуточные шаги: 
  поэлементные формулы, пошаговые арифметические выражения для каждой строки/столбца,
  объяснение откуда берётся каждое число. Удобно для проверки и понимания метода.<br>
• <b>Выключена</b> — отображаются только итоговые таблицы и оптимальные решения, 
  без промежуточных вычислений. Удобно для быстрого просмотра результатов.
</div>
""", unsafe_allow_html=True)

show_steps = st.checkbox("🔍 Показывать детальные вычисления (все промежуточные шаги)", value=True)

st.markdown("---")

# ------------------- Вероятности -------------------
st.header("🎲 Ввод вероятностей состояний среды pⱼ (опционально)")

st.markdown("""
<div class="checkbox-hint">
☑️ <b>Галочка «Задать вероятности состояний среды»</b>:<br>
• <b>Включена</b> — становятся доступны поля ввода вероятностей p₁–p₄. 
  Будут рассчитаны разделы 3 и 4: ожидаемый доход MQ, ожидаемые сожаления MR 
  и проверка теоремы эквивалентности. Это соответствует ситуации <i>частичной неопределённости</i> 
  (вероятности состояний известны).<br>
• <b>Выключена</b> — вероятности не задаются, разделы 3 и 4 не отображаются. 
  Рассчитываются только критерии полной неопределённости: Вальда, Сэвиджа и Гурвица.
</div>
""", unsafe_allow_html=True)

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

col_button1, col_button2, col_button3 = st.columns([1, 2, 1])
with col_button2:
    calculate = st.button("🚀 ВЫПОЛНИТЬ РАСЧЕТ", use_container_width=True, type="primary")

st.markdown("---")

# ------------------- Функции расчета -------------------
def build_risk_matrix(Q):
    max_by_col = Q.max(axis=0)
    R = max_by_col - Q
    return R, max_by_col

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
    return H, best_value, best_indices, max_per_row, min_per_row

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

# ------------------- Вспомогательные функции для вывода шагов -------------------
def show_risk_matrix_steps(Q, R, col_max):
    st.markdown('<div class="step-header">📐 Шаг 1: Находим максимум по каждому столбцу (наилучший исход при данном состоянии Sⱼ)</div>', unsafe_allow_html=True)
    lines = []
    for j in range(4):
        vals = ", ".join([str(int(Q[i,j])) for i in range(4)])
        lines.append(f"  max по S{j+1}: max({vals}) = {int(col_max[j])}")
    st.markdown('<div class="formula-box">' + "\n".join(lines) + '</div>', unsafe_allow_html=True)

    st.markdown('<div class="step-header">📐 Шаг 2: Вычисляем rᵢⱼ = max(qₖⱼ) − qᵢⱼ  для каждой ячейки</div>', unsafe_allow_html=True)
    for i in range(4):
        parts = []
        for j in range(4):
            parts.append(f"r{i+1}{j+1} = {int(col_max[j])} − {int(Q[i,j])} = {int(R[i,j])}")
        row_str = "  |  ".join(parts)
        st.markdown(f'<div class="formula-box">A{i+1}:  {row_str}</div>', unsafe_allow_html=True)

def show_wald_steps(Q, wald_min, wald_best_val, wald_best_idx):
    st.markdown('<div class="step-header">📐 Шаг 1: Находим минимум по каждой строке матрицы Q</div>', unsafe_allow_html=True)
    for i in range(4):
        vals = ", ".join([str(int(Q[i,j])) for j in range(4)])
        marker = " ← наилучший" if i in wald_best_idx else ""
        st.markdown(f'<div class="formula-box">A{i+1}: min({vals}) = {int(wald_min[i])}{marker}</div>', unsafe_allow_html=True)

    st.markdown('<div class="step-header">📐 Шаг 2: Выбираем максимум из найденных минимумов (maximin)</div>', unsafe_allow_html=True)
    mins_str = ", ".join([str(int(v)) for v in wald_min])
    st.markdown(f'<div class="formula-box">max({mins_str}) = {int(wald_best_val)}  →  Оптимум: A{wald_best_idx[0]+1}</div>', unsafe_allow_html=True)

def show_savage_steps(R, savage_max, savage_best_val, savage_best_idx):
    st.markdown('<div class="step-header">📐 Шаг 1: Находим максимальное сожаление по каждой строке матрицы R</div>', unsafe_allow_html=True)
    for i in range(4):
        vals = ", ".join([str(int(R[i,j])) for j in range(4)])
        marker = " ← наилучший" if i in savage_best_idx else ""
        st.markdown(f'<div class="formula-box">A{i+1}: max({vals}) = {int(savage_max[i])}{marker}</div>', unsafe_allow_html=True)

    st.markdown('<div class="step-header">📐 Шаг 2: Выбираем минимум из найденных максимумов (minimax риска)</div>', unsafe_allow_html=True)
    maxs_str = ", ".join([str(int(v)) for v in savage_max])
    st.markdown(f'<div class="formula-box">min({maxs_str}) = {int(savage_best_val)}  →  Оптимум: A{savage_best_idx[0]+1}</div>', unsafe_allow_html=True)

def show_hurwicz_steps(Q, lam, H, best_val, best_idx, row_max, row_min):
    st.markdown(f'<div class="step-header">📐 Шаг 1: Находим max и min по каждой строке (для λ = {lam})</div>', unsafe_allow_html=True)
    for i in range(4):
        vals = ", ".join([str(int(Q[i,j])) for j in range(4)])
        st.markdown(f'<div class="formula-box">A{i+1}: max({vals}) = {int(row_max[i])},  min = {int(row_min[i])}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="step-header">📐 Шаг 2: Вычисляем H = {lam}·max + {round(1-lam,1)}·min</div>', unsafe_allow_html=True)
    for i in range(4):
        marker = " ← оптимум" if i in best_idx else ""
        val_str = f"{lam}·{int(row_max[i])} + {round(1-lam,1)}·{int(row_min[i])} = {lam*row_max[i]:.1f} + {(1-lam)*row_min[i]:.1f} = {H[i]:.1f}"
        st.markdown(f'<div class="formula-box">A{i+1}: {val_str}{marker}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="step-header">📐 Шаг 3: Выбираем максимум критерия Гурвица</div>', unsafe_allow_html=True)
    h_str = ", ".join([f"{v:.1f}" for v in H])
    st.markdown(f'<div class="formula-box">max({h_str}) = {best_val:.1f}  →  Оптимум: A{best_idx[0]+1}</div>', unsafe_allow_html=True)

def show_mq_steps(Q, probs, MQ, best_val, best_idx):
    st.markdown('<div class="step-header">📐 Шаг 1: Вычисляем MQᵢ = q₁·p₁ + q₂·p₂ + q₃·p₃ + q₄·p₄</div>', unsafe_allow_html=True)
    for i in range(4):
        terms = " + ".join([f"{int(Q[i,j])}·{probs[j]:.3f}" for j in range(4)])
        parts = " + ".join([f"{Q[i,j]*probs[j]:.3f}" for j in range(4)])
        marker = " ← максимум" if i in best_idx else ""
        st.markdown(f'<div class="formula-box">MQ{i+1} = {terms}\n      = {parts}\n      = {MQ[i]:.4f}{marker}</div>', unsafe_allow_html=True)

    st.markdown('<div class="step-header">📐 Шаг 2: Выбираем решение с максимальным ожидаемым доходом</div>', unsafe_allow_html=True)
    mq_str = ", ".join([f"{v:.4f}" for v in MQ])
    st.markdown(f'<div class="formula-box">max({mq_str}) = {best_val:.4f}  →  Оптимум: A{best_idx[0]+1}</div>', unsafe_allow_html=True)

def show_mr_steps(R, probs, MR, best_val, best_idx):
    st.markdown('<div class="step-header">📐 Шаг 1: Вычисляем MRᵢ = r₁·p₁ + r₂·p₂ + r₃·p₃ + r₄·p₄</div>', unsafe_allow_html=True)
    for i in range(4):
        terms = " + ".join([f"{int(R[i,j])}·{probs[j]:.3f}" for j in range(4)])
        parts = " + ".join([f"{R[i,j]*probs[j]:.3f}" for j in range(4)])
        marker = " ← минимум" if i in best_idx else ""
        st.markdown(f'<div class="formula-box">MR{i+1} = {terms}\n      = {parts}\n      = {MR[i]:.4f}{marker}</div>', unsafe_allow_html=True)

    st.markdown('<div class="step-header">📐 Шаг 2: Выбираем решение с минимальными ожидаемыми сожалениями</div>', unsafe_allow_html=True)
    mr_str = ", ".join([f"{v:.4f}" for v in MR])
    st.markdown(f'<div class="formula-box">min({mr_str}) = {best_val:.4f}  →  Оптимум: A{best_idx[0]+1}</div>', unsafe_allow_html=True)

# ------------------- Расчёт при нажатии -------------------
if calculate:
    st.session_state.calculated = True

    R, col_max = build_risk_matrix(Q)
    wald_min, wald_best_val, wald_best_idx = wald_criterion(Q)
    savage_max, savage_best_val, savage_best_idx = savage_criterion(R)

    hurwicz_results = {}
    for lam in [0.2, 0.5, 0.8]:
        H, best_val, best_idx, row_max, row_min = hurwicz_criterion(Q, lam)
        hurwicz_results[lam] = {
            'H': H, 'best_val': best_val, 'best_idx': best_idx,
            'row_max': row_max, 'row_min': row_min
        }

    if use_probs and probs is not None:
        MQ, MQ_best_val, MQ_best_idx = expected_value_criterion(Q, probs)
        MR, MR_best_val, MR_best_idx = expected_regret_criterion(R, probs)

    st.session_state.R = R
    st.session_state.col_max = col_max
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
    st.session_state.show_steps = show_steps

    st.rerun()

# ------------------- Вывод результатов -------------------
if st.session_state.calculated:

    _Q = st.session_state.Q
    _R = st.session_state.R
    _col_max = st.session_state.col_max
    _show_steps = st.session_state.show_steps

    # 1. Матрицы Q и R
    st.header("1. Матрица последствий Q и матрица рисков R")
    st.markdown('<div class="explanation">📌 <b>Матрица Q</b> — исходные данные. <b>Матрица рисков R</b> строится по формуле: rᵢⱼ = max(qₖⱼ) − qᵢⱼ — показывает упущенную выгоду при выборе Aᵢ вместо наилучшего решения при состоянии Sⱼ.</div>', unsafe_allow_html=True)
    st.markdown("")

    col_q, col_r = st.columns(2)
    with col_q:
        st.subheader("Матрица последствий Q")
        df_Q = pd.DataFrame(_Q, index=[f"A{i+1}" for i in range(4)], columns=[f"S{j+1}" for j in range(4)])
        st.dataframe(df_Q, use_container_width=True)

    with col_r:
        st.subheader("Матрица рисков R")
        df_R = pd.DataFrame(_R, index=[f"A{i+1}" for i in range(4)], columns=[f"S{j+1}" for j in range(4)])
        st.dataframe(df_R, use_container_width=True)

    if _show_steps:
        st.markdown("#### 🔢 Детальные вычисления: построение матрицы рисков R")
        show_risk_matrix_steps(_Q, _R, _col_max)

    st.markdown("---")

    # 2. Критерии полной неопределённости
    st.header("2. Оптимальные решения в условиях полной неопределенности")
    st.markdown('<div class="explanation">Вероятности состояний среды неизвестны. Применяются критерии, основанные на пессимизме, осторожности или балансе оптимизма и пессимизма.</div>', unsafe_allow_html=True)
    st.markdown("")

    # Критерий Вальда
    st.subheader("🛡️ Критерий Вальда (максиминный критерий)")
    st.markdown('<div class="explanation">Для каждого решения берётся <b>минимальный выигрыш</b>. Выбирается решение с <b>максимальным из минимумов</b>. Позиция крайнего пессимизма — «рассчитывай на худшее».</div>', unsafe_allow_html=True)
    st.markdown("")

    wald_df = pd.DataFrame({
        "Решение": [f"A{i+1}" for i in range(4)],
        "min(Q) по строке": st.session_state.wald_min
    })
    st.dataframe(wald_df, use_container_width=True)
    st.success(f"✅ **Оптимальное решение:** A{st.session_state.wald_best_idx[0]+1} (значение критерия = {st.session_state.wald_best_val:.0f})")
    if len(st.session_state.wald_best_idx) > 1:
        st.info(f"Альтернативные оптимальные решения: {', '.join([f'A{i+1}' for i in st.session_state.wald_best_idx])}")

    if _show_steps:
        st.markdown("#### 🔢 Детальные вычисления: критерий Вальда")
        show_wald_steps(_Q, st.session_state.wald_min, st.session_state.wald_best_val, st.session_state.wald_best_idx)

    st.markdown("---")

    # Критерий Сэвиджа
    st.subheader("⚖️ Критерий Сэвиджа (минимаксный критерий риска)")
    st.markdown('<div class="explanation">Для каждого решения берётся <b>максимальное сожаление</b> из матрицы R. Выбирается решение с <b>минимальным из максимальных сожалений</b>. ЛПР стремится не упустить лучший вариант.</div>', unsafe_allow_html=True)
    st.markdown("")

    savage_df = pd.DataFrame({
        "Решение": [f"A{i+1}" for i in range(4)],
        "max(R) по строке": st.session_state.savage_max
    })
    st.dataframe(savage_df, use_container_width=True)
    st.success(f"✅ **Оптимальное решение:** A{st.session_state.savage_best_idx[0]+1} (значение критерия = {st.session_state.savage_best_val:.0f})")
    if len(st.session_state.savage_best_idx) > 1:
        st.info(f"Альтернативные оптимальные решения: {', '.join([f'A{i+1}' for i in st.session_state.savage_best_idx])}")

    if _show_steps:
        st.markdown("#### 🔢 Детальные вычисления: критерий Сэвиджа")
        show_savage_steps(_R, st.session_state.savage_max, st.session_state.savage_best_val, st.session_state.savage_best_idx)

    st.markdown("---")

    # Критерий Гурвица
    st.subheader("🎯 Критерий Гурвица (критерий пессимизма-оптимизма)")
    st.markdown('<div class="explanation">Формула: H = λ·max + (1−λ)·min. Коэффициент λ — степень оптимизма: λ=0 совпадает с Вальдом, λ=1 — полный оптимизм, λ=0.5 — нейтральная позиция.</div>', unsafe_allow_html=True)
    st.markdown("")

    for lam in [0.2, 0.5, 0.8]:
        label = {0.2: "пессимист", 0.5: "нейтральный", 0.8: "оптимист"}[lam]
        st.write(f"**λ = {lam}** ({label})")
        hurw_df = pd.DataFrame({
            "Решение": [f"A{i+1}" for i in range(4)],
            f"max(Q)": st.session_state.hurwicz_results[lam]['row_max'],
            f"min(Q)": st.session_state.hurwicz_results[lam]['row_min'],
            f"H = {lam}·max + {round(1-lam,1)}·min": [round(v, 2) for v in st.session_state.hurwicz_results[lam]['H']]
        })
        st.dataframe(hurw_df, use_container_width=True)
        st.success(f"✅ **Оптимальное решение:** A{st.session_state.hurwicz_results[lam]['best_idx'][0]+1} (значение критерия = {st.session_state.hurwicz_results[lam]['best_val']:.1f})")
        if len(st.session_state.hurwicz_results[lam]['best_idx']) > 1:
            st.info(f"Альтернативные оптимальные решения: {', '.join([f'A{i+1}' for i in st.session_state.hurwicz_results[lam]['best_idx']])}")

        if _show_steps:
            st.markdown(f"#### 🔢 Детальные вычисления: критерий Гурвица (λ = {lam})")
            show_hurwicz_steps(
                _Q, lam,
                st.session_state.hurwicz_results[lam]['H'],
                st.session_state.hurwicz_results[lam]['best_val'],
                st.session_state.hurwicz_results[lam]['best_idx'],
                st.session_state.hurwicz_results[lam]['row_max'],
                st.session_state.hurwicz_results[lam]['row_min']
            )
        st.markdown("")

    st.markdown("---")

    # 3. Ожидаемый доход и ожидаемые сожаления
    if st.session_state.use_probs and st.session_state.probs is not None:
        _probs = st.session_state.probs

        st.header("3. Оптимальные решения в условиях частичной неопределенности")
        st.markdown('<div class="explanation">Вероятности состояний известны. Рассчитываются математические ожидания: ожидаемый доход MQᵢ и ожидаемые сожаления MRᵢ.</div>', unsafe_allow_html=True)
        st.markdown("")

        st.write(f"**Вероятности состояний:** p₁ = {_probs[0]:.3f}, p₂ = {_probs[1]:.3f}, p₃ = {_probs[2]:.3f}, p₄ = {_probs[3]:.3f}")
        st.write(f"**Проверка:** p₁ + p₂ + p₃ + p₄ = {_probs[0]:.3f} + {_probs[1]:.3f} + {_probs[2]:.3f} + {_probs[3]:.3f} = {_probs.sum():.3f}")

        col_mq, col_mr = st.columns(2)

        with col_mq:
            st.subheader("💰 Ожидаемый доход MQᵢ")
            st.markdown('<div class="explanation">MQᵢ = Σ Qᵢⱼ·pⱼ. Выбирается решение с <b>максимальным MQ</b>.</div>', unsafe_allow_html=True)
            st.markdown("")
            mq_df = pd.DataFrame({
                "Решение": [f"A{i+1}" for i in range(4)],
                "MQᵢ = Σ Qᵢⱼ·pⱼ": [round(v, 4) for v in st.session_state.MQ]
            })
            st.dataframe(mq_df, use_container_width=True)
            st.success(f"✅ **Оптимальное решение:** A{st.session_state.MQ_best_idx[0]+1} (макс. ожидаемый доход = {st.session_state.MQ_best_val:.4f})")
            if len(st.session_state.MQ_best_idx) > 1:
                st.info(f"Альтернативы: {', '.join([f'A{i+1}' for i in st.session_state.MQ_best_idx])}")

        with col_mr:
            st.subheader("😟 Ожидаемые сожаления MRᵢ")
            st.markdown('<div class="explanation">MRᵢ = Σ Rᵢⱼ·pⱼ. Выбирается решение с <b>минимальным MR</b>.</div>', unsafe_allow_html=True)
            st.markdown("")
            mr_df = pd.DataFrame({
                "Решение": [f"A{i+1}" for i in range(4)],
                "MRᵢ = Σ Rᵢⱼ·pⱼ": [round(v, 4) for v in st.session_state.MR]
            })
            st.dataframe(mr_df, use_container_width=True)
            st.success(f"✅ **Оптимальное решение:** A{st.session_state.MR_best_idx[0]+1} (мин. ожидаемые сожаления = {st.session_state.MR_best_val:.4f})")
            if len(st.session_state.MR_best_idx) > 1:
                st.info(f"Альтернативы: {', '.join([f'A{i+1}' for i in st.session_state.MR_best_idx])}")

        if _show_steps:
            st.markdown("#### 🔢 Детальные вычисления: ожидаемый доход MQ")
            show_mq_steps(_Q, _probs, st.session_state.MQ, st.session_state.MQ_best_val, st.session_state.MQ_best_idx)

            st.markdown("#### 🔢 Детальные вычисления: ожидаемые сожаления MR")
            show_mr_steps(_R, _probs, st.session_state.MR, st.session_state.MR_best_val, st.session_state.MR_best_idx)

        st.markdown("---")

        # 4. Теорема эквивалентности
        st.header("4. Подтверждение теоремы эквивалентности")
        st.markdown('<div class="explanation">Теорема: решение, максимизирующее MQ, одновременно минимизирует MR — оба критерия <b>эквивалентны</b> при известных вероятностях.</div>', unsafe_allow_html=True)
        st.markdown("")

        if _show_steps:
            st.markdown("#### 🔢 Проверка эквивалентности")
            mq_str = ", ".join([f"MQ{i+1}={v:.4f}" for i, v in enumerate(st.session_state.MQ)])
            mr_str = ", ".join([f"MR{i+1}={v:.4f}" for i, v in enumerate(st.session_state.MR)])
            st.markdown(f'<div class="formula-box">Ожидаемые доходы:     {mq_str}\nОжидаемые сожаления: {mr_str}\n\nАргмакс(MQ) = A{st.session_state.MQ_best_idx[0]+1},  Аргмин(MR) = A{st.session_state.MR_best_idx[0]+1}</div>', unsafe_allow_html=True)

        if np.array_equal(np.sort(st.session_state.MQ_best_idx), np.sort(st.session_state.MR_best_idx)):
            st.success("✅ **Теорема эквивалентности подтверждена!**")
            st.write("Оптимальные решения по критериям ожидаемого дохода и ожидаемых сожалений совпадают.")
        else:
            st.warning("⚠️ Оптимальные решения не совпадают. Возможна множественность оптимумов.")
            st.write(f"Оптимум по MQ: решения {', '.join([f'A{i+1}' for i in st.session_state.MQ_best_idx])}")
            st.write(f"Оптимум по MR: решения {', '.join([f'A{i+1}' for i in st.session_state.MR_best_idx])}")

        st.markdown("---")

    else:
        st.info("ℹ️ Раздел 3 не отображается — вероятности не заданы.")

    # 5. Сводная таблица
    st.header("5. Сводная таблица результатов")
    st.markdown('<div class="explanation">Сравнение оптимальных решений по всем критериям.</div>', unsafe_allow_html=True)

    summary_rows = [
        {"Критерий": "Вальда (maximin)", "Тип": "Полная неопр.", "Оптимум": f"A{st.session_state.wald_best_idx[0]+1}", "Значение": f"{st.session_state.wald_best_val:.0f}"},
        {"Критерий": "Сэвиджа (minimax риска)", "Тип": "Полная неопр.", "Оптимум": f"A{st.session_state.savage_best_idx[0]+1}", "Значение": f"{st.session_state.savage_best_val:.0f}"},
    ]
    for lam in [0.2, 0.5, 0.8]:
        label = {0.2: "пессимист", 0.5: "нейтральный", 0.8: "оптимист"}[lam]
        summary_rows.append({
            "Критерий": f"Гурвица (λ={lam}, {label})",
            "Тип": "Полная неопр.",
            "Оптимум": f"A{st.session_state.hurwicz_results[lam]['best_idx'][0]+1}",
            "Значение": f"{st.session_state.hurwicz_results[lam]['best_val']:.1f}"
        })
    if st.session_state.use_probs and st.session_state.probs is not None:
        summary_rows.append({"Критерий": "Ожидаемый доход MQ", "Тип": "Частичная неопр.", "Оптимум": f"A{st.session_state.MQ_best_idx[0]+1}", "Значение": f"{st.session_state.MQ_best_val:.4f}"})
        summary_rows.append({"Критерий": "Ожид. сожаления MR", "Тип": "Частичная неопр.", "Оптимум": f"A{st.session_state.MR_best_idx[0]+1}", "Значение": f"{st.session_state.MR_best_val:.4f}"})

    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)
    st.markdown("---")

    # 6. Анализ стратегий
    st.header("6. Анализ выбора разных стратегий в условиях неопределенности")
    st.markdown("""
    <div class="explanation">
    <b>Почему в разных условиях выбираются разные стратегии?</b><br><br>
    🛡️ <b>Вальд</b> — крайний пессимизм, защита от худшего. <i>Пример: страховщик гарантирует себе защиту от катастрофических убытков.</i><br><br>
    ⚖️ <b>Сэвидж</b> — минимизация «горечи сожаления» об упущенной выгоде. ЛПР боится не столько проиграть, сколько упустить лучшее.<br><br>
    🎯 <b>Гурвиц</b> — гибкий баланс. При λ→0 совпадает с Вальдом, при λ→1 — выбирается максимально возможный выигрыш.<br><br>
    💰 <b>MQ и MR</b> — при известных вероятностях, нейтральное отношение к риску. <i>Пример: клиент при страховании груза ориентируется на ожидаемый доход, а не на худший сценарий.</i>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Лабораторная работа №2: Принятие решений в условиях неопределенности")

else:
    st.info("👆 Введите данные и нажмите кнопку «ВЫПОЛНИТЬ РАСЧЕТ» для отображения результатов")