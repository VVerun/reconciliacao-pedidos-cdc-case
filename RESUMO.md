## Resumo da Auditoria de Pedidos

Foi realizada uma auditoria comparando o sistema transacional (origem) com a tabela analítica utilizada pelo time comercial (destino). O objetivo foi identificar diferenças entre o estado real dos pedidos e o que está sendo apresentado nos relatórios.

### Resultado da auditoria

Foram identificados **23 pedidos com divergências reais** em um total de pedidos analisados. Além disso, foram encontrados **12 pedidos excluídos corretamente** na origem, que não foram considerados erro por representarem um comportamento esperado do sistema.

### Tipos de problemas encontrados

* **9 pedidos** apresentam divergência de valor: o pedido existe nos dois sistemas, mas o valor registrado no relatório é diferente do valor real.
* **6 pedidos** apresentam divergência de status: o valor está correto, porém o status do pedido no relatório está desatualizado.
* **5 pedidos** estão faltando no destino: existem no sistema transacional, mas não aparecem no relatório comercial.
* **3 pedidos** apresentam divergência simultânea de valor e status.

### Impacto financeiro

* **Faturamento real (origem):** R$ 56.311,22
* **Faturamento reportado (destino):** R$ 40.211,26
* **Diferença identificada:** R$ 16.099,96

Essa diferença representa pedidos ou informações que não estão sendo refletidos corretamente no relatório utilizado pela área comercial.

### Prioridade de correção

A principal prioridade deve ser corrigir os **pedidos faltantes no destino**. Esses casos indicam que vendas existentes no sistema de origem não chegaram à base analítica, impactando diretamente o faturamento apresentado ao time comercial.

Em seguida, devem ser tratadas as divergências de valor e status, que indicam falhas na atualização das informações entre os dois sistemas e podem comprometer indicadores operacionais e financeiros.
