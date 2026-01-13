import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaln

def gamma_MLE(dosya_yolu):

    df = pd.read_csv(dosya_yolu, sep=';', decimal=',', header=None)
    veri = df.iloc[:, 0].values.astype(float)
    veri = veri[veri > 0]

    n = len(veri)

    def negatif_log_olabilirlik(param):
        alfa, beta = param
        if alfa <= 0 or beta <= 0: return np.inf
        oyf = n*(alfa*np.log(beta)-gammaln(alfa))+(alfa-1)*np.sum(np.log(veri))-beta*np.sum(veri)
        return -oyf

    ortalama = np.mean(veri)
    varyans = np.var(veri)
    baslangic = [ortalama**2/varyans, ortalama/varyans]

    sonuc = minimize(negatif_log_olabilirlik, baslangic, method="L-BFGS-B", bounds=((1e-6,None),(1e-6,None)))
    alfa, beta = sonuc.x

    return {
        "Dagilim":"Gamma",
        "Alfa":float(alfa),
        "Beta":float(beta),
        "Beklenen_Deger":float(alfa/beta),
        "Gozlem_Sayisi":int(n)
    }
