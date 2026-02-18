# E-commerce Brazil Analysis Dashboard

Dashboard interativo desenvolvido para analisar dados de um e-commerce brasileiro. A aplicação integra consultas SQL, análise de dados com Pandas e um modelo de Machine Learning para segmentação de clientes.

## Tecnologias Utilizadas
- **Python 3.12**
- **Streamlit** (Interface e Interatividade)
- **Pandas** (Manipulação de Dados)
- **Plotly** (Visualizações Dinâmicas)
- **SQLite** (Banco de Dados Relacional)
- **Scikit-Learn** (Machine Learning para Segmentação de Clientes)

## Desafios Técnicos Superados
- **Modelagem de Dados:** Implementação de um "Join Triplo" entre as tabelas `orders`, `shopping` e `products` para extrair subcategorias de produtos, superando a falta de relação direta no dataset original.
- **Performance:** Centralização da lógica de filtros em uma única query SQL para reduzir a latência e garantir a consistência dos dados em todas as abas (_Single Source of Truth_).
- **UX/UI:** Organização do dashboard em abas (Visão Geral, Regional e Pagamentos) para facilitar a leitura executiva.
- **Inteligência Artificial:** Implementação de um modelo de clusterização **K-Means** para segmentação de clientes (RFM), com tratamento de dados via `StandardScaler` e nomeação dinâmica de clusters baseada em comportamento de consumo.

## Insights Gerados
- Identificação dos estados com maior faturamento.
- Análise de sazonalidade e evolução diária de vendas.
- Distribuição de _market share_ por método de pagamento.
- Identificação automática de clientes VIP, Ativos e em Risco de Churn para direcionamento de campanhas de marketing.

## Fonte de Dados
- [Kaggle: E-commerce Analytics Dataset Brazil](https://www.kaggle.com/datasets/joocarlosjr/e-commerce-analytics-dataset-brazil)

## Como rodar o projeto
1. Clone o repositório.
2. Instale as dependências: `pip install -r requirements.txt`.
3. Rode o comando: `streamlit run app/app.py`.