> Informe histórico de la primera búsqueda. La conexión ya fue habilitada y la recolección avanzó. Consultar [estado actual del corpus](corpus/ESTADO.md) y [guía para el agente revisor](PARA_EL_AGENTE.md).

# Investigaciones de estrategias con opciones y futuros

Fecha de consulta: 18 de octubre de 2026. Idioma de síntesis: español.

## Alcance real de esta entrega

Se localizaron **96 referencias candidatas** en OpenAlex, arXiv, SSRN y CME. Se prepararon **21 fichas de evidencia a partir de resúmenes**. No se descargaron ni revisaron sistemáticamente los textos completos. El catálogo no es exhaustivo ni una lista de estrategias recomendadas. Las referencias sin ficha siguen pendientes de evaluación de pertinencia y calidad; algunas son metodología, educación o investigaciones de acciones que sirven como contexto.

La descarga directa con Python no pudo ejecutarse porque el entorno no resuelve los dominios externos. El navegador de búsqueda sí permitió localizar las referencias. El recolector adjunto queda preparado para otro entorno con conexión y sus solicitudes reales no han podido verificarse aquí.

OpenAlex es un índice bibliográfico: un registro puede apuntar a arXiv o SSRN y no constituye un estudio independiente adicional. SSRN y arXiv alojan versiones y preprints; alojar un trabajo allí no confirma revisión por pares. CME mezcla investigación, comentarios de industria, documentación de contratos y educación. Un gráfico de payoff o una estrategia denominada «proven» no prueba rentabilidad neta.

## Hallazgos para orientar la lectura

- **Opciones: empezar por implementación y costos.** La ficha E01 documenta que 17 de 24 señales producen resultados brutos significativos, pero ninguna conserva rentabilidad en la implementación base con costos. La mitigación recupera 7 carteras: la conclusión depende de las reglas de ejecución.
- **Futuros: comparar tendencia y sus críticas conjuntamente.** E04 documenta momentum en 58 instrumentos. E05 cuestiona la predictibilidad y E06 la atribución al momentum frente al escalado por volatilidad. Ninguno demuestra una garantía de beneficio futuro.
- **Resultados negativos de minoristas no identifican por sí solos qué regla falla.** E07 muestra pérdidas en el 97% de quienes persistieron más de 300 días dentro de una población brasileña concreta.
- **Las primas de riesgo no son arbitrajes seguros.** Los documentos de CME sobre primas alternativas describen venta de volatilidad, carry y momentum; deben contrastarse con riesgos de cola, concentración, liquidez y crowding. Véase [documento de Gresham alojado por CME](https://www.cmegroup.com/education/files/alternative-risk-premia-in-commodities-gresham.pdf).
- **Separar simulación, backtest y operativa real.** Deep Hedging trata cobertura bajo fricciones; mejorar una cobertura en simulación no demuestra alpha. Los trabajos recientes de aprendizaje automático son candidatos para replicación, no evidencia independiente de resultados en vivo.

## Fichas de lectura prioritaria

### E01 · A Transaction Cost Perspective on Option Anomalies

[Registro original](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4806038) · SSRN · año de referencia 2024 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** James O’Donovan; Gloria Yang Yu. **Tema:** Opciones; anomalías delta-hedged.

**Resultado reportado:** Negativo en implementación base; condicionado al mitigar costos. De 24 señales, 17 ofrecen resultados brutos significativos; ninguna sobrevive a costos en la implementación base. Mitigar costos recupera rentabilidad en 7 carteras.

**Límite de la conclusión:** Costos y frecuencia de cobertura son decisivos; no se han reproducido los resultados.

**Nivel de revisión:** Resumen de SSRN; revisión indicada 12-12-2025; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E02 · Who Profits From Trading Options?

[Registro original](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3867129) · SSRN · año de referencia 2021 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Jianfeng Hu; Antonia Kirilova; Seongkyu Gilbert Park; Doojin Ryu. **Tema:** Opciones; estilos de inversores.

**Resultado reportado:** Mixto. Los minoristas con estrategias simples pierden frente al resto del mercado; el trading de volatilidad y estrategias neutrales muestran mejores métricas dentro de la muestra.

**Límite de la conclusión:** Datos por cuenta de un mercado particular; no extrapolar automáticamente.

**Nivel de revisión:** Resumen de SSRN; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E03 · Intraday Index Predictability and Options Trading Profitability

[Registro original](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2558059) · SSRN · año de referencia 2015 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Kian Guan Lim; Ying Chen; Nelson Yap. **Tema:** Opciones semanales sobre E-mini S&P 500.

**Resultado reportado:** Positivo condicionado. El resumen reporta rentabilidad neta en trading de skewness; para kurtosis reporta beneficios antes de costos.

**Límite de la conclusión:** Comprobar spreads, horarios, tamaño y reglas en el texto completo.

**Nivel de revisión:** Resumen indexado de SSRN; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E04 · Time Series Momentum

[Registro original](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2089463) · SSRN · año de referencia 2012 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Tobias J. Moskowitz; Yao Hua Ooi; Lasse Heje Pedersen. **Tema:** Futuros diversificados; seguimiento de tendencia.

**Resultado reportado:** Positivo histórico. Documenta persistencia de 1 a 12 meses en 58 instrumentos y resultados favorables de una cartera diversificada.

**Límite de la conclusión:** Contrastar con críticas de escalado por volatilidad y predictibilidad.

**Nivel de revisión:** Resumen de SSRN; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E05 · Time-Series Momentum: Is It There?

[Registro original](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3165284) · SSRN · año de referencia 2020 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Dashan Huang; Jiangyuan Li; Liyao Wang; Guofu Zhou. **Tema:** Futuros y otras clases; momentum temporal.

**Resultado reportado:** Cuestiona predictibilidad. Encuentra evidencia débil de predictibilidad; una estrategia basada en medias históricas logra resultados parecidos.

**Límite de la conclusión:** No equivale a demostrar que toda estrategia de tendencia pierde.

**Nivel de revisión:** Resumen de SSRN; referencia JFE 2020; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E06 · Time Series Momentum and Volatility Scaling

[Registro original](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2786955) · SSRN · año de referencia 2016 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Abby Kim; Yiuman Tse; John K. Wald. **Tema:** Futuros; momentum y asignación por volatilidad.

**Resultado reportado:** Cuestiona atribución del rendimiento. Atribuye gran parte de los resultados al escalado por volatilidad; sin él, momentum y buy-and-hold presentan resultados similares.

**Límite de la conclusión:** La ficha indica que no está disponible para descarga.

**Nivel de revisión:** Resumen de SSRN; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E07 · Day Trading for a Living?

[Registro original](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3423101) · SSRN · año de referencia 2020 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Fernando Chague; Rodrigo De-Losso; Bruno Giovannetti. **Tema:** Futuros sobre índices; minoristas en Brasil.

**Resultado reportado:** Negativo en la población estudiada. El 97% de quienes persistieron más de 300 días perdió dinero entre los participantes que comenzaron en 2013–2015.

**Límite de la conclusión:** Resultado de esa población; no evalúa cada regla de trading individual.

**Nivel de revisión:** Resumen de SSRN, revisión 2020; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E08 · Crowding and Factor Returns

[Registro original](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3803954) · SSRN · año de referencia 2021 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Wenjin Kang; K. Geert Rouwenhorst; Ke Tang. **Tema:** Futuros de materias primas; value, momentum y carry.

**Resultado reportado:** Condicionado al crowding. El posicionamiento agregado predice negativamente los retornos de factores; los beneficios se concentran en períodos de bajo crowding.

**Límite de la conclusión:** Correlación predictiva histórica; revisar medición y desfases de CFTC.

**Nivel de revisión:** Resumen de SSRN; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E09 · Investable Commodity Premia in China

[Registro original](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3525612) · SSRN · año de referencia 2021 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Robert J. Bianchi; John Hua Fan; Tingxi Zhang. **Tema:** Futuros chinos; carry, momentum y basis-momentum.

**Resultado reportado:** Implementación convencional inviable; mejoras condicionadas. Las configuraciones estándar sufren limitaciones de liquidez; rolling dinámico y ponderaciones estratégicas mejoran capacidad y resultados reportados.

**Límite de la conclusión:** Las reglas de liquidez y vencimientos son específicas del mercado.

**Nivel de revisión:** Resumen de SSRN; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E10 · Integrating Time Series and Cross-Sectional Signals for Optimal Commodity Portfolios

[Registro original](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3504394) · SSRN · año de referencia 2020 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Regina Hammerschmid; Harald Lohre. **Tema:** Futuros de materias primas; integración de señales.

**Resultado reportado:** Positivo histórico fuera de muestra. Combinar timing y selección transversal supera los benchmarks del estudio fuera de muestra y después de costos.

**Límite de la conclusión:** Pendiente examinar la selección de parámetros y los costos asumidos.

**Nivel de revisión:** Resumen de SSRN; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E11 · A Bayesian Perspective on Commodity Style-Integration

[Registro original](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4112383) · SSRN · año de referencia 2023 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Ana-Maria Fuertes; Nan Zhao. **Tema:** Futuros de materias primas; combinación de factores.

**Resultado reportado:** Positivo histórico fuera de muestra. La integración bayesiana de carry, momentum y otros factores mejora métricas frente a varias alternativas en el estudio.

**Límite de la conclusión:** Comprobar costos, capacidad y acceso a los datos.

**Nivel de revisión:** Resumen de SSRN; Journal of Commodity Markets; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E12 · Expected Option Returns

[Registro original](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=189840) · SSRN · año de referencia 2000 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Tyler Shumway; Joshua D. Coval. **Tema:** Opciones sobre índices; straddles de beta cero.

**Resultado reportado:** Negativo para compra de straddles en la muestra. Reporta pérdidas medias aproximadas de 3% semanal en straddles ATM de beta cero y sugiere un factor adicional de riesgo de volatilidad.

**Límite de la conclusión:** Resultado histórico; no implica que vender la posición sea una ganancia segura.

**Nivel de revisión:** Resumen de SSRN; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E13 · Profit-and-Loss of Option Strategies under Quadratic Skew Parametrization

[Registro original](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1697829) · SSRN · año de referencia 2010 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Artur Sepp. **Tema:** Opciones; straddle, risk reversal y butterfly.

**Resultado reportado:** Marco analítico. Deriva aproximaciones de P&L y umbrales de skew y convexidad realizados para posiciones con cobertura delta.

**Límite de la conclusión:** Herramienta de análisis; no establece una ventaja operable universal.

**Nivel de revisión:** Resumen de SSRN; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E14 · Deep Hedging

[Registro original](https://arxiv.org/abs/1802.03042) · arXiv · año de referencia 2018 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Hans Bühler; Lukas Gonon; Josef Teichmann; Ben Wood. **Tema:** Derivados; cobertura con aprendizaje profundo.

**Resultado reportado:** Positivo en simulación de cobertura. Mejora la cobertura frente a una solución de mercado completo en un mercado sintético Heston con costos.

**Límite de la conclusión:** Minimizar riesgo de cobertura no es demostrar alpha en trading real.

**Nivel de revisión:** Resumen de arXiv; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E15 · Deep Reinforcement Learning for Trading

[Registro original](https://arxiv.org/abs/1911.10107) · arXiv · año de referencia 2019 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Zihao Zhang; Stefan Zohren; Stephen Roberts. **Tema:** 50 futuros líquidos; aprendizaje por refuerzo.

**Resultado reportado:** Positivo en backtest reportado. Prueba futuros entre 2011 y 2019 y reporta resultados superiores al momentum base incluso con costos elevados.

**Límite de la conclusión:** Requiere reproducir partición temporal, ajustes y ejecución.

**Nivel de revisión:** Resumen de arXiv; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E16 · Spatio-Temporal Momentum: Jointly Learning Time-Series and Cross-Sectional Strategies

[Registro original](https://arxiv.org/abs/2302.10175) · arXiv · año de referencia 2023 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Wee Ling Tan; Stephen Roberts; Stefan Zohren. **Tema:** Acciones y 12 futuros sobre índices.

**Resultado reportado:** Positivo en backtest reportado. Combina momentum temporal y transversal; reporta persistencia frente a benchmarks con costos de 5–10 puntos básicos.

**Límite de la conclusión:** Universo mixto; separar los resultados específicos de futuros.

**Nivel de revisión:** Resumen de arXiv; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E17 · Structural Limits of OHLCV-Based Intraday Signals in MNQ Futures: A Systematic Falsification Study

[Registro original](https://arxiv.org/abs/2605.04004) · arXiv · año de referencia 2026 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Mathias Mesfin. **Tema:** Micro E-mini Nasdaq-100; intradía.

**Resultado reportado:** Negativo bajo los criterios del autor. Evalúa 14 familias de señales en 947 días de 2021–2025; ninguna cumple simultáneamente todos los criterios establecidos.

**Límite de la conclusión:** Preprint reciente; el costo fijo de dos puntos por ida y vuelta condiciona la conclusión.

**Nivel de revisión:** Resumen de arXiv; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E18 · DeePM: Regime-Robust Deep Learning for Systematic Macro Portfolio Management

[Registro original](https://arxiv.org/abs/2601.05975) · arXiv · año de referencia 2026 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Kieran Wood; Stephen J. Roberts; Stefan Zohren. **Tema:** 50 futuros; portfolio macro con deep learning.

**Resultado reportado:** Positivo en backtest reportado. Reporta mejoras frente a tendencia clásica en backtests 2010–2025 con costos.

**Límite de la conclusión:** Preprint reciente; desempeño y generalización no verificados independientemente.

**Nivel de revisión:** Resumen de arXiv; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E19 · Speculative Futures Trading under Mean Reversion

[Registro original](https://arxiv.org/abs/1601.04210) · arXiv · año de referencia 2016 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Tim Leung; Jiao Li; Xin Li; Zheng Wang. **Tema:** Futuros; reversión a la media.

**Resultado reportado:** Teórico y numérico. Resuelve reglas de entrada y salida bajo modelos OU, CIR y XOU incorporando costos y elección long/short.

**Límite de la conclusión:** La optimalidad depende del modelo; falta validación empírica para operar.

**Nivel de revisión:** Resumen de arXiv; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E20 · Statistical Arbitrage and Optimal Trading with Transaction Costs in Futures Markets

[Registro original](https://arxiv.org/abs/0801.3348) · arXiv · año de referencia 2008 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Theodoros Tsagaris. **Tema:** Futuros; arbitraje estadístico.

**Resultado reportado:** Teórico. Plantea maximización de utilidad con spread y variables no observables, con solución para la cartera óptima.

**Límite de la conclusión:** Solución matemática; no prueba de beneficios con datos reales.

**Nivel de revisión:** Resumen de arXiv; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

### E21 · Determining Optimal Trading Rules without Backtesting

[Registro original](https://arxiv.org/abs/1408.1159) · arXiv · año de referencia 2014 (puede ser año de versión o publicación, no necesariamente primer depósito).

**Autores:** Peter P. Carr; Marcos Lopez de Prado. **Tema:** Metodología; reglas de salida.

**Resultado reportado:** Marco para reducir sobreajuste. Propone calcular reglas bajo un proceso OU discreto sin explorar configuraciones con un motor de backtesting.

**Límite de la conclusión:** Condicionado al modelo; no sustituye la validación fuera de muestra.

**Nivel de revisión:** Resumen de arXiv; texto completo pendiente. Sharpe neto, drawdown, datos y código: no extraídos ni verificados salvo mención expresa.

## Cómo ampliar la investigación de forma sistemática

1. Buscar sin filtro inicial de años ni país. Cubrir futuros sobre índices, tasas, FX, energía, metales y agricultura; opciones sobre futuros, índices y acciones. Mantener separados los resultados de opciones sobre acciones y opciones sobre futuros.
2. Ejecutar las consultas en `consultas.json`. Buscar resultados positivos y negativos con los mismos criterios; no usar solo términos como profitable o successful.
3. En OpenAlex, paginar con cursor y guardar DOI, identificadores, autores, fecha, abstract reconstruido, referencias y localizaciones de acceso abierto. En arXiv, buscar categorías q-fin y términos explícitos de derivados; guardar identificador sin versión para deduplicar y conservar la versión por separado.
4. En SSRN, usar las búsquedas de título/resumen/palabras clave y registrar abstract_id; guardar revisiones y restricciones de acceso. En CME, recorrer investigación y educación por producto y seguir referencias del Research Digest. El recolector adjunto automatiza OpenAlex/arXiv; SSRN/CME requieren esta búsqueda documental adicional y no están automatizados en él.
5. Deduplicar primero por DOI, luego identificadores del repositorio y finalmente título normalizado + autores. Los títulos similares requieren revisión manual: un preprint y un artículo pueden ser el mismo estudio con resultados revisados.
6. Para cada texto completo accesible, extraer mercado, instrumento exacto, muestra, frecuencia, reglas de señal, entrada, salida, sizing, financiación, garantías y liquidación. En opciones: DTE, delta/strike, IV, spreads, cobertura y ejercicio/asignación. En futuros: contrato, método de roll, ajuste de serie continua, multiplicador y entrega.
7. Registrar comisiones, bid-ask, slippage, impacto, rotación, Sharpe neto, drawdown, pérdidas de cola, benchmark, pruebas fuera de muestra y sensibilidad por régimen. Un dato no publicado debe permanecer como «no informado», nunca convertirse en cero.
8. Seguir referencias y trabajos que citan cada estudio, especialmente réplicas y críticas. Medir cobertura por consulta: total declarado, páginas recuperadas, duplicados, exclusiones, errores y pendientes. Detener por saturación documentada o por un límite explícito; no declarar «todo» por haber agotado un buscador.

## Clasificación de evidencia

- Positivo histórico: resultado favorable en la muestra reportada; no implica persistencia.
- Negativo: resultado desfavorable bajo instrumento, período, costos y reglas concretos.
- Condicionado o mixto: depende de régimen, liquidez, implementación o restricciones.
- Teórico/simulación: resultado bajo supuestos del modelo; exige prueba empírica.
- Educativo/contextual: explica instrumentos o mecánicas; no mide una ventaja estadística.
- Pendiente: localizado, aún sin análisis suficiente.

## Archivos y uso

- `LEER_PRIMERO.md`: este informe y las 21 fichas.
- `catalogo.md`: listado enlazado de las 96 referencias candidatas.
- `catalogo.json`: catálogo legible por programas.
- `evidencia.json`: fichas estructuradas; valores no verificados permanecen vacíos o nulos.
- `consultas.json`: vocabulario y consultas para continuar; distingue búsquedas registradas de propuestas.
- `recolectar.py`: recolector de metadatos OpenAlex/arXiv con límites, caché, checkpoints y registro de errores. No descarga PDFs ni atraviesa restricciones de acceso.

Ejemplo en PowerShell, desde esta carpeta: `python .\recolectar.py --source openalex --max-pages 3`. Para arXiv: `python .\recolectar.py --source arxiv --max-pages 3`. Ambos recorren la lista de consultas, con un límite de páginas por consulta y una pausa entre solicitudes. Una clave opcional de OpenAlex se toma exclusivamente de la variable de entorno `OPENALEX_API_KEY`; el código no requiere credenciales incrustadas. Las páginas de documentación verificadas son [API OpenAlex](https://help.openalex.org/api/) y [autenticación OpenAlex](https://help.openalex.org/api/authentication/). Revise documentación vigente antes de una ejecución extensa.
