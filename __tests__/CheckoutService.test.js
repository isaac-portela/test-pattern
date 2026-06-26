import { CheckoutService } from '../src/services/CheckoutService.js';
import { Item } from '../src/domain/Item.js';
import { Pedido } from '../src/domain/Pedido.js';
import { CarrinhoBuilder } from './builders/CarrinhoBuilder.js';
import { UserMother } from './builders/UserMother.js';

describe('CheckoutService', () => {
    const cartaoCredito = {
        numero: '4111111111111111',
        validade: '12/30',
        cvv: '123',
    };

    describe('quando o pagamento falha', () => {
        test('retorna null e nao persiste nem envia email', async () => {
            // Arrange
            const carrinho = new CarrinhoBuilder().build();
            const gatewayStub = {
                cobrar: jest.fn().mockResolvedValue({ success: false }),
            };
            const repositoryDummy = {
                salvar: jest.fn(),
            };
            const emailDummy = {
                enviarEmail: jest.fn(),
            };
            const checkoutService = new CheckoutService(
                gatewayStub,
                repositoryDummy,
                emailDummy,
            );

            // Act
            const pedido = await checkoutService.processarPedido(carrinho, cartaoCredito);

            // Assert
            expect(pedido).toBeNull();
            expect(repositoryDummy.salvar).not.toHaveBeenCalled();
            expect(emailDummy.enviarEmail).not.toHaveBeenCalled();
        });
    });

    describe('quando um cliente Premium finaliza a compra', () => {
        test('aplica desconto, salva o pedido e envia email de aprovacao', async () => {
            // Arrange
            const userPremium = UserMother.umUsuarioPremium();
            const carrinho = new CarrinhoBuilder()
                .comUser(userPremium)
                .comItens([
                    new Item('Produto A', 120),
                    new Item('Produto B', 80),
                ])
                .build();
            const pedidoSalvo = new Pedido(10, carrinho, 180, 'PROCESSADO');
            const gatewayStub = {
                cobrar: jest.fn().mockResolvedValue({ success: true }),
            };
            const repositoryStub = {
                salvar: jest.fn().mockResolvedValue(pedidoSalvo),
            };
            const emailMock = {
                enviarEmail: jest.fn().mockResolvedValue(undefined),
            };
            const checkoutService = new CheckoutService(
                gatewayStub,
                repositoryStub,
                emailMock,
            );

            // Act
            const pedido = await checkoutService.processarPedido(carrinho, cartaoCredito);

            // Assert
            expect(pedido).toBe(pedidoSalvo);
            expect(gatewayStub.cobrar).toHaveBeenCalledWith(180, cartaoCredito);
            expect(repositoryStub.salvar).toHaveBeenCalledWith(
                expect.objectContaining({
                    carrinho,
                    totalFinal: 180,
                    status: 'PROCESSADO',
                }),
            );
            expect(emailMock.enviarEmail).toHaveBeenCalledTimes(1);
            expect(emailMock.enviarEmail).toHaveBeenCalledWith(
                'premium@email.com',
                'Seu Pedido foi Aprovado!',
                'Pedido 10 no valor de R$180',
            );
        });
    });
});
