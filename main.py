import fantas

window_config = fantas.WindowConfig()
window_config.title = "Fantas3 Demo"
window_config.window_size = (1920, 1080)

window = fantas.Window(window_config)

background = fantas.ColorBackground(color=fantas.Color("#e3e3e3"))
window.root_ui = background

test_label = fantas.ColorLabel(color=fantas.Color("#3498db"), rect=fantas.Rect(480, 270, 960, 540))
background.append(test_label)

test_text = fantas.ColorTextLine(rect=fantas.Rect(0, 0, 0, 0))
test_text.text = "Hello World!"
test_text.size = 48.0
test_label.append(test_text)

window.mainloop()
