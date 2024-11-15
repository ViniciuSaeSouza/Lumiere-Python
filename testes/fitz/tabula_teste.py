import tabula

tables = tabula.read_pdf("conta-ma.pdf", pages="1", encoding="utf-8")

teste = tables[1]
print(teste.get("kWh"))


# teste = tables.get("Qtd.kWh/mês")
# print(teste)