# **********************************************************************************************************************
#
#                             Copyright (c) 2021-2022 David Briant. All rights reserved.
#
# BSD 3-Clause License
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
#    following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#    following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# **********************************************************************************************************************


@coppertop(style=binary)
# def partitions_(es:N**T, sizes:N**index) -> N**N**N**T:
def partitions(es, sizes: pylist):
    sizes >> sum >> check >> equal >> (es >> count)
    return list(es) >> _partitions(_, es >> count, sizes)


@coppertop
# def _partitions2(es:N**T, n:index, sizes:N**index) -> N**N**(N**T):
def _partitions(es: pylist, n: index, sizes: pylist) -> pylist:
    if not sizes: return [[]]
    return es >> _combRest2(_, n, sizes >> first) \
        >> each >> (unpack >> (lambda x, y:
            y >> _partitions(_, n - (sizes >> first), sizes >> drop >> 1)
                >> each >> (lambda partitions:
                    x >> prependTo >> partitions
                )
        )) \
        >> joinAll


@coppertop
# def _combRest2(es:N**T, n:index, m:index) -> N**( (N**T)*(N**T) ):
def _combRest2(es: pylist, n: index, m: index) -> pylist:
    '''answer [m items chosen from n items, the rest]'''
    if m == 0: return [([], es)]
    if m == n: return [(es, [])]
    return \
        es >> drop >> 1 >> _combRest2(_, n - 1, m - 1) >> each >> (unpack >> (lambda x, y: (es >> take >> 1 >> join >> x, y))) \
        >> join >> (
        es >> drop >> 1 >> _combRest2(_, n - 1, m) >> each >> (unpack >> (lambda x, y: (x, es >> take >> 1 >> join >> y)))
        )


@coppertop(style=binary)
def prependTo(x, xs: pylist) -> pylist:
    return [x] + xs


@coppertop(style=rau)
def unpack(f):
    return lambda xy: f(xy[0], xy[1])  # needs to return a pipeable?

#%timeit range(13) >> partitions2_ >> [5,4,4] >> count >> PP
# 18 s ± 93.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
