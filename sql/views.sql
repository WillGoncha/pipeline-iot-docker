-- ============================================
-- VIEW 1: Temperatura média por ambiente
-- ============================================

CREATE OR REPLACE VIEW avg_temp_por_ambiente AS
SELECT
    ambiente,
    ROUND(AVG(temperatura), 2) AS temperatura_media
FROM leituras_iot
GROUP BY ambiente
ORDER BY ambiente;


-- ============================================
-- VIEW 2: Quantidade de leituras por hora
-- ============================================

CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM data_hora)::INTEGER AS hora,
    COUNT(*) AS contagem
FROM leituras_iot
GROUP BY EXTRACT(HOUR FROM data_hora)
ORDER BY hora;


-- ============================================
-- VIEW 3: Temperaturas máxima, mínima e média
-- por dia
-- ============================================

CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    DATE(data_hora) AS data,
    MAX(temperatura) AS temp_max,
    MIN(temperatura) AS temp_min,
    ROUND(AVG(temperatura), 2) AS temp_media
FROM leituras_iot
GROUP BY DATE(data_hora)
ORDER BY data;