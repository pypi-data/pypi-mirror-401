#include "util/main.cpp"


class BAMEntryFlag {
public:
    u16 value;

    BAMEntryFlag(u16 value) : value(value) {}

    bool paired() const {
        return (value & 0x1) != 0;
    }
    bool paired_properly() const {
        return (value & 0x2) != 0;
    }
    bool mapped() const {
        return (value & 0x4) == 0;
    }
    bool next_mapped() const {
        return (value & 0x8) == 0;
    }
    bool reversed() const {
        return (value & 0x10) != 0;
    }
    bool next_reversed() const {
        return (value & 0x20) != 0;
    }
    bool first_in_pair() const {
        return (value & 0x40) != 0;
    }
    bool last_in_pair() const {
        return (value & 0x80) != 0;
    }
    bool secondary_or_supplementary() const {
        if ((value & 0x100) != 0) return true;
        if ((value & 0x800) != 0) return true;
        return false;
    }
    bool failed_qc_or_duplicate() const {
        if ((value & 0x200) != 0) return true;
        if ((value & 0x400) != 0) return true;
        return false;
    }

};


class BAMCigar {
public:
    std::vector<u32> encoded;

    BAMCigar(const std::vector<u32>& encoded) : encoded(encoded) {}

    i64 reference_length() const {
        i64 ref_len = 0;
        for (const auto& cigar_op : encoded) {
            u32 op = cigar_op & 0xF;
            u32 len = cigar_op >> 4;
            // M, D, N, =, X consume reference
            if (op == 0 || op == 2 || op == 3 || op == 7 || op == 8) {
                ref_len += len;
            }
        }
        return ref_len;
    }

    i64 query_length() const {
        i64 query_len = 0;
        for (const auto& cigar_op : encoded) {
            u32 op = cigar_op & 0xF;
            u32 len = cigar_op >> 4;
            // M, I, S, =, X consume query
            if (op == 0 || op == 1 || op == 4 || op == 7 || op == 8) {
                query_len += len;
            }
        }
        return query_len;
    }

    str decoded() const {
        static const char cigar_ops[] = "MIDNSHP=X";
        str result;
        for (const auto& cigar_op : encoded) {
            u32 op = cigar_op & 0xF; // operation (0-8)
            u32 len = cigar_op >> 4; // length
            result += std::to_string(len);
            if (op < 9) {
                result += cigar_ops[op];
            } else {
                result += '?'; // invalid operation
            }
        }
        return result;
    }

};


class BAMSequence {
public:
    std::vector<u8> encoded;
    std::vector<u8> encoded_qualities;

    BAMSequence(
        const std::vector<u8>& encoded,
        const std::vector<u8>& encoded_qualities
    ) : encoded(encoded), encoded_qualities(encoded_qualities) {}

    str decoded() const {
        static const char seq_lookup[] = "=ACMGRSVTWYHKDBN";
        str result;
        i64 l_seq = static_cast<i64>(encoded.size()) * 2;
        result.reserve(l_seq);
        for (i64 i = 0; i < l_seq; ++i) {
            u8 encoded_byte = encoded[i / 2];
            u8 base_code = (i % 2 == 0) ? (encoded_byte >> 4) : (encoded_byte & 0xF);
            result += seq_lookup[base_code];
        }
        return result;
    }

    str decoded_qualities() const {
        str result;
        result.reserve(encoded_qualities.size());
        for (const auto& qual_byte : encoded_qualities) {
            if (qual_byte == 0xFF) {
                result += '*'; // missing quality
            } else {
                result += static_cast<char>(qual_byte + 33); // convert to ASCII
            }
        }
        return result;
    }

};


class BAMEntryTags {
public:
    std::unordered_map<str, std::tuple<char, char, ByteArray>> tags;

    std::vector<str> get_all_with_type(str type_name) const {
        std::set<char> matching_codes;
        if (type_name == "char") {
            matching_codes = {'A'};
        } else if (type_name == "int") {
            matching_codes = {'c', 'C', 's', 'S', 'i', 'I'};
        } else if (type_name == "float") {
            matching_codes = {'f'};
        } else if (type_name == "string") {
            matching_codes = {'Z', 'H'};
        } else if (type_name == "int_array" || type_name == "float_array") {
            matching_codes = {'B'};
        }
        std::vector<str> matching_tags;
        for (const auto& [tag, value] : tags) {
            auto& [type, subtype, data] = value;
            if (matching_codes.count(type) == 0) continue;
            if (type == 'B') {
                if (type_name == "int_array" && (
                    subtype == 'c' || subtype == 'C' || 
                    subtype == 's' || subtype == 'S' || 
                    subtype == 'i' || subtype == 'I')) {
                    matching_tags.push_back(tag);
                } else if (type_name == "float_array" && subtype == 'f') {
                    matching_tags.push_back(tag);
                }
            } else {
                matching_tags.push_back(tag);
            }
        }
        return matching_tags;
    }

    template<typename T>
    T get(const str& tag) const {
        auto it = tags.find(tag);
        if (it == tags.end()) throw std::runtime_error("tag " + tag + " not found");
        auto& [type, subtype, data] = it->second;
        if constexpr (std::is_same_v<T, char>) {
            if (type == 'A') return data.read<char>(0);
            throw std::runtime_error("tag " + tag + " has wrong type");
        } else if constexpr (std::is_same_v<T, i64>) {
            if (type == 'c') return static_cast<i64>(data.read<i8>(0));
            if (type == 'C') return static_cast<i64>(data.read<u8>(0));
            if (type == 's') return static_cast<i64>(data.read<i16>(0));
            if (type == 'S') return static_cast<i64>(data.read<u16>(0));
            if (type == 'i') return static_cast<i64>(data.read<i32>(0));
            if (type == 'I') return static_cast<i64>(data.read<u32>(0));
            throw std::runtime_error("tag " + tag + " has wrong type");
        } else if constexpr (std::is_same_v<T, f64>) {
            if (type == 'f') return static_cast<f64>(data.read<f32>(0));
            throw std::runtime_error("tag " + tag + " has wrong type");
        } else if constexpr (std::is_same_v<T, str>) {
            if (type == 'Z') return data.to_string();
            throw std::runtime_error("tag " + tag + " has wrong type");
        } else if constexpr (std::is_same_v<T, std::vector<i64> >) {
            std::vector<i64> result;
            if (type == 'B' && subtype == 'c') {
                auto array = data.read_array<i8>(data.size());
                result.reserve(array.size());
                for (auto v : array) result.push_back(static_cast<i64>(v));
            } else if (type == 'B' && subtype == 'C') {
                auto array = data.read_array<u8>(data.size());
                result.reserve(array.size());
                for (auto v : array) result.push_back(static_cast<i64>(v));
            } else if (type == 'B' && subtype == 's') {
                auto array = data.read_array<i16>(data.size() / 2);
                result.reserve(array.size());
                for (auto v : array) result.push_back(static_cast<i64>(v));
            } else if (type == 'B' && subtype == 'S') {
                auto array = data.read_array<u16>(data.size() / 2);
                result.reserve(array.size());
                for (auto v : array) result.push_back(static_cast<i64>(v));
            } else if (type == 'B' && subtype == 'i') {
                auto array = data.read_array<i32>(data.size() / 4);
                result.reserve(array.size());
                for (auto v : array) result.push_back(static_cast<i64>(v));
            } else if (type == 'B' && subtype == 'I') {
                auto array = data.read_array<u32>(data.size() / 4);
                result.reserve(array.size());
                for (auto v : array) result.push_back(static_cast<i64>(v));
            } else {
                throw std::runtime_error("tag " + tag + " has wrong type");
            }
            return result;
        } else if constexpr (std::is_same_v<T, std::vector<f64> >) {
            if (type == 'B' && subtype == 'f') {
                auto array = data.read_array<f32>(data.size() / 4);
                std::vector<f64> result;
                result.reserve(array.size());
                for (auto v : array) result.push_back(static_cast<f64>(v));
                return result;
            }
            throw std::runtime_error("tag " + tag + " has wrong type");
        }
        throw std::runtime_error("unsupported tag type for tag " + tag);
    }

};


class BAMEntry {
public:
    i64 chr_index; // reference sequence index
    i64 start; // 0-based leftmost coordinate
    i64 end; // 0-based exclusive end coordinate (from cigar)
    u8 mapping_quality; // mapping quality
    u16 bai_bin; // bin for indexing
    BAMEntryFlag flag; // bitwise flags
    i64 next_chr_index; // chr index of the next segment in the template
    i64 next_start; // start of the next segment in the template
    i64 template_length; // observed template length
    str read_name; // read name
    BAMCigar cigar; // cigar operations
    BAMSequence sequence; // read sequence and qualities
    BAMEntryTags tags; // optional fields

    BAMEntry(
        i64 chr_index,
        i64 start,
        i64 end,
        u8 mapping_quality,
        u16 bai_bin,
        BAMEntryFlag flag,
        i64 next_chr_index,
        i64 next_start,
        i64 template_length,
        const str& read_name,
        const BAMCigar& cigar,
        const BAMSequence& sequence,
        const BAMEntryTags& tags
    ) : chr_index(chr_index),
        start(start),
        end(end),
        mapping_quality(mapping_quality),
        bai_bin(bai_bin),
        flag(flag),
        next_chr_index(next_chr_index),
        next_start(next_start),
        template_length(template_length),
        read_name(read_name),
        cigar(cigar),
        sequence(sequence),
        tags(tags) {}
};


std::vector<BAMEntry> read_bam_entries(const ByteArray& bytes, bool parse_tags = false) {
    i64 offset = 0;
    std::vector<BAMEntry> entries;
    while (offset < bytes.size()) {
        i64 block_size = static_cast<i64>(bytes.read<u32>(offset));
        i64 chr_index = static_cast<i64>(bytes.read<i32>(offset + 4));
        i64 start = static_cast<i64>(bytes.read<i32>(offset + 8));
        u8 l_read_name = bytes.read<u8>(offset + 12);
        u8 mapping_quality = bytes.read<u8>(offset + 13);
        u16 bai_bin = bytes.read<u16>(offset + 14);
        u16 n_cigar_op = bytes.read<u16>(offset + 16);
        BAMEntryFlag flag = BAMEntryFlag(bytes.read<u16>(offset + 18));
        u32 l_seq = bytes.read<i32>(offset + 20);
        i64 next_chr_index = static_cast<i64>(bytes.read<i32>(offset + 24));
        i64 next_start = static_cast<i64>(bytes.read<i32>(offset + 28));
        i64 template_length = static_cast<i64>(bytes.read<i32>(offset + 32));
        str read_name = bytes.read_string(offset + 36, l_read_name);

        BAMCigar cigar(
            bytes.read_array<u32>(n_cigar_op, offset + 36 + l_read_name)
        );
        i64 end = start + cigar.reference_length();
        BAMSequence sequence(
            bytes.read_array<u8>((l_seq + 1) / 2, offset + 36 + l_read_name + n_cigar_op * 4),
            bytes.read_array<u8>(l_seq, offset + 36 + l_read_name + n_cigar_op * 4 + (l_seq + 1) / 2)
        );
        
        BAMEntryTags tags;
        if (parse_tags) {
            i64 tags_offset = offset + 36 + l_read_name + n_cigar_op * 4 + (l_seq + 1) / 2 + l_seq;
            i64 tags_end = offset + 4 + block_size;
            while (tags_offset < tags_end) {
                str tag = bytes.read_string(tags_offset, 2);
                tags_offset += 2;
                char type = bytes.read<char>(tags_offset);
                tags_offset += 1;
                if (type == 'B') {
                    char subtype = bytes.read<char>(tags_offset);
                    tags_offset += 1;
                    u32 size = bytes.read<u32>(tags_offset);
                    tags_offset += 4;
                    ByteArray data = bytes.sliced(tags_offset, size);
                    tags.tags[tag] = std::make_tuple(type, subtype, data);
                    tags_offset += size;
                } else if (type == 'Z' || type == 'H') {
                    i64 str_start = tags_offset;
                    while (bytes.read<u8>(tags_offset) != 0) {
                        tags_offset += 1;
                    }
                    i64 str_length = tags_offset - str_start;
                    ByteArray data = bytes.sliced(str_start, str_length);
                    tags.tags[tag] = std::make_tuple(type, '\0', data);
                    tags_offset += 1;
                } else {
                    i64 type_size =
                        (type == 'A' || type == 'c' || type == 'C') ? 1 :
                        (type == 's' || type == 'S') ? 2 :
                        (type == 'i' || type == 'I' || type == 'f') ? 4 :
                        0;
                    if (type_size == 0) throw std::runtime_error("unsupported tag type " + str(1, type));
                    ByteArray data = bytes.sliced(tags_offset, type_size);
                    tags.tags[tag] = std::make_tuple(type, '\0', data);
                    tags_offset += type_size;
                }
            }
        }

        BAMEntry entry(
            chr_index, start, end, mapping_quality, bai_bin, flag,
            next_chr_index, next_start, template_length, read_name,
            cigar, sequence, tags
        );
        
        entries.push_back(std::move(entry));
        offset += block_size + 4;
    }
    return entries;
}



