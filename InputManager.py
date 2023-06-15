inputConfig = {
    "key": [
        {"modifier1": "function1"},
        {"modifier2": "function2"}],
    "n": [
        {"None": ["addCurve", "None"]}
    ],
    "r": [
        {"None": ["rotateCurve", "clockwise"]},
        {"Shift": ["rotateCurve", "counter-clockwise"]}
    ]
   }


class InputManager:
    def __init__(self, configFilePath) -> None:
        self.loadConfigurationFromFile(configFilePath)

    def loadConfigurationFromFile(self, configFilePath):
        print(inputConfig)
