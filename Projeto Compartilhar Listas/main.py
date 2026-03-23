"""
Share Products - Aplicação Principal
Sistema de compartilhamento de produtos via QR Code
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
import qrcode
from PIL import Image, ImageTk
import io
import pyperclip
from database import Database
from typing import Dict, List
import cv2
import numpy as np

# Lazy loader for pyzbar.decode to avoid import-time failures when zbar native
# DLLs are missing on Windows. The function returns the `decode` callable or
# raises RuntimeError with the underlying error message so callers can show
# a helpful message to the user.
def ensure_pyzbar_decode():
    try:
        from pyzbar.pyzbar import decode
        return decode
    except Exception as e:
        raise RuntimeError(str(e))


class ShareProductsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("Share Products")
        self.geometry("1000x700")
        
        # Notificação temporária (toast)
        self.notification_label = None
        
        # Banco de dados
        self.db = Database()
        
        # Carrinho atual (em memória)
        self.carrinho_atual: Dict[int, Dict] = {}
        # Formato: {produto_id: {"produto": dict, "quantidade": int}}
        # Referência ao botão do carrinho (para atualizar contador sem recriar a tela)
        self.btn_carrinho = None
        # Cache de cards de produto para atualizações parciais (evita redraw completo)
        self.product_cards = {}
        # Cache de cards do carrinho (para sincronizar sem recriar)
        self.cart_items_frame = None
        self.cart_item_cards = {}  # produto_id -> {widgets com referências}
        self.cart_total_label = None
        
        # Container principal
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Iniciar com tela principal
        self.mostrar_tela_principal()
    
    def limpar_tela(self):
        """Remove todos os widgets do container principal"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def mostrar_notificacao(self, mensagem: str, duracao_ms: int = 2000):
        """Mostra uma notificação não-bloqueante (toast) no topo da tela"""
        # Remover notificação anterior se existir
        if self.notification_label:
            try:
                self.notification_label.destroy()
            except Exception:
                pass
        
        # Criar label de notificação
        self.notification_label = ctk.CTkLabel(
            self,
            text=mensagem,
            font=("Arial", 12),
            text_color="white",
            fg_color="#2ECC71",
            corner_radius=5
        )
        self.notification_label.place(relx=0.5, y=10, anchor="n")
        
        # Agendar remoção após duracao_ms
        def remover():
            try:
                if self.notification_label:
                    self.notification_label.destroy()
                    self.notification_label = None
            except Exception:
                pass
        
        self.after(duracao_ms, remover)
    
    # ===== TELA 1: PRINCIPAL - LISTAGEM DE PRODUTOS =====
    
    def mostrar_tela_principal(self):
        """Tela principal com listagem de produtos"""
        self.limpar_tela()
        
        # Header
        header = ctk.CTkFrame(self.main_container)
        header.pack(fill="x", padx=10, pady=10)
        
        titulo = ctk.CTkLabel(header, text="📦 Share Products", 
                             font=("Arial", 24, "bold"))
        titulo.pack(side="left", padx=10)
        
        # Botão carrinho (guardamos referência para atualizações locais rápidas)
        carrinho_info = f"🛒 Carrinho ({len(self.carrinho_atual)})"
        btn_carrinho = ctk.CTkButton(header, text=carrinho_info,
                                     command=self.mostrar_tela_carrinho,
                                     fg_color="#2ECC71", hover_color="#27AE60")
        btn_carrinho.pack(side="right", padx=10)
        self.btn_carrinho = btn_carrinho
        
        # Botão Ler QR Code
        btn_ler_qr = ctk.CTkButton(header, text="📷 Ler QR Code",
                                   command=self.mostrar_tela_ler_qrcode,
                                   fg_color="#9B59B6", hover_color="#8E44AD")
        btn_ler_qr.pack(side="right", padx=10)
        
        # Filtro
        filtro_frame = ctk.CTkFrame(self.main_container)
        filtro_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(filtro_frame, text="🔍 Filtrar:").pack(side="left", padx=5)
        
        self.filtro_entry = ctk.CTkEntry(filtro_frame, placeholder_text="Digite o nome do produto...")
        self.filtro_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.filtro_entry.bind("<KeyRelease>", lambda e: self.atualizar_lista_produtos())
        
        btn_limpar = ctk.CTkButton(filtro_frame, text="Limpar", width=80,
                                   command=self.limpar_filtro)
        btn_limpar.pack(side="right", padx=5)
        
        # Frame para lista de produtos (com scroll)
        self.produtos_frame = ctk.CTkScrollableFrame(self.main_container)
        self.produtos_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Carregar produtos
        self.atualizar_lista_produtos()
    
    def limpar_filtro(self):
        """Limpa o filtro de pesquisa"""
        self.filtro_entry.delete(0, "end")
        self.atualizar_lista_produtos()
    
    def atualizar_lista_produtos(self):
        """Atualiza a lista de produtos com base no filtro (sincroniza sem redraw completo)"""
        # Buscar produtos com filtro
        filtro = self.filtro_entry.get() if hasattr(self, 'filtro_entry') else ""
        produtos = self.db.get_produtos(filtro)
        
        # Se não há produtos, mostrar mensagem
        if not produtos:
            # Limpar cards em cache (já não existem)
            self.product_cards.clear()
            # Destruir widgets do frame
            for widget in self.produtos_frame.winfo_children():
                widget.destroy()
            ctk.CTkLabel(self.produtos_frame, 
                        text="Nenhum produto encontrado 😕",
                        font=("Arial", 16)).pack(pady=20)
            return
        
        # Obter IDs dos produtos atuais
        ids_atuais = {p["id"] for p in produtos}
        ids_em_cache = set(self.product_cards.keys())
        
        # Remover cards que não estão mais na lista (foram filtrados)
        for pid in ids_em_cache - ids_atuais:
            try:
                card = self.product_cards[pid]
                frame = card.get("frame")
                if frame:
                    frame.destroy()
                del self.product_cards[pid]
            except Exception:
                pass
        
        # Adicionar/atualizar cards
        for idx, produto in enumerate(produtos):
            pid = produto["id"]
            
            if pid in self.product_cards:
                # Card já existe: atualizar informações se necessário
                # (por enquanto apenas deixamos como está, pois preço/nome não muda)
                pass
            else:
                # Novo card: criar e adicionar
                self.criar_card_produto(produto, idx)
        
        # Limpar label "nenhum produto encontrado" se houver (raro, mas seguro)
        for widget in self.produtos_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and "Nenhum produto" in widget.cget("text"):
                widget.destroy()
    
    def criar_card_produto(self, produto: Dict, index: int):
        """Cria um card de produto"""
        row = index // 2
        col = index % 2
        
        card = ctk.CTkFrame(self.produtos_frame, corner_radius=10)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Configurar colunas do grid
        self.produtos_frame.grid_columnconfigure(0, weight=1)
        self.produtos_frame.grid_columnconfigure(1, weight=1)
        
        # Nome do produto
        nome = ctk.CTkLabel(card, text=produto["nome"], 
                           font=("Arial", 14, "bold"),
                           wraplength=350)
        nome.pack(padx=10, pady=(10, 5))
        
        # Descrição
        if produto.get("descricao"):
            desc = ctk.CTkLabel(card, text=produto["descricao"],
                               font=("Arial", 11),
                               text_color="gray",
                               wraplength=350)
            desc.pack(padx=10, pady=5)
        
        # Frame inferior (preço + botão)
        bottom = ctk.CTkFrame(card, fg_color="transparent")
        bottom.pack(fill="x", padx=10, pady=10)
        
        # Preço
        preco = ctk.CTkLabel(bottom, 
                            text=f"R$ {produto['preco_unitario']:.2f}",
                            font=("Arial", 16, "bold"),
                            text_color="#2ECC71")
        preco.pack(side="left")
        
        # Botão adicionar
        ja_no_carrinho = produto["id"] in self.carrinho_atual
        btn_text = "✓ No carrinho" if ja_no_carrinho else "🛒 Adicionar"
        btn_color = "#95A5A6" if ja_no_carrinho else "#3498DB"
        
        btn_add = ctk.CTkButton(bottom, text=btn_text,
                               command=lambda p=produto: self.adicionar_ao_carrinho(p),
                               fg_color=btn_color,
                               hover_color="#2C3E50" if ja_no_carrinho else "#2980B9",
                               width=120)
        btn_add.pack(side="right")
        # Salvar referência para atualizações locais (ex: mudar texto/cor ao adicionar)
        try:
            self.product_cards[produto["id"]] = {
                "frame": card,
                "btn_add": btn_add
            }
        except Exception:
            # Se algo falhar aqui, continuamos sem cache (não crítico)
            pass
    
    def adicionar_ao_carrinho(self, produto: Dict):
        """Adiciona um produto ao carrinho"""
        if produto["id"] in self.carrinho_atual:
            # Já está no carrinho, apenas incrementa
            self.carrinho_atual[produto["id"]]["quantidade"] += 1
        else:
            # Adiciona novo item
            self.carrinho_atual[produto["id"]] = {
                "produto": produto,
                "quantidade": 1
            }
        
        # Mostra notificação não-bloqueante (sem modal)
        self.mostrar_notificacao(f"✅ {produto['nome']} adicionado!")
        # Atualiza contador do carrinho sem recriar toda a tela
        self.atualizar_info_carrinho()
        # Atualiza apenas o botão do produto (se o card estiver em cache) para evitar redraw
        card = self.product_cards.get(produto.get("id"))
        if card:
            try:
                btn = card.get("btn_add")
                btn.configure(text="✓ No carrinho", fg_color="#95A5A6", hover_color="#2C3E50")
            except Exception:
                pass
        else:
            # Fallback: recarregar lista (caso o card não exista ainda)
            self.atualizar_lista_produtos()
    
    # ===== TELA 2: CARRINHO =====
    
    def mostrar_tela_carrinho(self):
        """Tela do carrinho de compras"""
        self.limpar_tela()
        self.cart_item_cards.clear()  # Limpar cache de cards antigos
        
        # Header
        header = ctk.CTkFrame(self.main_container)
        header.pack(fill="x", padx=10, pady=10)
        
        btn_voltar = ctk.CTkButton(header, text="← Voltar",
                                   command=self.mostrar_tela_principal,
                                   width=100)
        btn_voltar.pack(side="left", padx=10)
        
        titulo = ctk.CTkLabel(header, text="🛒 Meu Carrinho",
                             font=("Arial", 24, "bold"))
        titulo.pack(side="left", padx=20)
        
        # Verificar se há itens
        if not self.carrinho_atual:
            vazio = ctk.CTkLabel(self.main_container,
                                text="Carrinho vazio 🛒\n\nAdicione produtos para começar!",
                                font=("Arial", 18))
            vazio.pack(expand=True)
            return
        
        # Frame para itens (com scroll)
        self.cart_items_frame = ctk.CTkScrollableFrame(self.main_container, height=400)
        self.cart_items_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Listar itens
        for produto_id, item in self.carrinho_atual.items():
            self.criar_card_item_carrinho(self.cart_items_frame, produto_id, item)
        
        # Footer com total e botões
        footer = ctk.CTkFrame(self.main_container)
        footer.pack(fill="x", padx=10, pady=10)
        
        # Valor total
        total = self.calcular_total()
        self.cart_total_label = ctk.CTkLabel(footer, 
                                   text=f"Total: R$ {total:.2f}",
                                   font=("Arial", 20, "bold"),
                                   text_color="#2ECC71")
        self.cart_total_label.pack(side="left", padx=20)
        
        # Botões
        btn_limpar = ctk.CTkButton(footer, text="🗑️ Limpar Carrinho",
                                   command=self.limpar_carrinho,
                                   fg_color="#E74C3C", hover_color="#C0392B")
        btn_limpar.pack(side="right", padx=10)
        
        btn_compartilhar = ctk.CTkButton(footer, text="📤 Compartilhar",
                                        command=self.compartilhar_carrinho,
                                        fg_color="#9B59B6", hover_color="#8E44AD",
                                        width=150)
        btn_compartilhar.pack(side="right", padx=10)
    
    def sincronizar_tela_carrinho(self):
        """Sincroniza (atualiza) a tela do carrinho sem recriar widgets"""
        # Atualizar total
        if self.cart_total_label:
            try:
                total = self.calcular_total()
                self.cart_total_label.configure(text=f"Total: R$ {total:.2f}")
            except Exception:
                pass
        
        # Sincronizar cards existentes
        ids_atuais = set(self.carrinho_atual.keys())
        ids_em_cache = set(self.cart_item_cards.keys())
        
        # Remover cards que foram deletados
        for pid in ids_em_cache - ids_atuais:
            try:
                card = self.cart_item_cards[pid]
                frame = card.get("frame")
                if frame:
                    frame.destroy()
                del self.cart_item_cards[pid]
            except Exception:
                pass
        
        # Atualizar cards existentes
        for pid in ids_em_cache & ids_atuais:
            try:
                item = self.carrinho_atual[pid]
                qtd = item["quantidade"]
                preco_unit = item["produto"]["preco_unitario"]
                valor_total = qtd * preco_unit
                
                card = self.cart_item_cards[pid]
                
                # Atualizar entrada de quantidade
                qtd_entry = card.get("qtd_entry")
                if qtd_entry:
                    qtd_entry.delete(0, "end")
                    qtd_entry.insert(0, str(qtd))
                
                # Atualizar label de total
                total_label = card.get("total_label")
                if total_label:
                    total_label.configure(text=f"R$ {valor_total:.2f}")
            except Exception:
                pass
        
        # Adicionar novos cards (se houver produtos adicionados)
        for pid in ids_atuais - ids_em_cache:
            try:
                item = self.carrinho_atual[pid]
                self.criar_card_item_carrinho(self.cart_items_frame, pid, item)
            except Exception:
                pass
    
    def criar_card_item_carrinho(self, parent, produto_id: int, item: Dict):
        """Cria um card de item no carrinho"""
        produto = item["produto"]
        quantidade = item["quantidade"]
        
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.pack(fill="x", padx=10, pady=5)
        
        # Layout horizontal
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=10, pady=10)
        
        # Nome e preço unitário
        info = ctk.CTkFrame(content, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)
        
        nome = ctk.CTkLabel(info, text=produto["nome"],
                           font=("Arial", 14, "bold"),
                           anchor="w")
        nome.pack(anchor="w")
        
        preco_unit = ctk.CTkLabel(info, 
                                 text=f"R$ {produto['preco_unitario']:.2f} / unidade",
                                 font=("Arial", 11),
                                 text_color="gray",
                                 anchor="w")
        preco_unit.pack(anchor="w")
        
        # Controles de quantidade
        qtd_frame = ctk.CTkFrame(content, fg_color="transparent")
        qtd_frame.pack(side="right", padx=20)
        
        btn_menos = ctk.CTkButton(qtd_frame, text="-", width=40,
                                 command=lambda: self.alterar_quantidade(produto_id, -1))
        btn_menos.pack(side="left", padx=2)
        
        qtd_entry = ctk.CTkEntry(qtd_frame, width=60, justify="center")
        qtd_entry.insert(0, str(quantidade))
        qtd_entry.bind("<FocusOut>", 
                      lambda e, pid=produto_id, entry=qtd_entry: 
                      self.atualizar_quantidade_manual(pid, entry))
        qtd_entry.pack(side="left", padx=2)
        
        btn_mais = ctk.CTkButton(qtd_frame, text="+", width=40,
                                command=lambda: self.alterar_quantidade(produto_id, 1))
        btn_mais.pack(side="left", padx=2)
        
        # Valor total do item
        valor_total = quantidade * produto["preco_unitario"]
        total = ctk.CTkLabel(content, 
                            text=f"R$ {valor_total:.2f}",
                            font=("Arial", 16, "bold"),
                            text_color="#2ECC71")
        total.pack(side="right", padx=20)
        
        # Botão remover
        btn_remover = ctk.CTkButton(content, text="🗑️", width=40,
                                   fg_color="#E74C3C", hover_color="#C0392B",
                                   command=lambda: self.remover_do_carrinho(produto_id))
        btn_remover.pack(side="right", padx=5)
        
        # Salvar referências para atualização parcial
        try:
            self.cart_item_cards[produto_id] = {
                "frame": card,
                "qtd_entry": qtd_entry,
                "total_label": total
            }
        except Exception:
            pass
    
    def alterar_quantidade(self, produto_id: int, delta: int):
        """Altera a quantidade de um item no carrinho"""
        if produto_id in self.carrinho_atual:
            nova_qtd = self.carrinho_atual[produto_id]["quantidade"] + delta
            if nova_qtd <= 0:
                self.remover_do_carrinho(produto_id)
            else:
                self.carrinho_atual[produto_id]["quantidade"] = nova_qtd
                # Atualiza apenas os widgets que mudaram (sem recriar tela)
                self.atualizar_info_carrinho()
                self.sincronizar_tela_carrinho()
    
    def atualizar_quantidade_manual(self, produto_id: int, entry):
        """Atualiza quantidade quando editada manualmente"""
        try:
            nova_qtd = int(entry.get())
            if nova_qtd <= 0:
                self.remover_do_carrinho(produto_id)
            else:
                self.carrinho_atual[produto_id]["quantidade"] = nova_qtd
                self.atualizar_info_carrinho()
                self.sincronizar_tela_carrinho()
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida!")
            self.mostrar_tela_carrinho()
    
    def remover_do_carrinho(self, produto_id: int):
        """Remove um item do carrinho"""
        if produto_id in self.carrinho_atual:
            produto_nome = self.carrinho_atual[produto_id]["produto"]["nome"]
            del self.carrinho_atual[produto_id]
            # Mostra notificação não-bloqueante
            self.mostrar_notificacao(f"🗑️ {produto_nome} removido do carrinho")
            # Atualiza contador do carrinho rapidamente
            self.atualizar_info_carrinho()
            # Se houver card do produto na lista, atualize o botão para permitir adicionar novamente
            card = self.product_cards.get(produto_id)
            if card:
                try:
                    btn = card.get("btn_add")
                    btn.configure(text="🛒 Adicionar", fg_color="#3498DB", hover_color="#2980B9")
                except Exception:
                    pass
            # Sincroniza a tela do carrinho (remove card e atualiza total)
            self.sincronizar_tela_carrinho()
    
    def limpar_carrinho(self):
        """Limpa todo o carrinho"""
        if messagebox.askyesno("Confirmar", "Deseja limpar todo o carrinho?"):
            self.carrinho_atual.clear()
            # Atualiza contador e a tela
            self.atualizar_info_carrinho()
            self.mostrar_tela_carrinho()
    
    def calcular_total(self) -> float:
        """Calcula o valor total do carrinho"""
        total = 0.0
        for item in self.carrinho_atual.values():
            total += item["quantidade"] * item["produto"]["preco_unitario"]
        return total

    def atualizar_info_carrinho(self):
        """Atualiza elementos visuais relacionados ao carrinho (contador no header)."""
        try:
            if hasattr(self, 'btn_carrinho') and self.btn_carrinho:
                self.btn_carrinho.configure(text=f"🛒 Carrinho ({len(self.carrinho_atual)})")
        except Exception:
            # Segurança: não queremos que pequenas falhas de UI quebrem a lógica
            pass
    
    def compartilhar_carrinho(self):
        """Salva o carrinho e gera QR Code"""
        if not self.carrinho_atual:
            messagebox.showwarning("Aviso", "Carrinho vazio!")
            return
        
        # Prepara dados para salvar
        itens = []
        for produto_id, item in self.carrinho_atual.items():
            itens.append({
                "produto_id": produto_id,
                "quantidade": item["quantidade"],
                "preco_unitario": item["produto"]["preco_unitario"]
            })
        
        # Salva no banco
        codigo = self.db.salvar_carrinho(itens, "Meu Carrinho")
        
        # Mostra tela do QR Code
        self.mostrar_tela_qrcode(codigo)
    
    # ===== TELA 3: QR CODE =====
    
    def mostrar_tela_qrcode(self, codigo: str):
        """Tela de exibição do QR Code"""
        self.limpar_tela()
        
        # Header
        header = ctk.CTkFrame(self.main_container)
        header.pack(fill="x", padx=10, pady=10)
        
        btn_voltar = ctk.CTkButton(header, text="← Voltar ao Carrinho",
                                   command=self.mostrar_tela_carrinho,
                                   width=150)
        btn_voltar.pack(side="left", padx=10)
        
        titulo = ctk.CTkLabel(header, text="📤 Compartilhar Carrinho",
                             font=("Arial", 24, "bold"))
        titulo.pack(side="left", padx=20)
        
        # Conteúdo central
        content = ctk.CTkFrame(self.main_container)
        content.pack(expand=True, padx=20, pady=20)
        
        # Mensagem
        msg = ctk.CTkLabel(content,
                          text="✅ Carrinho salvo com sucesso!\n\nCompartilhe este código:",
                          font=("Arial", 16))
        msg.pack(pady=20)
        
        # Código
        codigo_frame = ctk.CTkFrame(content)
        codigo_frame.pack(pady=10)
        
        codigo_label = ctk.CTkLabel(codigo_frame, text=codigo,
                                    font=("Arial", 24, "bold"),
                                    text_color="#3498DB")
        codigo_label.pack(padx=20, pady=10)
        
        # Botão copiar
        btn_copiar = ctk.CTkButton(content, text="📋 Copiar Código",
                                   command=lambda: self.copiar_codigo(codigo),
                                   fg_color="#2ECC71", hover_color="#27AE60")
        btn_copiar.pack(pady=10)
        
        # QR Code
        qr_label = ctk.CTkLabel(content, text="")
        qr_label.pack(pady=20)
        
        # Gerar QR Code
        self.gerar_qrcode(codigo, qr_label)
        
        # Botão novo carrinho
        btn_novo = ctk.CTkButton(content, text="🛒 Novo Carrinho",
                                command=self.novo_carrinho,
                                fg_color="#9B59B6", hover_color="#8E44AD")
        btn_novo.pack(pady=10)
    
    def gerar_qrcode(self, codigo: str, label):
        """Gera e exibe o QR Code"""
        # Criar QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(codigo)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Redimensionar para caber na tela
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        
        # Converter para CTkImage
        photo = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 300))
        label.configure(image=photo)
        label.image = photo  # Manter referência
    
    def copiar_codigo(self, codigo: str):
        """Copia o código para a área de transferência"""
        pyperclip.copy(codigo)
        self.mostrar_notificacao("📋 Código copiado!", duracao_ms=1500)
    
    def novo_carrinho(self):
        """Limpa o carrinho e volta para a tela principal"""
        self.carrinho_atual.clear()
        # Atualiza contador e mostra tela principal
        self.atualizar_info_carrinho()
        self.mostrar_tela_principal()
    
    # ===== TELA 4: LER QR CODE =====
    
    def mostrar_tela_ler_qrcode(self):
        """Tela para ler QR Code"""
        self.limpar_tela()
        
        # Header
        header = ctk.CTkFrame(self.main_container)
        header.pack(fill="x", padx=10, pady=10)
        
        btn_voltar = ctk.CTkButton(header, text="← Voltar",
                                   command=self.mostrar_tela_principal,
                                   width=100)
        btn_voltar.pack(side="left", padx=10)
        
        titulo = ctk.CTkLabel(header, text="📷 Ler QR Code",
                             font=("Arial", 24, "bold"))
        titulo.pack(side="left", padx=20)
        
        # Conteúdo
        content = ctk.CTkFrame(self.main_container)
        content.pack(expand=True, padx=20, pady=20)
        
        # Opção 1: Digitar código
        ctk.CTkLabel(content, text="Digite o código do carrinho:",
                    font=("Arial", 16)).pack(pady=(20, 10))
        
        codigo_frame = ctk.CTkFrame(content, fg_color="transparent")
        codigo_frame.pack(pady=10)
        
        self.codigo_entry = ctk.CTkEntry(codigo_frame, width=300,
                                        placeholder_text="Ex: A1B2C3D4E5F6")
        self.codigo_entry.pack(side="left", padx=5)
        
        btn_carregar = ctk.CTkButton(codigo_frame, text="📥 Carregar",
                                     command=self.carregar_por_codigo,
                                     fg_color="#3498DB", hover_color="#2980B9")
        btn_carregar.pack(side="left", padx=5)
        
        # Separador
        ctk.CTkLabel(content, text="───────── OU ─────────",
                    font=("Arial", 12), text_color="gray").pack(pady=20)
        
        # Opção 2: Ler de imagem
        ctk.CTkLabel(content, text="Ler QR Code de uma imagem:",
                    font=("Arial", 16)).pack(pady=10)
        
        btn_imagem = ctk.CTkButton(content, text="📁 Abrir Imagem",
                                   command=self.ler_qrcode_imagem,
                                   fg_color="#2ECC71", hover_color="#27AE60")
        btn_imagem.pack(pady=10)
        
        # Opção 3: Ler da câmera
        ctk.CTkLabel(content, text="Ler QR Code da câmera:",
                    font=("Arial", 16)).pack(pady=10)
        
        btn_camera = ctk.CTkButton(content, text="📷 Usar Câmera",
                                   command=self.ler_qrcode_camera,
                                   fg_color="#9B59B6", hover_color="#8E44AD")
        btn_camera.pack(pady=10)
    
    def carregar_por_codigo(self):
        """Carrega um carrinho pelo código digitado"""
        codigo = self.codigo_entry.get().strip().upper()
        
        if not codigo:
            messagebox.showwarning("Aviso", "Digite um código!")
            return
        
        self.carregar_carrinho_compartilhado(codigo)
    
    def ler_qrcode_imagem(self):
        """Lê QR Code de uma imagem"""
        filepath = filedialog.askopenfilename(
            title="Selecione a imagem do QR Code",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp")]
        )
        
        if not filepath:
            return
        
        try:
            # Ler imagem
            img = cv2.imread(filepath)
            
            # Decodificar QR Code (importa pyzbar dinamicamente para tratar DLLs faltando)
            try:
                decode = ensure_pyzbar_decode()
            except RuntimeError as err:
                messagebox.showerror(
                    "Dependência ausente",
                    "Não foi possível carregar a biblioteca nativa para leitura de QR (zbar).\n\n"
                    "Soluções recomendadas:\n"
                    "- Se você usa conda/Anaconda: conda install -c conda-forge pyzbar zbar\n"
                    "- Caso use pip: pip install pipwin; pipwin install zbar\n"
                    "- Ou baixe os binários zbar/libiconv para Windows e coloque os .dll em um diretório do PATH ou em site-packages\\pyzbar\n\n"
                    "Erro: " + str(err)
                )
                return

            decoded = decode(img)
            
            if decoded:
                codigo = decoded[0].data.decode('utf-8')
                self.carregar_carrinho_compartilhado(codigo)
            else:
                messagebox.showerror("Erro", "Nenhum QR Code encontrado na imagem!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler imagem: {str(e)}")
    
    def ler_qrcode_camera(self):
        """Lê QR Code usando a câmera"""
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                messagebox.showerror("Erro", "Não foi possível acessar a câmera!")
                return
            
            messagebox.showinfo("Câmera", 
                              "Aponte a câmera para o QR Code.\nPressione ESC para cancelar.")
            
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                # Decodificar QR Code (importa pyzbar dinamicamente para tratar DLLs faltando)
                try:
                    decode = ensure_pyzbar_decode()
                except RuntimeError as err:
                    messagebox.showerror(
                        "Dependência ausente",
                        "Não foi possível carregar a biblioteca nativa para leitura de QR (zbar).\n\n"
                        "Soluções recomendadas:\n"
                        "- Se você usa conda/Anaconda: conda install -c conda-forge pyzbar zbar\n"
                        "- Caso use pip: pip install pipwin; pipwin install zbar\n"
                        "- Ou baixe os binários zbar/libiconv para Windows e coloque os .dll em um diretório do PATH ou em site-packages\\pyzbar\n\n"
                        "Erro: " + str(err)
                    )
                    cap.release()
                    cv2.destroyAllWindows()
                    return

                decoded = decode(frame)
                
                # Desenhar retângulo ao redor do QR Code
                for qr in decoded:
                    points = qr.polygon
                    if len(points) == 4:
                        pts = np.array(points, np.int32)
                        pts = pts.reshape((-1, 1, 2))
                        cv2.polylines(frame, [pts], True, (0, 255, 0), 3)
                    
                    # QR Code detectado
                    codigo = qr.data.decode('utf-8')
                    cap.release()
                    cv2.destroyAllWindows()
                    self.carregar_carrinho_compartilhado(codigo)
                    return
                
                # Mostrar frame
                cv2.imshow('Leia o QR Code - Pressione ESC para sair', frame)
                
                # ESC para sair
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao acessar câmera: {str(e)}")
    
    def carregar_carrinho_compartilhado(self, codigo: str):
        """Carrega um carrinho compartilhado"""
        carrinho = self.db.carregar_carrinho(codigo)
        
        if not carrinho:
            messagebox.showerror("Erro", 
                               f"Carrinho não encontrado!\nCódigo: {codigo}")
            return
        
        # Limpar carrinho atual
        self.carrinho_atual.clear()
        
        # Adicionar itens do carrinho compartilhado
        for item in carrinho["itens"]:
            produto = self.db.get_produto_by_id(item["produto_id"])
            if produto:
                self.carrinho_atual[produto["id"]] = {
                    "produto": produto,
                    "quantidade": item["quantidade"]
                }
        
        # Mostra notificação não-bloqueante
        self.mostrar_notificacao(f"✅ Carrinho carregado com {len(carrinho['itens'])} itens!", duracao_ms=2000)
        # Atualiza contador e mostra o carrinho carregado
        self.atualizar_info_carrinho()
        self.mostrar_tela_carrinho()


def main():
    """Função principal"""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = ShareProductsApp()
    app.mainloop()


if __name__ == "__main__":
    main()
