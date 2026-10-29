# teste-mutação
# Sistema de Gerenciamento de Biblioteca
Aluna: Giovanna Carla Andrade da Silva

## 1. Sobre o projeto

Este projeto foi desenvolvido para a disciplina de **Manutenção de Software** com o objetivo de aplicar e analisar a técnica de **teste de mutação** em um sistema implementado em Python.

O sistema simula o gerenciamento básico de uma biblioteca, permitindo cadastrar livros e usuários, realizar empréstimos e devoluções, calcular multas por atraso, gerenciar reservas e consultar empréstimos.

Além da implementação do sistema, foram desenvolvidos testes unitários para verificar seu comportamento e utilizada a ferramenta **Cosmic Ray** para avaliar a eficácia desses testes por meio da aplicação automática de mutações no código-fonte.

## 2. Objetivos

- Implementar um sistema simples que permita aplicar técnicas de teste de software.
- Desenvolver testes unitários para verificar os comportamentos esperados do sistema.
- Utilizar uma ferramenta automatizada de teste de mutação.
- Identificar alterações no código que não são detectadas pelos testes existentes.
- Melhorar a suíte de testes com base nos resultados obtidos.
- Comparar os resultados de diferentes execuções e documentar a evolução da eficácia dos testes.

## 3. Tecnologias e ferramentas utilizadas

| Tecnologia ou ferramenta | Finalidade |
|---|---|
| Python | Implementação do sistema de biblioteca. |
| `unittest` | Criação e execução dos testes unitários. |
| Cosmic Ray | Geração e execução de mutações no código-fonte. |
| SQLite | Armazenamento dos resultados das execuções do Cosmic Ray. |
| `cr-report` | Exibição dos resultados do teste de mutação no terminal. |
| `cr-html` | Geração de um relatório HTML para visualização dos resultados. |
| Visual Studio Code | Ambiente de desenvolvimento. |

## 4. Funcionalidades do sistema

O sistema de gerenciamento de biblioteca implementa as seguintes funcionalidades:

- **Cadastro de livros:** registra livros com identificador, título, autor e quantidade de exemplares.
- **Cadastro de usuários:** registra usuários com identificador e nome.
- **Busca de livros:** consulta os dados de um livro cadastrado.
- **Remoção de livros:** permite remover livros respeitando as regras de empréstimos e reservas.
- **Empréstimos:** realiza empréstimos, controla a disponibilidade dos exemplares e respeita o limite de empréstimos por usuário.
- **Devoluções:** registra a devolução, calcula multas por atraso e atualiza a disponibilidade dos exemplares.
- **Reservas:** gerencia a fila de reservas e a disponibilização de exemplares para usuários.
- **Consulta de empréstimos:** lista os empréstimos associados a determinado usuário.

O sistema utiliza estruturas de dados em memória, sem interface gráfica ou banco de dados externo para armazenar os dados funcionais da biblioteca.

## 5. Estrutura do projeto

```text
projeto_final/
├── biblioteca.py
├── test_biblioteca.py
├── cosmic-ray.toml
├── resultados.sqlite
├── resultados_v2.sqlite
├── relatorio_mutacao.html
└── README.md
```

**Descrição dos arquivos:**

- `biblioteca.py`: contém a implementação do sistema de gerenciamento de biblioteca.
- `test_biblioteca.py`: contém os testes unitários desenvolvidos com `unittest`.
- `cosmic-ray.toml`: configura o Cosmic Ray, indicando o módulo analisado e o comando utilizado para executar os testes.
- `resultados.sqlite`: armazena os resultados da primeira execução do teste de mutação.
- `resultados_v2.sqlite`: armazena os resultados da execução posterior, realizada após a ampliação dos testes.
- `relatorio_mutacao.html`: apresenta visualmente os resultados da execução mais recente do teste de mutação.
- `README.md`: documenta o projeto, sua execução e os resultados obtidos.

## 6. Testes unitários

Os testes unitários foram desenvolvidos utilizando o módulo `unittest`, disponível na biblioteca padrão do Python.

A suíte de testes verifica diferentes cenários, incluindo:

- Operações realizadas corretamente.
- Entradas inválidas e situações excepcionais.
- Limites de empréstimos e disponibilidade de exemplares.
- Regras de devolução e cálculo de multas.
- Gerenciamento de reservas.
- Consultas de empréstimos.
- Regras de negócio e condições de contorno.

As datas utilizadas nos testes são controladas em cenários que dependem de datas específicas, contribuindo para a repetibilidade dos resultados.

### Como executar os testes

Com o ambiente virtual ativado e o terminal aberto na pasta `projeto_final`, execute:

```bash
python -m unittest -v test_biblioteca.py
```

A opção `-v` exibe os nomes dos testes executados e seus respectivos resultados.

Na versão utilizada para o experimento, a suíte foi ampliada de 46 para 64 testes unitários. A execução deve terminar com `OK` para confirmar que todos os testes passaram.

## 7. Teste de mutação

### 7.1. Conceito

O teste de mutação é uma técnica utilizada para avaliar a capacidade de uma suíte de testes de identificar alterações incorretas no código-fonte.

A técnica consiste em gerar versões modificadas do programa, chamadas de **mutantes**, por meio de pequenas alterações em operadores, condições, expressões ou valores.

Em seguida, os testes unitários são executados contra essas versões modificadas.

Os resultados podem ser classificados da seguinte maneira:

- **Mutante morto (*killed*):** os testes detectam a alteração e falham para aquele mutante.
- **Mutante sobrevivente (*survived*):** os testes são executados, mas não detectam a alteração.
- **Execução incompleta ou com erro:** a execução não é concluída normalmente e precisa ser analisada separadamente.

Nem todo mutante sobrevivente indica necessariamente uma falha na suíte de testes. Alguns podem ser equivalentes ao programa original, isto é, produzir o mesmo comportamento observável para todas as entradas relevantes. Por isso, os sobreviventes devem ser interpretados com cuidado.

### 7.2. Ferramenta utilizada

Foi utilizada a ferramenta **Cosmic Ray**, responsável por gerar mutações no código Python e executar a suíte de testes para verificar quais alterações são detectadas.

A configuração do experimento está no arquivo `cosmic-ray.toml`:

```toml
[cosmic-ray]
module-path = "biblioteca.py"
timeout = 10.0
excluded-modules = []
test-command = "python -m unittest test_biblioteca.py"

[cosmic-ray.distributor]
name = "local"
```

O experimento foi executado localmente, utilizando o distribuidor `local` do Cosmic Ray.

### 7.3. Etapas do experimento

O trabalho foi realizado em duas etapas principais.

**Primeira etapa — execução inicial**

Inicialmente, o teste de mutação foi executado com a suíte de testes original, composta por 46 testes unitários.

Os resultados permitiram identificar mutantes que sobreviviam à execução, indicando pontos nos quais os testes existentes não detectavam determinadas alterações.

**Segunda etapa — ampliação da suíte de testes**

Após analisar os sobreviventes, foram adicionados testes para verificar outros cenários e reforçar a cobertura das regras de negócio, incluindo limites, condições específicas e interações entre usuários, empréstimos e reservas.

Em seguida, o experimento foi executado novamente, utilizando um novo banco de resultados, `resultados_v2.sqlite`, para registrar a nova execução.

Essa abordagem permitiu comparar os resultados antes e depois da ampliação dos testes.

### 7.4. Comandos utilizados

Os comandos abaixo devem ser executados no terminal, dentro da pasta do projeto, com o ambiente virtual ativado.

Verificação da configuração:

```bash
cosmic-ray --verbosity=INFO baseline cosmic-ray.toml
```

Inicialização do banco de resultados da primeira execução:

```bash
cosmic-ray init cosmic-ray.toml resultados.sqlite
```

Execução das mutações iniciais:

```bash
cosmic-ray exec cosmic-ray.toml resultados.sqlite
```

Consulta do relatório inicial:

```bash
cr-report resultados.sqlite
```

Inicialização do banco da segunda execução:

```bash
cosmic-ray init cosmic-ray.toml resultados_v2.sqlite
```

Execução das mutações após a ampliação dos testes:

```bash
cosmic-ray exec cosmic-ray.toml resultados_v2.sqlite
```

Consulta dos resultados mais recentes:

```bash
cr-report resultados_v2.sqlite
```

Para visualizar os mutantes sobreviventes e as alterações realizadas:

```bash
cr-report resultados_v2.sqlite --surviving-only --show-diff
```

Geração do relatório HTML:

```bash
cr-html resultados_v2.sqlite > relatorio_mutacao.html
```

O arquivo `relatorio_mutacao.html` pode ser aberto em um navegador para consultar a lista de execuções e seus resultados.

**Observação:** os bancos de resultados devem ser inicializados separadamente para cada experimento. Ao repetir uma execução, utilize um novo arquivo de banco quando desejar preservar e comparar os resultados anteriores.

## 8. Resultados obtidos

Foram realizadas duas execuções do teste de mutação, cada uma com 233 mutantes.

| Métrica | Primeira execução | Segunda execução |
|---|---:|---:|
| Total de mutantes | 233 | 233 |
| Execuções concluídas | 233 | 233 |
| Mutantes mortos | 177 | 211 |
| Mutantes sobreviventes | 56 | 22 |
| Percentual de sobreviventes | 24,03% | 9,44% |
| Percentual de mutantes mortos | 75,97% | 90,56% |

Na primeira execução, 177 dos 233 mutantes foram mortos pelos testes, enquanto 56 sobreviveram.

Após a ampliação da suíte de testes, a segunda execução apresentou 211 mutantes mortos e 22 sobreviventes.

A taxa de mutantes mortos aumentou de **75,97% para 90,56%**, correspondendo a uma melhoria de aproximadamente **14,59 pontos percentuais**.

Além disso, o número de mutantes sobreviventes diminuiu de 56 para 22, uma redução de 34 sobreviventes.

Os resultados indicam que os testes adicionais aumentaram a capacidade da suíte de detectar as alterações introduzidas pelo Cosmic Ray.

### 8.1. Interpretação dos resultados

A redução dos mutantes sobreviventes demonstra que a ampliação dos testes permitiu verificar comportamentos que não estavam suficientemente contemplados na suíte inicial.

Entretanto, a taxa de mutantes mortos não deve ser interpretada isoladamente como uma garantia de ausência de defeitos no sistema. O resultado depende dos operadores de mutação utilizados, dos mutantes gerados e dos comportamentos verificados pelos testes.

Os 22 mutantes sobreviventes representam oportunidades para investigações futuras. Sua análise pode revelar condições não testadas, comportamentos que precisam de verificações adicionais ou mutantes equivalentes ao código original.

## 9. Limitações

O projeto apresenta algumas limitações:

- Os dados da biblioteca são mantidos em memória e não persistem entre execuções do programa.
- O sistema implementa um conjunto delimitado de funcionalidades, não contemplando todas as necessidades de uma biblioteca real.
- O teste de mutação avalia os mutantes gerados pela ferramenta, não todas as alterações possíveis no código.
- A existência de mutantes sobreviventes não significa automaticamente que todos correspondem a defeitos nos testes.
- A taxa de mutantes mortos não garante que o programa esteja livre de erros.

Essas limitações devem ser consideradas ao interpretar os resultados do experimento.

## 10. Conclusão

O desenvolvimento do sistema de gerenciamento de biblioteca permitiu aplicar, de maneira prática, os conceitos de testes unitários e teste de mutação.

A utilização do Cosmic Ray possibilitou gerar alterações automaticamente no código e avaliar se os testes existentes eram capazes de detectá-las.

A comparação entre as duas execuções demonstrou uma melhoria na eficácia da suíte de testes: a taxa de mutantes mortos passou de 75,97% para 90,56%, enquanto o número de sobreviventes diminuiu de 56 para 22.

Conclui-se que o teste de mutação foi útil para identificar oportunidades de melhoria nos testes unitários e orientar a criação de novos casos de teste. A experiência também evidenciou a importância de analisar os resultados da ferramenta, em vez de considerar apenas a execução bem-sucedida dos testes convencionais.

## 11. Referências

- **Python — documentação oficial:** https://docs.python.org/3/
- **`unittest` — framework de testes unitários do Python:** https://docs.python.org/3/library/unittest.html
- **Cosmic Ray — documentação oficial:** https://cosmic-ray.readthedocs.io/
