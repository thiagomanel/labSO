## Como compilar e executar

```bash
make # compila
./xeu # roda o binário

# Ou, em uma linha:
make && ./xeu
```

## xeu_utils

No `xeu.cpp` há uma explicação do que pode ser útil para seu lab. Se alterar
algo na pasta `xeu_utils`, recomendo rodar os testes para verificar se ainda
está tudo funcionando:
```bash
make test  # requer c++11
```