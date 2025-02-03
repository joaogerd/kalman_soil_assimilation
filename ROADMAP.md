# **Roadmap Detalhado: Implementação do Filtro de Kalman e Integração de Dados**

## **1. Implementação do Extended Kalman Filter (EKF)**
🔹 *Objetivo:* Expandir o filtro de Kalman para a versão **não-linear** (EKF), permitindo maior flexibilidade na assimilação de dados.  
🔹 *Tarefas:*
   - [ ] Criar uma classe `ExtendedKalmanFilter` que herda de `KalmanFilter`.
   - [ ] Implementar a linearização via **Matriz Jacobiana** para o modelo de estado e matriz de observação.
   - [ ] Modificar o passo de previsão e atualização para incluir a **transformação não linear**.
   - [ ] Testar o EKF com dados sintéticos de umidade do solo para validar a implementação.

📌 *Entrega:* `kalman_soil/kalman_filter_ekf.py`

---

## **2. Desenvolvimento do Módulo de Carregamento de Dados**
🔹 *Objetivo:* Criar um **módulo de carregamento** para integrar dados observacionais e modelados, incluindo BAM/SSiB, NOAH e satélites.  
🔹 *Tarefas:*
   - [ ] Criar a estrutura da classe `DataLoader`.
   - [ ] Implementar métodos para leitura de arquivos NetCDF (`xarray`, `netCDF4`).
   - [ ] Criar funções específicas para carregar:
     - [ ] **Dados do BAM/SSiB** (modelados).
     - [ ] **Dados do NOAH** (modelados).
     - [ ] **Dados de satélite** (SMAP, ASCAT, GLDAS).
   - [ ] Testar a leitura dos arquivos e validar a estrutura dos dados.

📌 *Entrega:* `kalman_soil/data_loader.py`

---

## **3. Integração com Dados de Satélite**
🔹 *Objetivo:* Incorporar dados de **umidade do solo observacional** de satélites na assimilação.  
🔹 *Tarefas:*
   - [ ] Criar funções específicas no `DataLoader` para processar dados de:
     - [ ] **SMAP** (NASA Soil Moisture Active Passive)
     - [ ] **ASCAT** (EUMETSAT Scatterometer)
     - [ ] **GLDAS** (Global Land Data Assimilation System)
   - [ ] Padronizar as unidades e resoluções espaciais para compatibilidade com o modelo.
   - [ ] Interpolação dos dados satelitais para a grade do BAM/SSiB.
   - [ ] Testar a consistência dos dados observacionais com os simulados.

📌 *Entrega:* `kalman_soil/data_loader.py`

---

## **4. Desenvolvimento da Rotina de Assimilação**
🔹 *Objetivo:* Criar um módulo que **integre** os dados observacionais e modelados no filtro de Kalman.  
🔹 *Tarefas:*
   - [ ] Criar um novo módulo `assimilation.py`.
   - [ ] Implementar uma função `run_assimilation()` que:
     - [ ] Carrega os dados modelados e observacionais.
     - [ ] Inicializa o **Filtro de Kalman**.
     - [ ] Define matrizes de erro e ruído.
     - [ ] Executa os passos de **previsão** e **atualização**.
   - [ ] Criar um script para testar a assimilação com dados reais.

📌 *Entrega:* `kalman_soil/assimilation.py`

---

## **5. Validação contra Simulações do MONAN**
🔹 *Objetivo:* Comparar os resultados da assimilação com as previsões do MONAN/NOAH.  
🔹 *Tarefas:*
   - [ ] Criar uma rotina para leitura das saídas do MONAN.
   - [ ] Implementar métricas de avaliação:
     - [ ] **RMSE (Root Mean Square Error)**
     - [ ] **Bias**
     - [ ] **Análise de Anomalias**
   - [ ] Comparar mapas de umidade do solo antes e depois da assimilação.

📌 *Entrega:* `notebooks/validation_MONAN.ipynb`

---

## **6. Visualização e Análise dos Resultados**
🔹 *Objetivo:* Desenvolver gráficos para análise e comparação das estimativas de umidade do solo.  
🔹 *Tarefas:*
   - [ ] Criar um módulo `visualization.py` com funções para:
     - [ ] Geração de mapas de umidade do solo (`cartopy`).
     - [ ] Séries temporais das estimativas (`matplotlib`).
     - [ ] Histogramas das diferenças entre modelo e observação.
   - [ ] Implementar um **notebook Jupyter** com exemplos de análise.

📌 *Entrega:* `kalman_soil/visualization.py`, `notebooks/analysis.ipynb`

---

## **Resumo das Entregas**
✅ **Filtros de Kalman**  
✅ **Leitura de Dados Modelados e Observacionais**  
✅ **Integração de Satélites**  
✅ **Rotina de Assimilação**  
✅ **Validação com MONAN**  
✅ **Visualização dos Resultados**
