from JUSU import Div, H1, P, Button

class Hero:
    def __init__(self):
        self.page = Div(
            H1("Welcome to JUSU"),
            P("A tiny component-driven page."),
            Button("Get started", onclick="alert('Hello')"),
            cls="hero"
        )

    def render(self):
        return self.page.render()

# For the extension preview, consumers can import and use `Hero` or call `Hero().render()`
