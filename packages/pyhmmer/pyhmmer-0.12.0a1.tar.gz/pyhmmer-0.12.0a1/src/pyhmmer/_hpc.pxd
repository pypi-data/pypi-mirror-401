# coding: utf-8
# cython: language_level=3, linetrace=True

cimport openmp
from libc.stdlib cimport malloc, free
from libeasel.sq cimport ESL_SQ
from libhmmer.p7_bg cimport P7_BG
from libhmmer.p7_pipeline cimport P7_PIPELINE, p7_pipemodes_e
from libhmmer.p7_profile cimport P7_PROFILE
from libhmmer.p7_tophits cimport P7_TOPHITS

IF HMMER_IMPL == "VMX":
    from libhmmer.impl_vmx.p7_oprofile cimport P7_OPROFILE
ELIF HMMER_IMPL == "SSE":
    from libhmmer.impl_sse.p7_oprofile cimport P7_OPROFILE

from .easel cimport Alphabet, SequenceFile, DigitalSequence
from .plan7 cimport Background, Profile, OptimizedProfile, Pipeline


cdef class _HMMSearch:

    cdef int      cpus
    cdef int      blocksize
    cdef object   queries
    cdef object   callback

    cdef Alphabet alphabet

    cdef Background  background
    cdef P7_BG*     _background

    cdef list          profiles
    cdef P7_PROFILE** _profiles

    cdef list           oprofiles
    cdef P7_OPROFILE** _oprofiles

    cdef list       sequences
    cdef ESL_SQ**  _sequences

    cdef list           pipelines
    cdef P7_PIPELINE** _pipelines

    cdef list          results
    cdef P7_TOPHITS**  _results
