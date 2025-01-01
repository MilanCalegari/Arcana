import streamlit as st
import yaml

from modules.llm.card_interpreter import CardInterpreter
from modules.tarot.card import TarotDeck
from modules.utils.commom import CardReadingMethod, label4method

# Initialize deck and interpreter
deck = TarotDeck()
deck.get_cards()
interpreter = CardInterpreter()

st.set_page_config(
    page_title="Tarot Reading",
    page_icon="🔮",
    layout="centered"
)

st.title("🔮 Tarot Reading")

# Secret configurations
with st.sidebar:
    with st.expander("⚙️ Settings", expanded=False):
        reversed_prob = st.slider(
            "Probability of reversed cards",
            min_value=0.0,
            max_value=1.0,
            value=yaml.safe_load(open("config.yaml"))["reverse_probability"],
            step=0.1,
            help="Probability of a card appearing reversed (0.0 to 1.0)"
        )
        # TODO: Add Portuguese language support and translation
        # language = st.selectbox(
        #     "Language",
        #     ["English", "Portuguese"],
        #     index=0
        # )

reversed_prob -= 1

# User interface texts
welcome_text = "### Welcome to your Tarot Reading"
instructions_text = "Please select a reading method and provide a context for your consultation."
method_text = "Choose your reading method:"
context_text = "What would you like to know about? (Optional)"
context_placeholder = "Ex: I need guidance about finding my life purpose..."
draw_button = "Draw Cards"
spinner_texts = {
    "shuffle": "🔮 Shuffling the cards with mystical energy...",
    "channel": "✨ Channeling the energies of the universe...",
    "reveal": "🌟 Revealing the secrets of destiny...",
    "consult": "🧙‍♂️ Consulting ancient wisdom...",
    "cards": "### Your Cards:",
    "reading": "### Your Reading:",
    "default_context": "General daily reading"
}

# Display welcome message and instructions
st.markdown(welcome_text)
st.markdown(instructions_text)

# Reading method selection
method = st.selectbox(
    method_text,
    [
        CardReadingMethod.PAST_PRESENT_FUTURE.value,
        CardReadingMethod.CELTIC_CROSS.value,
        CardReadingMethod.HAND_OF_ERIS.value
    ]
)

# Reading context input
context = st.text_area(
    context_text,
    placeholder=context_placeholder
)

if st.button(draw_button):
    # Shuffle and draw cards
    with st.spinner(spinner_texts["shuffle"]):
        deck.shuffle(reversed_prob)
        
    with st.spinner(spinner_texts["channel"]):
        cards = deck.draw(CardReadingMethod(method))
    
    # Display cards
    st.markdown(spinner_texts["cards"])
    
    cols = st.columns(len(cards))
    for idx, (card, col) in enumerate(zip(cards, cols)):
        with col:
            with st.spinner(spinner_texts["reveal"]):
                st.image(card.image_pth, caption=f"{label4method[CardReadingMethod(method)][idx]}: {card.name}")
    
    # Generate and display interpretation
    with st.spinner(spinner_texts["consult"]):
        if context:
            interpretation = interpreter.generate_interpretation(cards, context, CardReadingMethod(method))
        else:
            interpretation = interpreter.generate_interpretation(cards, None, CardReadingMethod(method))
    
    st.markdown(spinner_texts["reading"])
    st.write(interpretation)
