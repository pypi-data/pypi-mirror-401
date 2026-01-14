# mtcli-prevsession

Plugin do **mtcli** para exibição dos **preços estruturais do pregão anterior** e **níveis percentuais derivados do preço de ajuste**, utilizando dados do **MetaTrader 5 (MT5)**.

Projetado para **day trade na B3**, com foco em:
- preparação de pregão (inclusive em fins de semana),
- leitura objetiva de contexto,
- integração com ferramentas de volume (VWAP, Volume Profile, VAP),
- saída acessível para leitores de tela (NVDA / JAWS).

---

## Funcionalidades

O plugin exibe:

### Pregão anterior
- Preço de ajuste
- Preço de fechamento
- VWAP do dia
- Preço mínimo
- Preço máximo

### Pregão atual
- Preço de abertura (quando existir)

### Níveis percentuais
- Variações simétricas de **0,5% até 3,0%**
- Calculadas **a partir do preço de ajuste**
- Níveis acima e abaixo (alta / baixa)

---

## Exemplo de saída

```text
Ativo: WING26
------------------------------------------------------------
Pregão anterior:
Preço de ajuste:      164215
Preço de fechamento: 164100
VWAP do dia:          164878
Preço mínimo:        164010
Preço máximo:        166260
------------------------------------------------------------
Pregão atual:
Preço de abertura:   166250
------------------------------------------------------------
Variações percentuais em relação ao ajuste:
0.5% acima: 165036 | 0.5% abaixo: 163394
1.0% acima: 165857 | 1.0% abaixo: 162573
...
````

---

## Instalação

### Requisitos

* Python 3.10+
* MetaTrader 5 instalado e configurado
* Biblioteca Python `MetaTrader5`
* `mtcli`

### Instalação via Poetry (desenvolvimento)

```bash
poetry install
```

Ou instale diretamente no ambiente do `mtcli`:

```bash
pip install .
```

---

## Uso

```bash
mtcli ps --symbol WING26
```

### Parâmetros

| Opção            | Descrição                                           |
| ---------------- | --------------------------------------------------- |
| `--symbol`, `-s` | Ativo negociado no MT5 (ex: WING26, WINJ26, WDOG26) |

---

## Arquitetura

O plugin segue **MVC explícito**, padrão adotado no ecossistema `mtcli`.

```text
mtcli_prevsession/
├── cli.py          # Comando Click
├── model.py        # Coleta de dados e cálculos
├── view.py         # Formatação e exibição
├── conf.py         # Configurações globais (ex: DIGITOS)
└── __init__.py
```

### Model

* Usa `copy_rates_from_pos`
* Não depende de datas ou timezone
* Funciona corretamente em:

  * dias úteis
  * fins de semana
  * feriados
  * virada de contrato

### View

* Saída 100% textual
* Formatação numérica baseada em `DIGITOS`
* Compatível com leitores de tela

### Controller

* Orquestra model e view
* Não contém regras de negócio

---

## Decisões importantes de projeto

### Identificação do pregão

> O pregão anterior **nunca é identificado por data**, apenas por posição do candle diário.

Isso evita erros comuns no MT5:

* timezone
* feriados
* execução fora do horário de pregão

### Preço de ajuste

* Usado como **âncora estrutural**
* Base para níveis percentuais
* Compatível com metodologias baseadas em VWAP e leilão

---

## Integração com outros plugins

Este plugin foi projetado para trabalhar em conjunto com:

* `mtcli-vwap`
* `mtcli-vap`
* `mtcli-market`
* `mtcli-timesales`

Permitindo:

* checklist pré-trade automático
* leitura de confluência
* classificação de viés (comprador / vendedor / neutro)

---

## Limitações conhecidas

* O ajuste utilizado é o **close do candle diário**
* O ajuste oficial da B3 pode diferir

> Versões futuras podem incorporar o ajuste oficial via Times & Trades.

---

## Roadmap (ideias futuras)

* [ ] Flag `--json`
* [ ] Classificação automática de contexto
* [ ] Integração direta com checklist pré-trade
* [ ] Ajuste oficial da B3
* [ ] VWAP real calculado por ticks

---

## Licença

GPL

---

## Autor

Valmir França
Day trader  Desenvolvedor Python  Arquitetura CLI  Volume & Auction Market Theory
