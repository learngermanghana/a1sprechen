import streamlit as st
import random

st.set_page_config(
    page_title="A1 Sprechen Trainer",
    page_icon="🗣️",
    layout="centered"
)

st.title("🗣️ Goethe A1 Sprechen Trainer")
st.subheader("By Learn Language Education Academy")

st.info("Please enter your name:")
student_name = st.text_input("Your Name:")

if not student_name:
    st.stop()

st.success(f"Hello {student_name}! Good luck with your practice.")

st.warning("⚠️ Your progress is saved on this device. If you don’t clear cookies and continue using this device, your progress will stay saved.")

# ---------- Session state initialization ----------
if "teil2_done" not in st.session_state:
    st.session_state["teil2_done"] = []
if "teil3_done" not in st.session_state:
    st.session_state["teil3_done"] = []
if "teil1_done" not in st.session_state:
    st.session_state["teil1_done"] = False
if "teil2_today" not in st.session_state:
    st.session_state["teil2_today"] = []
if "teil3_today" not in st.session_state:
    st.session_state["teil3_today"] = []
if "teil2_index" not in st.session_state:
    st.session_state["teil2_index"] = 0
if "teil3_index" not in st.session_state:
    st.session_state["teil3_index"] = 0
if "submitted_valid" not in st.session_state:
    st.session_state["submitted_valid"] = False

teil = st.radio(
    "Which part would you like to practice?",
    ["Teil 1 – Personal Introduction", "Teil 2 – Question & Answer", "Teil 3 – Request & Response"]
)

# ---------- Prompts ----------
teil2_prompts = [
    ("Familie", "Bruder"), ("Essen", "Pizza"), ("Freizeit", "Schwimmen"), ("Wohnung", "Balkon"),
    ("Beruf", "Lehrer"), ("Reisen", "Hotel"), ("Sport", "Fußball"), ("Haustier", "Hund"), ("Stadt", "Park"),
    ("Kleidung", "Jacke"), ("Auto", "Fahrer"), ("Musik", "Gitarre"), ("Film", "Komödie"), ("Schule", "Lehrer"),
    ("Bücher", "Roman"), ("Arbeit", "Kollege"), ("Urlaub", "Strand"), ("Gesundheit", "Arzt"), ("Geburtstag", "Geschenk"),
    ("Hobby", "Lesen"), ("Einkaufen", "Supermarkt"), ("Computer", "Laptop"), ("Telefon", "Handy"), ("Essen", "Salat"),
    ("Getränk", "Wasser"), ("Sport", "Tennis"), ("Haus", "Küche"), ("Stadt", "Brücke"), ("Reise", "Flughafen"),
    ("Familie", "Schwester"), ("Auto", "Benzin"), ("Film", "Drama"), ("Schule", "Schüler"), ("Arbeit", "Chef"),
    ("Freizeit", "Kino"), ("Wohnung", "Fenster"), ("Beruf", "Ingenieur"), ("Haustier", "Katze"),
    ("Stadt", "Bibliothek"), ("Musik", "Klavier"), ("Bücher", "Krimi"), ("Arzt", "Krankenschwester"),
    ("Geburtstag", "Kuchen"), ("Hobby", "Malen"), ("Einkaufen", "Bäckerei"), ("Computer", "Bildschirm"),
    ("Telefon", "Anruf"), ("Getränk", "Tee"), ("Sport", "Basketball"), ("Haus", "Garten")
]

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

# ---------- Teil 1 ----------
if teil.startswith("Teil 1"):
    st.info("Speak about: Name, Age, Country, City, Languages, Job, Hobby.")
    intro = st.text_area("💬 Write your introduction:")

    st.write("**Please also answer these questions:**")
    frage1 = st.text_input("Wie alt ist Ihre Mutter?")
    frage2 = st.text_input("Wie buchstabiert man Ihren Namen?")
    frage3 = st.text_input("Wie ist Ihre Telefonnummer?")

    if st.button("✅ Submit"):
        feedback = []
        if not any(phrase in intro.lower() for phrase in ["ich heiße", "mein name ist"]):
            feedback.append("Your introduction should include 'Ich heiße...' or 'Mein Name ist...'.")
        keywords = ["alt", "wohne", "komme", "spreche", "arbeite", "hobby"]
        missing = [word for word in keywords if word not in intro.lower()]
        if missing:
            feedback.append("Missing info: " + ", ".join(missing))
        if not frage1.strip():
            feedback.append("Please answer: Wie alt ist Ihre Mutter?")
        if not frage2.strip():
            feedback.append("Please answer: Wie buchstabiert man Ihren Namen?")
        if not frage3.strip():
            feedback.append("Please answer: Wie ist Ihre Telefonnummer?")

        if feedback:
            for f in feedback:
                st.error(f)
        else:
            st.success("✅ Well done! Your introduction is complete.")
            st.session_state["teil1_done"] = True


# ---------- Teil 2 ----------
elif teil.startswith("Teil 2"):
    total = len(teil2_prompts)
    done = len(st.session_state["teil2_done"])
    st.info(f"Total Thema + Wort: {total}. You have completed {done}.")

    remaining = [p for p in teil2_prompts if p not in st.session_state["teil2_done"]]

    if not remaining:
        st.success("🎉 You have completed all available Thema + Wort in Teil 2! Excellent job. You can review or start Teil 3 now.")
        st.stop()

    if not st.session_state["teil2_today"]:
        max_today = len(remaining)
        st.info("How many questions would you like to practice today? Minimum 1.")
        num_today = st.number_input(
            "Number of Thema to practice today:",
            min_value=1,
            max_value=max_today if max_today >= 1 else max_today,
            step=1
        )

        if st.button("🎯 Start Today’s Practice"):
            st.session_state["teil2_today"] = random.sample(remaining, min(num_today, len(remaining)))
            st.session_state["teil2_index"] = 0
            st.session_state["submitted_valid"] = False

    elif st.session_state["teil2_today"]:
        index = st.session_state["teil2_index"]
        batch = st.session_state["teil2_today"]

        if index < len(batch):
            thema, wort = batch[index]
            st.info(f"📝 Thema: {thema} | Wort: {wort}")

            st.warning("👉 Please type both your **question** and **answer**. End your question with a **?** and your answer with a **.**")

            text = st.text_area(
                "💬 Your question + answer:",
                key=f"qa_{index}",
                placeholder="Example: Wo wohnen Sie? Ich wohne in Accra."
            )

            if st.button("✅ Submit"):
                feedback = []

                if "?" not in text or "." not in text:
                    feedback.append("Please use a question mark (?) and a full stop (.)")
                    st.session_state["submitted_valid"] = False
                else:
                    frage_part = text.split("?")[0].strip().lower()
                    antwort_part = text.split("?")[1].strip().lower()

                    if any(w in frage_part for w in ["bist", "hast", "kannst", "wohnst", "gehst", "spielst", "du "]):
                        feedback.append("Please use the formal 'Sie' form in your question.")

                    w_words = ["wann", "wo", "was", "wie", "warum", "welche"]
                    sie_starts = [
                        "haben sie", "ist das", "ist es", "sind sie", "gehen sie", "lesen sie", "schauen sie",
                        "arbeiten sie", "wohnen sie", "spielen sie", "trinken sie", "essen sie", "kaufen sie",
                        "können sie", "mögen sie", "dürfen sie", "müssen sie", "wollen sie", "sollen sie",
                        "möchten sie", "reisen sie", "fahren sie", "sprechen sie", "machen sie", "sehen sie",
                        "malen sie", "schwimmen sie", "zeichnen sie", "tanzen sie", "besuchen sie", "gibt es"
                    ]

                    separable_starts = [
                        "machen sie an", "machen sie auf", "machen sie aus", "machen sie zu",
                        "steigen sie ein", "steigen sie aus", "steigen sie um", "schalten sie ein",
                        "schalten sie aus", "sehen sie an", "schauen sie an", "anschauen sie"
                    ]

                    if not (
                        any(frage_part.startswith(w) for w in w_words) or
                        any(frage_part.startswith(s) for s in sie_starts) or
                        any(frage_part.startswith(s) for s in separable_starts)
                    ):
                        feedback.append("Your question should start with a W-word or a verb in Sie-form.")

                    if len(antwort_part.strip()) < 3:
                        feedback.append("Your answer seems too short or missing.")

                if feedback:
                    for f in feedback:
                        st.error(f)
                    st.session_state["submitted_valid"] = False
                else:
                    st.success("✅ Answer saved. Click 'Next' to continue.")
                    st.session_state["submitted_valid"] = True

            if st.button("➡ Next"):
                if st.session_state["submitted_valid"]:
                    if (thema, wort) not in st.session_state["teil2_done"]:
                        st.session_state["teil2_done"].append((thema, wort))
                    st.session_state["teil2_index"] += 1
                    st.session_state["submitted_valid"] = False
                else:
                    st.warning("Please submit a valid answer before continuing.")

        else:
            st.success(f"🎉 You completed {len(batch)} Thema today.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Start new batch"):
                    st.session_state["teil2_today"] = []
                    st.session_state["teil2_index"] = 0
            with col2:
                if st.button("✅ Finish for today"):
                    st.success("👏 Great work today! Stay consistent and share your progress with your tutor.")
                    st.session_state["teil2_today"] = []
                    st.session_state["teil2_index"] = 0

    st.progress(done / total)

    # --- Download button for Teil 2 progress ---
    if st.session_state["teil2_done"]:
        teil2_text = "Your Teil 2 completed questions:\n\n"
        for thema, wort in st.session_state["teil2_done"]:
            teil2_text += f"Thema: {thema} | Wort: {wort}\n"

        st.download_button(
            "📥 Download Teil 2 Progress",
            teil2_text,
            file_name=f"{student_name}_Teil2_progress.txt"
        )

# ---------- Teil 3 ----------
elif teil.startswith("Teil 3"):
    total = len(teil3_prompts)
    done = len(st.session_state["teil3_done"])
    st.info(f"Total situations: {total}. You have completed {done}.")

    remaining = [s for s in teil3_prompts if s not in st.session_state["teil3_done"]]

    if not remaining:
        st.success("🎉 You have completed all available situations in Teil 3! Well done. You can review Teil 1 or Teil 2 again anytime.")
        st.stop()

    if not st.session_state["teil3_today"]:
        max_today = len(remaining)
        st.info("How many situations would you like to practice today? Minimum 1.")
        num_today = st.number_input(
            "Number of situations to practice today:",
            min_value=1,
            max_value=max_today if max_today >= 1 else max_today,
            step=1
        )

        if st.button("🎯 Start Today’s Practice"):
            st.session_state["teil3_today"] = random.sample(remaining, min(num_today, len(remaining)))
            st.session_state["teil3_index"] = 0
            st.session_state["submitted_valid"] = False

    elif st.session_state["teil3_today"]:
        index = st.session_state["teil3_index"]
        batch = st.session_state["teil3_today"]

        if index < len(batch):
            situation = batch[index]
            st.info(f"📝 Situation: {situation}")

            st.warning("👉 Please type both your **request** and **response**. End your request with a **?** and your response with a **.**")

            text = st.text_area(
                "💬 Your request + response:",
                key=f"bitteantwort_{index}",
                placeholder="Example: Können Sie mir bitte helfen? Ja, gerne."
            )

            if st.button("✅ Submit"):
                feedback = []

                if "?" not in text or "." not in text:
                    feedback.append("Please use a question mark (?) and a full stop (.)")
                    st.session_state["submitted_valid"] = False
                else:
                    bitte_part = text.split("?")[0].strip().lower()
                    antwort_part = text.split("?")[1].strip().lower()

                    if not any(w in bitte_part for w in ["können", "könnten", "bitte", "öffnen sie", "machen sie"]):
                        feedback.append("Your request should include 'können', 'könnten', 'bitte' or a Sie-form imperative.")

                    polite_responses = ["ja", "kein problem", "gerne", "natürlich"]
                    if not any(p in antwort_part for p in polite_responses):
                        feedback.append("Your response should be polite (e.g., 'Ja, gerne').")

                if feedback:
                    for f in feedback:
                        st.error(f)
                    st.session_state["submitted_valid"] = False
                else:
                    st.success("✅ Answer saved. Click 'Next' to continue.")
                    st.session_state["submitted_valid"] = True

            if st.button("➡ Next"):
                if st.session_state["submitted_valid"]:
                    if situation not in st.session_state["teil3_done"]:
                        st.session_state["teil3_done"].append(situation)
                    st.session_state["teil3_index"] += 1
                    st.session_state["submitted_valid"] = False
                else:
                    st.warning("Please submit a valid answer before continuing.")

        else:
            st.success(f"🎉 You completed {len(batch)} situations today.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Start new batch"):
                    st.session_state["teil3_today"] = []
                    st.session_state["teil3_index"] = 0
            with col2:
                if st.button("✅ Finish for today"):
                    st.success("👏 Great work today! Stay consistent and share your progress with your tutor.")
                    st.session_state["teil3_today"] = []
                    st.session_state["teil3_index"] = 0

    st.progress(done / total)

    # --- Download button for Teil 3 progress ---
    if st.session_state["teil3_done"]:
        teil3_text = "Your Teil 3 completed situations:\n\n"
        for situation in st.session_state["teil3_done"]:
            teil3_text += f"{situation}\n"

        st.download_button(
            "📥 Download Teil 3 Progress",
            teil3_text,
            file_name=f"{student_name}_Teil3_progress.txt"
        )

# ---------- Reset Progress ----------
st.divider()
st.info("If you want to start over, you can reset your progress below.")

if st.button("♻ Reset All Progress"):
    for key in [
        "teil2_done", "teil3_done", "teil1_done",
        "teil2_today", "teil3_today",
        "teil2_index", "teil3_index",
        "submitted_valid"
    ]:
        if key in st.session_state:
            del st.session_state[key]
    st.success("Progress has been reset. Please reload the page to start again.")
