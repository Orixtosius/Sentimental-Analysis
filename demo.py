import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from sumapi.api import SumAPI
import json

api_connect = SumAPI(username='********', password='********')

st.title("Cümle Duygu Bulucu Makine")
st.subheader("Cümlendeki derin manaları bulmamı ister misin ?")
st.subheader("Aşağıdaki butona tıkla ve cümleni söyle")
stt_button = Button(label="Başlat", width=100)
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.interimResults = true;
    recognition.lang = 'tr_TR';

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

col1, col2 = st.columns(2)

if result:
    if "GET_TEXT" in result:
        st.success("Ne demek istediğini anladım! -> "+ result.get("GET_TEXT"))
        result = api_connect.sentiment_analysis(result['GET_TEXT'], domain='general')
        result_list = list(result.values())
        splitted_list = list(result_list[1].values())
        percent = int(float(splitted_list[1]) * 100)

        if (splitted_list[0] == 'positive'):
            col1.subheader('Bu ifade %' + str(percent) + ' pozitiftir.')
            col2.image("https://pngimg.com/uploads/smiley/smiley_PNG36230.png", width=100)
        else:
            col1.subheader('Bu ifade %' + str(percent) + ' negatiftir.')
            col2.image("https://www.cambridge.org/elt/blog/wp-content/uploads/2019/07/Sad-Face-Emoji.png", width=100)




