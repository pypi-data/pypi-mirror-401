import numpy as np
import pandas as pd
import polars as pl

def _agrupamento_vidro(produto_descricao, agrupar_marca=True, agrupar_lado=True):
    marcas_vid = [' AIS-AGC',' NORDGLASS-AGC',' PK',' SG',' AGC',' FN',' FY',' XYG',' VITRO',' VFORTE',' TYC',' DEPO']
    lados = [' LD/LE ',' LE/LD ',' LE ',' LD ', ' E ', ' D ']

    produto_agrupado = produto_descricao

    if agrupar_marca:
        for marca in marcas_vid:
            if marca in produto_agrupado:
                produto_agrupado = produto_agrupado.replace(marca, '')
                break

    if agrupar_lado:
        for lado in lados:
            if (lado in produto_agrupado 
                and ' CLASSE E ' not in produto_agrupado 
                and ' PEUGEOT E ' not in produto_agrupado):
                produto_agrupado = produto_agrupado.replace(lado, ' ')
                break
            elif produto_agrupado.endswith((' E', ' D')):
                produto_agrupado = produto_agrupado[:-2]
                break
            elif produto_agrupado.endswith((' LE', ' LD')):
                produto_agrupado = produto_agrupado[:-3]
                break
            elif produto_agrupado.endswith(' LD/LE'):
                produto_agrupado = produto_agrupado[:-6]
                break

    produto_agrupado = produto_agrupado.replace(' EXC', '')

    if ' AMT' in produto_agrupado:
        if ' CNT' in produto_agrupado:
            produto_agrupado = produto_agrupado.replace(' AMT CNT', '')
        else:
            produto_agrupado = produto_agrupado.replace(' AMT AER', '')

    return produto_agrupado.strip()


def _agrupamento_retrovisor(produto_descricao, agrupar_marca=True, agrupar_lado=True):
    marcas_retrov = [' MTG/QXP',' MTG/VMAX',' MTG/PWAY',' MTG',' FCS',' VMAX',' SMR',' PWAY',
                     ' ORIGINAL',' F2J',' ARTEB*',' MEKRA',' HELLA',' TYC']
    lados = [' LD/LE ',' LE/LD ',' LE ',' LD ', ' E ', ' D ']

    casos_especificos = {
        'RETROV NISSAN FRONTIER LE 19/ CD ELET EXT CROM LD (CAM/PLED/RET) MTG',
        'ENC RETROV NISSAN FRONTIER LE 19/ CD ELET EXT CROM LD (CAM/LOGO/PLED/RET) ORIGINAL*'
    }

    if produto_descricao in casos_especificos:
        return produto_descricao.replace(' LD', '').strip()

    produto_agrupado = produto_descricao

    if agrupar_marca:
        for marca in marcas_retrov:
            if marca == ' ORIGINAL' and ' ORIGINAL*' in produto_agrupado:
                continue
            if marca in produto_agrupado:
                produto_agrupado = produto_agrupado.replace(marca, '')
                break

    if agrupar_lado:
        for lado in lados:
            if lado in produto_agrupado:
                produto_agrupado = produto_agrupado.replace(lado, ' ')
                break
            elif produto_agrupado.endswith((' E', ' D')):
                produto_agrupado = produto_agrupado[:-2]
                break
            elif produto_agrupado.endswith((' LE', ' LD')):
                produto_agrupado = produto_agrupado[:-3]
                break
            elif produto_agrupado.endswith(' LD/LE'):
                produto_agrupado = produto_agrupado[:-6]
                break

    produto_agrupado = produto_agrupado.replace(' EXC', '')

    if ' AMT' in produto_agrupado:
        if ' CNT' in produto_agrupado:
            produto_agrupado = produto_agrupado.replace(' AMT CNT', '')
        else:
            produto_agrupado = produto_agrupado.replace(' AMT AER', '')

    return produto_agrupado.strip()


def _agrupamento_farol_lanterna(produto_descricao, agrupar_marca=True, agrupar_lado=True):
    marcas_fl = [' IFCAR ARTEB',' VALEO/F2J',' MM',' CASP',' ARTEB',' TYC',' DEPO',
                 ' ORIGINAL',' F2J',' ARTEB*',' VALEO',' HELLA',' FITAM',' ORGUS']
    lados = [' LD/LE ',' LE/LD ',' LE ',' LD ', ' E ', ' D ']

    produto_agrupado = produto_descricao

    if agrupar_marca:
        for marca in marcas_fl:
            if marca == ' ORIGINAL' and ' ORIGINAL*' in produto_agrupado:
                continue
            if marca in produto_agrupado:
                produto_agrupado = produto_agrupado.replace(marca, '')
                break

    if agrupar_lado:
        for lado in lados:
            if lado in produto_agrupado:
                produto_agrupado = produto_agrupado.replace(lado, ' ')
                break
            elif produto_agrupado.endswith((' E', ' D')):
                produto_agrupado = produto_agrupado[:-2]
                break
            elif produto_agrupado.endswith((' LE', ' LD')):
                produto_agrupado = produto_agrupado[:-3]
                break
            elif produto_agrupado.endswith(' LD/LE'):
                produto_agrupado = produto_agrupado[:-6]

    produto_agrupado = produto_agrupado.replace(' EXC', '')

    if ' AMT' in produto_agrupado:
        if ' CNT' in produto_agrupado:
            produto_agrupado = produto_agrupado.replace(' AMT CNT', '')
        else:
            produto_agrupado = produto_agrupado.replace(' AMT AER', '')

    return produto_agrupado.strip()


def agrupar_produto(
    df: pd.DataFrame,
    coluna_origem: str,
    coluna_nova: str,
    agrupar_marca: bool = True,
    agrupar_lado: bool = True
) -> pd.DataFrame:
    """
    Agrupa descrições de produtos (vidro, retrovisor, farol/lanterna)
    criando uma nova coluna no DataFrame.
    """

    df = df.copy()

    def _aplicar(descricao):
        if pd.isna(descricao):
            return np.nan

        descricao = str(descricao)

        if 'VID ' in descricao:
            return _agrupamento_vidro(descricao, agrupar_marca, agrupar_lado)

        elif 'RETROV ' in descricao:
            return _agrupamento_retrovisor(descricao, agrupar_marca, agrupar_lado)

        elif 'FAROL ' in descricao or 'LANT ' in descricao:
            return _agrupamento_farol_lanterna(descricao, agrupar_marca, agrupar_lado)

        return descricao.strip()

    df[coluna_nova] = df[coluna_origem].apply(_aplicar)

    return df


def media_saneada(valores, min_amostras=3, cv_max=0.25):
    # 🔹 NORMALIZA ENTRADA
    if isinstance(valores, pl.Series):
        dados = pd.Series(valores.to_list()).dropna()
    elif isinstance(valores, (list, np.ndarray)):
        dados = pd.Series(valores).dropna()
    elif isinstance(valores, pd.Series):
        dados = valores.dropna()
    else:
        raise TypeError(
            f"Tipo não suportado: {type(valores)}. "
            "Esperado: list, np.ndarray, pd.Series ou pl.Series."
        )

    # 🔹 REGRA
    if len(dados) < min_amostras:
        return float(dados.median())

    while len(dados) > min_amostras:
        media = dados.mean()
        desvio = dados.std()
        cv = desvio / media if media != 0 else 0

        if cv <= cv_max:
            return float(media)

        li = media - desvio
        ls = media + desvio

        filtrados = dados[(dados >= li) & (dados <= ls)]

        if len(filtrados) < min_amostras:
            return float(np.median(np.sort(dados)[:min_amostras]))

        dados = filtrados

    return float(np.median(np.sort(dados)[:min_amostras]))


def media_saneada_groupby(
    df: pl.DataFrame,
    grupo: str,
    coluna: str,
    min_amostras: int = 3,
    cv_max: float = 0.25
) -> pl.DataFrame:
    return (
        df
        .group_by(grupo)
        .agg(
            pl.col(coluna).implode().alias("_valores")
        )
        .with_columns(
            pl.col("_valores")
            .map_elements(
                lambda x: media_saneada(x, min_amostras, cv_max),
                return_dtype=pl.Float64
            )
            .alias("media_saneada")
        )
        .select(grupo, "media_saneada")
        .sort(grupo)
    )