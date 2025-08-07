CREATE OR REPLACE VIEW vw_taxa_variacao_ida AS
WITH base AS (
	SELECT
        grupo_economico,
        TO_DATE(mes || '-01', 'YYYY-MM-DD') AS data_mes,
        ida
    FROM raw.ida
    WHERE variavel = 'Indicador de Desempenho no Atendimento (IDA)'
),
variacao AS (
    SELECT
        grupo_economico,
        data_mes,
        ida,
        LAG(ida) OVER (PARTITION BY grupo_economico ORDER BY data_mes) AS ida_mes_anterior
    FROM base
),
taxa_variacao AS (
    SELECT
        grupo_economico,
        data_mes,
        ROUND(
            ((ida - ida_mes_anterior) / NULLIF(ida_mes_anterior, 0)) * 100
        , 2) AS taxa_variacao
    FROM variacao
    WHERE ida_mes_anterior IS NOT NULL
),
media_variacao AS (
    SELECT
        data_mes,
        ROUND(AVG(taxa_variacao), 2) AS taxa_variacao_media
    FROM taxa_variacao
    GROUP BY data_mes
),
final AS (
    SELECT
        t.data_mes,
        m.taxa_variacao_media,
        t.grupo_economico,
        ROUND(t.taxa_variacao - m.taxa_variacao_media, 2) AS diferenca
    FROM taxa_variacao t
    JOIN media_variacao m ON t.data_mes = m.data_mes
)
SELECT
    TO_CHAR(data_mes, 'YYYY-MM') AS mes,
    taxa_variacao_media,
    MAX(CASE WHEN grupo_economico = 'ALGAR' THEN diferenca END) AS algar,
    MAX(CASE WHEN grupo_economico = 'CLARO' THEN diferenca END) AS claro,
    MAX(CASE WHEN grupo_economico = 'OI' THEN diferenca END) AS oi,
    MAX(CASE WHEN grupo_economico = 'SERCOMTEL' THEN diferenca END) AS sercomtel
FROM final
GROUP BY data_mes, taxa_variacao_media
ORDER BY data_mes;
