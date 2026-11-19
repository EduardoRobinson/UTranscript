"""Gera a apresentação de defesa do UTranscript a partir das figuras do TCC."""

import struct
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls, qn
from pptx.util import Emu, Inches, Pt

RAIZ = Path(__file__).resolve().parent
FIG = RAIZ / "figuras"
SAIDA = RAIZ / "Defesa-UTranscript.pptx"

AMARELO = RGBColor(0xF5, 0xC4, 0x00)
PRETO = RGBColor(0x14, 0x14, 0x14)
TINTA = RGBColor(0x1A, 0x1A, 0x1A)
CINZA = RGBColor(0x3E, 0x48, 0x52)
LINHA = RGBColor(0xE6, 0xE1, 0xD4)
CREME = RGBColor(0xF7, 0xF4, 0xEA)
BRANCO = RGBColor(0xFF, 0xFF, 0xFF)
CARTAO = RGBColor(0xFF, 0xFB, 0xF2)

LARGURA = 13.333
ALTURA = 7.5
FONTE = "Calibri"


def png_size(path):
    with open(path, "rb") as arquivo:
        arquivo.read(16)
        largura, altura = struct.unpack(">II", arquivo.read(8))
    return largura, altura


def sem_sombra(forma):
    efeito = forma._element.spPr.find(qn("a:effectLst"))
    if efeito is not None:
        forma._element.spPr.remove(efeito)
    forma.shadow.inherit = False


def retangulo(slide, esquerda, topo, largura, altura, preenchimento, linha=None):
    forma = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(esquerda),
        Inches(topo),
        Inches(largura),
        Inches(altura),
    )
    forma.fill.solid()
    forma.fill.fore_color.rgb = preenchimento
    if linha is None:
        forma.line.fill.background()
    else:
        forma.line.color.rgb = linha
        forma.line.width = Pt(1)
    sem_sombra(forma)
    return forma


def caixa(slide, esquerda, topo, largura, altura, ancora=MSO_ANCHOR.TOP):
    forma = slide.shapes.add_textbox(
        Inches(esquerda), Inches(topo), Inches(largura), Inches(altura)
    )
    quadro = forma.text_frame
    quadro.word_wrap = True
    quadro.auto_size = None
    quadro.margin_left = Emu(0)
    quadro.margin_right = Emu(0)
    quadro.margin_top = Emu(0)
    quadro.margin_bottom = Emu(0)
    forma.text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT
    try:
        quadro._txBody.bodyPr.set("anchor", {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}[ancora])
    except Exception:
        pass
    return quadro


def aplicar(trecho, tamanho, negrito, cor):
    trecho.font.name = FONTE
    trecho.font.size = Pt(tamanho)
    trecho.font.bold = negrito
    trecho.font.color.rgb = cor


def preencher(paragrafo, conteudo, tamanho, negrito, cor):
    partes = conteudo.split("\n")
    for indice, parte in enumerate(partes):
        trecho = paragrafo.add_run()
        trecho.text = parte if parte else " "
        aplicar(trecho, tamanho, negrito, cor)
        if indice < len(partes) - 1:
            trecho._r.append(parse_xml(f'<a:br {nsdecls("a")}/>'))


def escrever(quadro, conteudo, tamanho, negrito=False, cor=TINTA, alinhamento=PP_ALIGN.LEFT, espaco_depois=0, espaco_antes=0):
    paragrafo = quadro.paragraphs[0]
    paragrafo.clear()
    paragrafo.alignment = alinhamento
    paragrafo.space_after = Pt(espaco_depois)
    paragrafo.space_before = Pt(espaco_antes)
    preencher(paragrafo, conteudo, tamanho, negrito, cor)
    return paragrafo


def adicionar(quadro, conteudo, tamanho, negrito=False, cor=TINTA, alinhamento=PP_ALIGN.LEFT, espaco_depois=0, espaco_antes=0):
    paragrafo = quadro.add_paragraph()
    paragrafo.alignment = alinhamento
    paragrafo.space_after = Pt(espaco_depois)
    paragrafo.space_before = Pt(espaco_antes)
    preencher(paragrafo, conteudo, tamanho, negrito, cor)
    return paragrafo


def texto(slide, esquerda, topo, largura, altura, conteudo, tamanho=18, negrito=False, cor=TINTA, alinhamento=PP_ALIGN.LEFT, ancora=MSO_ANCHOR.TOP):
    quadro = caixa(slide, esquerda, topo, largura, altura, ancora)
    escrever(quadro, conteudo, tamanho, negrito, cor, alinhamento)
    return quadro


def itens(slide, esquerda, topo, largura, altura, linhas, tamanho=20, cor=TINTA, espaco=10):
    quadro = caixa(slide, esquerda, topo, largura, altura)
    for indice, linha in enumerate(linhas):
        if indice == 0:
            escrever(quadro, linha, tamanho, False, cor, espaco_depois=espaco)
        else:
            adicionar(quadro, linha, tamanho, False, cor, espaco_depois=espaco)
    return quadro


def imagem(slide, nome, esquerda, topo, largura_max, altura_max, moldura=True):
    caminho = FIG / nome
    pixels_l, pixels_a = png_size(caminho)
    proporcao = pixels_l / pixels_a
    if largura_max / altura_max > proporcao:
        altura = altura_max
        largura = altura_max * proporcao
    else:
        largura = largura_max
        altura = largura_max / proporcao
    x = esquerda + (largura_max - largura) / 2
    y = topo + (altura_max - altura) / 2
    if moldura:
        retangulo(slide, x - 0.04, y - 0.04, largura + 0.08, altura + 0.08, BRANCO, LINHA)
    slide.shapes.add_picture(str(caminho), Inches(x), Inches(y), Inches(largura), Inches(altura))
    return x, y, largura, altura


def notas(slide, fala):
    slide.notes_slide.notes_text_frame.text = fala.strip()


class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(LARGURA)
        self.prs.slide_height = Inches(ALTURA)
        self.prs.core_properties.title = "UTranscript: plataforma para transcrição e resumo de videoaulas"
        self.prs.core_properties.author = "Eduardo Robinson Silveira Junior"
        self.prs.core_properties.subject = "Defesa de TCC — UTFPR, Ponta Grossa, 2026"
        self.slides = []
        self.layout = self.prs.slide_layouts[6]

    def novo(self):
        slide = self.prs.slides.add_slide(self.layout)
        self.slides.append(slide)
        return slide

    def fechar(self, secao):
        total = len(self.slides)
        for numero, slide in enumerate(self.slides, start=1):
            if numero == 1:
                continue
            retangulo(slide, 0, 7.22, LARGURA, 0.28, PRETO)
            texto(slide, 0.48, 7.24, 8.5, 0.24, secao[numero], 11, False, AMARELO, ancora=MSO_ANCHOR.MIDDLE)
            texto(
                slide, 10.3, 7.24, 2.55, 0.24,
                f"{numero}  /  {total}",
                11, False, BRANCO, PP_ALIGN.RIGHT, MSO_ANCHOR.MIDDLE,
            )

    def salvar(self):
        self.prs.save(str(SAIDA))


def cabecalho(slide, secao, titulo):
    retangulo(slide, 0, 0, LARGURA, 0.08, AMARELO)
    texto(slide, 0.48, 0.2, 12, 0.28, secao.upper(), 12, True, RGBColor(0x8A, 0x6A, 0x00))
    texto(slide, 0.48, 0.46, 12.3, 0.55, titulo, 28, True, PRETO)


def capa(deck):
    slide = deck.novo()
    retangulo(slide, 0, 0, 4.55, ALTURA, PRETO)
    retangulo(slide, 4.55, 0, 0.12, ALTURA, AMARELO)
    texto(slide, 0.42, 0.48, 3.7, 0.9, "UTFPR", 20, True, AMARELO)
    texto(slide, 0.42, 1.15, 3.7, 1.3, "Universidade\nTecnológica\nFederal do Paraná", 18, False, BRANCO)
    texto(slide, 0.42, 6.35, 3.7, 0.3, "Ponta Grossa", 16, False, BRANCO)
    texto(slide, 0.42, 6.7, 3.7, 0.3, "2026", 16, True, AMARELO)

    texto(slide, 5.15, 1.15, 7.6, 0.35, "TRABALHO DE CONCLUSÃO DE CURSO", 14, True, RGBColor(0x8A, 0x6A, 0x00))
    texto(slide, 5.15, 1.6, 7.6, 1.15, "UTranscript", 48, True, PRETO)
    texto(
        slide, 5.15, 2.85, 7.5, 1.0,
        "Plataforma para transcrição e resumo de videoaulas",
        24, False, TINTA,
    )
    retangulo(slide, 5.15, 4.15, 2.1, 0.07, AMARELO)
    texto(slide, 5.15, 4.45, 7.5, 0.4, "Eduardo Robinson Silveira Junior", 20, True, PRETO)
    texto(slide, 5.15, 5.05, 7.5, 0.32, "Orientador: Prof. Dr. Vinícius Camargo Andrade", 16, False, CINZA)
    texto(slide, 5.15, 5.4, 7.5, 0.32, "Coorientador: Prof. Dr. Richard Duarte Ribeiro", 16, False, CINZA)
    texto(slide, 5.15, 6.15, 7.5, 0.55, "Bacharelado em Ciência da Computação", 16, False, CINZA)
    notas(
        slide,
        "Bom dia. Eu sou o Eduardo Robinson Silveira Junior. Apresento o UTranscript, "
        "plataforma para transcrição e resumo de videoaulas, orientado pelo professor "
        "Vinícius Camargo Andrade e coorientado pelo professor Richard Duarte Ribeiro. "
        "A apresentação segue o trabalho escrito e dura cerca de 25 minutos. "
        "No fim, fico à disposição da banca.",
    )


def agenda(deck):
    slide = deck.novo()
    cabecalho(slide, "Abertura", "Agenda")
    blocos = [
        ("01", "Contexto", "Videoaula, ferramentas existentes e a lacuna"),
        ("02", "Problema e questão", "O que o trabalho se propõe a responder"),
        ("03", "Objetivos", "Geral e quatro objetivos específicos"),
        ("04", "Conceitos", "Modelos, critérios e a forma da arquitetura"),
        ("05", "Método", "Do levantamento à avaliação"),
        ("06", "Desenvolvimento", "Arquitetura, fluxo, ficha e modelos"),
        ("07", "Resultados", "O que a plataforma faz, nas telas"),
        ("08", "Avaliação", "Qualidade dos resumos e o ensaio de tempo"),
        ("09", "Conclusão", "O que foi alcançado, limites e continuidade"),
    ]
    for indice, (numero, titulo, detalhe) in enumerate(blocos):
        coluna = 0 if indice < 5 else 1
        linha = indice if indice < 5 else indice - 5
        x = 0.5 + coluna * 6.4
        y = 1.3 + linha * 1.1
        retangulo(slide, x, y, 6.05, 0.95, CREME)
        retangulo(slide, x, y, 0.08, 0.95, AMARELO)
        texto(slide, x + 0.28, y + 0.12, 1.0, 0.7, numero, 22, True, RGBColor(0x8A, 0x6A, 0x00), ancora=MSO_ANCHOR.MIDDLE)
        texto(slide, x + 1.25, y + 0.14, 4.5, 0.38, titulo, 18, True, PRETO)
        texto(slide, x + 1.25, y + 0.5, 4.5, 0.32, detalhe, 13, False, CINZA)
    notas(
        slide,
        "O caminho é o do texto. Começo pelo contexto e pela lacuna, passo pelos objetivos "
        "e pelos conceitos que a banca precisa ter em mãos, e então mostro como o trabalho "
        "foi feito, o que foi construído e como isso foi avaliado. Fecho retomando cada objetivo, "
        "com o limite do que foi medido.",
    )


def intro_contexto(deck):
    slide = deck.novo()
    cabecalho(slide, "Introdução", "A videoaula virou material de estudo")
    itens(
        slide, 0.5, 1.35, 12.3, 4.6,
        [
            "Em 2020, o ensino remoto emergencial levou plataformas digitais a todos os níveis de ensino.",
            "Nos primeiros meses de isolamento, os canais de videoaula de ciências no YouTube cresceram cerca de 140% (Souza e Vilela, 2021).",
            "O formato se consolidou. Rever a aula inteira, ou achar um trecho do que foi dito, continua custando tempo.",
            "O material audiovisual segue amplamente usado. O que falta é um meio de consumi-lo em texto, em menos tempo.",
        ],
        22, espaco=16,
    )
    notas(
        slide,
        "O ponto de partida é a pandemia. O ensino remoto colocou a videoaula no centro do estudo, "
        "e Souza e Vilela registram um crescimento de cerca de 140% nos canais de ciências no YouTube "
        "logo no início do isolamento. Isso não voltou atrás: a videoaula continua sendo material de estudo. "
        "O custo, para o estudante, é o tempo de rever a aula e a dificuldade de consultar um ponto específico do que foi falado. "
        "É nesse cenário que o trabalho se coloca.",
    )


def intro_ferramentas(deck):
    slide = deck.novo()
    cabecalho(slide, "Introdução", "Três ferramentas, e o que falta nelas")
    cartoes = [
        ("YouTube", "Legendas automáticas e o recurso “Resuma o vídeo”, no próprio player, em geral sem custo extra.", "Não organiza a aula por universidade, curso e tema, nem guarda transcrição editável e PDF ligados a essa ficha."),
        ("Otter.ai", "Transcreve e resume. O produto é desenhado como ata de reunião, e o uso contínuo depende de plano pago.", "Não cataloga a videoaula por disciplina e não oferece o texto em Libras."),
        ("Notta", "Também transcreve e resume, como serviço hospedado e tarifado.", "Não traz o fluxo de metadados de uma disciplina nem a opção de obter o texto em Libras."),
    ]
    for indice, (nome, faz, falta) in enumerate(cartoes):
        y = 1.28 + indice * 1.85
        retangulo(slide, 0.48, y, 12.35, 1.72, CREME)
        retangulo(slide, 0.48, y, 0.1, 1.72, AMARELO)
        texto(slide, 0.85, y + 0.14, 11.6, 0.36, nome, 20, True, PRETO)
        texto(slide, 0.85, y + 0.54, 11.6, 0.48, faz, 15, False, TINTA)
        texto(slide, 0.85, y + 1.08, 11.6, 0.5, falta, 15, True, CINZA)
    notas(
        slide,
        "A contribuição não começa do zero. Três ferramentas já fazem transcrição ou resumo. "
        "As legendas e o Resuma o vídeo do YouTube ficam no player: não há ficha acadêmica, "
        "transcrição editável pelo autor da aula nem PDF ligado a essa ficha. "
        "O Otter é um produto de ata de reunião, pago no uso contínuo, sem Libras. "
        "O Notta também é um serviço tarifado, sem os metadados de uma disciplina e sem Libras. "
        "O que o UTranscript acrescenta aparece no próximo slide.",
    )


def problema(deck):
    slide = deck.novo()
    cabecalho(slide, "Problema de pesquisa", "A lacuna não é inventar a transcrição")
    texto(
        slide, 0.5, 1.28, 12.3, 0.7,
        "Reunir, numa aplicação própria e com modelos de pesos abertos, o que essas ferramentas deixam separado.",
        20, False, CINZA,
    )
    partes = [
        ("01", "Ficha da videoaula", "Universidade, curso e tema no mesmo registro da mídia."),
        ("02", "Transcrição editável", "O autor da aula corrige o texto que o modelo produziu."),
        ("03", "Resumo em PDF", "Síntese ligada a essa ficha, para baixar depois do processamento."),
        ("04", "VLibras sobre o texto", "O usuário aciona o avatar. A inferência não é uma assinatura por aluno."),
    ]
    for indice, (numero, titulo, detalhe) in enumerate(partes):
        coluna = indice % 2
        linha = indice // 2
        x = 0.48 + coluna * 6.4
        y = 2.2 + linha * 2.2
        retangulo(slide, x, y, 6.1, 2.0, CREME)
        texto(slide, x + 0.28, y + 0.22, 1.3, 0.45, numero, 22, True, RGBColor(0x8A, 0x6A, 0x00))
        texto(slide, x + 0.28, y + 0.75, 5.5, 0.4, titulo, 20, True, PRETO)
        texto(slide, x + 0.28, y + 1.22, 5.5, 0.55, detalhe, 15, False, CINZA)
    notas(
        slide,
        "O problema não é a inexistência de transcrição automática. Ela já existe. "
        "A lacuna é reunir, numa aplicação própria, a ficha da videoaula, a transcrição que o autor pode editar, "
        "o resumo em PDF e o acionamento do VLibras sobre o texto. "
        "Os modelos são de pesos abertos: Distil-Whisper large-v3 e Llama 3.1 8B Instruct. "
        "O custo da inferência fica na infraestrutura de quem opera o sistema, e não numa assinatura por aluno.",
    )


def questao(deck):
    slide = deck.novo()
    cabecalho(slide, "Questão de pesquisa", "A pergunta que orienta o trabalho")
    retangulo(slide, 0.7, 1.7, 11.9, 3.5, CREME)
    retangulo(slide, 0.7, 1.7, 0.12, 3.5, AMARELO)
    texto(
        slide, 1.15, 2.05, 11.1, 2.8,
        "Como oferecer aos estudantes um meio de consumir videoaulas em menos tempo, com o conteúdo em texto, num contexto em que o material audiovisual continua amplamente usado?",
        28, False, PRETO,
    )
    texto(
        slide, 0.7, 5.5, 11.9, 0.7,
        "Formulação do capítulo 1. A resposta construída é a plataforma UTranscript.",
        16, False, CINZA,
    )
    notas(
        slide,
        "Esta é a formulação do problema no capítulo 1, lida como pergunta. "
        "Como oferecer ao estudante um meio de consumir a videoaula em menos tempo, com o conteúdo em texto, "
        "sem ignorar que o audiovisual continua sendo o material de estudo. "
        "A resposta que o trabalho constrói é o UTranscript. Os objetivos dizem o que essa resposta precisava entregar.",
    )


def objetivos(deck):
    slide = deck.novo()
    cabecalho(slide, "Objetivos", "O que se pretendia alcançar")
    retangulo(slide, 0.48, 1.25, 12.35, 1.35, PRETO)
    texto(slide, 0.75, 1.4, 11.8, 0.28, "OBJETIVO GERAL", 12, True, AMARELO)
    texto(
        slide, 0.75, 1.72, 11.8, 0.7,
        "Criar uma aplicação web, em arquitetura de microsserviços, para transcrever e resumir videoaulas.",
        20, False, BRANCO,
    )
    especificos = [
        ("1", "Interface", "Envio da videoaula e exibição estruturada da transcrição e do resumo."),
        ("2", "Reconhecimento de fala", "Distil-Whisper large-v3 para converter o áudio em texto."),
        ("3", "Resumo", "Llama 3.1 sobre o texto transcrito."),
        ("4", "Avaliação", "Qualidade e fidelidade, por leitura técnica da aula e do resumo."),
    ]
    for indice, (numero, titulo, detalhe) in enumerate(especificos):
        x = 0.48 + indice * 3.15
        retangulo(slide, x, 2.85, 3.02, 3.55, CREME)
        texto(slide, x + 0.18, 3.05, 2.65, 0.5, numero, 26, True, RGBColor(0x8A, 0x6A, 0x00))
        texto(slide, x + 0.18, 3.65, 2.65, 0.85, titulo, 18, True, PRETO)
        texto(slide, x + 0.18, 4.55, 2.65, 1.5, detalhe, 14, False, CINZA)
    notas(
        slide,
        "O objetivo geral é a aplicação web, em microsserviços, capaz de transcrever e resumir videoaulas. "
        "Os específicos são quatro, e a conclusão volta a eles na mesma ordem. "
        "Primeiro, a interface de envio e de consulta. Segundo, o reconhecimento de fala com o Distil-Whisper large-v3. "
        "Terceiro, o resumo com o Llama 3.1. Quarto, avaliar a qualidade e a fidelidade por leitura técnica, "
        "comparando o texto sintetizado com a aula. É esse quarto objetivo que o capítulo de avaliação responde.",
    )


def conceitos_modelos(deck):
    slide = deck.novo()
    cabecalho(slide, "Conceitos", "Dois modelos, papéis diferentes")
    retangulo(slide, 0.48, 1.28, 6.1, 5.5, CREME)
    retangulo(slide, 6.75, 1.28, 6.1, 5.5, CREME)
    texto(slide, 0.75, 1.48, 5.6, 0.3, "RECONHECIMENTO DE FALA", 13, True, RGBColor(0x8A, 0x6A, 0x00))
    texto(slide, 0.75, 1.9, 5.6, 0.8, "Distil-Whisper large-v3", 24, True, PRETO)
    itens(
        slide, 0.75, 2.9, 5.5, 3.4,
        [
            "É o modelo. Arquitetura encoder-decoder, versão destilada.",
            "O motor de inferência é outro componente: a biblioteca faster-whisper, sobre o CTranslate2.",
            "Mantém o reconhecimento e reduz tempo e memória em relação ao Whisper large original (Gandhi, von Werra e Wolf, 2023).",
        ],
        16, espaco=12,
    )
    texto(slide, 7.02, 1.48, 5.6, 0.3, "RESUMO", 13, True, RGBColor(0x8A, 0x6A, 0x00))
    texto(slide, 7.02, 1.9, 5.6, 0.8, "Llama 3.1 8B Instruct", 24, True, PRETO)
    itens(
        slide, 7.02, 2.9, 5.5, 3.4,
        [
            "Modelo de linguagem de 8 bilhões de parâmetros, ajustado para seguir instrução.",
            "A transcrição entra no prompt. O modelo gera o resumo a partir desse texto.",
            "Na placa de 8 GB, a execução é em 4 bits (NF4).",
        ],
        16, espaco=12,
    )
    notas(
        slide,
        "Aqui separo modelo e motor, porque são coisas diferentes. "
        "O modelo de fala é o Distil-Whisper large-v3. Quem o executa é a biblioteca faster-whisper, com o CTranslate2. "
        "A versão destilada foi escolhida por reduzir tempo e memória, com reconhecimento comparável ao Whisper large. "
        "O resumo é outro modelo: Llama 3.1 8B Instruct, da Meta, ajustado para seguir instrução. "
        "Ele não ouve o áudio. Ele lê a transcrição que o Whisper colocou no prompt. "
        "Na RTX 4060 Ti, de 8 GB, esse Llama roda quantizado em 4 bits.",
    )


def conceitos_criterios(deck):
    slide = deck.novo()
    cabecalho(slide, "Conceitos", "O que “qualidade” significa neste trabalho")
    criterios = [
        ("Fidelidade", "Não inventar fala nem conceito ausente da aula, e não distorcer o que foi dito."),
        ("Cobertura", "Os tópicos centrais da aula aparecem no resumo."),
        ("Omissão", "Tópico importante que ficou de fora."),
        ("Informação inventada", "Frase do resumo ou da transcrição que não está no vídeo."),
        ("Erro factual", "Informação reconhecível, porém trocada."),
        ("Organização", "Tópicos legíveis, sem mistura de assuntos."),
    ]
    for indice, (nome, definicao) in enumerate(criterios):
        coluna = indice % 3
        linha = indice // 3
        x = 0.48 + coluna * 4.2
        y = 1.28 + linha * 1.85
        retangulo(slide, x, y, 4.02, 1.7, CREME)
        texto(slide, x + 0.2, y + 0.16, 3.62, 0.4, nome, 16, True, PRETO)
        texto(slide, x + 0.2, y + 0.62, 3.62, 0.9, definicao, 14, False, CINZA)
    texto(
        slide, 0.5, 5.15, 12.3, 1.7,
        "O juiz avalia o resumo comum e o personalizado: nota absoluta de um único texto, sem compará-lo a outro (Zheng et al., 2023; Liu et al., 2023).",
        16, False, TINTA,
    )
    notas(
        slide,
        "Estes seis termos voltam na avaliação, então vale fixá-los agora. "
        "Fidelidade é não inventar e não distorcer. Cobertura é o tópico central estar no resumo. "
        "Omissão é o que ficou de fora. Informação inventada é frase que não está no vídeo. "
        "Erro factual é informação reconhecível, mas trocada. Organização é o texto em tópicos legíveis. "
        "Além da leitura humana, o Qwen3 avalia o resumo comum e o personalizado. "
        "Ele lê o prompt que foi usado na geração e o texto produzido, e dá nota absoluta a um texto só, sem escolher entre dois resumos. "
        "Zheng e colegas chamam isso de single answer grading; Liu e colegas usam o mesmo tipo de nota no G-Eval.",
    )


def conceitos_arquitetura(deck):
    slide = deck.novo()
    cabecalho(slide, "Conceitos", "Três processos, não três camadas")
    topicos = [
        "Não é arquitetura em camadas",
        "Interface, Spring Boot e microsserviço Python",
        "Processo com deploy próprio (Newman, 2021)",
        "VLibras: avatar sobre o texto",
        "Sem teste com usuários de Libras",
    ]
    for indice, linha in enumerate(topicos):
        y = 1.28 + indice * 1.08
        retangulo(slide, 0.48, y, 7.35, 0.94, CREME)
        retangulo(slide, 0.48, y, 0.08, 0.94, AMARELO)
        texto(slide, 0.78, y, 6.85, 0.94, linha, 18, False, PRETO, ancora=MSO_ANCHOR.MIDDLE)
    imagem(slide, "vlibras.png", 8.15, 1.28, 4.6, 5.4)
    notas(
        slide,
        "Uma correção de conceito, antes de mostrar o sistema. "
        "Arquitetura em camadas seria apresentação, regra de negócio e dados. Não é isso que está no trabalho. "
        "Há uma interface, uma aplicação Spring Boot, que concentra regra, autenticação e banco, "
        "e um processo Python separado para a inferência. Newman trata o microsserviço como processo com deploy próprio, e é nesse sentido que a palavra é usada. "
        "O VLibras entra como opção: o usuário aciona o avatar sobre o texto. "
        "Não afirmo que o sistema melhora a aprendizagem de estudantes surdos, porque não houve avaliação com esses usuários. "
        "Exportar um vídeo de Libras, fora do avatar, ficou como trabalho futuro.",
    )


def metodo_caminho(deck):
    slide = deck.novo()
    cabecalho(slide, "Método", "Como o trabalho foi conduzido")
    passos = [
        ("1", "Origem", "Um transcritor de atas de reunião mostrou o uso da transcrição no contexto educacional."),
        ("2", "Requisitos", "Oito requisitos funcionais e seis não funcionais, entre eles a ficha da aula, o PDF e o VLibras."),
        ("3", "Construção", "Projeto da solução e implementação iterativa, em Kanban no Trello, de julho a outubro de 2025."),
        ("4", "Exame", "Leitura técnica do autor e nota do juiz, no resumo comum e no personalizado."),
    ]
    for indice, (numero, titulo, detalhe) in enumerate(passos):
        y = 1.25 + indice * 1.4
        retangulo(slide, 0.48, y, 12.35, 1.25, CREME)
        retangulo(slide, 0.48, y, 0.9, 1.25, PRETO)
        texto(slide, 0.48, y, 0.9, 1.25, numero, 22, True, AMARELO, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
        texto(slide, 1.6, y + 0.16, 10.9, 0.35, titulo, 18, True, PRETO)
        texto(slide, 1.6, y + 0.55, 10.9, 0.55, detalhe, 16, False, CINZA)
    notas(
        slide,
        "O método é o caminho do próprio desenvolvimento, não um experimento com grupo controle. "
        "A ferramenta nasceu de um transcritor de atas. Dessa experiência vieram os requisitos: "
        "cadastro, envio, YouTube, transcrição, PDF, edição, busca, exclusão, e os não funcionais de segurança, "
        "usabilidade, Libras e o restante. "
        "A construção foi iterativa, num quadro Kanban, de julho a outubro de 2025. "
        "O exame do que foi construído é o capítulo 4, que eu detalho no próximo slide e retomo na avaliação. "
        "O juiz automático nota os dois resumos: o comum, quando o campo fica vazio, e o personalizado.",
    )


def metodo_avaliacao(deck):
    slide = deck.novo()
    cabecalho(slide, "Método", "Como a solução foi examinada")
    cartoes = [
        ("Quem", "O autor. Não há segundo avaliador humano e, portanto, não há procedimento de divergência entre pessoas."),
        ("O que se compara", "O trecho da videoaula e o resumo em PDF. A transcrição é julgada por esse resumo, porque é ela que entra no prompt."),
        ("Critérios", "Fidelidade, cobertura, omissão, informação inventada, erro factual e organização, como definidos há pouco."),
        ("Complemento", "O Qwen3-0.6B lê o prompt usado, comum ou personalizado, e o resultado, e devolve quatro notas de 0 a 1."),
    ]
    for indice, (titulo, detalhe) in enumerate(cartoes):
        coluna = indice % 2
        linha = indice // 2
        x = 0.48 + coluna * 6.4
        y = 1.28 + linha * 2.35
        retangulo(slide, x, y, 6.15, 2.15, CREME)
        texto(slide, x + 0.25, y + 0.2, 5.65, 0.4, titulo, 18, True, PRETO)
        texto(slide, x + 0.25, y + 0.7, 5.65, 1.2, detalhe, 15, False, CINZA)
    notas(
        slide,
        "A avaliação principal é qualitativa e foi feita por mim. Assisto ao trecho e leio o PDF. "
        "Não houve segundo avaliador, então não há como tratar divergência entre pessoas. Isso é um limite, e eu o assumo na conclusão. "
        "A transcrição não foi comparada a um texto de referência palavra por palavra. "
        "Ela entra no prompt do resumo; se o resumo traz a informação certa da aula, a transcrição levou esse conteúdo ao modelo. "
        "O Qwen3 de 0,6 bilhão de parâmetros lê o prompt que foi gravado na transcrição, seja o acadêmico padrão ou o personalizado, e devolve adesão, fidelidade, cobertura e organização. "
        "O tempo de processamento foi medido no Docker, mas não é o critério de qualidade. A placa do ensaio é uma placa de jogos.",
    )


def dev_processos(deck):
    slide = deck.novo()
    cabecalho(slide, "Desenvolvimento", "A solução em três processos")
    colunas = [
        ("Interface", "Ionic 8, Angular 19 e TypeScript. Formulários, rotas e o estado da sessão no navegador."),
        ("Spring Boot", "Regra de negócio, JWT em cookie HttpOnly e PostgreSQL 15, via JPA. É quem grava a ficha."),
        ("FastAPI", "Python 3.10. Recebe o áudio, roda os modelos na GPU e devolve texto e status."),
    ]
    for indice, (titulo, detalhe) in enumerate(colunas):
        x = 0.48 + indice * 4.2
        retangulo(slide, x, 1.3, 4.0, 3.15, PRETO if indice == 1 else CREME)
        cor_titulo = AMARELO if indice == 1 else PRETO
        cor_texto = BRANCO if indice == 1 else CINZA
        texto(slide, x + 0.25, 1.5, 3.5, 0.7, titulo, 22, True, cor_titulo)
        texto(slide, x + 0.25, 2.35, 3.5, 1.8, detalhe, 16, False, cor_texto)
    texto(
        slide, 0.5, 4.7, 12.3, 2.1,
        "A conversa entre os três é REST, em JSON. O arquivo da videoaula vai em multipart/form-data. Editar e excluir só é efetivado se o usuário do token for o autor do registro.",
        18, False, TINTA,
    )
    notas(
        slide,
        "Na prática são três processos. A interface é Ionic com Angular 19. "
        "O Spring Boot é o núcleo: autentica com JWT num cookie HttpOnly, aplica a regra de autoria e persiste no PostgreSQL 15. "
        "O FastAPI fica isolado porque é ele que segura a GPU. "
        "Quem edita ou apaga uma videoaula precisa ser o autor, e essa checagem está no serviço, não só escondendo o botão na tela. "
        "O próximo slide é a ordem em que uma aula percorre esses processos.",
    )


def dev_fluxo(deck):
    slide = deck.novo()
    cabecalho(slide, "Desenvolvimento", "O processamento não trava a interface")
    imagem(slide, "sequencia.png", 1.3, 1.18, 10.7, 5.8)
    notas(
        slide,
        "Este é o diagrama de sequência do trabalho. O usuário pede a transcrição. "
        "O Spring salva o registro como Em andamento e já responde, para a tela não ficar presa. "
        "Em paralelo, manda o áudio ao FastAPI. O FastAPI confirma o recebimento e, noutra thread, chama o Distil-Whisper e depois o Llama 3.1. "
        "Quando termina, faz um PUT no Spring com a transcrição, o resumo e o status Concluída. Se falhar, o mesmo caminho grava Com erro. "
        "O PDF não nasce nessa thread. Ele é montado na exportação, quando o usuário pede o download. "
        "Foi o que o ensaio de desempenho também mostrou: a exportação ocorreu depois e não entrou nos 10 minutos e 27 segundos.",
    )


def dev_ficha(deck):
    slide = deck.novo()
    cabecalho(slide, "Desenvolvimento", "A videoaula fica numa ficha")
    imagem(slide, "casos_uso.png", 3.8, 1.18, 5.7, 5.85)
    notas(
        slide,
        "À esquerda está o que o banco guarda. O usuário nasce ligado a uma universidade e a um curso. "
        "O tema é do curso. A videoaula é a ficha: título, data, professor, e o usuário que a criou. "
        "A transcrição é um para um com essa videoaula. "
        "À direita, o caso de uso só desenha o que o usuário faz diretamente. "
        "Criar a transcrição sempre dispara o processamento. Baixar o vídeo pode ser o arquivo inteiro ou só o áudio. "
        "A exclusão não aparece no diagrama porque obedece à mesma regra de autoria da edição. "
        "Transcrição automática e PDF também não são casos de uso próprios: acontecem dentro do processamento.",
    )


def dev_prompts(deck):
    slide = deck.novo()
    cabecalho(slide, "Desenvolvimento", "Resumo comum ou extração pedida")
    retangulo(slide, 0.45, 1.25, 6.15, 2.55, CREME)
    texto(slide, 0.7, 1.4, 5.7, 0.35, "Campo vazio", 18, True, PRETO)
    texto(
        slide, 0.7, 1.9, 5.7, 1.65,
        "Vale o resumo acadêmico. Em exercício, o texto prioriza enunciado, passos e resultado. Se a fala não fecha a resolução, entra a subseção Resolução complementar, marcada como elaborada pelo sistema.",
        15, False, CINZA,
    )
    retangulo(slide, 0.45, 4.0, 6.15, 2.55, PRETO)
    texto(slide, 0.7, 4.15, 5.7, 0.35, "Campo preenchido", 18, True, AMARELO)
    texto(
        slide, 0.7, 4.65, 5.7, 1.65,
        "A instrução é enviada antes da inferência. O modelo deixa o resumo geral e devolve só o que a instrução pediu, a partir da transcrição.",
        15, False, BRANCO,
    )
    imagem(slide, "prompt_form.png", 6.85, 1.25, 6.0, 5.55)
    notas(
        slide,
        "No cadastro há um campo opcional de prompt. Se o usuário deixa vazio, o sistema faz o resumo acadêmico. "
        "A instrução pede, para cada tema, o conceito e o exemplo, e, quando há exercício, enunciado, passos e resultado. "
        "Se o professor enunciou um exercício e não o resolveu, ou se a transcrição da resolução ficou ilegível, "
        "o sistema pode completar, numa subseção chamada Resolução complementar, deixando explícito que aquilo foi elaborado pelo sistema. "
        "Fora desses exercícios, a instrução proíbe inventar conteúdo. "
        "Se o campo vem preenchido, como nesta tela, o modelo não resume a aula inteira: extrai o que a instrução pediu. "
        "Neste exemplo, só o segundo exercício.",
    )


def dev_parametros(deck):
    slide = deck.novo()
    cabecalho(slide, "Desenvolvimento", "O que cada modelo executa")
    linhas_tabela = [
        ("Distil-Whisper large-v3", "GPU, compute_type int8_float16, idioma português. Biblioteca faster-whisper."),
        ("Llama 3.1 8B Instruct", "4 bits, NF4, no máximo 1024 tokens novos. O PDF é montado depois dessa geração."),
        ("Qwen3-0.6B", "Juiz do resumo comum e do personalizado. A variante de 8B não coube junto do Llama e do Whisper."),
    ]
    for indice, (modelo, detalhe) in enumerate(linhas_tabela):
        y = 1.35 + indice * 1.55
        retangulo(slide, 0.48, y, 12.35, 1.4, CREME)
        texto(slide, 0.75, y + 0.18, 11.8, 0.4, modelo, 20, True, PRETO)
        texto(slide, 0.75, y + 0.68, 11.8, 0.5, detalhe, 16, False, CINZA)
    notas(
        slide,
        "Três fatos que a banca costuma perguntar. "
        "O Whisper em execução é o distil-large-v3, na GPU, com compute_type int8_float16 e idioma português, pela faster-whisper. "
        "O Llama 3.1 8B Instruct gera no máximo 1024 tokens novos. Esse teto não é um detalhe de configuração: "
        "ele corta a resposta final de vários exercícios, e isso aparece na avaliação. "
        "O juiz é o Qwen3 de 0,6 bilhão, não o de 8. Na RTX 4060 Ti o Llama em 4 bits e o Whisper já ocupam a memória de vídeo, "
        "e o Qwen de 8 bilhões não permanece carregado junto deles. "
        "Ele avalia o resumo comum e o personalizado: recebe o prompt gravado na transcrição e o texto gerado. "
        "O juiz não reescreve o resumo. Ele devolve as quatro notas.",
    )


def dev_docker(deck):
    slide = deck.novo()
    cabecalho(slide, "Desenvolvimento", "O ensaio subiu em quatro containers")
    servicos = [
        ("db-tcc", "PostgreSQL 15"),
        ("backend-spring", "API na porta 8080"),
        ("frontend-angular", "Interface na porta 4200"),
        ("ai-python", "Modelos na porta 5000, com a GPU"),
    ]
    for indice, (nome, detalhe) in enumerate(servicos):
        x = 0.48 + indice * 3.2
        retangulo(slide, x, 1.4, 3.02, 2.15, PRETO if indice == 3 else CREME)
        texto(slide, x + 0.18, 1.58, 2.66, 0.7, nome, 16, True, AMARELO if indice == 3 else PRETO)
        texto(slide, x + 0.18, 2.4, 2.66, 0.8, detalhe, 15, False, BRANCO if indice == 3 else CINZA)
    texto(
        slide, 0.5, 3.9, 12.3, 2.6,
        "A GPU reservada ao ai-python foi uma NVIDIA GeForce RTX 4060 Ti, com 8188 MiB. O protótipo rodou nessa máquina. Não ficou acessível 24 horas por dia.",
        20, False, TINTA,
    )
    notas(
        slide,
        "O ensaio de desempenho, que eu mostro mais à frente, não instalou os processos direto no sistema. "
        "O Docker Compose sobe quatro containers: o banco PostgreSQL 15, o Spring na 8080, a interface na 4200 "
        "e o ai-python na 5000, com runtime NVIDIA e uma GPU reservada, a RTX 4060 Ti de 8188 MiB. "
        "Nesse container estão o Distil-Whisper e o Llama. "
        "Vale antecipar o limite do requisito de disponibilidade: o protótipo é local. Não ficou no ar o tempo todo.",
    )


def resultados_cadastro(deck):
    slide = deck.novo()
    cabecalho(slide, "Resultados", "Da conta à ficha da aula")
    imagem(slide, "tela_48.png", 1.7, 1.2, 3.45, 5.75)
    imagem(slide, "tela_49.png", 5.5, 1.2, 6.1, 5.75)
    notas(
        slide,
        "A partir daqui é o sistema em uso, com telas do manual. "
        "No cadastro, o estudante informa nome, e-mail, senha, universidade e curso. A ficha acadêmica começa aí. "
        "Na criação da videoaula, os mesmos metadados reaparecem: universidade, curso, professor e tema, mais o arquivo. "
        "O campo de prompt personalizado está na mesma tela. Se ficar vazio, a extração é a comum. "
        "O envio dispara o fluxo assíncrono que mostrei no diagrama.",
    )


def resultados_consulta(deck):
    slide = deck.novo()
    cabecalho(slide, "Resultados", "Consulta, texto e PDF")
    imagem(slide, "tela_52.png", 0.3, 1.2, 5.5, 5.7)
    imagem(slide, "tela_51.png", 5.95, 1.2, 7.0, 5.7)
    notas(
        slide,
        "À esquerda, a consulta filtra por título, tema, universidade e curso, e mostra o status Concluído. "
        "À direita, o detalhe da videoaula: a ficha, o texto gerado e o botão de exportar para PDF. "
        "O ícone azul é o acionamento do VLibras sobre esse texto. "
        "Quem é o autor vê a edição. Quem não é, não conclui a alteração no serviço, mesmo que a tela esconda o controle. "
        "O fluxo observável do primeiro objetivo é este: criar a conta, enviar a mídia, acompanhar o status e baixar o PDF.",
    )


def resultados_libras(deck):
    slide = deck.novo()
    cabecalho(slide, "Resultados", "Vídeo de origem e texto em Libras")
    imagem(slide, "tela_53.png", 0.45, 2.0, 7.3, 3.6)
    imagem(slide, "vlibras.png", 8.2, 1.25, 4.5, 5.55)
    texto(
        slide, 0.5, 5.7, 7.4, 1.2,
        "O download parte de uma URL do YouTube. O avatar é uma opção sobre o texto, não uma avaliação com usuários.",
        16, False, CINZA,
    )
    notas(
        slide,
        "Duas funções que completam o uso, e que eu não quero superdimensionar. "
        "O YouTube Downloader recebe a URL e obtém o vídeo para o fluxo de transcrição, ou para o usuário baixar a mídia. "
        "O VLibras é o widget oficial, acionado na tela do texto. O avatar traduz o que está escrito. "
        "Isso atende o requisito de oferecer a opção. Não é evidência de que a tradução foi boa para um usuário de Libras, "
        "porque esse teste não foi feito.",
    )


def avaliacao_criterios(deck):
    slide = deck.novo()
    cabecalho(slide, "Avaliação", "Quem avaliou e com quais critérios")
    retangulo(slide, 0.48, 1.25, 12.35, 1.45, PRETO)
    texto(
        slide, 0.75, 1.45, 11.85, 1.05,
        "Avaliador: o autor. Procedimento: assistir ao trecho e ler o PDF. A transcrição é conferida pelo que o resumo extraiu dela.",
        20, False, BRANCO,
    )
    pares = [
        ("Fidelidade", "Não inventa e não distorce"),
        ("Cobertura", "O tópico central está no texto"),
        ("Omissão", "O que ficou de fora"),
        ("Invenção", "Frase que não está no vídeo"),
        ("Erro factual", "Informação trocada"),
        ("Organização", "Tópicos legíveis"),
    ]
    for indice, (nome, detalhe) in enumerate(pares):
        x = 0.48 + (indice % 6) * 2.1
        retangulo(slide, x, 2.95, 2.0, 1.7, CREME)
        texto(slide, x + 0.1, 3.08, 1.8, 0.7, nome, 14, True, PRETO, PP_ALIGN.CENTER)
        texto(slide, x + 0.1, 3.75, 1.8, 0.7, detalhe, 12, False, CINZA, PP_ALIGN.CENTER)
    texto(
        slide, 0.5, 4.9, 12.3, 1.9,
        "A leitura de conteúdo usa as aulas que podem ser conferidas nas figuras: limites, como resolução de exercício; Dijkstra, como aula explicativa; e três prompts personalizados.",
        18, False, TINTA,
    )
    notas(
        slide,
        "Entro na avaliação. O avaliador sou eu. Não há segunda pessoa, e isso limita o quanto a leitura pode ser generalizada. "
        "O procedimento é assistir ao trecho e ler o PDF, com os critérios que defini antes. "
        "A transcrição não tem uma referência palavra a palavra. Eu a avalio pelo resumo, porque é a transcrição que o modelo lê. "
        "As aulas desta leitura foram escolhidas porque o resumo, o trecho ou a nota do juiz aparecem nas figuras do trabalho: "
        "a aula de limites, a de Dijkstra, e os prompts personalizados de grafos, de um segundo exercício e de análise sintática.",
    )


def avaliacao_tipos(deck):
    slide = deck.novo()
    cabecalho(slide, "Avaliação", "Exercício e aula explicativa")
    imagem(slide, "resumo_exercicio.png", 0.35, 1.2, 6.2, 4.85)
    imagem(slide, "resumo_dijkstra.png", 6.75, 1.2, 6.2, 4.85)
    texto(slide, 0.4, 6.15, 6.2, 0.85, "Limites: a explicação e o encaminhamento saem em texto. O valor do limite, não.", 13, False, CINZA, PP_ALIGN.CENTER)
    texto(slide, 6.75, 6.15, 6.2, 0.85, "Dijkstra: o texto segue o roteiro e perde o encadeamento da fala.", 13, False, CINZA, PP_ALIGN.CENTER)
    notas(
        slide,
        "O mesmo procedimento dá resultados desiguais. "
        "Na videoaula de limites, que é resolução de exercício, o resumo descreve a explicação e o encaminhamento: conjugados, potenciação, o passo a passo. "
        "O funcionamento favorece esse tipo de aula. "
        "Na aula do algoritmo de Dijkstra, que é explicativa e não tem exercício resolvido, o modelo extrai as informações, mas o texto perde o encadeamento que a fala constrói. "
        "A cobertura fica mais pobre. O que permanece saiu da transcrição, então o conteúdo certo ainda indica que a transcrição levou a aula ao modelo. "
        "A perda de encadeamento não é falha de envio do arquivo. "
        "No Dijkstra, a sugestão final de otimizar a implementação é o trecho que sai do roteiro da aula, e ela não desenvolve o critério do algoritmo.",
    )


def avaliacao_teto(deck):
    slide = deck.novo()
    cabecalho(slide, "Avaliação", "O teto de 1024 tokens")
    topicos = [
        "Teto de 1024 tokens novos",
        "O procedimento ocupa o espaço",
        "A resposta final fica de fora",
        "Gemini: quatro exercícios e os intervalos",
        "Os dois deixam a álgebra sem fechar",
        "Gemini marca os tempos; o UTranscript explica o conjugado",
    ]
    for indice, linha in enumerate(topicos):
        y = 1.25 + indice * 0.9
        retangulo(slide, 0.48, y, 7.55, 0.78, CREME)
        retangulo(slide, 0.48, y, 0.08, 0.78, AMARELO)
        texto(slide, 0.75, y, 7.1, 0.78, linha, 16, False, PRETO, ancora=MSO_ANCHOR.MIDDLE)
    imagem(slide, "resumo_youtube.png", 8.25, 1.22, 4.65, 5.7)
    notas(
        slide,
        "O teto de 1024 tokens novos explica uma parte do que se vê no resumo de exercício. "
        "O modelo ocupa os tokens com a técnica e o passo, e muitas vezes não sobra espaço para o resultado. "
        "Na aula de limites, o recurso Resuma o vídeo do YouTube, operado pelo Gemini, organizou a aula em quatro exercícios, "
        "com o minuto em que cada um aparece: raiz cúbica, conjugado, limites laterais e o limite com h. "
        "Esse texto também não traz a resolução algébrica fechada. "
        "A diferença é o recorte. O Gemini lista os exercícios e empurra a explicação do conjugado para uma pergunta seguinte. "
        "No UTranscript, a instrução pede o conceito no próprio resumo, e o conjugado já sai escrito. O valor do limite é que fica de fora, pelo teto.",
    )


def avaliacao_juiz(deck):
    slide = deck.novo()
    cabecalho(slide, "Avaliação", "A nota do juiz")
    texto(slide, 0.45, 1.15, 6.3, 0.32, "Grafos, exercício 5 (Maioli, 2020)", 16, True, PRETO)
    texto(slide, 0.45, 1.46, 6.3, 0.32, "O mesmo juiz também avalia o resumo comum.", 13, False, CINZA)
    texto(slide, 0.45, 1.82, 6.3, 0.55, "Nota 0,8875", 28, True, PRETO)
    texto(slide, 0.45, 2.42, 6.3, 0.75, "Adesão 0,85    Fidelidade 0,95\nCobertura 0,9    Organização 0,85", 16, False, CINZA)
    texto(
        slide, 0.45, 3.25, 6.3, 1.3,
        "Leitura do autor: a tabela não cobre a árvore inteira. Ficam de fora o nó de subtração e folhas. O texto chama a árvore de arbusto.",
        15, False, TINTA,
    )
    retangulo(slide, 0.45, 4.65, 6.3, 2.15, PRETO)
    texto(slide, 0.7, 4.8, 5.85, 0.35, "Análise Sintática Parte 2 (Lins, 2012)", 15, True, AMARELO)
    texto(slide, 0.7, 5.15, 5.85, 0.5, "Nota 0,965", 24, True, BRANCO)
    texto(slide, 0.7, 5.68, 5.85, 0.9, "Adesão 0,95 · Fidelidade 0,98\nCobertura 0,97 · Organização 0,96", 14, False, BRANCO)
    imagem(slide, "prompt_nota.png", 6.95, 1.18, 5.95, 5.7)
    notas(
        slide,
        "O Qwen avalia os dois resumos. O Spring envia o prompt gravado na transcrição, comum ou personalizado, junto com o texto gerado. "
        "As notas desta tela são de prompts personalizados. Neles, a referência da leitura é a instrução, não a aula inteira. "
        "Na videoaula de dez exercícios de grafos, o pedido foi só o exercício 5. "
        "O juiz deu nota 0,8875: adesão 0,85, fidelidade 0,95, cobertura 0,9 e organização 0,85. "
        "A minha leitura discorda do elogio da justificativa. A tabela não cobre a árvore do slide: "
        "faltam o nó de subtração e folhas, e o texto chama a árvore de arbusto. A nota alta não apaga essa omissão. "
        "Na aula de Análise Sintática Parte 2, o prompt pedia o que o professor comentou sobre a análise top-down. "
        "A nota foi 0,965, com adesão 0,95, fidelidade 0,98, cobertura 0,97 e organização 0,96. "
        "O juiz é complemento. A leitura de conteúdo continua sendo a minha.",
    )


def avaliacao_tempo(deck):
    slide = deck.novo()
    cabecalho(slide, "Avaliação", "O tempo foi medido, e não é o critério")
    texto(slide, 0.48, 1.2, 12.3, 0.55, "Notação assintótica, resolução de exercícios. 30 minutos, 42 MB. 29 de setembro de 2026.", 16, False, CINZA)
    marcas = [
        ("9 min 3 s", "Transcrição\nDistil-Whisper"),
        ("1 min 24 s", "Resumo\nLlama 3.1"),
        ("10 min 27 s", "Total, sem\no PDF"),
    ]
    for indice, (valor, rotulo) in enumerate(marcas):
        x = 0.48 + indice * 4.2
        retangulo(slide, x, 1.85, 4.0, 1.55, PRETO if indice == 2 else CREME)
        texto(slide, x + 0.2, 1.95, 3.6, 0.55, valor, 26, True, AMARELO if indice == 2 else PRETO, PP_ALIGN.CENTER)
        texto(slide, x + 0.2, 2.55, 3.6, 0.7, rotulo, 14, False, BRANCO if indice == 2 else CINZA, PP_ALIGN.CENTER)
    imagem(slide, "cpu.png", 0.4, 3.55, 8.5, 3.45)
    retangulo(slide, 8.85, 4.15, 4.0, 2.2, CREME)
    retangulo(slide, 8.85, 4.15, 0.08, 2.2, AMARELO)
    texto(slide, 9.15, 4.32, 3.5, 0.4, "Memória de vídeo", 16, True, PRETO)
    texto(slide, 9.15, 4.8, 3.5, 1.25, "Cerca de 7,8 GiB de 8,2 GiB. Os modelos permanecem carregados.", 15, False, CINZA)
    notas(
        slide,
        "Este slide é um registro de desempenho, não a avaliação do trabalho. "
        "A aula é a de notação assintótica, resolução de exercícios, com 30 minutos e 42 MB, medida em 29 de setembro de 2026. "
        "As outras aulas deste parâmetro tinham entre 10 e 20 minutos e ficaram na mesma faixa. "
        "No gráfico, o pico isolado perto de 15:29 é o download do YouTube. "
        "O bloco das 15:34 às 15:44 é a transcrição seguida do resumo. "
        "Pelos logs: Distil-Whisper, 9 minutos e 3 segundos; Llama, 1 minuto e 24 segundos; total, 10 minutos e 27 segundos. "
        "A exportação do PDF foi pedida depois e não entra nesse total. "
        "A memória de vídeo ficou em cerca de 7,8 GiB de 8,2 GiB mesmo depois da CPU cair, porque os modelos continuam carregados. "
        "A RTX 4060 Ti é placa de jogos. Almeida mede que um acelerador chega a cerca de 1,5 vez a vazão de uma placa de consumo. "
        "Por isso o tempo não é o critério. O critério é a qualidade do resumo.",
    )


def conclusao_objetivos(deck):
    slide = deck.novo()
    cabecalho(slide, "Conclusão", "O que cada objetivo alcançou")
    linhas_obj = [
        ("Geral", "A aplicação foi implementada: interface, Spring Boot e microsserviço Python transcrevem e resumem a videoaula."),
        ("Interface", "Conta, envio, detalhe com texto, busca e download do PDF formam o fluxo completo."),
        ("Fala", "Distil-Whisper large-v3, via faster-whisper. A conferência é o que o resumo extrai da transcrição."),
        ("Resumo", "Llama 3.1 8B Instruct. No exercício, a explicação sai em texto. Na aula explicativa, o desenvolvimento se perde."),
        ("Qualidade", "A leitura favorece a resolução de exercício. O mesmo procedimento, na aula explicativa, perde encadeamento."),
    ]
    for indice, (titulo, detalhe) in enumerate(linhas_obj):
        y = 1.22 + indice * 1.12
        retangulo(slide, 0.48, y, 1.7, 1.0, PRETO)
        retangulo(slide, 2.18, y, 10.65, 1.0, CREME)
        texto(slide, 0.55, y, 1.55, 1.0, titulo, 14, True, AMARELO, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
        texto(slide, 2.4, y + 0.15, 10.25, 0.72, detalhe, 15, False, TINTA, ancora=MSO_ANCHOR.MIDDLE)
    notas(
        slide,
        "Retomo os objetivos na ordem do texto. "
        "O geral foi alcançado: existe a aplicação, com interface, Spring e o microsserviço, transcrevendo e resumindo. "
        "A interface cumpre o fluxo de conta, envio, consulta e PDF. "
        "O reconhecimento de fala está em execução com o Distil-Whisper large-v3, pela faster-whisper, e a evidência dele é indireta: "
        "o acerto da informação no resumo. "
        "O Llama produz o resumo, e o resultado depende do tipo de aula. "
        "Por isso o quarto objetivo fecha assim: a qualidade observada favorece a videoaula de resolução de exercício. "
        "Na aula explicativa, o mesmo procedimento perde o desenvolvimento da fala.",
    )


def conclusao_limites(deck):
    slide = deck.novo()
    cabecalho(slide, "Conclusão", "Contribuição e limites")
    retangulo(slide, 0.45, 1.25, 6.15, 5.55, PRETO)
    texto(slide, 0.7, 1.45, 5.7, 0.4, "Contribuição", 20, True, AMARELO)
    texto(
        slide, 0.7, 2.05, 5.7, 4.3,
        "Uma aplicação própria, com modelos de pesos abertos, que guarda a videoaula numa ficha por universidade, curso e tema, com transcrição editável, resumo em PDF e a opção de acionar o VLibras sobre o texto.",
        18, False, BRANCO,
    )
    retangulo(slide, 6.8, 1.25, 6.05, 5.55, CREME)
    texto(slide, 7.05, 1.45, 5.6, 0.4, "Limites", 20, True, PRETO)
    itens(
        slide, 7.05, 2.05, 5.55, 4.4,
        [
            "Um avaliador humano.",
            "Transcrição conferida pelo resumo, sem texto de referência.",
            "Teto de 1024 tokens corta respostas.",
            "Aula explicativa perde encadeamento.",
            "Protótipo local, sem ficar no ar o tempo todo.",
        ],
        16, espaco=8,
    )
    notas(
        slide,
        "A contribuição, em uma frase: não é ter inventado a transcrição. "
        "É reunir a ficha acadêmica, a transcrição editável, o PDF e o VLibras, com modelos abertos, "
        "e com o custo da inferência na infraestrutura, não na assinatura do aluno. "
        "Os limites são os que a avaliação sustentou. Só eu li as aulas. "
        "A transcrição não foi medida contra uma referência. O teto de tokens corta a resposta. "
        "A aula explicativa perde encadeamento. E o protótipo rodou na máquina local, com GPU: "
        "o requisito de disponibilidade contínua não foi obtido.",
    )


def conclusao_futuro(deck):
    slide = deck.novo()
    cabecalho(slide, "Conclusão", "O que permanece em aberto")
    cartoes = [
        ("Libras fora do avatar", "Um módulo que converta o texto em vídeo de Libras, para o conteúdo ser usado e compartilhado sem depender do widget."),
        ("Infraestrutura", "A instância de GPU e a implantação contínua ficaram pendentes no Kanban. O protótipo não é um serviço 24 horas."),
        ("O tempo", "Com a mesma placa de jogos, aulas de 10 a 20 minutos ficaram na faixa do ensaio de 30 minutos. Mudar de classe exige um ambiente de processamento."),
    ]
    for indice, (titulo, detalhe) in enumerate(cartoes):
        y = 1.3 + indice * 1.85
        retangulo(slide, 0.48, y, 12.35, 1.7, CREME)
        retangulo(slide, 0.48, y, 0.1, 1.7, AMARELO)
        texto(slide, 0.85, y + 0.18, 11.6, 0.4, titulo, 20, True, PRETO)
        texto(slide, 0.85, y + 0.7, 11.6, 0.75, detalhe, 16, False, CINZA)
    notas(
        slide,
        "Três continuidades, todas já escritas no trabalho. "
        "A primeira é um módulo que gere vídeo de Libras a partir do texto, para o estudante usar esse formato fora do avatar, até offline. "
        "A segunda é de infraestrutura: a escolha da instância GPU e o balanceamento ficaram como tarefas a fazer. "
        "A terceira é sobre o tempo. Ele se manteve na mesma faixa porque o hardware não mudou, e esse hardware não é o acelerador indicado para a inferência. "
        "Almeida mostra que a relação de vazão entre placa de consumo e acelerador se mantém no intervalo de modelos que inclui o nosso. "
        "O tempo só mudaria de classe num ambiente de processamento.",
    )


def referencias(deck):
    slide = deck.novo()
    cabecalho(slide, "Referências", "Fontes citadas nesta apresentação")
    fontes = [
        "Souza e Vilela (2021). Videoaulas de ciências no YouTube durante o isolamento.",
        "YouTube (2026); Otter.ai (2026); Notta (2026). Ferramentas de transcrição e resumo.",
        "Gandhi, von Werra e Wolf (2023). Distil-Whisper.",
        "Newman (2021). Microsserviço como processo de deploy próprio.",
        "Zheng et al. (2023); Liu et al. (2023). Nota absoluta, sem comparação entre dois textos.",
        "Almeida (2025). Inferência em placa de consumo e em acelerador.",
        "Maioli (2020); Lins (2012). Videoaulas usadas na leitura do prompt personalizado.",
        "Brasil. Governo Digital. VLibras.",
    ]
    itens(slide, 0.55, 1.28, 12.2, 5.6, fontes, 18, espaco=10)
    notas(
        slide,
        "Estas são só as fontes que apareceram nos slides. A lista completa está no trabalho escrito. "
        "Se a banca quiser o detalhe de uma delas, eu recupero na arguição.",
    )


def encerramento(deck):
    slide = deck.novo()
    retangulo(slide, 0, 0, LARGURA, ALTURA, PRETO)
    retangulo(slide, 0, 0, LARGURA, 0.12, AMARELO)
    texto(slide, 0.7, 1.5, 12, 0.4, "UTFPR  ·  PONTA GROSSA  ·  2026", 14, True, AMARELO)
    texto(slide, 0.7, 2.15, 12, 1.1, "Obrigado.", 54, True, BRANCO)
    texto(slide, 0.7, 3.5, 11, 0.8, "Fico à disposição da banca.", 24, False, BRANCO)
    retangulo(slide, 0.7, 4.6, 2.1, 0.07, AMARELO)
    texto(slide, 0.7, 4.9, 11, 0.4, "Eduardo Robinson Silveira Junior", 20, True, BRANCO)
    texto(slide, 0.7, 5.4, 11, 0.35, "eduardorobinson@alunos.utfpr.edu.br", 18, False, AMARELO)
    texto(slide, 0.7, 5.9, 11, 0.35, "Bacharelado em Ciência da Computação", 16, False, BRANCO)
    notas(
        slide,
        "Encerro por aqui. Obrigado pelo tempo. Fico à disposição para as perguntas.",
    )


def main():
    deck = Deck()
    capa(deck)
    agenda(deck)
    intro_contexto(deck)
    intro_ferramentas(deck)
    problema(deck)
    questao(deck)
    objetivos(deck)
    conceitos_modelos(deck)
    conceitos_criterios(deck)
    conceitos_arquitetura(deck)
    metodo_caminho(deck)
    metodo_avaliacao(deck)
    dev_processos(deck)
    dev_fluxo(deck)
    dev_ficha(deck)
    dev_prompts(deck)
    dev_parametros(deck)
    dev_docker(deck)
    resultados_cadastro(deck)
    resultados_consulta(deck)
    resultados_libras(deck)
    avaliacao_criterios(deck)
    avaliacao_tipos(deck)
    avaliacao_teto(deck)
    avaliacao_juiz(deck)
    avaliacao_tempo(deck)
    conclusao_objetivos(deck)
    conclusao_limites(deck)
    conclusao_futuro(deck)
    referencias(deck)
    encerramento(deck)
    secoes = {
        2: "Agenda",
        3: "Introdução",
        4: "Introdução",
        5: "Problema",
        6: "Questão de pesquisa",
        7: "Objetivos",
        8: "Conceitos",
        9: "Conceitos",
        10: "Conceitos",
        11: "Método",
        12: "Método",
        13: "Desenvolvimento",
        14: "Desenvolvimento",
        15: "Desenvolvimento",
        16: "Desenvolvimento",
        17: "Desenvolvimento",
        18: "Desenvolvimento",
        19: "Resultados",
        20: "Resultados",
        21: "Resultados",
        22: "Avaliação",
        23: "Avaliação",
        24: "Avaliação",
        25: "Avaliação",
        26: "Avaliação",
        27: "Conclusão",
        28: "Conclusão",
        29: "Conclusão",
        30: "Referências",
        31: "Encerramento",
    }
    deck.fechar(secoes)
    deck.salvar()
    print(f"{len(deck.slides)} slides em {SAIDA}")


if __name__ == "__main__":
    main()
