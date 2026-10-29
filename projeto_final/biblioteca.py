
from datetime import date, timedelta


class Biblioteca:
    def __init__(
        self,
        limite_emprestimos=3,
        dias_emprestimo=14,
        multa_diaria=2.0
    ):
        if limite_emprestimos < 1:
            raise ValueError("O limite de empréstimos deve ser positivo")
        if dias_emprestimo < 1:
            raise ValueError("O prazo deve ser positivo")
        if multa_diaria < 0:
            raise ValueError("A multa não pode ser negativa")

        self.limite_emprestimos = limite_emprestimos
        self.dias_emprestimo = dias_emprestimo
        self.multa_diaria = multa_diaria

        self.livros = {}
        self.usuarios = {}
        self.emprestimos = {}
        self.reservas = {}
        self.proximo_emprestimo_id = 1

    def cadastrar_livro(self, livro_id, titulo, autor, quantidade=1):
        if not livro_id or not isinstance(livro_id, str):
            raise ValueError("O ID do livro é obrigatório")
        if not titulo or not titulo.strip():
            raise ValueError("O título é obrigatório")
        if not autor or not autor.strip():
            raise ValueError("O autor é obrigatório")
        if not isinstance(quantidade, int) or isinstance(quantidade, bool):
            raise ValueError("A quantidade deve ser um inteiro")
        if quantidade < 1:
            raise ValueError("A quantidade deve ser positiva")
        if livro_id in self.livros:
            raise ValueError("Já existe um livro com esse ID")

        self.livros[livro_id] = {
            "titulo": titulo.strip(),
            "autor": autor.strip(),
            "quantidade": quantidade,
            "disponiveis": quantidade
        }

    def cadastrar_usuario(self, usuario_id, nome):
        if not usuario_id or not isinstance(usuario_id, str):
            raise ValueError("O ID do usuário é obrigatório")
        if not nome or not nome.strip():
            raise ValueError("O nome é obrigatório")
        if usuario_id in self.usuarios:
            raise ValueError("Já existe um usuário com esse ID")

        self.usuarios[usuario_id] = {
            "nome": nome.strip()
        }

    def buscar_livro(self, livro_id):
        if livro_id not in self.livros:
            raise ValueError("Livro não encontrado")
        return self.livros[livro_id].copy()

    def remover_livro(self, livro_id):
        if livro_id not in self.livros:
            raise ValueError("Livro não encontrado")

        livro_emprestado = any(
            emprestimo["livro_id"] == livro_id
            and emprestimo["devolvido_em"] is None
            for emprestimo in self.emprestimos.values()
        )

        if livro_emprestado:
            raise ValueError("Não é possível remover um livro emprestado")

        if self.livros[livro_id]["disponiveis"] != self.livros[livro_id]["quantidade"]:
            raise ValueError("O livro possui exemplares reservados")

        del self.livros[livro_id]
        self.reservas.pop(livro_id, None)

    def emprestar(self, livro_id, usuario_id, data_emprestimo=None):
        if livro_id not in self.livros:
            raise ValueError("Livro não encontrado")
        if usuario_id not in self.usuarios:
            raise ValueError("Usuário não encontrado")

        emprestimos_ativos = [
            emprestimo
            for emprestimo in self.emprestimos.values()
            if emprestimo["usuario_id"] == usuario_id
            and emprestimo["devolvido_em"] is None
        ]

        if len(emprestimos_ativos) >= self.limite_emprestimos:
            raise ValueError("Usuário atingiu o limite de empréstimos")

        reserva = next(
            (
                item for item in self.reservas.get(livro_id, [])
                if item["usuario_id"] == usuario_id
                and item["status"] == "disponivel"
            ),
            None
        )

        if self.livros[livro_id]["disponiveis"] <= 0 and reserva is None:
            raise ValueError("Não há exemplares disponíveis")

        if data_emprestimo is None:
            data_emprestimo = date.today()
        if not isinstance(data_emprestimo, date):
            raise ValueError("A data do empréstimo é inválida")

        if reserva is not None:
            reserva["status"] = "atendida"
        else:
            self.livros[livro_id]["disponiveis"] -= 1

        emprestimo_id = self.proximo_emprestimo_id
        self.proximo_emprestimo_id += 1

        self.emprestimos[emprestimo_id] = {
            "livro_id": livro_id,
            "usuario_id": usuario_id,
            "emprestado_em": data_emprestimo,
            "vencimento": data_emprestimo + timedelta(
                days=self.dias_emprestimo
            ),
            "devolvido_em": None
        }

        return emprestimo_id

    def devolver(self, emprestimo_id, data_devolucao=None):
        if emprestimo_id not in self.emprestimos:
            raise ValueError("Empréstimo não encontrado")

        emprestimo = self.emprestimos[emprestimo_id]

        if emprestimo["devolvido_em"] is not None:
            raise ValueError("Este empréstimo já foi devolvido")

        if data_devolucao is None:
            data_devolucao = date.today()
        if not isinstance(data_devolucao, date):
            raise ValueError("A data da devolução é inválida")
        if data_devolucao < emprestimo["emprestado_em"]:
            raise ValueError("A devolução não pode anteceder o empréstimo")

        dias_atraso = (
            data_devolucao - emprestimo["vencimento"]
        ).days
        dias_atraso = max(0, dias_atraso)
        multa = dias_atraso * self.multa_diaria

        emprestimo["devolvido_em"] = data_devolucao
        livro_id = emprestimo["livro_id"]
        self.livros[livro_id]["disponiveis"] += 1

        fila = self.reservas.get(livro_id, [])
        proxima_reserva = next(
            (item for item in fila if item["status"] == "aguardando"),
            None
        )

        if proxima_reserva is not None:
            proxima_reserva["status"] = "disponivel"
            self.livros[livro_id]["disponiveis"] -= 1

        return round(multa, 2)

    def reservar(self, livro_id, usuario_id):
        if livro_id not in self.livros:
            raise ValueError("Livro não encontrado")
        if usuario_id not in self.usuarios:
            raise ValueError("Usuário não encontrado")

        if self.livros[livro_id]["disponiveis"] > 0:
            raise ValueError("O livro está disponível para empréstimo")

        fila = self.reservas.setdefault(livro_id, [])

        reserva_existente = any(
            item["usuario_id"] == usuario_id
            and item["status"] in ("aguardando", "disponivel")
            for item in fila
        )

        if reserva_existente:
            raise ValueError("Usuário já possui uma reserva ativa")

        fila.append({
            "usuario_id": usuario_id,
            "status": "aguardando"
        })

    def consultar_emprestimos(self, usuario_id):
        if usuario_id not in self.usuarios:
            raise ValueError("Usuário não encontrado")

        return [
            emprestimo.copy()
            for emprestimo in self.emprestimos.values()
            if emprestimo["usuario_id"] == usuario_id
        ]
