
import unittest
from datetime import date, timedelta

from biblioteca import Biblioteca


class TestBiblioteca(unittest.TestCase):
    

    def setUp(self):
        """Cria uma biblioteca nova para cada teste."""
        self.biblioteca = Biblioteca()
        self.biblioteca.cadastrar_livro(
            "L001", "Algoritmos", "Thomas Cormen", quantidade=3
        )
        self.biblioteca.cadastrar_livro(
            "L002", "Python Básico", "Autor Teste", quantidade=1
        )
        self.biblioteca.cadastrar_usuario("U001", "Ana")
        self.biblioteca.cadastrar_usuario("U002", "Bruno")
        self.biblioteca.cadastrar_usuario("U003", "Carla")

        self.hoje = date(2026, 10, 28)
        

    # --------------------------------------------------
    # 1. Inicialização e configurações
    # --------------------------------------------------

    def test_criar_biblioteca_com_configuracoes_padrao(self):
        biblioteca = Biblioteca()
        self.assertEqual(biblioteca.limite_emprestimos, 3)
        self.assertEqual(biblioteca.dias_emprestimo, 14)
        self.assertEqual(biblioteca.multa_diaria, 2.0)

    def test_rejeitar_limite_de_emprestimos_invalido(self):
        with self.assertRaises(ValueError):
            Biblioteca(limite_emprestimos=0)

    def test_rejeitar_prazo_invalido(self):
        with self.assertRaises(ValueError):
            Biblioteca(dias_emprestimo=0)

    def test_rejeitar_multa_negativa(self):
        with self.assertRaises(ValueError):
            Biblioteca(multa_diaria=-1)

    # --------------------------------------------------
    # 2. Cadastro e consulta de livros
    # --------------------------------------------------

    def test_cadastrar_e_buscar_livro(self):
        livro = self.biblioteca.buscar_livro("L001")
        self.assertEqual(livro["titulo"], "Algoritmos")
        self.assertEqual(livro["autor"], "Thomas Cormen")
        self.assertEqual(livro["quantidade"], 3)
        self.assertEqual(livro["disponiveis"], 3)

    def test_remover_espacos_externos_do_titulo_e_autor(self):
        self.biblioteca.cadastrar_livro(
            "L003", "  Estruturas de Dados  ", "  Maria  "
        )
        livro = self.biblioteca.buscar_livro("L003")
        self.assertEqual(livro["titulo"], "Estruturas de Dados")
        self.assertEqual(livro["autor"], "Maria")

    def test_rejeitar_id_de_livro_vazio(self):
        with self.assertRaises(ValueError):
            self.biblioteca.cadastrar_livro("", "Livro", "Autor")

    def test_rejeitar_titulo_vazio(self):
        with self.assertRaises(ValueError):
            self.biblioteca.cadastrar_livro("L003", "   ", "Autor")

    def test_rejeitar_autor_vazio(self):
        with self.assertRaises(ValueError):
            self.biblioteca.cadastrar_livro("L003", "Livro", "  ")

    def test_rejeitar_quantidade_zero(self):
        with self.assertRaises(ValueError):
            self.biblioteca.cadastrar_livro(
                "L003", "Livro", "Autor", quantidade=0
            )

    def test_rejeitar_quantidade_nao_inteira(self):
        with self.assertRaises(ValueError):
            self.biblioteca.cadastrar_livro(
                "L003", "Livro", "Autor", quantidade=1.5
            )

    def test_rejeitar_quantidade_booleana(self):
        with self.assertRaises(ValueError):
            self.biblioteca.cadastrar_livro(
                "L003", "Livro", "Autor", quantidade=True
            )

    def test_rejeitar_id_de_livro_duplicado(self):
        with self.assertRaises(ValueError):
            self.biblioteca.cadastrar_livro(
                "L001", "Outro Livro", "Outro Autor"
            )

    def test_buscar_livro_inexistente(self):
        with self.assertRaises(ValueError):
            self.biblioteca.buscar_livro("INEXISTENTE")

    # --------------------------------------------------
    # 3. Cadastro de usuários
    # --------------------------------------------------

    def test_cadastrar_usuario(self):
        self.biblioteca.cadastrar_usuario("U004", "  Daniela  ")
        self.assertEqual(
            self.biblioteca.usuarios["U004"]["nome"], "Daniela"
        )

    def test_rejeitar_nome_de_usuario_vazio(self):
        with self.assertRaises(ValueError):
            self.biblioteca.cadastrar_usuario("U004", "   ")

    def test_rejeitar_usuario_duplicado(self):
        with self.assertRaises(ValueError):
            self.biblioteca.cadastrar_usuario("U001", "Outra Pessoa")

    # --------------------------------------------------
    # 4. Remoção de livros
    # --------------------------------------------------

    def test_remover_livro_sem_emprestimos(self):
        self.biblioteca.remover_livro("L002")
        self.assertNotIn("L002", self.biblioteca.livros)

    def test_rejeitar_remocao_de_livro_inexistente(self):
        with self.assertRaises(ValueError):
            self.biblioteca.remover_livro("INEXISTENTE")

    def test_rejeitar_remocao_de_livro_emprestado(self):
        self.biblioteca.emprestar("L002", "U001", self.hoje)
        with self.assertRaises(ValueError):
            self.biblioteca.remover_livro("L002")

    # --------------------------------------------------
    # 5. Empréstimos
    # --------------------------------------------------

    def test_realizar_emprestimo(self):
        emprestimo_id = self.biblioteca.emprestar(
            "L001", "U001", self.hoje
        )
        emprestimo = self.biblioteca.emprestimos[emprestimo_id]

        self.assertEqual(emprestimo["livro_id"], "L001")
        self.assertEqual(emprestimo["usuario_id"], "U001")
        self.assertEqual(emprestimo["vencimento"], self.hoje + timedelta(days=14))
        self.assertIsNone(emprestimo["devolvido_em"])

    def test_emprestimo_reduz_exemplares_disponiveis(self):
        self.biblioteca.emprestar("L001", "U001", self.hoje)
        self.assertEqual(
            self.biblioteca.buscar_livro("L001")["disponiveis"], 2
        )

    def test_rejeitar_emprestimo_de_livro_inexistente(self):
        with self.assertRaises(ValueError):
            self.biblioteca.emprestar("INEXISTENTE", "U001", self.hoje)

    def test_rejeitar_emprestimo_para_usuario_inexistente(self):
        with self.assertRaises(ValueError):
            self.biblioteca.emprestar("L001", "INEXISTENTE", self.hoje)

    def test_rejeitar_emprestimo_sem_exemplares_disponiveis(self):
        self.biblioteca.emprestar("L002", "U001", self.hoje)
        with self.assertRaises(ValueError):
            self.biblioteca.emprestar("L002", "U002", self.hoje)

    def test_permitir_emprestimo_ate_o_limite(self):
        for _ in range(3):
            self.biblioteca.emprestar("L001", "U001", self.hoje)

        self.assertEqual(
            len(self.biblioteca.consultar_emprestimos("U001")), 3
        )

    def test_rejeitar_emprestimo_acima_do_limite(self):
        for _ in range(3):
            self.biblioteca.emprestar("L001", "U001", self.hoje)

        with self.assertRaises(ValueError):
            self.biblioteca.emprestar("L001", "U001", self.hoje)

    def test_rejeitar_data_de_emprestimo_invalida(self):
        with self.assertRaises(ValueError):
            self.biblioteca.emprestar("L001", "U001", "28/10/2026")

    

    # --------------------------------------------------
    # 6. Devoluções e multas
    # --------------------------------------------------

    def test_devolucao_no_prazo_sem_multa(self):
        emprestimo_id = self.biblioteca.emprestar(
            "L002", "U001", self.hoje
        )
        devolucao = self.hoje + timedelta(days=14)

        multa = self.biblioteca.devolver(emprestimo_id, devolucao)
        self.assertEqual(multa, 0.0)

    def test_devolucao_atrasada_calcula_multa(self):
        emprestimo_id = self.biblioteca.emprestar(
            "L002", "U001", self.hoje
        )
        devolucao = self.hoje + timedelta(days=17)

        multa = self.biblioteca.devolver(emprestimo_id, devolucao)
        self.assertEqual(multa, 6.0)

    def test_devolucao_um_dia_atrasada(self):
        emprestimo_id = self.biblioteca.emprestar(
            "L002", "U001", self.hoje
        )
        devolucao = self.hoje + timedelta(days=15)

        multa = self.biblioteca.devolver(emprestimo_id, devolucao)
        self.assertEqual(multa, 2.0)

    def test_devolucao_restaura_disponibilidade(self):
        self.biblioteca.emprestar("L002", "U001", self.hoje)
        emprestimo_id = 1

        self.biblioteca.devolver(
            emprestimo_id, self.hoje + timedelta(days=5)
        )
        self.assertEqual(
            self.biblioteca.buscar_livro("L002")["disponiveis"], 1
        )

    def test_rejeitar_devolucao_de_emprestimo_inexistente(self):
        with self.assertRaises(ValueError):
            self.biblioteca.devolver(999, self.hoje)

    def test_rejeitar_devolucao_dupla(self):
        emprestimo_id = self.biblioteca.emprestar(
            "L002", "U001", self.hoje
        )
        self.biblioteca.devolver(
            emprestimo_id, self.hoje + timedelta(days=2)
        )

        with self.assertRaises(ValueError):
            self.biblioteca.devolver(
                emprestimo_id, self.hoje + timedelta(days=3)
            )

    def test_rejeitar_devolucao_anterior_ao_emprestimo(self):
        emprestimo_id = self.biblioteca.emprestar(
            "L002", "U001", self.hoje
        )

        with self.assertRaises(ValueError):
            self.biblioteca.devolver(
                emprestimo_id, self.hoje - timedelta(days=1)
            )

    def test_rejeitar_data_de_devolucao_invalida(self):
        emprestimo_id = self.biblioteca.emprestar(
            "L002", "U001", self.hoje
        )

        with self.assertRaises(ValueError):
            self.biblioteca.devolver(emprestimo_id, "data inválida")

    # --------------------------------------------------
    # 7. Reservas
    # --------------------------------------------------

    def test_reservar_livro_indisponivel(self):
        self.biblioteca.emprestar("L002", "U001", self.hoje)
        self.biblioteca.reservar("L002", "U002")

        fila = self.biblioteca.reservas["L002"]
        self.assertEqual(len(fila), 1)
        self.assertEqual(fila[0]["status"], "aguardando")

    def test_rejeitar_reserva_de_livro_disponivel(self):
        with self.assertRaises(ValueError):
            self.biblioteca.reservar("L001", "U001")

    def test_rejeitar_reserva_de_livro_inexistente(self):
        with self.assertRaises(ValueError):
            self.biblioteca.reservar("INEXISTENTE", "U001")

    def test_rejeitar_reserva_para_usuario_inexistente(self):
        self.biblioteca.emprestar("L002", "U001", self.hoje)

        with self.assertRaises(ValueError):
            self.biblioteca.reservar("L002", "INEXISTENTE")

    def test_rejeitar_reserva_ativa_duplicada(self):
        self.biblioteca.emprestar("L002", "U001", self.hoje)
        self.biblioteca.reservar("L002", "U002")

        with self.assertRaises(ValueError):
            self.biblioteca.reservar("L002", "U002")

    def test_devolucao_disponibiliza_livro_para_proxima_reserva(self):
        self.biblioteca.emprestar("L002", "U001", self.hoje)
        self.biblioteca.reservar("L002", "U002")

        self.biblioteca.devolver(1, self.hoje + timedelta(days=3))

        reserva = self.biblioteca.reservas["L002"][0]
        self.assertEqual(reserva["status"], "disponivel")
        self.assertEqual(
            self.biblioteca.buscar_livro("L002")["disponiveis"], 0
        )

    def test_usuario_com_reserva_disponivel_pode_emprestar(self):
        self.biblioteca.emprestar("L002", "U001", self.hoje)
        self.biblioteca.reservar("L002", "U002")
        self.biblioteca.devolver(1, self.hoje + timedelta(days=3))

        novo_id = self.biblioteca.emprestar(
            "L002", "U002", self.hoje + timedelta(days=3)
        )

        self.assertEqual(
            self.biblioteca.emprestimos[novo_id]["usuario_id"], "U002"
        )
        self.assertEqual(
            self.biblioteca.reservas["L002"][0]["status"], "atendida"
        )

    # --------------------------------------------------
    # 8. Consulta de empréstimos
    # --------------------------------------------------

    def test_consultar_emprestimos_do_usuario(self):
        self.biblioteca.emprestar("L001", "U001", self.hoje)
        self.biblioteca.emprestar("L002", "U002", self.hoje)

        emprestimos = self.biblioteca.consultar_emprestimos("U001")
        self.assertEqual(len(emprestimos), 1)
        self.assertEqual(emprestimos[0]["livro_id"], "L001")

    def test_usuario_sem_emprestimos_retorna_lista_vazia(self):
        self.assertEqual(
            self.biblioteca.consultar_emprestimos("U003"), []
        )

    def test_rejeitar_consulta_de_usuario_inexistente(self):
        with self.assertRaises(ValueError):
            self.biblioteca.consultar_emprestimos("INEXISTENTE")

    
    def test_remover_livro_nao_emprestado_quando_outro_esta_emprestado(self):
        self.biblioteca.emprestar("L001", "U001", self.hoje)

        self.biblioteca.remover_livro("L002")

        self.assertNotIn("L002", self.biblioteca.livros)

    def test_emprestimos_de_outro_usuario_nao_contam_para_limite_1(self):
        for _ in range(3):
            self.biblioteca.emprestar("L001", "U001", self.hoje)

        emprestimo_id = self.biblioteca.emprestar(
            "L002", "U002", self.hoje
        )

        self.assertEqual(
            self.biblioteca.emprestimos[emprestimo_id]["usuario_id"],
            "U002"
        )

    def test_emprestimos_de_outro_usuario_nao_contam_para_limite_2(self):
        for _ in range(3):
            self.biblioteca.emprestar("L001", "U002", self.hoje)

        emprestimo_id = self.biblioteca.emprestar(
            "L002", "U001", self.hoje
        )

        self.assertEqual(
            self.biblioteca.emprestimos[emprestimo_id]["usuario_id"],
            "U001"
        )

    def test_limite_de_emprestimos_bloqueia_livro_disponivel(self):
        for _ in range(3):
            self.biblioteca.emprestar("L001", "U001", self.hoje)

        with self.assertRaisesRegex(ValueError, "limite de empréstimos"):
            self.biblioteca.emprestar("L002", "U001", self.hoje)

    def test_consultar_emprestimos_retorna_apenas_do_usuario(self):
        self.biblioteca.emprestar("L001", "U001", self.hoje)
        self.biblioteca.emprestar("L002", "U002", self.hoje)

        emprestimos = self.biblioteca.consultar_emprestimos("U001")

        self.assertEqual(len(emprestimos), 1)
        self.assertTrue(
            all(item["usuario_id"] == "U001" for item in emprestimos)
        )

    def test_outro_usuario_pode_reservar_o_mesmo_livro(self):
        self.biblioteca.emprestar("L002", "U001", self.hoje)

        self.biblioteca.reservar("L002", "U002")
        self.biblioteca.reservar("L002", "U003")

        reservas = self.biblioteca.reservas["L002"]
        self.assertEqual(len(reservas), 2)

    def test_reserva_aguardando_nao_permite_emprestimo(self):
        self.biblioteca.emprestar("L002", "U001", self.hoje)
        self.biblioteca.reservar("L002", "U002")

        with self.assertRaisesRegex(ValueError, "disponíveis"):
            self.biblioteca.emprestar("L002", "U002", self.hoje)

    def test_usuario_sem_reserva_nao_pode_usar_reserva_de_outro(self):
        emprestimo_id = self.biblioteca.emprestar(
            "L002", "U001", self.hoje
        )
        self.biblioteca.reservar("L002", "U002")
        self.biblioteca.devolver(
            emprestimo_id,
            self.hoje + timedelta(days=14)
        )

        with self.assertRaisesRegex(ValueError, "disponíveis"):
            self.biblioteca.emprestar("L002", "U003", self.hoje)

    def test_aceitar_limite_de_emprestimos_igual_a_um(self):
        biblioteca = Biblioteca(limite_emprestimos=1)
        self.assertEqual(biblioteca.limite_emprestimos, 1)

    def test_aceitar_prazo_de_emprestimo_de_um_dia(self):
        biblioteca = Biblioteca(dias_emprestimo=1)
        self.assertEqual(biblioteca.dias_emprestimo, 1)

    def test_aceitar_multa_diaria_igual_a_zero(self):
        biblioteca = Biblioteca(multa_diaria=0)
        self.assertEqual(biblioteca.multa_diaria, 0)

    def test_devolucao_no_mesmo_dia_do_emprestimo(self):
        emprestimo_id = self.biblioteca.emprestar(
            "L002", "U001", self.hoje
        )

        multa = self.biblioteca.devolver(emprestimo_id, self.hoje)

        self.assertEqual(multa, 0)

    def test_devolucao_antes_do_vencimento_nao_gera_multa(self):
        emprestimo_id = self.biblioteca.emprestar(
            "L002", "U001", self.hoje
        )

        multa = self.biblioteca.devolver(
            emprestimo_id,
            self.hoje + timedelta(days=3)
        )

        self.assertEqual(multa, 0)

    def test_ids_de_emprestimos_sao_sequenciais(self):
        primeiro = self.biblioteca.emprestar(
            "L001", "U001", self.hoje
        )
        segundo = self.biblioteca.emprestar(
            "L001", "U002", self.hoje
        )

        self.assertEqual(primeiro, 1)
        self.assertEqual(segundo, 2)

    def test_multa_e_arredondada_para_duas_casas_decimais(self):
        biblioteca = Biblioteca(multa_diaria=1.237)
        biblioteca.cadastrar_livro("L100", "Livro", "Autor")
        biblioteca.cadastrar_usuario("U100", "Pessoa")

        emprestimo_id = biblioteca.emprestar(
            "L100", "U100", self.hoje
        )
        vencimento = self.hoje + timedelta(days=14)

        multa = biblioteca.devolver(
            emprestimo_id,
            vencimento + timedelta(days=1)
        )

        self.assertEqual(multa, 1.24)

    def test_rejeitar_id_de_usuario_nao_textual(self):
        with self.assertRaises(ValueError):
            self.biblioteca.cadastrar_usuario(123, "Pessoa")

    def test_quantidade_padrao_de_livros_e_um(self):
        self.biblioteca.cadastrar_livro("L100", "Livro", "Autor")

        livro = self.biblioteca.buscar_livro("L100")

        self.assertEqual(livro["quantidade"], 1)
        self.assertEqual(livro["disponiveis"], 1)

    def test_nao_remover_livro_com_reserva_disponivel(self):
        emprestimo_id = self.biblioteca.emprestar(
            "L002", "U001", self.hoje
        )
        self.biblioteca.reservar("L002", "U002")
        self.biblioteca.devolver(
            emprestimo_id,
            self.hoje + timedelta(days=14)
        )

        with self.assertRaisesRegex(ValueError, "reservados"):
            self.biblioteca.remover_livro("L002")



if __name__ == "__main__":
    unittest.main()
