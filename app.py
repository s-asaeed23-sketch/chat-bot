import streamlit as st
import random

st.set_page_config(page_title="بوت جدول تعلم الإنجليزية", page_icon="🎓")

LEVELS = ["مبتدئ", "متوسط", "متقدم"]
FOCUS_OPTIONS = ["مفردات", "قواعد", "محادثة", "استماع", "كل حاجة"]

VOCAB_TOPICS = [
    "كلمات يومية أساسية", "كلمات العمل والدراسة", "كلمات السفر",
    "كلمات المشاعر والوصف", "كلمات الأكل والصحة", "كلمات التكنولوجيا",
]

GRAMMAR_TOPICS = [
    "Present Simple", "Present Continuous", "Past Simple",
    "Future (will/going to)", "Present Perfect", "Modal Verbs",
    "Comparatives & Superlatives", "Conditionals (If)",
]


def build_schedule(level: str, hours: str, focus: str) -> str:
    try:
        hours_num = float(hours)
    except ValueError:
        hours_num = 1.0

    daily_activities = []
    if focus in ("مفردات", "كل حاجة"):
        daily_activities.append("15-20 دقيقة: حفظ ومراجعة كلمات جديدة")
    if focus in ("قواعد", "كل حاجة"):
        daily_activities.append("15-20 دقيقة: قاعدة نحوية + تمارين عليها")
    if focus in ("محادثة", "كل حاجة"):
        daily_activities.append("10-15 دقيقة: تدريب على المحادثة (مع نفسك أو تطبيق)")
    if focus in ("استماع", "كل حاجة"):
        daily_activities.append("10-15 دقيقة: سماع فيديو/بودكاست قصير بالإنجليزي")
    if not daily_activities:
        daily_activities = ["مراجعة عامة شاملة"]

    lines = []
    lines.append("## 📅 خطة تعلم الإنجليزية لمدة 30 يوم")
    lines.append(f"**المستوى:** {level}  |  **الوقت المتاح يوميًا:** {hours_num} ساعة  |  **التركيز:** {focus}\n")
    lines.append("### الأنشطة اليومية الثابتة:")
    for act in daily_activities:
        lines.append(f"- {act}")
    lines.append("")
    lines.append("### جدول تفصيلي أسبوعي:")
    for week in range(1, 5):
        lines.append(f"\n**الأسبوع {week}:**")
        for day in range(1, 8):
            day_num = (week - 1) * 7 + day
            if day_num > 30:
                break
            vocab = random.choice(VOCAB_TOPICS)
            grammar = random.choice(GRAMMAR_TOPICS)
            if day % 7 == 0:
                lines.append(f"- اليوم {day_num}: 🔄 مراجعة شاملة لكل اللي اتعلمته الأسبوع ده")
            else:
                extra = []
                if focus in ("مفردات", "كل حاجة"):
                    extra.append(f"مفردات: {vocab}")
                if focus in ("قواعد", "كل حاجة"):
                    extra.append(f"قاعدة: {grammar}")
                extra_txt = " | ".join(extra) if extra else "مراجعة عامة"
                lines.append(f"- اليوم {day_num}: {extra_txt}")

    lines.append("\n### نصايح:")
    lines.append("- حاول تلتزم بنفس الميعاد كل يوم عشان تتعود.")
    lines.append("- اكتب جملة أو اتنين بالكلمات الجديدة كل يوم.")
    lines.append("- في آخر كل أسبوع، اختبر نفسك من غير ما تشوف الملاحظات.")
    return "\n".join(lines)


st.title("🎓 بوت جدول تعلم الإنجليزية")
st.write("بوت بسيط بيسألك 3 أسئلة وبيطلعلك جدول تعلم إنجليزي لمدة شهر كامل.")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.step = 0
    st.session_state.messages.append(
        {"role": "assistant", "content": "أهلاً بيك! 👋 هساعدك تعمل جدول لتعلم الإنجليزية في شهر.\n\nإيه مستواك الحالي؟ (اكتب: مبتدئ / متوسط / متقدم)"}
    )

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("اكتب هنا...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    step = st.session_state.step

    if step == 0:
        st.session_state.level = user_input.strip()
        reply = "تمام 👍\nكام ساعة تقريبًا تقدر تخصص للمذاكرة كل يوم؟ (اكتب رقم مثلاً: 1 أو 0.5)"
    elif step == 1:
        st.session_state.hours = user_input.strip()
        options = " / ".join(FOCUS_OPTIONS)
        reply = f"جميل! وعايز تركز على إيه أكتر؟\nاختار من: {options}"
    elif step == 2:
        focus = user_input.strip() if user_input.strip() in FOCUS_OPTIONS else "كل حاجة"
        reply = build_schedule(st.session_state.level, st.session_state.hours, focus)
        reply += "\n\nلو عايز جدول جديد، اكتب أي حاجة وهبدأ معاك من الأول 🔁"
    else:
        st.session_state.step = -1
        reply = "خلينا نبدأ جدول جديد 🎯\nإيه مستواك الحالي؟ (مبتدئ / متوسط / متقدم)"

    st.session_state.step += 1
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
