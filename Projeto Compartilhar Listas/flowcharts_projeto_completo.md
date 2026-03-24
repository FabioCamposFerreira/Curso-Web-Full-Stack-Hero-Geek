# Fluxogramas do Projeto Share Products

Arquivo com todos os fluxogramas do projeto, separados por ação do usuário.

## 1) Abrir o app

```mermaid
flowchart TD
    A[Executar main.py] --> B[Configurar tema do customtkinter]
    B --> C[Criar janela root]
    C --> D[Chamar init_db]
    D --> E{Banco shareproducts.db existe?}
    E -- Sim --> F[Não recria o banco]
    E -- Não --> G[Ler database.sql]
    G --> H[Criar tabela produtos]
    H --> I[Inserir produtos iniciais]
    F --> J[Chamar atualizar_tela]
    I --> J
    J --> K[Mostrar tela_produtos]
    K --> L[App pronto]
```

## 2) Ver produtos na Tela 1

```mermaid
flowchart TD
    A[Entrar em tela_produtos] --> B[Limpar tela atual]
    B --> C[Criar frame principal]
    C --> D[Criar cabeçalho]
    D --> E[Mostrar botão Carrinho]
    E --> F[Mostrar botão Ler QR]
    F --> G[Criar campo de filtro]
    G --> H[Criar lista scrollável]
    H --> I[Chamar atualizar_produtos]
    I --> J[Limpar itens visuais anteriores]
    J --> K[Buscar produtos com get_produtos]
    K --> L{Existe filtro digitado?}
    L -- Sim --> M[SELECT com WHERE nome LIKE]
    L -- Não --> N[SELECT de todos os produtos]
    M --> O[Renderizar cards dos produtos]
    N --> O
    O --> P[Mostrar botão Adicionar em cada card]
```

## 3) Pesquisar produto na Tela 1

```mermaid
flowchart TD
    A[Usuário digita no campo filtro] --> B[trace_add detecta alteração]
    B --> C[Chamar atualizar_produtos]
    C --> D[Apagar cards atuais]
    D --> E[Chamar get_produtos com texto digitado]
    E --> F{Filtro está vazio?}
    F -- Sim --> G[Buscar todos os produtos]
    F -- Não --> H[Buscar produtos com LIKE]
    G --> I[Montar lista filtrada]
    H --> I
    I --> J[Atualizar tela com os cards encontrados]
```

## 4) Adicionar produto ao carrinho

```mermaid
flowchart TD
    A[Clicar em Adicionar] --> B[Chamar adicionar(produto)]
    B --> C{Produto já existe no carrinho?}
    C -- Sim --> D[Somar 1 na qtd]
    C -- Não --> E[Criar item no carrinho com qtd 1]
    D --> F[Mostrar notificação de sucesso]
    E --> F
    F --> G[Atualizar texto do botão Carrinho]
```

## 5) Abrir Tela 2 do carrinho

```mermaid
flowchart TD
    A[Clicar no botão Carrinho] --> B[Chamar tela_carrinho]
    B --> C[Limpar tela atual]
    C --> D[Criar nova tela]
    D --> E[Mostrar botão Voltar]
    E --> F[Mostrar título Meu Carrinho]
    F --> G{Carrinho está vazio?}
    G -- Sim --> H[Mostrar mensagem Carrinho vazio]
    G -- Não --> I[Criar área scrollável]
    I --> J[Percorrer itens do carrinho]
    J --> K[Renderizar card de cada item]
    K --> L[Mostrar menos, quantidade, mais, total e lixeira]
    L --> M[Salvar referências em itens_carrinho]
    M --> N[Mostrar total geral]
    N --> O[Mostrar botões Limpar e Compartilhar]
```

## 6) Aumentar quantidade de um item

```mermaid
flowchart TD
    A[Clicar no botão +] --> B[Chamar alterar_qtd(pid, 1)]
    B --> C{Item existe no carrinho?}
    C -- Não --> D[Fim]
    C -- Sim --> E[Somar 1 na qtd]
    E --> F{Qtd ficou menor ou igual a 0?}
    F -- Não --> G[Chamar atualizar_item_carrinho]
    G --> H[Atualizar label da quantidade]
    H --> I[Atualizar total do item]
    I --> J[Atualizar total geral]
    J --> K[Atualizar botão Carrinho]
```

## 7) Diminuir quantidade de um item

```mermaid
flowchart TD
    A[Clicar no botão -] --> B[Chamar alterar_qtd(pid, -1)]
    B --> C{Item existe no carrinho?}
    C -- Não --> D[Fim]
    C -- Sim --> E[Subtrair 1 da qtd]
    E --> F{Qtd ficou menor ou igual a 0?}
    F -- Não --> G[Atualizar item visualmente]
    F -- Sim --> H[Chamar remover(pid)]
```

## 8) Remover item do carrinho

```mermaid
flowchart TD
    A[Clicar na lixeira] --> B[Chamar remover(pid)]
    B --> C{Item existe no carrinho?}
    C -- Não --> D[Fim]
    C -- Sim --> E[Remover item do dicionário carrinho]
    E --> F[Mostrar notificação Removido]
    F --> G[Atualizar botão Carrinho]
    G --> H{Item tem card desenhado na tela?}
    H -- Não --> I[Fim]
    H -- Sim --> J[Destruir card visual]
    J --> K[Remover referência de itens_carrinho]
    K --> L{Ainda restam itens no carrinho?}
    L -- Sim --> M[Atualizar total geral]
    L -- Não --> N[Reabrir tela_carrinho]
```

## 9) Limpar carrinho inteiro

```mermaid
flowchart TD
    A[Clicar em Limpar] --> B[Chamar limpar_carrinho]
    B --> C[Mostrar caixa de confirmação]
    C --> D{Usuário confirmou?}
    D -- Não --> E[Fim]
    D -- Sim --> F[Executar carrinho.clear]
    F --> G[Atualizar botão Carrinho]
    G --> H[Reabrir tela_carrinho]
    H --> I[Mostrar carrinho vazio]
```

## 10) Compartilhar carrinho

```mermaid
flowchart TD
    A[Clicar em Compartilhar] --> B[Chamar tela_qr]
    B --> C[Limpar tela atual]
    C --> D[Criar tela de compartilhamento]
    D --> E[Mostrar mensagem Carrinho salvo]
    E --> F[Percorrer carrinho]
    F --> G[Montar lista itens com id, qty e preco]
    G --> H[Chamar salvar_carrinho(itens)]
    H --> I[Gerar código único]
    I --> J{Arquivo carrinhos.json existe?}
    J -- Sim --> K[Ler JSON existente]
    J -- Não --> L[Criar estrutura vazia]
    K --> M[Calcular total]
    L --> M
    M --> N[Salvar carrinho no JSON]
    N --> O[Retornar código]
    O --> P[Mostrar código na tela]
    P --> Q[Gerar imagem QRCode]
    Q --> R[Exibir QR na interface]
    R --> S[Mostrar botão Copiar]
    S --> T[Mostrar botão Novo Carrinho]
```

## 11) Copiar código do carrinho

```mermaid
flowchart TD
    A[Clicar em Copiar] --> B[Executar pyperclip.copy(codigo)]
    B --> C[Mostrar notificação Copiado]
    C --> D[Fim]
```

## 12) Criar novo carrinho depois de compartilhar

```mermaid
flowchart TD
    A[Clicar em Novo Carrinho] --> B[Executar carrinho.clear]
    B --> C[Chamar tela_produtos]
    C --> D[Mostrar lista de produtos vazia no carrinho]
```

## 13) Abrir tela para ler QR ou código

```mermaid
flowchart TD
    A[Clicar em Ler QR] --> B[Chamar tela_qr_reader]
    B --> C[Limpar tela atual]
    C --> D[Criar tela de leitura]
    D --> E[Mostrar campo para digitar código]
    E --> F[Mostrar botão Carregar]
    F --> G[Mostrar botão Abrir Imagem]
    G --> H[Mostrar botão Usar Câmera]
```

## 14) Carregar carrinho digitando o código

```mermaid
flowchart TD
    A[Digitar código e clicar em Carregar] --> B[Chamar carregar_qr(codigo)]
    B --> C[Executar strip e upper no código]
    C --> D[Chamar carregar_carrinho]
    D --> E{Arquivo carrinhos.json existe?}
    E -- Não --> F[Retornar None]
    E -- Sim --> G[Ler JSON e buscar código]
    G --> H{Código encontrado?}
    H -- Não --> I[Mostrar erro Carrinho não encontrado]
    H -- Sim --> J[Limpar carrinho atual]
    J --> K[Percorrer itens carregados]
    K --> L[Buscar produto real com get_produto(id)]
    L --> M{Produto existe no banco?}
    M -- Não --> N[Pular item]
    M -- Sim --> O[Inserir produto no carrinho]
    O --> P[Mostrar notificação Carrinho carregado]
    P --> Q[Abrir tela_carrinho]
```

## 15) Ler carrinho por imagem

```mermaid
flowchart TD
    A[Clicar em Abrir Imagem] --> B[Chamar ler_imagem]
    B --> C[Abrir seletor de arquivos]
    C --> D{Usuário escolheu imagem?}
    D -- Não --> E[Fim]
    D -- Sim --> F[Ler imagem com cv2.imread]
    F --> G[Decodificar com pyzbar.decode]
    G --> H{QR encontrado?}
    H -- Não --> I[Mostrar erro QR Code não encontrado]
    H -- Sim --> J[Extrair texto do QR]
    J --> K[Chamar carregar_qr(codigo)]
    K --> L[Montar carrinho e abrir tela_carrinho]
    G --> M{Erro na leitura?}
    M -- Sim --> N[Mostrar mensagem de erro]
```

## 16) Ler carrinho pela câmera

```mermaid
flowchart TD
    A[Clicar em Usar Câmera] --> B[Chamar ler_camera]
    B --> C[Abrir câmera com cv2.VideoCapture]
    C --> D{Câmera abriu?}
    D -- Não --> E[Mostrar erro Câmera não disponível]
    D -- Sim --> F[Mostrar aviso ESC para cancelar]
    F --> G[Entrar no loop de captura]
    G --> H[Ler frame da câmera]
    H --> I{Leitura do frame ok?}
    I -- Não --> J[Sair do loop]
    I -- Sim --> K[Decodificar frame com pyzbar.decode]
    K --> L{QR encontrado?}
    L -- Sim --> M[Fechar câmera e janelas]
    M --> N[Chamar carregar_qr(codigo)]
    N --> O[Abrir tela_carrinho]
    L -- Não --> P[Mostrar frame na janela]
    P --> Q{Tecla ESC pressionada?}
    Q -- Sim --> R[Sair do loop]
    Q -- Não --> G
    R --> S[Fechar câmera e janelas]
    J --> S
```

## 17) Estrutura resumida de todas as ações

```mermaid
flowchart TD
    A[Iniciar app] --> B[Tela de produtos]
    B --> C[Filtrar produtos]
    B --> D[Adicionar produto]
    B --> E[Abrir carrinho]
    B --> F[Abrir leitor de QR]

    E --> G[Aumentar qtd]
    E --> H[Diminuir qtd]
    E --> I[Remover item]
    E --> J[Limpar carrinho]
    E --> K[Compartilhar]

    K --> L[Gerar código]
    L --> M[Salvar no JSON]
    M --> N[Gerar QR]

    F --> O[Digitar código]
    F --> P[Ler imagem]
    F --> Q[Ler câmera]

    O --> R[Carregar carrinho]
    P --> R
    Q --> R
    R --> E
```
