from .gamma import gamma_MLE
from .pareto import pareto_MLE
from .lomax import lomax_MLE

class DagilimAnalizcisi:
    def __init__(self, dosya_yolu):
        self.dosya_yolu = dosya_yolu

    def gamma(self):
        return gamma_MLE(self.dosya_yolu)

    def pareto(self):
        return pareto_MLE(self.dosya_yolu)

    def lomax(self):
        return lomax_MLE(self.dosya_yolu)
