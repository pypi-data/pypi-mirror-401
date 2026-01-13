# prompt_personagem_ia
Projeto que gera uma ficha simples de composição de personagem

[![Made with Python](https://img.shields.io/badge/Python->=3.10-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")
![license - MIT](https://img.shields.io/badge/license-MIT-green)
![site - prazocerto.me](https://img.shields.io/badge/site-prazocerto.me-230023)
![linkedin - @marioluciofjr](https://img.shields.io/badge/linkedin-marioluciofjr-blue)

## Índice

* [Introdução](#introdução)
* [Estrutura do projeto](#estrutura-do-projeto)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Requisitos](#requisitos)
* [Links úteis](#links-úteis)
* [Contribuições](#contribuições)
* [Licença](#licença)
* [Contato](#contato)

## Introdução

Este projeto é uma ferramenta em Python desenvolvida para gerar automaticamente prompts detalhados de personagens para inteligência artificial. Utilizando listas pré-definidas de atributos, o script cria descrições únicas combinando gênero, idade, tom de pele, penteado e poses variadas. Ideal para artistas e criadores que buscam inspiração rápida ou necessitam de referências visuais diversificadas para seus projetos, garantindo consistência e criatividade na geração de imagens com especificações técnicas definidas, tais como ângulo de câmera e proporção.

## Estrutura do projeto

Para entender como tudo funciona, imagine que este projeto é um assistente criativo dividido em duas partes principais:

*   **`listas.py`**: Pense neste arquivo como um grande catálogo ou despensa. É aqui que guardamos todas as opções disponíveis para criar um personagem, como tipos de cabelo, tons de pele, roupas e poses. Ele não toma decisões, apenas armazena as informações que serão usadas.

*   **`prompt.py`**: Este é o "cérebro" da operação. Ele consulta o arquivo `listas.py`, sorteia aleatoriamente um item de cada categoria e organiza tudo em um texto coerente. É ele quem monta a "ficha" final do personagem que você receberá.

### Como usar no Google Colab

Como o projeto está publicado no PyPI você só precisa seguir este passo a passo: 

1 - Instale o projeto
```python
!pip install -qU prompt-personagem-ia
```

2 - Importe o pacote necessário
```python
from prompt import gerar_prompt

gerar_prompt()
```

> [!IMPORTANT]
> Want to better understand this repository, but you don't speak Portuguese? Check out this complete tutorial: [`Codebase - prompt_personagem_ia`](https://code2tutorial.com/tutorial/9ebd63ce-6ac7-4b2e-883f-92e74953efde/index.md)

## Tecnologias utilizadas

<div>
  <img align="center" height="60" width="80" src="https://github.com/user-attachments/assets/76e7aca0-5321-4238-9742-164c20af5b4a" />&nbsp;&nbsp;&nbsp
  <img align="center" height="60" width="80" src="https://camo.githubusercontent.com/13caad70455ed743a53c3624ce9e033554f2aabc28a46c14f43e05214f963a92/68747470733a2f2f692e6e616d752e77696b692f692f6b415278316e5039474861546b74785f347954493448584c4f6a6d64334a5a614b4a6b48545867453262763455415457586b566c766f45366b74464f344d464936794d6356353078367a2d7069734f4544424f554f512e77656270" />&nbsp;&nbsp;&nbsp
 </div><br>

* Python;
* Antigravity.

## Requisitos

Antes de começar, certifique-se de ter instalado:
*   [Python 3.10](https://www.python.org/downloads/) ou superior.
*   [UV](https://github.com/astral-sh/uv) (Recomendado) ou PIP.

## Links úteis

* [Como instalar o VSCode](https://code.visualstudio.com/download)- Link direto para download
* [Documentação oficial do pacote uv](https://docs.astral.sh/uv/) - Você saberá todos os detalhes sobre o `uv` e como ele é importante no python
* [venv — Criação de ambientes virtuais](https://docs.python.org/pt-br/3/library/venv.html) - Explicação completa de como funcionam os venvs
* [Conjunto de ícones de modelos de IA/LLM](https://lobehub.com/pt-BR/icons) - site muito bom para conseguir ícones do ecossistema de IA
* [Devicon](https://devicon.dev/) - site bem completo também com ícones gerais sobre tecnologia
* [Smolagents](https://github.com/huggingface/smolagents) - documenttação oficial da biblioteca smolagents
* [Como baixar o Antigravity](https://antigravity.google/download) - Página oficial de download da IDE do Google DeepMind
* [All Poses Reference](https://posemy.art/all-poses-reference/) - Site com vários mockups de poses diferentes

## Contribuições

Contribuições são bem-vindas! Se você tem ideias para melhorar este projeto, sinta-se à vontade para fazer um fork do repositório.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](https://github.com/marioluciofjr/prompt_personagem_ia/blob/main/LICENSE) para detalhes.

## Contato
    
Mário Lúcio - Prazo Certo®
<div>  	
  <a href="https://www.linkedin.com/in/marioluciofjr" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a> 
  <a href = "mailto:marioluciofjr@gmail.com" target="_blank"><img src="https://img.shields.io/badge/-Gmail-%23333?style=for-the-badge&logo=gmail&logoColor=white"></a>
  <a href="https://prazocerto.me/contato" target="_blank"><img src="https://img.shields.io/badge/prazocerto.me/contato-230023?style=for-the-badge&logo=wordpress&logoColor=white"></a>
</div> 


