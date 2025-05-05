import streamlit as st
import random
import re

st.set_page_config(
    page_title="A1 Sprechen Chat Trainer",
    page_icon="🗣️",
    layout="centered"
)

st.title("🗣️ Goethe A1 Sprechen Chat Trainer")
st.subheader("By Learn Language Education Academy")

st.markdown("""
Welcome to your A1 Sprechen training app! 
Please type your answers and **record yourself speaking**. 
Then send your recording to your teacher via WhatsApp for feedback.
""")

st.info("📖 For more examples and pictures, check **Chapter 15 PDF** in your Google Classroom.")

# ------------------------- TEIL SELECTION -------------------------
teil = st.selectbox(
    "Choose the Sprechen part (Teil):",
    ["Teil 1 – Personal Introduction", "Teil 2 – Frage & Antwort", "Teil 3 – Bitte / Request"]
)

# ------------------------- DAILY TASK INFO -------------------------
if teil.startswith("Teil 2"):
    st.warning("Today: Complete 10 Thema + Wort pairs. You have 5 days to finish all 50.")
elif teil.startswith("Teil 3"):
    st.warning("Today: Complete 10 situations. You have 2 days to finish all 20.")

# ------------------------- PROMPT LISTS -------------------------

# Teil 2: 50 Thema + Wort
teil2_prompts = [
    ("Familie", "Bruder"), ("Essen", "Pizza"), ("Freizeit", "Schwimmen"), ("Wohnung", "Balkon"),
    ("Beruf", "Lehrer"), ("Reisen", "Hotel"), ("Sport", "Fußball"), ("Haustier", "Hund"),
    ("Stadt", "Park"), ("Kleidung", "Jacke"), ("Auto", "Fahrer"), ("Musik", "Gitarre"),
    ("Film", "Komödie"), ("Schule", "Lehrer"), ("Bücher", "Roman"), ("Arbeit", "Kollege"),
    ("Urlaub", "Strand"), ("Gesundheit", "Arzt"), ("Geburtstag", "Geschenk"), ("Hobby", "Lesen"),
    ("Einkaufen", "Supermarkt"), ("Computer", "Laptop"), ("Telefon", "Handy"), ("Essen", "Salat"),
    ("Getränk", "Wasser"), ("Sport", "Tennis"), ("Haus", "Küche"), ("Stadt", "Brücke"),
    ("Reise", "Flughafen"), ("Familie", "Schwester"), ("Auto", "Benzin"), ("Film", "Drama"),
    ("Schule", "Schüler"), ("Arbeit", "Chef"), ("Freizeit", "Kino"), ("Wohnung", "Fenster"),
    ("Beruf", "Ingenieur"), ("Haustier", "Katze"), ("Stadt", "Bibliothek"), ("Musik", "Klavier"),
    ("Bücher", "Krimi"), ("Arzt", "Krankenschwester"), ("Geburtstag", "Kuchen"), ("Hobby", "Malen"),
    ("Einkaufen", "Bäckerei"), ("Computer", "Bildschirm"), ("Telefon", "Anruf"), ("Getränk", "Tee"),
    ("Sport", "Basketball"), ("Haus", "Garten"),
    # Your requested Thema + Wort pairs:
    ("Zeit", "Uhr"), ("Adresse", "Goethe Straße"), ("Stadt", "Stade"), ("Haus", "schließen")
]

# Teil 3: 20 Situationen
teil3_prompts = [
    "Bitten Sie um Hilfe beim Tragen einer Tasche.",
    "Bitten Sie jemanden, das Fenster zu öffnen.",
    "Bitten Sie jemanden, das Licht auszumachen.",
    "Fragen Sie nach der Uhrzeit.",
    "Bitten Sie um ein Glas Wasser.",
    "Fragen Sie, ob jemand ein Foto machen kann.",
    "Bitten Sie jemanden, langsamer zu sprechen.",
    "Bitten Sie jemanden, die Tür zu schließen.",
    "Fragen Sie, ob jemand das Fenster öffnen kann.",
    "Bitten Sie jemanden, Ihnen den Weg zu zeigen.",
    "Bitten Sie jemanden, leiser zu sprechen.",
    "Bitten Sie um einen Stift.",
    "Bitten Sie um Hilfe beim Öffnen einer Flasche.",
    "Bitten Sie jemanden, die Musik leiser zu machen.",
    "Fragen Sie nach dem Preis eines Produkts.",
    "Bitten Sie jemanden, den Computer einzuschalten.",
    "Bitten Sie jemanden, die Tasche zu halten.",
    "Bitten Sie jemanden, Ihnen das Datum zu sagen.",
    "Fragen Sie, ob jemand die Tür aufhalten kann.",
    "Bitten Sie um Hilfe beim Tragen von Kisten."
]

# Teil 1 follow-up questions
teil1_questions = [
    ("Wie schreibt man Ihren Namen?", "teil1_q1"),
    ("Wie alt sind Sie?", "teil1_q2"),
    ("Wie ist Ihre Telefonnummer?", "teil1_q3"),
    ("Wie buchstabiert man Ihre Stadt?", "teil1_q4"),
    ("Wie alt ist Ihre Mutter?", "teil1_q5"),
    ("Welche Sprachen sprechen Sie?", "teil1_q6"),
    ("Was ist Ihr Hobby?", "teil1_q7"),
    ("Haben Sie Geschwister?", "teil1_q8")
]

# ------------------------- DAY SELECTION FOR TEIL 2 & TEIL 3 -------------------------

day = None

if teil.startswith("Teil 2"):
    day = st.selectbox(
        "Select your day (1 to 5):", ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
    )
elif teil.startswith("Teil 3"):
    day = st.selectbox(
        "Select your day (1 or 2):", ["Day 1", "Day 2"]
    )

# ------------------------- PROMPT FILTERING & CHAT PROMPTS -------------------------

if teil.startswith("Teil 1"):
    st.chat_message("assistant").markdown(
        "👩‍🏫 **Examiner:** Please introduce yourself. Use these keywords: **Name, Alter, Land, Wohnort, Sprachen, Beruf, Hobby**. Write 4–6 sentences."
    )
    student_intro = st.text_area("💬 Your introduction:", key="teil1_intro")

    # ---- Randomly select 2 follow-up questions ----
    selected_questions = random.sample(teil1_questions, 2)

    follow_up_answers = {}
    for question, key in selected_questions:
        st.chat_message("assistant").markdown(f"👩‍🏫 **Examiner:** {question}")
        follow_up_answers[key] = st.text_input("💬 Your answer:", key=key)

elif teil.startswith("Teil 2"):
    day_number = int(day.split()[1])
    start = (day_number - 1) * 10
    end = start + 10
    day_prompts = teil2_prompts[start:end]
    thema, wort = random.choice(day_prompts)

    st.chat_message("assistant").markdown(
        f"👩‍🏫 **Examiner:** Thema: **{thema}** | Wort: **{wort}**.\n\nPlease write a **question** and **answer** using the keyword."
    )

    # Clear previous answers if not already set
    if "teil2_frage" not in st.session_state:
        st.session_state["teil2_frage"] = ""
    if "teil2_antwort" not in st.session_state:
        st.session_state["teil2_antwort"] = ""

    frage = st.text_input("💬 Your question:", value=st.session_state["teil2_frage"], key="teil2_frage_input")
    antwort = st.text_input("💬 Your answer:", value=st.session_state["teil2_antwort"], key="teil2_antwort_input")

elif teil.startswith("Teil 3"):
    day_number = int(day.split()[1])
    start = (day_number - 1) * 10
    end = start + 10
    day_prompts = teil3_prompts[start:end]
    situation = random.choice(day_prompts)

    st.chat_message("assistant").markdown(
        f"👩‍🏫 **Examiner:** Situation: **{situation}**.\n\nPlease write a **request (question)** and a possible **answer**."
    )

    if "teil3_frage" not in st.session_state:
        st.session_state["teil3_frage"] = ""
    if "teil3_antwort" not in st.session_state:
        st.session_state["teil3_antwort"] = ""

    frage = st.text_input("💬 Your request (question):", value=st.session_state["teil3_frage"], key="teil3_frage_input")
    antwort = st.text_input("💬 Your answer:", value=st.session_state["teil3_antwort"], key="teil3_antwort_input")

# ------------------------- TEIL 1 ANALYSIS & SCORING -------------------------

if teil.startswith("Teil 1"):
    submitted = st.button("✅ Submit Teil 1")

    if submitted:
        if student_intro and all(follow_up_answers.values()):
            score = 25
            feedback = []

            keyword_checks = {
                "name": ["heiße", "ich bin"],
                "alter": ["jahre alt", "ich bin"],
                "land": ["aus"],
                "wohnort": ["wohne", "in"],
                "sprachen": ["spreche"],
                "beruf": ["arbeite", "lehrer", "student", "arzt", "fahrer"],
                "hobby": ["hobby", "gern", "liebe", "mag"]
            }

            missing = []
            for keyword, patterns in keyword_checks.items():
                if not any(pat in student_intro.lower() for pat in patterns):
                    missing.append(keyword)

            if missing:
                feedback.append(f"❌ Missing ideas: {', '.join(missing)}")
                score -= len(missing) * 2

            if not re.search(r"[.!?]", student_intro):
                feedback.append("❌ Please use punctuation marks.")
                score -= 1

            lowercase_nouns = re.findall(r' [a-z][a-z]+', student_intro)
            if lowercase_nouns:
                feedback.append("⚠️ Possible capitalization errors.")
                score -= 1

            score = max(score, 5)

            st.success("✅ You completed Teil 1.")
            st.markdown(f"**🎯 Your score: {score} / 25**")

            if feedback:
                st.error("Feedback:")
                for item in feedback:
                    st.write(item)
            else:
                st.success("Excellent! No major issues found.")

            st.info("💡 Please record yourself reading your introduction and answers. 📤 Send your recording to your teacher via WhatsApp.")

            st.session_state["teil1_score"] = score

        else:
            st.warning("Please complete your introduction and both follow-up answers before submitting.")

# ------------------------- TEIL 2 SPEAKING REMINDER + NEXT BUTTON -------------------------

elif teil.startswith("Teil 2"):
    if frage and antwort:
        st.success("✅ Well done! You completed this Thema.")
        st.info("💡 Please read your **question and answer aloud** and record yourself. 📤 Send your recording to your teacher via WhatsApp.")

        if st.button("➡ Next Thema"):
            st.session_state["teil2_frage"] = ""
            st.session_state["teil2_antwort"] = ""
            st.session_state["teil2_completed"] = st.session_state.get("teil2_completed", 0) + 1
            st.rerun()

# ------------------------- TEIL 3 SPEAKING REMINDER + NEXT BUTTON -------------------------

elif teil.startswith("Teil 3"):
    if frage and antwort:
        st.success("✅ Well done! You completed this Situation.")
        st.info("💡 Please read your **request and answer aloud** and record yourself. 📤 Send your recording to your teacher via WhatsApp.")

        if st.button("➡ Next Situation"):
            st.session_state["teil3_frage"] = ""
            st.session_state["teil3_antwort"] = ""
            st.session_state["teil3_completed"] = st.session_state.get("teil3_completed", 0) + 1
            st.rerun()
