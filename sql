SELECT i.descricao "Item",
		CONCAT("R$", ROUND(avg(hp.preco), 2)) "Média últimos 3 dias",
		CONCAT("R$", i.precovendido) "Preço vendido",
		CASE WHEN (i.precovendido > avg(hp.preco)) THEN CONCAT('+ ', ABS(ROUND(((avg(hp.preco) - i.precovendido) / i.precovendido) * 100, 2)), '%')
		WHEN (i.precovendido < avg(hp.preco)) THEN CONCAT('- ', ABS(ROUND(((avg(hp.preco) - i.precovendido) / i.precovendido) * 100, 2)), '%')
		end as "R"
FROM historicoprecos hp
INNER JOIN item i on i.coditem = hp.coditem
WHERE hp.datacons BETWEEN (CURRENT_DATE - 3) and CURRENT_DATE
GROUP BY hp.coditem, i.coditem