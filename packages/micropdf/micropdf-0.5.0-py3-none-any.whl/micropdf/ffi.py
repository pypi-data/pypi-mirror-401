"""
FFI bindings to the MicroPDF Rust library.

This module uses cffi to interface with the compiled Rust library.
It defines all the C function signatures and provides a low-level interface.

The library provides ~2300+ functions covering:
- Core document operations (open, read, write, render)
- Enhanced MicroPDF features (mp_* functions)
- PDF manipulation (annotations, forms, signatures)
- Image processing (pixmaps, colorspaces)
- Text extraction and search
- And much more...
"""

import os
import sys
from typing import Optional
from cffi import FFI

# Initialize FFI
ffi = FFI()

# Define C structures and function signatures
ffi.cdef("""
    // Type aliases
    typedef int8_t i8;
    typedef int16_t i16;
    typedef int32_t i32;
    typedef int64_t i64;
    typedef uint8_t u8;
    typedef uint16_t u16;
    typedef uint32_t u32;
    typedef uint64_t u64;
    typedef float f32;
    typedef double f64;

    // Geometry structures
    typedef struct {
        float x, y;
    } fz_point;

    typedef struct {
        float x0, y0, x1, y1;
    } fz_rect;

    typedef struct {
        int x0, y0, x1, y1;
    } fz_irect;

    typedef struct {
        float a, b, c, d, e, f;
    } fz_matrix;

    typedef struct {
        fz_point ul, ur, ll, lr;
    } fz_quad;

    // Opaque handle types
    typedef uint64_t fz_context;
    typedef uint64_t fz_document;
    typedef uint64_t fz_page;
    typedef uint64_t fz_pixmap;
    typedef uint64_t fz_buffer;
    typedef uint64_t fz_colorspace;
    typedef uint64_t fz_stext_page;
    typedef uint64_t fz_link;
    typedef uint64_t fz_stream;
    typedef uint64_t fz_output;
    typedef uint64_t fz_font;
    typedef uint64_t fz_image;
    typedef uint64_t fz_cookie;
    typedef uint64_t fz_device_handle;
    typedef uint64_t fz_path;

    // Context functions
    fz_context fz_new_context(const void* alloc, const void* locks, size_t max_store);
    void fz_drop_context(fz_context ctx);
    fz_context fz_clone_context(fz_context ctx);

    // Document functions
    fz_document fz_open_document(fz_context ctx, const char* filename);
    fz_document fz_open_document_with_buffer(fz_context ctx, const char* magic, const unsigned char* data, size_t len);
    void fz_drop_document(fz_context ctx, fz_document doc);
    int fz_count_pages(fz_context ctx, fz_document doc);
    int fz_needs_password(fz_context ctx, fz_document doc);
    int fz_authenticate_password(fz_context ctx, fz_document doc, const char* password);
    int fz_has_permission(fz_context ctx, fz_document doc, int permission);
    int fz_lookup_metadata(fz_context ctx, fz_document doc, const char* key, char* buf, int size);
    void pdf_save_document(fz_context ctx, fz_document doc, const char* filename, const void* opts);

    // Page functions
    fz_page fz_load_page(fz_context ctx, fz_document doc, int number);
    void fz_drop_page(fz_context ctx, fz_page page);
    fz_rect fz_bound_page(fz_context ctx, fz_page page);

    // Colorspace functions
    fz_colorspace fz_device_rgb(fz_context ctx);
    fz_colorspace fz_device_gray(fz_context ctx);
    fz_colorspace fz_device_bgr(fz_context ctx);
    fz_colorspace fz_device_cmyk(fz_context ctx);
    int fz_colorspace_n(fz_context ctx, fz_colorspace cs);
    const char* fz_colorspace_name(fz_context ctx, fz_colorspace cs);

    // Matrix functions
    fz_matrix fz_identity(void);
    fz_matrix fz_scale(float sx, float sy);
    fz_matrix fz_translate(float tx, float ty);
    fz_matrix fz_rotate(float degrees);
    fz_matrix fz_concat(fz_matrix a, fz_matrix b);

    // Pixmap functions
    fz_pixmap fz_new_pixmap(fz_context ctx, fz_colorspace cs, int w, int h, int alpha);
    fz_pixmap fz_new_pixmap_from_page(fz_context ctx, fz_page page, fz_matrix ctm, fz_colorspace cs, int alpha);
    void fz_drop_pixmap(fz_context ctx, fz_pixmap pix);
    int fz_pixmap_width(fz_context ctx, fz_pixmap pix);
    int fz_pixmap_height(fz_context ctx, fz_pixmap pix);
    int fz_pixmap_components(fz_context ctx, fz_pixmap pix);
    int fz_pixmap_stride(fz_context ctx, fz_pixmap pix);
    unsigned char* fz_pixmap_samples(fz_context ctx, fz_pixmap pix);
    void fz_clear_pixmap(fz_context ctx, fz_pixmap pix);

    // Buffer functions
    fz_buffer fz_new_buffer(fz_context ctx, size_t capacity);
    fz_buffer fz_new_buffer_from_copied_data(fz_context ctx, const unsigned char* data, size_t size);
    void fz_drop_buffer(fz_context ctx, fz_buffer buf);
    size_t fz_buffer_storage(fz_context ctx, fz_buffer buf, unsigned char** datap);
    const unsigned char* fz_buffer_data(fz_context ctx, fz_buffer buf, size_t* len);
    void fz_append_data(fz_context ctx, fz_buffer buf, const void* data, size_t len);
    void fz_append_string(fz_context ctx, fz_buffer buf, const char* str);
    void fz_clear_buffer(fz_context ctx, fz_buffer buf);
    fz_buffer fz_new_buffer_from_pixmap_as_png(fz_context ctx, fz_pixmap pix, int color_params);

    // Text extraction functions
    fz_stext_page fz_new_stext_page_from_page(fz_context ctx, fz_page page, const void* options);
    void fz_drop_stext_page(fz_context ctx, fz_stext_page stext);
    fz_buffer fz_new_buffer_from_stext_page(fz_context ctx, fz_stext_page stext);

    // Search functions
    int fz_search_stext_page(fz_context ctx, fz_stext_page stext, const char* needle, int* mark, fz_quad* hit_bbox, int hit_max);

    // Link functions
    fz_link fz_load_links(fz_context ctx, fz_page page);
    void fz_drop_link(fz_context ctx, fz_link link);
    fz_rect fz_link_rect(fz_context ctx, fz_link link);
    const char* fz_link_uri(fz_context ctx, fz_link link);
    fz_link fz_link_next(fz_context ctx, fz_link link);

    // Stream functions
    fz_stream fz_open_file(fz_context ctx, const char* filename);
    fz_stream fz_open_memory(fz_context ctx, const unsigned char* data, size_t len);
    void fz_drop_stream(fz_context ctx, fz_stream stm);
    size_t fz_read(fz_context ctx, fz_stream stm, unsigned char* data, size_t len);
    int fz_read_byte(fz_context ctx, fz_stream stm);
    int fz_is_eof(fz_context ctx, fz_stream stm);
    void fz_seek(fz_context ctx, fz_stream stm, int64_t offset, int whence);
    int64_t fz_tell(fz_context ctx, fz_stream stm);

    // Output functions
    fz_output fz_new_output_with_path(fz_context ctx, const char* filename, int append);
    fz_output fz_new_output_with_buffer(fz_context ctx, fz_buffer buf);
    void fz_drop_output(fz_context ctx, fz_output out);
    void fz_write_data(fz_context ctx, fz_output out, const void* data, size_t size);
    void fz_write_string(fz_context ctx, fz_output out, const char* s);
    void fz_write_byte(fz_context ctx, fz_output out, unsigned char byte);
    int64_t fz_tell_output(fz_context ctx, fz_output out);

    // Font functions
    fz_font fz_new_font(fz_context ctx, const char* name, int is_bold, int is_italic, uint64_t font_file);
    fz_font fz_new_font_from_file(fz_context ctx, const char* name, const char* path, int index, int use_glyph_bbox);
    fz_font fz_new_font_from_memory(fz_context ctx, const char* name, const unsigned char* data, int len, int index, int use_glyph_bbox);
    void fz_drop_font(fz_context ctx, fz_font font);
    void fz_font_name(fz_context ctx, fz_font font, char* buf, int size);
    int fz_font_is_bold(fz_context ctx, fz_font font);
    int fz_font_is_italic(fz_context ctx, fz_font font);

    // Image functions
    fz_image fz_new_image_from_file(fz_context ctx, const char* path);
    fz_image fz_new_image_from_buffer(fz_context ctx, fz_buffer buffer);
    fz_image fz_new_image_from_pixmap(fz_context ctx, fz_pixmap pixmap, fz_image mask);
    void fz_drop_image(fz_context ctx, fz_image image);
    int fz_image_width(fz_context ctx, fz_image image);
    int fz_image_height(fz_context ctx, fz_image image);

    // Cookie functions (progress tracking)
    fz_cookie fz_new_cookie(fz_context ctx);
    void fz_drop_cookie(fz_context ctx, fz_cookie cookie);
    void fz_abort_cookie(fz_context ctx, fz_cookie cookie);
    int fz_cookie_is_aborted(fz_context ctx, fz_cookie cookie);

    // Path functions
    fz_path fz_new_path(fz_context ctx);
    void fz_drop_path(fz_context ctx, fz_path path);
    void fz_moveto(fz_context ctx, fz_path path, float x, float y);
    void fz_lineto(fz_context ctx, fz_path path, float x, float y);
    void fz_curveto(fz_context ctx, fz_path path, float x1, float y1, float x2, float y2, float x3, float y3);
    void fz_closepath(fz_context ctx, fz_path path);
    void fz_rectto(fz_context ctx, fz_path path, float x, float y, float w, float h);

    // ============================================================================
    // Enhanced MicroPDF Functions (120 functions)
    // ============================================================================
    
    // Document Operations
    int32_t mp_add_blank_page(int32_t ctx, int32_t doc, float width, float height);
    int32_t mp_merge_pdfs(int32_t ctx, const char * const * paths, int32_t count, const char * output_path);
    int32_t mp_split_pdf(int32_t ctx, const char * input_path, const char * output_dir);
    int32_t mp_write_pdf(int32_t ctx, int32_t doc, const char * path);
    int32_t mp_optimize_pdf(int32_t ctx, const char * path);
    int32_t mp_linearize_pdf(int32_t ctx, const char * input_path, const char * output_path);
    
    // Watermark & Drawing
    int32_t mp_add_watermark(int32_t ctx, const char * input_path, const char * output_path, const char * text, float x, float y, float font_size, float opacity);
    int32_t mp_draw_rectangle(int32_t ctx, int32_t page, float x, float y, float width, float height, float r, float g, float b, float alpha, int32_t fill);
    int32_t mp_draw_circle(int32_t ctx, int32_t page, float x, float y, float radius, float r, float g, float b, float alpha, int32_t fill);
    int32_t mp_draw_line(int32_t ctx, int32_t page, float x0, float y0, float x1, float y1, float r, float g, float b, float alpha, float line_width);
    
    // Print Production - N-Up Layouts
    int mp_create_2up(const char * input_path, const char * output_path, int page_size);
    int mp_create_4up(const char * input_path, const char * output_path, int page_size);
    int mp_create_9up(const char * input_path, const char * output_path, int page_size);
    int mp_create_nup(const char * input_path, const char * output_path, int cols, int rows, int page_size);
    
    // Print Production - Booklet
    int mp_create_booklet(const char * input_path, const char * output_path, int binding_type, int page_size, int add_blanks);
    int mp_create_saddle_stitch_booklet(const char * input_path, const char * output_path);
    
    // Print Production - Poster/Tiling
    int mp_create_poster(const char * input_path, const char * output_path, int tile_size, float overlap_mm, int cut_marks);
    int mp_poster_tile_count(const char * pdf_path, int tile_size, float overlap_mm);
    
    // Page Box Management
    int32_t mp_page_box_manager_create(const char * pdf_path);
    void mp_page_box_manager_free(int32_t handle);
    int mp_page_box_manager_page_count(int32_t handle);
    int mp_page_box_get(int32_t handle, int page, int box_type, void * rect_out);
    int mp_page_box_set(int32_t handle, int page, int box_type, float llx, float lly, float urx, float ury);
    int mp_page_box_add_bleed(int32_t handle, float bleed, int unit);
    int mp_page_box_save(int32_t handle, const char * output_path);
    
    // PDF Validation & Repair
    int mp_validate_pdf(const char * pdf_path, int mode, void * result_out);
    int mp_quick_validate(const char * pdf_path);
    int mp_repair_pdf(const char * input_path, const char * output_path);
    
    // Encryption & Decryption
    int mp_is_encrypted(const char * pdf_path);
    int mp_encrypt_pdf(const char * input_path, const char * output_path, int32_t options);
    int mp_decrypt_pdf(const char * input_path, const char * output_path, const char * password);
    int32_t mp_encryption_options_new(void);
    void mp_encryption_options_drop(int32_t options);
    int mp_encryption_set_user_password(int32_t options, const char * password);
    int mp_encryption_set_owner_password(int32_t options, const char * password);
    int mp_encryption_set_permissions(int32_t options, int permissions);
    int mp_encryption_set_algorithm(int32_t options, int algorithm);
    
    // Digital Signatures - Certificates
    int32_t mp_certificate_load_pem(const char * cert_path, const char * key_path, const char * key_password);
    int32_t mp_certificate_load_pkcs12(const char * path, const char * password);
    void mp_certificate_drop(int32_t cert);
    int mp_certificate_is_valid(int32_t cert);
    const char * mp_certificate_get_subject(int32_t cert);
    const char * mp_certificate_get_issuer(int32_t cert);
    
    // Digital Signatures - Signing & Verification
    int mp_signature_create(const char * input_path, const char * output_path, int32_t cert, const char * field_name, int page, float x, float y, float width, float height, const char * reason, const char * location);
    int mp_signature_create_invisible(const char * input_path, const char * output_path, int32_t cert, const char * field_name, const char * reason, const char * location);
    int mp_signature_verify(const char * pdf_path, const char * field_name, void * result);
    void mp_signature_verify_result_free(void * result);
    int mp_signature_count(const char * pdf_path);
    int mp_tsa_timestamp(const char * tsa_url, const uint8_t * data, size_t data_len, const uint8_t * * timestamp_out, size_t * timestamp_len_out);
    
    // HTML to PDF Conversion
    int32_t mp_html_to_pdf(const char * html, const char * output_path, int32_t options);
    int32_t mp_html_file_to_pdf(const char * html_path, const char * output_path, int32_t options);
    int32_t mp_html_options_create(void);
    void mp_html_options_free(int32_t handle);
    int32_t mp_html_options_set_page_size(int32_t handle, int32_t page_size);
    int32_t mp_html_options_set_page_size_custom(int32_t handle, float width, float height);
    int32_t mp_html_options_set_margins(int32_t handle, float top, float right, float bottom, float left);
    int32_t mp_html_options_set_landscape(int32_t handle, int32_t landscape);
    int32_t mp_html_options_set_scale(int32_t handle, float scale);
    int32_t mp_html_options_set_print_background(int32_t handle, int32_t enabled);
    int32_t mp_html_options_set_header(int32_t handle, const char * html);
    int32_t mp_html_options_set_footer(int32_t handle, const char * html);
    int32_t mp_html_options_set_javascript(int32_t handle, int32_t enabled);
    int32_t mp_html_options_set_base_url(int32_t handle, const char * url);
    int32_t mp_html_options_set_stylesheet(int32_t handle, const char * css);
    float mp_html_options_get_page_width(int32_t handle);
    float mp_html_options_get_page_height(int32_t handle);
    float mp_html_options_get_content_width(int32_t handle);
    float mp_html_options_get_content_height(int32_t handle);
    
    // Document Composition - DocTemplate
    int32_t mp_doc_template_create(const char * filename);
    void mp_doc_template_free(int32_t handle);
    int32_t mp_doc_template_set_page_size(int32_t handle, float width, float height);
    int32_t mp_doc_template_set_margins(int32_t handle, float left, float right, float top, float bottom);
    
    // Document Composition - Frames
    int32_t mp_frame_create(const char * id, float x, float y, float width, float height);
    void mp_frame_free(int32_t handle);
    float mp_frame_available_width(int32_t handle);
    float mp_frame_available_height(int32_t handle);
    
    // Document Composition - Flowables
    int32_t mp_paragraph_create(const char * text);
    void mp_paragraph_free(int32_t handle);
    int32_t mp_paragraph_set_font_size(int32_t handle, float size);
    int32_t mp_paragraph_set_leading(int32_t handle, float leading);
    int32_t mp_spacer_create(float height);
    void mp_spacer_free(int32_t handle);
    int32_t mp_hr_create(void);
    void mp_hr_free(int32_t handle);
    int32_t mp_hr_set_thickness(int32_t handle, float thickness);
    int32_t mp_image_create(const char * path);
    void mp_image_free(int32_t handle);
    int32_t mp_image_set_width(int32_t handle, float width);
    int32_t mp_image_set_height(int32_t handle, float height);
    int32_t mp_list_item_bullet(const char * text);
    int32_t mp_list_item_numbered(size_t number, const char * text);
    void mp_list_item_free(int32_t handle);
    
    // Document Composition - Typography
    int32_t mp_paragraph_style_create(const char * name);
    void mp_paragraph_style_free(int32_t handle);
    int32_t mp_paragraph_style_set_font_size(int32_t handle, float size);
    int32_t mp_paragraph_style_set_leading(int32_t handle, float leading);
    int32_t mp_paragraph_style_set_alignment(int32_t handle, int32_t align);
    int32_t mp_stylesheet_create(void);
    void mp_stylesheet_free(int32_t handle);
    int32_t mp_stylesheet_add_style(int32_t sheet_handle, int32_t style_handle);
    
    // Document Composition - Tables
    int32_t mp_table_create(size_t rows, size_t cols);
    void mp_table_free(int32_t handle);
    size_t mp_table_num_rows(int32_t handle);
    size_t mp_table_num_cols(int32_t handle);
    int32_t mp_table_style_create(void);
    void mp_table_style_free(int32_t handle);
    int32_t mp_table_style_add_grid(int32_t handle, float weight, float r, float g, float b);
    int32_t mp_table_style_add_background(int32_t handle, int32_t start_col, int32_t start_row, int32_t end_col, int32_t end_row, float r, float g, float b);
    
    // Document Composition - Table of Contents
    int32_t mp_toc_create(void);
    void mp_toc_free(int32_t handle);
    int32_t mp_toc_set_title(int32_t handle, const char * title);
    int32_t mp_toc_add_entry(int32_t handle, const char * title, uint8_t level, size_t page);
    int32_t mp_toc_builder_create(void);
    void mp_toc_builder_free(int32_t handle);
    int32_t mp_toc_builder_add_heading(int32_t handle, const char * title, uint8_t level, size_t page);
    
    // Document Composition - Story
    int32_t mp_story_create(void);
    void mp_story_free(int32_t handle);
    size_t mp_story_len(int32_t handle);
    
    // Memory Management
    void mp_free_string(char * s);
    void mp_free_timestamp(uint8_t * data, size_t len);
""")

# Constants
FZ_STORE_DEFAULT = 256 * 1024 * 1024  # 256 MB


def _find_library() -> Optional[str]:
    """
    Find the MicroPDF shared library.
    
    This function uses the native module to find or download the library.
    """
    try:
        from .native import get_library_path
        lib_path = get_library_path()
        if lib_path:
            return str(lib_path)
    except ImportError:
        pass
    
    # Fallback: legacy search paths
    lib_names = ["libmicropdf.so", "libmicropdf.dylib", "micropdf.dll"]

    search_paths = [
        # Bundled in package
        os.path.join(os.path.dirname(__file__), "lib", "linux-x64"),
        os.path.join(os.path.dirname(__file__), "lib", "darwin-x64"),
        os.path.join(os.path.dirname(__file__), "lib", "darwin-arm64"),
        os.path.join(os.path.dirname(__file__), "lib", "win32-x64"),
        # Relative to this file (development mode)
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "micropdf-rs", "target", "release"),
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "micropdf-rs", "target", "debug"),
        # System paths
        "/usr/local/lib",
        "/usr/lib",
        os.path.expanduser("~/.local/lib"),
    ]

    if sys.platform == "darwin":
        search_paths.append("/opt/homebrew/lib")

    for path in search_paths:
        for lib_name in lib_names:
            lib_path = os.path.join(path, lib_name)
            if os.path.exists(lib_path):
                return lib_path

    return None


# Load the library
_lib_path = _find_library()
lib: Optional[object] = None

if _lib_path is not None:
    try:
        lib = ffi.dlopen(_lib_path)
    except OSError as e:
        print(f"[micropdf] Warning: Could not load library from {_lib_path}: {e}")
        lib = None

if lib is None:
    # Create a mock library for type checking and basic functionality
    print("[micropdf] Warning: Native library not available")
    print("[micropdf] Some functionality will be limited")
    print("[micropdf] To enable full functionality:")
    print("[micropdf]   1. Install from PyPI: pip install micropdf")
    print("[micropdf]   2. Or build from source: cd micropdf-rs && cargo build --release")
    
    # Mock library that raises errors when used
    class MockLib:
        def __getattr__(self, name: str):
            def mock_func(*args, **kwargs):
                raise RuntimeError(
                    f"Function '{name}' requires native library. "
                    "Please install micropdf with native bindings."
                )
            return mock_func
    
    lib = MockLib()

__all__ = ["ffi", "lib", "FZ_STORE_DEFAULT"]

