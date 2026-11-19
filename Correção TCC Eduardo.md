# Correção TCC Eduardo

### Introdução

- Não deixa clara a contribuição do trabalho:
  
  - Você menciona o contexto, problema e solução, OK! 
  
  - Existem outras ferramentas que fazem transcrição e sumarização de vídeos? Se sim, comente sobre elas. Não precisa comentar sobre todas, mas, pelo menos, as 3 mais populares. 
  
  - Com isso, você conseguirá distinguir a tua ferramenta das já existentes, pode ser em termos de funcionalidades, valor (R$) se as outras foram pagas, tecnologias que usam, como o VLibras, enfim, você preca deixar explícito o que exatamente seu TCC acrescenta em relação às inúmeras ferramentas existentes de transcrição e sumarização de vídeos. Isso lhe dará o que mencionei no início, "a contribuição do trabalho".

### Objetivos Específicos

- Um dos objetivos específicos é: "Avaliar a qualidade e a fidelidade dos resumos gerados por meio de uma análise qualitativa, baseada na leitura técnica e na comparação direta entre o texto sintetizado e o conteúdo acadêmico apresentado nas videoaulas."
  
  - Não encontrei essa avaliação no trabalho. E ela é de extrema importância, pois, um trabalho acadêmico precisa ter três partes em que a última, como citei no email, é a **avaliação**. Sem isso, não há como atestar se o que foi desenvolvido é bom ou ruim.
  - Você precisa de um Capítulo de Avaliação após o desenvolvimento. Nele você deve responder algumas perguntas como:
    -   Quantas videoaulas foram avaliadas?
    - Quais videoaulas?
    - Quem avaliou?
    - Qual foi o critério de qualidade?
    - O que significa "fidelidade"?
    - Foi avaliada a cobertura das informações?
    - Houve erros factuais?
    - Houve informações inventadas?
    - Houve perda de informações importantes?
    - Como foi feita a comparação entre vídeo, transcrição e resumo?
    - Houve mais de um avaliador?
    - Como divergências foram tratadas?
  - Note que, sem essas respostas, como o leitor vai saber se a transcrição gerada é satisfatória ou não? Se ela cobre o assunto todo da videoaula ou se deixa assuntos importantes "de fora"? ou pior, se a transcrição "alucinou" e como resultado trouxe informações inverídicas ou que, se quer, fazem parte da aula?

### Tecnologias

- Na introdução e na seção de arquiterura você menciona que foi utilizado o Llama 3.1, porém na descrição do processamento paralelo você menciona que o "resumo via Phi‑4". Qual modelo realmente você usou? Verifique se não há inconsistência.

- Fiquei confuso quando você menciona os termos: "Whisper-large (OpenAI)", "Distil-Whisper-large-v3" e "faster-whisper". São três conceitos diferentes. Sugiro definir o que é cada um:
  
  - **Modelo:** Distil-Whisper large-v3
  
  - **Implementação/motor de inferência:** faster-whisper/CTranslate2.

### Arquitetura em Camadas

- A literatura estabelece que a **arquitetura em camadas** é: apresentação, lógica (negócio) e dados.

- **Microsserviços** é uma outra arquitetura de software, que tem como foco a decomposição do sistema em serviços independentes.

- Você pode utilizar: front-end + aplicação monolítica Spring + microsserviço Python. Não é errado, mas chamá-la de **arquitetura em camadas**, é conceitualmente errado.

### Implementação

- Você menciona que "foi implementado" tal coisa, porém, senti falta de mostrar alguns código. Não é necessário mostrar o programa inteiro, porém, mostre as partes mais importantes e explique-as. Isso deve vir antes da seção "Manual de Uso"

- Você pode finalizar relatando que o código em sua totalidade está disponível para consulta no link tal, e colocar o link do github.

### Avaliação

- Como citei no email, um TCC precisa ter começo, meio e fim. Sendo o começo, a introdução, explicando o contexto/problema/solução/objetivos, o meio sendo o desenvolvimento do que está se propondo, e o fim sendo a avaliação daquilo que foi desenvolvido. Logo, teu TCC hoje não tem a última parte, pois não foi avaliado o sistema. Ou, se foi, não está descrito no trabalho.

- Sugiro fazer as avaliações de:
  
  - Transcrição: precisa comparar uma transcrição considerada correta com a transcrição gerada pela ferramenta;
  
  - Resumo: cada resumo deve ser verificado se contempla as informações consideradas importantes do vídeo, se omite informações relevantes, se introduz informações que não estão presentes no vídeo, se apresenta informações incorretas ou distorcidas, e se as informações são organizadas de maneira clara
  
  - Desempenho: necessário avaliar o tempo de processamento das videoaulas. Para cada vídeo devem ser registrados: duração do vídeo, tamanho do arquivo, tempo de transcrição, tempo de reração do resumo, tempo total de processamento, e recursos computacionais utilizados.
  
  - Acessibilidade: você menciona no texto todo que o sistema provê uma melhor acessibilidade, mas então isso tem que ser comprovado. Isso só pode ser atestado por meio de uma avaliação com usuários finais. Se você não fizer isso, evite as frases como "o sistema melhora a aprendizagem dos estudantes surdos", ou "o sistema garante acessibilidade". 

- 















### Conclusão

- Recomendo verificar a conclusão de maneira geral. Você escreveu com palavras bonitas e frases de efeito, porém não há conteúdo relevante, típico de escrita de IAs.

- Não sou contra a escrita utilizando IA para ajudar, mas ctrl c e ctrl v, sem ter lido o que está escrito, não há como defender. Seja crítico com o conteúdo que a IA fornece. Na maioria das vezes, não há profundidade no assunto.

- Você tem objetivos específicos, utilize eles como estrutura para escrever a conclusão:
  
  - Objetivo 1: desenvolver interface funcional. Comente do desenvolvimento dessas interfaces e dos resultados delas.
  
  - Objetivo 2: implementação do ASR. escreva sobre o modelo, as configurações e os testes realizados que mostrem que esse objetivo foi atingido.
  
  - Objetivo 3: Implementação do LLM. escreva dobre o modelo, configurações, exemplos e resultados obtidos que mostrem que o objetivo específico foi atingido.
  
  - Objetivo 4: Qualidade dos resumos. mostre a metodologia que utilizou para avaliação os resumos, escreva sobre os resultado obtidos.



#### 
