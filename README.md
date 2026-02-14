# E-commerce Brazil Analysis Dashboard

Dashboard interativo desenvolvido para analisar dados de um e-commerce brasileiro, integrando informações de vendas, produtos, clientes e logística.

## Tecnologias Utilizadas
- **Python 3.12**
- **Streamlit** (Interface e Interatividade)
- **Pandas** (Manipulação de Dados)
- **Plotly** (Visualizações Dinâmicas)
- **SQLite** (Banco de Dados Relacional)

## Desafios Técnicos Superados
- **Modelagem de Dados:** Implementação de um "Join Triplo" entre as tabelas `orders`, `shopping` e `products` para extrair subcategorias de produtos, superando a falta de relação direta no dataset original.
- **Performance:** Centralização da lógica de filtros em uma única query SQL para reduzir a latência e garantir a consistência dos dados em todas as abas (_Single Source of Truth_).
- **UX/UI:** Organização do dashboard em abas (Visão Geral, Regional e Pagamentos) para facilitar a leitura executiva.

## Insights Gerados
- Identificação dos estados com maior faturamento.
- Análise de sazonalidade e evolução diária de vendas.
- Distribuição de _market share_ por método de pagamento.

## Como rodar o projeto
1. Clone o repositório.
2. Instale as dependências: `pip install -r requirements.txt`.
3. Rode o comando: `streamlit run app/app.py`.