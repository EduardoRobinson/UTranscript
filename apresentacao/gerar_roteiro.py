"""Gera o roteiro de fala alinhado aos 31 slides da defesa."""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

SAIDA = r"C:\Users\adminsmart\Documents\TCC\TCC\apresentacao\Roteiro-Defesa-UTranscript.docx"

PRETO = RGBColor(0x14, 0x14, 0x14)
CINZA = RGBColor(0x3E, 0x48, 0x52)
OURO = RGBColor(0x8A, 0x6A, 0x00)


def fonte(run, tamanho=12, negrito=False, italico=False, cor=PRETO):
    run.font.name = "Calibri"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    run.font.size = Pt(tamanho)
    run.font.bold = negrito
    run.font.italic = italico
    run.font.color.rgb = cor


def paragrafo(doc, texto, tamanho=12, negrito=False, italico=False, cor=PRETO, espaco_depois=8, espaco_antes=0, alinhamento=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = alinhamento
    p.paragraph_format.space_after = Pt(espaco_depois)
    p.paragraph_format.space_before = Pt(espaco_antes)
    p.paragraph_format.line_spacing = 1.15
    trecho = p.add_run(texto)
    fonte(trecho, tamanho, negrito, italico, cor)
    return p


def titulo(doc, texto, nivel=1):
    h = doc.add_heading(texto, level=nivel)
    for trecho in h.runs:
        fonte(trecho, 18 if nivel == 1 else 13, True, False, PRETO if nivel == 1 else OURO)
    h.paragraph_format.space_before = Pt(0 if nivel == 1 else 12)
    h.paragraph_format.space_after = Pt(6)
    return h


def marcador(doc, texto):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.08
    p.clear()
    trecho = p.add_run(texto)
    fonte(trecho, 12, False, False, PRETO)
    return p


def quebra(doc):
    doc.add_page_break()


def rodape(section):
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    esquerda = p.add_run("Roteiro de defesa  ·  UTranscript")
    fonte(esquerda, 9, False, False, CINZA)
    direita = p.add_run("          ")
    fonte(direita, 9)
    campo_inicio = OxmlElement("w:fldChar")
    campo_inicio.set(qn("w:fldCharType"), "begin")
    instrucao = OxmlElement("w:instrText")
    instrucao.set(qn("xml:space"), "preserve")
    instrucao.text = " PAGE "
    campo_fim = OxmlElement("w:fldChar")
    campo_fim.set(qn("w:fldCharType"), "end")
    numero = p.add_run()
    fonte(numero, 9, False, False, CINZA)
    numero._r.append(campo_inicio)
    numero._r.append(instrucao)
    numero._r.append(campo_fim)


SLIDES = [
    {
        "secao": "Capa",
        "titulo": "UTranscript",
        "tela": [
            "Título, nome, orientador e coorientador.",
            "UTFPR, Ponta Grossa, 2026. Bacharelado em Ciência da Computação.",
            "Não há data de aprovação nem nomes da banca.",
        ],
        "fala": (
            "Bom dia. Meu nome é Eduardo Robinson Silveira Junior. Apresento o trabalho de conclusão de curso "
            "UTranscript, plataforma para transcrição e resumo de videoaulas, orientado pelo professor Vinícius "
            "Camargo Andrade e coorientado pelo professor Richard Duarte Ribeiro, no bacharelado em Ciência da "
            "Computação da UTFPR, em Ponta Grossa. A apresentação dura cerca de 25 minutos. Sigo a ordem do texto "
            "que a banca recebeu: o contexto, o problema, o que foi construído e como isso foi avaliado. No fim, "
            "fico à disposição para as perguntas."
        ),
    },
    {
        "secao": "Agenda",
        "titulo": "Agenda",
        "tela": [
            "Nove blocos: contexto, problema e questão, objetivos, conceitos, método, desenvolvimento, resultados, avaliação e conclusão.",
        ],
        "fala": (
            "O caminho é o do documento. Começo pelo cenário das videoaulas e pelas ferramentas que já transcrevem "
            "ou resumem, para deixar a lacuna explícita. Em seguida vêm a questão, os objetivos e os conceitos que "
            "preciso fixar antes de mostrar o sistema: o que é cada modelo, o que qualidade significa neste trabalho "
            "e como a arquitetura está organizada. Depois descrevo o método, o desenvolvimento e as telas. A parte "
            "em que peço mais atenção é a avaliação, porque é ela que sustenta a conclusão. Fecho retomando cada "
            "objetivo, com o limite do que foi medido."
        ),
    },
    {
        "secao": "Introdução",
        "titulo": "A videoaula virou material de estudo",
        "tela": [
            "Ensino remoto em 2020.",
            "Cerca de 140% a mais de canais de videoaula de ciências no YouTube (Souza e Vilela, 2021).",
            "Rever a aula e localizar um trecho continua custando tempo.",
        ],
        "fala": (
            "O ponto de partida é 2020. O distanciamento social tornou o ensino remoto a alternativa para continuar "
            "as aulas, do ensino básico ao superior. Nesse movimento, a videoaula deixou de ser só um complemento e "
            "passou a ser material de estudo. Souza e Vilela registram, nos primeiros meses de isolamento, um "
            "acréscimo de cerca de 140% na criação de canais de videoaulas de ciências no YouTube. O formato se "
            "consolidou e continua em uso. Para o estudante, o custo é prático: rever a aula inteira, ou achar o "
            "trecho em que o professor disse uma definição, consome o tempo que poderia estar no conteúdo. O "
            "material continua audiovisual. O que o trabalho busca é um meio de consumir essa aula em texto, em "
            "menos tempo."
        ),
        "perguntas": (
            "Souza e Vilela fizeram um levantamento de videoaulas de ciências para o ensino fundamental, no YouTube, "
            "comparando o isolamento com o período anterior. A pesquisa é transversal. O resultado que o TCC usa é "
            "específico: nos cinco primeiros meses de isolamento houve acréscimo de 140% na criação de canais com "
            "videoaulas de ciências, totalizando 42 canais. Não é um crescimento de 140% em todas as videoaulas da "
            "plataforma, nem uma medida de aprendizagem. O número entra só como evidência de que o YouTube se tornou "
            "veículo de conteúdo educacional nesse período."
        ),
    },
    {
        "secao": "Introdução",
        "titulo": "Três ferramentas, e o que falta nelas",
        "tela": [
            "YouTube: legendas e “Resuma o vídeo”, sem ficha acadêmica, sem transcrição editável e sem PDF ligado a essa ficha.",
            "Otter.ai: ata de reunião, plano pago, sem Libras.",
            "Notta: serviço tarifado, sem metadados de disciplina e sem Libras.",
        ],
        "fala": (
            "A transcrição automática já existe. Comparo três produtos difundidos para mostrar o que falta. As "
            "legendas do YouTube transcrevem o vídeo no player, em geral sem custo extra para quem assiste, e o "
            "recurso Resuma o vídeo produz uma síntese ali mesmo. Nenhum dos dois organiza a aula por universidade, "
            "curso e tema, guarda uma transcrição que o autor edita, nem gera um PDF ligado a essa ficha. O Otter.ai "
            "transcreve e resume, mas o produto é uma ata de reunião. O uso contínuo depende de plano pago, e não há "
            "opção de obter o texto em Libras. O Notta oferece transcrição e resumo como serviço hospedado e "
            "tarifado, sem os metadados de uma disciplina e sem Libras. O próximo slide é o que este trabalho "
            "acrescenta em relação a elas."
        ),
    },
    {
        "secao": "Problema de pesquisa",
        "titulo": "A lacuna não é inventar a transcrição",
        "tela": [
            "Ficha da videoaula por universidade, curso e tema.",
            "Transcrição editável.",
            "Resumo em PDF.",
            "VLibras sobre o texto. O custo da inferência fica na infraestrutura.",
        ],
        "fala": (
            "A contribuição é reunir, numa aplicação própria e com modelos de pesos abertos, quatro coisas que "
            "essas ferramentas deixam separadas. A primeira é a ficha da videoaula: universidade, curso e tema no "
            "mesmo registro da mídia. A segunda é a transcrição editável, para o autor corrigir o que o modelo "
            "errou. A terceira é o resumo em PDF, ligado a essa ficha. A quarta é o acionamento do VLibras sobre o "
            "texto, quando o usuário quer esse formato. Os modelos são o Distil-Whisper large-v3 e o Llama 3.1 8B "
            "Instruct. O custo da inferência fica na infraestrutura de quem opera o sistema."
        ),
    },
    {
        "secao": "Questão de pesquisa",
        "titulo": "A pergunta que orienta o trabalho",
        "tela": [
            "Como oferecer aos estudantes um meio de consumir videoaulas em menos tempo, com o conteúdo em texto, num contexto em que o material audiovisual continua amplamente usado?",
            "A formulação é a do capítulo 1.",
        ],
        "fala": (
            "A pergunta que orienta o capítulo 1 é esta: como oferecer aos estudantes um meio de consumir videoaulas "
            "em menos tempo, com o conteúdo em texto, num contexto em que o material audiovisual continua "
            "amplamente usado? A resposta que o trabalho constrói é a plataforma UTranscript. Os objetivos dizem o "
            "que essa resposta precisava entregar, e a avaliação diz o que de fato foi observado."
        ),
    },
    {
        "secao": "Objetivos",
        "titulo": "O que se pretendia alcançar",
        "tela": [
            "Geral: aplicação web, em microsserviços, para transcrever e resumir videoaulas.",
            "Interface de envio e de consulta.",
            "ASR com Distil-Whisper large-v3.",
            "Resumo com Llama 3.1.",
            "Avaliação qualitativa da qualidade e da fidelidade.",
        ],
        "fala": (
            "O objetivo geral é criar uma aplicação web, em arquitetura de microsserviços, capaz de transcrever e "
            "resumir videoaulas. Há quatro objetivos específicos, e a conclusão volta a eles nesta ordem. O primeiro "
            "é a interface: enviar a videoaula e ver a transcrição e o resumo de forma estruturada. O segundo é o "
            "reconhecimento de fala com o Distil-Whisper large-v3. O terceiro é o resumo, processando o texto "
            "transcrito com o Llama 3.1. O quarto é avaliar a qualidade e a fidelidade dos resumos por leitura "
            "técnica, comparando o texto sintetizado com a aula. Esse quarto objetivo é o que fecha o trabalho. "
            "Sem ele, o sistema estaria descrito, mas não examinado."
        ),
    },
    {
        "secao": "Conceitos",
        "titulo": "Dois modelos, papéis diferentes",
        "tela": [
            "Modelo de fala: Distil-Whisper large-v3. Motor: faster-whisper sobre CTranslate2.",
            "Modelo de resumo: Llama 3.1 8B Instruct, em 4 bits (NF4) na GPU.",
            "O Llama lê a transcrição. Ele não ouve o áudio.",
        ],
        "fala": (
            "Aqui separo modelo e motor. O modelo de fala é o Distil-Whisper large-v3, um encoder-decoder na linha "
            "destilada do Whisper. Quem o executa neste sistema é outra peça: a biblioteca faster-whisper, sobre o "
            "CTranslate2, com compute_type int8_float16, na GPU, em português. O modelo de resumo é o Llama 3.1 8B "
            "Instruct, da Meta, com 8 bilhões de parâmetros e ajuste para seguir instrução. Ele não ouve o áudio. "
            "Ele lê a transcrição que entrou no prompt. Na placa de 8 GB, esse Llama roda em 4 bits, no formato NF4."
        ),
        "perguntas": (
            "Gandhi, von Werra e Wolf (2023) descrevem a destilação do Whisper por pseudo-rotulagem em larga escala. "
            "No artigo, o modelo destilado fica cerca de 1 ponto percentual de WER do modelo professor, em testes de "
            "inglês fora da distribuição de treino, com cerca de 5,8 vezes mais velocidade e 51% menos parâmetros. "
            "Esse número é do artigo. Não é uma medição do UTranscript. Este trabalho não calculou WER. A escolha do "
            "distil-large-v3, executado pela faster-whisper, segue o que o TCC descreve: manter o reconhecimento com "
            "menos tempo e menos memória de vídeo do que o Whisper large original. A faster-whisper é o motor "
            "adotado aqui. O artigo não é o manual desse motor.\n\n"
            "Dubey e colegas (2024), em The Llama 3 Herd of Models, apresentam a família com versões de 8, 70 e 405 "
            "bilhões de parâmetros. O pós-treino ajusta o modelo para seguir instrução. A versão usada aqui é a "
            "Llama 3.1 8B Instruct. O artigo descreve janela de contexto longa na família, de até 128 mil tokens no "
            "modelo maior. Neste sistema, a geração do resumo está limitada a 1024 tokens novos, por restrição da "
            "máquina. Não afirmo que a janela inteira do modelo foi usada."
        ),
    },
    {
        "secao": "Conceitos",
        "titulo": "O que “qualidade” significa neste trabalho",
        "tela": [
            "Fidelidade, cobertura, omissão, informação inventada, erro factual e organização.",
            "O juiz avalia o resumo comum e o personalizado, com nota absoluta de um único texto (Zheng et al., 2023; Liu et al., 2023).",
        ],
        "fala": (
            "Estes seis termos voltam na avaliação. Fidelidade significa o texto não inventar fala nem conceito "
            "ausente da aula e não distorcer o que foi dito. Cobertura significa os tópicos centrais aparecerem no "
            "resumo. Omissão é tópico importante que ficou de fora. Informação inventada é frase do resumo ou da "
            "transcrição que não está no vídeo. Erro factual é informação reconhecível, porém trocada. Organização "
            "é o resumo em tópicos legíveis, sem mistura de assuntos. O juiz automático avalia o resumo comum e o "
            "personalizado. Ele lê o prompt que foi usado na geração e o texto produzido, e dá uma nota absoluta a "
            "um único texto, sem escolher entre dois resumos. Zheng e "
            "colegas chamam esse procedimento de avaliação de resposta única. Liu e colegas usam o mesmo tipo de "
            "nota na sumarização, no G-Eval: o avaliador preenche critérios de um resumo isolado, sem um resumo de "
            "referência."
        ),
        "perguntas": (
            "Zheng e colegas (2023) separam a comparação par a par da nota absoluta. Na comparação par a par, o "
            "juiz escolhe entre duas respostas e pode inverter o julgamento só porque a ordem mudou. É o viés de "
            "posição. A nota absoluta é mais simples de aplicar a cada saída, mas oscila mais quando o modelo juiz "
            "muda. O artigo também descreve viés de verbosidade e a tendência de um juiz favorecer saídas do próprio "
            "modelo. O acordo acima de 80% com humanos, nesse artigo, foi obtido com um juiz forte, o GPT-4. Esse "
            "percentual não é resultado do UTranscript.\n\n"
            "Liu e colegas (2023), no G-Eval, usam um modelo de linguagem para preencher uma ficha de qualidade de "
            "um texto gerado, sem referência humana. No artigo, com GPT-4, a correlação de Spearman com humanos na "
            "sumarização foi de 0,514. Esse 0,514 é do artigo, com outro modelo. O juiz deste trabalho é o "
            "Qwen3-0.6B. Uso o G-Eval para nomear o procedimento: a nota de um resumo sozinho."
        ),
    },
    {
        "secao": "Conceitos",
        "titulo": "Três processos, não três camadas",
        "tela": [
            "Não é arquitetura em camadas.",
            "Interface, Spring Boot e microsserviço Python.",
            "Processo com deploy próprio (Newman, 2021).",
            "VLibras: avatar sobre o texto.",
            "Sem teste com usuários de Libras.",
        ],
        "fala": (
            "O que foi construído é uma interface web, uma aplicação Spring Boot e um microsserviço Python. O "
            "Spring concentra regra de negócio, autenticação e persistência. O processo Python existe para a "
            "inferência, com deploy próprio. Newman trata o microsserviço como processo independente, e é nesse "
            "sentido que a palavra aparece no trabalho. O VLibras entra como opção: o usuário aciona um avatar "
            "sobre o texto. Não houve teste com usuários de Libras. A opção existe na interface. O efeito sobre a "
            "aprendizagem não foi medido. Exportar um vídeo de Libras, fora do avatar, ficou como trabalho futuro."
        ),
        "perguntas": (
            "Se a pergunta for sobre arquitetura em camadas, a resposta cabe em uma frase. Camadas, na discussão do "
            "TCC, são apresentação, lógica e dados. Aqui a separação que importa é de processo: a interface, o "
            "Spring e o FastAPI sobem separados. O banco fica com o Spring. A GPU fica com o Python. Não resumo o "
            "livro de Newman além dessa definição, que é a usada no texto."
        ),
    },
    {
        "secao": "Método",
        "titulo": "Como o trabalho foi conduzido",
        "tela": [
            "Origem: transcritor de atas de reunião.",
            "Oito requisitos funcionais e seis não funcionais.",
            "Kanban no Trello, de julho a outubro de 2025.",
            "Exame: leitura do autor e nota do juiz, no resumo comum e no personalizado.",
        ],
        "fala": (
            "O método é o caminho do desenvolvimento. A ferramenta nasceu de um transcritor de atas de reunião. "
            "Essa experiência mostrou o uso da transcrição no estudo, e o escopo passou a ser a videoaula, com o "
            "texto e a opção de Libras pelo VLibras. Daí vieram oito requisitos funcionais, do cadastro à exclusão, "
            "e seis não funcionais, entre segurança, usabilidade, portabilidade, Libras e uma meta de tempo que "
            "depois não foi usada como critério. A construção foi iterativa, num quadro Kanban no Trello, de julho "
            "a outubro de 2025. O exame do que foi construído é o capítulo 4. O juiz automático nota o resumo comum, "
            "quando o campo de prompt fica vazio, e também o personalizado."
        ),
    },
    {
        "secao": "Método",
        "titulo": "Como a solução foi examinada",
        "tela": [
            "Avaliador: o autor. Sem segundo avaliador.",
            "Compara o trecho da aula com o PDF. A transcrição é julgada pelo resumo.",
            "O Qwen3-0.6B nota o resumo comum e o personalizado, em quatro notas de 0 a 1.",
            "O tempo foi medido e não é o critério de qualidade.",
        ],
        "fala": (
            "A avaliação principal é qualitativa e foi feita por mim. Eu assisto ao trecho da videoaula e leio o "
            "PDF. Não há segundo avaliador humano, então não há procedimento de divergência entre pessoas. Esse é "
            "um limite, e eu o assumo na conclusão. A transcrição não foi comparada a um texto de referência palavra "
            "por palavra. Ela entra no prompt do resumo. Quando o resumo traz a informação certa da aula, a "
            "transcrição levou esse conteúdo ao modelo. O Qwen3 de 0,6 bilhão de parâmetros lê o prompt gravado na "
            "transcrição, comum ou personalizado, e o resultado, e devolve quatro notas de 0 a 1: adesão, fidelidade, cobertura e "
            "organização, mais uma justificativa curta. O tempo de processamento foi medido no Docker. Ele não é o "
            "critério de qualidade, porque a placa do ensaio é uma placa de jogos."
        ),
    },
    {
        "secao": "Desenvolvimento",
        "titulo": "A solução em três processos",
        "tela": [
            "Ionic 8, Angular 19 e TypeScript.",
            "Spring Boot, JWT em cookie HttpOnly, PostgreSQL 15.",
            "FastAPI em Python 3.10, na GPU.",
            "Edição e exclusão só do autor, no serviço.",
        ],
        "fala": (
            "Na prática são três processos. A interface é Ionic 8 com Angular 19 e TypeScript. Ela cuida do "
            "formulário, das rotas e do que a sessão mostra. O Spring Boot autentica com JWT num cookie HttpOnly, "
            "aplica a regra de autoria e persiste no PostgreSQL 15, via JPA. O FastAPI, em Python 3.10, recebe o "
            "áudio e roda os modelos na GPU. A conversa entre os três é REST, em JSON. O arquivo vai em multipart. "
            "Editar ou excluir uma videoaula só se efetiva se o usuário do token for o autor do registro. Essa "
            "checagem está no serviço. Esconder o botão na tela não substitui a autorização."
        ),
    },
    {
        "secao": "Desenvolvimento",
        "titulo": "O processamento não trava a interface",
        "tela": [
            "Somente o diagrama de sequência. A explicação do fluxo fica na fala.",
        ],
        "fala": (
            "Este é o diagrama de sequência do trabalho. O usuário pede a transcrição. O Spring grava a aula com "
            "status Em andamento e responde na hora, para a tela não ficar presa. Em paralelo, envia o áudio ao "
            "FastAPI. O FastAPI confirma o recebimento e, noutra thread, chama o Distil-Whisper e depois o Llama "
            "3.1. No fim, faz um PUT no Spring com a transcrição, o resumo e o status Concluída. Se a thread falha, "
            "o mesmo caminho grava Com erro. O PDF não nasce nessa thread. Ele é montado quando o usuário pede a "
            "exportação. O ensaio de desempenho mostrou o mesmo: a exportação ocorreu depois e não entrou nos 10 "
            "minutos e 27 segundos."
        ),
    },
    {
        "secao": "Desenvolvimento",
        "titulo": "A videoaula fica numa ficha",
        "tela": [
            "Somente a figura da ficha e dos casos de uso. A leitura do diagrama fica na fala.",
        ],
        "fala": (
            "O banco guarda a ficha. O usuário se vincula a uma universidade e a um curso. O tema pertence a um "
            "curso. A videoaula guarda título, data, professor e o autor. Cada videoaula tem uma transcrição. No "
            "diagrama, só aparece o que o usuário faz diretamente. Criar a transcrição sempre inclui processar. "
            "Baixar pode ser o vídeo inteiro ou só o áudio. A exclusão não aparece como caso de uso próprio porque "
            "segue a mesma regra de autoria da edição. A transcrição automática e o PDF também acontecem dentro do "
            "processamento, e por isso não são casos de uso separados."
        ),
    },
    {
        "secao": "Desenvolvimento",
        "titulo": "Resumo comum ou extração pedida",
        "tela": [
            "Campo vazio: resumo acadêmico. Exercício pede enunciado, passos e resultado.",
            "Resolução complementar, marcada como elaborada pelo sistema, quando a fala não fecha o exercício.",
            "Campo preenchido: a instrução vale antes da inferência. A tela mostra o pedido do segundo exercício.",
        ],
        "fala": (
            "No cadastro há um campo opcional de prompt. Se fica vazio, vale o resumo acadêmico. A instrução pede, "
            "para cada tema central, o conceito e o exemplo e, quando há exercício, enunciado, passos e resultado. "
            "Se o professor enunciou um exercício e não o resolveu, ou se a fala da resolução ficou ilegível, o "
            "sistema pode completar numa subseção chamada Resolução complementar, marcada como elaborada pelo "
            "sistema. Fora desses exercícios, a instrução proíbe acrescentar o que não está na transcrição. Se o "
            "campo vem preenchido, como nesta tela, o modelo extrai o que a instrução pediu. Neste exemplo, só o "
            "segundo exercício da aula de derivada."
        ),
    },
    {
        "secao": "Desenvolvimento",
        "titulo": "O que cada modelo executa",
        "tela": [
            "Distil-Whisper large-v3: GPU, int8_float16, português, faster-whisper.",
            "Llama 3.1 8B Instruct: 4 bits, no máximo 1024 tokens novos.",
            "Qwen3-0.6B: juiz do resumo comum e do personalizado. A variante de 8B não coube junto dos outros dois.",
        ],
        "fala": (
            "Três fatos de execução. O Whisper em uso é o distil-large-v3, na GPU, com compute_type int8_float16 e "
            "idioma português, pela faster-whisper. O Llama 3.1 8B Instruct gera no máximo 1024 tokens novos. Esse "
            "teto corta a resposta final de vários exercícios, e isso aparece na avaliação. O juiz é o Qwen3 de "
            "0,6 bilhão, não o de 8. Na RTX 4060 Ti, o Llama em 4 bits e o Whisper já ocupam a memória de vídeo, e "
            "o Qwen de 8 bilhões não permanece carregado junto deles. Ele avalia o resumo comum e o personalizado: "
            "recebe o prompt gravado na transcrição e o texto gerado. O juiz não reescreve o resumo. Ele devolve as "
            "quatro notas."
        ),
        "perguntas": (
            "O TCC cita Yang e colegas (2025) para o ajuste enable_thinking desligado. Com esse ajuste, o Qwen3 não "
            "devolve o bloco de raciocínio, e a saída fica nas notas pedidas. Senthil Kumar (2026), no mesmo "
            "modelo, observa que o modo de raciocínio piora o cumprimento de formato: a restrição de forma exata "
            "sofre quando a resposta fica mais longa. Por isso a execução deixa o pensamento desligado. A variante "
            "de 0,6 bilhão foi a que coube na placa junto dos outros dois modelos. Não apresento o Qwen3-0.6B como "
            "um juiz da mesma classe do GPT-4 usado nos artigos de Zheng e de Liu."
        ),
    },
    {
        "secao": "Desenvolvimento",
        "titulo": "O ensaio subiu em quatro containers",
        "tela": [
            "db-tcc: PostgreSQL 15.",
            "backend-spring na porta 8080.",
            "frontend-angular na porta 4200.",
            "ai-python na porta 5000, com a RTX 4060 Ti (8188 MiB).",
            "O protótipo não ficou no ar 24 horas.",
        ],
        "fala": (
            "O ensaio de desempenho não instalou os processos direto no sistema operacional. O Docker Compose sobe "
            "quatro containers. O db-tcc é o PostgreSQL 15. O backend-spring é a API na porta 8080. O "
            "frontend-angular é a interface na porta 4200. O ai-python, na porta 5000, reserva uma GPU, a NVIDIA "
            "GeForce RTX 4060 Ti, com 8188 MiB. Nesse container estão o Distil-Whisper e o Llama. O protótipo rodou "
            "nessa máquina. Não ficou acessível 24 horas por dia. O requisito de disponibilidade contínua não foi "
            "obtido."
        ),
    },
    {
        "secao": "Resultados",
        "titulo": "Da conta à ficha da aula",
        "tela": [
            "Duas telas, sem legenda: cadastro da conta e nova videoaula.",
            "Universidade, curso, professor, tema, prompt opcional e arquivo são ditos na fala.",
        ],
        "fala": (
            "A partir daqui o sistema aparece em uso, com telas do manual. No cadastro, a conta já pede "
            "universidade e curso. A ficha acadêmica começa aí. Na criação da videoaula, os mesmos metadados "
            "reaparecem: título, universidade, curso, professor e tema, mais o arquivo. O campo de prompt "
            "personalizado está na mesma tela. Vazio, a extração é a comum. O envio dispara o fluxo assíncrono do "
            "diagrama. Há também o caminho pelo YouTube, que mostro daqui a dois slides."
        ),
    },
    {
        "secao": "Resultados",
        "titulo": "Consulta, texto e PDF",
        "tela": [
            "Consulta por título, tema, universidade e curso, com status Concluído.",
            "Detalhe da videoaula, texto gerado, botão de PDF e ícone do VLibras.",
        ],
        "fala": (
            "À esquerda, a consulta filtra por título, tema, universidade e curso, e mostra o status Concluído. À "
            "direita, o detalhe da videoaula: a ficha, o texto gerado e o botão de exportar para PDF. O ícone azul "
            "é o acionamento do VLibras sobre esse texto. Quem é o autor edita. Quem não é, não conclui a alteração "
            "no serviço. O resultado observável do primeiro objetivo é este fluxo: criar a conta, enviar a mídia, "
            "acompanhar o status e baixar o PDF."
        ),
    },
    {
        "secao": "Resultados",
        "titulo": "Vídeo de origem e texto em Libras",
        "tela": [
            "Tela para colar a URL do YouTube e baixar o vídeo.",
            "Avatar do VLibras.",
            "A legenda do slide lembra que não houve avaliação com usuários.",
        ],
        "fala": (
            "Duas funções completam o uso. O download parte de uma URL do YouTube e obtém a mídia para o fluxo de "
            "transcrição, ou para o usuário guardar o arquivo. O VLibras é o widget oficial, acionado na tela do "
            "texto. O avatar apresenta em Libras o que está escrito. Isso cumpre o requisito de oferecer a opção. "
            "Não é evidência de que a tradução foi adequada para um usuário de Libras, porque esse teste não foi "
            "feito."
        ),
    },
    {
        "secao": "Avaliação",
        "titulo": "Quem avaliou e com quais critérios",
        "tela": [
            "Avaliador: o autor. Procedimento: assistir ao trecho e ler o PDF.",
            "Os seis critérios, em cartões.",
            "Aulas nas figuras: limites, Dijkstra e três prompts personalizados.",
        ],
        "fala": (
            "O avaliador sou eu. Não há segunda pessoa, e isso limita o quanto a leitura pode ser generalizada. O "
            "procedimento é assistir ao trecho e ler o PDF, com os critérios já definidos. A transcrição é "
            "conferida pelo que o resumo extraiu dela. As aulas desta leitura foram escolhidas porque o resumo, o "
            "trecho ou a nota do juiz aparecem nas figuras do trabalho. A aula de limites é uma resolução de "
            "exercício. A do algoritmo de Dijkstra é explicativa, sem exercício resolvido. Os prompts "
            "personalizados cobrem o exercício 5 de grafos, um segundo exercício de derivada e a aula de análise "
            "sintática."
        ),
    },
    {
        "secao": "Avaliação",
        "titulo": "Exercício e aula explicativa",
        "tela": [
            "Resumo da aula de limites: a explicação e o encaminhamento saem em texto. O valor do limite, não.",
            "Resumo de Dijkstra: o texto segue o roteiro e perde o encadeamento da fala.",
        ],
        "fala": (
            "O mesmo procedimento dá resultados desiguais, e essa diferença é o achado central. Na videoaula de "
            "limites, que é resolução de exercício, o resumo descreve a explicação e o encaminhamento: conjugados, "
            "potenciação, o passo. O funcionamento favorece esse tipo de aula. O valor numérico do limite não entra, "
            "e o próximo slide explica por quê. Na aula do algoritmo de Dijkstra, que é explicativa, o modelo extrai "
            "informações, mas o texto perde o encadeamento que a fala constrói. A cobertura dos tópicos centrais "
            "fica mais pobre. O que permanece saiu da transcrição, então o conteúdo certo ainda indica que a "
            "transcrição levou a aula ao modelo. A perda de encadeamento não é falha de envio do arquivo. No "
            "Dijkstra, a sugestão final de otimizar a implementação é o trecho que sai do roteiro da aula, e ela não "
            "desenvolve o critério do algoritmo."
        ),
        "perguntas": (
            "No resumo do exercício, a explicação dos conjugados vai além da paráfrase da transcrição. Maynez e "
            "colegas (2020) chamam de extrínseco o conteúdo que não se infere da fonte. O artigo, com avaliação "
            "humana, mostra que resumos abstrativos produzem conteúdo infiel ao documento de origem com frequência. "
            "Cao, Dong e Cheung (2022) observam que parte desse acréscimo permanece consistente com o conhecimento "
            "de mundo, e que esse apoio pode ser útil quando não distorce o assunto. É nesse sentido que o TCC lê a "
            "explicação da técnica de conjugados.\n\n"
            "No Dijkstra, o texto se mantém no roteiro da aula. O TCC associa isso à consistência factual discutida "
            "por Fabbri e colegas (2021), que reavaliaram métricas automáticas de resumo contra julgamentos humanos. "
            "A sugestão final de otimização é o ponto que deixa esse roteiro."
        ),
    },
    {
        "secao": "Avaliação",
        "titulo": "O teto de 1024 tokens",
        "tela": [
            "Teto de 1024 tokens novos.",
            "O procedimento ocupa o espaço; a resposta final fica de fora.",
            "Gemini: quatro exercícios e os intervalos.",
            "Os dois deixam a álgebra sem fechar.",
            "Gemini marca os tempos; o UTranscript explica o conjugado.",
            "Figura do resumo do YouTube.",
        ],
        "fala": (
            "O teto de 1024 tokens novos explica uma parte do que se vê no resumo de exercício. O modelo ocupa os "
            "tokens com a técnica e o passo, e muitas vezes não sobra espaço para o resultado. Na mesma aula de "
            "limites, o recurso Resuma o vídeo do YouTube, operado pelo Gemini, organizou a aula em quatro "
            "exercícios, com o intervalo de cada um: raiz cúbica, conjugado, limites laterais e o limite com a "
            "variável h. Esse texto também não traz a resolução algébrica fechada. A diferença está no recorte. O "
            "Gemini lista os exercícios e deixa a explicação do conjugado para uma pergunta seguinte. No "
            "UTranscript, a instrução pede o conceito no próprio resumo, e o conjugado já sai escrito. O valor do "
            "limite é que fica de fora, pelo teto."
        ),
    },
    {
        "secao": "Avaliação",
        "titulo": "A nota do juiz",
        "tela": [
            "O mesmo juiz também avalia o resumo comum. As notas da tela são de prompts personalizados.",
            "Grafos, exercício 5 (Maioli, 2020): nota 0,8875. Adesão 0,85, fidelidade 0,95, cobertura 0,9, organização 0,85.",
            "A leitura do autor: a tabela não cobre a árvore inteira e chama a árvore de arbusto.",
            "Análise Sintática Parte 2 (Lins, 2012): nota 0,965. Adesão 0,95, fidelidade 0,98, cobertura 0,97, organização 0,96.",
            "A tela à direita mostra a nota 0,8875.",
        ],
        "fala": (
            "O Qwen avalia os dois resumos. O Spring envia o prompt gravado na transcrição, comum ou personalizado, "
            "junto com o texto gerado. As notas desta tela são de prompts personalizados. Neles, a referência da "
            "leitura é a instrução, não a aula inteira. Na videoaula de "
            "dez exercícios de grafos, de Maioli, o pedido foi só o exercício 5. O juiz deu nota 0,8875: adesão "
            "0,85, fidelidade 0,95, cobertura 0,9 e organização 0,85. A minha leitura discorda do elogio da "
            "justificativa. A tabela não cobre a árvore do slide. Ficam de fora o nó de subtração e folhas, e o "
            "texto chama a árvore de arbusto. A nota alta não apaga essa omissão. Na aula de Análise Sintática Parte "
            "2, de Lins, o prompt pedia o que o professor comentou sobre a análise top-down. A nota foi 0,965, com "
            "adesão 0,95, fidelidade 0,98, cobertura 0,97 e organização 0,96. O juiz é complemento. A leitura de "
            "conteúdo continua sendo a minha."
        ),
        "perguntas": (
            "Zheng e colegas alertam que a nota absoluta oscila mais quando o modelo juiz muda, e que um juiz tende "
            "a favorecer texto do próprio modelo. Neste ensaio, quem escreveu o resumo foi o Llama, e quem julgou "
            "foi o Qwen3. Não há um segundo candidato na consulta. Isso afasta o caso em que o juiz compara uma "
            "saída sua com a de outro modelo, e não transforma o Qwen3-0.6B num avaliador da classe do GPT-4 do "
            "artigo. A discordância no exercício de grafos é o exemplo concreto: a nota e a justificativa elogiam a "
            "tabela, e a leitura do autor encontra omissão. Por isso a nota do juiz não substitui a leitura."
        ),
    },
    {
        "secao": "Avaliação",
        "titulo": "O tempo foi medido, e não é o critério",
        "tela": [
            "Aula de notação assintótica, 30 minutos, 42 MB, 29 de setembro de 2026.",
            "Transcrição: 9 min 3 s. Resumo: 1 min 24 s. Total: 10 min 27 s, sem o PDF.",
            "Gráfico de CPU, sem legenda. O pico e o bloco contínuo são ditos na fala.",
            "Tópico: memória de vídeo em cerca de 7,8 GiB de 8,2 GiB, com os modelos carregados.",
        ],
        "fala": (
            "Este slide é um registro de desempenho. A aula é a de notação assintótica, resolução de exercícios, "
            "com 30 minutos e 42 MB, medida em 29 de setembro de 2026. As outras aulas deste parâmetro tinham entre "
            "10 e 20 minutos e ficaram na mesma faixa, com o hardware fixo. No gráfico, o pico isolado perto de "
            "15:29 é o download do YouTube. O bloco das 15:34 às 15:44 é a transcrição seguida do resumo. Pelos "
            "logs, o Distil-Whisper levou 9 minutos e 3 segundos, e o Llama, 1 minuto e 24 segundos. O total é 10 "
            "minutos e 27 segundos. A exportação do PDF foi pedida depois e não entra nesse total. A memória de "
            "vídeo ficou em cerca de 7,8 GiB de 8,2 GiB mesmo depois da CPU cair, porque os modelos continuam "
            "carregados. A utilização da GPU no minuto final do resumo ficou entre 35% e 36%."
        ),
        "perguntas": (
            "Almeida (2025) mede inferência de modelos de linguagem, de 1,5 a 70 bilhões de parâmetros, numa RTX "
            "4090 e numa H100. O TCC usa o resultado assim: a H100 chega a 1,5 vez a vazão da placa de consumo, com "
            "latência de cauda abaixo de 55 ms, e quatro RTX 4090 entregam de 62% a 78% da vazão da H100. A relação "
            "se mantém nesse intervalo de modelos, e a sumarização em lote é uma das cargas que o artigo atribui à "
            "placa de jogos. A placa deste ensaio é uma RTX 4060 Ti, de 8 GB, a mesma em todas as aulas. Por isso o "
            "tempo permanece na mesma faixa e não é tratado como critério de qualidade. O critério é o resumo. A "
            "meta de elicitação, arquivos de até 500 MB em menos de 15 minutos, não foi o parâmetro desta avaliação. "
            "O arquivo medido tem 42 MB."
        ),
    },
    {
        "secao": "Conclusão",
        "titulo": "O que cada objetivo alcançou",
        "tela": [
            "Geral: a aplicação foi implementada.",
            "Interface: conta, envio, detalhe, busca e PDF.",
            "Fala: Distil-Whisper large-v3, conferido pelo que o resumo extrai.",
            "Resumo: exercício preserva o encaminhamento; aula explicativa perde desenvolvimento.",
            "Qualidade: o funcionamento favorece a resolução de exercício.",
        ],
        "fala": (
            "Retomo os objetivos na ordem do texto. O geral foi alcançado: a aplicação existe, com interface, "
            "Spring Boot e microsserviço Python, e transcreve e resume a videoaula. A interface cumpre o fluxo de "
            "conta, envio, consulta e PDF. O reconhecimento de fala está em execução com o Distil-Whisper large-v3, "
            "pela faster-whisper, em português, na GPU. A evidência dele é o que o resumo extrai da transcrição. O "
            "Llama 3.1 8B Instruct produz o resumo, e o resultado depende do tipo de aula. No exercício, a "
            "explicação e o encaminhamento saem em texto. Na aula explicativa, o desenvolvimento se perde. O quarto "
            "objetivo fecha assim: a leitura favorece a resolução de exercício. O mesmo procedimento, na aula "
            "explicativa, perde encadeamento."
        ),
    },
    {
        "secao": "Conclusão",
        "titulo": "Contribuição e limites",
        "tela": [
            "Contribuição: ficha, transcrição editável, PDF e VLibras, com modelos de pesos abertos.",
            "Limites: um avaliador; transcrição conferida pelo resumo; teto de 1024 tokens; aula explicativa; protótipo local.",
        ],
        "fala": (
            "A contribuição é reunir a ficha acadêmica, a transcrição editável, o PDF e a opção de VLibras, com "
            "modelos de pesos abertos, e com o custo da inferência na infraestrutura de quem opera o sistema. Os "
            "limites são os que a avaliação sustentou. Só eu li as aulas. A transcrição não foi medida contra uma "
            "referência. O teto de 1024 tokens corta respostas. A aula explicativa perde encadeamento. O protótipo "
            "rodou na máquina local, com GPU, e o requisito de disponibilidade contínua não foi obtido. Para quem "
            "acessa, a interface é web: o cadastro, o envio, a consulta e o download foram feitos pelo navegador, e "
            "a inferência ficou no servidor."
        ),
    },
    {
        "secao": "Conclusão",
        "titulo": "O que permanece em aberto",
        "tela": [
            "Vídeo de Libras fora do avatar.",
            "Instância de GPU e implantação contínua, pendentes no Kanban.",
            "O tempo só mudaria de classe num ambiente de processamento.",
        ],
        "fala": (
            "Três continuidades já estão escritas no trabalho. A primeira é um módulo que gere vídeo de Libras a "
            "partir do texto, para o estudante usar esse formato fora do avatar, inclusive offline ou em outro "
            "contexto. A segunda é de infraestrutura: a escolha da instância de GPU e a implantação contínua "
            "ficaram pendentes no Kanban. A terceira é sobre o tempo. Ele se manteve na mesma faixa porque o "
            "hardware não mudou, e esse hardware não é o acelerador indicado para a inferência. O tempo só mudaria "
            "de classe num ambiente de processamento."
        ),
    },
    {
        "secao": "Referências",
        "titulo": "Fontes citadas nesta apresentação",
        "tela": [
            "Souza e Vilela (2021); YouTube, Otter.ai e Notta (2026).",
            "Gandhi, von Werra e Wolf (2023); Newman (2021).",
            "Zheng et al. (2023); Liu et al. (2023); Almeida (2025).",
            "Maioli (2020); Lins (2012); VLibras.",
        ],
        "fala": (
            "Estas são as fontes que apareceram nos slides. A lista completa está no trabalho escrito. Se a banca "
            "pedir o detalhe de uma delas, eu recupero na arguição, separando o que o artigo mediu do que este TCC "
            "mediu. Os blocos “Se perguntarem” deste roteiro já deixam essa separação pronta para Distil-Whisper, "
            "Llama, juiz automático, alucinação de resumo e placa de consumo."
        ),
    },
    {
        "secao": "Encerramento",
        "titulo": "Obrigado",
        "tela": [
            "Nome, e-mail eduardorobinson@alunos.utfpr.edu.br e o curso.",
            "A frase de abertura da arguição: fico à disposição da banca.",
        ],
        "fala": (
            "Encerro por aqui. Obrigado pelo tempo. Fico à disposição da banca."
        ),
    },
]


def configurar(doc):
    secao = doc.sections[0]
    secao.page_width = Cm(21.0)
    secao.page_height = Cm(29.7)
    secao.left_margin = Cm(2.0)
    secao.right_margin = Cm(2.0)
    secao.top_margin = Cm(1.8)
    secao.bottom_margin = Cm(1.8)
    secao.header_distance = Cm(0.6)
    secao.footer_distance = Cm(0.6)
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(12)
    normal.font.color.rgb = PRETO
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    rodape(secao)
    propriedades = doc.core_properties
    propriedades.title = "Roteiro de fala — UTranscript"
    propriedades.author = "Eduardo Robinson Silveira Junior"
    propriedades.subject = "Defesa de TCC, alinhada aos 31 slides"
    propriedades.category = "Defesa"


def capa(doc):
    paragrafo(doc, "UTFPR  ·  PONTA GROSSA  ·  2026", 12, True, False, OURO, espaco_depois=12)
    paragrafo(doc, "Roteiro de fala", 28, True, False, PRETO, espaco_depois=2)
    paragrafo(doc, "UTranscript: plataforma para transcrição e resumo de videoaulas", 16, False, False, CINZA, espaco_depois=12)
    paragrafo(doc, "Eduardo Robinson Silveira Junior", 14, True, False, PRETO, espaco_depois=2)
    paragrafo(doc, "Orientador: Prof. Dr. Vinícius Camargo Andrade", 12, False, False, CINZA, espaco_depois=0)
    paragrafo(doc, "Coorientador: Prof. Dr. Richard Duarte Ribeiro", 12, False, False, CINZA, espaco_depois=14)
    paragrafo(doc, "Como usar este documento", 16, True, False, PRETO, espaco_depois=6)
    paragrafo(
        doc,
        "Cada bloco abaixo corresponde a um slide de Defesa-UTranscript.pptx, na mesma ordem. "
        "Fale o texto de “Fala” olhando para a plateia e para a figura. Não leia o que está projetado. "
        "O conjunto das falas foi escrito para cerca de 25 minutos. O bloco “Se perguntarem” fica para a arguição. "
        "Quando esse bloco cita um número de artigo, o número é do artigo. Não é uma medição do UTranscript, "
        "salvo quando a frase diz que o dado veio do ensaio ou do capítulo 4.",
        espaco_depois=8,
    )
    paragrafo(doc, "Sugestão de tempo", 14, True, False, PRETO, espaco_antes=6, espaco_depois=4)
    for linha in [
        "Slides 1 a 6. Contexto, problema e questão. Cerca de 5 minutos.",
        "Slides 7 a 12. Objetivos, conceitos e método. Cerca de 6 minutos.",
        "Slides 13 a 18. Desenvolvimento. Cerca de 6 minutos.",
        "Slides 19 a 21. Resultados, nas telas. Cerca de 3 minutos.",
        "Slides 22 a 26. Avaliação. Cerca de 6 minutos. Não encurte este bloco.",
        "Slides 27 a 31. Conclusão e encerramento. Cerca de 4 minutos.",
    ]:
        marcador(doc, linha)
    paragrafo(
        doc,
        "Ensaie com cronômetro. Se passar de 28 minutos, encurte o desenvolvimento e preserve a avaliação.",
        italico=True,
        cor=CINZA,
        espaco_antes=8,
    )


def palavras(texto):
    return len(texto.replace("\n", " ").split())


def slide(doc, numero, item, minutos):
    quebra(doc)
    titulo(doc, f"Slide {numero}  ·  {item['titulo']}")
    paragrafo(doc, f"{item['secao']}    ·    cerca de {minutos}", 11, True, False, OURO, espaco_depois=8)
    titulo(doc, "O que está no slide", 2)
    for linha in item["tela"]:
        marcador(doc, linha)
    titulo(doc, "Fala", 2)
    for bloco in item["fala"].split("\n\n"):
        paragrafo(doc, bloco.strip())
    if item.get("perguntas"):
        titulo(doc, "Se perguntarem", 2)
        paragrafo(
            doc,
            "Não leia isto na apresentação. Use só se a banca pedir o conceito.",
            11,
            False,
            True,
            CINZA,
            espaco_depois=6,
        )
        for bloco in item["perguntas"].split("\n\n"):
            paragrafo(doc, bloco.strip())


def main():
    doc = Document()
    configurar(doc)
    capa(doc)
    total = 0
    for numero, item in enumerate(SLIDES, start=1):
        n = palavras(item["fala"])
        total += n
        minutos = "menos de 1 minuto" if n < 90 else f"{max(1, round(n / 130))} min"
        if 90 <= n < 150:
            minutos = "1 min"
        elif n >= 150:
            minutos = "1 min 30 s"
        slide(doc, numero, item, minutos)
        print(f"{numero:02d}  {n:4d}  {item['titulo']}")
    doc.save(SAIDA)
    print(f"TOTAL FALA {total} palavras  ~{round(total / 130)} min")
    print(SAIDA)


if __name__ == "__main__":
    main()
