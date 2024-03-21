import solara

@solara.component
def Page():
    with solara.Column(align="center"):
        markdown = """
# Discovering Land Degradation in Brazil

Hello and welcome! 

We present to you a novel and engaging way to delves into the depths of land degradation in Brazil. Our website uses an easy-to-understand **Interactive Map** to exemplify the current scenario and historical development of land degeneration in different regions of the largest country in South America.
        """

        solara.Markdown(markdown)