# Case Técnico — Engenheiro(a) de Dados

**Prazo de entrega:** 7 dias corridos a partir do recebimento
**Esforço estimado:** 6 a 8 horas
**Apresentação:** 8 minutos na entrevista, seguidos de perguntas

---

## Contexto

Uma empresa mantém seus pedidos num sistema transacional (a **origem**). Toda vez que um pedido é criado, alterado ou excluído, o sistema grava um evento num log. Esse log é lido por um processo que atualiza uma tabela analítica (o **destino**), usada pela área de negócio para relatórios.

O time comercial reclamou: os números do relatório não batem com o sistema. Alguns pedidos aparecem com status errado, outros simplesmente não aparecem, e o faturamento total do relatório está diferente do faturamento real.

Ninguém sabe o tamanho do problema nem quais pedidos estão afetados.

**Sua tarefa é descobrir.**

---

## O que você recebe

### `pedidos_origem.csv` — log de eventos do sistema transacional

| Coluna | Descrição |
|---|---|
| `id_pedido` | Identificador do pedido |
| `id_cliente` | Identificador do cliente |
| `status` | Status do pedido naquele momento |
| `valor_total` | Valor do pedido naquele momento |
| `atualizado_em` | Momento em que o evento ocorreu |
| `operacao` | `I` = criação, `U` = alteração, `D` = exclusão |

**Importante:** este arquivo é um histórico, não uma lista de pedidos. Um mesmo `id_pedido` aparece várias vezes, uma para cada mudança que sofreu. Os eventos **não estão em ordem cronológica** — chegaram por uma fila e foram gravados na ordem em que chegaram.

A fila que trouxe esses eventos não oferece nenhuma garantia forte de entrega: um evento pode chegar mais de uma vez, e a captura pode ter começado depois de o sistema já estar em operação. O log também não é necessariamente perfeito — ele reflete o que o sistema conseguiu registrar, não o que idealmente deveria ter registrado.

### `pedidos_destino.csv` — tabela analítica

| Coluna | Descrição |
|---|---|
| `id_pedido` | Identificador do pedido |
| `id_cliente` | Identificador do cliente |
| `status` | Status atual do pedido |
| `valor_total` | Valor atual do pedido |
| `atualizado_em` | Momento da última atualização |

Este arquivo **deveria** conter exatamente o estado atual de cada pedido que existe na origem, e nada além disso.

> Os dois sistemas foram construídos por equipes diferentes, em momentos diferentes. Não assuma que registram as informações da mesma forma.

---

## O que você deve entregar

### 1. Código

Um script (Python, SQL, ou os dois) que:

- Leia os dois arquivos
- Reconstrua, a partir do log, qual é o **estado atual real** de cada pedido
- Compare esse estado com o destino
- Gere o relatório de divergências

Pode usar qualquer biblioteca. Pode usar banco de dados se preferir. O código precisa rodar do início ao fim sem intervenção manual.

### 2. `relatorio_divergencias.csv`

Uma linha por divergência encontrada, com no mínimo:

- `id_pedido`
- `tipo_divergencia` — a classificação que **você** definir
- `valor_origem` e `valor_destino` — o que cada lado diz

Você decide quais tipos de divergência existem e como nomeá-los. Essa classificação é parte da avaliação.

**Atenção:** nem tudo que parece divergência é divergência. Reportar um caso que na verdade está correto (falso positivo) pesa tanto quanto deixar de reportar um caso real. Um relatório de reconciliação em que o negócio não confia é pior do que nenhum relatório.

### 3. `RESUMO.md`

Meia página, escrita para o gerente comercial, não para um técnico. Deve responder:

- Quantos pedidos estão divergentes, de um total de quantos
- Quais são os tipos de problema e quantos casos de cada
- Qual o impacto em dinheiro (diferença entre o faturamento real e o do relatório)
- Qual problema você resolveria primeiro, e por quê

### 4. `DECISOES.md`

O documento mais importante da entrega. Deve conter:

- **Decisões tomadas.** Onde os dados eram ambíguos, o que você decidiu e por quê. Onde havia mais de um caminho possível, qual você escolheu e o que descartou.
- **Casos sem resposta única.** Estes dados contêm situações em que **não existe resposta certa** — só resposta justificada. Identificá-las e explicar seu critério vale mais do que qualquer linha de código deste case. Se você não encontrou nenhuma, provavelmente passou por cima delas.
- **Premissas assumidas.** O que você teve que supor porque o enunciado não dizia.
- **Limitações.** O que sua solução não cobre, ou onde ela quebraria com um volume 1000x maior.
- **Uso de IA.** Quais ferramentas você usou (ChatGPT, Claude, Copilot, Cursor, Lovable, qualquer outra), em quais partes, e para quê.

---

## Sobre uso de inteligência artificial

**É permitido e esperado.** Usamos IA no dia a dia e não faz sentido avaliar você num ambiente artificial.

A única exigência é que você **declare** o uso no `DECISOES.md` e **entenda o que entregou**.

Na entrevista você vai explicar trechos do seu próprio código — escolhidos por nós, não por você — e justificar por que fez daquela forma e não de outra. Código que você não sabe explicar conta contra, tenha sido gerado por IA ou escrito à mão. Uso declarado de IA não conta contra em nenhuma hipótese.

---

## Como será avaliado

| Critério | Peso |
|---|---|
| **Correção** — encontrou as divergências reais, sem inventar as que não existem | 25% |
| **Raciocínio** — decisões e justificativas no `DECISOES.md`, especialmente nos casos ambíguos | 35% |
| **Defesa** — capacidade de explicar o próprio código e sustentar as escolhas | 25% |
| **Comunicação** — o `RESUMO.md` é compreensível para alguém que não é técnico | 15% |

O que **não** é avaliado: elegância do código, interface gráfica, uso de ferramenta sofisticada, quantidade de linhas.

Uma solução simples, correta e bem justificada vale mais que uma solução complexa e mal explicada.

Este case foi desenhado para **não** ter uma resposta única. Duas pessoas competentes podem chegar a números finais diferentes e as duas estarem certas, desde que cada uma saiba explicar por que decidiu como decidiu. É exatamente isso que estamos medindo.

---

## Formato da apresentação

Na entrevista você terá **8 minutos cronometrados** para apresentar. Sugestão de estrutura:

1. O que você encontrou (o resultado, não o processo) — 3 min
2. Como chegou lá, em linhas gerais — 3 min
3. O que faria diferente com mais tempo — 2 min

Não prepare slides. Compartilhe a tela com o código e os arquivos.

Depois da apresentação, faremos perguntas sobre o código e sobre decisões específicas.

---

## Regras

- Prazo: 7 dias corridos. Atraso sem aviso prévio é considerado na avaliação.
- Se travar em algo, pode perguntar — mas traga **contexto, o que já tentou e uma pergunta específica**. Perguntar não conta contra.
- Se identificar um problema no próprio enunciado ou nos dados, aponte. Isso conta a favor.
- Entrega: repositório Git
---



## Um último ponto

O objetivo deste case não é te reprovar. É ver como você pensa quando o problema não vem com instruções completas — que é como todo problema real chega.

Entregar uma solução parcial, com as lacunas identificadas e explicadas honestamente, é melhor do que entregar algo aparentemente completo que você não sabe defender.

Boa sorte.
