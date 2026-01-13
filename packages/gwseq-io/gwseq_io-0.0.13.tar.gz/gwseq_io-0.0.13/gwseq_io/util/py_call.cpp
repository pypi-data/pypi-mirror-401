#pragma once

#include "includes.cpp"


#ifdef NO_CURL

inline i64 py_get_url_size(const str& url) {
    py::gil_scoped_acquire acquire;
    
    try {
        py::module_ urllib_request = py::module_::import("urllib.request");
        
        // Open URL with HEAD request to get content length
        py::object Request = urllib_request.attr("Request");
        py::object request = Request(url);
        request.attr("get_method") = py::cpp_function([]() { return "HEAD"; });
        
        py::object response = urllib_request.attr("urlopen")(request);
        
        // Get Content-Length header
        py::object headers = response.attr("headers");
        py::str content_length = headers.attr("get")("Content-Length");
        
        if (content_length.is_none()) {
            throw std::runtime_error("Content-Length header not available");
        }
        
        return content_length.cast<i64>();
    } catch (const py::error_already_set& e) {
        throw std::runtime_error(std::string("python url size error: ") + e.what());
    }
}

inline std::vector<u8> py_read_url_all(const str& url) {
    py::gil_scoped_acquire acquire;
    
    try {
        py::module_ urllib_request = py::module_::import("urllib.request");
        
        // Open URL and read all content
        py::object response = urllib_request.attr("urlopen")(url);
        py::bytes content = response.attr("read")();
        
        // Convert to vector
        std::string_view sv = content.cast<std::string>();
        return std::vector<u8>(sv.begin(), sv.end());
    } catch (const py::error_already_set& e) {
        throw std::runtime_error(std::string("python url read error: ") + e.what());
    }
}

inline std::vector<u8> py_read_url(const str& url, i64 size, i64 offset) {
    py::gil_scoped_acquire acquire;
    
    try {
        py::module_ urllib_request = py::module_::import("urllib.request");
        
        // Create request with Range header
        py::object Request = urllib_request.attr("Request");
        py::object request = Request(url);
        
        // Set Range header for partial content
        std::string range_header = "bytes=" + std::to_string(offset) + "-" + std::to_string(offset + size - 1);
        request.attr("add_header")("Range", range_header);
        
        // Open URL and read content
        py::object response = urllib_request.attr("urlopen")(request);
        py::bytes content = response.attr("read")();
        
        // Convert to vector
        std::string_view sv = content.cast<std::string>();
        return std::vector<u8>(sv.begin(), sv.end());
    } catch (const py::error_already_set& e) {
        throw std::runtime_error(std::string("python url read error: ") + e.what());
    }
}

#endif
