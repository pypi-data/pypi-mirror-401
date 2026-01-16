
from __future__ import annotations
from copy import deepcopy
from typing import TypeAlias, Union, Literal

TreeType: TypeAlias = list[dict[Literal['exec', ''], list[Union[str, 'TreeType']]] | 'ExecComplier']

class ExecComplier:
    def __init__(self, tree: TreeType) -> None:
        self._tree: TreeType = deepcopy(tree)

    def __copy__(self) -> ExecComplier:
        return ExecComplier(self._tree)

    def __call__(self) -> str:
        tree: TreeType = self._tree
        if isinstance(tree, list):
            end_strlist: list[str] = []
            for _item in tree:
                item: dict[Literal['exec', 'call', ''], list[Union[str, 'TreeType']]] = _item._tree if isinstance(_item, ExecComplier) else _item # pyright: ignore[reportAssignmentType]
                key, value = next(iter(item.items()))
                if key == execute:
                    pass # TODO
                else: end_strlist.append(key)
            return '\n'.join(end_strlist)
        else:
            raise TypeError(f'Unknown type: {type(tree)}')

    @property
    def num(self):
        return deepcopy(self._tree)

preprocessing_directive: str = 'preprocessing_directive'
execute: str = 'exec'

if __name__ == '__main__':
    test: ExecComplier = ExecComplier([
        {'exec': ['expr', '3 * 4 + 5']}
    ])
