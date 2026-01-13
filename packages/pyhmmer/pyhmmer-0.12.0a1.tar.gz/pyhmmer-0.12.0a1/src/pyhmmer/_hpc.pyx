# coding: utf-8
# cython: language_level=3, linetrace=True

cimport openmp
from cython.parallel import prange
from libc.stdlib cimport malloc, free
from libc.stdio cimport printf
from libeasel.sq cimport ESL_SQ

IF HMMER_IMPL == "VMX":
    from libhmmer.impl_vmx cimport p7_oprofile
ELIF HMMER_IMPL == "SSE":
    from libhmmer.impl_sse cimport p7_oprofile

from .easel cimport Alphabet, SequenceFile, DigitalSequence
from .plan7 cimport Background, HMM, Pipeline, Profile, OptimizedProfile, TopHits

import queue
from .utils import peekable



cdef class _HMMSearch:

    def __init__(self, queries, sequences, cpus=0, callback=None, blocksize=100, **options):

        cdef DigitalSequence  seq
        cdef Profile          profile
        cdef OptimizedProfile oprofile
        cdef Pipeline         pipeline

        self.queries = peekable(queries)
        self.sequences = list(sequences)
        self.alphabet = self.queries.peek().alphabet
        self.cpus = cpus if cpus > 0 else openmp.omp_get_max_threads()
        self.callback = callback
        self.blocksize = blocksize

        # create one pipeline for each CPU
        self._pipelines = <P7_PIPELINE**> malloc(sizeof(P7_PIPELINE*) * self.cpus * self.blocksize)
        self.pipelines = []
        for i in range(self.cpus * self.blocksize):
            pipeline = Pipeline(alphabet=self.alphabet, **options)
            self.pipelines.append(pipeline)
            self._pipelines[i] = pipeline._pli

        # store background model
        self.background = Background(self.alphabet)
        self._background = self.background._bg

        # store sequences
        self._sequences = <ESL_SQ**> malloc(sizeof(ESL_SQ*) * (len(self.sequences) + 1))
        for i, seq in enumerate(sequences):
            self._sequences[i] = seq._sq
        self._sequences[len(self.sequences)] = NULL

        # create buffers to store profiles
        self._profiles = <P7_PROFILE**> malloc(sizeof(P7_PROFILE*) * self.cpus * self.blocksize)
        self.profiles = []
        for i in range(self.cpus * self.blocksize):
            profile = Profile(200, self.alphabet)
            self.profiles.append(profile)
            self._profiles[i] = profile._gm

        # create buffers to store optimized profiles
        self._oprofiles = <P7_OPROFILE**> malloc(sizeof(P7_OPROFILE*) * self.cpus * self.blocksize)
        self.oprofiles = []
        for i in range(self.cpus * self.blocksize):
            oprofile = self.profiles[i].optimized()
            self.oprofiles.append(oprofile)
            self._oprofiles[i] = oprofile._om

        # create buffers to store results
        self._results = <P7_TOPHITS**> malloc(sizeof(P7_TOPHITS*) * self.cpus * self.blocksize)
        self.results = []

    def __dealloc__(self):
        free(self._sequences)
        free(self._results)
        free(self._oprofiles)
        free(self._profiles)

    def __iter__(self):
        return self

    def __next__(self):

        cdef ssize_t          i
        cdef ssize_t          j
        # cdef HMM              hmm
        cdef Profile          profile
        cdef OptimizedProfile oprofile
        cdef TopHits          top_hits

        # cdef list             hmms        = []
        cdef int              cpus        = self.cpus
        cdef int              blocksize   = self.blocksize
        cdef P7_OPROFILE**    _oprofiles  = self._oprofiles
        cdef P7_BG*           _background = self._background
        cdef ESL_SQ**         _sequences  = self._sequences
        cdef P7_PIPELINE**    _pipelines  = self._pipelines
        cdef P7_TOPHITS**     _results    = self._results


        if self.results:
            return self.results.pop(0)

        for i in prange(cpus*blocksize, nogil=True, schedule="dynamic"):
            hmm = next(self.queries, None)
            if hmm is not None:
                if hmm.M > self._profiles[i].M:
                    profile = Profile(hmm.M, self.alphabet)
                    self.profiles[i] = profile
                    self._profiles[i] = profile._gm
                    oprofile = OptimizedProfile(hmm.M, self.alphabet)
                    self.oprofiles[i] = oprofile
                    self._oprofiles[i] = oprofile._om

                profile = self.profiles[i]
                profile._configure(hmm, self.pipelines[i].background, len(self.sequences[0]))
                p7_oprofile.p7_oprofile_Convert(self._profiles[i], self._oprofiles[i])

                top_hits = TopHits()
                self.results.append(top_hits)
                self._results[i] = top_hits._th
                # hmms.append(hmm)
            else:
                self.profiles[i] = self.oprofiles[i] = None
                self._profiles[i] = self._oprofiles[i]  = self._results[i] = NULL

        if not self.results:
            raise StopIteration

        for i in prange(cpus*blocksize, nogil=True, schedule="dynamic"):
            if _oprofiles[i] != NULL:
                Pipeline._search_loop(
                    _pipelines[i],
                    _oprofiles[i],
                    _background,
                    _sequences,
                    _results[i],
                )

        for i in range(cpus * blocksize):
            # sort and threshold results
            if _oprofiles[i] != NULL:
                top_hits = self.results[i]
                top_hits._sort_by_key()
                top_hits._threshold(self.pipelines[i])
            # reset pipelines for next run
            self.pipelines[i].clear()

        return self.results.pop(0)
