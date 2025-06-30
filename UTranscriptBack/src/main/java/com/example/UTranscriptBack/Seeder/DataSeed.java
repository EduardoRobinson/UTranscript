package com.example.UTranscriptBack.Seeder;

import java.util.List;

import com.example.UTranscriptBack.models.CursoModel;
import com.example.UTranscriptBack.models.StatusTranscriptionModel;
import com.example.UTranscriptBack.models.UniversidadeModel;

public class DataSeed {
    public static final List<UniversidadeModel> UNIVERSIDADES = List.of(
            new UniversidadeModel(null, "Universidade de São Paulo", "USP"),
            new UniversidadeModel(null, "Universidade Estadual de Campinas", "UNICAMP"),
            new UniversidadeModel(null, "Universidade Federal de Minas Gerais", "UFMG"),
            new UniversidadeModel(null, "Universidade Federal do Rio de Janeiro", "UFRJ"),
            new UniversidadeModel(null, "Universidade Estadual Paulista", "UNESP"),
            new UniversidadeModel(null, "Universidade Federal do Rio Grande do Sul", "UFRGS"),
            new UniversidadeModel(null, "Universidade Federal de Santa Catarina", "UFSC"),
            new UniversidadeModel(null, "Universidade Federal do Paraná", "UFPR"),
            new UniversidadeModel(null, "Universidade Federal de Pernambuco", "UFPE"),
            new UniversidadeModel(null, "Universidade Federal da Bahia", "UFBA"),
            new UniversidadeModel(null, "Universidade de Brasília", "UnB"),
            new UniversidadeModel(null, "Universidade Federal de São Carlos", "UFSCar"),
            new UniversidadeModel(null, "Universidade Federal do Ceará", "UFC"),
            new UniversidadeModel(null, "Universidade Federal do Espírito Santo", "UFES"),
            new UniversidadeModel(null, "Universidade Federal de Goiás", "UFG"),
            new UniversidadeModel(null, "Universidade Federal do Pará", "UFPA"),
            new UniversidadeModel(null, "Universidade Federal de Uberlândia", "UFU"),
            new UniversidadeModel(null, "Universidade Federal de São João del-Rei", "UFSJ"),
            new UniversidadeModel(null, "Universidade Federal de Viçosa", "UFV"),
            new UniversidadeModel(null, "Universidade Federal do ABC", "UFABC"),
            new UniversidadeModel(null, "Pontifícia Universidade Católica de São Paulo", "PUC-SP"),
            new UniversidadeModel(null, "Pontifícia Universidade Católica do Rio de Janeiro", "PUC-Rio"),
            new UniversidadeModel(null, "Pontifícia Universidade Católica do Paraná", "PUC-PR"),
            new UniversidadeModel(null, "Pontifícia Universidade Católica do Rio Grande do Sul", "PUC-RS"),
            new UniversidadeModel(null, "Universidade Estadual do Ceará", "UECE"),
            new UniversidadeModel(null, "Universidade Estadual de Maringá", "UEM"),
            new UniversidadeModel(null, "Universidade Estadual de Londrina", "UEL"),
            new UniversidadeModel(null, "Universidade Estadual do Centro-Oeste", "UNICENTRO"),
            new UniversidadeModel(null, "Universidade Federal do Maranhão", "UFMA"),
            new UniversidadeModel(null, "Universidade Federal da Paraíba", "UFPB"),
            new UniversidadeModel(null, "Universidade Federal de Alagoas", "UFAL"),
            new UniversidadeModel(null, "Universidade Federal de Sergipe", "UFS"),
            new UniversidadeModel(null, "Universidade Federal de Juiz de Fora", "UFJF"),
            new UniversidadeModel(null, "Universidade Federal de Lavras", "UFLA"),
            new UniversidadeModel(null, "Universidade Federal de Itajubá", "UNIFEI"),
            new UniversidadeModel(null, "Universidade Federal do Triângulo Mineiro", "UFTM"),
            new UniversidadeModel(null, "Universidade Federal de Pelotas", "UFPel"),
            new UniversidadeModel(null, "Universidade Federal do Pampa", "UNIPAMPA"),
            new UniversidadeModel(null, "Universidade Federal de Roraima", "UFRR"),
            new UniversidadeModel(null, "Universidade Federal do Acre", "UFAC"),
            new UniversidadeModel(null, "Universidade Federal do Amapá", "UNIFAP"),
            new UniversidadeModel(null, "Universidade Federal do Tocantins", "UFT"),
            new UniversidadeModel(null, "Universidade Federal de Campina Grande", "UFCG"),
            new UniversidadeModel(null, "Universidade Federal do Oeste do Pará", "UFOPA"),
            new UniversidadeModel(null, "Universidade Federal do Vale do São Francisco", "UNIVASF"),
            new UniversidadeModel(null, "Universidade Federal do Recôncavo da Bahia", "UFRB"),
            new UniversidadeModel(null, "Universidade Estadual do Maranhão", "UEMA"),
            new UniversidadeModel(null, "Universidade Estadual de Feira de Santana", "UEFS"),
            new UniversidadeModel(null, "Universidade Estadual da Paraíba", "UEPB"),
            new UniversidadeModel(null, "Universidade Tecnólogica Federal do Paraná", "UTFPR"));

    public static final List<CursoModel> CURSOS = List.of(
            new CursoModel(null, "Engenharia de Software"),
            new CursoModel(null, "Ciência da Computação"),
            new CursoModel(null, "Engenharia Elétrica"),
            new CursoModel(null, "Engenharia Mecânica"),
            new CursoModel(null, "Engenharia Química"),
            new CursoModel(null, "Engenharia de Produção"),
            new CursoModel(null, "Engenharia de Bioprocessos e Biotecnologia"),
            new CursoModel(null, "Ciências Biológicas"),
            new CursoModel(null, "Automação Industrial"),
            new CursoModel(null, "Análise e Desenvolvimento de Sistemas"),
            new CursoModel(null, "Fabricação Mecânica"));
    public static final List<Object> TEMAS = List.of(
            java.util.Map.of("curso", "Ciência da computação", "materia", "Algoritmos"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Matemática Discreta"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Estruturas de Dados"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Banco de Dados"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Sistemas Operacionais"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Redes de Computadores"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Engenharia de Software"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Inteligência Artificial"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Programação Orientada a Objetos"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Desenvolvimento Web"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Desenvolvimento de Aplicativos Móveis"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Compiladores"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Análise E Projeto De Algoritmos"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Interação Humano-Computador"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Mineração De Dados"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Segurança da Informação"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Computação Gráfica"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Sistemas Distribuídos"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Computação Quântica"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Computação em Nuvem"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Sistemas Microcontrolados"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Teoria dos Grafos"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Processamento de Linguagem Natural"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Visão Computacional"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Robótica"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Sistemas Embarcados"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Desenvolvimento de Jogos"),
            java.util.Map.of("curso", "Ciência da computação", "materia", "Linguagens Formais e Autômatos"));

    public static final List<StatusTranscriptionModel> STATUS = List.of(
            new StatusTranscriptionModel(null, "Pendente"),
            new StatusTranscriptionModel(null, "Em Andamento"),
            new StatusTranscriptionModel(null, "Concluído"));

}
