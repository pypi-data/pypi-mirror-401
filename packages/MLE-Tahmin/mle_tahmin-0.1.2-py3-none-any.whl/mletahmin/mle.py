from .gamma import Gamma_MLE
from .lomax import Lomax_MLE
from .pareto import Pareto_MLE

class DagilimAnalizcisi:
    def __init__(self, dosya_yolu):
        self.dosya_yolu = dosya_yolu

    def gamma_MLE(self):
        return Gamma_MLE(self.dosya_yolu)

    def lomax_MLE(self):
        return Lomax_MLE(self.dosya_yolu)

    def pareto_MLE(self):
        return Pareto_MLE(self.dosya_yolu)
