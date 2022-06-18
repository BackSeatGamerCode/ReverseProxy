import PySimpleGUI as sg

import source.defaults as defaults
import source.tts as tts

VOICES = {voice.name: voice.id for voice in tts.TTS_ENGINE.getProperty('voices')}


def create_window():
    default_voice = tts.TTS_ENGINE.getProperty('voices')[0].name

    for name, voice in VOICES.items():
        if voice == tts.TTS_ENGINE.getProperty('voice'):
            default_voice = name

    layout = [
        [sg.Text("Text To Speech Settings")],
        [sg.Text("Rate"), sg.Slider(
            (100, 300), default_value=tts.TTS_ENGINE.getProperty('rate'), resolution=1, orientation="horizontal",
            disable_number_display=True, key="rate", enable_events=False
        )],
        [sg.Text("Volume"), sg.Slider(
            (0, 100), default_value=tts.TTS_ENGINE.getProperty('volume') * 100, resolution=1, orientation="horizontal",
            disable_number_display=True, key="volume", enable_events=False
        )],
        [
            sg.Text("Voice"),
            sg.Combo(list(VOICES.keys()), readonly=True, default_value=default_voice, key="voice")
        ],
        [sg.Button("Save"), sg.Button("Cancel")]
    ]

    return sg.Window(layout=layout, **defaults.WINDOW_SETTINGS)


def show():
    window = create_window()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "Save":
            tts.TTS_ENGINE.setProperty('rate', values["rate"])
            tts.TTS_ENGINE.setProperty('volume', values["volume"] / 100)
            tts.TTS_ENGINE.setProperty('voice', VOICES[values["voice"]])

            defaults.set_defaults("tts", {
                'rate': values["rate"],
                'volume': values["volume"] / 100,
                'voice': VOICES[values["voice"]]
            })

            break

        if event == "Cancel":
            break

    window.close()
