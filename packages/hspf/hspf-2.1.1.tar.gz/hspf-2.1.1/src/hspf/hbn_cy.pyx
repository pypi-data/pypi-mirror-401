# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True
# hbn_cy.pyx - Cython helpers for reading HBN binary files
from cpython.bytes cimport PyBytes_AsStringAndSize
cimport cython
import numpy as np
cimport numpy as cnp
from datetime import datetime, timedelta

@cython.inline
cdef unsigned int _read_uint32_le(const unsigned char* buf, Py_ssize_t offset) nogil:
    """Reads a little-endian unsigned 32-bit integer."""
    return buf[offset] | (buf[offset+1] << 8) | (buf[offset+2] << 16) | (buf[offset+3] << 24)

@cython.boundscheck(False)
@cython.wraparound(False)
def map_hbn_file(str file_path):
    """
    Parses an HBN file from a file path to produce mapn and mapd dictionaries.
    Returns (mapn, mapd, data_bytes).
    """
    cdef:
        bytes data_bytes
        const unsigned char* cbuf
        Py_ssize_t buf_len, index = 1, i, slen, ln
        unsigned int rectype, tcode, idval, reclen
        unsigned char rc1, rc2, rc3, rc
        dict mapn = {}
        dict mapd = {}

    with open(file_path, 'rb') as f:
        data_bytes = f.read()
    if not data_bytes:
        raise ValueError(f"File is empty: {file_path}")

    PyBytes_AsStringAndSize(data_bytes, <char **>&cbuf, &buf_len)
    if cbuf[0] != 0xFD:
        raise ValueError("BAD HBN FILE - must start with magic number 0xFD")

    while index < buf_len:
        if index + 28 > buf_len: break
        rc1 = cbuf[index]; rc2 = cbuf[index+1]; rc3 = cbuf[index+2]; rc = cbuf[index+3]
        rectype = _read_uint32_le(cbuf, index + 4)
        idval = _read_uint32_le(cbuf, index + 16)
        reclen = (<unsigned int>(rc) * 4194304) + (<unsigned int>(rc3) * 16384) + (<unsigned int>(rc2) * 64) + (<unsigned int>(rc1) >> 2) - 24

        operation = data_bytes[index+8:index+16].decode('ascii', 'ignore').strip()
        activity = data_bytes[index+20:index+28].decode('ascii', 'ignore').strip()

        if rectype == 1:  # data record
            if index + 36 > buf_len: break
            tcode = _read_uint32_le(cbuf, index + 32)
            key = (operation, idval, activity, int(tcode))
            if key not in mapd: mapd[key] = []
            mapd[key].append((index, reclen))
        elif rectype == 0:  # data names record
            key = (operation, idval, activity)
            if key not in mapn: mapn[key] = []
            i = index + 28
            slen = 0
            while slen < reclen:
                if i + slen + 4 > buf_len: break
                ln = _read_uint32_le(cbuf, i + slen)
                if i + slen + 4 + ln > buf_len: break
                name = data_bytes[i + slen + 4 : i + slen + 4 + ln].decode('ascii', 'ignore').strip().replace('-', '')
                mapn[key].append(name)
                slen += 4 + ln
        
        if reclen < 36: index += reclen + 29
        else: index += reclen + 30

    return mapn, mapd, data_bytes

@cython.boundscheck(False)
@cython.wraparound(False)
def read_data_entries(bytes data_bytes, list entries, int nvals):
    """
    Reads data entries from the file's bytes. Returns (times, rows_array).
    """
    cdef:
        const unsigned char* cbuf
        Py_ssize_t buf_len, num_entries = len(entries), k, idx
        unsigned int yr, mo, dy, hr, mn
        cnp.ndarray[cnp.float32_t, ndim=2] rows2d = np.empty((num_entries, nvals), dtype=np.float32)
        list times = [None] * num_entries

    PyBytes_AsStringAndSize(data_bytes, <char **>&cbuf, &buf_len)

    for k in range(num_entries):
        idx = entries[k][0] # Get just the index from the (index, reclen) tuple
        
        # Boundary check for safety
        if idx + 56 + (nvals * 4) > buf_len: continue

        yr = _read_uint32_le(cbuf, idx + 36)
        mo = _read_uint32_le(cbuf, idx + 40)
        dy = _read_uint32_le(cbuf, idx + 44)
        hr = _read_uint32_le(cbuf, idx + 48)
        mn = _read_uint32_le(cbuf, idx + 52)
        
        try:
            times[k] = datetime(int(yr), int(mo), int(dy), int(hr) - 1, int(mn))
        except ValueError:
            times[k] = datetime(1900, 1, 1) # Fallback for bad date data

        rows2d[k] = np.frombuffer(data_bytes, dtype=np.float32, count=nvals, offset=idx + 56)
        
    return times, rows2d