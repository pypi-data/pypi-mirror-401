import numpy as np
import pandas as pd
from joblib import Parallel, delayed


def media_saneada(valores, min_amostras=3, cv_max=0.25):
    """
    Calcula a média saneada de um conjunto de valores numéricos.

    A função remove iterativamente valores fora do intervalo
    [média ± desvio padrão] até que o coeficiente de variação (CV)
    fique abaixo do limite definido ou o número mínimo de amostras
    seja atingido.

    Parâmetros
    ----------
    valores : array-like
        Lista, array NumPy ou pd.Series contendo valores numéricos.
    min_amostras : int, default=3
        Número mínimo de observações permitido.
    cv_max : float, default=0.25
        Coeficiente de variação máximo aceitável.

    Retorna
    -------
    float
        Média saneada ou mediana dos últimos `min_amostras` valores.
    """
    arr = np.asarray(valores, dtype=float)
    arr = arr[~np.isnan(arr)]

    n = arr.size
    if n < min_amostras:
        return float(np.median(arr))

    while True:
        media = arr.mean()
        desvio = arr.std()

        if media != 0 and (desvio / media) <= cv_max:
            return float(media)

        if n <= min_amostras:
            break

        li = media - desvio
        ls = media + desvio

        mask = (arr >= li) & (arr <= ls)
        novo_n = mask.sum()

        if novo_n < min_amostras:
            arr.sort()
            return float(np.median(arr[:min_amostras]))

        if novo_n == n:
            break

        arr = arr[mask]
        n = novo_n

    arr.sort()
    return float(np.median(arr[:min_amostras]))

def _media_saneada_worker(key, valores, min_amostras, cv_max):
    return (*key, media_saneada(valores, min_amostras, cv_max))


def media_saneada_groupby(
    df,
    group_cols,
    value_col,
    min_amostras=3,
    cv_max=0.25,
    n_jobs=-1,
    output_col="media_saneada"
):
    """
    Aplica a média saneada por grupo em um DataFrame,
    utilizando paralelização por múltiplos processos.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame de entrada.
    group_cols : list[str]
        Colunas utilizadas para o agrupamento.
    value_col : str
        Coluna numérica sobre a qual será calculada a média saneada.
    min_amostras : int, default=3
        Número mínimo de observações permitido por grupo.
    cv_max : float, default=0.25
        Coeficiente de variação máximo aceitável.
    n_jobs : int, default=-1
        Número de processos paralelos. -1 utiliza todos os cores.
    output_col : str, default="media_saneada"
        Nome da coluna de saída.

    Retorna
    -------
    pd.DataFrame
        DataFrame agregado com a média saneada por grupo.
    """
    grouped = df.groupby(group_cols, sort=False)[value_col]

    results = Parallel(
        n_jobs=n_jobs,
        backend="loky",
        prefer="processes"
    )(
        delayed(_media_saneada_worker)(
            key,
            group.values,
            min_amostras,
            cv_max
        )
        for key, group in grouped
    )

    return pd.DataFrame(
        results,
        columns=[*group_cols, output_col]
    )
