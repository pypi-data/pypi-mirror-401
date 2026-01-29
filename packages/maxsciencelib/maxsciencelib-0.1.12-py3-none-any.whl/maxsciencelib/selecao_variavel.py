def escolha_variaveis(*args, **kwargs):
    """
    Wrapper para carregar a implementação pesada sob demanda.
    """
    try:
        from ._selecao_variavel_impl import escolha_variaveis as _impl
    except ImportError as e:
        raise ImportError(
            "A função escolha_variaveis requer dependências opcionais de ML.\n"
            "Instale com: pip install maxsciencelib[selecao_variavel]"
        ) from e

    return _impl(*args, **kwargs)
