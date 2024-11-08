import subprocess
import os
import sys
import torch
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def transcribe(input_file, model='large-v3'):
    print(f"Iniciando transcrição de {input_file}...")
    start_time = time.time()  # Tempo de início da transcrição
    
    output_folder = 'tmp'
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    srt_file = os.path.join(output_folder, f"{base_name}.srt")
    tsv_file = os.path.join(output_folder, f"{base_name}.tsv")  # Assuming you want to capture the TSV file too

    # Verifica se o arquivo SRT já existe
    if os.path.exists(srt_file):
        print(f"O arquivo {srt_file} já existe. Pulando a transcrição.")
        return srt_file  # Adjusted return statement
    
    if os.path.exists(tsv_file):
        print(f"O arquivo {tsv_file} já existe. Pulando a transcrição.")
        return tsv_file  # Adjusted return statement

    # Verifica se há uma GPU disponível e define o tipo de processamento
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"{'GPU detected, using CUDA.' if device == 'cuda' else 'No GPU detected, using CPU.'}")


    command = [
        "whisperx",
        input_file,
        "--model", model,
        "--task", "transcribe",
        "--align_model", "WAV2VEC2_ASR_LARGE_LV60K_960H",
        "--interpolate_method", "linear",
        "--chunk_size", "10",
        "--verbose", "True",
        "--vad_onset", "0.4",
        "--vad_offset", "0.3",
        "--no_align",
        "--segment_resolution", "sentence",
        "--compute_type", "float32",
        "--batch_size", "10",
        "--output_dir", output_folder,
        "--output_format", "all",
        "--device", device
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        end_time = time.time()  # Tempo de término da transcrição
        elapsed_time = end_time - start_time  # Tempo total de execução

        # Cálculo de minutos e segundos
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        print(f"Transcrição concluída. Saída salva em {srt_file}.")
        print(f"Levou {minutes} minutos e {seconds} segundos para transcrever usando {device}.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Erro durante a transcrição: {e}")
        print(f"Saída de erro: {e.stderr}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

    # Verifica se os arquivos SRT e TSV foram criados
    if os.path.exists(srt_file):
        print(f"Arquivo SRT {srt_file} criado com sucesso.")
    if os.path.exists(tsv_file):
        print(f"Arquivo TSV {tsv_file} criado com sucesso.")

    return srt_file, tsv_file  # Ensure both files are returned
