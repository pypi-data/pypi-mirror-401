import numpy as np
import pandas as pd


class Mapper:
    r"""A mapper to map ``(pkey, batch)`` pairs to contiguous node IDs.

    Args:
        num_examples: The maximum number of examples to add/retrieve.
    """
    def __init__(self, num_examples: int):
        self._pkey_dtype: pd.CategoricalDtype | None = None
        self._indices: list[np.ndarray] = []
        self._index_dtype: pd.CategoricalDtype | None = None
        self._num_examples = num_examples

    def add(self, pkey: pd.Series, batch: np.ndarray) -> None:
        r"""Adds a set of ``(pkey, batch)`` pairs to the mapper.

        Args:
            pkey: The primary keys.
            batch: The batch vector.
        """
        if self._pkey_dtype is not None:
            category = np.concatenate([
                self._pkey_dtype.categories.values,
                pkey,
            ], axis=0)
            category = pd.unique(category)
            self._pkey_dtype = pd.CategoricalDtype(category)
        elif pd.api.types.is_string_dtype(pkey):
            category = pd.unique(pkey)
            self._pkey_dtype = pd.CategoricalDtype(category)

        if self._pkey_dtype is not None:
            index = pd.Categorical(pkey, dtype=self._pkey_dtype).codes
            index = index.astype('int64')
        else:
            index = pkey.to_numpy()
        index = self._num_examples * index + batch
        self._indices.append(index)
        self._index_dtype = None

    def get(self, pkey: pd.Series, batch: np.ndarray) -> np.ndarray:
        r"""Retrieves the node IDs for a set of ``(pkey, batch)`` pairs.

        Returns ``-1`` for any pair not registered in the mapping.

        Args:
            pkey: The primary keys.
            batch: The batch vector.
        """
        if len(self._indices) == 0:
            return np.full(len(pkey), -1, dtype=np.int64)

        if self._index_dtype is None:  # Lazy build index:
            category = pd.unique(np.concatenate(self._indices))
            self._index_dtype = pd.CategoricalDtype(category)

        if self._pkey_dtype is not None:
            index = pd.Categorical(pkey, dtype=self._pkey_dtype).codes
            index = index.astype('int64')
        else:
            index = pkey.to_numpy()
        index = self._num_examples * index + batch

        out = pd.Categorical(index, dtype=self._index_dtype).codes
        out = out.astype('int64')
        return out
