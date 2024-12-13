"""
Utilities useful to develop simple console/terminal/text-mode based 
applications.
"""
import os
import subprocess


__all__ = [
    'accept',
    'show_msg',
    # TODO: terminar depois
]


DEFAULT_INDENTATION = 3

def accept(
        msg: str, 
        error_msg: str, 
        convert_fn = lambda x: x, 
        check_fn = lambda _: True,
        indent = DEFAULT_INDENTATION
):
    """
    TODO: write a proper doc string...
    """
    while True:
        value_str = ask(msg, indent = indent)
        if check_fn(value_str):
            try:
                return convert_fn(value_str)
            except Exception:
                pass
        # we reached this point iif the check failed or an
        # exception was raised
        show_msg(error_msg.format(value_str))
        pause('')
        cls()
#:

def confirm(msg: str, default = '', indent = DEFAULT_INDENTATION) -> bool:
    """
    >>> confirm("Do you like peanuts? ")
    Do you like peanuts? [yn] maybe
    Please answer Y or N.
    Do you like peanuts? [yn]
    An explicit awnser is required. Please answer Y or N.
    Do you like peanuts? [yn] n
    False
    >>> confirm("Will it rain tomorrow? ", default = 'Y')
    Will it rain tomorrow? [Yn] ja
    Please answer Y or N.
    Will it rain tomorrow? [Yn]
    True
    >>> confirm("Tomorrow is the day after yesterday? ", default = 'N')
    Tomorrow is the day after yesterday? [yN] nein
    Please answer Y or N.
    Tomorrow is the day after yesterday? [yN]
    False
    >>> confirm("Tomorrow is the day after yesterday? ", default = 'BATATAS')
    Traceback (most recent call last):
    ...
    ValueError: Invalid default value: BATATAS
    """
    default_text = {
        'Y': '[Yn]',
        'N': '[yN]',
        '': '[yn]'
    }.get(default)
    if default_text is None:
        raise ValueError(f"Invalid default value: {default}")
    msg += f'{default_text} '
    while True:
        ans = ask(msg, indent = indent).strip()
        match ans.upper():
            case 'Y' | 'YES':
                return True
            case 'N' | 'NO':
                return False
            case '':
                if default:
                    return default == 'Y'
                show_msg("An explicit answer is required. Please answer Y or N.", indent = indent)
            case _:
                print("Please answer Y or N.")
#:

def ask(msg: str, indent = DEFAULT_INDENTATION) -> str:
    return input(f"{indent * ' '}{msg}")
#:

def show_msg(*args, indent = DEFAULT_INDENTATION, **kargs):
    print_args = [' ' * (indent - 1), *args] if indent > 0 else [*args]
    print(*print_args, **kargs)
#:

def pause(msg: str="Pressione ENTER para continuar...", indent = DEFAULT_INDENTATION):
    msg = f"{' ' * indent}{msg}"
    match os.name:
        case 'nt':      # Windows (excepto Win9X)
            # pode ser inseguro! utilizar módulo subprocess se for...
            show_msg(msg)
            os.system("pause>null|set/p=''")
        case 'posix':   # Unixes e compatíveis
            subprocess.run(['read', '-s', '-n', '1', '-p', msg], check=True)
        case _:
            input(msg)
#:

def cls():
    """
    https://stackoverflow.com/questions/4553129/when-to-use-os-name-sys-platform-or-platform-system
    """
    match os.name:
        case 'nt':      # Windows (excepto Win9X)
            subprocess.run(['cls'], shell=True)
        case 'posix':   # Unixes e compatíveis
            subprocess.run(['clear'])
#:


"""
PROGRAMAÇÃO FUNCIONAL (INTRO);

# def filtra_pares(nums: Iterable) -> list:
#     encontrados = []
#     for num in nums:
#         if num % 2 == 0:
#             encontrados.append(num)
#     return encontrados
# #:

# def filtra_positivos(nums: Iterable) -> list:
#     encontrados = []
#     for num in nums:
#         if num > 0:
#             encontrados.append(num)
#     return encontrados
# #:

# criterio -> função que recebe um elemento e devolve ou True ou False
#             (ou seja, é uma função booleana)

nums = [10, -20, 31, 44, 73]
nomes = ('Alberto', 'Ana', 'Arnaldo', 'Zé')

def filtra(elems: Iterable, criterio) -> list:
    encontrados = []
    for elem in elems:
        if criterio(elem):
            encontrados.append(elem)
    return encontrados
#:

def is_positive(num) -> bool:
    return num > 0
#:

def cinco_ou_mais(txt: str) -> bool:
    return len(txt) >= 5
#:

filtra(nums, is_positive)
filtra(nomes, cinco_ou_mais)

filtra(nums, lambda num: num > 0)
filtra(nomes, lambda nome: len(nome) >= 5)


# EM PSEUDO-JS:
# 
# filtra(nums, (num) => num > 0)
# filtra(nums, function(num) { 
#     return num > 0;
# })

"""