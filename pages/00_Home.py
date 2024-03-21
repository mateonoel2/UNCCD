import solara

@solara.component
def Page():
    with solara.Column(align="center"):
        markdown = """
# Discovering Land Degradation in Brazil

Hello and welcome! 

We present to you a novel and engaging way to delves into the depths of land degradation in Brazil. Our website uses an easy-to-understand **Interactive Map** to exemplify the current scenario and historical development of land degeneration in different regions of the largest country in South America.

![Brazil Terrain](https://example.com/brazil_terrain.jpg)

---
## Interactive Map: A Gateway To Real-time Information

Our interactive map is more than just a visual representation. It is as much an educational tool as it is a doorway to real-time, updated information about land degradation in various parts of Brazil.

The tool offers the following features:

- **Area Specific Details**: Zoom into any area on the map to access the details about the extent of land degradation in that specific region.
- **Comparative Analysis**: Compare regions to understand the severity and difference in degradation amongst different areas.
- **Historical Data**: Access archived data to understand the progression (or regression) of land degradation in Brazil.

To begin your journey, simply hover over any area on the map.

![Interactive Map](https://example.com/interactive_map.jpg)

---
## Why Should You Care?

Land degradation is not just a local problem but one that impacts global environmental health. It directly influences climate change and biodiversity. Understanding the extent and details of such environmental issues can help all of us become more informed and contribute to ameliorating the situation.

---
We've made it our aim to contribute to the global effort in battling the pressing issue of land degradation, and we hope this resource helps you gain better insight into the scenario in Brazil!

Though we strive to ensure the accuracy of the information on this website, continuous changes in actual conditions may cause slight differentiation. Nevertheless, the platform offers an overview and serves as a great starting point for researchers, educators, policy-makers, and anyone interested in environmental studies.

Come, let's explore, learn, and work towards better land health in Brazil!
        """

        solara.Markdown(markdown)