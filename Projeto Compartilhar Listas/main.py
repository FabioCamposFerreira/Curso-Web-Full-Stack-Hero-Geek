import customtkinter as ctk
from tkinter import messagebox, filedialog

import qrcode
import pyperclip
import cv2
from PIL import ImageTk

from database import (
    init_db,
    get_produtos,
    get_produto,
    salvar_carrinho,
    carregar_carrinho,
)

carrinho = {}
tela_atual = root = btn_carrinho = label_total = None
itens_carrinho = {}

def limpar_tela():
    global tela_atual, btn_carrinho, label_total, itens_carrinho
    if tela_atual:
        tela_atual.destroy()
    tela_atual = btn_carrinho = label_total = None
    itens_carrinho = {}

def mostrar_notificacao(msg):
    label = ctk.CTkLabel(
        root,
        text=msg,
        font=("Arial", 10),
        text_color="white",
        fg_color="#2ECC71",
        corner_radius=5,
    )
    label.place(relx=0.5, y=10, anchor="n")
    root.after(2000, lambda: label.winfo_exists() and label.destroy())

def atualizar_tela():
    def total_carrinho():
        total = 0
        for item in carrinho.values():
            total += item["qtd"] * item["produto"]["preco"]
        return total

    def atualizar_botao_carrinho():
        if btn_carrinho and btn_carrinho.winfo_exists():
            btn_carrinho.configure(text=f"🛒 Carrinho ({len(carrinho)})")

    def atualizar_total_carrinho():
        if label_total and label_total.winfo_exists():
            label_total.configure(text=f"Total: R$ {total_carrinho():.2f}")

    def atualizar_item_carrinho(pid):
        if pid in carrinho and pid in itens_carrinho:
            item = carrinho[pid]
            itens_carrinho[pid][1].configure(text=str(item["qtd"]))
            itens_carrinho[pid][2].configure(
                text=f"Total: R$ {item['qtd'] * item['produto']['preco']:.2f}"
            )
        atualizar_total_carrinho()
        atualizar_botao_carrinho()

    def tela_produtos():
        global tela_atual, btn_carrinho
        limpar_tela()
        tela_atual = ctk.CTkFrame(root)
        tela_atual.pack(fill="both", expand=True, padx=10, pady=10)

        header = ctk.CTkFrame(tela_atual)
        header.pack(fill="x", pady=10)
        ctk.CTkLabel(
            header, text="📦 Share Products", font=("Arial", 24, "bold")
        ).pack(side="left")
        btn_carrinho = ctk.CTkButton(
            header,
            text=f"🛒 Carrinho ({len(carrinho)})",
            command=tela_carrinho,
            fg_color="#2ECC71",
        )
        btn_carrinho.pack(side="right", padx=5)
        ctk.CTkButton(
            header, text="📷 Ler QR", command=tela_qr_reader, fg_color="#9B59B6"
        ).pack(side="right", padx=5)

        filtro_var = ctk.StringVar()
        ctk.CTkEntry(
            tela_atual, textvariable=filtro_var, placeholder_text="🔍 Filtrar..."
        ).pack(fill="x", pady=5)
        frame_produtos = ctk.CTkScrollableFrame(tela_atual)
        frame_produtos.pack(fill="both", expand=True)

        def atualizar_produtos(*args):
            for w in frame_produtos.winfo_children():
                w.destroy()
            for produto in get_produtos(filtro_var.get()):
                card = ctk.CTkFrame(frame_produtos, corner_radius=10)
                card.pack(fill="x", padx=5, pady=5)
                ctk.CTkLabel(
                    card,
                    text=f"{produto['nome']} - R$ {produto['preco']:.2f}",
                    font=("Arial", 12),
                ).pack(side="left", padx=10, pady=8)
                ctk.CTkButton(
                    card,
                    text="🛒 Adicionar",
                    width=100,
                    command=lambda p=produto: adicionar(p),
                ).pack(side="right", padx=5, pady=5)

        filtro_var.trace_add("write", atualizar_produtos)
        atualizar_produtos()

    def tela_carrinho():
        global tela_atual, label_total, itens_carrinho
        limpar_tela()
        tela_atual = ctk.CTkFrame(root)
        tela_atual.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkButton(tela_atual, text="← Voltar", command=tela_produtos).pack(
            pady=10
        )
        ctk.CTkLabel(
            tela_atual, text="🛒 Meu Carrinho", font=("Arial", 20, "bold")
        ).pack()
        if not carrinho:
            ctk.CTkLabel(
                tela_atual, text="Carrinho vazio :(", font=("Arial", 14)
            ).pack(pady=50)
            return

        scroll = ctk.CTkScrollableFrame(tela_atual)
        scroll.pack(fill="both", expand=True, pady=10)
        for pid, item in carrinho.items():
            p = item["produto"]
            card = ctk.CTkFrame(scroll, corner_radius=10)
            card.pack(fill="x", padx=5, pady=5)
            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(fill="x", padx=10, pady=8)
            ctk.CTkLabel(
                info, text=f"{p['nome']} - R$ {p['preco']:.2f}", font=("Arial", 12)
            ).pack(anchor="w")
            ctrl = ctk.CTkFrame(info, fg_color="transparent")
            ctrl.pack(fill="x", pady=5)
            ctk.CTkButton(
                ctrl,
                text="-",
                width=30,
                command=lambda pid=pid: alterar_qtd(pid, -1),
            ).pack(side="left", padx=2)
            qtd = ctk.CTkLabel(ctrl, text=str(item["qtd"]), font=("Arial", 12))
            qtd.pack(side="left", padx=10)
            ctk.CTkButton(
                ctrl,
                text="+",
                width=30,
                command=lambda pid=pid: alterar_qtd(pid, 1),
            ).pack(side="left", padx=2)
            total_item = ctk.CTkLabel(
                ctrl,
                text=f"Total: R$ {item['qtd'] * p['preco']:.2f}",
                font=("Arial", 12, "bold"),
                text_color="#2ECC71",
            )
            total_item.pack(side="right")
            ctk.CTkButton(
                ctrl,
                text="🗑️",
                width=30,
                fg_color="#E74C3C",
                command=lambda pid=pid: remover(pid),
            ).pack(side="right", padx=5)
            itens_carrinho[pid] = card, qtd, total_item

        label_total = ctk.CTkLabel(
            tela_atual,
            text=f"Total: R$ {total_carrinho():.2f}",
            font=("Arial", 16, "bold"),
            text_color="#2ECC71",
        )
        label_total.pack(pady=10)
        footer = ctk.CTkFrame(tela_atual)
        footer.pack(fill="x", pady=10)
        ctk.CTkButton(
            footer,
            text="🗑️ Limpar",
            command=limpar_carrinho,
            fg_color="#E74C3C",
        ).pack(side="right", padx=5)
        ctk.CTkButton(
            footer, text="📤 Compartilhar", command=tela_qr, fg_color="#9B59B6"
        ).pack(side="right", padx=5)

    def tela_qr():
        global tela_atual
        limpar_tela()
        tela_atual = ctk.CTkFrame(root)
        tela_atual.pack(fill="both", expand=True, padx=20, pady=20)
        ctk.CTkButton(tela_atual, text="← Voltar", command=tela_carrinho).pack(
            pady=10
        )
        ctk.CTkLabel(
            tela_atual, text="📤 Compartilhar", font=("Arial", 20, "bold")
        ).pack(pady=20)
        ctk.CTkLabel(tela_atual, text="✅ Carrinho salvo!", font=("Arial", 14)).pack()

        itens = []
        for pid, item in carrinho.items():
            itens.append(
                {
                    "id": pid,
                    "qty": item["qtd"],
                    "preco": item["produto"]["preco"],
                }
            )
        codigo = salvar_carrinho(itens)
        ctk.CTkLabel(
            tela_atual, text=codigo, font=("Arial", 16, "bold"), text_color="#3498DB"
        ).pack(pady=20)

        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(codigo)
        qr.make(fit=True)
        photo = ImageTk.PhotoImage(
            qr.make_image(fill_color="black", back_color="white").resize((250, 250))
        )
        qr_label = ctk.CTkLabel(tela_atual, text="", image=photo)
        qr_label.image = photo
        qr_label.pack(pady=20)

        ctk.CTkButton(
            tela_atual,
            text="📋 Copiar",
            command=lambda: (
                pyperclip.copy(codigo),
                mostrar_notificacao("Copiado!"),
            ),
        ).pack(pady=5)
        ctk.CTkButton(
            tela_atual,
            text="🛒 Novo Carrinho",
            command=lambda: (carrinho.clear(), tela_produtos()),
            fg_color="#2ECC71",
        ).pack(pady=5)

    def tela_qr_reader():
        global tela_atual
        limpar_tela()
        tela_atual = ctk.CTkFrame(root)
        tela_atual.pack(fill="both", expand=True, padx=20, pady=20)
        ctk.CTkButton(tela_atual, text="← Voltar", command=tela_produtos).pack(
            pady=10
        )
        ctk.CTkLabel(
            tela_atual, text="📷 Ler QR Code", font=("Arial", 20, "bold")
        ).pack(pady=20)
        ctk.CTkLabel(tela_atual, text="Digite o código:", font=("Arial", 14)).pack()
        codigo_input = ctk.CTkEntry(tela_atual, width=250)
        codigo_input.pack(pady=10)
        ctk.CTkButton(
            tela_atual,
            text="📥 Carregar",
            command=lambda: carregar_qr(codigo_input.get()),
        ).pack(pady=5)
        ctk.CTkLabel(tela_atual, text="─── OU ───", text_color="gray").pack(pady=20)
        ctk.CTkButton(
            tela_atual, text="📁 Abrir Imagem", command=ler_imagem, fg_color="#2ECC71"
        ).pack(pady=5)
        ctk.CTkButton(
            tela_atual, text="📷 Usar Câmera", command=ler_camera, fg_color="#9B59B6"
        ).pack(pady=5)

    def adicionar(p):
        if p["id"] in carrinho:
            carrinho[p["id"]]["qtd"] += 1
        else:
            carrinho[p["id"]] = {"produto": p, "qtd": 1}
        mostrar_notificacao(f"✅ {p['nome']} adicionado!")
        atualizar_botao_carrinho()

    def alterar_qtd(pid, delta):
        if pid in carrinho:
            carrinho[pid]["qtd"] += delta
            if carrinho[pid]["qtd"] <= 0:
                remover(pid)
            else:
                atualizar_item_carrinho(pid)

    def remover(pid):
        if pid in carrinho:
            del carrinho[pid]
            mostrar_notificacao("🗑️ Removido!")
            atualizar_botao_carrinho()
            if pid in itens_carrinho:
                itens_carrinho[pid][0].destroy()
                del itens_carrinho[pid]
                if carrinho:
                    atualizar_total_carrinho()
                else:
                    tela_carrinho()

    def limpar_carrinho():
        if messagebox.askyesno("Confirmar", "Limpar carrinho?"):
            carrinho.clear()
            atualizar_botao_carrinho()
            tela_carrinho()

    def carregar_qr(codigo):
        c = carregar_carrinho(codigo.strip().upper())
        if not c:
            messagebox.showerror("Erro", "Carrinho não encontrado!")
            return
        carrinho.clear()
        for item in c["itens"]:
            p = get_produto(item["id"])
            if p:
                carrinho[p["id"]] = {"produto": p, "qtd": item["qty"]}
        mostrar_notificacao("✅ Carrinho carregado!")
        tela_carrinho()

    def ler_imagem():
        f = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg")])
        if f:
            try:
                from pyzbar.pyzbar import decode

                d = decode(cv2.imread(f))
                if d:
                    carregar_qr(d[0].data.decode())
                else:
                    messagebox.showerror("Erro", "QR Code não encontrado!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    def ler_camera():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Erro", "Câmera não disponível!")
            return
        messagebox.showinfo("Câmera", "ESC para cancelar")
        try:
            from pyzbar.pyzbar import decode

            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                d = decode(frame)
                if d:
                    cap.release()
                    cv2.destroyAllWindows()
                    carregar_qr(d[0].data.decode())
                    return
                cv2.imshow("Câmera - ESC para sair", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            cap.release()
            cv2.destroyAllWindows()

    tela_produtos()


def main():
    global root
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Share Products")
    root.geometry("800x600")
    init_db()
    atualizar_tela()
    root.mainloop()


if __name__ == "__main__":
    main()
