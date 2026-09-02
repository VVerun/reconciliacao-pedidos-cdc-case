## Decisões tomadas

### 1. Limpeza e padronização dos dados

Antes da comparação, padronizei os dados da origem e do destino para evitar divergências causadas apenas por formatação. Removi espaços em branco nas extremidades dos textos e converti todos os valores da coluna `status` para caixa alta.

Também removi registros duplicados da origem e do destino para garantir que eventos repetidos não alterassem o resultado da reconciliação, já que o enunciado informa que a fila pode entregar o mesmo evento mais de uma vez.

### 2. Tratamento das datas

Os eventos da origem e do destino utilizam formatos de data diferentes. Converti ambos para o tipo `datetime` e removi a informação de fuso horário para que todos os registros fossem comparados utilizando o mesmo relógio local.

### 3. Reconstrução do estado atual dos pedidos

O arquivo `pedidos_origem.csv` representa um histórico de eventos, e não o estado atual dos pedidos. Por isso, ordenei os eventos por `id_pedido` e `atualizado_em` antes de reconstruir o estado final.

Também utilizei `forward fill` para preencher informações ausentes em eventos de atualização, assumindo que um update pode registrar apenas os campos alterados e manter os demais iguais ao último estado conhecido.

Para obter o estado atual de cada pedido utilizei o último evento cronológico (`tail(1)`), preservando a linha completa do evento mais recente.

### 4. Empate de eventos no mesmo horário

Considerei um caso em que dois eventos do mesmo pedido possuem exatamente o mesmo timestamp. Nessa situação defini uma prioridade entre operações:

- `I` (Insert) → prioridade 1
- `U` (Update) → prioridade 2
- `D` (Delete) → prioridade 3

Assim, uma exclusão prevalece sobre uma atualização registrada no mesmo instante.

### 5. Estratégia de reconciliação

A comparação entre origem e destino foi feita utilizando um **Full Outer Join** pela coluna `id_pedido`. Essa abordagem permite identificar três situações:

- pedidos existentes apenas na origem;
- pedidos existentes apenas no destino;
- pedidos presentes nos dois sistemas.

Depois do cruzamento, as divergências foram classificadas de forma vetorizada com `numpy.select`, evitando processamento linha a linha.

Também comparei valores monetários utilizando arredondamento para duas casas decimais (`round(2)`), evitando diferenças causadas por precisão de ponto flutuante.

---

## Casos sem resposta única

### Pedidos sem evento de criação (`I`)

O enunciado informa que a captura do log pode ter começado depois de o sistema já estar em operação. Por isso, um pedido cujo primeiro evento seja `U` foi considerado válido e reconstruído a partir do primeiro evento disponível.

### Atualizações parciais

Assumi que um evento de atualização pode não trazer todos os campos do pedido. Nesses casos, mantive o último valor conhecido para reconstruir o estado completo do pedido.

### Pedidos excluídos

Quando o último evento da origem é uma operação `D` e o pedido não existe no destino, considerei esse caso como comportamento esperado e não como divergência.

---

## Premissas assumidas

- O `id_pedido` identifica unicamente cada pedido.
- O evento com maior timestamp representa o estado mais recente do pedido.
- Eventos duplicados representam reentregas da fila e não novas alterações.
- Valores ausentes em atualizações representam campos não modificados.

---

## Limitações da solução

A solução foi desenvolvida utilizando Python e Pandas, mantendo todos os dados em memória. Ela funciona bem para o volume deste case, mas não seria a abordagem ideal para bases muito maiores.

Em um cenário com milhões de eventos, a reconstrução do estado poderia ser feita de forma incremental utilizando SQL (funções de janela) ou ferramentas distribuídas como PySpark, reduzindo consumo de memória e tempo de processamento.

---

## Uso de IA

Utilizei **ChatGPT** e **Gemini** como ferramentas de apoio durante o desenvolvimento do case.

O uso foi restrito a:
- revisão da lógica de reconciliação e validação de possíveis casos de borda;
- discussão de melhorias na implementação (como deduplicação, reconstrução do estado final e classificação vetorizada);
- revisão e refinamento da documentação (`RESUMO.md` e `DECISOES.md`).

Toda a implementação, execução dos testes, validação dos resultados e compreensão das decisões apresentadas foram realizadas por mim.