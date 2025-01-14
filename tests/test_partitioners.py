# -*- coding: utf-8 -*-
from __future__ import absolute_import
from new_frontera.contrib.backends.partitioners import (
    FingerprintPartitioner,
    Crc32NamePartitioner,
)
from six.moves import range


def test_fingerprint_partitioner():
    partitions = list(range(0, 5))
    fp = FingerprintPartitioner(partitions)
    key = "1be68ff556fd0bbe5802d1a100850da29f7f15b1"
    partition = fp.partition(key, partitions)
    assert partition == 2

    partition = fp.partition(key, None)
    assert partition == 2


def test_crc32name_partitioner():
    partitions = list(range(0, 5))
    cp = Crc32NamePartitioner(partitions)
    key = "1be68ff556fd0bbe5802d1a100850da29f7f15b11"
    partition = cp.partition(key, partitions)
    assert partition == 3

    partition = cp.partition(None, partitions)
    assert partition == 0

    partition = cp.partition(key, None)
    assert partition == 3
