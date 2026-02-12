-- Query principal para os gráficos e KPIs com filtro
SELECT 
    o.Id, 
    o.Order_Date, 
    o.Total, 
    o.Purchase_Status,
    p.Subcategory
FROM orders o
JOIN shopping s ON o.Id = s.Id
JOIN products p ON s.Product = p.Product_Name
WHERE o.Purchase_Status = 'Confirmado'; -- Exemplo de filtro