#include "includes.cpp"


constexpr i64 ZLIB_BUFFER_SIZE = 32768; // 32 kB
constexpr i64 ZLIB_MAX_SIZE = 1073741824; // 1 GB


int get_zlib_window_bits(str format) {
    std::transform(format.begin(), format.end(), format.begin(), ::tolower);
    if (format == "gzip" || format == "gz") {
        return 15 + 16; // 15 base + 16 for gzip
    } else if (format == "zlib") {
        return 15; // default zlib
    } else if (format == "deflate") {
        return -15; // raw deflate
    } else {
        throw std::invalid_argument("invalid compression format: " + format);
    }
}


#ifndef NO_ZLIB


std::vector<u8> compress_bytes(
    const std::vector<u8>& data,
    str format = "gzip",
    i8 compression_level = 1
) {
    uLong compressed_size = compressBound(static_cast<uLong>(data.size()));
    std::vector<u8> compressed_data(compressed_size);
    z_stream stream{};
    stream.avail_in = static_cast<uInt>(data.size());
    stream.next_in = const_cast<Bytef*>(data.data());
    stream.avail_out = static_cast<uInt>(compressed_size);
    stream.next_out = compressed_data.data();
    int window_bits = get_zlib_window_bits(format);
    int init_result = deflateInit2(&stream, compression_level, Z_DEFLATED, window_bits, 8, Z_DEFAULT_STRATEGY);
    if (init_result != Z_OK) {
        throw std::runtime_error(
            "failed to initialize zlib for compression: " + 
            str(stream.msg ? stream.msg : "unknown error"));
    }
    int ret = deflate(&stream, Z_FINISH);
    if (ret != Z_STREAM_END) {
        str error_msg = "zlib compression of " +
            std::to_string(data.size()) + " bytes failed: ";
        if (ret == Z_OK) {
            error_msg += "incomplete compression";
        } else if (ret == Z_STREAM_ERROR) {
            error_msg += "invalid compression level or parameters";
        } else if (ret == Z_BUF_ERROR) {
            error_msg += "no progress possible or output buffer too small";
        } else {
            error_msg += "error code " + std::to_string(ret);
        }
        if (stream.msg) error_msg += " (" + str(stream.msg) + ")";
        deflateEnd(&stream);
        throw std::runtime_error(error_msg);
    }
    compressed_data.resize(stream.total_out);
    deflateEnd(&stream);
    return compressed_data;
}


std::vector<u8> decompress_bytes(
    const std::vector<u8>& data,
    i64 buffer_size = ZLIB_BUFFER_SIZE,
    i64 max_size = 1073741824
) {
    if (buffer_size < 1 || buffer_size > max_size) {
        throw std::runtime_error("buffer size " + std::to_string(buffer_size) + " invalid");
    }
    std::vector<u8> decompressed_data;
    std::vector<u8> buffer(buffer_size);
    z_stream stream{};
    stream.avail_in = static_cast<uInt>(data.size());
    stream.next_in = const_cast<Bytef*>(data.data());
    int init_result = inflateInit2(&stream, 15 + 32);
    if (init_result != Z_OK) {
        throw std::runtime_error(
            "failed to initialize zlib for decompression: " + 
            str(stream.msg ? stream.msg : "unknown error"));
    }
    while (true) {
        stream.avail_out = static_cast<uInt>(buffer_size);
        stream.next_out = buffer.data();
        int ret = inflate(&stream, Z_NO_FLUSH);
        if (ret != Z_OK && ret != Z_STREAM_END) {
            str error_msg = "zlib decompression of " +
                std::to_string(data.size()) + " bytes failed: ";
            if (ret == Z_STREAM_ERROR) {
                error_msg += "invalid compression level";
            } else if (ret == Z_DATA_ERROR) {
                error_msg += "invalid or incomplete deflate data";
            } else if (ret == Z_MEM_ERROR) {
                error_msg += "out of memory";
            } else if (ret == Z_BUF_ERROR) {
                error_msg += "no progress possible or output buffer too small";
            } else {
                error_msg += "error code " + std::to_string(ret);
            }
            if (stream.msg) error_msg += " (" + str(stream.msg) + ")";
            inflateEnd(&stream);
            throw std::runtime_error(error_msg);
        }
        i64 decompressed = buffer_size - stream.avail_out;
        if (decompressed_data.size() + decompressed > static_cast<u64>(max_size)) {
            inflateEnd(&stream);
            throw std::runtime_error("decompressed data exceeds limit (" + std::to_string(max_size) + ")");
        }
        if (ret == Z_STREAM_END && decompressed_data.size() == 0 && decompressed == buffer_size) {
            decompressed_data = std::move(buffer);
            break;
        }
        decompressed_data.insert(decompressed_data.end(), buffer.begin(), buffer.begin() + decompressed);
        if (ret == Z_STREAM_END) break;
    }
    inflateEnd(&stream);
    return decompressed_data;
}


#else


std::vector<u8> compress_bytes(
    const std::vector<u8>& data,
    str format = "gzip",
    i8 compression_level = 1
) {
    int window_bits = get_zlib_window_bits(format);
    py::gil_scoped_acquire acquire;
    
    try {
        py::module_ zlib = py::module_::import("zlib");
        
        // Convert vector to bytes
        py::bytes data_bytes(reinterpret_cast<const char*>(data.data()), data.size());
        
        // Call zlib.compress with appropriate wbits
        py::object compressobj = zlib.attr("compressobj")(compression_level, py::int_(8), window_bits);
        py::bytes compressed_part = compressobj.attr("compress")(data_bytes);
        py::bytes compressed_final = compressobj.attr("flush")();
        
        // Concatenate the two parts
        std::string_view sv1 = compressed_part.cast<std::string>();
        std::string_view sv2 = compressed_final.cast<std::string>();
        std::vector<u8> result(sv1.begin(), sv1.end());
        result.insert(result.end(), sv2.begin(), sv2.end());
        
        return result;
    } catch (const py::error_already_set& e) {
        throw std::runtime_error(std::string("python zlib compress error: ") + e.what());
    }
}


std::vector<u8> decompress_bytes(
    const std::vector<u8>& data,
    [[maybe_unused]] i64 buffer_size = ZLIB_BUFFER_SIZE,
    [[maybe_unused]] i64 max_size = ZLIB_MAX_SIZE
) {
    py::gil_scoped_acquire acquire;
    
    try {
        py::module_ zlib = py::module_::import("zlib");
        
        // Convert vector to bytes
        py::bytes data_bytes(reinterpret_cast<const char*>(data.data()), data.size());
        
        // Call zlib.decompress
        py::bytes decompressed = zlib.attr("decompress")(data_bytes, 15 + 32);
        
        // Convert back to vector
        std::string_view sv = decompressed.cast<std::string>();
        return std::vector<u8>(sv.begin(), sv.end());
    } catch (const py::error_already_set& e) {
        throw std::runtime_error(std::string("python zlib decompress error: ") + e.what());
    }
}


class PyCompressionInChunks {
    py::module_ zlib;
    py::object compressobj;
    bool compute_crc32;

public:
    u32 crc32;

    PyCompressionInChunks(
        str format = "gzip",
        i8 compression_level = 1,
        bool compute_crc32 = false
    ) : compute_crc32(compute_crc32), crc32(0) {
        py::gil_scoped_acquire acquire;

        try {
            zlib = py::module_::import("zlib");
            int window_bits = get_zlib_window_bits(format);
            compressobj = zlib.attr("compressobj")(
                compression_level,
                zlib.attr("DEFLATED"),
                window_bits
            );
        } catch (const py::error_already_set& e) {
            throw std::runtime_error(std::string("python zlib compressobj error: ") + e.what());
        }        
    }

    std::vector<u8> compress_chunk(std::vector<u8>& data) {
        py::gil_scoped_acquire acquire;

        try {
            py::bytes data_bytes(reinterpret_cast<const char*>(data.data()), data.size());
            py::bytes compressed_part = compressobj.attr("compress")(data_bytes);
            if (compute_crc32) crc32 = zlib.attr("crc32")(data_bytes, crc32).cast<u32>();
            std::string_view sv = compressed_part;
            return std::vector<u8>(sv.begin(), sv.end());
        } catch (const py::error_already_set& e) {
            throw std::runtime_error(std::string("python zlib compress chunk error: ") + e.what());
        }
    }

    std::vector<u8> flush() {
        py::gil_scoped_acquire acquire;

        try {
            py::bytes compressed_final = compressobj.attr("flush")();
            std::string_view sv = compressed_final;
            return std::vector<u8>(sv.begin(), sv.end());
        } catch (const py::error_already_set& e) {
            throw std::runtime_error(std::string("python zlib flush error: ") + e.what());
        }
    }

};


class PyDecompressionInChunks {
    py::module_ zlib;
    py::object decompressobj;

public:
    PyDecompressionInChunks() {
        py::gil_scoped_acquire acquire;

        try {
            zlib = py::module_::import("zlib");
            decompressobj = zlib.attr("decompressobj")(15 + 32); // Auto-detect gzip/zlib
        } catch (const py::error_already_set& e) {
            throw std::runtime_error(std::string("python zlib decompressobj error: ") + e.what());
        }        
    }

    std::vector<u8> decompress_chunk(std::vector<u8>& data) {
        py::gil_scoped_acquire acquire;

        try {
            py::bytes data_bytes(reinterpret_cast<const char*>(data.data()), data.size());
            py::bytes decompressed_part = decompressobj.attr("decompress")(data_bytes);
            std::string_view sv = decompressed_part; 
            return std::vector<u8>(sv.begin(), sv.end());
        } catch (const py::error_already_set& e) {
            throw std::runtime_error(std::string("python zlib decompress chunk error: ") + e.what());
        }
    }

    std::vector<u8> flush() {
        py::gil_scoped_acquire acquire;

        try {
            py::bytes remaining = decompressobj.attr("flush")();
            std::string_view sv = remaining;
            return std::vector<u8>(sv.begin(), sv.end());
        } catch (const py::error_already_set& e) {
            throw std::runtime_error(std::string("python zlib flush error: ") + e.what());
        }
    }

};


#endif
