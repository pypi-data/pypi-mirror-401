"""
Full FFI bindings to the MicroPDF Rust library.

This module contains the complete C API definitions extracted from the
MicroPDF header files. It provides ~2300+ functions for comprehensive
PDF manipulation.
"""

# This module extends the base ffi.py with additional function definitions

FULL_FFI_DEFS = """
    // ============================================================================
    // CONTEXT FUNCTIONS (28)
    // ============================================================================
    
    int fz_aa_level(uint64_t ctx);
    int fz_caught(uint64_t ctx);
    const char* fz_caught_message(uint64_t ctx);
    uint64_t fz_clone_context(uint64_t ctx);
    int fz_context_is_valid(uint64_t ctx);
    const char* fz_convert_error(uint64_t ctx, int* code);
    void fz_disable_icc(uint64_t ctx);
    void fz_drop_context(uint64_t ctx);
    void fz_empty_store(uint64_t ctx);
    void fz_enable_icc(uint64_t ctx);
    void fz_flush_warnings(uint64_t ctx);
    int fz_has_error(uint64_t ctx);
    void fz_ignore_error(uint64_t ctx);
    uint64_t fz_keep_context(uint64_t ctx);
    uint64_t fz_new_context(const void* alloc, const void* locks, size_t max_store);
    uint64_t fz_new_default_context(void);
    void fz_report_error(uint64_t ctx);
    void fz_rethrow(uint64_t ctx);
    void fz_set_aa_level(uint64_t ctx, int bits);
    void fz_shrink_store(uint64_t ctx, int percent);
    int fz_store_scavenge(uint64_t ctx, size_t size, int* phase);
    size_t fz_store_size(uint64_t ctx);
    void fz_throw(uint64_t ctx, int errcode, const char* fmt);
    void* fz_user_context(uint64_t ctx);
    void fz_warn(uint64_t ctx, const char* fmt);
    
    // ============================================================================
    // DOCUMENT FUNCTIONS (30)
    // ============================================================================
    
    int fz_authenticate_password(uint64_t ctx, uint64_t doc, const char* password);
    fz_rect fz_bound_page(uint64_t ctx, uint64_t page);
    fz_rect fz_bound_page_box(uint64_t ctx, uint64_t page, int box_type);
    uint64_t fz_clone_document(uint64_t ctx, uint64_t doc);
    int fz_count_chapter_pages(uint64_t ctx, uint64_t doc, int chapter);
    int fz_count_chapters(uint64_t ctx, uint64_t doc);
    int fz_count_pages(uint64_t ctx, uint64_t doc);
    int fz_document_format(uint64_t ctx, uint64_t doc, char* buf, int size);
    int fz_document_is_valid(uint64_t ctx, uint64_t doc);
    void fz_drop_document(uint64_t ctx, uint64_t doc);
    void fz_drop_page(uint64_t ctx, uint64_t page);
    int fz_has_permission(uint64_t ctx, uint64_t doc, int permission);
    int fz_is_document_reflowable(uint64_t ctx, uint64_t doc);
    uint64_t fz_keep_document(uint64_t ctx, uint64_t doc);
    uint64_t fz_keep_page(uint64_t ctx, uint64_t page);
    void fz_layout_document(uint64_t ctx, uint64_t doc, float w, float h, float em);
    uint64_t fz_load_chapter_page(uint64_t ctx, uint64_t doc, int chapter, int page);
    uint64_t fz_load_outline(uint64_t ctx, uint64_t doc);
    uint64_t fz_load_page(uint64_t ctx, uint64_t doc, int page_num);
    int fz_lookup_metadata(uint64_t ctx, uint64_t doc, const char* key, char* buf, int size);
    char* fz_make_location_uri(uint64_t ctx, uint64_t doc, int page, char* buf, int size);
    int fz_needs_password(uint64_t ctx, uint64_t doc);
    uint64_t fz_open_document(uint64_t ctx, const char* filename);
    uint64_t fz_open_document_with_stream(uint64_t ctx, const char* magic, uint64_t stm);
    int fz_page_label(uint64_t ctx, uint64_t doc, int page_num, char* buf, int size);
    int fz_page_number_from_location(uint64_t ctx, uint64_t doc, int chapter, int page);
    int fz_resolve_link(uint64_t ctx, uint64_t doc, const char* uri, float* xp, float* yp);
    void fz_run_page(uint64_t ctx, uint64_t page, uint64_t device, fz_matrix transform, void* cookie);
    void fz_run_page_annots(uint64_t ctx, uint64_t page, uint64_t device, fz_matrix transform, void* cookie);
    void fz_run_page_contents(uint64_t ctx, uint64_t page, uint64_t device, fz_matrix transform, void* cookie);

    // ============================================================================
    // PIXMAP FUNCTIONS (32)
    // ============================================================================
    
    uint64_t fz_new_pixmap(uint64_t ctx, uint64_t cs, int w, int h, uint64_t seps, int alpha);
    uint64_t fz_new_pixmap_with_bbox(uint64_t ctx, uint64_t cs, fz_irect bbox, uint64_t seps, int alpha);
    uint64_t fz_new_pixmap_with_data(uint64_t ctx, uint64_t cs, int w, int h, uint64_t seps, int alpha, int stride, unsigned char* samples);
    uint64_t fz_new_pixmap_from_page(uint64_t ctx, uint64_t page, fz_matrix ctm, uint64_t cs, int alpha);
    uint64_t fz_new_pixmap_from_page_number(uint64_t ctx, uint64_t doc, int number, fz_matrix ctm, uint64_t cs, int alpha);
    uint64_t fz_new_pixmap_from_display_list(uint64_t ctx, uint64_t list, fz_matrix ctm, uint64_t cs, int alpha);
    void fz_drop_pixmap(uint64_t ctx, uint64_t pix);
    uint64_t fz_keep_pixmap(uint64_t ctx, uint64_t pix);
    int fz_pixmap_width(uint64_t ctx, uint64_t pix);
    int fz_pixmap_height(uint64_t ctx, uint64_t pix);
    int fz_pixmap_x(uint64_t ctx, uint64_t pix);
    int fz_pixmap_y(uint64_t ctx, uint64_t pix);
    int fz_pixmap_components(uint64_t ctx, uint64_t pix);
    int fz_pixmap_stride(uint64_t ctx, uint64_t pix);
    int fz_pixmap_alpha(uint64_t ctx, uint64_t pix);
    uint64_t fz_pixmap_colorspace(uint64_t ctx, uint64_t pix);
    unsigned char* fz_pixmap_samples(uint64_t ctx, uint64_t pix);
    fz_irect fz_pixmap_bbox(uint64_t ctx, uint64_t pix);
    void fz_clear_pixmap(uint64_t ctx, uint64_t pix);
    void fz_clear_pixmap_with_value(uint64_t ctx, uint64_t pix, int value);
    void fz_clear_pixmap_rect_with_value(uint64_t ctx, uint64_t pix, int value, fz_irect r);
    void fz_invert_pixmap(uint64_t ctx, uint64_t pix);
    void fz_invert_pixmap_rect(uint64_t ctx, uint64_t pix, fz_irect r);
    void fz_gamma_pixmap(uint64_t ctx, uint64_t pix, float gamma);
    void fz_tint_pixmap(uint64_t ctx, uint64_t pix, int black, int white);
    uint64_t fz_scale_pixmap(uint64_t ctx, uint64_t src, int x, int y, int w, int h, fz_irect* clip);
    uint64_t fz_clone_pixmap(uint64_t ctx, uint64_t old);
    uint64_t fz_convert_pixmap(uint64_t ctx, uint64_t pix, uint64_t default_cs, uint64_t prf, uint64_t params, int keep_alpha);
    size_t fz_pixmap_size(uint64_t ctx, uint64_t pix);
    void fz_set_pixmap_resolution(uint64_t ctx, uint64_t pix, int xres, int yres);
    int fz_pixmap_x_resolution(uint64_t ctx, uint64_t pix);
    int fz_pixmap_y_resolution(uint64_t ctx, uint64_t pix);
    
    // ============================================================================
    // BUFFER FUNCTIONS (44)
    // ============================================================================
    
    uint64_t fz_new_buffer(uint64_t ctx, size_t capacity);
    uint64_t fz_new_buffer_from_copied_data(uint64_t ctx, const unsigned char* data, size_t size);
    uint64_t fz_new_buffer_from_base64(uint64_t ctx, const char* data, size_t size);
    uint64_t fz_new_buffer_from_shared_data(uint64_t ctx, const unsigned char* data, size_t size);
    void fz_drop_buffer(uint64_t ctx, uint64_t buf);
    uint64_t fz_keep_buffer(uint64_t ctx, uint64_t buf);
    size_t fz_buffer_storage(uint64_t ctx, uint64_t buf, unsigned char** datap);
    const unsigned char* fz_buffer_data(uint64_t ctx, uint64_t buf, size_t* len);
    void fz_append_data(uint64_t ctx, uint64_t buf, const void* data, size_t len);
    void fz_append_string(uint64_t ctx, uint64_t buf, const char* str);
    void fz_append_byte(uint64_t ctx, uint64_t buf, int c);
    void fz_append_rune(uint64_t ctx, uint64_t buf, int c);
    void fz_append_int16_le(uint64_t ctx, uint64_t buf, int x);
    void fz_append_int16_be(uint64_t ctx, uint64_t buf, int x);
    void fz_append_int32_le(uint64_t ctx, uint64_t buf, int x);
    void fz_append_int32_be(uint64_t ctx, uint64_t buf, int x);
    void fz_append_bits(uint64_t ctx, uint64_t buf, int value, int count);
    void fz_append_bits_pad(uint64_t ctx, uint64_t buf);
    void fz_append_pdf_string(uint64_t ctx, uint64_t buf, const char* text);
    void fz_append_buffer(uint64_t ctx, uint64_t buf, uint64_t extra);
    void fz_clear_buffer(uint64_t ctx, uint64_t buf);
    void fz_trim_buffer(uint64_t ctx, uint64_t buf);
    void fz_grow_buffer(uint64_t ctx, uint64_t buf);
    void fz_resize_buffer(uint64_t ctx, uint64_t buf, size_t capacity);
    void fz_terminate_buffer(uint64_t ctx, uint64_t buf);
    void fz_md5_buffer(uint64_t ctx, uint64_t buf, unsigned char* digest);
    char* fz_md5_buffer_string(uint64_t ctx, uint64_t buf);
    void fz_sha256_buffer(uint64_t ctx, uint64_t buf, unsigned char* digest);
    void fz_sha512_buffer(uint64_t ctx, uint64_t buf, unsigned char* digest);
    uint64_t fz_new_buffer_from_pixmap_as_png(uint64_t ctx, uint64_t pix, uint64_t params);
    uint64_t fz_new_buffer_from_pixmap_as_pnm(uint64_t ctx, uint64_t pix);
    uint64_t fz_new_buffer_from_pixmap_as_pam(uint64_t ctx, uint64_t pix);
    uint64_t fz_new_buffer_from_pixmap_as_psd(uint64_t ctx, uint64_t pix);
    uint64_t fz_new_buffer_from_pixmap_as_jpeg(uint64_t ctx, uint64_t pix, uint64_t params);
    uint64_t fz_new_buffer_from_page(uint64_t ctx, uint64_t page, uint64_t opts);
    uint64_t fz_new_buffer_from_page_number(uint64_t ctx, uint64_t doc, int page, uint64_t opts);
    uint64_t fz_new_buffer_from_stext_page(uint64_t ctx, uint64_t stext);
    size_t fz_buffer_extract(uint64_t ctx, uint64_t buf, unsigned char** data);
    void fz_write_buffer(uint64_t ctx, uint64_t out, uint64_t buf);
    void fz_save_buffer(uint64_t ctx, uint64_t buf, const char* filename);
    void fz_append_base64(uint64_t ctx, uint64_t buf, const unsigned char* data, size_t size);
    void fz_append_hex(uint64_t ctx, uint64_t buf, const unsigned char* data, size_t size);
    void fz_append_int(uint64_t ctx, uint64_t buf, int64_t value);
    void fz_append_float(uint64_t ctx, uint64_t buf, float value);
    
    // ============================================================================
    // COLORSPACE FUNCTIONS (42)
    // ============================================================================
    
    uint64_t fz_device_gray(uint64_t ctx);
    uint64_t fz_device_rgb(uint64_t ctx);
    uint64_t fz_device_bgr(uint64_t ctx);
    uint64_t fz_device_cmyk(uint64_t ctx);
    uint64_t fz_device_lab(uint64_t ctx);
    void fz_drop_colorspace(uint64_t ctx, uint64_t cs);
    uint64_t fz_keep_colorspace(uint64_t ctx, uint64_t cs);
    int fz_colorspace_n(uint64_t ctx, uint64_t cs);
    const char* fz_colorspace_name(uint64_t ctx, uint64_t cs);
    int fz_colorspace_type(uint64_t ctx, uint64_t cs);
    int fz_colorspace_is_gray(uint64_t ctx, uint64_t cs);
    int fz_colorspace_is_rgb(uint64_t ctx, uint64_t cs);
    int fz_colorspace_is_cmyk(uint64_t ctx, uint64_t cs);
    int fz_colorspace_is_lab(uint64_t ctx, uint64_t cs);
    int fz_colorspace_is_indexed(uint64_t ctx, uint64_t cs);
    int fz_colorspace_is_device(uint64_t ctx, uint64_t cs);
    int fz_colorspace_is_device_gray(uint64_t ctx, uint64_t cs);
    int fz_colorspace_is_device_cmyk(uint64_t ctx, uint64_t cs);
    int fz_colorspace_is_subtractive(uint64_t ctx, uint64_t cs);
    uint64_t fz_colorspace_base(uint64_t ctx, uint64_t cs);
    int fz_colorspace_colorant(uint64_t ctx, uint64_t cs, int i, const char** name);
    int fz_colorspace_device_n_has_only_cmyk(uint64_t ctx, uint64_t cs);
    int fz_colorspace_device_n_has_cmyk(uint64_t ctx, uint64_t cs);
    uint64_t fz_new_icc_colorspace(uint64_t ctx, int type, int flags, const char* name, uint64_t buf);
    uint64_t fz_new_indexed_colorspace(uint64_t ctx, uint64_t base, int high, unsigned char* lookup);
    uint64_t fz_new_cal_gray_colorspace(uint64_t ctx, float wp0, float wp1, float wp2, float gamma);
    uint64_t fz_new_cal_rgb_colorspace(uint64_t ctx, float* whitepoint, float* gamma, float* matrix);
    void fz_clamp_color(uint64_t ctx, uint64_t cs, const float* in, float* out);
    void fz_convert_color(uint64_t ctx, uint64_t ss, const float* sv, uint64_t ds, float* dv, uint64_t is, uint64_t params);
    void fz_find_rendering_intent(uint64_t ctx, const char* name, int* intent);
    void fz_find_blendmode(uint64_t ctx, const char* name, int* mode);
    const char* fz_blendmode_name(uint64_t ctx, int mode);
    uint64_t fz_new_colorspace(uint64_t ctx, int type, int flags, int n, const char* name);
    
    // ============================================================================
    // FONT FUNCTIONS (22)
    // ============================================================================
    
    uint64_t fz_new_base14_font(uint64_t ctx, const char* name);
    uint64_t fz_new_cjk_font(uint64_t ctx, int ordering);
    uint64_t fz_new_font_from_file(uint64_t ctx, const char* name, const char* path, int index, int use_glyph_bbox);
    uint64_t fz_new_font_from_memory(uint64_t ctx, const char* name, const unsigned char* data, int len, int index, int use_glyph_bbox);
    uint64_t fz_new_font_from_buffer(uint64_t ctx, const char* name, uint64_t buffer, int index, int use_glyph_bbox);
    void fz_drop_font(uint64_t ctx, uint64_t font);
    uint64_t fz_keep_font(uint64_t ctx, uint64_t font);
    const char* fz_font_name(uint64_t ctx, uint64_t font);
    int fz_font_is_bold(uint64_t ctx, uint64_t font);
    int fz_font_is_italic(uint64_t ctx, uint64_t font);
    int fz_font_is_serif(uint64_t ctx, uint64_t font);
    int fz_font_is_monospaced(uint64_t ctx, uint64_t font);
    fz_rect fz_font_bbox(uint64_t ctx, uint64_t font);
    int fz_encode_character(uint64_t ctx, uint64_t font, int unicode);
    int fz_encode_character_with_fallback(uint64_t ctx, uint64_t font, int unicode, int script, int language, uint64_t* out_font);
    float fz_advance_glyph(uint64_t ctx, uint64_t font, int glyph, int wmode);
    int fz_glyph_cacheable(uint64_t ctx, uint64_t font, int glyph);
    uint64_t fz_font_ft_face(uint64_t ctx, uint64_t font);
    uint64_t fz_font_t3_procs(uint64_t ctx, uint64_t font);
    void fz_decouple_type3_font(uint64_t ctx, uint64_t font, void* t3_doc);
    fz_rect fz_bound_glyph(uint64_t ctx, uint64_t font, int glyph, fz_matrix trm);
    int fz_glyph_name(uint64_t ctx, uint64_t font, int glyph, char* buf, int size);
    
    // ============================================================================
    // IMAGE FUNCTIONS (22)
    // ============================================================================
    
    uint64_t fz_new_image_from_file(uint64_t ctx, const char* path);
    uint64_t fz_new_image_from_buffer(uint64_t ctx, uint64_t buffer);
    uint64_t fz_new_image_from_pixmap(uint64_t ctx, uint64_t pixmap, uint64_t mask);
    uint64_t fz_new_image_from_compressed_buffer(uint64_t ctx, int w, int h, int bpc, uint64_t colorspace, int xres, int yres, int interpolate, int imagemask, float* decode, int* colorkey, uint64_t buffer, uint64_t mask);
    void fz_drop_image(uint64_t ctx, uint64_t image);
    uint64_t fz_keep_image(uint64_t ctx, uint64_t image);
    int fz_image_width(uint64_t ctx, uint64_t image);
    int fz_image_height(uint64_t ctx, uint64_t image);
    int fz_image_xres(uint64_t ctx, uint64_t image);
    int fz_image_yres(uint64_t ctx, uint64_t image);
    int fz_image_number_of_components(uint64_t ctx, uint64_t image);
    int fz_image_bits_per_component(uint64_t ctx, uint64_t image);
    int fz_image_is_imagemask(uint64_t ctx, uint64_t image);
    uint64_t fz_image_colorspace(uint64_t ctx, uint64_t image);
    uint64_t fz_image_mask(uint64_t ctx, uint64_t image);
    uint64_t fz_get_pixmap_from_image(uint64_t ctx, uint64_t image, fz_irect* subarea, fz_matrix* ctm, int* w, int* h);
    uint64_t fz_get_unscaled_pixmap_from_image(uint64_t ctx, uint64_t image);
    size_t fz_image_size(uint64_t ctx, uint64_t image);
    uint64_t fz_compressed_image_buffer(uint64_t ctx, uint64_t image);
    void fz_set_compressed_image_buffer(uint64_t ctx, uint64_t image, uint64_t buf);
    uint64_t fz_get_compressed_image_type(uint64_t ctx, uint64_t image);
    void fz_drop_image_base(uint64_t ctx, uint64_t image);
    
    // ============================================================================
    // STREAM FUNCTIONS (29)
    // ============================================================================
    
    uint64_t fz_open_file(uint64_t ctx, const char* filename);
    uint64_t fz_open_file_ptr_no_close(uint64_t ctx, void* file);
    uint64_t fz_open_memory(uint64_t ctx, const unsigned char* data, size_t len);
    uint64_t fz_open_buffer(uint64_t ctx, uint64_t buf);
    void fz_drop_stream(uint64_t ctx, uint64_t stm);
    uint64_t fz_keep_stream(uint64_t ctx, uint64_t stm);
    size_t fz_read(uint64_t ctx, uint64_t stm, unsigned char* data, size_t len);
    size_t fz_skip(uint64_t ctx, uint64_t stm, size_t len);
    int fz_read_byte(uint64_t ctx, uint64_t stm);
    int fz_peek_byte(uint64_t ctx, uint64_t stm);
    void fz_unread_byte(uint64_t ctx, uint64_t stm);
    int fz_is_eof(uint64_t ctx, uint64_t stm);
    int fz_is_eof_bits(uint64_t ctx, uint64_t stm);
    void fz_sync_bits(uint64_t ctx, uint64_t stm);
    unsigned int fz_read_bits(uint64_t ctx, uint64_t stm, int n);
    unsigned int fz_read_rbits(uint64_t ctx, uint64_t stm, int n);
    void fz_seek(uint64_t ctx, uint64_t stm, int64_t offset, int whence);
    int64_t fz_tell(uint64_t ctx, uint64_t stm);
    size_t fz_available(uint64_t ctx, uint64_t stm, size_t max);
    uint64_t fz_read_all(uint64_t ctx, uint64_t stm, size_t initial);
    char* fz_read_line(uint64_t ctx, uint64_t stm, char* buf, size_t max);
    int64_t fz_stream_meta(uint64_t ctx, uint64_t stm, int key, int size, void* ptr);
    void fz_seek_stream(uint64_t ctx, uint64_t stm, int64_t offset, int whence);
    int fz_stream_sanity_check(uint64_t ctx, uint64_t stm);
    void fz_deflate_bound(uint64_t ctx, size_t size, size_t* out);
    size_t fz_deflate(uint64_t ctx, unsigned char* dest, size_t* destLen, const unsigned char* source, size_t sourceLen, int level);
    uint64_t fz_open_deflated(uint64_t ctx, uint64_t chain, int zip_compatible);
    uint64_t fz_open_dctd(uint64_t ctx, uint64_t chain, int color_transform, int l2factor, uint64_t jpegtables);
    uint64_t fz_open_faxd(uint64_t ctx, uint64_t chain, int k, int end_of_line, int encoded_byte_align, int columns, int rows, int end_of_block, int black_is_1);
    
    // ============================================================================
    // OUTPUT FUNCTIONS (34)
    // ============================================================================
    
    uint64_t fz_new_output_with_path(uint64_t ctx, const char* filename, int append);
    uint64_t fz_new_output_with_buffer(uint64_t ctx, uint64_t buf);
    uint64_t fz_stdout(uint64_t ctx);
    uint64_t fz_stderr(uint64_t ctx);
    void fz_drop_output(uint64_t ctx, uint64_t out);
    void fz_seek_output(uint64_t ctx, uint64_t out, int64_t off, int whence);
    int64_t fz_tell_output(uint64_t ctx, uint64_t out);
    void fz_write_data(uint64_t ctx, uint64_t out, const void* data, size_t size);
    void fz_write_string(uint64_t ctx, uint64_t out, const char* s);
    void fz_write_int32_be(uint64_t ctx, uint64_t out, int x);
    void fz_write_int32_le(uint64_t ctx, uint64_t out, int x);
    void fz_write_int16_be(uint64_t ctx, uint64_t out, int x);
    void fz_write_int16_le(uint64_t ctx, uint64_t out, int x);
    void fz_write_byte(uint64_t ctx, uint64_t out, unsigned char byte);
    void fz_write_rune(uint64_t ctx, uint64_t out, int rune);
    void fz_write_base64(uint64_t ctx, uint64_t out, const unsigned char* data, size_t size, int newline);
    void fz_write_base64_buffer(uint64_t ctx, uint64_t out, uint64_t buf, int newline);
    void fz_write_float(uint64_t ctx, uint64_t out, float f);
    void fz_write_printf(uint64_t ctx, uint64_t out, const char* fmt, ...);
    void fz_write_pdf_string(uint64_t ctx, uint64_t out, const char* text);
    void fz_write_ps_string(uint64_t ctx, uint64_t out, const char* text);
    void fz_write_vprintf(uint64_t ctx, uint64_t out, const char* fmt, void* args);
    void fz_flush_output(uint64_t ctx, uint64_t out);
    void fz_close_output(uint64_t ctx, uint64_t out);
    void fz_save_pixmap_as_png(uint64_t ctx, uint64_t pix, const char* path);
    void fz_save_pixmap_as_pnm(uint64_t ctx, uint64_t pix, const char* path);
    void fz_save_pixmap_as_pam(uint64_t ctx, uint64_t pix, const char* path);
    void fz_save_pixmap_as_pbm(uint64_t ctx, uint64_t pix, const char* path);
    void fz_save_pixmap_as_pkm(uint64_t ctx, uint64_t pix, const char* path);
    void fz_save_pixmap_as_tga(uint64_t ctx, uint64_t pix, const char* path);
    void fz_save_pixmap_as_pwg(uint64_t ctx, uint64_t pix, const char* path, uint64_t pwg);
    void fz_save_pixmap_as_psd(uint64_t ctx, uint64_t pix, const char* path);
    void fz_save_pixmap_as_jpeg(uint64_t ctx, uint64_t pix, const char* path, int quality);
    void fz_write_pixmap_as_png(uint64_t ctx, uint64_t out, uint64_t pix);

    // ============================================================================
    // TEXT EXTRACTION - STEXT FUNCTIONS (37)
    // ============================================================================
    
    uint64_t fz_new_stext_page(uint64_t ctx, fz_rect mediabox);
    void fz_drop_stext_page(uint64_t ctx, uint64_t page);
    uint64_t fz_new_stext_page_from_page(uint64_t ctx, uint64_t page, uint64_t options);
    uint64_t fz_new_stext_device(uint64_t ctx, uint64_t page, uint64_t options);
    int fz_search_stext_page(uint64_t ctx, uint64_t page, const char* needle, int* hit_mark, fz_quad* hit_bbox, int hit_max);
    fz_rect fz_stext_page_mediabox(uint64_t ctx, uint64_t page);
    int fz_stext_page_block_count(uint64_t ctx, uint64_t page);
    uint64_t fz_stext_page_get_block(uint64_t ctx, uint64_t page, int idx);
    int fz_stext_block_type(uint64_t ctx, uint64_t block);
    fz_rect fz_stext_block_bbox(uint64_t ctx, uint64_t block);
    int fz_stext_block_line_count(uint64_t ctx, uint64_t block);
    uint64_t fz_stext_block_get_line(uint64_t ctx, uint64_t block, int idx);
    fz_rect fz_stext_line_bbox(uint64_t ctx, uint64_t line);
    int fz_stext_line_wmode(uint64_t ctx, uint64_t line);
    fz_point fz_stext_line_dir(uint64_t ctx, uint64_t line);
    int fz_stext_line_char_count(uint64_t ctx, uint64_t line);
    uint64_t fz_stext_line_get_char(uint64_t ctx, uint64_t line, int idx);
    int fz_stext_char_c(uint64_t ctx, uint64_t ch);
    fz_point fz_stext_char_origin(uint64_t ctx, uint64_t ch);
    fz_quad fz_stext_char_quad(uint64_t ctx, uint64_t ch);
    float fz_stext_char_size(uint64_t ctx, uint64_t ch);
    uint64_t fz_stext_char_font(uint64_t ctx, uint64_t ch);
    char* fz_copy_selection(uint64_t ctx, uint64_t page, fz_point a, fz_point b, int crlf);
    char* fz_copy_rectangle(uint64_t ctx, uint64_t page, fz_rect r, int crlf);
    int fz_highlight_selection(uint64_t ctx, uint64_t page, fz_point a, fz_point b, fz_quad* quads, int max_quads);
    void fz_print_stext_page_as_html(uint64_t ctx, uint64_t out, uint64_t page, int id);
    void fz_print_stext_page_as_xhtml(uint64_t ctx, uint64_t out, uint64_t page, int id);
    void fz_print_stext_page_as_xml(uint64_t ctx, uint64_t out, uint64_t page, int id);
    void fz_print_stext_page_as_json(uint64_t ctx, uint64_t out, uint64_t page, float scale);
    void fz_print_stext_page_as_text(uint64_t ctx, uint64_t out, uint64_t page);
    void fz_print_stext_header_as_html(uint64_t ctx, uint64_t out);
    void fz_print_stext_trailer_as_html(uint64_t ctx, uint64_t out);
    void fz_print_stext_header_as_xhtml(uint64_t ctx, uint64_t out);
    void fz_print_stext_trailer_as_xhtml(uint64_t ctx, uint64_t out);
    char* fz_stext_get_text(uint64_t ctx, uint64_t page);
    void fz_add_stext_block(uint64_t ctx, uint64_t page, int type, fz_rect bbox);
    void fz_add_stext_char(uint64_t ctx, uint64_t page, uint64_t font, float size, int wmode, int c, fz_point origin, fz_quad quad);
    
    // ============================================================================
    // LINK FUNCTIONS (23)
    // ============================================================================
    
    uint64_t fz_load_links(uint64_t ctx, uint64_t page);
    void fz_drop_link(uint64_t ctx, uint64_t link);
    uint64_t fz_keep_link(uint64_t ctx, uint64_t link);
    fz_rect fz_link_rect(uint64_t ctx, uint64_t link);
    const char* fz_link_uri(uint64_t ctx, uint64_t link);
    uint64_t fz_link_next(uint64_t ctx, uint64_t link);
    int fz_is_external_link(uint64_t ctx, const char* uri);
    int fz_is_page_link(uint64_t ctx, const char* uri);
    uint64_t fz_new_link(uint64_t ctx, fz_rect rect, const char* uri);
    void fz_set_link_rect(uint64_t ctx, uint64_t link, fz_rect rect);
    void fz_set_link_uri(uint64_t ctx, uint64_t link, const char* uri);
    uint64_t fz_new_link_of_size(uint64_t ctx, int size, fz_rect rect, const char* uri);
    
    // ============================================================================
    // OUTLINE FUNCTIONS (38)
    // ============================================================================
    
    void fz_drop_outline(uint64_t ctx, uint64_t outline);
    uint64_t fz_keep_outline(uint64_t ctx, uint64_t outline);
    const char* fz_outline_title(uint64_t ctx, uint64_t outline);
    const char* fz_outline_uri(uint64_t ctx, uint64_t outline);
    int fz_outline_page(uint64_t ctx, uint64_t outline, uint64_t doc);
    int fz_outline_is_open(uint64_t ctx, uint64_t outline);
    uint64_t fz_outline_down(uint64_t ctx, uint64_t outline);
    uint64_t fz_outline_next(uint64_t ctx, uint64_t outline);
    void fz_set_outline_title(uint64_t ctx, uint64_t outline, const char* title);
    void fz_set_outline_uri(uint64_t ctx, uint64_t outline, const char* uri);
    void fz_set_outline_is_open(uint64_t ctx, uint64_t outline, int is_open);
    uint64_t fz_new_outline(uint64_t ctx);
    void fz_outline_insert_child(uint64_t ctx, uint64_t parent, uint64_t child);
    void fz_outline_insert_sibling(uint64_t ctx, uint64_t sibling, uint64_t outline);
    void fz_outline_remove_child(uint64_t ctx, uint64_t parent, uint64_t child);
    uint64_t fz_outline_parent(uint64_t ctx, uint64_t outline);
    int fz_outline_count(uint64_t ctx, uint64_t outline);
    uint64_t fz_outline_get_child(uint64_t ctx, uint64_t outline, int i);
    int fz_outline_iterator_item(uint64_t ctx, uint64_t iter);
    const char* fz_outline_iterator_title(uint64_t ctx, uint64_t iter);
    const char* fz_outline_iterator_uri(uint64_t ctx, uint64_t iter);
    int fz_outline_iterator_is_open(uint64_t ctx, uint64_t iter);
    int fz_outline_iterator_down(uint64_t ctx, uint64_t iter);
    int fz_outline_iterator_up(uint64_t ctx, uint64_t iter);
    int fz_outline_iterator_next(uint64_t ctx, uint64_t iter);
    int fz_outline_iterator_prev(uint64_t ctx, uint64_t iter);
    int fz_outline_iterator_insert(uint64_t ctx, uint64_t iter, const char* title, const char* uri, int is_open);
    int fz_outline_iterator_delete(uint64_t ctx, uint64_t iter);
    int fz_outline_iterator_update(uint64_t ctx, uint64_t iter, const char* title, const char* uri, int is_open);
    uint64_t fz_new_outline_iterator(uint64_t ctx, uint64_t doc);
    void fz_drop_outline_iterator(uint64_t ctx, uint64_t iter);
    
    // ============================================================================
    // PATH FUNCTIONS (35)
    // ============================================================================
    
    uint64_t fz_new_path(uint64_t ctx);
    void fz_drop_path(uint64_t ctx, uint64_t path);
    uint64_t fz_keep_path(uint64_t ctx, uint64_t path);
    void fz_moveto(uint64_t ctx, uint64_t path, float x, float y);
    void fz_lineto(uint64_t ctx, uint64_t path, float x, float y);
    void fz_curveto(uint64_t ctx, uint64_t path, float x1, float y1, float x2, float y2, float x3, float y3);
    void fz_curvetov(uint64_t ctx, uint64_t path, float x2, float y2, float x3, float y3);
    void fz_curvetoy(uint64_t ctx, uint64_t path, float x1, float y1, float x3, float y3);
    void fz_closepath(uint64_t ctx, uint64_t path);
    void fz_rectto(uint64_t ctx, uint64_t path, float x1, float y1, float x2, float y2);
    void fz_transform_path(uint64_t ctx, uint64_t path, fz_matrix ctm);
    fz_rect fz_bound_path(uint64_t ctx, uint64_t path, uint64_t stroke, fz_matrix ctm);
    uint64_t fz_clone_path(uint64_t ctx, uint64_t path);
    uint64_t fz_trim_path(uint64_t ctx, uint64_t path);
    int fz_path_packed(uint64_t ctx, uint64_t path);
    int fz_path_current_point(uint64_t ctx, uint64_t path, fz_point* p);
    void fz_quadto(uint64_t ctx, uint64_t path, float x1, float y1, float x2, float y2);
    int fz_count_path_points(uint64_t ctx, uint64_t path);
    int fz_path_cmds_count(uint64_t ctx, uint64_t path);
    int fz_path_coords_count(uint64_t ctx, uint64_t path);
    void fz_enumerate_path(uint64_t ctx, uint64_t path, void* user, void* moveto, void* lineto, void* curveto, void* closepath);
    void fz_walk_path(uint64_t ctx, uint64_t path, uint64_t walker, void* arg);
    uint64_t fz_new_stroke_state(uint64_t ctx);
    uint64_t fz_new_stroke_state_with_dash_len(uint64_t ctx, int len);
    void fz_drop_stroke_state(uint64_t ctx, uint64_t stroke);
    uint64_t fz_keep_stroke_state(uint64_t ctx, uint64_t stroke);
    uint64_t fz_unshare_stroke_state(uint64_t ctx, uint64_t stroke);
    uint64_t fz_unshare_stroke_state_with_dash_len(uint64_t ctx, uint64_t stroke, int len);
    uint64_t fz_clone_stroke_state(uint64_t ctx, uint64_t stroke);
    
    // ============================================================================
    // DEVICE FUNCTIONS (30)
    // ============================================================================
    
    void fz_drop_device(uint64_t ctx, uint64_t dev);
    uint64_t fz_keep_device(uint64_t ctx, uint64_t dev);
    void fz_close_device(uint64_t ctx, uint64_t dev);
    void fz_enable_device_hints(uint64_t ctx, uint64_t dev, int hints);
    void fz_disable_device_hints(uint64_t ctx, uint64_t dev, int hints);
    int fz_device_current_scissor(uint64_t ctx, uint64_t dev, fz_rect* r);
    void fz_fill_path(uint64_t ctx, uint64_t dev, uint64_t path, int even_odd, fz_matrix ctm, uint64_t colorspace, const float* color, float alpha, uint64_t color_params);
    void fz_stroke_path(uint64_t ctx, uint64_t dev, uint64_t path, uint64_t stroke, fz_matrix ctm, uint64_t colorspace, const float* color, float alpha, uint64_t color_params);
    void fz_clip_path(uint64_t ctx, uint64_t dev, uint64_t path, int even_odd, fz_matrix ctm, fz_rect scissor);
    void fz_clip_stroke_path(uint64_t ctx, uint64_t dev, uint64_t path, uint64_t stroke, fz_matrix ctm, fz_rect scissor);
    void fz_fill_text(uint64_t ctx, uint64_t dev, uint64_t text, fz_matrix ctm, uint64_t colorspace, const float* color, float alpha, uint64_t color_params);
    void fz_stroke_text(uint64_t ctx, uint64_t dev, uint64_t text, uint64_t stroke, fz_matrix ctm, uint64_t colorspace, const float* color, float alpha, uint64_t color_params);
    void fz_clip_text(uint64_t ctx, uint64_t dev, uint64_t text, fz_matrix ctm, fz_rect scissor);
    void fz_clip_stroke_text(uint64_t ctx, uint64_t dev, uint64_t text, uint64_t stroke, fz_matrix ctm, fz_rect scissor);
    void fz_ignore_text(uint64_t ctx, uint64_t dev, uint64_t text, fz_matrix ctm);
    void fz_fill_shade(uint64_t ctx, uint64_t dev, uint64_t shade, fz_matrix ctm, float alpha, uint64_t color_params);
    void fz_fill_image(uint64_t ctx, uint64_t dev, uint64_t image, fz_matrix ctm, float alpha, uint64_t color_params);
    void fz_fill_image_mask(uint64_t ctx, uint64_t dev, uint64_t image, fz_matrix ctm, uint64_t colorspace, const float* color, float alpha, uint64_t color_params);
    void fz_clip_image_mask(uint64_t ctx, uint64_t dev, uint64_t image, fz_matrix ctm, fz_rect scissor);
    void fz_pop_clip(uint64_t ctx, uint64_t dev);
    void fz_begin_mask(uint64_t ctx, uint64_t dev, fz_rect area, int luminosity, uint64_t colorspace, const float* bc, uint64_t color_params);
    void fz_end_mask(uint64_t ctx, uint64_t dev);
    void fz_begin_group(uint64_t ctx, uint64_t dev, fz_rect area, uint64_t colorspace, int isolated, int knockout, int blendmode, float alpha);
    void fz_end_group(uint64_t ctx, uint64_t dev);
    void fz_begin_tile(uint64_t ctx, uint64_t dev, fz_rect area, fz_rect view, float xstep, float ystep, fz_matrix ctm);
    int fz_begin_tile_id(uint64_t ctx, uint64_t dev, fz_rect area, fz_rect view, float xstep, float ystep, fz_matrix ctm, int id);
    void fz_end_tile(uint64_t ctx, uint64_t dev);
    void fz_render_flags(uint64_t ctx, uint64_t dev, int set, int clear);
    void fz_set_default_colorspaces(uint64_t ctx, uint64_t dev, uint64_t default_cs);
    void fz_begin_layer(uint64_t ctx, uint64_t dev, const char* layer_name);
    
    // ============================================================================
    // GEOMETRY FUNCTIONS (58)
    // ============================================================================
    
    fz_matrix fz_identity_matrix(void);
    fz_matrix fz_scale(float sx, float sy);
    fz_matrix fz_shear(float sx, float sy);
    fz_matrix fz_rotate(float degrees);
    fz_matrix fz_translate(float tx, float ty);
    fz_matrix fz_concat(fz_matrix one, fz_matrix two);
    fz_matrix fz_pre_scale(fz_matrix m, float sx, float sy);
    fz_matrix fz_pre_shear(fz_matrix m, float sx, float sy);
    fz_matrix fz_pre_rotate(fz_matrix m, float degrees);
    fz_matrix fz_pre_translate(fz_matrix m, float tx, float ty);
    fz_matrix fz_post_scale(fz_matrix m, float sx, float sy);
    fz_matrix fz_invert_matrix(fz_matrix m);
    int fz_try_invert_matrix(fz_matrix* inv, fz_matrix m);
    int fz_is_identity(fz_matrix m);
    int fz_is_rectilinear(fz_matrix m);
    float fz_matrix_expansion(fz_matrix m);
    float fz_matrix_max_expansion(fz_matrix m);
    fz_point fz_transform_point(fz_point p, fz_matrix m);
    fz_point fz_transform_vector(fz_point p, fz_matrix m);
    fz_rect fz_transform_rect(fz_rect r, fz_matrix m);
    fz_rect fz_make_rect(float x0, float y0, float x1, float y1);
    fz_irect fz_make_irect(int x0, int y0, int x1, int y1);
    fz_point fz_make_point(float x, float y);
    fz_matrix fz_make_matrix(float a, float b, float c, float d, float e, float f);
    int fz_is_empty_rect(fz_rect r);
    int fz_is_infinite_rect(fz_rect r);
    int fz_is_empty_irect(fz_irect r);
    int fz_is_infinite_irect(fz_irect r);
    fz_rect fz_infinite_rect(void);
    fz_irect fz_infinite_irect(void);
    fz_rect fz_empty_rect(void);
    fz_irect fz_empty_irect(void);
    fz_rect fz_unit_rect(void);
    fz_rect fz_intersect_rect(fz_rect a, fz_rect b);
    fz_irect fz_intersect_irect(fz_irect a, fz_irect b);
    fz_rect fz_union_rect(fz_rect a, fz_rect b);
    fz_rect fz_expand_rect(fz_rect r, float expand);
    fz_rect fz_include_point_in_rect(fz_rect r, fz_point p);
    fz_rect fz_translate_rect(fz_rect r, float x, float y);
    int fz_contains_rect(fz_rect a, fz_rect b);
    fz_irect fz_irect_from_rect(fz_rect r);
    fz_irect fz_round_rect(fz_rect r);
    fz_rect fz_rect_from_irect(fz_irect r);
    fz_rect fz_rect_from_quad(fz_quad q);
    fz_quad fz_quad_from_rect(fz_rect r);
    fz_quad fz_transform_quad(fz_quad q, fz_matrix m);
    int fz_is_point_inside_rect(fz_point p, fz_rect r);
    int fz_is_point_inside_irect(int x, int y, fz_irect r);
    int fz_is_point_inside_quad(fz_point p, fz_quad q);
    float fz_quad_area(fz_quad q);
    fz_quad fz_make_quad(float ulx, float uly, float urx, float ury, float llx, float lly, float lrx, float lry);
    float fz_rect_width(fz_rect r);
    float fz_rect_height(fz_rect r);
    float fz_normalize_vector(fz_point* p);
    float fz_distance_point_to_rect(fz_point p, fz_rect r);
    float fz_distance_point_to_point(fz_point p1, fz_point p2);
    float fz_abs(float f);
    float fz_min(float a, float b);
    float fz_max(float a, float b);
    
    // ============================================================================
    // PDF-SPECIFIC FUNCTIONS (Selected - 100+)
    // ============================================================================
    
    // PDF Document
    uint64_t pdf_open_document(uint64_t ctx, const char* filename);
    uint64_t pdf_open_document_with_stream(uint64_t ctx, uint64_t stm);
    void pdf_drop_document(uint64_t ctx, uint64_t doc);
    void pdf_save_document(uint64_t ctx, uint64_t doc, const char* filename, uint64_t opts);
    int pdf_count_pages(uint64_t ctx, uint64_t doc);
    uint64_t pdf_load_page(uint64_t ctx, uint64_t doc, int page_num);
    uint64_t pdf_page_contents(uint64_t ctx, uint64_t page);
    fz_rect pdf_bound_page(uint64_t ctx, uint64_t page);
    void pdf_drop_page(uint64_t ctx, uint64_t page);
    
    // PDF Objects
    uint64_t pdf_new_null(uint64_t ctx, uint64_t doc);
    uint64_t pdf_new_bool(uint64_t ctx, uint64_t doc, int b);
    uint64_t pdf_new_int(uint64_t ctx, uint64_t doc, int64_t i);
    uint64_t pdf_new_real(uint64_t ctx, uint64_t doc, float f);
    uint64_t pdf_new_string(uint64_t ctx, uint64_t doc, const char* s, size_t n);
    uint64_t pdf_new_text_string(uint64_t ctx, uint64_t doc, const char* s);
    uint64_t pdf_new_name(uint64_t ctx, uint64_t doc, const char* name);
    uint64_t pdf_new_indirect(uint64_t ctx, uint64_t doc, int num, int gen);
    uint64_t pdf_new_array(uint64_t ctx, uint64_t doc, int initialcap);
    uint64_t pdf_new_dict(uint64_t ctx, uint64_t doc, int initialcap);
    uint64_t pdf_copy_array(uint64_t ctx, uint64_t doc, uint64_t array);
    uint64_t pdf_copy_dict(uint64_t ctx, uint64_t doc, uint64_t dict);
    uint64_t pdf_deep_copy_obj(uint64_t ctx, uint64_t obj);
    void pdf_drop_obj(uint64_t ctx, uint64_t obj);
    uint64_t pdf_keep_obj(uint64_t ctx, uint64_t obj);
    
    // Object Type Checking
    int pdf_is_null(uint64_t ctx, uint64_t obj);
    int pdf_is_bool(uint64_t ctx, uint64_t obj);
    int pdf_is_int(uint64_t ctx, uint64_t obj);
    int pdf_is_real(uint64_t ctx, uint64_t obj);
    int pdf_is_number(uint64_t ctx, uint64_t obj);
    int pdf_is_name(uint64_t ctx, uint64_t obj);
    int pdf_is_string(uint64_t ctx, uint64_t obj);
    int pdf_is_array(uint64_t ctx, uint64_t obj);
    int pdf_is_dict(uint64_t ctx, uint64_t obj);
    int pdf_is_indirect(uint64_t ctx, uint64_t obj);
    int pdf_is_stream(uint64_t ctx, uint64_t obj);
    
    // Object Value Extraction
    int pdf_to_bool(uint64_t ctx, uint64_t obj);
    int64_t pdf_to_int(uint64_t ctx, uint64_t obj);
    float pdf_to_real(uint64_t ctx, uint64_t obj);
    const char* pdf_to_name(uint64_t ctx, uint64_t obj);
    const char* pdf_to_text_string(uint64_t ctx, uint64_t obj);
    const char* pdf_to_string(uint64_t ctx, uint64_t obj, size_t* len);
    int pdf_to_num(uint64_t ctx, uint64_t obj);
    int pdf_to_gen(uint64_t ctx, uint64_t obj);
    
    // Array Operations
    int pdf_array_len(uint64_t ctx, uint64_t array);
    uint64_t pdf_array_get(uint64_t ctx, uint64_t array, int i);
    void pdf_array_put(uint64_t ctx, uint64_t array, int i, uint64_t obj);
    void pdf_array_push(uint64_t ctx, uint64_t array, uint64_t obj);
    void pdf_array_insert(uint64_t ctx, uint64_t array, int i, uint64_t obj);
    void pdf_array_delete(uint64_t ctx, uint64_t array, int i);
    int pdf_array_contains(uint64_t ctx, uint64_t array, uint64_t obj);
    int pdf_array_find(uint64_t ctx, uint64_t array, uint64_t obj);
    void pdf_array_push_int(uint64_t ctx, uint64_t array, int64_t i);
    void pdf_array_push_real(uint64_t ctx, uint64_t array, float f);
    void pdf_array_push_bool(uint64_t ctx, uint64_t array, int b);
    void pdf_array_push_name(uint64_t ctx, uint64_t array, const char* name);
    void pdf_array_push_string(uint64_t ctx, uint64_t array, const char* s, size_t n);
    void pdf_array_push_text_string(uint64_t ctx, uint64_t array, const char* s);
    
    // Dictionary Operations
    int pdf_dict_len(uint64_t ctx, uint64_t dict);
    uint64_t pdf_dict_get_key(uint64_t ctx, uint64_t dict, int i);
    uint64_t pdf_dict_get_val(uint64_t ctx, uint64_t dict, int i);
    uint64_t pdf_dict_get(uint64_t ctx, uint64_t dict, uint64_t key);
    uint64_t pdf_dict_gets(uint64_t ctx, uint64_t dict, const char* key);
    uint64_t pdf_dict_getp(uint64_t ctx, uint64_t dict, const char* path);
    void pdf_dict_put(uint64_t ctx, uint64_t dict, uint64_t key, uint64_t val);
    void pdf_dict_puts(uint64_t ctx, uint64_t dict, const char* key, uint64_t val);
    void pdf_dict_putp(uint64_t ctx, uint64_t dict, const char* path, uint64_t val);
    void pdf_dict_del(uint64_t ctx, uint64_t dict, uint64_t key);
    void pdf_dict_dels(uint64_t ctx, uint64_t dict, const char* key);
    void pdf_dict_put_bool(uint64_t ctx, uint64_t dict, uint64_t key, int b);
    void pdf_dict_put_int(uint64_t ctx, uint64_t dict, uint64_t key, int64_t i);
    void pdf_dict_put_real(uint64_t ctx, uint64_t dict, uint64_t key, float f);
    void pdf_dict_put_name(uint64_t ctx, uint64_t dict, uint64_t key, const char* name);
    void pdf_dict_put_string(uint64_t ctx, uint64_t dict, uint64_t key, const char* s, size_t n);
    void pdf_dict_put_text_string(uint64_t ctx, uint64_t dict, uint64_t key, const char* s);
    void pdf_dict_put_rect(uint64_t ctx, uint64_t dict, uint64_t key, fz_rect rect);
    void pdf_dict_put_matrix(uint64_t ctx, uint64_t dict, uint64_t key, fz_matrix mtx);
    int pdf_dict_get_bool(uint64_t ctx, uint64_t dict, uint64_t key);
    int64_t pdf_dict_get_int(uint64_t ctx, uint64_t dict, uint64_t key);
    float pdf_dict_get_real(uint64_t ctx, uint64_t dict, uint64_t key);
    const char* pdf_dict_get_name(uint64_t ctx, uint64_t dict, uint64_t key);
    const char* pdf_dict_get_string(uint64_t ctx, uint64_t dict, uint64_t key, size_t* sizep);
    const char* pdf_dict_get_text_string(uint64_t ctx, uint64_t dict, uint64_t key);
    fz_rect pdf_dict_get_rect(uint64_t ctx, uint64_t dict, uint64_t key);
    fz_matrix pdf_dict_get_matrix(uint64_t ctx, uint64_t dict, uint64_t key);
    
    // PDF Page Operations
    uint64_t pdf_new_page(uint64_t ctx, uint64_t doc, int page_no, fz_rect mediabox, int rotate, uint64_t resources, uint64_t contents);
    void pdf_insert_page(uint64_t ctx, uint64_t doc, int page_no, uint64_t page);
    void pdf_delete_page(uint64_t ctx, uint64_t doc, int page_no);
    void pdf_delete_page_range(uint64_t ctx, uint64_t doc, int start, int end);
    
    // PDF Annotations
    uint64_t pdf_first_annot(uint64_t ctx, uint64_t page);
    uint64_t pdf_next_annot(uint64_t ctx, uint64_t annot);
    int pdf_annot_type(uint64_t ctx, uint64_t annot);
    fz_rect pdf_annot_rect(uint64_t ctx, uint64_t annot);
    void pdf_set_annot_rect(uint64_t ctx, uint64_t annot, fz_rect rect);
    const char* pdf_annot_contents(uint64_t ctx, uint64_t annot);
    void pdf_set_annot_contents(uint64_t ctx, uint64_t annot, const char* text);
    uint64_t pdf_create_annot(uint64_t ctx, uint64_t page, int type);
    void pdf_delete_annot(uint64_t ctx, uint64_t page, uint64_t annot);
    void pdf_update_annot(uint64_t ctx, uint64_t annot);
    int pdf_annot_has_open(uint64_t ctx, uint64_t annot);
    int pdf_annot_is_open(uint64_t ctx, uint64_t annot);
    void pdf_set_annot_is_open(uint64_t ctx, uint64_t annot, int is_open);
    void pdf_annot_color(uint64_t ctx, uint64_t annot, int* n, float* color);
    void pdf_set_annot_color(uint64_t ctx, uint64_t annot, int n, const float* color);
    void pdf_annot_interior_color(uint64_t ctx, uint64_t annot, int* n, float* color);
    void pdf_set_annot_interior_color(uint64_t ctx, uint64_t annot, int n, const float* color);
    float pdf_annot_border(uint64_t ctx, uint64_t annot);
    void pdf_set_annot_border(uint64_t ctx, uint64_t annot, float w);
    int pdf_annot_quadding(uint64_t ctx, uint64_t annot);
    void pdf_set_annot_quadding(uint64_t ctx, uint64_t annot, int q);
    float pdf_annot_opacity(uint64_t ctx, uint64_t annot);
    void pdf_set_annot_opacity(uint64_t ctx, uint64_t annot, float opacity);
    
    // PDF Forms / Interactive Elements
    uint64_t pdf_first_widget(uint64_t ctx, uint64_t page);
    uint64_t pdf_next_widget(uint64_t ctx, uint64_t widget);
    int pdf_widget_type(uint64_t ctx, uint64_t widget);
    fz_rect pdf_widget_rect(uint64_t ctx, uint64_t widget);
    int pdf_text_widget_max_len(uint64_t ctx, uint64_t widget);
    const char* pdf_text_widget_value(uint64_t ctx, uint64_t widget);
    int pdf_text_widget_set_value(uint64_t ctx, uint64_t widget, const char* value);
    int pdf_choice_widget_options(uint64_t ctx, uint64_t widget, int exportval, const char** opts);
    int pdf_choice_widget_is_multiselect(uint64_t ctx, uint64_t widget);
    int pdf_choice_widget_value(uint64_t ctx, uint64_t widget, const char** vals);
    void pdf_choice_widget_set_value(uint64_t ctx, uint64_t widget, int n, const char** vals);
    int pdf_toggle_widget(uint64_t ctx, uint64_t widget);
    
    // PDF Signatures
    int pdf_signature_is_signed(uint64_t ctx, uint64_t doc, uint64_t field);
    void pdf_sign_signature(uint64_t ctx, uint64_t widget, uint64_t signer);
    void pdf_clear_signature(uint64_t ctx, uint64_t widget);
    int pdf_check_signature(uint64_t ctx, uint64_t widget);
    uint64_t pdf_signature_error_description(int err);
    int pdf_count_signatures(uint64_t ctx, uint64_t doc);
    
    // PDF Metadata
    const char* pdf_metadata(uint64_t ctx, uint64_t doc, const char* key);
    void pdf_set_metadata(uint64_t ctx, uint64_t doc, const char* key, const char* value);
    uint64_t pdf_trailer(uint64_t ctx, uint64_t doc);
    uint64_t pdf_catalog(uint64_t ctx, uint64_t doc);
    int pdf_version(uint64_t ctx, uint64_t doc);
    
    // PDF Creation/Modification
    uint64_t pdf_add_object(uint64_t ctx, uint64_t doc, uint64_t obj);
    uint64_t pdf_add_object_drop(uint64_t ctx, uint64_t doc, uint64_t obj);
    void pdf_update_object(uint64_t ctx, uint64_t doc, int num, uint64_t obj);
    void pdf_delete_object(uint64_t ctx, uint64_t doc, int num);
    uint64_t pdf_add_stream(uint64_t ctx, uint64_t doc, uint64_t buf, uint64_t obj, int compressed);
    void pdf_update_stream(uint64_t ctx, uint64_t doc, uint64_t ref, uint64_t buf, int compressed);
    uint64_t pdf_load_stream(uint64_t ctx, uint64_t ref);
    uint64_t pdf_load_stream_number(uint64_t ctx, uint64_t doc, int num);
    
    // PDF Resources
    uint64_t pdf_add_simple_font(uint64_t ctx, uint64_t doc, uint64_t font, int encoding);
    uint64_t pdf_add_cjk_font(uint64_t ctx, uint64_t doc, uint64_t font, int ordering, int wmode, int serif);
    uint64_t pdf_add_cid_font(uint64_t ctx, uint64_t doc, uint64_t font);
    uint64_t pdf_add_image(uint64_t ctx, uint64_t doc, uint64_t image);
    
    // PDF Write Options
    uint64_t pdf_write_options_new(uint64_t ctx);
    void pdf_write_options_drop(uint64_t ctx, uint64_t opts);
    void pdf_write_options_set_incremental(uint64_t ctx, uint64_t opts, int incremental);
    void pdf_write_options_set_pretty(uint64_t ctx, uint64_t opts, int pretty);
    void pdf_write_options_set_ascii(uint64_t ctx, uint64_t opts, int ascii);
    void pdf_write_options_set_compress(uint64_t ctx, uint64_t opts, int compress);
    void pdf_write_options_set_compress_images(uint64_t ctx, uint64_t opts, int compress_images);
    void pdf_write_options_set_compress_fonts(uint64_t ctx, uint64_t opts, int compress_fonts);
    void pdf_write_options_set_decompress(uint64_t ctx, uint64_t opts, int decompress);
    void pdf_write_options_set_garbage(uint64_t ctx, uint64_t opts, int garbage);
    void pdf_write_options_set_linear(uint64_t ctx, uint64_t opts, int linear);
    void pdf_write_options_set_clean(uint64_t ctx, uint64_t opts, int clean);
    void pdf_write_options_set_sanitize(uint64_t ctx, uint64_t opts, int sanitize);
    void pdf_write_options_set_encryption(uint64_t ctx, uint64_t opts, int encryption);
    void pdf_write_options_set_permissions(uint64_t ctx, uint64_t opts, int permissions);
    void pdf_write_options_set_owner_password(uint64_t ctx, uint64_t opts, const char* pwd);
    void pdf_write_options_set_user_password(uint64_t ctx, uint64_t opts, const char* pwd);
"""

__all__ = ["FULL_FFI_DEFS"]
