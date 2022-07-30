# **********************************************************************************************************************
#    This is a derivation of Jay Damask's work from:
#       https://gitlab.com/thucyd-dev/thucyd, and,
#       https://gitlab.com/thucyd-dev/thucyd-eigen-working-examples
#    Original Copyright 2019 Buell Lane Press, LLC (buell-lane-press.co)
#    Licensed under Apache License, Version 2.0, January 2004, see http://www.apache.org/licenses/
#
#    Changes are Copyright (c) 2022 David Briant. All rights reserved.
#
# DESCRIPTION:
#       Implementation of the theory of consistently oriented eigenvectors
# **********************************************************************************************************************


import numpy as np

from coppertop.pipe import *
from coppertop.core import Missing
from dm.core.structs import tvseq
from ribs.types import num, count, offset, index, missing
# from dm.core.types import matrix, vec
from bones.lang.metatypes import BTTuple

vec = np.ndarray
matrix = np.ndarray

BTTuple(matrix, matrix, vec, matrix, vec).setCoercer(tvseq)
BTTuple(matrix, matrix).setCoercer(tvseq)




__all__ = ['orientEigenvectors', 'generate_oriented_eigenvectors']



@coppertop(style=nullary)
def orientEigenvectors(V:matrix, E:matrix) -> BTTuple(matrix, matrix, vec, matrix, vec):
    '''
    answers:
    
    Vor                 Eigenvector matrix cast into an oriented basis, see Note 1
    Eor                 Eigenvalue matrix conformant to Vor, see Note 2
    sign_flip_vector    Vector of signs that was applied to (sorted) `V` such that `Vor` is oriented
    theta_matrix        upper-trianglar matrix of angles embedded in `Vor` with respect to the constituent basis in
                        which (sorted) `V` is matrialized
    sort_indices        Permutation vector such that Vsort = V[:, sort_indices]


    `sign_flip_vector` is such that `Vor = V diag(sign_flip_vector)`, i.e. Vor is an oriented basis


    where:
    
    V                   Eigenvector matrix with columns vectors
    E                   Eigenvalue matrix conformant to V



    notes:

    1. The columns of `Vor` are ordered such that their associated eigenvalues are sorted in descending order of 
       absolute value. That the absolute value is taken on the eigenvalues is to treat the general case of an input 
       Hermitian matrix. For data analysis, SVD will generally yield a positive (semi)definite eigensystem, so negative 
       eigenvalues are not attained.

    2. The diagonal entries of `Eor` are ordered in descending absolute value of the input eigenvalue matrix `E`.

    '''

    
    Vsort, Esort, sort_indices = sortEigenvectors(V, E)
    Vwork = Vsort.copy()                                            # make a copy for local work
    n = Vwork.shape[0]
    angles2D = np.zeros(Vwork.shape)
    signFlips = np.zeros(n)

    for cursor in np.arange(n):
        signFlips[cursor] = 1.0 if Vwork[cursor, cursor] >= 0.0 else -1.0
        Vwork[:, cursor] *= signFlips[cursor]
        Vwork, angles = reduceDimensionByOne(n, cursor, Vwork)
        angles2D[cursor, :] = angles.T                              # persist the angles in an upper triangular matrix
    Vor = Vsort.dot(np.diag(signFlips))                             # calculate Vor, the right-handed basis for Vsort
    return (Vor, Esort, signFlips, angles2D, sort_indices) | BTTuple(matrix, matrix, vec, matrix, vec)


@coppertop
def generate_oriented_eigenvectors(angles2D:matrix, kth_eigenvector:index+missing=Missing) -> matrix:
    '''
    answers R, the rotation matrix

    where:

    angles2D            upper-triangular (n x n) matrix of angles
    kth_eigenvector     base(1) index of the eigenvector to rotate into its constituent axis


    The call `orientEigenvectors` consumes an eigenvector matrix `V` that is not necessarily oriented and
    returns `Vor`, its oriented counterpart. The `orientEigenvectors` call also returns `angles2D`.

    This function consumes `angles2D` (instead of `V`) to produce `Vor`, the oriented eigenvector matrix.

    Recall that

    (1)    Vor = V S = R

    where `S` is a diagonal matrix with +/- 1 entries, and `R` is a rotation matrix. `orientEigenvectors` computes
    `V S` while this function computes `R`.

    For a constituent basis I(n), the identity matrix, `R` rotates `I` into `Vor`,

    (2)    Vor = R I

    In this way we identify `R` with the rotation that brings `I` into alignment with `Vor`.

    Rotation matrix `R` itself is a cascade of rotations, one for each eigenvector,

    (3)    R = R_1 R_2 ... R_n

    Moreover, rotation R_k is itself a cascade of elemental Givens rotations. In R^4, the R_1 rotation is

    (4)    R_1(theta_(1,2), theta_(1,3), theta_(1,4)) =
                R_(1,2)(theta_(1,2))
                    x R_(1,3)(theta_(1,3))
                        x R_(1,4)(theta_(1,4))

    The angles are read from `angles2D` such that

              -                  -
              | 0  t12  t13  t14 |  <-- row for R_1
    ang_mtx = |    0    t23  t24 |  <-- row for R_2
              |    *    0    t34 |   ..
              |    *    *    0   |
              -                  -


    notes:

    The full dimension of the space, `n`, is inferred from the dimension of `angles2D`. Given `n`, the
    rotation matrix that corresponds to the kth eigenvector is constructed from elementary Givens rotations. In
    R^4, the rotation matrix for the 1st eigenvector is

    (1) R_1(theta_(1,2), theta_(1,3), theta_(1,4)) = R_(1,2)(theta_(1,2)) x R_(1,3)(theta_(1,3)) x R_(1,4)(theta_(1,4))

    The rotation matrix for the full eigenbasis in R^4 is

    (2) R = R_1 R_2 R_3 R_4

    '''

    n = angles2D.shape[0]

    if kth_eigenvector is not Missing:
        # evaluate (3) from the notes above
        cursor = kth_eigenvector - 1
        angles = angles2D[cursor, :].T  # conform to function interface
        R = constructSubspaceRotationMatrix(n, cursor, angles)

    else:
        # evaluate (4) from the notes above
        R = np.eye(n)
        for cursor in np.arange(n):
            angles = angles2D[cursor, :].T  # conform to function interface
            # Rk+1 = R_k.dot(R_(k+1))
            R = R.dot(
                constructSubspaceRotationMatrix(
                    n,
                    cursor,
                    angles)
            )

    return R


def reduceDimensionByOne(n:count, cursor:offset, Vwork:matrix) -> BTTuple(matrix, matrix):
    '''
    answers:

    Vwork       updated Vwork matrix
    angles      Givens rotation angles applied to input Vwork

    Transforms `Vwork` such that a 1 appears on the cursor pivot and the lower-right sub-space is, consequently, rotated

    where:

    n           dimension of the full space
    cursor     offset of the lower right subspace embedded in R^n
    Vwork       current workspace matrix such that the upper-left pivots outside of the current subspace are 1 while
                the lower-right subspace itself remains (almost surely) unaligned to the constituent basis


    The goal is to apply rotation matrix R.T such that the current sub-space dimension of Vwork is reduced by one. In
    block form,

            -            -     -            -
            | 1          |     | 1          |
     R.T x  |    *  *  * |  =  |    1       |
            |    *  *  * |     |       *  * |
            |    *  *  * |     |       *  * |
            -            -     -            -
    '''
    
    angles = solveRotationAnglesInSubdim(n, cursor, Vwork[:, cursor])
    R = constructSubspaceRotationMatrix(n, cursor, angles)      # construct subspace rotation matrix via a cascade of Givens rotations
    Vwork = R.T.dot(Vwork)                                      # Apply R.T to reduce the non-identity subspace by one dimension.
    return (Vwork, angles) | BTTuple(matrix, matrix)


def solveRotationAnglesInSubdim(n:count, cursor:offset, Vcol:vec) -> vec:
    '''
    answers a vector `angles` sized to the full dimension `n`

    Solves for embedded angles necessary to rotate a unit vector pointing along the `cursor` axis, within `n`,
    into the input `Vcol` vector.

    Recursive solution strategy to calculate rotation angles required to rotate the principal axis of a sub dimension
    onto an axis of its corresponding constituent basis.

    where:

    n           dimension of the full space
    cursor     offset the lower right subspace embedded in R^n
    Vcol        (column) vector in `n` whose elements at and above `cursor` will be matched by the
                rotation sequence


    notes:

    The recursion in this function solves for angles theta_2, theta_3, ... such that:

        -          -     -    -
        | c2 c3 c4 |     | v1 |
        | s2 c3 c4 |  =  | v2 |,  {s|c}k = {sin|cos}(theta_k)
        |   s3 c4  |     | v3 |
        |    s4    |     | v4 |
        -          -     -    -

    In particular, the arcsin recursion equations are implemented because they have better edge-case properties than
    the arctan recursion.
    '''
 
    subCursors = np.arange(cursor + 1, n)       # create scan array of sub-cursors as they range [cursor + 1: full-dim)
    angles = np.zeros(n + 1)                    # prepare for the recursion
    r = 1.0

    for subCursor in subCursors[::-1]:          # iterate over rows in subspace to calculate full 2-pi angles
        y = Vcol[subCursor]
        r *= np.cos(angles[subCursor + 1])
        angles[subCursor] = np.arcsin(y / r) if r != 0.0 else 0.0

    return angles[:n]                           # return work angles sized to n


def constructSubspaceRotationMatrix(n:count, cursor:offset, angles:vec) -> matrix:
    '''
    answers a rotation matrix 'R' that spans the subspace indicated by `cursor` by cascading a sequence of Givens
    rotations, thus:

    for `n` = 4 and `cursor` = 1

    -            --            -     -            -
    | 1          || 1          |     | 1          |
    |   c  -s    ||   c     -s |  =  |    *  *  * |
    |   s   c    ||      1     |     |    *  *  * |
    |          1 ||   s      c |     |    *  *  * |
    -            --            -     -            -
          ^              ^
      theta_2,3     theta_2,4               R

    where:

    n           dimension of the full space
    cursor     offset of the lower right subspace embedded in R^n
    angles      rotation angles in current subspace. This is a view on `angles2D` from the outer scope
    '''

    R = np.eye(n)
    subCursors = np.arange(cursor + 1, n)   # create scan array of sub-cursors as they range [cursor + 1: full-dim)
    # iterate over angles (reverse order), build a Givens matrix, and apply
    for subCursor in subCursors[::-1]:
        R = Givens(n, cursor, subCursor, angles[subCursor]).dot(R)
    return R


def Givens(n:count, cursor:offset, subCursor:offset, theta:num) -> matrix:
    '''
    answers a Givens matrix, such as for n = 4:

            -          -
            | 1        |
        R = |   c   -s |
            |     1    |
            |   s    c |
            -          -
                ^    ^
                |    |
             cursor  |
                sub-cursor

    where:

    n           dimension of the full space
    cursor     offset of the lower right subspace embedded in R^n
    subCursor  offset of the pivot position of the lower cos(.) entry
    theta       rotation angle
    '''

    R = np.eye(n)
    R[cursor, cursor] = np.cos(theta)
    R[cursor, subCursor] = -np.sin(theta)
    R[subCursor, cursor] = np.sin(theta)
    R[subCursor, subCursor] = np.cos(theta)
    return R


def sortEigenvectors(V:matrix, E:matrix) -> BTTuple(matrix, matrix, vec):
    # Given V a matrix of eigen col vectors and S a vector of eigen values answer the same but in S descending order
    diagE = np.diag(E)
    sort_indices = np.argsort(np.fabs(diagE))[::-1]     # descending sort of absolute values of E diag
    Vsort = V[:, sort_indices]
    Esort = np.diag(diagE[sort_indices])
    return Vsort, Esort, sort_indices
