import json

def carregar_gramatica_de_txt(caminho_do_arquivo):
    gramatica = {}
    with open(caminho_do_arquivo, 'r') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha:
                partes = linha.split('->')
                nao_terminal = partes[0].strip()
                producoes = [prod.strip() for prod in partes[1].split('|')]
                gramatica[nao_terminal] = producoes
    return gramatica

class GramaticaLC:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.simbolos_nao_terminais = set(gramatica.keys())
        self.simbolos_terminais = self._get_terminais()

    def _get_terminais(self):
        terminais = set()
        for producoes in self.gramatica.values():
            for producao in producoes:
                for simbolo in producao:
                    if simbolo.islower() and simbolo not in self.simbolos_nao_terminais:
                        terminais.add(simbolo)
        return terminais

    def _identificar_geradores(self):
        geradores = set()
        while True:
            novos_geradores = set()
            for nao_terminal, producoes in self.gramatica.items():
                for producao in producoes:
                    if all(simbolo in self.simbolos_terminais or simbolo in geradores for simbolo in producao):
                        novos_geradores.add(nao_terminal)
            if novos_geradores.issubset(geradores):
                break
            geradores.update(novos_geradores)
        return geradores

    def simplificar_simbolos_inuteis(self):
        geradores = self._identificar_geradores()
        self.gramatica = {
            nao_terminal: [
                producao for producao in producoes
                if all(simbolo in self.simbolos_terminais or simbolo in geradores for simbolo in producao)
            ]
            for nao_terminal, producoes in self.gramatica.items()
            if nao_terminal in geradores
        }

    def simplificar_simbolos_inalcancaveis(self):
        alcancaveis = set('S')
        verificar = ['S']
        while verificar:
            nao_terminal = verificar.pop()
            for producao in self.gramatica.get(nao_terminal, []):
                for simbolo in producao:
                    if simbolo in self.simbolos_nao_terminais and simbolo not in alcancaveis:
                        alcancaveis.add(simbolo)
                        verificar.append(simbolo)
        self.gramatica = {
            nao_terminal: producoes
            for nao_terminal, producoes in self.gramatica.items()
            if nao_terminal in alcancaveis
        }

    def remover_producoes_vazias(self):
        producoes_vazias = {nt for nt, prods in self.gramatica.items() if '' in prods}
        while True:
            novos_vazios = {
                nt for nt, prods in self.gramatica.items()
                if any(all(s in producoes_vazias for s in prod) for prod in prods)
            }
            if novos_vazios.issubset(producoes_vazias):
                break
            producoes_vazias.update(novos_vazios)
        
        novas_producoes = {}
        for nt, prods in self.gramatica.items():
            novas_producoes[nt] = []
            for prod in prods:
                if prod != '':
                    novas_producoes[nt].append(prod)
                if any(s in producoes_vazias for s in prod):
                    novas_producoes[nt].extend(self._producoes_derivadas(prod, producoes_vazias))
        
        self.gramatica = novas_producoes

    def _producoes_derivadas(self, producao, producoes_vazias):
        if not producao:
            return ['']
        derivadas = set([producao])
        for i, simbolo in enumerate(producao):
            if simbolo in producoes_vazias:
                for deriv in self._producoes_derivadas(producao[:i] + producao[i+1:], producoes_vazias):
                    derivadas.add(deriv)
        return list(derivadas)

    def substituir_producoes(self):
        alterou = True
        while alterou:
            alterou = False
            novas_producoes = {}
            for nao_terminal, producoes in self.gramatica.items():
                novas_producoes[nao_terminal] = []
                for producao in producoes:
                    if len(producao) == 1 and producao in self.simbolos_nao_terminais:
                        alterou = True
                        novas_producoes[nao_terminal].extend(self.gramatica[producao])
                    else:
                        novas_producoes[nao_terminal].append(producao)
            self.gramatica = novas_producoes

    def converter_para_chomsky(self):
        # Implementação da conversão para a forma normal de Chomsky
        pass

    def converter_para_greibach(self):
        # Implementação da conversão para a forma normal de Greibach
        pass

    def fatoracao_a_esquerda(self):
        # Implementação da fatoração à esquerda
        pass

    def remocao_de_recursao_a_esquerda(self):
        # Implementação da remoção de recursão à esquerda
        pass

def salvar_gramatica_em_json(gramatica, caminho_do_arquivo):
    with open(caminho_do_arquivo, 'w') as arquivo:
        json.dump(gramatica, arquivo, indent=4)

def main():
    caminho_entrada = 'entrada.txt'
    caminho_saida = 'saida.json'

    gramatica = carregar_gramatica_de_txt(caminho_entrada)
    
    gramatica_lc = GramaticaLC(gramatica)
    
    print("Gramática lida:", gramatica)
    gramatica_lc.simplificar_simbolos_inuteis()
    print("Símbolos inúteis removidos:", gramatica_lc.gramatica)
    
    gramatica_lc.simplificar_simbolos_inalcancaveis()
    print("Símbolos inalcançáveis removidos:", gramatica_lc.gramatica)
    
    gramatica_lc.remover_producoes_vazias()
    print("Produções vazias removidas:", gramatica_lc.gramatica)
    
    gramatica_lc.substituir_producoes()
    print("Produções substituídas:", gramatica_lc.gramatica)
    
    gramatica_lc.converter_para_chomsky()
    print("Forma normal de Chomsky:", gramatica_lc.gramatica)
    
    gramatica_lc.converter_para_greibach()
    print("Forma normal de Greibach:", gramatica_lc.gramatica)
    
    gramatica_lc.fatoracao_a_esquerda()
    print("Fatoração à esquerda:", gramatica_lc.gramatica)
    
    gramatica_lc.remocao_de_recursao_a_esquerda()
    print("Remoção de recursão à esquerda:", gramatica_lc.gramatica)
    
    salvar_gramatica_em_json(gramatica_lc.gramatica, caminho_saida)

if __name__ == "__main__":
    main()
