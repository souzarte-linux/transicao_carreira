# 🛒 Prompt Mestre — Aplicativo de Lista de Compras Domésticas

> **Objetivo**: Este prompt contém todas as especificações necessárias para reconstruir do zero o aplicativo de gerenciamento de compras domésticas, mantendo funcionalidades, regras de negócio, estrutura e design já definidos.

---

## 1. Visão Geral do Projeto

Aplicativo web mobile-first para **planejamento, execução e análise de compras de supermercado**. O usuário planeja itens em casa, executa a compra no mercado registrando preços/marcas, e depois visualiza dashboards com histórico de gastos.

**Idioma da interface**: Português brasileiro (pt-BR).

### Stack Tecnológica
- **Frontend**: React 18 + TypeScript + Vite
- **Estilização**: Tailwind CSS + shadcn/ui + CSS Variables (design tokens HSL)
- **Ícones**: Lucide React
- **Gráficos**: Recharts
- **Persistência local**: localStorage (via hook customizado `useLocalStorage`)
- **Backend**: Supabase (Lovable Cloud) — tabela `products` para catálogo + Edge Function para busca IA
- **IA**: Lovable AI (modelo `google/gemini-3-flash-preview`) via Edge Function para sugestão de produtos
- **PWA**: vite-plugin-pwa
- **Fonte**: Plus Jakarta Sans (Google Fonts)
- **Roteamento**: React Router DOM
- **SEO**: react-helmet-async
- **Datas**: date-fns com locale ptBR

---

## 2. Arquitetura e Estrutura de Arquivos

```
src/
├── pages/
│   ├── Index.tsx              # Página principal com 3 abas
│   └── NotFound.tsx
├── components/
│   ├── AddItemForm.tsx        # Formulário de adição com autocomplete triplo
│   ├── BottomNavigation.tsx   # Navegação inferior fixa (3 abas)
│   ├── CartTotalFooter.tsx    # Rodapé fixo com total + botão Finalizar
│   ├── CategoryBadge.tsx      # Badge visual de categoria com ícone e cor
│   ├── FloatingActionButton.tsx # FAB "Ir às Compras"
│   ├── PaymentModal.tsx       # Modal de seleção de forma de pagamento
│   ├── PendingItemCard.tsx    # Card de item pendente (legado)
│   ├── PlanningTab.tsx        # Aba de Planejamento
│   ├── ShoppingTab.tsx        # Aba de Compras
│   ├── ShoppingItemCard.tsx   # Card expansível de item na compra
│   ├── ShoppingCategorySection.tsx # Seção colapsável por categoria (compras)
│   ├── SwipeableItemCard.tsx  # Card com gestos de swipe (planejamento)
│   ├── HistoryTab.tsx         # Aba de Histórico/Dashboard
│   └── dashboard/
│       ├── CategoryPieChart.tsx   # Gráfico pizza por categoria
│       ├── StoreBarChart.tsx      # Gráfico barras por estabelecimento
│       ├── SpendingLineChart.tsx  # Gráfico linha evolução de gastos
│       ├── HistoryTable.tsx       # Tabela detalhada com busca/ordenação
│       └── PeriodFilter.tsx       # Filtro de período (toggle group)
├── hooks/
│   ├── useShoppingStore.ts    # Store principal (estado + lógica de negócio)
│   ├── useLocalStorage.ts     # Hook genérico de persistência em localStorage
│   ├── use-mobile.tsx         # Detecção de dispositivo mobile
│   └── use-toast.ts           # Hook de toasts
├── types/
│   └── shopping.ts            # Tipos, constantes, categorias, cores, ícones
├── integrations/supabase/
│   ├── client.ts              # Cliente Supabase (auto-gerado, NÃO editar)
│   └── types.ts               # Tipos do banco (auto-gerado, NÃO editar)
├── index.css                  # Design tokens CSS (cores, sombras, categorias)
└── App.tsx                    # Providers e rotas
supabase/
└── functions/
    └── search-products/
        └── index.ts           # Edge Function de busca IA de produtos
```

---

## 3. Modelo de Dados

### 3.1 Tipos TypeScript (localStorage)

```typescript
type Category = 
  | 'hygiene' | 'cleaning' | 'cereal' | 'fruits' | 'vegetables' 
  | 'meats' | 'dairy' | 'bakery' | 'beverages' | 'snacks' 
  | 'frozen' | 'canned' | 'condiments' | 'pasta' | 'pets' 
  | 'baby' | 'pharmacy' | 'household' | 'others';

type PackageUnit = 'pacote' | 'unidade' | 'gramas' | 'kg';

type PaymentMethod = 
  | 'dinheiro' | 'credito' | 'debito' 
  | 'vale_alimentacao' | 'vale_refeicao' | 'pix' | 'fiado';

type PeriodFilter = 'daily' | 'weekly' | 'monthly' | 'quarterly' | 'yearly';

interface Product {
  id: string;          // UUID
  name: string;
  category: Category;
  createdAt: Date;
}

interface PendingItem {
  id: string;
  productId: string;
  productName: string;
  category: Category;
  quantity: number;
  isSelected: boolean;  // Para seleção em massa
  createdAt: Date;
}

interface ShoppingItem extends Omit<PendingItem, 'isSelected'> {
  isPurchased: boolean;
  purchasedAt?: Date;
  brand?: string;
  store?: string;
  packageUnit?: PackageUnit;
  packageQuantity?: number;
  price?: number;
}

interface ShoppingTrip {
  id: string;
  items: ShoppingItem[];
  startedAt: Date;
  completedAt?: Date;
  totalPrice?: number;
  paymentMethod?: PaymentMethod;
}
```

### 3.2 Banco de Dados (Supabase)

Tabela `products` (catálogo público, sem RLS):
| Coluna     | Tipo      | Default            | Descrição                     |
|------------|-----------|---------------------|-------------------------------|
| id         | UUID PK   | gen_random_uuid()  |                               |
| name       | TEXT      | NOT NULL, UNIQUE   | Nome do produto               |
| category   | TEXT      | NOT NULL           | Categoria (key do enum)       |
| source     | TEXT      | 'manual'           | Origem: 'manual' ou 'online' |
| created_at | TIMESTAMPTZ | now()            |                               |
| updated_at | TIMESTAMPTZ | now()            |                               |

### 3.3 Chaves de localStorage
- `shopping-products` — Products[]
- `shopping-pending` — PendingItem[]
- `shopping-current-trip` — ShoppingTrip | null
- `shopping-history` — ShoppingTrip[]
- `shopping-brands` — string[]
- `shopping-stores` — string[]

---

## 4. Categorias — Labels, Ícones e Cores

19 categorias com labels em pt-BR, ícones Lucide e cores HSL únicas:

| Key          | Label PT-BR           | Ícone Lucide  | Cor HSL              |
|--------------|----------------------|---------------|----------------------|
| fruits       | Frutas               | Apple         | 350, 70%, 55%       |
| vegetables   | Verduras e Legumes   | Carrot        | 120, 50%, 45%       |
| meats        | Carnes               | Beef          | 0, 65%, 50%         |
| dairy        | Laticínios           | Milk          | 40, 70%, 60%        |
| bakery       | Padaria              | Croissant     | 25, 70%, 50%        |
| beverages    | Bebidas              | GlassWater    | 190, 70%, 50%       |
| cereal       | Cereais e Grãos      | Wheat         | 35, 80%, 50%        |
| pasta        | Massas               | Soup          | 50, 60%, 50%        |
| canned       | Enlatados            | Package       | 45, 50%, 45%        |
| frozen       | Congelados           | Snowflake     | 210, 80%, 60%       |
| snacks       | Lanches e Doces      | Candy         | 320, 60%, 55%       |
| condiments   | Temperos e Molhos    | Droplets      | 15, 80%, 50%        |
| hygiene      | Higiene              | Sparkles      | 280, 60%, 55%       |
| cleaning     | Limpeza              | SprayCan      | 200, 80%, 50%       |
| household    | Utilidades           | Wrench        | 220, 30%, 50%       |
| pets         | Pet Shop             | PawPrint      | 25, 50%, 45%        |
| baby         | Bebê                 | Baby          | 300, 50%, 60%       |
| pharmacy     | Farmácia             | Pill          | 170, 60%, 45%       |
| others       | Outros               | Package       | 220, 15%, 50%       |

Cada categoria possui CSS variable `--category-{key}` definida em `index.css` e registrada no Tailwind config para uso como classes `bg-category-{key}`, `text-category-{key}`, `border-category-{key}`.

---

## 5. Funcionalidades por Aba

### 5.1 Aba Planejamento (PlanningTab)

**Header fixo** com título "Planejamento" e contador de itens pendentes.

**Formulário de Adição (AddItemForm)**:
- Campo de texto para nome do produto com autocomplete de 3 fontes (em ordem de prioridade):
  1. **Local** (localStorage) — produtos já usados pelo usuário
  2. **Banco de dados** (Supabase `products`) — catálogo compartilhado
  3. **IA Online** (Edge Function) — busca inteligente via Lovable AI (ativada após 500ms se não houver sugestões locais/DB, mínimo 3 caracteres)
- Ao selecionar uma sugestão, o foco é transferido para o controle de quantidade
- Produtos novos são salvos no banco via `upsert` (onConflict: 'name')
- Dropdown de seleção de categoria (19 opções com ícone)
- Controle de quantidade (−/+), mínimo 1
- Botão de adicionar (+)

**Lista de Pendências**:
- Agrupada por categoria em cards colapsáveis (Collapsible)
- Título da categoria com ícone, label e contagem, alinhados à esquerda
- Itens dentro das categorias com indentação à esquerda e separadores sutis
- Cada item possui:
  - Checkbox de seleção (para transferência em massa)
  - Nome do produto
  - Controles de quantidade (−/+)
  - Botão de lixeira (exclusão individual)
- **Gestos de swipe** (touch + mouse):
  - ← Esquerda: exclui o item (fundo vermelho com ícone Trash2 e label "Excluir")
  - → Direita: move individualmente para Compras (fundo verde com ícone ShoppingCart e label "Comprar")
  - Threshold: 80px, máximo: 100px
  - Animação de slide-out (300ms) antes da ação

**Controles de seleção**:
- Contador "{X} de {Y} selecionados"
- Link "Selecionar todos" / "Desmarcar todos"
- Dica de swipe: "← Deslize para excluir | Deslize para comprar →"

**FAB (Floating Action Button)**:
- Posicionado no canto inferior direito, acima da navegação
- Label: "Ir às Compras" com ícone ShoppingCart e badge de contagem
- Desabilitado quando nenhum item está selecionado
- Ao clicar: transfere todos os itens selecionados para a aba Compras

### 5.2 Aba Compras (ShoppingTab)

**Estado vazio**: Quando não há trip ativa, exibe mensagem "Pronto para comprar?" com botão "Ir para Planejamento".

**Header fixo** com:
- Título "Compras" e progresso "{X} de {Y} itens"
- Botão "Cancelar" (retorna todos os itens ao Planejamento)
- **Campo de busca** em tempo real com ícone de lupa e botão X para limpar
- **Barra de progresso** visual (percentual de itens comprados)

**Comportamento da busca**:
- Expande automaticamente categorias que contêm itens correspondentes
- Oculta categorias sem resultados
- Ao interagir com um item (toque), limpa a busca e fecha o teclado
- A categoria do item interagido permanece expandida

**Lista de compras** (agrupada por categoria em seções colapsáveis):
- Cada categoria mostra badge + contagem (comprados/total) + chevron
- Cada item é um **card expansível** (ShoppingItemCard):
  - **Cabeçalho**: Checkbox circular de comprado (verde quando marcado), nome (riscado se comprado), quantidade editável, badge de categoria, subtotal
  - **Detalhes expandidos** (grid 2 colunas):
    - **Marca**: dropdown dinâmico das marcas já utilizadas + opção "+ Nova marca"
    - **Local de Compra**: dropdown dinâmico dos estabelecimentos + opção "+ Novo local"
    - **Unidade/Embalagem**: dropdown (Pacote, Unidade, Gramas, Kg)
    - **Qtd. Embalagem**: input numérico com comparação com última compra
    - **Preço (R$)**: input numérico com comparação com última compra
  - **Comparação visual com histórico**: bordas coloridas nos campos de embalagem e preço:
    - 🟢 Verde (border-success): valor menor que última compra
    - 🟡 Amarelo (border-warning): valor igual
    - 🔴 Vermelho (border-destructive): valor maior

**Rodapé fixo (CartTotalFooter)**:
- Posicionado acima da navegação inferior
- Ícone de carrinho + progresso + **total em R$**
- **Botão "Finalizar Compras"** (largura total, verde, desabilitado se 0 itens comprados)
- Ao clicar, abre o **PaymentModal**

**PaymentModal**:
- Exibe o total da compra
- Grid de 7 formas de pagamento com ícones: Dinheiro, Crédito, Débito, Vale Alimentação, Vale Refeição, PIX, Fiado
- Botão "Confirmar" (só habilitado com método selecionado)

### 5.3 Aba Histórico (HistoryTab)

**Estado vazio**: Mensagem "Nenhum histórico ainda".

**Header**: Título "Dashboard", contagem de compras + total gasto no período, filtro de período.

**Filtro de período** (ToggleGroup): Diário, Semanal, Mensal (padrão), Trimestral, Anual.

**Gráficos** (2 colunas em desktop, 1 em mobile):
1. **Gráfico Pizza (CategoryPieChart)**: Gastos por categoria (donut chart com labels percentuais)
2. **Gráfico Barras (StoreBarChart)**: Gastos por estabelecimento (barras horizontais, tons de verde, top 6)
3. **Gráfico Linha (SpendingLineChart)**: Evolução de gastos ao longo do tempo (agrupado conforme o período selecionado)

**Tabela Detalhada (HistoryTable)**:
- Colunas: Data, Produto, Categoria, Qtd, Valor
- Cabeçalhos ordenáveis (data, produto, categoria, valor)
- Campo de pesquisa por produto/marca/loja
- Botão "Agrupar por Categoria" (mostra subtotais por categoria)
- Rodapé com total geral

---

## 6. Regras de Negócio Críticas

### 6.1 Transferência de Itens (Planejamento → Compras)

**REGRA FUNDAMENTAL**: A aba Compras funciona como **lista acumulativa e persistente**. Nunca deve ser substituída ao receber novos itens.

- **Transferência em massa** (botão "Ir às Compras"): Move todos os itens selecionados. Se já existe uma trip ativa, os novos itens são **mesclados** (merge). Produtos duplicados têm quantidade incrementada.
- **Transferência individual** (swipe → direita): Move um único item. Se já existe uma trip ativa, o item é acrescentado. Se o produto já existe na trip, a quantidade é incrementada.
- **Implementação obrigatória**: Usar o **functional updater pattern** (`setCurrentTrip(prev => ...)`) para evitar stale closures. NUNCA ler `currentTrip` diretamente do closure.
- Itens transferidos são removidos do Planejamento.

### 6.2 Finalização de Compra
- Itens **comprados** (isPurchased = true) vão para o histórico.
- Itens **não comprados** retornam ao Planejamento (com isSelected = false).
- O total é calculado como soma de (preço × quantidade) de todos os itens.

### 6.3 Cancelamento de Compra
- **Todos** os itens da trip ativa retornam ao Planejamento.
- A trip é descartada (setCurrentTrip(null)).

### 6.4 Marcas e Estabelecimentos
- Listas dinâmicas mantidas em localStorage.
- Ao preencher marca/loja em qualquer item, o valor é salvo na lista para reutilização futura.

### 6.5 Comparação com Histórico
- Para cada produto na aba Compras, o sistema busca a última compra registrada no histórico (trip mais recente com o mesmo productId, isPurchased = true, price definido).
- Labels "última: X" aparecem nos campos de quantidade de embalagem e preço.

---

## 7. Design System

### 7.1 Paleta de Cores (CSS Variables HSL)

```css
:root {
  --background: 150 20% 98%;
  --foreground: 160 30% 15%;
  --card: 0 0% 100%;
  --primary: 162 63% 41%;           /* Verde principal */
  --primary-foreground: 0 0% 100%;
  --secondary: 160 25% 94%;
  --muted: 150 15% 92%;
  --accent: 35 95% 55%;             /* Laranja/dourado */
  --destructive: 0 72% 51%;         /* Vermelho */
  --success: 162 63% 41%;           /* Verde (= primary) */
  --warning: 35 95% 55%;            /* Amarelo (= accent) */
  --info: 200 80% 50%;              /* Azul */
  --nav-height: 4.5rem;
}
```

Modo escuro definido com classe `.dark`.

### 7.2 Tipografia
- Fonte: **Plus Jakarta Sans** (weights: 400, 500, 600, 700)
- Importada via Google Fonts no index.css

### 7.3 Sombras Customizadas
- `shadow-card`: sombra média para cards
- `shadow-elevated`: sombra grande para dropdowns/popovers
- `shadow-fab`: sombra extra-grande para FAB

### 7.4 Utilitários CSS
- `.safe-bottom`: padding inferior que considera nav-height + safe-area-inset-bottom
- `.nav-blur`: backdrop-filter blur(12px) para headers/nav

### 7.5 Componentes shadcn/ui Utilizados
Accordion, Alert Dialog, Avatar, Badge, Button, Calendar, Card, Carousel, Chart, Checkbox, Collapsible, Command, Context Menu, Dialog, Drawer, Dropdown Menu, Form, Hover Card, Input, Input OTP, Label, Menubar, Navigation Menu, Pagination, Popover, Progress, Radio Group, Resizable, Scroll Area, Select, Separator, Sheet, Sidebar, Skeleton, Slider, Sonner, Switch, Table, Tabs, Textarea, Toast, Toggle, Toggle Group, Tooltip.

---

## 8. Navegação

**Bottom Navigation** fixa com 3 abas:
1. **Planejamento** (ClipboardList) — lista de itens pendentes
2. **Compras** (ShoppingCart) — trip ativa de compras (badge pulsante quando há trip ativa)
3. **Histórico** (History) — dashboard e histórico

Apenas uma aba visível por vez (renderização condicional, não tabs).

---

## 9. Edge Function — Busca Inteligente de Produtos

**Endpoint**: `search-products`

**Comportamento**:
1. Recebe `{ query: string }` no body
2. Se query < 2 chars, retorna array vazio
3. Se `LOVABLE_API_KEY` não disponível, faz fallback para detecção local de categoria por keywords
4. Caso contrário, chama Lovable AI (`google/gemini-3-flash-preview`) com prompt em português para sugerir até 5 produtos de supermercado brasileiro com categoria
5. Retorna `{ success: true, suggestions: [{ name, category }] }`

**Keywords de fallback**: Mapeamento extenso de palavras-chave em pt-BR para cada categoria (ex: "maçã,banana,laranja" → fruits).

---

## 10. Persistência e Estado

### Hook `useLocalStorage<T>`
- Inicializa com `localStorage.getItem` (fallback para valor inicial)
- Setter usa functional updater pattern
- Escuta `storage` events para sincronização entre abas
- **Bug conhecido corrigido**: O setter deve usar o `storedValue` atual dentro do callback para evitar valores stale.

### Hook `useShoppingStore`
Centraliza toda a lógica de negócio:
- **Products**: addProduct (dedup por nome), getProductSuggestions
- **Pending Items**: addPendingItem (dedup por productId, incrementa qty), toggleItemSelection, selectAll, deselectAll, remove, updateQuantity
- **Shopping Trip**: startShopping (DEVE usar functional updater), togglePurchased, updateShoppingItem, finishShopping, cancelShopping
- **Move Individual**: moveItemToShopping (DEVE usar functional updater)
- **Computed**: selectedCount, groupedPendingItems, cartTotal, getLastHistoricalItem
- **Brands/Stores**: addBrand, addStore (dedup)

---

## 11. Responsividade e Mobile

- Design **mobile-first** com suporte a desktop
- Safe area insets para dispositivos com notch
- Meta tags: `viewport-fit=cover`, `theme-color: #2eb87b`, `apple-mobile-web-app-capable`
- Gestos de touch (swipe) + fallback para mouse (drag)
- Teclado mobile: campos de busca fazem blur() ao interagir com itens
- PWA configurada via vite-plugin-pwa

---

## 12. Acessibilidade e UX

- `aria-current="page"` na aba ativa
- `focus-visible` rings nos botões de navegação
- Animações: `animate-fade-in`, `animate-slide-up`, `animate-scale-in`
- Toasts de confirmação para ações importantes (iniciar compras, finalizar, cancelar)
- Estados vazios com ilustração e call-to-action em todas as abas

---

## 13. Formato de Moeda

- Moeda: Real brasileiro (R$)
- Formato: `R$ {valor.toFixed(2)}`
- Separador decimal: ponto (padrão JS, exibido como ponto)

---

## 14. Ordem de Implementação Recomendada

1. **Setup**: Criar projeto Vite + React + TypeScript + Tailwind + shadcn/ui
2. **Design tokens**: Configurar index.css com todas as CSS variables e tailwind.config.ts
3. **Tipos**: Definir todos os tipos, constantes, labels, ícones e cores em `types/shopping.ts`
4. **Hooks**: Implementar useLocalStorage e useShoppingStore
5. **Componentes base**: CategoryBadge, BottomNavigation
6. **Aba Planejamento**: AddItemForm → SwipeableItemCard → PlanningTab → FloatingActionButton
7. **Aba Compras**: ShoppingItemCard → ShoppingCategorySection → CartTotalFooter → PaymentModal → ShoppingTab
8. **Aba Histórico**: PeriodFilter → gráficos (Pie, Bar, Line) → HistoryTable → HistoryTab
9. **Integração Supabase**: Tabela products + Edge Function search-products
10. **PWA**: Configurar vite-plugin-pwa
11. **Página principal**: Index.tsx orquestrando as 3 abas
12. **Testes e ajustes**: Validar fluxo completo de transferência de itens

---

## 15. Bugs Conhecidos e Soluções Aplicadas

### Bug: Lista de compras sobrescrita ao transferir itens
**Causa**: Stale closures — funções `startShopping` e `moveItemToShopping` liam `currentTrip` diretamente do closure, obtendo valor desatualizado.
**Solução**: Usar functional updater `setCurrentTrip(prev => ...)` em TODAS as funções que modificam a trip. Remover `currentTrip` das dependências do useCallback.

---

*Este prompt foi gerado em 20/03/2026 com base no estado completo do aplicativo.*
PROMPT_EOF
echo "Done"