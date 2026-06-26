from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "relatorio-test-pattern.pdf"


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawRightString(
        A4[0] - 2 * cm,
        1.25 * cm,
        f"Pagina {doc.page}",
    )
    canvas.restoreState()


def build_styles():
    styles = getSampleStyleSheet()
    styles["Title"].fontName = "Helvetica-Bold"
    styles["Title"].fontSize = 20
    styles["Title"].leading = 26
    styles["Title"].spaceAfter = 18

    styles["Heading1"].fontName = "Helvetica-Bold"
    styles["Heading1"].fontSize = 14
    styles["Heading1"].leading = 18
    styles["Heading1"].spaceBefore = 12
    styles["Heading1"].spaceAfter = 8
    styles["Heading1"].textColor = colors.HexColor("#1F2937")

    styles["Heading2"].fontName = "Helvetica-Bold"
    styles["Heading2"].fontSize = 11
    styles["Heading2"].leading = 14
    styles["Heading2"].spaceBefore = 8
    styles["Heading2"].spaceAfter = 5

    styles["BodyText"].fontName = "Helvetica"
    styles["BodyText"].fontSize = 10
    styles["BodyText"].leading = 14
    styles["BodyText"].spaceAfter = 7

    code_block = ParagraphStyle(
        "CodeBlock",
        parent=styles["Code"],
        fontName="Courier",
        fontSize=7.7,
        leading=10,
        leftIndent=8,
        rightIndent=8,
        borderColor=colors.HexColor("#D1D5DB"),
        borderWidth=0.5,
        borderPadding=6,
        backColor=colors.HexColor("#F9FAFB"),
        spaceBefore=4,
        spaceAfter=8,
    )
    styles.add(code_block)
    return styles


def p(text, styles):
    return Paragraph(text, styles["BodyText"])


def h1(text, styles):
    return Paragraph(text, styles["Heading1"])


def h2(text, styles):
    return Paragraph(text, styles["Heading2"])


def code(text, styles):
    return Preformatted(text.strip(), styles["CodeBlock"])


def build_story(styles):
    story = []

    story.append(Paragraph("Relatorio - Padroes de Teste em Checkout de E-commerce", styles["Title"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(p("<b>Disciplina:</b> Engenharia de Software / Testes de Software", styles))
    story.append(p("<b>Trabalho:</b> Padroes de Teste - Object Mother, Data Builder, Stubs e Mocks", styles))
    story.append(p("<b>Aluno:</b> [preencher nome completo]", styles))
    story.append(p("<b>Matricula:</b> [preencher matricula]", styles))
    story.append(p("<b>Repositorio:</b> https://github.com/CleitonSilvaT/test-pattern ou fork do aluno", styles))
    story.append(Spacer(1, 1.0 * cm))
    story.append(p(
        "Este relatorio descreve a implementacao de uma suite de testes unitarios para o "
        "servico CheckoutService. O objetivo foi prevenir Test Smells por meio de padroes "
        "de criacao de dados de teste e test doubles, mantendo os testes legiveis, focados "
        "e isolados de dependencias externas.",
        styles,
    ))
    story.append(PageBreak())

    story.append(h1("1. Padroes de Criacao de Dados", styles))
    story.append(h2("1.1 Object Mother para User", styles))
    story.append(p(
        "O padrao Object Mother foi aplicado na classe UserMother para criar usuarios "
        "simples e recorrentes, como um usuario PADRAO e um usuario PREMIUM. Esse padrao "
        "e adequado quando a entidade tem poucos campos relevantes e quando seus cenarios "
        "mais comuns sao estaveis entre os testes.",
        styles,
    ))

    story.append(h2("1.2 Por que CarrinhoBuilder em vez de CarrinhoMother", styles))
    story.append(p(
        "O Carrinho e mais variavel que User: pode estar vazio, possuir diferentes usuarios "
        "e conter listas distintas de itens. Se fosse usado um CarrinhoMother, seriam "
        "necessarios muitos metodos como carrinhoVazio, carrinhoPremium, carrinhoComDoisItens "
        "e carrinhoComValorEspecifico. Essa proliferacao reduz a clareza e torna a manutencao "
        "mais dificil.",
        styles,
    ))
    story.append(p(
        "O CarrinhoBuilder resolve esse problema com uma API fluente. Ele fornece defaults "
        "seguros, mas permite explicitar apenas o que importa para cada caso de teste, como "
        "o usuario Premium e os itens que totalizam R$ 200,00.",
        styles,
    ))

    story.append(h2("1.3 Antes: setup manual complexo", styles))
    story.append(code(
        """
const user = new User(2, 'Usuario Premium', 'premium@email.com', 'PREMIUM');
const itens = [
    new Item('Produto A', 120),
    new Item('Produto B', 80),
];
const carrinho = new Carrinho(user, itens);
        """,
        styles,
    ))

    story.append(h2("1.4 Depois: setup com Data Builder", styles))
    story.append(code(
        """
const userPremium = UserMother.umUsuarioPremium();
const carrinho = new CarrinhoBuilder()
    .comUser(userPremium)
    .comItens([
        new Item('Produto A', 120),
        new Item('Produto B', 80),
    ])
    .build();
        """,
        styles,
    ))
    story.append(p(
        "A segunda versao deixa a intencao do teste mais evidente: o que importa e que o "
        "carrinho pertence a um cliente Premium e possui R$ 200,00 em itens. Os detalhes "
        "padrao ficam encapsulados no builder, reduzindo repeticao e setup obscuro.",
        styles,
    ))

    story.append(PageBreak())

    story.append(h1("2. Padroes de Test Doubles", styles))
    story.append(h2("2.1 Stub no cenario de falha de pagamento", styles))
    story.append(p(
        "No teste de falha, o GatewayPagamento foi usado como Stub. Sua funcao foi apenas "
        "controlar o fluxo do SUT retornando { success: false } quando cobrar fosse chamado. "
        "A verificacao principal foi de estado: o metodo processarPedido deveria retornar "
        "null e nao deveria persistir pedido nem enviar email.",
        styles,
    ))
    story.append(code(
        """
const gatewayStub = {
    cobrar: jest.fn().mockResolvedValue({ success: false }),
};

const pedido = await checkoutService.processarPedido(carrinho, cartaoCredito);

expect(pedido).toBeNull();
        """,
        styles,
    ))

    story.append(h2("2.2 Stub e Mock no cenario de sucesso Premium", styles))
    story.append(p(
        "No teste de sucesso para cliente Premium, o GatewayPagamento tambem atuou "
        "principalmente como Stub, pois retornou { success: true } para permitir que o fluxo "
        "continuasse. O PedidoRepository tambem foi usado como Stub, retornando um pedido "
        "salvo com id conhecido. Ja o EmailService foi usado como Mock, porque a finalidade "
        "do teste era verificar a interacao: se o email foi enviado uma vez e com os "
        "argumentos esperados.",
        styles,
    ))
    story.append(code(
        """
expect(gatewayStub.cobrar).toHaveBeenCalledWith(180, cartaoCredito);
expect(emailMock.enviarEmail).toHaveBeenCalledTimes(1);
expect(emailMock.enviarEmail).toHaveBeenCalledWith(
    'premium@email.com',
    'Seu Pedido foi Aprovado!',
    'Pedido 10 no valor de R$180',
);
        """,
        styles,
    ))
    story.append(p(
        "Essa separacao demonstra a diferenca entre verificacao de estado e verificacao de "
        "comportamento. O Stub ajuda a simular uma resposta externa e observar o resultado "
        "do SUT. O Mock, por sua vez, valida que uma colaboracao obrigatoria aconteceu da "
        "forma correta.",
        styles,
    ))

    story.append(h1("3. Conclusao", styles))
    story.append(p(
        "O uso deliberado de Object Mother, Data Builder, Stubs e Mocks torna a suite de "
        "testes mais sustentavel. Os builders reduzem setup obscuro e deixam cada teste "
        "expressar apenas o dado relevante para o cenario. Os test doubles isolam o "
        "CheckoutService de servicos externos, evitando testes frageis e lentos. Como "
        "resultado, a suite fica mais legivel, mais facil de manter e mais eficiente para "
        "detectar regressao nas regras de negocio.",
        styles,
    ))

    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Relatorio - Padroes de Teste",
        author="[preencher nome completo]",
    )
    doc.build(build_story(styles), onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(OUTPUT)


if __name__ == "__main__":
    main()
