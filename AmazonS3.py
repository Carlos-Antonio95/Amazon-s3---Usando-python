#bibliotecas

import boto3
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Criação do cliente S3 e chaves para acessar o bucket
usuario = boto3.client('s3',
    aws_access_key_id='*****',
    aws_secret_access_key='*******',
    region_name='sa-east-1'
)

#Nome do bucket
nome_do_bucket = 'ads-banco-de-dados'

# Função para listar arquivos no bucket
def listar_arquivos_bucket():
    try:
        obj_buckets = usuario.list_objects_v2(Bucket=nome_do_bucket)
        lista_nomes = [obj['Key'] for obj in obj_buckets.get('Contents', [])]
        return lista_nomes #retonra a lista com os nomes
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar arquivos no bucket:\n{e}")
        return []


# Função de download
def fazer_download():
    arquivos = listar_arquivos_bucket()
    if not arquivos:
        return

    # Exibir uma janela para o usuário escolher

    escolha = simpledialog.askstring("Download", f"Arquivos disponíveis:\n\n" + "\n".join(
        arquivos) + "\n\nDigite o nome do arquivo:")

    if escolha and escolha in arquivos:
        try:
            usuario.download_file(nome_do_bucket, escolha, escolha)
            messagebox.showinfo("Sucesso", f'Download feito com sucesso: {escolha}')
        except Exception as e:
            messagebox.showerror("Erro", f'Erro ao fazer download:\n{e}')
    else:
        messagebox.showwarning("Atenção", "Arquivo não encontrado ou não informado.")

# Função de upload
def fazer_upload():
    caminho_arquivo = filedialog.askopenfilename(title="Escolha um arquivo para upload")
    if caminho_arquivo:
        nome_arquivo_s3 = simpledialog.askstring("Upload", "Nome do arquivo no S3:")
        if not nome_arquivo_s3:
            messagebox.showwarning("Atenção", "Arquivo não enviado, deve por nome do arquivo no S3")
            return
        if nome_arquivo_s3:
            try:
                usuario.upload_file(caminho_arquivo, nome_do_bucket , nome_arquivo_s3)
                messagebox.showinfo("Sucesso", f'Upload feito com sucesso: {nome_arquivo_s3}')
            except Exception as e:
                messagebox.showerror("Erro", f'Erro ao fazer upload:\n{e}')

# Interface Gráfica
janela = tk.Tk()
janela.title("AWS S3 - Upload e Download")
janela.geometry("750x750")

btn_download = tk.Button(janela, text="Fazer Download", command=fazer_download, width=30)
btn_download.pack(pady=20)

btn_upload = tk.Button(janela, text="Fazer Upload", command=fazer_upload, width=30)
btn_upload.pack(pady=20)

janela.mainloop()
