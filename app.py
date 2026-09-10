import gradio as gr
import random

# ---------------------------------------------------------
# منطق تحديد المرحلة اللي المستخدم وصلها في المحادثة
# ---------------------------------------------------------

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
    """بيبني جدول تعلم لمدة 30 يوم على حسب اختيارات المستخدم"""
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
    lines.append(f"## 📅 خطة تعلم الإنجليزية لمدة 30 يوم")
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


# ---------------------------------------------------------
# منطق البوت الحواري (بيسأل 3 أسئلة وبعدين يطلع الجدول)
# ---------------------------------------------------------

def chatbot_response(message, history):
    # نحسب هو في أي مرحلة بناءً على عدد الردود اللي فاتت
    step = len(history)

    if step == 0:
        return "أهلاً بيك! 👋 هساعدك تعمل جدول لتعلم الإنجليزية في شهر.\n\nإيه مستواك الحالي؟ (اكتب: مبتدئ / متوسط / متقدم)"

    if step == 1:
        return "تمام 👍\nكام ساعة تقريبًا تقدر تخصص للمذاكرة كل يوم؟ (اكتب رقم مثلاً: 1 أو 0.5)"

    if step == 2:
        options = " / ".join(FOCUS_OPTIONS)
        return f"جميل! وعايز تركز على إيه أكتر؟\nاختار من: {options}"

    if step == 3:
        # نجمع الإجابات من الهيستوري
        level = history[0][1] if False else None
        try:
            level_msg = history[0][0].strip()
        except Exception:
            level_msg = "مبتدئ"
        try:
            hours_msg = history[1][0].strip()
        except Exception:
            hours_msg = "1"
        focus_msg = message.strip()

        # نتأكد إن القيم منطقية، ولو مش موجودة في القوائم نسيبها زي ما هي
        level = level_msg if level_msg in LEVELS else level_msg
        focus = focus_msg if focus_msg in FOCUS_OPTIONS else "كل حاجة"

        schedule = build_schedule(level, hours_msg, focus)
        return schedule + "\n\nلو عايز جدول جديد بمواصفات مختلفة، اكتب أي حاجة وهبدأ معاك من الأول 🔁"

    # لو المحادثة كملت، نبدأ من جديد
    return "خلينا نبدأ جدول جديد 🎯\nإيه مستواك الحالي؟ (مبتدئ / متوسط / متقدم)"


# ---------------------------------------------------------
# واجهة Gradio
# ---------------------------------------------------------

demo = gr.ChatInterface(
    fn=chatbot_response,
    title="🎓 بوت جدول تعلم الإنجليزية",
    description="بوت بسيط بيسألك 3 أسئلة وبيطلعلك جدول تعلم إنجليزي لمدة شهر كامل.",
    examples=["مبتدئ", "متوسط", "متقدم"],
    theme="soft",
)

if __name__ == "__main__":
    demo.launch()
