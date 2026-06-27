# Como executar a atividade

Instale a dependência tabulate:

```bash
pip install tabulate
```


## Como executar

```bash
python3 main.py
```

## Perguntas

### Onde foi usada a fila?
- Em fila_atendimento

### Onde foi usada a pilha?
- No histórico de ações (historico_acoes)

### Onde foi usada a árvore?
- Para salvar as ocorrências por id e fazer a busca rápida.

### Onde foi usada a heap?
- Para salvar a ocorrencia de maior prioridade

### Onde foi usada a hash table?
- Foi usada para buscar as ocorrencias por nome ou tipo

### Qual algoritmo de ordenação foi implementado?
- Bubble Sort

### Qual estrutura foi mais adequada para busca rápida?
- Hash Table

### Qual estrutura foi mais adequada para atendimento por prioridade?
- A heap. O extrair_max retorna a ocorrência de mais alta prioridade

### Qual foi a maior dificuldade do grupo?
- O desfazer ações, principalmente ao desfazer uma ocorrência, pois precisa atualizar todas as estruturas novamente.
