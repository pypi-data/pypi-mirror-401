import setuptools

def filecontent(fname: str):
    content = ""
    with open(fname, "r") as file:
        content = file.read()
    return content

def load_requirements(fname: str) -> list[str]:
    content: list[str] = []
    with open(fname, mode="rt", encoding="UTF-8") as file:
        for line in file.readlines():
            content.append(line.strip())
    return content

setuptools.setup(
    description = "System Monitor Tool using MQTT and supporting HomeAssistant discovery",
    package_dir={"":"src"},
    packages=setuptools.find_packages("src"),  # include all packages under src
    package_data={"": ["resources/*.src"]},
    include_package_data=True
)
