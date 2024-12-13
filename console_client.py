import json
import sys

from products import PRODUCT_TYPES, Product, ProductCollection, InvalidProdAttr
from console_utils import accept, ask, show_msg, pause, cls


PRODUCTS_CSV_PATH = 'gestao_de_produtos_3/products.csv'
prods_collection: ProductCollection


def main():
    global prods_collection
    try: 
        prods_collection = ProductCollection.from_csv(PRODUCTS_CSV_PATH)
        exec_menu()
    except InvalidProdAttr as ex:
        print("Erro ao carregar produtos")
        print(ex)
    except KeyboardInterrupt:
        exec_end()
#:

def exec_menu():
    print("MENU PRINCIPAL")
    while True:
        cls()
        print()
        show_msg("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        show_msg("┃                                           ┃")
        show_msg("┃   L  - Listar catálogo                    ┃")
        show_msg("┃   P  - Pesquisar por id                   ┃")
        show_msg("┃   PT - Pesquisar por tipo                 ┃")
        show_msg("┃   A  - Acrescentar produto                ┃")
        show_msg("┃   E  - Eliminar produto                   ┃")
        show_msg("┃   G  - Guardar catálogo em ficheiro       ┃")
        show_msg("┃                                           ┃")
        show_msg("┃   T  - Terminar programa                  ┃")
        show_msg("┃                                           ┃")
        show_msg("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print()

        option = ask("  OPÇÃO> ")

        match option.upper():
            case 'L' | 'LISTAR':
                exec_list_products()
            case 'P' | 'PESQUISAR':
                exec_search_by_id()
            case 'PT' | 'TIPO':
                exec_search_by_type()
            case 'A' |'ACRESCENTAR':
                exec_add()
            case 'T' | 'TERMINAR':
                exec_end()
            case 'E' | 'ELIMINAR':
                exec_eliminate()
            case 'G' | 'GUARDAR':
                exec_save_catalog_to_file("catalogo.json", prods_collection)    
            case _:
                print("Opção inválida")

#:

def exec_add():
    enter_menu("ADICIONAR PRODUTO")
    print("Menu de adicionar produto iniciado.")
    
    try:
        # Solicita o ID do produto
        id_ = accept(
            msg="Indique o ID do produto: ",
            error_msg="ID inválido! Tente novamente.",
            convert_fn=int
        )        
        
        # Solicita o nome do produto
        name = accept(
            msg="Indique o nome do produto: ",
            error_msg="Nome não pode estar vazio! Tente novamente.",
            convert_fn=str
        ).strip()
       
        
        # Solicita o tipo do produto
        prod_type = accept(
            msg="Indique o tipo do produto ('AL', 'DL', 'FRL'): ",
            error_msg="Tipo inválido! Escolha entre 'AL', 'DL' ou 'FRL'.",
            convert_fn=str
        ).strip().upper()
        
        
        # Verifica se o tipo é válido
        if prod_type not in ['AL', 'DL', 'FRL']:
            raise ValueError("Tipo inválido! Escolha entre 'AL', 'DL' ou 'FRL'.")
        
        # Solicita a quantidade do produto
        quantity = accept(
            msg="Indique a quantidade do produto: ",
            error_msg="Quantidade inválida! Tente novamente.",
            convert_fn=int
        )
        
        
        # Solicita o preço do produto
        price = accept(
            msg="Indique o preço do produto: ",
            error_msg="Preço inválido! Tente novamente.",
            convert_fn=float  # Verifique se o construtor de Product usa float ou outro tipo
        )
       
        
        # Aqui, vamos criar o produto com todos os parâmetros
        new_product = Product(id_, name, prod_type, quantity, price)
        print(f"Produto criado: {new_product}")
        
        # Adiciona o produto à coleção
        prods_collection.append(new_product)
        print(f"Produto adicionado à coleção.")
        
        # Exibe uma mensagem de sucesso
        show_msg(f"Produto '{name}' adicionado com sucesso!")
    
    except Exception as e:
        show_msg(f"Ocorreu um erro ao adicionar o produto: {e}")
    
    print()
    pause()


#:

def exec_save_catalog_to_file(file_name, product_collection):
    # Acessa o atributo _products diretamente
    data = [
        {"id": product.id, "name": product.name, "quantity": product.quantity}
        for product in product_collection._products
    ]
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Catálogo guardado em '{file_name}'.")

#:

def exec_eliminate():
    enter_menu("ELIMINAR PRODUTO")
    show_table_with_prods(prods_collection)
    print()
    id_ = accept(
        msg = "Indique o ID do produto a eliminar: ",
        error_msg = "ID {} inválido! Tente novamente.",
        convert_fn = int,
    )
    if prod := prods_collection.search_by_id(id_):
        show_table_with_prods(ProductCollection([prod]))
        confirm = accept(
            msg="Produto encontrado. Confirma a exclusão do produto? (S/N): ",
            error_msg="Resposta inválida! Digite 'S' para Sim ou 'N' para Não.",
            convert_fn=lambda x: x.strip().upper(),
        )
        if confirm == "S":
            # Remove o produto
            prods_collection.remove_by_id(id_)
            show_msg(f"Produto com ID {id_} eliminado com sucesso.")
        else:
            show_msg("Operação cancelada. Nenhum produto foi eliminado.")
    else:
        show_msg(f"Produto com ID {id_} não encontrado.")    
    print()
    pause()
        
      
#:


def exec_list_products():
    enter_menu("PRODUTOS")
    show_table_with_prods(prods_collection)
    print()
    pause()
#:

def exec_search_by_id():
    enter_menu("PESQUISAR POR ID")
    id_ = accept(
        msg = "Indique o ID do produto a pesquisar: ",
        error_msg = "ID {} inválido! Tente novamente.",
        convert_fn = int,
    )
    
    if prod := prods_collection.search_by_id(id_):
        show_msg("Produto encontrado.")
        print()
        show_table_with_prods(ProductCollection([prod]))
    else:
        show_msg(f"Produto com ID {id_} não encontrado.")

    print()
    pause()
#:

def exec_search_by_type():
    enter_menu("PESQUISA POR TIPO")
    prod_type = accept(
        msg = "Indique o tipo do produto a pesquisar: ",
        error_msg = "Tipo {} inválido! Tente novamente",
        check_fn = lambda prod: prod in PRODUCT_TYPES,
    )
    print()

    if prods := prods_collection.search(lambda prod: prod.prod_type == prod_type):
        show_msg("Foram encontrados os seguintes produtos:")
        print()
        show_table_with_prods(ProductCollection(prods))
    else:
        show_msg(f"Não foram encontrados produtos com tipo {prod_type}.")

    print()
    pause()
#:

def exec_end():
    print("  O programa vai terminar...")
    sys.exit(0)
#:

def show_table_with_prods(prods: ProductCollection):
    header = f'{"ID":^8} | {"Nome":^26} | {"Tipo":^8} | {"Quantidade":^16} | {"Preço":^14}'
    sep = f'{"-" * 9}+{"-" * 28}+{"-" * 10}+{"-" * 18}+{"-" * 16}'

    show_msg(header)
    show_msg(sep)

    for prod in prods:
        data_line = f'{prod.id:^8} | {prod.name:<26} | {prod.prod_type:<8} | {prod.quantity:>16} | {prod.price:>14.2f}€'
        show_msg(data_line)
#:

def enter_menu(title: str):
    cls()
    show_msg(title.upper())
    print()
#:

if __name__ == "__main__":  # verifica se o script foi executado
    main()  # na linha de comandos


# y: int = 20

# def fun():
#     print(y)
#     # global y
#     # y = 10
