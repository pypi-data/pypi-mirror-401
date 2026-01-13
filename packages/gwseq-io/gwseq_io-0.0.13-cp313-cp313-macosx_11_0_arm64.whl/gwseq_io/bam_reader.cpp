#include "util/main.cpp"


class BAMReader {
    str path;
    i64 parallel;
    str index_path;
    FilePool file_pool;

public:
    std::unique_ptr<BAMIndex> index;

    SAMHeader header;
    OrderedMap<str, ChrItem> chr_map;

    BAMReader(
        str path,
        i64 parallel = 1,
        i64 file_buffer_size = -1,
        i64 max_file_buffer_count = -1,
        str index_path = ""
    ) : path(path),
        parallel(parallel),
        index_path(index_path),
        file_pool(path, "r", parallel, file_buffer_size, max_file_buffer_count)
    {   
        auto file = file_pool.get_pseudo_file();
        auto [h, c] = read_bam_header(file);
        header = std::move(h);
        chr_map = std::move(c);
        if (index_path == "") index_path = path + ".bai";
        try {
            index = std::make_unique<BAMIndex>(index_path);
        } catch (...) {
            index = nullptr;
        }
    }
    
    // get chunks that overlap with a specified region
    std::vector<BAMChunk> get_overlapping_chunks(str chr_id, i64 start, i64 end) {
        if (!index) throw std::runtime_error("bam file is not indexed");
        i64 chr_idx = chr_map.at(chr_id).index;
        return index->get_overlapping_chunks(chr_idx, start, end);
    }

    ByteArray decompress_chunks(const std::vector<BAMChunk>& chunks) {
        ByteArray data;
        auto file = file_pool.get_pseudo_file();
        for (const auto& chunk : chunks) {
            i64 file_offset = static_cast<i64>(chunk.start >> 16);
            i64 block_offset = static_cast<i64>(chunk.start & 0xFFFF);
            i64 end_file_offset = static_cast<i64>(chunk.end >> 16);
            i64 end_block_offset = static_cast<i64>(chunk.end & 0xFFFF);
            
            // calculate how much data to read
            // add extra space to ensure we get the complete last block
            i64 size = (end_file_offset - file_offset) + 65536;
            if (size < 65536) size = 65536; // ensure we read at least one full block
            
            ByteArray chunk_raw_data = file.read(size, file_offset);
            std::vector<ByteArray> blocks;
            i64 index = 0;
            
            // decompress all blocks that we need
            while (index < chunk_raw_data.size()) {
                // check if we have enough data for a BGZF block header
                if (index + 18 > chunk_raw_data.size()) break;
                
                u16 block_size = chunk_raw_data.read<u16>(index + 16) + 1;
                
                // check if we have the complete block
                if (index + block_size > chunk_raw_data.size()) break;
                
                ByteArray raw_block = chunk_raw_data.sliced(index, block_size);
                ByteArray block = raw_block.decompressed();
                blocks.push_back(std::move(block));
                
                index += block_size;
                
                // if we've passed the end file offset, we can stop
                // (but always read at least one block if file offsets are equal)
                i64 current_file_offset = file_offset + index;
                if (current_file_offset > end_file_offset && blocks.size() > 0) break;
            }
            
            // trim the first and last blocks to the correct offsets
            if (blocks.size() == 0) {
                // no blocks found - might indicate an issue
                continue;
            } else if (blocks.size() == 1) {
                // single block - slice from block_offset to end_block_offset
                if (end_block_offset > block_offset) {
                    blocks[0] = blocks[0].sliced(block_offset, end_block_offset - block_offset);
                }
            } else {
                // multiple blocks
                // trim first block from block_offset to end
                blocks[0] = blocks[0].sliced(block_offset, blocks[0].size() - block_offset);
                // trim last block from start to end_block_offset
                if (end_block_offset > 0 && end_block_offset < blocks[blocks.size() - 1].size()) {
                    blocks[blocks.size() - 1] = blocks[blocks.size() - 1].sliced(0, end_block_offset);
                }
            }
            
            // append all blocks to the result
            for (const auto& block : blocks) {
                data.append(block);
            }
        }
        return data;
    }

    std::vector<BAMEntry> read_entries(
        str chr_id,
        i64 start,
        i64 end,
        bool filter = true,
        bool parse_tags = false
    ) {
        auto chunks = get_overlapping_chunks(chr_id, start, end);
        ByteArray data = decompress_chunks(chunks);
        auto all_entries = read_bam_entries(data, parse_tags);
        
        std::vector<BAMEntry> filtered_entries;
        i64 chr_index = chr_map.at(chr_id).index;
        for (auto& entry : all_entries) {
            if (entry.chr_index != chr_index) continue;
            if (entry.start >= end || entry.end <= start) continue;
            if (filter) {
                if (!entry.flag.mapped()) continue;
                if (entry.flag.paired() && !entry.flag.paired_properly()) continue;
                if (entry.flag.secondary_or_supplementary()) continue;
                if (entry.flag.failed_qc_or_duplicate()) continue;
            }
            filtered_entries.push_back(std::move(entry));
        }
        
        return filtered_entries;
    }





};

